"""
核心工具集

简化的工具入口，整合多个工具为统一操作：
- testhub_start: 开始/切换任务
- testhub_finish: 一站式完成开发
- testhub_log: 记录开发进度
- testhub_status: 综合状态查看
"""

from datetime import datetime
from typing import Optional
from mcp.types import Tool, TextContent
from loguru import logger

from ..api_client import TestHubClient, APIError
from ..context import get_context, MCPContext


# ==================== 工具定义 ====================


def start_tool() -> Tool:
    """定义开始任务工具"""
    return Tool(
        name="testhub_start",
        description="""开始/切换到指定任务。

**使用场景**：
- 开始新任务前
- 切换到另一个任务
- 恢复之前的任务

**自动执行**：
1. 获取任务详情
2. 更新任务状态为"进行中"
3. 切换上下文到该任务
4. 返回任务详情和验收标准

**参数说明**：
- task_code: 任务编号（如 TASK-001）
- create_if_not_exist: 如果任务不存在是否自动创建（默认 false）
- title: 创建时的标题（仅在 create_if_not_exist=true 时使用）

**示例**：
当用户说"开始 TASK-042"或"切换到 TASK-001"时调用此工具。""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号，如 TASK-001"
                },
                "create_if_not_exist": {
                    "type": "boolean",
                    "default": False,
                    "description": "任务不存在时是否自动创建"
                },
                "title": {
                    "type": "string",
                    "description": "创建时的标题（仅在 create_if_not_exist=true 时使用）"
                }
            },
            "required": ["task_code"]
        }
    )


def finish_tool() -> Tool:
    """定义一站式完成工具"""
    return Tool(
        name="testhub_finish",
        description="""一站式完成开发任务。

**使用场景**：
- 开发功能完成后
- Bug 修复完成后
- 重构完成后

**自动执行**：
1. 更新任务状态为"已完成"
2. 生成变更摘要文档（DevDocument）
3. 建议测试点（可选）

**参数说明**：
- task_code: 可选，不传则使用当前任务
- change_summary: 变更摘要，我可以根据对话自动生成
- files_changed: 本次修改的文件列表
- test_points: 建议的测试点
- completion_note: 完成备注

**示例**：
当用户说"开发完成了"、"Bug 修好了"或"可以提交了"时调用此工具。""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号（可选；不传则默认使用当前上下文中的任务）"
                },
                "change_summary": {
                    "type": "string",
                    "description": "变更摘要（AI 可根据对话自动生成）"
                },
                "files_changed": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "修改的文件列表"
                },
                "test_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "建议的测试点"
                },
                "completion_note": {
                    "type": "string",
                    "description": "完成备注"
                }
            },
            "required": []
        }
    )


def log_tool() -> Tool:
    """定义进度记录工具"""
    return Tool(
        name="testhub_log",
        description="""记录开发过程中的进度和问题。

**使用场景**：
- 完成了某个代码变更
- 解决了一个问题
- 遇到了阻塞
- 需要记录备忘
- 执行 Git 提交后记录

**日志类型**：
- code_change: 代码变更
- problem_solved: 解决的问题
- blocker: 阻塞问题
- note: 备忘笔记
- git_commit: Git 提交记录

**参数说明**：
- type: 日志类型
- summary: 简要描述
- files: 涉及的文件列表
- code_snippet: 关键代码片段（可选）
- commit_hash: Git 提交哈希（git_commit 类型时使用）

**示例**：
开发过程中我会自动调用此工具记录重要变更。
执行 git commit 后调用: testhub_log(type="git_commit", summary="提交信息", files=["文件列表"], commit_hash="abc123")""",
        inputSchema={
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["code_change", "problem_solved", "blocker", "note", "git_commit"],
                    "description": "日志类型"
                },
                "summary": {
                    "type": "string",
                    "description": "简要描述"
                },
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "涉及的文件列表"
                },
                "code_snippet": {
                    "type": "string",
                    "description": "关键代码片段（可选）"
                },
                "task_code": {
                    "type": "string",
                    "description": "任务编号（可选，默认当前任务）"
                },
                "commit_hash": {
                    "type": "string",
                    "description": "Git 提交哈希（git_commit 类型时使用）"
                }
            },
            "required": ["type", "summary"]
        }
    )


def status_tool() -> Tool:
    """定义综合状态查看工具"""
    return Tool(
        name="testhub_status",
        description="""查看当前工作状态和待办事项。

**使用场景**：
- 开始一天的工作
- 查看当前任务状态
- 准备收工前检查
- 了解待办事项

**查看范围**：
- current: 当前任务状态
- daily: 今日工作摘要
- weekly: 本周工作概览

**返回内容**：
- 当前任务信息
- 待处理任务列表
- 待验证缺陷
- 待审阅评审
- 智能建议（可选）

**示例**：
当用户说"今天有什么任务"、"查看状态"或"工作摘要"时调用此工具。""",
        inputSchema={
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "enum": ["current", "daily", "weekly"],
                    "default": "daily",
                    "description": "查看范围：current(当前任务)、daily(今日摘要)、weekly(本周概览)"
                },
                "include_suggestions": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否包含智能建议"
                }
            }
        }
    )


