"""
统一搜索工具模块

整合任务、缺陷、评审的搜索功能为单一工具入口 testhub_search。
"""

from typing import TYPE_CHECKING, Optional

from mcp.types import Tool, TextContent

if TYPE_CHECKING:
    from ..api_client import TestHubAPIClient


# ============== 工具定义 ==============

def unified_search_tool() -> Tool:
    """统一搜索工具定义"""
    return Tool(
        name="testhub_search",
        description="""统一搜索工具，支持搜索任务、缺陷、评审。

**搜索类型**：
- `task`: 搜索任务列表
- `bug`: 搜索缺陷列表
- `review`: 搜索评审列表
- `all`: 同时搜索所有类型

**使用示例**：
- 搜索我的任务: type="task", assignee="me"
- 搜索待处理缺陷: type="bug", status="open"
- 关键字搜索: type="all", keyword="登录"
- 搜索进行中的任务: type="task", status="in_progress\"""",
        inputSchema={
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["task", "bug", "review", "all"],
                    "default": "all",
                    "description": "搜索类型",
                },
                "keyword": {
                    "type": "string",
                    "description": "关键字搜索（支持标题/描述）",
                },
                "status": {
                    "type": "string",
                    "description": "状态筛选（不同类型支持不同状态）",
                },
                "assignee": {
                    "type": "string",
                    "description": "负责人筛选（'me' 表示当前用户）",
                },
                "severity": {
                    "type": "string",
                    "enum": ["critical", "major", "minor", "trivial"],
                    "description": "严重程度筛选（仅 bug 类型）",
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "每种类型返回数量限制",
                },
            },
            "required": [],
        },
    )


# ============== 格式化函数 ==============

# 任务状态标签
TASK_STATUS_LABELS = {
    "pending": "🔵 待开发",
    "in_progress": "🟡 开发中",
    "review": "🟠 待评审",
    "testing": "🟣 测试中",
    "completed": "✅ 已完成",
    "blocked": "🔴 阻塞",
    "cancelled": "⚫ 已取消",
}

# 缺陷状态标签
BUG_STATUS_LABELS = {
    "open": "🔴 待处理",
    "fixing": "🟡 修复中",
    "to_verify": "🔵 待验证",
    "closed": "✅ 已关闭",
    "reopened": "🟠 重新打开",
    "archived": "📦 已归档",
}

# 评审状态标签
REVIEW_STATUS_LABELS = {
    "draft": "📝 草稿",
    "submitted": "📤 已提交",
    "in_review": "🔍 评审中",
    "approved": "✅ 已通过",
    "rejected": "❌ 已拒绝",
    "revision": "🔄 需修改",
}

# 复杂度图标
COMPLEXITY_ICONS = {"S": "🟢", "M": "🟡", "L": "🔴"}

# 严重程度标签
SEVERITY_LABELS = {
    "critical": "💀 致命",
    "major": "🔥 严重",
    "minor": "⚠️ 一般",
    "trivial": "📝 轻微",
}


def format_task_results(tasks: list, keyword: str = "") -> str:
    """格式化任务搜索结果"""
    if not tasks:
        return "暂无匹配的任务\n"
    
    output = ""
    for t in tasks:
        complexity = t.get("complexity", "M")
        task_status = t.get("status", "pending")
        c_icon = COMPLEXITY_ICONS.get(complexity, "⚪")
        s_label = TASK_STATUS_LABELS.get(task_status, task_status)
        
        output += f"- {c_icon} **{t.get('task_code', '-')}** - {t.get('title', '-')}\n"
        output += f"  状态: {s_label}"
        if t.get("assignee"):
            output += f" | 负责人: {t.get('assignee')}"
        output += "\n"
    
    return output


def format_bug_results(bugs: list, keyword: str = "") -> str:
    """格式化缺陷搜索结果"""
    if not bugs:
        return "暂无匹配的缺陷\n"
    
    output = ""
    for b in bugs:
        status = b.get("status", "open")
        status_label = BUG_STATUS_LABELS.get(status, status)
        severity = b.get("severity", "minor")
        severity_label = SEVERITY_LABELS.get(severity, severity)
        
        output += f"- **#{b.get('id')}** {status_label} {severity_label}\n"
        output += f"  {b.get('title', '无标题')}"
        if b.get("assignee"):
            output += f" | 负责人: {b.get('assignee')}"
        output += "\n"
    
    return output


def format_review_results(reviews: list, keyword: str = "") -> str:
    """格式化评审搜索结果"""
    if not reviews:
        return "暂无匹配的评审\n"
    
    output = ""
    for r in reviews:
        status = r.get("status", "draft")
        status_label = REVIEW_STATUS_LABELS.get(status, status)
        
        output += f"- **#{r.get('id')}** {status_label}\n"
        task_code = r.get("task_code", "")
        task_title = r.get("task_title", "")
        if task_code:
            output += f"  任务: [{task_code}] {task_title}\n"
        else:
            output += f"  提交人: {r.get('submitter_name', '未知')}\n"
    
    return output


