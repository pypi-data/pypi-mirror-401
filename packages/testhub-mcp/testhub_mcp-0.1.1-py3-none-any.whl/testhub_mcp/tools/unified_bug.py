"""
统一缺陷工具模块

将所有缺陷相关操作整合为单一工具入口 testhub_bug。
支持的操作: create, update, close, reopen, archive, get, list, stats
"""

from typing import TYPE_CHECKING, Optional

from mcp.types import Tool, TextContent

if TYPE_CHECKING:
    from ..api_client import TestHubAPIClient


# ============== 工具定义 ==============

def unified_bug_tool() -> Tool:
    """统一缺陷工具定义"""
    return Tool(
        name="testhub_bug",
        description="""统一缺陷操作工具。

**支持的操作**：
- `create`: 创建新缺陷
- `update`: 更新缺陷信息
- `close`: 关闭缺陷
- `reopen`: 重新打开缺陷
- `archive`: 归档已关闭的缺陷
- `get`: 获取缺陷详情
- `list`: 获取缺陷列表
- `stats`: 获取缺陷统计

**使用示例**：
- 创建缺陷: action="create", title="登录按钮无响应", severity="major"
- 关闭缺陷: action="close", bug_id=1
- 查看列表: action="list", status="open"
- 获取统计: action="stats\"""",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["create", "update", "close", "reopen", "archive", "get", "list", "stats"],
                    "description": "操作类型",
                },
                "bug_id": {
                    "type": "integer",
                    "description": "缺陷ID（除 create/list/stats 外的操作需要）",
                },
                "title": {
                    "type": "string",
                    "description": "缺陷标题（create 时必填，update 时可选）",
                },
                "description": {
                    "type": "string",
                    "description": "详细描述",
                },
                "severity": {
                    "type": "string",
                    "enum": ["critical", "major", "minor", "trivial"],
                    "default": "minor",
                    "description": "严重程度",
                },
                "assignee": {
                    "type": "string",
                    "description": "负责人",
                },
                "due_date": {
                    "type": "string",
                    "description": "截止日期（ISO格式，如 2024-12-31）",
                },
                "related_task_code": {
                    "type": "string",
                    "description": "关联任务编号",
                },
                "status": {
                    "type": "string",
                    "enum": ["open", "fixing", "to_verify", "to_update", "closed", "reopened"],
                    "description": "状态筛选（list 时使用）",
                },
                "keyword": {
                    "type": "string",
                    "description": "关键字搜索（list 时使用）",
                },
                "include_archived": {
                    "type": "boolean",
                    "default": False,
                    "description": "是否包含已归档（list 时使用）",
                },
                "page": {
                    "type": "integer",
                    "default": 1,
                    "description": "页码（list 时使用）",
                },
                "page_size": {
                    "type": "integer",
                    "default": 20,
                    "description": "每页数量（list 时使用）",
                },
                "session_id": {
                    "type": "integer",
                    "description": "会话ID（list/stats 时使用）",
                },
            },
            "required": ["action"],
        },
    )


# ============== 格式化函数 ==============

STATUS_LABELS = {
    "open": "🔴 待处理",
    "fixing": "🟡 修复中",
    "to_verify": "🔵 待验证",
    "to_update": "🟠 待更新",
    "closed": "✅ 已关闭",
    "reopened": "⚠️ 重新打开",
    "archived": "📦 已归档",
}

SEVERITY_LABELS = {
    "critical": "💀 致命",
    "major": "🔥 严重",
    "minor": "⚠️ 一般",
    "trivial": "📝 轻微",
}


def format_bug_list(data: dict) -> str:
    """格式化缺陷列表输出"""
    items = data.get("items", [])
    total = data.get("total", 0)
    page = data.get("page", 1)
    
    output = f"🐛 **缺陷列表** (第 {page} 页，共 {total} 条)\n\n"
    
    if not items:
        output += "暂无缺陷记录\n"
        return output
    
    for bug in items:
        status = bug.get("status", "open")
        status_label = STATUS_LABELS.get(status, status)
        severity = bug.get("severity", "minor")
        severity_label = SEVERITY_LABELS.get(severity, severity)
        assignee = bug.get("assignee") or "未分配"
        due_date = bug.get("due_date")
        
        output += f"**#{bug['id']}** {status_label} {severity_label}\n"
        output += f"  **标题**: {bug.get('title', '无标题')}\n"
        output += f"  **负责人**: {assignee}"
        if due_date:
            output += f" | **截止**: {due_date}"
        output += "\n"
        if bug.get("source_session_name"):
            output += f"  **会话**: {bug.get('source_session_name')}\n"
        output += "\n"
    
    return output