def pause_tool() -> Tool:
    """定义暂停任务工具"""
    return Tool(
        name="testhub_pause",
        description="""暂停当前任务。

**使用场景**：
- 临时切换到其他更紧急的任务
- 需要等待外部依赖（不是阻塞）
- 下班或需要休息时保存进度
- 计划稍后继续的情况

**与阻塞的区别**：
- 暂停（pause）：主动选择暂停，随时可以恢复
- 阻塞（block）：被动遇到问题，需要解决后才能继续

**参数说明**：
- task_code: 任务编号（可选，默认使用当前任务）
- reason: 暂停原因（可选）

**示例**：
当用户说"暂停任务"、"先放一下"、"等会继续"时调用此工具。""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号（可选，默认使用当前任务）"
                },
                "reason": {
                    "type": "string",
                    "description": "暂停原因"
                }
            }
        }
    )


def block_tool() -> Tool:
    """定义标记阻塞工具"""
    return Tool(
        name="testhub_block",
        description="""标记任务为阻塞状态。

**使用场景**：
- 遇到技术问题无法继续
- 等待他人提供信息或资源
- 外部依赖未就绪
- 需要请求帮助才能继续

**与暂停的区别**：
- 暂停（pause）：主动选择暂停，随时可以恢复
- 阻塞（block）：被动遇到问题，需要解决后才能继续

**参数说明**：
- task_code: 任务编号（可选，默认使用当前任务）
- reason: 阻塞原因（必填）

**自动行为**：
- 会自动记录一条 blocker 类型的进度日志
- 更新任务状态为阻塞

**示例**：
当用户说"任务卡住了"、"遇到问题无法继续"、"需要等待XX"时调用此工具。""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号（可选，默认使用当前任务）"
                },
                "reason": {
                    "type": "string",
                    "description": "阻塞原因（必填）"
                }
            },
            "required": ["reason"]
        }
    )


