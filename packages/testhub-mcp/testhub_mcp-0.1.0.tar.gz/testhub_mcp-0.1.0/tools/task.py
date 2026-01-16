"""
任务相关工具

提供开发任务的获取、更新、列表等功能。
"""

from mcp.types import Tool, TextContent
from ..api_client import TestHubClient, APIError


def get_task_tool() -> Tool:
    """定义获取任务详情工具"""
    return Tool(
        name="testhub_get_task",
        description="获取开发任务详情，包括任务描述、验收标准、技术备注、复杂度等信息",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号，如 TASK-001 或 TASK-042"
                }
            },
            "required": ["task_code"]
        }
    )


def task_overview_tool() -> Tool:
    """定义任务全景视图工具"""
    return Tool(
        name="testhub_task_overview",
        description="一次性返回任务详情 + 评审状态 + 关联缺陷",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号，如 TASK-001 或 TASK-042",
                }
            },
            "required": ["task_code"],
        },
    )


def update_task_status_tool() -> Tool:
    """定义更新任务状态工具"""
    return Tool(
        name="testhub_update_task_status",
        description="更新任务状态（pending→in_progress→review→testing→completed）",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号（可选；不传则默认使用当前上下文中的任务）"
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "review", "testing", "completed", "blocked"],
                    "description": "目标状态"
                },
                "comment": {
                    "type": "string",
                    "description": "状态变更说明（可选）"
                }
            },
            "required": ["status"]
        }
    )


def list_my_tasks_tool() -> Tool:
    """定义获取我的任务列表工具"""
    return Tool(
        name="testhub_list_my_tasks",
        description="获取当前用户的待办任务列表",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "review", "testing", "blocked"],
                    "description": "状态过滤（可选）"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "返回数量限制"
                }
            }
        }
    )


