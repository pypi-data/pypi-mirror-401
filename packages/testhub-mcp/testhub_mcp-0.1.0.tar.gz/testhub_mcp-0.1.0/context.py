"""
MCP 上下文管理

提供会话上下文的持久化存储，支持：
- 当前任务追踪
- 对话 ID 管理
- 会话状态保存
- 进度日志追踪
- 智能建议生成
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger

if TYPE_CHECKING:
    from .api_client import TestHubAPIClient


class ProgressLogType(str, Enum):
    """进度日志类型"""
    CODE_CHANGE = "code_change"      # 代码变更
    PROBLEM_SOLVED = "problem_solved"  # 问题已解决
    BLOCKER = "blocker"              # 阻塞问题
    NOTE = "note"                    # 一般笔记


@dataclass
class ProgressLogEntry:
    """进度日志条目"""
    log_type: str
    summary: str
    files: List[str] = field(default_factory=list)
    code_snippet: Optional[str] = None
    timestamp: Optional[str] = None
    task_code: Optional[str] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "log_type": self.log_type,
            "summary": self.summary,
            "files": self.files,
            "code_snippet": self.code_snippet,
            "timestamp": self.timestamp,
            "task_code": self.task_code,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgressLogEntry":
        return cls(
            log_type=data.get("log_type", "note"),
            summary=data.get("summary", ""),
            files=data.get("files", []),
            code_snippet=data.get("code_snippet"),
            timestamp=data.get("timestamp"),
            task_code=data.get("task_code"),
        )


@dataclass
class MCPContext:
    """
    MCP 会话上下文（支持持久化）
    
    存储当前工作状态，包括：
    - 当前正在处理的任务
    - 当前对话 ID
    - 当前会话 ID
    - 会话开始时间
    - 最后活动时间
    - 进度日志（代码变更、问题解决、阻塞等）
    - 智能建议
    - 时间追踪
    """
    
    current_task_code: Optional[str] = None
    current_task_title: Optional[str] = None
    current_conversation_id: Optional[str] = None
    current_session_id: Optional[int] = None
    session_start_time: Optional[str] = None
    last_activity_time: Optional[str] = None
    
    # 任务历史（最近切换的任务）
    task_history: list = field(default_factory=list)
    
    # 统计信息
    tasks_started: int = 0
    tasks_completed: int = 0
    reviews_created: int = 0
    
    # 进度追踪（新增）
    progress_logs: List[Dict] = field(default_factory=list)
    last_completed_task: Optional[str] = None
    last_completed_task_title: Optional[str] = None
    files_changed_in_session: List[str] = field(default_factory=list)
    problems_solved: int = 0
    blockers_encountered: int = 0
    
    # 时间追踪（Agent 5 新增）
    task_start_time: Optional[str] = None  # 当前任务开始时间（ISO格式）
    task_elapsed_seconds: int = 0  # 当前任务累计耗时（秒）
    is_task_paused: bool = False  # 任务计时是否暂停
    pause_start_time: Optional[str] = None  # 暂停开始时间
    
    # 后端状态缓存（用于冲突检测）
    _backend_task_status: Optional[str] = None
    _backend_sync_time: Optional[str] = None
    
    # 评审状态缓存（用于智能建议，避免频繁 API 调用）
    _review_status_cache: Dict[str, Dict] = field(default_factory=dict)
    _cache_expiry: Optional[str] = None
    
    def __post_init__(self):
        if not self.session_start_time:
            self.session_start_time = datetime.now().isoformat()
    
    @property
    def _state_file(self) -> str:
        """状态文件路径"""
        return os.path.join(
            Path.home(), 
            ".testhub_mcp", 
            "context.json"
        )
    
    @property
    def has_code_changes(self) -> bool:
        """检测本次会话是否有代码变更"""
        return len(self.files_changed_in_session) > 0 or any(
            log.get("log_type") == ProgressLogType.CODE_CHANGE.value
            for log in self.progress_logs
        )
    
    @property
    def has_unresolved_blockers(self) -> bool:
        """检测是否有未解决的阻塞"""
        # 检查是否有 blocker 类型日志且没有对应的 problem_solved
        blockers = [
            log for log in self.progress_logs 
            if log.get("log_type") == ProgressLogType.BLOCKER.value
        ]
        return len(blockers) > self.problems_solved
    
    def set_current_task(self, task_code: str, task_title: Optional[str] = None, backend_status: Optional[str] = None):
        """
        设置当前任务
        
        Args:
            task_code: 任务编号
            task_title: 任务标题
            backend_status: 后端任务状态（用于冲突检测）
        """
        # 如果切换了任务，先完成上一个任务的计时
        if self.current_task_code and self.current_task_code != task_code:
            self._finalize_task_time()
            self._add_to_history(self.current_task_code, self.current_task_title)
        
        self.current_task_code = task_code
        self.current_task_title = task_title
        self.last_activity_time = datetime.now().isoformat()
        
        # 更新后端状态缓存
        if backend_status:
            self._backend_task_status = backend_status
            self._backend_sync_time = datetime.now().isoformat()
        
        self._save()
    
    def get_current_task(self) -> Optional[str]:
        """获取当前任务编号"""
        return self.current_task_code
    
    def clear_current_task(self):
        """清除当前任务"""
        if self.current_task_code:
            self._add_to_history(self.current_task_code, self.current_task_title)
        
        self.current_task_code = None
        self.current_task_title = None
        self._save()
    
    def set_conversation_id(self, conv_id: str):
        """设置当前对话 ID"""
        self.current_conversation_id = conv_id
        self.last_activity_time = datetime.now().isoformat()
        self._save()
    
    def set_session_id(self, session_id: int):
        """设置当前会话 ID"""
        self.current_session_id = session_id
        self.last_activity_time = datetime.now().isoformat()
        self._save()
    
    def record_task_started(self):
        """记录任务开始"""
        self.tasks_started += 1
        self._save()
    
    def record_task_completed(self, task_code: Optional[str] = None, task_title: Optional[str] = None):
        """
        记录任务完成
        
        Args:
            task_code: 完成的任务编号（默认使用当前任务）
            task_title: 任务标题
        """
        self.tasks_completed += 1
        
        # 记录最近完成的任务（用于智能建议）
        completed_code = task_code or self.current_task_code
        completed_title = task_title or self.current_task_title
        
        if completed_code:
            self.last_completed_task = completed_code
            self.last_completed_task_title = completed_title
            # 清除该任务的评审缓存，以便后续检查
            if completed_code in self._review_status_cache:
                del self._review_status_cache[completed_code]
        
        self._save()
    
    def record_review_created(self):
        """记录评审创建"""
        self.reviews_created += 1
        self._save()
    
    # ============== 时间追踪方法（Agent 5 新增） ==============
    
    def start_task_timer(self):
        """
        开始任务计时
        
        在任务开始时调用，记录开始时间。
        如果之前有暂停的计时，会保留已累计的时间。
        """
        now = datetime.now()
        
        # 如果之前是暂停状态，恢复计时
        if self.is_task_paused and self.pause_start_time:
            # 暂停期间的时间不计入
            self.is_task_paused = False
            self.pause_start_time = None
        else:
            # 全新开始
            self.task_start_time = now.isoformat()
            # 不重置 task_elapsed_seconds，可能是切换回之前的任务
        
        self.last_activity_time = now.isoformat()
        self._save()
        
        logger.debug(f"任务计时开始: task={self.current_task_code}, start_time={self.task_start_time}")
    
    def pause_task_timer(self):
        """
        暂停任务计时
        
        记录当前已消耗时间并标记为暂停状态。
        """
        if not self.task_start_time or self.is_task_paused:
            return  # 没有开始或已经暂停
        
        now = datetime.now()
        
        # 计算自开始以来的时间并累加
        try:
            start_time = datetime.fromisoformat(self.task_start_time)
            elapsed = (now - start_time).total_seconds()
            self.task_elapsed_seconds += int(elapsed)
        except (ValueError, TypeError):
            pass
        
        self.is_task_paused = True
        self.pause_start_time = now.isoformat()
        self.last_activity_time = now.isoformat()
        self._save()
        
        logger.debug(
            f"任务计时暂停: task={self.current_task_code}, "
            f"elapsed={self.task_elapsed_seconds}s"
        )
    
    def resume_task_timer(self):
        """
        恢复任务计时
        
        从暂停状态恢复，继续累计时间。
        """
        if not self.is_task_paused:
            return  # 没有暂停
        
        now = datetime.now()
        
        # 重新设置开始时间（从现在开始继续计时）
        self.task_start_time = now.isoformat()
        self.is_task_paused = False
        self.pause_start_time = None
        self.last_activity_time = now.isoformat()
        self._save()
        
        logger.debug(
            f"任务计时恢复: task={self.current_task_code}, "
            f"previous_elapsed={self.task_elapsed_seconds}s"
        )
    
    def get_task_elapsed_time(self) -> int:
        """
        获取当前任务的总耗时（秒）
        
        Returns:
            总耗时秒数，包括之前累计的时间和当前正在计时的时间
        """
        total = self.task_elapsed_seconds
        
        # 如果正在计时（非暂停状态），加上当前时间段
        if self.task_start_time and not self.is_task_paused:
            try:
                start_time = datetime.fromisoformat(self.task_start_time)
                current_elapsed = (datetime.now() - start_time).total_seconds()
                total += int(current_elapsed)
            except (ValueError, TypeError):
                pass
        
        return total
    
    def format_elapsed_time(self, seconds: Optional[int] = None) -> str:
        """
        格式化耗时显示
        
        Args:
            seconds: 秒数，不传则使用当前任务耗时
            
        Returns:
            格式化的时间字符串，如 "1小时23分钟" 或 "45分钟"
        """
        if seconds is None:
            seconds = self.get_task_elapsed_time()
        
        if seconds < 60:
            return f"{seconds}秒"
        
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes}分钟"
        
        hours = minutes // 60
        remaining_minutes = minutes % 60
        
        if remaining_minutes == 0:
            return f"{hours}小时"
        return f"{hours}小时{remaining_minutes}分钟"
    
    def _finalize_task_time(self) -> int:
        """
        完成当前任务的计时（内部方法）
        
        停止计时并返回总耗时。用于任务切换或完成时。
        
        Returns:
            总耗时秒数
        """
        total = self.get_task_elapsed_time()
        
        # 重置计时状态
        self.task_start_time = None
        self.task_elapsed_seconds = 0
        self.is_task_paused = False
        self.pause_start_time = None
        
        return total
    
    def finish_task_timer(self) -> tuple[int, str]:
        """
        完成任务计时
        
        停止计时，返回总耗时并重置状态。
        
        Returns:
            (总耗时秒数, 格式化的时间字符串)
        """
        total_seconds = self._finalize_task_time()
        formatted = self.format_elapsed_time(total_seconds)
        
        logger.debug(
            f"任务计时完成: task={self.current_task_code}, "
            f"total={total_seconds}s ({formatted})"
        )
        
        self._save()
        return total_seconds, formatted
    
    # ============== 上下文同步方法（Agent 5 新增） ==============
    
    def update_backend_status(self, status: str, sync_time: Optional[str] = None):
        """
        更新后端状态缓存
        
        Args:
            status: 后端任务状态
            sync_time: 同步时间（ISO格式），默认为当前时间
        """
        self._backend_task_status = status
        self._backend_sync_time = sync_time or datetime.now().isoformat()
        self._save()
    
    def check_status_conflict(self, backend_status: str) -> Optional[str]:
        """
        检查本地状态与后端是否存在冲突
        
        Args:
            backend_status: 后端返回的当前状态
            
        Returns:
            冲突描述，如果没有冲突返回 None
        """
        if not self._backend_task_status:
            return None
        
        # 状态映射（用于比较）
        status_priority = {
            "pending": 0,
            "in_progress": 1,
            "review": 2,
            "testing": 3,
            "completed": 4,
            "blocked": -1,
            "cancelled": -2,
            "paused": 0.5,
        }
        
        cached_priority = status_priority.get(self._backend_task_status, 0)
        current_priority = status_priority.get(backend_status, 0)
        
        # 如果后端状态已经更新（不是由我们触发的）
        if self._backend_task_status != backend_status:
            # 检查是否是向后退的状态变更（可能有冲突）
            if current_priority < cached_priority and cached_priority > 0:
                return (
                    f"状态冲突：本地缓存状态为 '{self._backend_task_status}'，"
                    f"但后端当前状态为 '{backend_status}'。"
                    f"可能有其他人修改了任务状态。"
                )
        
        return None
    
    def get_sync_info(self) -> Dict[str, Any]:
        """
        获取同步信息
        
        Returns:
            包含后端状态缓存和同步时间的字典
        """
        return {
            "backend_status": self._backend_task_status,
            "sync_time": self._backend_sync_time,
            "is_stale": self._is_sync_stale(),
        }
    
    def _is_sync_stale(self) -> bool:
        """检查同步是否过期（超过5分钟）"""
        if not self._backend_sync_time:
            return True
        
        try:
            sync_time = datetime.fromisoformat(self._backend_sync_time)
            age = (datetime.now() - sync_time).total_seconds()
            return age > 300  # 5分钟
        except (ValueError, TypeError):
            return True
    
    # ============== 进度追踪方法（新增） ==============
    
    def add_progress_log(
        self,
        log_type: str,
        summary: str,
        files: Optional[List[str]] = None,
        code_snippet: Optional[str] = None,
        task_code: Optional[str] = None,
    ) -> ProgressLogEntry:
        """
        添加进度日志
        
        Args:
            log_type: 日志类型 (code_change, problem_solved, blocker, note)
            summary: 简要描述
            files: 涉及的文件列表
            code_snippet: 关键代码片段
            task_code: 关联的任务编号（默认使用当前任务）
        
        Returns:
            创建的日志条目
        """
        entry = ProgressLogEntry(
            log_type=log_type,
            summary=summary,
            files=files or [],
            code_snippet=code_snippet,
            task_code=task_code or self.current_task_code,
        )
        
        self.progress_logs.append(entry.to_dict())
        
        # 更新统计
        if log_type == ProgressLogType.PROBLEM_SOLVED.value:
            self.problems_solved += 1
        elif log_type == ProgressLogType.BLOCKER.value:
            self.blockers_encountered += 1
        elif log_type == ProgressLogType.CODE_CHANGE.value and files:
            # 记录变更的文件
            for f in files:
                if f not in self.files_changed_in_session:
                    self.files_changed_in_session.append(f)
        
        self.last_activity_time = datetime.now().isoformat()
        
        # 只保留最近 50 条日志
        if len(self.progress_logs) > 50:
            self.progress_logs = self.progress_logs[-50:]
        
        self._save()
        return entry
    
    def record_file_changed(self, file_path: str, summary: Optional[str] = None):
        """
        记录文件变更
        
        Args:
            file_path: 变更的文件路径
            summary: 变更描述
        """
        if file_path not in self.files_changed_in_session:
            self.files_changed_in_session.append(file_path)
        
        if summary:
            self.add_progress_log(
                log_type=ProgressLogType.CODE_CHANGE.value,
                summary=summary,
                files=[file_path],
            )
        else:
            self.last_activity_time = datetime.now().isoformat()
            self._save()
    
    def record_problem_solved(self, summary: str, files: Optional[List[str]] = None):
        """
        记录问题已解决
        
        Args:
            summary: 问题描述
            files: 涉及的文件
        """
        self.add_progress_log(
            log_type=ProgressLogType.PROBLEM_SOLVED.value,
            summary=summary,
            files=files,
        )
    
    def record_blocker(self, summary: str, files: Optional[List[str]] = None):
        """
        记录阻塞问题
        
        Args:
            summary: 阻塞描述
            files: 涉及的文件
        """
        self.add_progress_log(
            log_type=ProgressLogType.BLOCKER.value,
            summary=summary,
            files=files,
        )
    
    def get_progress_logs_for_task(self, task_code: Optional[str] = None) -> List[Dict]:
        """
        获取指定任务的进度日志
        
        Args:
            task_code: 任务编号（默认当前任务）
        
        Returns:
            该任务的进度日志列表
        """
        target_task = task_code or self.current_task_code
        if not target_task:
            return self.progress_logs
        
        return [
            log for log in self.progress_logs
            if log.get("task_code") == target_task
        ]
    
    def _time_since_last_update(self) -> int:
        """
        计算距离最后活动的时间（秒）
        
        Returns:
            秒数，如果没有记录则返回 0
        """
        if not self.last_activity_time:
            return 0
        
        try:
            last_time = datetime.fromisoformat(self.last_activity_time)
            delta = datetime.now() - last_time
            return int(delta.total_seconds())
        except (ValueError, TypeError):
            return 0
    
    def _is_cache_valid(self) -> bool:
        """检查缓存是否有效（5分钟内）"""
        if not self._cache_expiry:
            return False
        try:
            expiry = datetime.fromisoformat(self._cache_expiry)
            return datetime.now() < expiry
        except (ValueError, TypeError):
            return False
    
    def update_review_cache(self, task_code: str, has_review: bool, review_status: Optional[str] = None):
        """
        更新评审状态缓存
        
        Args:
            task_code: 任务编号
            has_review: 是否有评审
            review_status: 评审状态
        """
        self._review_status_cache[task_code] = {
            "has_review": has_review,
            "status": review_status,
            "updated_at": datetime.now().isoformat(),
        }
        # 缓存 5 分钟后过期
        self._cache_expiry = (datetime.now() + timedelta(minutes=5)).isoformat()
    
    def get_cached_review_status(self, task_code: str) -> Optional[Dict]:
        """
        获取缓存的评审状态
        
        Returns:
            缓存的状态，如果无效返回 None
        """
        if not self._is_cache_valid():
            self._review_status_cache.clear()
            return None
        return self._review_status_cache.get(task_code)
    
    def get_suggestions(self, include_api_check: bool = False) -> List[str]:
        """
        根据当前状态生成智能建议
        
        这是一个同步方法，使用缓存的数据生成建议。
        如需最新的 API 数据，请使用 get_suggestions_async。
        
        Args:
            include_api_check: 是否包含基于 API 的检查（需要缓存有效）
        
        Returns:
            建议列表
        """
        suggestions = []
        
        # 1. 检测到代码修改但没有关联任务
        if self.has_code_changes and not self.current_task_code:
            suggestions.append(
                "💡 检测到代码修改但未关联任务，建议创建或关联任务以便追踪"
            )
        
        # 2. 任务进行中但长时间没有更新（超过 1 小时）
        if self.current_task_code:
            time_since_update = self._time_since_last_update()
            if time_since_update > 3600:  # 1 小时
                hours = time_since_update // 3600
                suggestions.append(
                    f"⏰ 任务 {self.current_task_code} 已进行 {hours} 小时未更新，"
                    f"建议记录进度或完成任务"
                )
            elif time_since_update > 1800:  # 30 分钟
                suggestions.append(
                    f"📝 任务 {self.current_task_code} 进行中，建议记录一下当前进度"
                )
        
        # 3. 任务完成但没有评审（基于缓存检查）
        if self.last_completed_task and include_api_check:
            cached = self.get_cached_review_status(self.last_completed_task)
            if cached and not cached.get("has_review"):
                suggestions.append(
                    f"📋 任务 {self.last_completed_task} 已完成，建议创建设计评审"
                )
        
        # 4. 有未解决的阻塞问题
        if self.has_unresolved_blockers:
            suggestions.append(
                "🚧 检测到未解决的阻塞问题，需要协助吗？"
            )
        
        # 5. 会话时间过长提醒（超过 4 小时）
        if self.session_start_time:
            try:
                start_time = datetime.fromisoformat(self.session_start_time)
                session_hours = (datetime.now() - start_time).total_seconds() / 3600
                if session_hours > 4:
                    suggestions.append(
                        f"☕ 会话已持续 {int(session_hours)} 小时，建议适当休息"
                    )
            except (ValueError, TypeError):
                pass
        
        # 6. 修改文件较多提醒
        if len(self.files_changed_in_session) > 10:
            suggestions.append(
                f"📁 本次会话已修改 {len(self.files_changed_in_session)} 个文件，"
                f"建议及时提交或拆分变更"
            )
        
        # 7. 任务完成但有大量未记录的代码变更
        if (self.tasks_completed > 0 and 
            len(self.files_changed_in_session) > 5 and 
            len([l for l in self.progress_logs if l.get("log_type") == "code_change"]) == 0):
            suggestions.append(
                "📝 本次完成了任务但变更记录较少，建议补充变更摘要"
            )
        
        return suggestions
    
    async def get_suggestions_async(self, api_client: "TestHubAPIClient") -> List[str]:
        """
        异步获取智能建议（包含 API 调用）
        
        Args:
            api_client: TestHub API 客户端
        
        Returns:
            建议列表
        """
        suggestions = self.get_suggestions(include_api_check=False)
        
        # 检查最近完成的任务是否有评审
        if self.last_completed_task:
            try:
                # 使用缓存避免频繁调用
                cached = self.get_cached_review_status(self.last_completed_task)
                if cached is None:
                    # 缓存无效，调用 API
                    result = await api_client.get_task_review_status(self.last_completed_task)
                    has_review = result.get("has_review", False)
                    review_status = result.get("status")
                    self.update_review_cache(self.last_completed_task, has_review, review_status)
                    
                    if not has_review:
                        suggestions.append(
                            f"📋 任务 {self.last_completed_task} 已完成，建议创建设计评审"
                        )
                    elif review_status == "draft":
                        suggestions.append(
                            f"📋 任务 {self.last_completed_task} 的评审还是草稿状态，建议补充文档后提交"
                        )
            except Exception as e:
                logger.debug(f"获取评审状态失败: {e}")
        
        return suggestions
    
    def clear(self):
        """清除当前上下文（保留统计信息和进度日志）"""
        if self.current_task_code:
            self._add_to_history(self.current_task_code, self.current_task_title)
        
        self.current_task_code = None
        self.current_task_title = None
        self.current_conversation_id = None
        # 不清除 session_id，保持会话关联
        # 不清除进度日志和统计信息
        self._save()
    
    def reset(self):
        """完全重置上下文（包括统计信息和进度日志）"""
        self.current_task_code = None
        self.current_task_title = None
        self.current_conversation_id = None
        self.current_session_id = None
        self.session_start_time = datetime.now().isoformat()
        self.last_activity_time = None
        self.task_history = []
        self.tasks_started = 0
        self.tasks_completed = 0
        self.reviews_created = 0
        
        # 重置进度追踪
        self.progress_logs = []
        self.last_completed_task = None
        self.last_completed_task_title = None
        self.files_changed_in_session = []
        self.problems_solved = 0
        self.blockers_encountered = 0
        self._review_status_cache = {}
        self._cache_expiry = None
        
        # 重置时间追踪（Agent 5 新增）
        self.task_start_time = None
        self.task_elapsed_seconds = 0
        self.is_task_paused = False
        self.pause_start_time = None
        self._backend_task_status = None
        self._backend_sync_time = None
        
        self._save()
    
    def clear_session_progress(self):
        """
        清除本次会话的进度数据（保留任务历史和统计）
        
        适用于开始新的工作日或切换项目时
        """
        self.progress_logs = []
        self.files_changed_in_session = []
        self.problems_solved = 0
        self.blockers_encountered = 0
        self._review_status_cache = {}
        self._cache_expiry = None
        
        # 重置时间追踪（Agent 5 新增）
        self.task_start_time = None
        self.task_elapsed_seconds = 0
        self.is_task_paused = False
        self.pause_start_time = None
        
        self._save()
    
    def _add_to_history(self, task_code: str, task_title: Optional[str] = None):
        """添加任务到历史记录"""
        # 避免重复
        if self.task_history and self.task_history[-1].get("code") == task_code:
            return
        
        self.task_history.append({
            "code": task_code,
            "title": task_title,
            "time": datetime.now().isoformat(),
        })
        
        # 只保留最近 10 个
        if len(self.task_history) > 10:
            self.task_history = self.task_history[-10:]
    
    def _save(self):
        """持久化到本地文件"""
        try:
            os.makedirs(os.path.dirname(self._state_file), exist_ok=True)
            with open(self._state_file, 'w', encoding='utf-8') as f:
                data = {
                    # 基本状态
                    "current_task_code": self.current_task_code,
                    "current_task_title": self.current_task_title,
                    "current_conversation_id": self.current_conversation_id,
                    "current_session_id": self.current_session_id,
                    "session_start_time": self.session_start_time,
                    "last_activity_time": self.last_activity_time,
                    "task_history": self.task_history,
                    
                    # 统计信息
                    "tasks_started": self.tasks_started,
                    "tasks_completed": self.tasks_completed,
                    "reviews_created": self.reviews_created,
                    
                    # 进度追踪
                    "progress_logs": self.progress_logs,
                    "last_completed_task": self.last_completed_task,
                    "last_completed_task_title": self.last_completed_task_title,
                    "files_changed_in_session": self.files_changed_in_session,
                    "problems_solved": self.problems_solved,
                    "blockers_encountered": self.blockers_encountered,
                    
                    # 时间追踪（Agent 5 新增）
                    "task_start_time": self.task_start_time,
                    "task_elapsed_seconds": self.task_elapsed_seconds,
                    "is_task_paused": self.is_task_paused,
                    "pause_start_time": self.pause_start_time,
                    
                    # 后端状态缓存（Agent 5 新增）
                    "_backend_task_status": self._backend_task_status,
                    "_backend_sync_time": self._backend_sync_time,
                    
                    # 评审缓存数据
                    "_review_status_cache": self._review_status_cache,
                    "_cache_expiry": self._cache_expiry,
                }
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # 持久化失败不影响主流程
            logger.warning(f"保存上下文失败: {e}")
    
    @classmethod
    def load(cls) -> "MCPContext":
        """从本地文件加载状态"""
        state_file = os.path.join(Path.home(), ".testhub_mcp", "context.json")
        
        try:
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    ctx = cls(
                        # 基本状态
                        current_task_code=data.get("current_task_code"),
                        current_task_title=data.get("current_task_title"),
                        current_conversation_id=data.get("current_conversation_id"),
                        current_session_id=data.get("current_session_id"),
                        session_start_time=data.get("session_start_time"),
                        last_activity_time=data.get("last_activity_time"),
                        task_history=data.get("task_history", []),
                        
                        # 统计信息
                        tasks_started=data.get("tasks_started", 0),
                        tasks_completed=data.get("tasks_completed", 0),
                        reviews_created=data.get("reviews_created", 0),
                        
                        # 进度追踪
                        progress_logs=data.get("progress_logs", []),
                        last_completed_task=data.get("last_completed_task"),
                        last_completed_task_title=data.get("last_completed_task_title"),
                        files_changed_in_session=data.get("files_changed_in_session", []),
                        problems_solved=data.get("problems_solved", 0),
                        blockers_encountered=data.get("blockers_encountered", 0),
                        
                        # 时间追踪（Agent 5 新增）
                        task_start_time=data.get("task_start_time"),
                        task_elapsed_seconds=data.get("task_elapsed_seconds", 0),
                        is_task_paused=data.get("is_task_paused", False),
                        pause_start_time=data.get("pause_start_time"),
                        
                        # 后端状态缓存（Agent 5 新增）
                        _backend_task_status=data.get("_backend_task_status"),
                        _backend_sync_time=data.get("_backend_sync_time"),
                        
                        # 评审缓存数据
                        _review_status_cache=data.get("_review_status_cache", {}),
                        _cache_expiry=data.get("_cache_expiry"),
                    )
                    return ctx
        except Exception as e:
            logger.warning(f"加载上下文失败: {e}")
        
        return cls()
    
    def to_display(self, include_suggestions: bool = True) -> str:
        """
        生成可显示的上下文信息
        
        Args:
            include_suggestions: 是否包含智能建议
        """
        lines = ["📍 **当前上下文**"]
        lines.append("")
        
        if self.current_task_code:
            lines.append(f"**当前任务**：{self.current_task_code}")
            if self.current_task_title:
                lines.append(f"  - {self.current_task_title}")
            
            # 显示时间追踪信息
            if self.task_start_time:
                elapsed = self.get_task_elapsed_time()
                elapsed_str = self.format_elapsed_time(elapsed)
                if self.is_task_paused:
                    lines.append(f"  - ⏸️ 计时已暂停，累计耗时：{elapsed_str}")
                else:
                    lines.append(f"  - ⏱️ 进行中，已耗时：{elapsed_str}")
        else:
            lines.append("**当前任务**：无")
        
        if self.current_session_id:
            lines.append(f"**会话 ID**：{self.current_session_id}")
        
        lines.append("")
        lines.append("**本次会话统计**：")
        lines.append(f"- 开始任务：{self.tasks_started} 个")
        lines.append(f"- 完成任务：{self.tasks_completed} 个")
        lines.append(f"- 创建评审：{self.reviews_created} 个")
        
        # 进度追踪统计（新增）
        if self.files_changed_in_session or self.problems_solved or self.blockers_encountered:
            lines.append("")
            lines.append("**进度追踪**：")
            if self.files_changed_in_session:
                lines.append(f"- 修改文件：{len(self.files_changed_in_session)} 个")
            if self.problems_solved:
                lines.append(f"- 解决问题：{self.problems_solved} 个")
            if self.blockers_encountered:
                unresolved = max(0, self.blockers_encountered - self.problems_solved)
                lines.append(f"- 遇到阻塞：{self.blockers_encountered} 个" + 
                           (f"（未解决：{unresolved}）" if unresolved > 0 else ""))
        
        # 最近进度日志（新增）
        if self.progress_logs:
            recent_logs = self.progress_logs[-3:]  # 最近 3 条
            lines.append("")
            lines.append("**最近进度**：")
            for log in reversed(recent_logs):
                log_type = log.get("log_type", "note")
                summary = log.get("summary", "")
                timestamp = log.get("timestamp", "")
                
                # 格式化时间
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%H:%M")
                except (ValueError, TypeError):
                    time_str = ""
                
                # 类型图标
                type_icons = {
                    "code_change": "📝",
                    "problem_solved": "✅",
                    "blocker": "🚧",
                    "note": "📌",
                }
                icon = type_icons.get(log_type, "📌")
                
                # 截断过长的摘要
                if len(summary) > 50:
                    summary = summary[:50] + "..."
                
                if time_str:
                    lines.append(f"- {icon} [{time_str}] {summary}")
                else:
                    lines.append(f"- {icon} {summary}")
        
        if self.task_history:
            lines.append("")
            lines.append("**最近切换的任务**：")
            for item in reversed(self.task_history[-5:]):
                title = item.get("title", "")
                if title:
                    lines.append(f"- {item['code']} - {title}")
                else:
                    lines.append(f"- {item['code']}")
        
        # 智能建议（新增）
        if include_suggestions:
            suggestions = self.get_suggestions(include_api_check=True)
            if suggestions:
                lines.append("")
                lines.append("**💡 建议**：")
                for suggestion in suggestions:
                    lines.append(f"- {suggestion}")
        
        if self.session_start_time:
            lines.append("")
            lines.append(f"_会话开始于：{self.session_start_time}_")
        
        return "\n".join(lines)
    
    def to_dict(self, include_suggestions: bool = False) -> dict:
        """
        转换为字典
        
        Args:
            include_suggestions: 是否包含智能建议
        """
        result = {
            # 基本状态
            "current_task_code": self.current_task_code,
            "current_task_title": self.current_task_title,
            "current_conversation_id": self.current_conversation_id,
            "current_session_id": self.current_session_id,
            "session_start_time": self.session_start_time,
            "last_activity_time": self.last_activity_time,
            "task_history": self.task_history,
            
            # 统计信息
            "statistics": {
                "tasks_started": self.tasks_started,
                "tasks_completed": self.tasks_completed,
                "reviews_created": self.reviews_created,
                "files_changed": len(self.files_changed_in_session),
                "problems_solved": self.problems_solved,
                "blockers_encountered": self.blockers_encountered,
            },
            
            # 进度追踪
            "progress": {
                "last_completed_task": self.last_completed_task,
                "last_completed_task_title": self.last_completed_task_title,
                "files_changed_in_session": self.files_changed_in_session,
                "recent_logs": self.progress_logs[-10:] if self.progress_logs else [],
                "has_code_changes": self.has_code_changes,
                "has_unresolved_blockers": self.has_unresolved_blockers,
            },
            
            # 时间追踪（Agent 5 新增）
            "time_tracking": {
                "task_start_time": self.task_start_time,
                "task_elapsed_seconds": self.get_task_elapsed_time(),
                "task_elapsed_formatted": self.format_elapsed_time(),
                "is_paused": self.is_task_paused,
                "pause_start_time": self.pause_start_time,
            },
            
            # 同步信息（Agent 5 新增）
            "sync_info": self.get_sync_info(),
        }
        
        if include_suggestions:
            result["suggestions"] = self.get_suggestions(include_api_check=True)
        
        return result


# 全局上下文实例（懒加载）
_global_context: Optional[MCPContext] = None


def get_context() -> MCPContext:
    """获取全局上下文实例"""
    global _global_context
    if _global_context is None:
        _global_context = MCPContext.load()
    return _global_context


def reset_context():
    """重置全局上下文"""
    global _global_context
    _global_context = MCPContext()
    _global_context._save()