def resume_tool() -> Tool:
    """定义恢复任务工具"""
    return Tool(
        name="testhub_resume",
        description="""恢复暂停或阻塞的任务。

**使用场景**：
- 从暂停状态恢复继续工作
- 阻塞问题已解决，可以继续
- 重新开始之前中断的任务

**参数说明**：
- task_code: 任务编号（可选，默认使用当前任务）
- comment: 恢复备注（可选，如"阻塞问题已解决"）

**自动行为**：
- 将任务状态从 blocked/paused 改为 in_progress
- 更新本地上下文

**示例**：
当用户说"继续任务"、"问题解决了"、"恢复工作"时调用此工具。""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号（可选，默认使用当前任务）"
                },
                "comment": {
                    "type": "string",
                    "description": "恢复备注（如'阻塞问题已解决'）"
                }
            }
        }
    )


# ==================== 工具处理器 ====================


async def handle_start(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理开始任务"""
    task_code = args.get("task_code")
    create_if_not_exist = args.get("create_if_not_exist", False)
    title = args.get("title")
    
    if not task_code:
        return [TextContent(type="text", text="❌ 请提供任务编号")]
    
    try:
        ctx = get_context()
        conflict_warning = None
        
        # 检查是否切换任务（需要同步当前任务的时间）
        if ctx.current_task_code and ctx.current_task_code != task_code:
            # 获取当前任务耗时
            elapsed_seconds, elapsed_str = ctx.finish_task_timer()
            
            # 如果有耗时，可选地同步到后端
            if elapsed_seconds > 60:  # 超过1分钟才同步
                try:
                    await client.create_time_entry(
                        task_code=ctx.current_task_code,
                        duration_minutes=max(1, elapsed_seconds // 60),
                        description=f"任务切换前累计工时（本地追踪）",
                        entry_type="coding",
                    )
                except Exception as e:
                    logger.warning(f"同步时间条目失败: {e}")
        
        # 尝试开始任务
        try:
            result = await client.start_task(task_code)
            task = result.get("task", {})
        except APIError as e:
            # 任务不存在，检查是否需要创建
            if "不存在" in str(e) and create_if_not_exist and title:
                # 创建新任务
                new_task = await client.create_task(
                    title=title,
                    task_type="feature",
                    assign_to_me=True,
                )
                # 开始新创建的任务
                new_task_code = new_task.get("task_code")
                result = await client.start_task(new_task_code)
                task = result.get("task", {})
                task_code = new_task_code
            else:
                raise
        
        # 检查状态冲突（Agent 5：上下文同步）
        backend_status = task.get("status", "in_progress")
        conflict_warning = ctx.check_status_conflict(backend_status)
        
        # 更新上下文，包含后端状态
        ctx.set_current_task(
            task.get("task_code", task_code), 
            task.get("title"),
            backend_status=backend_status
        )
        ctx.record_task_started()
        
        # 开始任务计时（Agent 5：时间追踪）
        ctx.start_task_timer()
        
        # 状态标签映射
        status_labels = {
            "pending": "待开发 🔵",
            "in_progress": "开发中 🟡",
            "review": "待评审 🟠",
            "testing": "测试中 🟣",
            "completed": "已完成 ✅",
            "blocked": "阻塞 🔴",
            "paused": "已暂停 ⏸️",
        }
        
        # 复杂度图标
        complexity_icons = {
            "S": "🟢 简单",
            "M": "🟡 中等",
            "L": "🔴 复杂",
        }
        
        status = task.get("status", "in_progress")
        complexity = task.get("complexity", "M")
        
        output = f"""🚀 **任务已开始！**

**编号**：{task.get('task_code', task_code)}
**标题**：{task.get('title', '-')}
**状态**：{status_labels.get(status, status)}
**复杂度**：{complexity_icons.get(complexity, complexity)}
**模块**：{task.get('module', '-')}
**计时**：⏱️ 已开始计时

---

**描述**：
{task.get('description') or '（无）'}

**验收标准**：
{task.get('acceptance_criteria') or '（无）'}

**技术备注**：
{task.get('technical_notes') or '（无）'}
"""
        
        # 标签
        tags = task.get('tags') or []
        if tags:
            output += f"\n**标签**：{', '.join(tags)}\n"
        
        # 状态冲突警告（Agent 5：上下文同步）
        if conflict_warning:
            output += f"""
---

⚠️ **状态冲突警告**：
{conflict_warning}
"""
        
        # L 级任务提醒
        if complexity == 'L':
            output += """
---

⚠️ **注意**：这是 L 级复杂任务，建议：
1. 确认设计文档已完成
2. 拆分为多个子任务
3. 定期使用 `testhub_log` 记录进度
"""
        else:
            output += """
---

💡 **提示**：
- 开发过程中可使用 `testhub_log` 记录进度
- 完成后使用 `testhub_finish` 一键完成（包含耗时统计）
"""
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 开始任务失败: {str(e)}")]
    except Exception as e:
        logger.error(f"开始任务失败: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 开始任务失败: {str(e)}")]


async def handle_finish(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理一站式完成（v1.27.0 简化：移除评审，专注文档）"""
    task_code = args.get("task_code")
    change_summary = args.get("change_summary")
    files_changed = args.get("files_changed") or []
    test_points = args.get("test_points") or []
    completion_note = args.get("completion_note")
    
    # 获取当前任务和上下文
    ctx = get_context()
    if not task_code:
        task_code = ctx.current_task_code
    
    if not task_code:
        return [TextContent(
            type="text",
            text="❌ 错误：请提供 task_code 或先使用 `testhub_start` 设置当前任务"
        )]
    
    try:
        output_parts = []
        
        # Agent 5：完成时间追踪，获取耗时
        elapsed_seconds = 0
        elapsed_str = "0分钟"
        task_start_time_for_sync = None
        actual_hours = None
        if ctx.current_task_code == task_code and ctx.task_start_time:
            task_start_time_for_sync = ctx.task_start_time
            elapsed_seconds, elapsed_str = ctx.finish_task_timer()
            # 计算实际工时（四舍五入到小时）
            if elapsed_seconds > 0:
                actual_hours = max(1, round(elapsed_seconds / 3600))
        
        # 1. 使用 finish_task API 一站式完成
        # 后端会自动：生成变更摘要文档（DevDocument）
        result = await client.finish_task(
            task_code=task_code,
            change_summary=change_summary,
            files_changed=files_changed,
            test_points=test_points,
            completion_note=completion_note,
            actual_hours=actual_hours,
        )
        
        output_parts.append(f"""✅ **任务已完成！**

**编号**：{task_code}
**状态**：已完成 ✅
**本次耗时**：⏱️ {elapsed_str}
""")
        
        if completion_note:
            output_parts.append(f"**完成备注**：{completion_note}\n")
        
        # Agent 5：同步时间到后端
        if elapsed_seconds > 60:  # 超过1分钟才同步
            try:
                await client.create_time_entry(
                    task_code=task_code,
                    duration_minutes=max(1, elapsed_seconds // 60),
                    description=f"任务完成 - 本地追踪耗时",
                    entry_type="coding",
                    started_at=task_start_time_for_sync,
                )
                output_parts.append("✅ 工时已同步到后端\n")
            except Exception as e:
                logger.warning(f"同步时间条目失败: {e}")
                output_parts.append(f"⚠️ 工时同步失败（不影响任务完成）\n")
        
        
        # 3. 处理 DevDocument（v1.23.0 新增）
        dev_document = result.get("dev_document")
        if dev_document:
            doc_code = dev_document.get("doc_code")
            output_parts.append(f"""
📄 **开发文档已创建**
**文档编号**：{doc_code}
""")
        
        # 4. 处理测试点建议（v1.26.0 简化：不再自动创建测试任务）
        # 开发会话创建时已自动绑定测试会话，测试项由测试人员手动创建
        if test_points:
            output_parts.append("""
---

🧪 **建议测试点**：
""")
            for i, point in enumerate(test_points[:10], 1):
                output_parts.append(f"  {i}. {point}\n")
            if len(test_points) > 10:
                output_parts.append(f"  _... 还有 {len(test_points) - 10} 个测试点_\n")
            output_parts.append("\n💡 _提示：可在关联的测试会话中创建测试项_\n")
        
        # 5. 下一步提示
        output_parts.append("""
---

💡 **下一步**：
""")
        
        output_parts.append("- 使用 `testhub_docs` 管理开发文档\n")
        output_parts.append("- 使用 `testhub_status` 查看更多任务\n")
        output_parts.append("- 使用 `testhub_start` 开始下一个任务\n")
        
        # 更新上下文
        ctx.record_task_completed(task_code=task_code)
        ctx.clear_current_task()
        
        return [TextContent(type="text", text="".join(output_parts))]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 完成任务失败: {str(e)}")]
    except Exception as e:
        logger.error(f"完成任务失败: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 完成任务失败: {str(e)}")]


def _build_change_summary_doc(
    change_summary: Optional[str],
    files_changed: list[str],
    test_points: list[str],
    elapsed_time: Optional[str] = None,  # Agent 5: 添加耗时信息
) -> str:
    """构建变更摘要文档内容"""
    parts = ["# 变更摘要\n"]
    
    if change_summary:
        parts.append(f"## 概述\n\n{change_summary}\n")
    
    if files_changed:
        parts.append("\n## 修改文件\n")
        for f in files_changed:
            parts.append(f"- `{f}`\n")
    
    if test_points:
        parts.append("\n## 建议测试点\n")
        for i, point in enumerate(test_points, 1):
            parts.append(f"{i}. {point}\n")
    
    # Agent 5: 添加耗时信息
    footer_parts = []
    if elapsed_time:
        footer_parts.append(f"开发耗时: {elapsed_time}")
    footer_parts.append(f"生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    parts.append(f"\n---\n_由 AI 自动生成 | {' | '.join(footer_parts)}_\n")
    
    return "".join(parts)


async def handle_log(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理进度记录 - 同步到后端，本地文件作为备份"""
    log_type = args.get("type")
    summary = args.get("summary")
    files = args.get("files") or []
    code_snippet = args.get("code_snippet")
    task_code = args.get("task_code")
    commit_hash = args.get("commit_hash")  # Git 提交哈希
    
    if not log_type or not summary:
        return [TextContent(type="text", text="❌ 请提供日志类型和描述")]
    
    # 获取当前任务
    ctx = get_context()
    if not task_code:
        task_code = ctx.current_task_code
    
    # 日志类型图标
    type_icons = {
        "code_change": "📝",
        "problem_solved": "✅",
        "blocker": "🔴",
        "note": "📌",
        "git_commit": "🔀",
    }
    
    type_labels = {
        "code_change": "代码变更",
        "problem_solved": "问题解决",
        "blocker": "阻塞问题",
        "note": "备忘",
        "git_commit": "Git 提交",
    }
    
    icon = type_icons.get(log_type, "📋")
    label = type_labels.get(log_type, log_type)
    
    # 构建元数据（用于存储额外信息）
    metadata = {}
    if commit_hash:
        metadata["commit_hash"] = commit_hash
    
    # 构建日志条目（用于本地备份）
    log_entry = {
        "type": log_type,
        "summary": summary,
        "files": files,
        "code_snippet": code_snippet,
        "task_code": task_code,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata if metadata else None,
    }
    
    # 1. 同步到后端（主要）
    sync_success = False
    sync_log_id = None
    sync_error = None
    
    try:
        result = await _sync_progress_log_to_backend(
            client=client,
            log_type=log_type,
            summary=summary,
            task_code=task_code,
            files=files,
            code_snippet=code_snippet,
            metadata=metadata if metadata else None,
        )
        if result:
            sync_success = True
            sync_log_id = result.get("id")
            log_entry["synced"] = True
            log_entry["backend_id"] = sync_log_id
    except Exception as e:
        sync_error = str(e)
        logger.warning(f"同步进度日志到后端失败: {e}")
    
    # 2. 存储到本地上下文（备份/离线缓存）
    _store_progress_log(ctx, log_entry)
    
    # 构建输出
    output = f"""{icon} **进度已记录**

**类型**：{label}
**描述**：{summary}
"""
    
    if task_code:
        output += f"**关联任务**：{task_code}\n"
    
    if commit_hash:
        output += f"**提交哈希**：`{commit_hash}`\n"
    
    if files:
        output += f"**涉及文件**：{', '.join(files)}\n"
    
    if code_snippet:
        output += f"\n**代码片段**：\n```\n{code_snippet[:500]}{'...' if len(code_snippet) > 500 else ''}\n```\n"
    
    # 同步状态
    output += "\n---\n"
    if sync_success:
        output += f"✅ **已同步到 TestHub** (ID: {sync_log_id})\n"
    else:
        output += f"⚠️ **同步失败，已保存到本地**: {sync_error or '未知错误'}\n"
        output += "_日志将在下次操作时自动重试同步_\n"
    
    # 阻塞问题提醒
    if log_type == "blocker":
        output += """
---

⚠️ **阻塞问题提醒**：
- 使用 `testhub_block` 将任务状态更新为阻塞（会同步到 TestHub）
- 问题解决后使用 `testhub_resume` 恢复任务
- 或寻求帮助解决问题
"""
    
    output += f"\n_记录于 {datetime.now().strftime('%H:%M:%S')}_"
    
    return [TextContent(type="text", text=output)]


async def _sync_progress_log_to_backend(
    client: TestHubClient,
    log_type: str,
    summary: str,
    task_code: Optional[str] = None,
    files: Optional[list] = None,
    code_snippet: Optional[str] = None,
    metadata: Optional[dict] = None,
    max_retries: int = 2,
) -> Optional[dict]:
    """
    同步进度日志到后端，带重试逻辑
    
    Args:
        client: API 客户端
        log_type: 日志类型
        summary: 描述
        task_code: 任务编号
        files: 文件列表
        code_snippet: 代码片段
        metadata: 额外元数据（如 commit_hash）
        max_retries: 最大重试次数
        
    Returns:
        成功返回日志信息，失败返回 None
    """
    import asyncio
    
    for attempt in range(max_retries + 1):
        try:
            result = await client.create_progress_log(
                log_type=log_type,
                summary=summary,
                task_code=task_code,
                files=files,
                code_snippet=code_snippet,
                metadata=metadata,
            )
            
            # 从响应中提取数据
            data = result.get("data", result)
            if data and data.get("id"):
                logger.info(f"进度日志已同步到后端: id={data.get('id')}, task_code={task_code}")
                return data
            
            # 响应格式异常，但不报错
            logger.warning(f"进度日志同步响应格式异常: {result}")
            return result
            
        except APIError as e:
            # 400 错误不重试（参数错误）
            if e.status_code and 400 <= e.status_code < 500:
                logger.warning(f"进度日志同步失败 (客户端错误): {e}")
                raise
            
            # 其他错误重试
            if attempt < max_retries:
                wait_time = (attempt + 1) * 1.0  # 指数退避
                logger.warning(f"进度日志同步失败，{wait_time}秒后重试 ({attempt + 1}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                raise
                
        except Exception as e:
            if attempt < max_retries:
                wait_time = (attempt + 1) * 1.0
                logger.warning(f"进度日志同步异常，{wait_time}秒后重试: {e}")
                await asyncio.sleep(wait_time)
            else:
                raise
    
    return None


def _store_progress_log(ctx: MCPContext, log_entry: dict) -> None:
    """存储进度日志到本地上下文"""
    import json
    import os
    from pathlib import Path
    
    # 日志文件路径
    log_file = os.path.join(Path.home(), ".testhub_mcp", "progress_logs.json")
    
    try:
        # 读取现有日志
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        # 添加新日志
        logs.append(log_entry)
        
        # 保留最近 100 条
        if len(logs) > 100:
            logs = logs[-100:]
        
        # 保存
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        logger.warning(f"保存进度日志失败: {e}")


async def handle_status(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理状态查看"""
    scope = args.get("scope", "daily")
    include_suggestions = args.get("include_suggestions", True)
    
    try:
        ctx = get_context()
        output_parts = []
        
        # ========== 团队和用户信息 ==========
        team_info = None
        user_info = None
        try:
            # 尝试从 daily_summary 获取团队信息
            resp = await client.get_daily_summary(limit=1)
            data = resp.get("data", resp) if isinstance(resp, dict) else resp
            if isinstance(data, dict):
                team_info = data.get("team")
                user_info = data.get("user")
        except Exception:
            pass  # 获取失败不影响主流程
        
        if team_info or user_info:
            output_parts.append("🔑 **上下文信息**\n\n")
            
            if team_info:
                team_id = team_info.get("id")
                team_name = team_info.get("name", "未知团队")
                team_code = team_info.get("code", "-")
                output_parts.append(f"- 🏢 **团队**：{team_name}（{team_code}）\n")
                output_parts.append(f"  - ID：{team_id}\n")
            
            if user_info:
                user_id = user_info.get("id")
                user_username = user_info.get("username", "-")
                user_nickname = user_info.get("nickname")
                user_email = user_info.get("email", "-")
                
                # 显示名优先使用昵称，其次用户名
                display_name = user_nickname or user_username or user_email
                output_parts.append(f"- 👤 **用户**：{display_name}\n")
                output_parts.append(f"  - ID：{user_id}\n")
                output_parts.append(f"  - 用户名：{user_username}\n")
                if user_nickname:
                    output_parts.append(f"  - 昵称：{user_nickname}\n")
                output_parts.append(f"  - 邮箱：{user_email}\n")
            
            output_parts.append("\n")
        
        # ========== 当前上下文 ==========
        output_parts.append("📍 **当前状态**\n\n")
        
        if ctx.current_task_code:
            # 获取当前任务最新状态（Agent 5：上下文同步）
            try:
                task_resp = await client.refresh_task_status(ctx.current_task_code)
                task = task_resp if isinstance(task_resp, dict) else {}
                
                status_labels = {
                    "pending": "待开发 🔵",
                    "in_progress": "开发中 🟡",
                    "review": "待评审 🟠",
                    "testing": "测试中 🟣",
                    "completed": "已完成 ✅",
                    "blocked": "阻塞 🔴",
                    "paused": "已暂停 ⏸️",
                }
                
                backend_status = task.get("status", "pending") if task else "unknown"
                
                # Agent 5：检查状态冲突
                conflict = ctx.check_status_conflict(backend_status)
                
                # 更新缓存的后端状态
                ctx.update_backend_status(backend_status)
                
                output_parts.append(f"**当前任务**：{ctx.current_task_code}\n")
                if ctx.current_task_title:
                    output_parts.append(f"  - {ctx.current_task_title}\n")
                output_parts.append(f"  - 状态：{status_labels.get(backend_status, backend_status)}\n")
                
                # Agent 5：显示时间追踪信息
                if ctx.task_start_time:
                    elapsed = ctx.get_task_elapsed_time()
                    elapsed_str = ctx.format_elapsed_time(elapsed)
                    if ctx.is_task_paused:
                        output_parts.append(f"  - ⏸️ 计时已暂停，累计耗时：{elapsed_str}\n")
                    else:
                        output_parts.append(f"  - ⏱️ 进行中，已耗时：{elapsed_str}\n")
                
                # Agent 5：显示状态冲突警告
                if conflict:
                    output_parts.append(f"\n⚠️ **状态冲突警告**：{conflict}\n")
                
                if task and task.get("acceptance_criteria"):
                    output_parts.append(f"\n**验收标准**：\n{task.get('acceptance_criteria')}\n")
                    
            except Exception as e:
                logger.debug(f"获取任务状态失败: {e}")
                output_parts.append(f"**当前任务**：{ctx.current_task_code}\n")
                if ctx.current_task_title:
                    output_parts.append(f"  - {ctx.current_task_title}\n")
                
                # Agent 5：即使获取后端失败，也显示本地时间追踪
                if ctx.task_start_time:
                    elapsed = ctx.get_task_elapsed_time()
                    elapsed_str = ctx.format_elapsed_time(elapsed)
                    if ctx.is_task_paused:
                        output_parts.append(f"  - ⏸️ 计时已暂停，累计耗时：{elapsed_str}\n")
                    else:
                        output_parts.append(f"  - ⏱️ 进行中，已耗时：{elapsed_str}\n")
        else:
            output_parts.append("**当前任务**：无\n")
        
        # 会话统计
        output_parts.append(f"""
**本次会话统计**：
- 开始任务：{ctx.tasks_started} 个
- 完成任务：{ctx.tasks_completed} 个
""")
        
        # ========== 根据 scope 获取更多信息 ==========
        if scope in ["daily", "weekly"]:
            output_parts.append("\n---\n")
            
            # 获取每日摘要
            try:
                limit = 10 if scope == "daily" else 20
                resp = await client.get_daily_summary(limit=limit)
                data = resp.get("data", resp) if isinstance(resp, dict) else resp
                
                tasks = data.get("tasks", {}) if isinstance(data, dict) else {}
                bugs = data.get("bugs_to_verify", {}) if isinstance(data, dict) else {}
                date_str = data.get("date") if isinstance(data, dict) else None
                
                output_parts.append(f"\n📅 **{'今日' if scope == 'daily' else '本周'}工作摘要**（{date_str or '-'}）\n\n")
                
                # 待处理任务
                output_parts.append("## 📋 待处理任务\n")
                task_total = tasks.get("total", 0)
                output_parts.append(f"- 总数：{task_total}\n")
                
                task_items = tasks.get("items") or []
                if task_items:
                    for t in task_items[:5]:  # 最多显示 5 个
                        code = t.get("task_code") or f"#{t.get('id')}"
                        complexity = t.get("complexity", "M")
                        c_icon = {"S": "🟢", "M": "🟡", "L": "🔴"}.get(complexity, "⚪")
                        output_parts.append(f"- {c_icon} **{code}** - {t.get('title', '-')}\n")
                    
                    if task_total > 5:
                        output_parts.append(f"  _... 还有 {task_total - 5} 个任务_\n")
                else:
                    output_parts.append("- （暂无）\n")
                
                # 待验证缺陷
                output_parts.append("\n## 🐛 待验证缺陷\n")
                bug_total = bugs.get("total", 0)
                output_parts.append(f"- 总数：{bug_total}\n")
                
                bug_items = bugs.get("items") or []
                if bug_items:
                    for b in bug_items[:3]:  # 最多显示 3 个
                        severity_icons = {
                            "critical": "💀",
                            "major": "🔥",
                            "minor": "⚠️",
                            "trivial": "📝",
                        }
                        s_icon = severity_icons.get(b.get("severity"), "⚪")
                        output_parts.append(f"- {s_icon} **BUG-{b.get('id')}** - {b.get('title', '-')}\n")
                    
                    if bug_total > 3:
                        output_parts.append(f"  _... 还有 {bug_total - 3} 个缺陷_\n")
                else:
                    output_parts.append("- （暂无）\n")
                
            except Exception as e:
                logger.warning(f"获取每日摘要失败: {e}")
                output_parts.append(f"\n⚠️ 获取详细摘要失败: {e}\n")
        
        # ========== 近期进度日志（从后端获取） ==========
        if ctx.current_task_code:
            await _append_recent_progress_logs(client, ctx.current_task_code, output_parts)
        
        # ========== 智能建议 ==========
        if include_suggestions:
            suggestions = _generate_suggestions(ctx, scope)
            if suggestions:
                output_parts.append("\n---\n\n💡 **建议**\n\n")
                for i, suggestion in enumerate(suggestions, 1):
                    output_parts.append(f"{i}. {suggestion}\n")
        
        # 最近切换的任务
        if ctx.task_history:
            output_parts.append("\n---\n\n**最近任务历史**：\n")
            for item in reversed(ctx.task_history[-3:]):
                title = item.get("title", "")
                if title:
                    output_parts.append(f"- {item['code']} - {title}\n")
                else:
                    output_parts.append(f"- {item['code']}\n")
        
        return [TextContent(type="text", text="".join(output_parts))]
        
    except Exception as e:
        logger.error(f"获取状态失败: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 获取状态失败: {str(e)}")]


def _generate_suggestions(ctx: MCPContext, scope: str) -> list[str]:
    """根据当前状态生成建议"""
    suggestions = []
    
    # 没有当前任务
    if not ctx.current_task_code:
        suggestions.append("当前没有进行中的任务，使用 `testhub_start` 开始一个任务")
    
    # 长时间没有活动
    if ctx.last_activity_time:
        try:
            last_activity = datetime.fromisoformat(ctx.last_activity_time)
            hours_since_activity = (datetime.now() - last_activity).total_seconds() / 3600
            
            if hours_since_activity > 2 and ctx.current_task_code:
                suggestions.append("任务进行中已超过 2 小时，建议使用 `testhub_log` 记录进度")
        except Exception:
            pass
    
    # 开始但未完成较多任务
    if ctx.tasks_started > ctx.tasks_completed + 2:
        suggestions.append("有多个任务已开始但未完成，建议专注完成当前任务")
    
    return suggestions


async def _append_recent_progress_logs(
    client: TestHubClient,
    task_code: str,
    output_parts: list[str],
    limit: int = 5,
) -> None:
    """
    追加当前任务的近期进度日志到输出
    
    Args:
        client: API 客户端
        task_code: 任务编号
        output_parts: 输出部分列表（直接修改）
        limit: 显示条数限制
    """
    try:
        # 从后端获取进度日志
        resp = await client.list_progress_logs(
            task_code=task_code,
            page=1,
            page_size=limit,
        )
        
        data = resp.get("data", resp) if isinstance(resp, dict) else resp
        items = data.get("items", []) if isinstance(data, dict) else []
        total = data.get("total", 0) if isinstance(data, dict) else 0
        
        if not items:
            return
        
        # 日志类型图标
        type_icons = {
            "code_change": "📝",
            "problem_solved": "✅",
            "blocker": "🔴",
            "note": "📌",
        }
        
        output_parts.append(f"\n---\n\n📜 **任务进度日志** ({task_code})\n\n")
        
        for item in items:
            log_type = item.get("log_type", "note")
            icon = type_icons.get(log_type, "📋")
            summary = item.get("summary", "-")
            created_at = item.get("created_at", "")
            
            # 格式化时间
            time_str = ""
            if created_at:
                try:
                    # 尝试解析 ISO 格式时间
                    if isinstance(created_at, str):
                        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        time_str = dt.strftime("%m-%d %H:%M")
                except Exception:
                    time_str = str(created_at)[:16]
            
            # 截断过长的摘要
            if len(summary) > 80:
                summary = summary[:77] + "..."
            
            output_parts.append(f"- {icon} [{time_str}] {summary}\n")
            
            # 显示涉及的文件（如果有）
            files = item.get("files") or []
            if files and len(files) <= 3:
                files_str = ", ".join(f"`{f}`" for f in files[:3])
                output_parts.append(f"  _文件: {files_str}_\n")
        
        if total > limit:
            output_parts.append(f"\n_共 {total} 条日志，显示最近 {limit} 条_\n")
            
    except Exception as e:
        logger.warning(f"获取任务进度日志失败: {e}")
        # 不显示错误，静默失败


async def handle_pause(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理暂停任务"""
    task_code = args.get("task_code")
    reason = args.get("reason")
    
    # 获取当前任务
    ctx = get_context()
    if not task_code:
        task_code = ctx.current_task_code
    
    if not task_code:
        return [TextContent(
            type="text",
            text="❌ 错误：请提供 task_code 或先使用 `testhub_start` 设置当前任务"
        )]
    
    try:
        # 调用 API 暂停任务
        result = await client.pause_task(task_code, reason)
        
        data = result.get("data", result)
        old_status = data.get("old_status", "unknown")
        new_status = data.get("new_status", "paused")
        
        output = f"""⏸️ **任务已暂停**

**编号**：{task_code}
**状态变更**：{old_status} → {new_status}
"""
        
        if reason:
            output += f"**暂停原因**：{reason}\n"
        
        output += """
---

💡 **提示**：
- 使用 `testhub_resume` 可以恢复任务
- 使用 `testhub_start` 可以切换到其他任务
"""
        
        # 记录进度日志
        ctx.add_progress_log(
            log_type="note",
            summary=f"任务暂停" + (f": {reason}" if reason else ""),
            task_code=task_code,
        )
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 暂停任务失败: {str(e)}")]
    except Exception as e:
        logger.error(f"暂停任务失败: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 暂停任务失败: {str(e)}")]


async def handle_block(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理标记阻塞"""
    task_code = args.get("task_code")
    reason = args.get("reason")
    
    if not reason:
        return [TextContent(type="text", text="❌ 请提供阻塞原因")]
    
    # 获取当前任务
    ctx = get_context()
    if not task_code:
        task_code = ctx.current_task_code
    
    if not task_code:
        return [TextContent(
            type="text",
            text="❌ 错误：请提供 task_code 或先使用 `testhub_start` 设置当前任务"
        )]
    
    try:
        # 先记录 blocker 日志
        blocker_entry = ctx.add_progress_log(
            log_type="blocker",
            summary=reason,
            task_code=task_code,
        )
        
        # 调用 API 标记阻塞
        result = await client.block_task(task_code, reason)
        
        data = result.get("data", result)
        old_status = data.get("old_status", "unknown")
        new_status = data.get("new_status", "blocked")
        
        output = f"""🔴 **任务已标记为阻塞**

**编号**：{task_code}
**状态变更**：{old_status} → {new_status}
**阻塞原因**：{reason}

---

⚠️ **阻塞问题已记录**

需要帮助解决吗？可以：
1. 描述具体问题，我可以帮忙分析
2. 使用 `testhub_resume` 恢复任务（问题解决后）
3. 使用 `testhub_start` 切换到其他任务
"""
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 标记阻塞失败: {str(e)}")]
    except Exception as e:
        logger.error(f"标记阻塞失败: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 标记阻塞失败: {str(e)}")]


async def handle_resume(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理恢复任务"""
    task_code = args.get("task_code")
    comment = args.get("comment")
    
    # 获取当前任务
    ctx = get_context()
    if not task_code:
        task_code = ctx.current_task_code
    
    if not task_code:
        return [TextContent(
            type="text",
            text="❌ 错误：请提供 task_code 或先使用 `testhub_start` 设置当前任务"
        )]
    
    try:
        # 调用 API 恢复任务
        result = await client.resume_task(task_code, comment)
        
        data = result.get("data", result)
        old_status = data.get("old_status", "unknown")
        new_status = data.get("new_status", "in_progress")
        
        output = f"""▶️ **任务已恢复**

**编号**：{task_code}
**状态变更**：{old_status} → {new_status}
"""
        
        if comment:
            output += f"**备注**：{comment}\n"
        
        output += """
---

💡 **提示**：
- 继续开发，使用 `testhub_log` 记录进度
- 完成后使用 `testhub_finish` 提交
"""
        
        # 记录进度日志
        ctx.add_progress_log(
            log_type="note",
            summary=f"任务恢复" + (f": {comment}" if comment else ""),
            task_code=task_code,
        )
        
        # 如果之前有阻塞，记录问题解决
        if old_status == "blocked":
            ctx.add_progress_log(
                log_type="problem_solved",
                summary=comment or "阻塞问题已解决",
                task_code=task_code,
            )
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 恢复任务失败: {str(e)}")]
    except Exception as e:
        logger.error(f"恢复任务失败: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 恢复任务失败: {str(e)}")]


# ==================== 工具注册 ====================


def get_all_core_tools() -> list[Tool]:
    """获取所有核心工具定义"""
    return [
        start_tool(),
        finish_tool(),
        log_tool(),
        status_tool(),
        pause_tool(),
        block_tool(),
        resume_tool(),
    ]


# 工具名称到处理器的映射
CORE_TOOL_HANDLERS = {
    "testhub_start": handle_start,
    "testhub_finish": handle_finish,
    "testhub_log": handle_log,
    "testhub_status": handle_status,
    "testhub_pause": handle_pause,
    "testhub_block": handle_block,
    "testhub_resume": handle_resume,
}


async def handle_core_tool(
    client: TestHubClient,
    tool_name: str,
    args: dict
) -> Optional[list[TextContent]]:
    """
    处理核心工具调用
    
    Args:
        client: TestHub API 客户端
        tool_name: 工具名称
        args: 工具参数
        
    Returns:
        处理结果，如果工具名称不匹配则返回 None
    """
    handler = CORE_TOOL_HANDLERS.get(tool_name)
    if handler:
        return await handler(client, args)
    return None