async def handle_get_task(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理获取任务详情"""
    task_code = args["task_code"]
    
    try:
        task_response = await client.get_task_by_code(task_code)
        
        # 从响应中提取任务数据
        if isinstance(task_response, dict):
            task = task_response.get("data", task_response) if task_response.get("success") else task_response
        else:
            task = task_response
        
        if not task:
            return [TextContent(type="text", text=f"❌ 任务 {task_code} 不存在")]
        
        # 状态标签映射
        status_labels = {
            "pending": "待开发 🔵",
            "in_progress": "开发中 🟡",
            "review": "待评审 🟠",
            "testing": "测试中 🟣",
            "completed": "已完成 ✅",
            "blocked": "阻塞 🔴",
            "cancelled": "已取消 ⚫",
        }
        
        # 优先级标签映射
        priority_labels = {
            "critical": "🔴 紧急 P0",
            "high": "🟠 高 P1",
            "medium": "🟡 中 P2",
            "low": "🟢 低 P3",
        }
        
        # 复杂度图标映射
        complexity_icons = {
            "S": "🟢 简单",
            "M": "🟡 中等",
            "L": "🔴 复杂",
        }
        
        # 格式化输出
        status = task.get("status", "pending")
        priority = task.get("priority", "medium")
        complexity = task.get("complexity", "M")
        
        output = f"""📋 **任务详情**

**编号**：{task.get('task_code', '-')}
**标题**：{task.get('title', '-')}
**状态**：{status_labels.get(status, status)}
**复杂度**：{complexity_icons.get(complexity, complexity)}
**优先级**：{priority_labels.get(priority, priority)}
**类型**：{task.get('task_type', 'feature')}
**模块**：{task.get('module', '-')}

---

**描述**：
{task.get('description') or '（无）'}

**验收标准**：
{task.get('acceptance_criteria') or '（无）'}

**技术备注**：
{task.get('technical_notes') or '（无）'}
"""
        
        # 显示标签
        tags = task.get('tags') or []
        if tags:
            output += f"\n**标签**：{', '.join(tags)}\n"
        
        # 显示负责人
        assignee = task.get('assignee')
        if assignee:
            output += f"\n**负责人**：{assignee}\n"
        
        # L 级任务提醒
        if complexity == 'L':
            output += """
---

⚠️ **注意**：这是 L 级复杂任务，建议先完成设计评审再开始编码。
"""
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 获取任务失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取任务失败: {str(e)}")]


async def handle_task_overview(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理任务全景视图"""
    task_code = args["task_code"]

    try:
        result = await client.get_task_overview(task_code)
        if not isinstance(result, dict) or not result.get("success"):
            return [TextContent(type="text", text=f"❌ 获取任务概览失败: {result.get('message', '未知错误') if isinstance(result, dict) else '未知错误'}")]

        data = result.get("data") or {}
        task = data.get("task") or {}
        review = data.get("review")
        bugs = data.get("bugs") or []

        # 状态标签映射（复用 get_task 的映射逻辑）
        status_labels = {
            "pending": "待开发 🔵",
            "in_progress": "开发中 🟡",
            "review": "待评审 🟠",
            "testing": "测试中 🟣",
            "completed": "已完成 ✅",
            "blocked": "阻塞 🔴",
            "cancelled": "已取消 ⚫",
        }
        priority_labels = {
            "critical": "🔴 紧急 P0",
            "high": "🟠 高 P1",
            "medium": "🟡 中 P2",
            "low": "🟢 低 P3",
        }
        complexity_icons = {"S": "🟢 简单", "M": "🟡 中等", "L": "🔴 复杂"}

        status = task.get("status", "pending")
        priority = task.get("priority", "medium")
        complexity = task.get("complexity", "M")

        output = f"""🧭 **任务全景视图**

## 📋 任务

**编号**：{task.get('task_code', task_code)}
**标题**：{task.get('title', '-')}
**状态**：{status_labels.get(status, status)}
**复杂度**：{complexity_icons.get(complexity, complexity)}
**优先级**：{priority_labels.get(priority, priority)}
**类型**：{task.get('task_type', 'feature')}
**模块**：{task.get('module', '-')}
"""

        # 评审状态
        output += "\n---\n\n## 🧪 评审\n\n"
        if review:
            review_status_labels = {
                "draft": "📝 草稿",
                "submitted": "📤 已提交",
                "in_review": "🔍 评审中",
                "approved": "✅ 已通过",
                "rejected": "❌ 已拒绝",
                "revision": "🔄 需修改",
            }
            output += f"**已有评审**：是\n"
            output += f"**评审ID**：#{review.get('id')}\n"
            output += f"**状态**：{review_status_labels.get(review.get('status'), review.get('status'))}\n"
            output += f"**评论数**：{review.get('comment_count', 0)}\n"
        else:
            output += "**已有评审**：否\n"

        # 关联缺陷
        output += "\n---\n\n## 🐛 关联缺陷\n\n"
        if not bugs:
            output += "（无）\n"
        else:
            status_labels_bug = {
                "open": "🔴 待处理",
                "fixing": "🟡 修复中",
                "to_verify": "🔵 待验证",
                "closed": "✅ 已关闭",
                "reopened": "🟠 重新打开",
                "archived": "📦 已归档",
            }
            severity_labels_bug = {
                "critical": "💀 致命",
                "major": "🔥 严重",
                "minor": "⚠️ 一般",
                "trivial": "📝 轻微",
            }
            for b in bugs:
                output += (
                    f"- **#{b.get('id')}** {status_labels_bug.get(b.get('status'), b.get('status'))} "
                    f"{severity_labels_bug.get(b.get('severity'), b.get('severity'))}：{b.get('title', '')}\n"
                )

        return [TextContent(type="text", text=output)]

    except APIError as e:
        return [TextContent(type="text", text=f"❌ 获取任务概览失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取任务概览失败: {str(e)}")]


async def handle_update_task_status(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理更新任务状态"""
    task_code = args.get("task_code")
    if not task_code:
        from ..context import get_context

        ctx = get_context()
        task_code = ctx.current_task_code
    if not task_code:
        return [
            TextContent(
                type="text",
                text="❌ 错误：请提供 task_code 或先使用 testhub_start_task 设置当前任务",
            )
        ]
    status = args["status"]
    comment = args.get("comment")
    
    try:
        await client.update_task_status(task_code, status, comment)
        
        status_labels = {
            "pending": "待开发",
            "in_progress": "开发中",
            "review": "待评审",
            "testing": "测试中",
            "completed": "已完成",
            "blocked": "阻塞",
        }
        
        output = f"✅ 任务 **{task_code}** 状态已更新为：**{status_labels.get(status, status)}**"
        if comment:
            output += f"\n📝 备注：{comment}"
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 更新状态失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 更新状态失败: {str(e)}")]


async def handle_list_my_tasks(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理获取我的任务列表"""
    status = args.get("status")
    limit = args.get("limit", 10)
    
    try:
        result = await client.list_my_tasks(status=status, limit=limit)
        
        # 从响应中提取任务列表数据
        if isinstance(result, dict):
            tasks = result.get("data", []) if result.get("success") else []
        else:
            tasks = result if isinstance(result, list) else []
        
        if not tasks:
            return [TextContent(type="text", text="📋 暂无待办任务")]
        
        # 复杂度图标
        complexity_icons = {"S": "🟢", "M": "🟡", "L": "🔴"}
        
        # 状态图标
        status_icons = {
            "pending": "🔵",
            "in_progress": "🟡",
            "review": "🟠",
            "testing": "🟣",
            "blocked": "🔴",
        }
        
        output = f"📋 **我的任务列表** ({len(tasks)} 个)\n\n"
        
        for t in tasks:
            complexity = t.get("complexity", "M")
            task_status = t.get("status", "pending")
            c_icon = complexity_icons.get(complexity, "⚪")
            s_icon = status_icons.get(task_status, "⚪")
            
            output += f"- {c_icon} **{t.get('task_code', '-')}** - {t.get('title', '-')} {s_icon}\n"
            
            # 显示简要描述（如果有）
            desc = t.get("description")
            if desc and len(desc) > 50:
                output += f"  _{desc[:50]}..._\n"
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 获取任务列表失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取任务列表失败: {str(e)}")]


# 工具注册辅助函数
def get_all_task_tools() -> list[Tool]:
    """获取所有任务工具定义"""
    return [
        get_task_tool(),
        task_overview_tool(),
        update_task_status_tool(),
        list_my_tasks_tool(),
    ]