def format_bug_detail(data: dict) -> str:
    """格式化缺陷详情输出"""
    status = data.get("status", "open")
    status_label = STATUS_LABELS.get(status, status)
    severity = data.get("severity", "minor")
    severity_label = SEVERITY_LABELS.get(severity, severity)
    
    output = f"""🐛 **缺陷详情 #{data.get('id')}**

**标题**: {data.get('title', '无标题')}
**状态**: {status_label}
**严重程度**: {severity_label}
**负责人**: {data.get('assignee') or '未分配'}
**截止日期**: {data.get('due_date') or '未设置'}

**来源会话**: {data.get('source_session_name') or '无'}
**功能分类**: {data.get('category') or '未分类'}

**创建时间**: {data.get('created_at', '未知')}
**修复时间**: {data.get('fixed_at') or '未修复'}
**验证时间**: {data.get('verified_at') or '未验证'}

"""
    
    if data.get("description"):
        output += f"## 📝 描述\n\n{data['description']}\n\n"
    
    screenshots = data.get("screenshots", [])
    if screenshots:
        output += f"## 📷 截图 ({len(screenshots)})\n\n"
        for i, url in enumerate(screenshots, 1):
            output += f"{i}. {url}\n"
    
    return output


def format_bug_stats(data: dict) -> str:
    """格式化缺陷统计输出"""
    output = """📊 **缺陷统计概览**

## 总体数据

"""
    output += f"- **总数**: {data.get('total', 0)}\n"
    output += f"- **待处理**: {data.get('open', 0)}\n"
    output += f"- **修复中**: {data.get('fixing', 0)}\n"
    output += f"- **待验证**: {data.get('to_verify', 0)}\n"
    output += f"- **待更新**: {data.get('to_update', 0)}\n"
    output += f"- **已关闭**: {data.get('closed', 0)}\n"
    
    by_severity = data.get("by_severity", {})
    if by_severity:
        output += "\n## 按严重程度分布\n\n"
        for severity, count in by_severity.items():
            label = SEVERITY_LABELS.get(severity, severity)
            output += f"- {label}: {count}\n"
    
    return output


# ============== 操作处理函数 ==============