# ============== 搜索处理函数 ==============

async def _search_tasks(
    api_client: "TestHubAPIClient",
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    limit: int = 10,
) -> tuple[list, Optional[str]]:
    """搜索任务"""
    try:
        # 如果 assignee 是 "me"，使用我的任务列表 API
        if assignee == "me":
            result = await api_client.list_my_tasks(status=status, limit=limit)
        else:
            # 使用通用任务列表 API（如果有）
            result = await api_client.list_my_tasks(status=status, limit=limit)
        
        if isinstance(result, dict):
            if result.get("success"):
                tasks = result.get("data", [])
            else:
                return [], result.get("message", "获取任务失败")
        else:
            tasks = result if isinstance(result, list) else []
        
        # 如果有关键字，在结果中过滤
        if keyword and tasks:
            keyword_lower = keyword.lower()
            tasks = [
                t for t in tasks
                if keyword_lower in (t.get("title", "") or "").lower()
                or keyword_lower in (t.get("description", "") or "").lower()
                or keyword_lower in (t.get("task_code", "") or "").lower()
            ]
        
        return tasks[:limit], None
        
    except Exception as e:
        return [], str(e)


async def _search_bugs(
    api_client: "TestHubAPIClient",
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 10,
) -> tuple[list, Optional[str]]:
    """搜索缺陷"""
    try:
        result = await api_client.list_bugs(
            keyword=keyword,
            status=status,
            assignee=assignee if assignee != "me" else None,
            severity=severity,
            page=1,
            page_size=limit,
        )
        
        if not result.get("success"):
            return [], result.get("message", "获取缺陷失败")
        
        bugs = result.get("data", {}).get("items", [])
        return bugs[:limit], None
        
    except Exception as e:
        return [], str(e)


async def _search_reviews(
    api_client: "TestHubAPIClient",
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 10,
) -> tuple[list, Optional[str]]:
    """搜索评审"""
    try:
        result = await api_client.list_reviews(
            status=status,
            page=1,
            page_size=limit,
        )
        
        if not result.get("success"):
            return [], result.get("message", "获取评审失败")
        
        reviews = result.get("data", {}).get("items", [])
        
        # 如果有关键字，在结果中过滤
        if keyword and reviews:
            keyword_lower = keyword.lower()
            reviews = [
                r for r in reviews
                if keyword_lower in (r.get("task_title", "") or "").lower()
                or keyword_lower in (r.get("task_code", "") or "").lower()
            ]
        
        return reviews[:limit], None
        
    except Exception as e:
        return [], str(e)


# ============== 主处理函数 ==============

async def handle_unified_search(
    api_client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """处理统一搜索工具调用"""
    search_type = args.get("type", "all")
    keyword = args.get("keyword")
    status = args.get("status")
    assignee = args.get("assignee")
    severity = args.get("severity")
    limit = args.get("limit", 10)
    
    output = "🔍 **搜索结果**\n\n"
    
    # 添加搜索条件说明
    conditions = []
    if keyword:
        conditions.append(f"关键字: {keyword}")
    if status:
        conditions.append(f"状态: {status}")
    if assignee:
        conditions.append(f"负责人: {assignee}")
    if severity:
        conditions.append(f"严重程度: {severity}")
    
    if conditions:
        output += f"**筛选条件**: {' | '.join(conditions)}\n\n"
    
    output += "---\n\n"
    
    errors = []
    
    # 搜索任务
    if search_type in ["task", "all"]:
        tasks, task_error = await _search_tasks(
            api_client, keyword, status, assignee, limit
        )
        output += f"## 📋 任务 ({len(tasks)})\n\n"
        if task_error:
            output += f"⚠️ 获取任务失败: {task_error}\n\n"
            errors.append(f"任务: {task_error}")
        else:
            output += format_task_results(tasks, keyword or "")
        output += "\n"
    
    # 搜索缺陷
    if search_type in ["bug", "all"]:
        bugs, bug_error = await _search_bugs(
            api_client, keyword, status, assignee, severity, limit
        )
        output += f"## 🐛 缺陷 ({len(bugs)})\n\n"
        if bug_error:
            output += f"⚠️ 获取缺陷失败: {bug_error}\n\n"
            errors.append(f"缺陷: {bug_error}")
        else:
            output += format_bug_results(bugs, keyword or "")
        output += "\n"
    
    # 搜索评审
    if search_type in ["review", "all"]:
        reviews, review_error = await _search_reviews(
            api_client, keyword, status, limit
        )
        output += f"## 📝 评审 ({len(reviews)})\n\n"
        if review_error:
            output += f"⚠️ 获取评审失败: {review_error}\n\n"
            errors.append(f"评审: {review_error}")
        else:
            output += format_review_results(reviews, keyword or "")
    
    return [TextContent(type="text", text=output)]


# ============== 获取工具 ==============

def get_unified_search_tool() -> Tool:
    """获取统一搜索工具定义"""
    return unified_search_tool()



