"""
统一测试工具

支持测试用例管理的各种操作：
- submit: 提交测试用例到测试会话
- list: 查看测试项列表
- update_result: 更新测试项执行结果
- report: 生成测试报告

会话上下文：
- 工具会自动使用 MCP 连接时配置的开发会话 ID
- 如果需要指定其他会话，可以手动传入 test_session_id
"""

from typing import Optional
from mcp.types import Tool, TextContent
from loguru import logger

from ..api_client import TestHubClient, APIError


def get_unified_test_tool() -> Tool:
    """获取统一测试工具定义"""
    return Tool(
        name="testhub_test",
        description="""测试用例管理工具。

**支持的操作**：
- `list_sessions`: 查看测试会话列表（了解有哪些可用的测试会话）
- `submit`: 提交测试用例到测试会话
- `list`: 查看测试项列表
- `update_result`: 更新测试项执行结果
- `report`: 生成测试报告

**会话上下文**：
- 工具会自动使用 MCP 连接时配置的开发会话关联的测试会话
- 如果需要指定其他会话，可以手动传入 test_session_id 覆盖
- 使用 list_sessions 可以查看所有可用的测试会话

**使用示例**：
- 查看测试会话: action="list_sessions"
- 提交测试用例: action="submit", cases=[{"title": "登录功能测试", "steps": "1. 输入用户名..."}]
- 查看测试项: action="list"
- 按任务查询: action="list", task_code="TASK-001"
- 更新结果: action="update_result", item_id=1, status="passed", actual_result="测试通过"
- 生成报告: action="report"

**测试项状态说明**：
- pending: 待测试
- testing: 测试中
- passed: 通过
- failed: 不通过
- blocked: 阻塞
- skipped: 跳过

**测试会话状态说明**：
- planning: 计划中
- in_progress: 进行中
- completed: 已完成
- archived: 已归档

**优先级说明**：
- P0: 最高优先级（阻塞发布）
- P1: 高优先级（核心功能）
- P2: 普通优先级（一般功能）""",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["list_sessions", "submit", "list", "update_result", "report"],
                    "description": "操作类型"
                },
                "test_session_id": {
                    "type": "integer",
                    "description": "测试会话 ID（可选，默认使用当前开发会话关联的测试会话）"
                },
                "session_status": {
                    "type": "string",
                    "enum": ["planning", "in_progress", "completed", "archived"],
                    "description": "测试会话状态筛选（list_sessions 时使用）"
                },
                "task_code": {
                    "type": "string",
                    "description": "任务编号（list 时可选，用于按任务查询）"
                },
                "cases": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "测试场景/标题（必填）"
                            },
                            "steps": {
                                "type": "string",
                                "description": "测试步骤"
                            },
                            "expected_result": {
                                "type": "string",
                                "description": "预期结果"
                            },
                            "focus_points": {
                                "type": "string",
                                "description": "观察重点"
                            },
                            "category": {
                                "type": "string",
                                "description": "分类"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["P0", "P1", "P2"],
                                "description": "优先级"
                            },
                            "estimated_minutes": {
                                "type": "integer",
                                "description": "预计时间（分钟）"
                            }
                        },
                        "required": ["title"]
                    },
                    "description": "测试用例列表（submit 时使用）"
                },
                "item_id": {
                    "type": "integer",
                    "description": "测试项 ID（update_result 时使用）"
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "testing", "passed", "failed", "blocked", "skipped"],
                    "description": "测试状态（update_result 时使用）"
                },
                "actual_result": {
                    "type": "string",
                    "description": "实际结果/备注（update_result 时使用）"
                }
            },
            "required": ["action"]
        }
    )