async def _handle_create(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """创建缺陷"""
    title = args.get("title")
    if not title:
        return [TextContent(type="text", text="❌ 请提供缺陷标题 (title 参数)")]
    
    try:
        result = await api_client.create_bug(
            title=title,
            description=args.get("description"),
            severity=args.get("severity", "minor"),
            assignee=args.get("assignee"),
            related_task_code=args.get("related_task_code"),
            due_date=args.get("due_date"),
        )
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 创建缺陷失败: {result.get('message', '未知错误')}")]
        
        bug_data = result.get("data", {})
        severity_label = SEVERITY_LABELS.get(args.get('severity', 'minor'), 'minor')
        output = f"""✅ **缺陷创建成功**

**缺陷ID**: #{bug_data.get('id')}
**标题**: {title}
**严重程度**: {severity_label}
**负责人**: {args.get('assignee') or '未分配'}
"""
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 创建缺陷失败: {str(e)}")]


async def _handle_update(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """更新缺陷"""
    bug_id = args.get("bug_id")
    if not bug_id:
        return [TextContent(type="text", text="❌ 请提供 bug_id")]
    
    # 收集更新字段
    update_data = {}
    for field in ["title", "description", "severity", "assignee", "due_date"]:
        if field in args and args[field] is not None:
            update_data[field] = args[field]
    
    if not update_data:
        return [TextContent(type="text", text="❌ 请提供要更新的字段")]
    
    try:
        result = await api_client.update_bug(bug_id, **update_data)
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 更新缺陷失败: {result.get('message', '未知错误')}")]
        
        return [TextContent(type="text", text=f"✅ **缺陷 #{bug_id} 更新成功**")]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 更新缺陷失败: {str(e)}")]


async def _handle_close(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """关闭缺陷"""
    bug_id = args.get("bug_id")
    if not bug_id:
        return [TextContent(type="text", text="❌ 请提供 bug_id")]
    
    try:
        result = await api_client.update_bug_status(bug_id, "closed")
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 关闭缺陷失败: {result.get('message', '未知错误')}")]
        
        return [TextContent(type="text", text=f"✅ **缺陷 #{bug_id} 已关闭**")]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 关闭缺陷失败: {str(e)}")]


async def _handle_reopen(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """重新打开缺陷"""
    bug_id = args.get("bug_id")
    if not bug_id:
        return [TextContent(type="text", text="❌ 请提供 bug_id")]
    
    try:
        result = await api_client.update_bug_status(bug_id, "reopened")
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 重新打开缺陷失败: {result.get('message', '未知错误')}")]
        
        return [TextContent(type="text", text=f"🟠 **缺陷 #{bug_id} 已重新打开**")]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 重新打开缺陷失败: {str(e)}")]


async def _handle_archive(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """归档缺陷"""
    bug_id = args.get("bug_id")
    if not bug_id:
        return [TextContent(type="text", text="❌ 请提供 bug_id")]
    
    try:
        result = await api_client.archive_bug(bug_id)
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 归档缺陷失败: {result.get('message', '未知错误')}")]
        
        return [TextContent(type="text", text=f"📦 **缺陷 #{bug_id} 已归档**")]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 归档缺陷失败: {str(e)}")]


async def _handle_get(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """获取缺陷详情"""
    bug_id = args.get("bug_id")
    if not bug_id:
        return [TextContent(type="text", text="❌ 请提供 bug_id")]
    
    try:
        result = await api_client.get_bug(bug_id)
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 获取缺陷详情失败: {result.get('message', '未知错误')}")]
        
        output = format_bug_detail(result.get("data", {}))
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取缺陷详情失败: {str(e)}")]


async def _handle_list(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """获取缺陷列表"""
    try:
        result = await api_client.list_bugs(
            status=args.get("status"),
            severity=args.get("severity"),
            assignee=args.get("assignee"),
            keyword=args.get("keyword"),
            session_id=args.get("session_id"),
            include_archived=args.get("include_archived", False),
            page=args.get("page", 1),
            page_size=args.get("page_size", 20),
        )
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 获取缺陷列表失败: {result.get('message', '未知错误')}")]
        
        output = format_bug_list(result.get("data", {}))
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取缺陷列表失败: {str(e)}")]


async def _handle_stats(api_client: "TestHubAPIClient", args: dict) -> list[TextContent]:
    """获取缺陷统计"""
    try:
        session_id = args.get("session_id")
        
        if session_id:
            result = await api_client.get_bug_session_stats(session_id)
        else:
            result = await api_client.get_bug_stats()
        
        if not result.get("success"):
            return [TextContent(type="text", text=f"❌ 获取统计失败: {result.get('message', '未知错误')}")]
        
        data = result.get("data", {})
        
        if session_id:
            # 会话统计格式
            output = f"""📊 **会话 #{session_id} 缺陷统计**

## 总体数据

- **总数（不含归档）**: {data.get('total', 0)}
- **未修复**: {data.get('unfixed', 0)}
- **已关闭**: {data.get('fixed', 0)}
- **已归档**: {data.get('archived', 0)}

## 按状态分布

"""
            by_status = data.get("by_status", {})
            for status, count in by_status.items():
                label = STATUS_LABELS.get(status, status)
                output += f"- {label}: {count}\n"
            
            by_assignee = data.get("by_assignee", [])
            if by_assignee:
                output += "\n## 按负责人统计\n\n"
                output += "| 负责人 | 未修复 | 已修复 | 总计 |\n"
                output += "|--------|--------|--------|------|\n"
                for item in by_assignee:
                    name = item.get("display_name", "未分配")
                    output += f"| {name} | {item.get('unfixed', 0)} | {item.get('fixed', 0)} | {item.get('total', 0)} |\n"
        else:
            output = format_bug_stats(data)
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取统计失败: {str(e)}")]


# ============== 主处理函数 ==============

async def handle_unified_bug(
    api_client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """处理统一缺陷工具调用"""
    action = args.get("action")
    
    if not action:
        return [TextContent(type="text", text="❌ 请提供 action 参数")]
    
    handlers = {
        "create": _handle_create,
        "update": _handle_update,
        "close": _handle_close,
        "reopen": _handle_reopen,
        "archive": _handle_archive,
        "get": _handle_get,
        "list": _handle_list,
        "stats": _handle_stats,
    }
    
    handler = handlers.get(action)
    if not handler:
        return [TextContent(type="text", text=f"❌ 未知操作: {action}。支持的操作: {', '.join(handlers.keys())}")]
    
    return await handler(api_client, args)


# ============== 获取工具 ==============

def get_unified_bug_tool() -> Tool:
    """获取统一缺陷工具定义"""
    return unified_bug_tool()

