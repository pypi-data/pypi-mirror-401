"""
TestHub API Client

用于 MCP Server 调用 TestHub 后端 API。
支持 API Token 认证和重试机制。
"""

import os
import asyncio
from typing import Optional, Any
from urllib.parse import urljoin

import httpx
from loguru import logger


class APIError(Exception):
    """API 调用错误"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class TestHubAPIClient:
    """
    TestHub API 客户端
    
    用于 MCP Server 与 TestHub 后端通信。
    支持：
    - API Token 认证
    - 自动重试
    - 错误处理
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_token: Optional[str] = None,
        team_id: Optional[int] = None,
        default_session_id: Optional[int] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """
        初始化 API 客户端
        
        Args:
            base_url: API 基础 URL，默认从环境变量读取
            api_token: API Token，默认从环境变量读取
            team_id: 团队 ID，默认从环境变量读取
            default_session_id: 默认开发会话 ID，默认从环境变量读取
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.base_url = base_url or os.environ.get("TESTHUB_API_URL", "http://localhost:8000/api/v1")
        self.api_token = api_token or os.environ.get("TESTHUB_API_TOKEN", "")
        self.team_id = team_id or int(os.environ.get("TESTHUB_TEAM_ID", "0")) or None
        self.default_session_id = default_session_id or (
            int(os.environ.get("TESTHUB_SESSION_ID", "0")) or None
        )
        self.timeout = timeout
        self.max_retries = max_retries
        
        # 创建 HTTP 客户端
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """获取或创建 HTTP 客户端"""
        if self._client is None or self._client.is_closed:
            headers = {
                "Content-Type": "application/json",
            }
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            if self.team_id:
                headers["X-Team-Id"] = str(self.team_id)
            if self.default_session_id:
                headers["X-Session-ID"] = str(self.default_session_id)
            
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            )
        return self._client
    
    async def close(self):
        """关闭客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json_data: Optional[dict] = None,
        retry_count: int = 0,
    ) -> dict:
        """
        发送 HTTP 请求
        
        Args:
            method: HTTP 方法
            path: API 路径
            params: 查询参数
            json_data: JSON 请求体
            retry_count: 当前重试次数
        
        Returns:
            响应数据
        """
        client = await self._get_client()
        
        try:
            response = await client.request(
                method=method,
                url=path,
                params=params,
                json=json_data,
            )
            
            # 解析响应
            try:
                data = response.json()
            except Exception:
                data = {"message": response.text}
            
            # 检查 HTTP 状态
            if response.status_code >= 400:
                error_message = data.get("detail") or data.get("message") or f"HTTP {response.status_code}"
                
                # 可重试的错误
                if response.status_code >= 500 and retry_count < self.max_retries:
                    logger.warning(f"API 请求失败 ({response.status_code})，重试 {retry_count + 1}/{self.max_retries}")
                    await asyncio.sleep(1 * (retry_count + 1))  # 指数退避
                    return await self._request(method, path, params, json_data, retry_count + 1)
                
                raise APIError(error_message, response.status_code, data)
            
            return data
            
        except httpx.TimeoutException:
            if retry_count < self.max_retries:
                logger.warning(f"API 请求超时，重试 {retry_count + 1}/{self.max_retries}")
                await asyncio.sleep(1 * (retry_count + 1))
                return await self._request(method, path, params, json_data, retry_count + 1)
            raise APIError("请求超时")
            
        except httpx.ConnectError as e:
            raise APIError(f"连接失败: {str(e)}")
    
    async def get(self, path: str, params: Optional[dict] = None) -> dict:
        """GET 请求"""
        return await self._request("GET", path, params=params)
    
    async def post(self, path: str, data: Optional[dict] = None, params: Optional[dict] = None) -> dict:
        """POST 请求"""
        return await self._request("POST", path, params=params, json_data=data)
    
    async def put(self, path: str, data: Optional[dict] = None) -> dict:
        """PUT 请求"""
        return await self._request("PUT", path, json_data=data)
    
    async def patch(self, path: str, data: Optional[dict] = None, params: Optional[dict] = None) -> dict:
        """PATCH 请求"""
        return await self._request("PATCH", path, params=params, json_data=data)
    
    async def delete(self, path: str, params: Optional[dict] = None) -> dict:
        """DELETE 请求"""
        return await self._request("DELETE", path, params=params)
    
    # ============== 缺陷相关 API（使用 MCP 端点） ==============
    
    async def list_bugs(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        category: Optional[str] = None,
        assignee: Optional[str] = None,
        keyword: Optional[str] = None,
        session_id: Optional[int] = None,
        include_archived: bool = False,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """获取缺陷列表"""
        params = {
            "page": page,
            "page_size": page_size,
            "include_archived": include_archived,
        }
        if status:
            params["status"] = status
        if severity:
            params["severity"] = severity
        if category:
            params["category"] = category
        if assignee:
            params["assignee"] = assignee
        if keyword:
            params["keyword"] = keyword
        if session_id:
            params["session_id"] = session_id
        
        return await self.get("/mcp/bugs", params=params)
    
    async def get_bug(self, bug_id: int) -> dict:
        """获取缺陷详情"""
        return await self.get(f"/mcp/bugs/{bug_id}")
    
    async def create_bug(
        self,
        title: str,
        description: Optional[str] = None,
        severity: str = "minor",
        assignee: Optional[str] = None,
        related_task_code: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> dict:
        """创建缺陷"""
        data = {
            "title": title,
            "severity": severity,
        }
        if description:
            data["description"] = description
        if assignee:
            data["assignee"] = assignee
        if related_task_code:
            data["related_task_code"] = related_task_code
        if due_date:
            data["due_date"] = due_date
        
        return await self.post("/mcp/bugs", data=data)
    
    async def update_bug(
        self,
        bug_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        severity: Optional[str] = None,
        assignee: Optional[str] = None,
        due_date: Optional[str] = None,
        screenshots: Optional[list] = None,
    ) -> dict:
        """更新缺陷"""
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if severity is not None:
            data["severity"] = severity
        if assignee is not None:
            data["assignee"] = assignee
        if due_date is not None:
            data["due_date"] = due_date
        if screenshots is not None:
            data["screenshots"] = screenshots
        
        return await self.put(f"/mcp/bugs/{bug_id}", data=data)
    
    async def update_bug_status(
        self,
        bug_id: int,
        status: str,
        verified_in_session_id: Optional[int] = None,
    ) -> dict:
        """更新缺陷状态"""
        return await self.patch(f"/mcp/bugs/{bug_id}/status", params={"status": status})
    
    async def delete_bug(self, bug_id: int) -> dict:
        """删除缺陷"""
        return await self.delete(f"/mcp/bugs/{bug_id}")
    
    async def archive_bug(self, bug_id: int) -> dict:
        """归档缺陷"""
        return await self.post(f"/mcp/bugs/{bug_id}/archive")
    
    async def get_bug_stats(self) -> dict:
        """获取缺陷统计"""
        return await self.get("/mcp/bugs/stats")
    
    async def get_bug_session_stats(self, session_id: int) -> dict:
        """获取会话缺陷统计"""
        return await self.get(f"/mcp/bugs/session/{session_id}/stats")
    
    # ============== 任务相关 API ==============
    
    async def list_dev_tasks(
        self,
        session_id: Optional[int] = None,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """获取开发任务列表"""
        params = {"page": page, "page_size": page_size}
        if session_id:
            params["session_id"] = session_id
        if status:
            params["status"] = status
        if assignee:
            params["assignee"] = assignee
        if keyword:
            params["keyword"] = keyword
        
        return await self.get("/dev-tasks", params=params)
    
    async def get_dev_task(self, task_id: int) -> dict:
        """获取开发任务详情"""
        return await self.get(f"/dev-tasks/{task_id}")
    
    async def update_dev_task_status(self, task_id: int, status: str) -> dict:
        """更新开发任务状态"""
        return await self.patch(f"/dev-tasks/{task_id}/status", data={"status": status})
    
    # ============== 会话相关 API ==============
    
    async def list_dev_sessions(
        self,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """获取开发会话列表"""
        params = {"page": page, "page_size": page_size}
        if status:
            params["status"] = status
        
        return await self.get("/dev-sessions", params=params)
    
    async def get_dev_session(self, session_id: int) -> dict:
        """获取开发会话详情"""
        return await self.get(f"/dev-sessions/{session_id}")
    
    # ============== Cursor 会话 API ==============
    
    async def create_cursor_session(
        self,
        title: str,
        task_code: Optional[str] = None,
        description: Optional[str] = None,
        workspace_path: Optional[str] = None,
    ) -> dict:
        """创建 Cursor 编程会话"""
        data = {"title": title}
        if task_code:
            data["task_code"] = task_code
        if description:
            data["description"] = description
        if workspace_path:
            data["workspace_path"] = workspace_path
        return await self.post("/mcp/cursor-sessions", data=data)
    
    async def sync_cursor_message(
        self,
        session_code: str,
        role: str,
        content: str,
        model: Optional[str] = None,
        tokens_input: Optional[int] = None,
        tokens_output: Optional[int] = None,
        context_files: Optional[list] = None,
        code_changes: Optional[list] = None,
    ) -> dict:
        """同步 Cursor 对话消息"""
        data = {
            "role": role,
            "content": content,
        }
        if model:
            data["model"] = model
        if tokens_input is not None:
            data["tokens_input"] = tokens_input
        if tokens_output is not None:
            data["tokens_output"] = tokens_output
        if context_files:
            data["context_files"] = context_files
        if code_changes:
            data["code_changes"] = code_changes
        return await self.post(f"/mcp/cursor-sessions/{session_code}/messages", data=data)
    
    async def end_cursor_session(
        self,
        session_code: str,
        summary: Optional[str] = None,
    ) -> dict:
        """结束 Cursor 会话"""
        data = {}
        if summary:
            data["summary"] = summary
        return await self.post(f"/mcp/cursor-sessions/{session_code}/end", data=data)
    
    async def list_cursor_sessions(
        self,
        status: Optional[str] = None,
        task_code: Optional[str] = None,
        limit: int = 10,
    ) -> dict:
        """获取 Cursor 会话列表"""
        params = {"limit": limit}
        if status:
            params["status"] = status
        if task_code:
            params["task_code"] = task_code
        return await self.get("/mcp/cursor-sessions", params=params)
    
    async def get_cursor_session_messages(
        self,
        session_code: str,
        limit: int = 50,
    ) -> dict:
        """获取 Cursor 会话消息列表"""
        params = {"limit": limit}
        return await self.get(f"/mcp/cursor-sessions/{session_code}/messages", params=params)
    
    # ============== MCP 专用 API ==============
    
    async def get_task_by_code(self, task_code: str) -> dict:
        """通过任务编号获取任务详情（MCP 专用）"""
        return await self.get(f"/mcp/tasks/by-code/{task_code}")

    async def get_task_overview(self, task_code: str) -> dict:
        """获取任务概览（任务详情 + 评审状态 + 关联缺陷）（MCP 专用）"""
        return await self.get(f"/mcp/tasks/by-code/{task_code}/overview")
    
    async def update_task_status_by_code(self, task_code: str, status: str, comment: Optional[str] = None) -> dict:
        """通过任务编号更新任务状态（MCP 专用）"""
        data = {"status": status}
        if comment:
            data["comment"] = comment
        return await self.patch(f"/mcp/tasks/by-code/{task_code}/status", data=data)
    
    # 别名方法，兼容 task.py
    async def update_task_status(self, task_code: str, status: str, comment: Optional[str] = None) -> dict:
        """通过任务编号更新任务状态（别名）"""
        return await self.update_task_status_by_code(task_code, status, comment)
    
    async def get_my_tasks(self, status: Optional[str] = None, limit: int = 10) -> dict:
        """获取我的任务列表（MCP 专用）"""
        params = {"limit": limit}
        if status:
            params["status"] = status
        return await self.get("/mcp/tasks/my", params=params)
    
    # 别名方法，兼容 task.py
    async def list_my_tasks(self, status: Optional[str] = None, limit: int = 10) -> dict:
        """获取我的任务列表（别名）"""
        return await self.get_my_tasks(status, limit)
    
    async def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        category: str = "其他",
        complexity: str = "M",
        priority: str = "medium",
        task_type: str = "feature",
        acceptance_criteria: Optional[str] = None,
        technical_notes: Optional[str] = None,
        module: Optional[str] = None,
        assign_to_me: bool = True,
        session_id: Optional[int] = None,
    ) -> dict:
        """创建开发任务（MCP 专用）"""
        data = {
            "title": title,
            "category": category,
            "complexity": complexity,
            "priority": priority,
            "task_type": task_type,
            "assign_to_me": assign_to_me,
        }
        if description:
            data["description"] = description
        if acceptance_criteria:
            data["acceptance_criteria"] = acceptance_criteria
        if technical_notes:
            data["technical_notes"] = technical_notes
        if module:
            data["module"] = module
        if session_id:
            data["session_id"] = session_id
        
        result = await self.post("/mcp/tasks", data=data)
        return result.get("data", result)
    
    async def start_task(self, task_code: str, comment: Optional[str] = None) -> dict:
        """开始任务（MCP 专用）"""
        data = {}
        if comment:
            data["comment"] = comment
        result = await self.post(f"/mcp/tasks/by-code/{task_code}/start", data=data if data else None)
        return result.get("data", result)
    
    async def complete_task(
        self,
        task_code: str,
        completion_note: Optional[str] = None,
    ) -> dict:
        """完成任务（MCP 专用）"""
        data = {}
        if completion_note:
            data["completion_note"] = completion_note
        result = await self.post(f"/mcp/tasks/by-code/{task_code}/complete", data=data if data else None)
        return result.get("data", result)

    async def finish_task(
        self,
        task_code: str,
        change_summary: Optional[str] = None,
        files_changed: Optional[list] = None,
        test_points: Optional[list] = None,
        completion_note: Optional[str] = None,
        actual_hours: Optional[int] = None,
    ) -> dict:
        """一站式完成任务（MCP 专用）
        
        自动执行：
        1. 更新任务状态为"已完成"
        2. 生成变更摘要文档（DevDocument）
        3. 记录建议测试点（不自动创建测试用例）
        """
        data = {
            "change_summary": change_summary,
            "files_changed": files_changed or [],
            "test_points": test_points or [],
            "completion_note": completion_note,
        }
        if actual_hours:
            data["actual_hours"] = actual_hours
        
        result = await self.post(f"/mcp/tasks/by-code/{task_code}/finish", data=data)
        return result.get("data", result)

    async def get_daily_summary(self, limit: int = 10) -> dict:
        """获取每日工作摘要（MCP 专用）"""
        return await self.get("/mcp/daily-summary", params={"limit": limit})
    
    # ============== MCP Bug API ==============
    
    async def mcp_list_bugs(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        assignee: Optional[str] = None,
        keyword: Optional[str] = None,
        session_id: Optional[int] = None,
        include_archived: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """获取缺陷列表（MCP 专用）"""
        params = {
            "page": page,
            "page_size": page_size,
            "include_archived": include_archived,
        }
        if status:
            params["status"] = status
        if severity:
            params["severity"] = severity
        if assignee:
            params["assignee"] = assignee
        if keyword:
            params["keyword"] = keyword
        if session_id:
            params["session_id"] = session_id
        return await self.get("/mcp/bugs", params=params)
    
    async def mcp_get_bug(self, bug_id: int) -> dict:
        """获取缺陷详情（MCP 专用）"""
        return await self.get(f"/mcp/bugs/{bug_id}")
    
    async def mcp_create_bug(
        self,
        title: str,
        description: str,
        severity: str = "medium",
        related_task_code: Optional[str] = None,
        steps_to_reproduce: Optional[str] = None,
        expected_behavior: Optional[str] = None,
        actual_behavior: Optional[str] = None,
    ) -> dict:
        """创建缺陷（MCP 专用）"""
        data = {
            "title": title,
            "description": description,
            "severity": severity,
        }
        if related_task_code:
            data["related_task_code"] = related_task_code
        if steps_to_reproduce:
            data["steps_to_reproduce"] = steps_to_reproduce
        if expected_behavior:
            data["expected_behavior"] = expected_behavior
        if actual_behavior:
            data["actual_behavior"] = actual_behavior
        return await self.post("/mcp/bugs", data=data)
    
    async def mcp_update_bug_status(self, bug_id: int, status: str) -> dict:
        """更新缺陷状态（MCP 专用）"""
        return await self.patch(f"/mcp/bugs/{bug_id}/status", params={"status": status})
    
    async def mcp_archive_bug(self, bug_id: int) -> dict:
        """归档缺陷（MCP 专用）"""
        return await self.post(f"/mcp/bugs/{bug_id}/archive")
    
    async def mcp_get_bug_stats(self) -> dict:
        """获取缺陷统计（MCP 专用）"""
        return await self.get("/mcp/bugs/stats")
    
    async def mcp_get_session_bug_stats(self, session_id: int) -> dict:
        """获取会话缺陷统计（MCP 专用）"""
        return await self.get(f"/mcp/bugs/session/{session_id}/stats")
    
    # ============== MCP 进度日志 API ==============
    
    async def create_progress_log(
        self,
        log_type: str,
        summary: str,
        task_code: Optional[str] = None,
        files: Optional[list] = None,
        code_snippet: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        创建进度日志（同步到后端）
        
        Args:
            log_type: 日志类型 (code_change/problem_solved/blocker/note)
            summary: 简要描述
            task_code: 任务编号（可选）
            files: 涉及的文件列表
            code_snippet: 关键代码片段
            metadata: 额外元数据
            
        Returns:
            创建结果包含 log id、task_code 等
        """
        data = {
            "log_type": log_type,
            "summary": summary,
        }
        if task_code:
            data["task_code"] = task_code
        if files:
            data["files"] = files
        if code_snippet:
            data["code_snippet"] = code_snippet[:10000]  # 限制长度
        if metadata:
            data["metadata"] = metadata
        
        return await self.post("/mcp/progress-logs", data=data)
    
    async def list_progress_logs(
        self,
        task_code: Optional[str] = None,
        task_id: Optional[int] = None,
        log_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """
        获取进度日志列表
        
        Args:
            task_code: 任务编号筛选
            task_id: 任务ID筛选
            log_type: 日志类型筛选 (code_change/problem_solved/blocker/note)
            page: 页码
            page_size: 每页数量
            
        Returns:
            进度日志列表和分页信息
        """
        params = {"page": page, "page_size": page_size}
        if task_code:
            params["task_code"] = task_code
        if task_id:
            params["task_id"] = task_id
        if log_type:
            params["log_type"] = log_type
        
        return await self.get("/mcp/progress-logs", params=params)
    
    async def get_progress_log_stats(
        self,
        task_id: Optional[int] = None,
        days: int = 7,
    ) -> dict:
        """
        获取进度日志统计
        
        Args:
            task_id: 任务ID（可选，不传则统计全部）
            days: 统计最近天数（默认7天）
            
        Returns:
            日志统计信息
        """
        params = {"days": days}
        if task_id:
            params["task_id"] = task_id
        
        return await self.get("/mcp/progress-logs/stats", params=params)
    
    async def get_task_progress_summary(self, task_code: str) -> dict:
        """
        获取任务进度摘要
        
        Args:
            task_code: 任务编号
            
        Returns:
            任务进度摘要，包括最近日志、涉及文件、阻塞列表等
        """
        return await self.get(f"/mcp/progress-logs/task/{task_code}/summary")
    
    # MCP 测试任务 API 已废弃（v1.26.0），测试管理统一使用 TestSession
    
    # ============== MCP 工具日志 API ==============
    
    async def log_tool_call(
        self,
        tool_name: str,
        tool_category: str,
        input_params: Optional[dict] = None,
        output_result: Optional[str] = None,
        is_success: bool = True,
        error_message: Optional[str] = None,
        duration_ms: int = 0,
        session_code: Optional[str] = None,
    ) -> Optional[dict]:
        """
        记录 MCP 工具调用日志
        
        Args:
            tool_name: 工具名称
            tool_category: 工具分类 (task/review/bug/docs/suggest/other)
            input_params: 输入参数
            output_result: 输出结果（截断存储）
            is_success: 是否成功
            error_message: 错误信息
            duration_ms: 执行耗时(毫秒)
            session_code: Cursor 会话编码
        
        Returns:
            创建的日志记录，如果失败返回 None
        """
        try:
            data = {
                "tool_name": tool_name,
                "tool_category": tool_category,
                "is_success": is_success,
                "duration_ms": duration_ms,
            }
            
            if input_params:
                data["input_params"] = input_params
            if output_result:
                # 截断过长的输出结果（最多 10000 字符）
                if len(output_result) > 10000:
                    data["output_result"] = output_result[:10000] + "...(truncated)"
                else:
                    data["output_result"] = output_result
            if error_message:
                data["error_message"] = error_message
            if session_code:
                data["session_code"] = session_code
            
            return await self.post("/mcp/tool-logs", data=data)
            
        except Exception as e:
            # 日志记录失败不应影响主流程
            logger.warning(f"记录工具调用日志失败: tool={tool_name}, error={e}")
            return None


    # ============== MCP 任务状态扩展 API ==============
    
    async def pause_task(
        self, 
        task_code: str, 
        reason: Optional[str] = None
    ) -> dict:
        """
        暂停任务（MCP 专用）
        
        Args:
            task_code: 任务编号
            reason: 暂停原因
        
        Returns:
            更新后的任务状态信息
        """
        data = {
            "status": "paused",
            "pause_reason": reason,
        }
        return await self.patch(f"/mcp/tasks/by-code/{task_code}/status/extended", data=data)
    
    async def block_task(
        self, 
        task_code: str, 
        reason: str,
        blocker_log_id: Optional[int] = None
    ) -> dict:
        """
        标记任务为阻塞状态（MCP 专用）
        
        Args:
            task_code: 任务编号
            reason: 阻塞原因（必填）
            blocker_log_id: 关联的 blocker 日志 ID
        
        Returns:
            更新后的任务状态信息
        """
        data = {
            "status": "blocked",
            "blocker_reason": reason,
        }
        if blocker_log_id:
            data["blocker_log_id"] = blocker_log_id
        return await self.patch(f"/mcp/tasks/by-code/{task_code}/status/extended", data=data)
    
    async def resume_task(
        self, 
        task_code: str, 
        comment: Optional[str] = None
    ) -> dict:
        """
        恢复任务（从暂停/阻塞状态恢复为进行中）（MCP 专用）
        
        Args:
            task_code: 任务编号
            comment: 恢复备注
        
        Returns:
            更新后的任务状态信息
        """
        data = {
            "status": "in_progress",
            "comment": comment or "任务已恢复",
        }
        return await self.patch(f"/mcp/tasks/by-code/{task_code}/status/extended", data=data)
    
    # ============== MCP 时间追踪 API（Agent 5 新增） ==============
    
    async def create_time_entry(
        self,
        task_code: str,
        duration_minutes: int,
        description: Optional[str] = None,
        entry_type: str = "coding",
        started_at: Optional[str] = None,
    ) -> dict:
        """
        创建时间条目（MCP 专用）
        
        用于记录任务的工时。
        
        Args:
            task_code: 任务编号
            duration_minutes: 时长（分钟）
            description: 工作内容描述
            entry_type: 时间类型 (coding/review/testing/meeting/other)
            started_at: 开始时间（ISO格式，可选）
        
        Returns:
            创建的时间条目
        """
        data = {
            "duration_minutes": duration_minutes,
            "entry_type": entry_type,
        }
        if description:
            data["description"] = description
        if started_at:
            data["started_at"] = started_at
        
        result = await self.post(f"/mcp/tasks/{task_code}/time-entries", data=data)
        return result.get("data", result)
    
    async def get_time_summary(self, task_code: str) -> dict:
        """
        获取任务时间汇总（MCP 专用）
        
        Args:
            task_code: 任务编号
        
        Returns:
            时间汇总信息，包含总工时、按类型统计、按用户统计等
        """
        result = await self.get(f"/mcp/tasks/{task_code}/time-summary")
        return result.get("data", result)
    
    async def refresh_task_status(self, task_code: str) -> dict:
        """
        刷新任务状态（从后端获取最新状态）（MCP 专用）
        
        用于上下文同步，确保本地状态与后端一致。
        
        Args:
            task_code: 任务编号
        
        Returns:
            任务的最新状态信息
        """
        result = await self.get_task_by_code(task_code)
        return result.get("data", result) if isinstance(result, dict) else result
    
    # ============== MCP 文档中心 API (DevDocHub) ==============
    
    async def list_dev_documents(
        self,
        doc_type: Optional[str] = None,
        status: Optional[str] = None,
        module_name: Optional[str] = None,
        task_code: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """
        获取文档列表（MCP 专用）
        
        Args:
            doc_type: 文档类型筛选 (architecture/data_model/api_design/...)
            status: 状态筛选 (draft/published/archived)
            module_name: 模块名称筛选
            task_code: 关联任务筛选
            keyword: 关键词搜索（标题/摘要）
            page: 页码
            page_size: 每页数量
        
        Returns:
            文档列表和分页信息
        """
        params = {"page": page, "page_size": page_size}
        if doc_type:
            params["doc_type"] = doc_type
        if status:
            params["status"] = status
        if module_name:
            params["module_name"] = module_name
        if task_code:
            params["task_code"] = task_code
        if keyword:
            params["keyword"] = keyword
        
        return await self.get("/mcp/dev-documents", params=params)
    
    async def get_dev_document(self, doc_code: str) -> dict:
        """
        获取文档详情（MCP 专用）
        
        Args:
            doc_code: 文档编号 (如 DOC-001)
        
        Returns:
            文档详情
        """
        return await self.get(f"/mcp/dev-documents/{doc_code}")
    
    async def create_dev_document(
        self,
        title: str,
        doc_type: str,
        content: str,
        summary: Optional[str] = None,
        module_name: Optional[str] = None,
        task_code: Optional[str] = None,
        tags: Optional[list] = None,
        is_ai_generated: bool = True,
        status: str = "draft",
    ) -> dict:
        """
        创建文档（MCP 专用）
        
        Args:
            title: 文档标题
            doc_type: 文档类型 (architecture/data_model/api_design/technical_memo/
                      problem_record/change_summary/implementation/best_practice)
            content: Markdown 内容
            summary: 摘要（可选，自动生成）
            module_name: 所属模块
            task_code: 关联任务编号
            tags: 标签列表
            is_ai_generated: 是否由 AI 生成
            status: 状态 (draft/published)
        
        Returns:
            创建的文档信息
        """
        data = {
            "title": title,
            "doc_type": doc_type,
            "content": content,
            "is_ai_generated": is_ai_generated,
            "status": status,
        }
        if summary:
            data["summary"] = summary
        if module_name:
            data["module_name"] = module_name
        if task_code:
            data["task_code"] = task_code
        if tags:
            data["tags"] = tags
        
        return await self.post("/mcp/dev-documents", data=data)
    
    async def update_dev_document(
        self,
        doc_code: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        summary: Optional[str] = None,
        module_name: Optional[str] = None,
        tags: Optional[list] = None,
        status: Optional[str] = None,
        change_note: Optional[str] = None,
    ) -> dict:
        """
        更新文档（MCP 专用）
        
        更新时会自动创建新版本（如果内容有变化）
        
        Args:
            doc_code: 文档编号
            title: 文档标题
            content: Markdown 内容
            summary: 摘要
            module_name: 所属模块
            tags: 标签列表
            status: 状态 (draft/published/archived)
            change_note: 变更说明（用于版本记录）
        
        Returns:
            更新后的文档信息
        """
        data = {}
        if title is not None:
            data["title"] = title
        if content is not None:
            data["content"] = content
        if summary is not None:
            data["summary"] = summary
        if module_name is not None:
            data["module_name"] = module_name
        if tags is not None:
            data["tags"] = tags
        if status is not None:
            data["status"] = status
        if change_note is not None:
            data["change_note"] = change_note
        
        return await self.put(f"/mcp/dev-documents/{doc_code}", data=data)
    
    async def delete_dev_document(self, doc_code: str) -> dict:
        """
        删除文档（MCP 专用）
        
        Args:
            doc_code: 文档编号
        
        Returns:
            删除结果
        """
        return await self.delete(f"/mcp/dev-documents/{doc_code}")
    
    async def publish_dev_document(self, doc_code: str) -> dict:
        """
        发布文档（MCP 专用）
        
        将草稿状态的文档发布为已发布状态
        
        Args:
            doc_code: 文档编号
        
        Returns:
            发布结果
        """
        return await self.post(f"/mcp/dev-documents/{doc_code}/publish")
    
    async def archive_dev_document(self, doc_code: str) -> dict:
        """
        归档文档（MCP 专用）
        
        将文档归档，归档后不会在默认列表中显示
        
        Args:
            doc_code: 文档编号
        
        Returns:
            归档结果
        """
        return await self.post(f"/mcp/dev-documents/{doc_code}/archive")
    
    async def unarchive_dev_document(self, doc_code: str) -> dict:
        """
        取消归档（MCP 专用）
        
        将已归档的文档恢复为草稿状态
        
        Args:
            doc_code: 文档编号
        
        Returns:
            取消归档结果
        """
        return await self.post(f"/mcp/dev-documents/{doc_code}/unarchive")
    
    async def restore_dev_document_version(
        self,
        doc_code: str,
        version: int,
        change_note: Optional[str] = None,
    ) -> dict:
        """
        恢复到历史版本（MCP 专用）
        
        将文档内容恢复到指定的历史版本，当前内容会作为新版本保存
        
        Args:
            doc_code: 文档编号
            version: 版本号
            change_note: 变更说明
        
        Returns:
            恢复结果
        """
        data = {}
        if change_note:
            data["change_note"] = change_note
        return await self.post(
            f"/mcp/dev-documents/{doc_code}/versions/{version}/restore",
            data=data if data else None,
        )
    
    async def list_dev_document_versions(
        self,
        doc_code: str,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """
        获取文档版本列表（MCP 专用）
        
        Args:
            doc_code: 文档编号
            page: 页码
            page_size: 每页数量
        
        Returns:
            版本列表
        """
        params = {"page": page, "page_size": page_size}
        return await self.get(f"/mcp/dev-documents/{doc_code}/versions", params=params)
    
    async def get_dev_document_version(
        self,
        doc_code: str,
        version: int,
    ) -> dict:
        """
        获取文档历史版本内容（MCP 专用）
        
        Args:
            doc_code: 文档编号
            version: 版本号
        
        Returns:
            版本内容
        """
        return await self.get(f"/mcp/dev-documents/{doc_code}/versions/{version}")
    
    async def get_documents_by_task_code(self, task_code: str) -> dict:
        """
        根据任务编号获取关联文档列表
        
        便捷方法，用于快速获取指定任务的所有关联文档。
        
        Args:
            task_code: 任务编号 (如 TASK-001)
        
        Returns:
            文档列表和分页信息
        """
        return await self.list_dev_documents(task_code=task_code)
    
    async def search_dev_documents(
        self,
        query: str,
        doc_type: Optional[str] = None,
        module_name: Optional[str] = None,
        limit: int = 10,
    ) -> dict:
        """
        全文搜索文档（MCP 专用）
        
        Args:
            query: 搜索关键词
            doc_type: 文档类型筛选
            module_name: 模块名称筛选
            limit: 返回数量限制
        
        Returns:
            搜索结果
        """
        params = {"query": query, "page_size": limit}  # 后端使用 page_size 参数
        if doc_type:
            params["doc_type"] = doc_type
        if module_name:
            params["module_name"] = module_name
        
        return await self.get("/mcp/dev-documents/search", params=params)
    
    async def list_document_comments(self, doc_code: str) -> dict:
        """
        获取文档评论列表（MCP 专用）
        
        返回文档的所有评论，支持树形结构（父子评论）
        
        Args:
            doc_code: 文档编号 (如 DOC-001)
        
        Returns:
            评论列表（树形结构）
        """
        return await self.get(f"/mcp/dev-documents/{doc_code}/comments")
    
    async def add_document_comment(
        self,
        doc_code: str,
        content: str,
        parent_id: Optional[int] = None,
    ) -> dict:
        """
        添加文档评论（MCP 专用）
        
        为文档添加评论，支持回复（指定 parent_id）
        
        Args:
            doc_code: 文档编号 (如 DOC-001)
            content: 评论内容
            parent_id: 父评论 ID（用于回复）
        
        Returns:
            创建的评论信息
        """
        data = {"content": content}
        if parent_id:
            data["parent_id"] = parent_id
        return await self.post(f"/mcp/dev-documents/{doc_code}/comments", data=data)
    
    async def delete_document_comment(
        self,
        doc_code: str,
        comment_id: int,
    ) -> dict:
        """
        删除文档评论（MCP 专用）
        
        删除指定的评论
        
        Args:
            doc_code: 文档编号 (如 DOC-001)
            comment_id: 评论 ID
        
        Returns:
            删除结果
        """
        return await self.delete(f"/mcp/dev-documents/{doc_code}/comments/{comment_id}")
    
    # ============== MCP 测试会话 API ==============
    
    async def list_test_sessions(
        self,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """
        获取测试会话列表（MCP 专用）
        
        Args:
            status: 状态筛选 (planning/in_progress/completed/archived)
            page: 页码
            page_size: 每页数量
        
        Returns:
            测试会话列表和分页信息
        """
        params = {"page": page, "page_size": page_size}
        if status:
            params["status"] = status
        
        result = await self.get("/mcp/test-sessions", params=params)
        return result.get("data", result)
    
    # ============== MCP 测试项 API ==============
    
    async def submit_test_items(
        self,
        test_session_id: int,
        cases: list,
        task_code: Optional[str] = None,
    ) -> dict:
        """
        批量提交测试用例到测试会话（MCP 专用）
        
        Args:
            test_session_id: 测试会话 ID
            cases: 测试用例列表，每个用例包含:
                - title: 测试场景/标题（必填）
                - steps: 测试步骤
                - expected_result: 预期结果
                - focus_points: 观察重点
                - category: 分类
                - priority: 优先级 (P0/P1/P2/P3)
                - estimated_minutes: 预计时间（分钟）
            task_code: 关联任务编号（可选）
        
        Returns:
            创建结果，包含 created_count 和 items
        """
        data = {
            "test_session_id": test_session_id,
            "cases": cases,
        }
        if task_code:
            data["task_code"] = task_code
        
        result = await self.post("/mcp/test-items/submit", data=data)
        return result.get("data", result)
    
    async def list_test_items(
        self,
        test_session_id: Optional[int] = None,
        task_code: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """
        查询测试项列表（MCP 专用）
        
        Args:
            test_session_id: 测试会话 ID（可选）
            task_code: 任务编号（可选）
            status: 状态筛选 (pending/testing/passed/failed/blocked/skipped)
            page: 页码
            page_size: 每页数量
        
        Returns:
            测试项列表和分页信息
        """
        params = {"page": page, "page_size": page_size}
        if test_session_id:
            params["test_session_id"] = test_session_id
        if task_code:
            params["task_code"] = task_code
        if status:
            params["status"] = status
        
        result = await self.get("/mcp/test-items", params=params)
        return result.get("data", result)
    
    async def update_test_item_result(
        self,
        item_id: int,
        status: str,
        actual_result: Optional[str] = None,
        screenshots: Optional[list] = None,
    ) -> dict:
        """
        更新测试项执行结果（MCP 专用）
        
        Args:
            item_id: 测试项 ID
            status: 新状态 (pending/testing/passed/failed/blocked/skipped)
            actual_result: 实际结果/备注
            screenshots: 截图 URL 列表
        
        Returns:
            更新结果
        """
        data = {"status": status}
        if actual_result:
            data["actual_result"] = actual_result
        if screenshots:
            data["screenshots"] = screenshots
        
        result = await self.put(f"/mcp/test-items/{item_id}/result", data=data)
        return result.get("data", result)
    
    async def get_test_report(
        self,
        test_session_id: int,
    ) -> dict:
        """
        生成测试报告（MCP 专用）
        
        Args:
            test_session_id: 测试会话 ID
        
        Returns:
            测试报告，包含 summary, by_status, by_priority, items
        """
        params = {"test_session_id": test_session_id}
        result = await self.get("/mcp/test-items/report", params=params)
        return result.get("data", result)


# 兼容旧代码的别名
TestHubClient = TestHubAPIClient