async def handle_unified_test(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理统一测试工具调用"""
    action = args.get("action")
    
    if not action:
        return [TextContent(type="text", text="❌ 请提供操作类型 (action)")]
    
    handlers = {
        "list_sessions": _handle_list_sessions,
        "submit": _handle_submit,
        "list": _handle_list,
        "update_result": _handle_update_result,
        "report": _handle_report,
    }
    
    handler = handlers.get(action)
    if not handler:
        return [TextContent(
            type="text",
            text=f"❌ 不支持的操作类型: {action}\n支持的操作: {', '.join(handlers.keys())}"
        )]
    
    try:
        return await handler(client, args)
    except APIError as e:
        logger.warning(f"测试工具 API 错误: action={action}, error={e}")
        return [TextContent(type="text", text=f"❌ API 错误: {str(e)}")]
    except Exception as e:
        logger.error(f"测试工具错误: action={action}, error={e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 操作失败: {str(e)}")]


async def _handle_list_sessions(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理查看测试会话列表"""
    session_status = args.get("session_status")
    page = args.get("page", 1)
    page_size = args.get("page_size", 20)
    
    result = await client.list_test_sessions(
        status=session_status,
        page=page,
        page_size=page_size,
    )
    
    items = result.get("items", [])
    total = result.get("total", 0)
    
    # 标记当前使用的会话
    current_session_id = client.default_session_id
    
    output = f"""📋 **测试会话列表**

**总数**: {total}
"""
    
    if current_session_id:
        output += f"**当前开发会话 ID**: {current_session_id}\n"
    
    if session_status:
        output += f"**状态筛选**: {session_status}\n"
    
    output += "\n"
    
    # 找出关联到当前开发会话的测试会话
    linked_test_session = None
    if current_session_id and items:
        for item in items:
            if item.get("linked_dev_session_id") == current_session_id:
                linked_test_session = item
                break
    
    if linked_test_session:
        output += f"✅ **当前开发会话关联的测试会话**: {linked_test_session.get('name')} (ID: {linked_test_session.get('id')})\n\n"
    elif current_session_id:
        output += f"⚠️ **当前开发会话 {current_session_id} 未关联任何测试会话**\n\n"
    
    if items:
        output += "### 测试会话列表\n\n"
        output += "| 测试会话ID | 名称 | 状态 | 关联开发会话 | 测试项 | 创建日期 |\n"
        output += "|------------|------|------|--------------|--------|----------|\n"
        
        for item in items[:15]:
            session_id = item.get("id")
            session_name = item.get("name", "未命名")[:20]
            session_status_val = item.get("status", "planning")
            linked_dev_id = item.get("linked_dev_session_id")
            items_total = item.get("items_total", 0)
            items_completed = item.get("items_completed", 0)
            created = item.get("created_at", "")[:10] if item.get("created_at") else "-"
            
            # 标记当前关联
            if linked_dev_id == current_session_id:
                session_name = f"⭐ {session_name}"
            
            linked_str = str(linked_dev_id) if linked_dev_id else "❌ 未关联"
            items_str = f"{items_completed}/{items_total}" if items_total else "-"
            
            output += f"| {session_id} | {session_name} | {session_status_val} | {linked_str} | {items_str} | {created} |\n"
        
        if total > 15:
            output += f"\n_显示 15/{total} 条，可通过 page 参数翻页_\n"
    else:
        output += "_暂无测试会话_\n"
    
    output += """
---

💡 **提示**:
- 使用 `testhub_test(action="submit", test_session_id=<ID>, cases=[...])` 向指定会话提交测试用例
- 使用 `testhub_test(action="list", test_session_id=<ID>)` 查看指定会话的测试项
- 如果已配置默认会话，可以省略 test_session_id 参数
"""
    
    return [TextContent(type="text", text=output)]


def _get_session_id(client: TestHubClient, args: dict) -> Optional[int]:
    """
    获取测试会话 ID
    
    优先级：
    1. 用户显式传入的 test_session_id
    2. 客户端的 default_session_id（MCP 连接时配置的开发会话 ID）
    """
    test_session_id = args.get("test_session_id")
    if test_session_id:
        return test_session_id
    
    # 使用客户端默认会话 ID
    if client.default_session_id:
        logger.debug(f"使用默认会话 ID: {client.default_session_id}")
        return client.default_session_id
    
    return None


async def _handle_submit(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理提交测试用例"""
    test_session_id = _get_session_id(client, args)
    cases = args.get("cases")
    task_code = args.get("task_code")
    
    if not test_session_id:
        return [TextContent(
            type="text", 
            text="❌ 无法确定测试会话 ID\n\n"
                 "请确保：\n"
                 "1. MCP 连接时已配置开发会话 ID，或\n"
                 "2. 手动传入 test_session_id 参数"
        )]
    
    if not cases or not isinstance(cases, list):
        return [TextContent(type="text", text="❌ 请提供测试用例列表 (cases)")]
    
    # 验证用例格式
    for i, case in enumerate(cases):
        if not isinstance(case, dict) or not case.get("title"):
            return [TextContent(
                type="text",
                text=f"❌ 测试用例 {i + 1} 格式错误: 必须包含 title 字段"
            )]
    
    result = await client.submit_test_items(
        test_session_id=test_session_id,
        cases=cases,
        task_code=task_code,
    )
    
    created_count = result.get("created_count", 0)
    items = result.get("items", [])
    
    output = f"""✅ **测试用例已提交**

**测试会话 ID**: {test_session_id}
**提交数量**: {created_count}
"""
    
    if task_code:
        output += f"**关联任务**: {task_code}\n"
    
    if items:
        output += "\n**创建的测试项**:\n"
        for item in items[:10]:
            priority = item.get("priority", "P1")
            priority_icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢", "P3": "⚪"}.get(priority, "⚪")
            output += f"- {priority_icon} **{item.get('title', '-')}**"
            if item.get("category"):
                output += f" [{item.get('category')}]"
            output += "\n"
        
        if len(items) > 10:
            output += f"  _... 还有 {len(items) - 10} 个测试项_\n"
    
    output += """
---

💡 **下一步**:
- 使用 `testhub_test(action="list", test_session_id=...)` 查看测试项列表
- 使用 `testhub_test(action="update_result", item_id=..., status="passed")` 更新测试结果
"""
    
    return [TextContent(type="text", text=output)]


async def _handle_list(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理查看测试项列表"""
    test_session_id = _get_session_id(client, args)
    task_code = args.get("task_code")
    status = args.get("status")
    
    # 如果有 task_code，可以不需要 session_id
    # 如果都没有，尝试使用默认会话
    if not test_session_id and not task_code:
        return [TextContent(
            type="text",
            text="❌ 无法确定查询范围\n\n"
                 "请确保：\n"
                 "1. MCP 连接时已配置开发会话 ID，或\n"
                 "2. 传入 test_session_id 参数，或\n"
                 "3. 传入 task_code 参数按任务查询"
        )]
    
    result = await client.list_test_items(
        test_session_id=test_session_id,
        task_code=task_code,
        status=status,
    )
    
    items = result.get("items", [])
    total = result.get("total", 0)
    
    output = f"""📋 **测试项列表**

"""
    
    if test_session_id:
        output += f"**测试会话 ID**: {test_session_id}\n"
    if task_code:
        output += f"**关联任务**: {task_code}\n"
    if status:
        output += f"**状态筛选**: {status}\n"
    
    output += f"**总数**: {total}\n\n"
    
    if items:
        # 状态图标
        status_icons = {
            "pending": "⏳",
            "testing": "🔄",
            "passed": "✅",
            "failed": "❌",
            "blocked": "🔴",
            "skipped": "⏭️",
        }
        
        # 优先级图标
        priority_icons = {
            "P0": "🔴",
            "P1": "🟡",
            "P2": "🟢",
            "P3": "⚪",
        }
        
        for item in items[:15]:
            item_status = item.get("status", "pending")
            priority = item.get("priority", "P1")
            s_icon = status_icons.get(item_status, "⚪")
            p_icon = priority_icons.get(priority, "⚪")
            
            output += f"- {s_icon} {p_icon} **{item.get('title', '-')}**"
            if item.get("item_code"):
                output += f" ({item.get('item_code')})"
            output += f"\n  ID: {item.get('id')} | 状态: {item_status}"
            if item.get("category"):
                output += f" | 分类: {item.get('category')}"
            output += "\n"
        
        if total > 15:
            output += f"\n_显示 15/{total} 条，更多请指定筛选条件_\n"
    else:
        output += "_暂无测试项_\n"
    
    return [TextContent(type="text", text=output)]


async def _handle_update_result(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理更新测试项结果"""
    item_id = args.get("item_id")
    status = args.get("status")
    actual_result = args.get("actual_result")
    
    if not item_id:
        return [TextContent(type="text", text="❌ 请提供测试项 ID (item_id)")]
    
    if not status:
        return [TextContent(type="text", text="❌ 请提供状态 (status)")]
    
    valid_statuses = ["pending", "testing", "passed", "failed", "blocked", "skipped"]
    if status not in valid_statuses:
        return [TextContent(
            type="text",
            text=f"❌ 无效的状态: {status}\n有效状态: {', '.join(valid_statuses)}"
        )]
    
    result = await client.update_test_item_result(
        item_id=item_id,
        status=status,
        actual_result=actual_result,
    )
    
    # 状态图标
    status_icons = {
        "pending": "⏳",
        "testing": "🔄",
        "passed": "✅",
        "failed": "❌",
        "blocked": "🔴",
        "skipped": "⏭️",
    }
    
    old_status = result.get("old_status", "unknown")
    new_status = result.get("new_status", status)
    old_icon = status_icons.get(old_status, "⚪")
    new_icon = status_icons.get(new_status, "⚪")
    
    output = f"""✅ **测试结果已更新**

**测试项 ID**: {item_id}
**标题**: {result.get('title', '-')}
**状态变更**: {old_icon} {old_status} → {new_icon} {new_status}
"""
    
    if actual_result:
        output += f"**实际结果**: {actual_result}\n"
    
    if result.get("updated_at"):
        output += f"**更新时间**: {result.get('updated_at')}\n"
    
    return [TextContent(type="text", text=output)]


async def _handle_report(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理生成测试报告"""
    test_session_id = _get_session_id(client, args)
    
    if not test_session_id:
        return [TextContent(
            type="text", 
            text="❌ 无法确定测试会话 ID\n\n"
                 "请确保：\n"
                 "1. MCP 连接时已配置开发会话 ID，或\n"
                 "2. 手动传入 test_session_id 参数"
        )]
    
    result = await client.get_test_report(test_session_id=test_session_id)
    
    summary = result.get("summary", {})
    by_status = result.get("by_status", {})
    by_priority = result.get("by_priority", {})
    items = result.get("items", [])
    
    output = f"""📊 **测试报告**

**测试会话 ID**: {test_session_id}
"""
    
    if result.get("test_session_name"):
        output += f"**会话名称**: {result.get('test_session_name')}\n"
    
    # 摘要统计
    output += f"""
## 📈 执行摘要

| 指标 | 数值 |
|------|------|
| 总计 | {summary.get('total', 0)} |
| 已执行 | {summary.get('executed', 0)} |
| 待测试 | {summary.get('pending', 0)} |
| 通过 | {summary.get('passed', 0)} |
| 失败 | {summary.get('failed', 0)} |
| 阻塞 | {summary.get('blocked', 0)} |
| 跳过 | {summary.get('skipped', 0)} |
| **通过率** | **{summary.get('pass_rate', 0)}%** |

## 📊 按状态分布

"""
    
    # 状态分布
    status_icons = {
        "pending": "⏳",
        "testing": "🔄",
        "passed": "✅",
        "failed": "❌",
        "blocked": "🔴",
        "skipped": "⏭️",
    }
    
    for status, count in by_status.items():
        icon = status_icons.get(status, "⚪")
        output += f"- {icon} {status}: {count}\n"
    
    output += "\n## 📊 按优先级分布\n\n"
    
    # 优先级分布
    priority_icons = {
        "P0": "🔴",
        "P1": "🟡",
        "P2": "🟢",
        "P3": "⚪",
    }
    
    for priority in ["P0", "P1", "P2"]:
        count = by_priority.get(priority, 0)
        if count > 0:
            icon = priority_icons.get(priority, "⚪")
            output += f"- {icon} {priority}: {count}\n"
    
    # 失败的测试项
    failed_items = [item for item in items if item.get("status") == "failed"]
    if failed_items:
        output += "\n## ❌ 失败的测试项\n\n"
        for item in failed_items[:5]:
            output += f"- **{item.get('title', '-')}**"
            if item.get("actual_result"):
                output += f"\n  实际结果: {item.get('actual_result')[:100]}"
            output += "\n"
        if len(failed_items) > 5:
            output += f"  _... 还有 {len(failed_items) - 5} 个失败项_\n"
    
    # 阻塞的测试项
    blocked_items = [item for item in items if item.get("status") == "blocked"]
    if blocked_items:
        output += "\n## 🔴 阻塞的测试项\n\n"
        for item in blocked_items[:3]:
            output += f"- **{item.get('title', '-')}**\n"
        if len(blocked_items) > 3:
            output += f"  _... 还有 {len(blocked_items) - 3} 个阻塞项_\n"
    
    return [TextContent(type="text", text=output)]



