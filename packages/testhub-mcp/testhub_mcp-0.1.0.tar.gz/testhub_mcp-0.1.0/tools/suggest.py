"""
智能任务建议工具

提供任务创建、快捷操作等功能：
- testhub_suggest_task: 根据对话内容建议创建任务
- testhub_create_task: 创建新的开发任务
- testhub_start_task: 快速开始一个任务
- testhub_complete_task: 快速完成一个任务
- testhub_daily_summary: 每日工作摘要（待处理任务、待验证缺陷、待审阅评审）
"""

from mcp.types import Tool, TextContent
from ..api_client import TestHubClient, APIError


def suggest_task_tool() -> Tool:
    """定义智能任务建议工具"""
    return Tool(
        name="testhub_suggest_task",
        description="根据对话内容建议创建任务。当识别到用户描述了新功能、Bug修复、优化需求等时调用此工具，会返回建议的任务信息供用户确认。",
        inputSchema={
            "type": "object",
            "properties": {
                "suggested_title": {
                    "type": "string",
                    "description": "从对话中提取的任务标题"
                },
                "suggested_description": {
                    "type": "string",
                    "description": "从对话中总结的任务描述"
                },
                "suggested_category": {
                    "type": "string",
                    "enum": ["后端", "前端", "数据库", "DevOps", "测试", "其他"],
                    "description": "任务分类"
                },
                "suggested_complexity": {
                    "type": "string",
                    "enum": ["S", "M", "L"],
                    "description": "复杂度预估：S(简单)、M(中等)、L(复杂)"
                },
                "suggested_type": {
                    "type": "string",
                    "enum": ["feature", "bug", "refactor", "optimize", "docs"],
                    "description": "任务类型：feature(新功能)、bug(缺陷修复)、refactor(重构)、optimize(优化)、docs(文档)"
                },
                "context_summary": {
                    "type": "string",
                    "description": "触发建议的对话上下文摘要"
                },
                "auto_create": {
                    "type": "boolean",
                    "default": False,
                    "description": "是否自动创建（需用户在规则中开启）"
                }
            },
            "required": ["suggested_title", "context_summary"]
        }
    )


def create_task_tool() -> Tool:
    """定义创建任务工具"""
    return Tool(
        name="testhub_create_task",
        description="创建新的开发任务。当用户确认创建任务后调用此工具。",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "任务标题"
                },
                "description": {
                    "type": "string",
                    "description": "任务描述"
                },
                "category": {
                    "type": "string",
                    "enum": ["后端", "前端", "数据库", "DevOps", "测试", "其他"],
                    "description": "任务分类"
                },
                "complexity": {
                    "type": "string",
                    "enum": ["S", "M", "L"],
                    "description": "复杂度"
                },
                "priority": {
                    "type": "string",
                    "enum": ["critical", "high", "medium", "low"],
                    "description": "优先级"
                },
                "task_type": {
                    "type": "string",
                    "enum": ["feature", "bug", "refactor", "optimize", "docs"],
                    "description": "任务类型"
                },
                "acceptance_criteria": {
                    "type": "string",
                    "description": "验收标准"
                },
                "technical_notes": {
                    "type": "string",
                    "description": "技术备注"
                },
                "module": {
                    "type": "string",
                    "description": "所属模块"
                },
                "assign_to_me": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否分配给自己"
                }
            },
            "required": ["title"]
        }
    )


def start_task_tool() -> Tool:
    """定义快速开始任务工具"""
    return Tool(
        name="testhub_start_task",
        description="开始一个任务（获取详情并更新状态为进行中）。这是一个便捷工具，一步完成获取任务信息和开始任务。",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号，如 TASK-001"
                }
            },
            "required": ["task_code"]
        }
    )


def complete_task_tool() -> Tool:
    """定义快速完成任务工具"""
    return Tool(
        name="testhub_complete_task",
        description="完成一个任务。可选同时创建评审记录。",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "任务编号（可选；不传则默认使用当前上下文中的任务）"
                },
                "create_review": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否同时创建评审"
                },
                "completion_note": {
                    "type": "string",
                    "description": "完成备注"
                }
            },
            "required": []
        }
    )


def daily_summary_tool() -> Tool:
    """定义每日工作摘要工具"""
    return Tool(
        name="testhub_daily_summary",
        description="返回今日工作摘要（待处理任务、待验证缺陷、待审阅评审）。适合在开始一天工作或准备收尾时快速查看当前待办。",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50,
                    "description": "每类返回数量限制（默认 10）"
                }
            },
        },
    )


async def handle_suggest_task(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理智能任务建议"""
    title = args.get("suggested_title", "")
    description = args.get("suggested_description", "")
    category = args.get("suggested_category", "其他")
    complexity = args.get("suggested_complexity", "M")
    task_type = args.get("suggested_type", "feature")
    context = args.get("context_summary", "")
    auto_create = args.get("auto_create", False)
    
    # 类型映射
    type_labels = {
        "feature": "新功能",
        "bug": "Bug修复",
        "refactor": "重构",
        "optimize": "优化",
        "docs": "文档",
    }
    
    # 复杂度图标
    complexity_icons = {
        "S": "🟢 简单",
        "M": "🟡 中等",
        "L": "🔴 复杂",
    }
    
    if auto_create:
        # 自动创建模式：直接调用创建任务
        try:
            task = await client.create_task(
                title=title,
                description=description,
                category=category,
                complexity=complexity,
                task_type=task_type,
            )
            
            output = f"""✅ 任务已自动创建

**任务编号**：{task.get('task_code', '-')}
**标题**：{title}
**类型**：{type_labels.get(task_type, task_type)}
**复杂度**：{complexity_icons.get(complexity, complexity)}
**分类**：{category}

---

📋 **创建原因**：
{context}

已自动分配给你，可以使用 `testhub_start_task` 开始任务。
"""
            return [TextContent(type="text", text=output)]
            
        except APIError as e:
            return [TextContent(type="text", text=f"❌ 自动创建任务失败: {str(e)}")]
    else:
        # 建议模式：返回建议信息，等待用户确认
        output = f"""💡 **识别到潜在任务**

根据对话内容，我识别到以下可能的开发任务：

---

**建议标题**：{title}
**任务类型**：{type_labels.get(task_type, task_type)}
**复杂度**：{complexity_icons.get(complexity, complexity)}
**分类**：{category}

**描述**：
{description or '（从对话中总结）'}

---

📝 **识别依据**：
{context}

---

是否需要创建这个任务？

- 回复"**创建**"或"**确认**"：我将为你创建任务
- 回复"**修改**"：可以修改任务信息后再创建
- 回复"**不用**"或"**跳过**"：不创建任务

你也可以直接使用 `testhub_create_task` 工具手动创建任务。
"""
        return [TextContent(type="text", text=output)]


async def handle_create_task(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理创建任务"""
    title = args.get("title")
    if not title:
        return [TextContent(type="text", text="❌ 任务标题不能为空")]
    
    description = args.get("description")
    category = args.get("category", "其他")
    complexity = args.get("complexity", "M")
    priority = args.get("priority", "medium")
    task_type = args.get("task_type", "feature")
    acceptance_criteria = args.get("acceptance_criteria")
    technical_notes = args.get("technical_notes")
    module = args.get("module")
    assign_to_me = args.get("assign_to_me", True)
    
    try:
        task = await client.create_task(
            title=title,
            description=description,
            category=category,
            complexity=complexity,
            priority=priority,
            task_type=task_type,
            acceptance_criteria=acceptance_criteria,
            technical_notes=technical_notes,
            module=module,
            assign_to_me=assign_to_me,
        )
        
        # 类型映射
        type_labels = {
            "feature": "新功能",
            "bug": "Bug修复",
            "refactor": "重构",
            "optimize": "优化",
            "docs": "文档",
        }
        
        # 优先级标签
        priority_labels = {
            "critical": "🔴 紧急 P0",
            "high": "🟠 高 P1",
            "medium": "🟡 中 P2",
            "low": "🟢 低 P3",
        }
        
        # 复杂度图标
        complexity_icons = {
            "S": "🟢 简单",
            "M": "🟡 中等",
            "L": "🔴 复杂",
        }
        
        task_code = task.get("task_code", "-")
        
        output = f"""✅ 任务创建成功！

**编号**：{task_code}
**标题**：{title}
**类型**：{type_labels.get(task_type, task_type)}
**优先级**：{priority_labels.get(priority, priority)}
**复杂度**：{complexity_icons.get(complexity, complexity)}
**分类**：{category}
"""
        
        if module:
            output += f"**模块**：{module}\n"
        
        if description:
            output += f"\n**描述**：\n{description}\n"
        
        if acceptance_criteria:
            output += f"\n**验收标准**：\n{acceptance_criteria}\n"
        
        if technical_notes:
            output += f"\n**技术备注**：\n{technical_notes}\n"
        
        output += f"""
---

🚀 **下一步**：
- 使用 `testhub_start_task` 开始任务：`task_code: {task_code}`
- 或使用 `testhub_get_task` 查看完整详情
"""
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 创建任务失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 创建任务失败: {str(e)}")]


async def handle_start_task(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理快速开始任务"""
    task_code = args.get("task_code")
    if not task_code:
        return [TextContent(type="text", text="❌ 请提供任务编号")]
    
    try:
        # 调用开始任务 API
        result = await client.start_task(task_code)
        
        task = result.get("task", {})
        
        # 在成功启动任务后，自动切换上下文到当前任务
        from ..context import get_context
        ctx = get_context()
        ctx.set_current_task(task.get("task_code", task_code), task.get("title"))
        
        # 状态标签映射
        status_labels = {
            "pending": "待开发 🔵",
            "in_progress": "开发中 🟡",
            "review": "待评审 🟠",
            "testing": "测试中 🟣",
            "completed": "已完成 ✅",
            "blocked": "阻塞 🔴",
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

---

**描述**：
{task.get('description') or '（无）'}

**验收标准**：
{task.get('acceptance_criteria') or '（无）'}

**技术备注**：
{task.get('technical_notes') or '（无）'}
"""
        
        # L 级任务提醒
        if complexity == 'L':
            output += """
---

⚠️ **注意**：这是 L 级复杂任务，建议：
1. 确认设计文档已完成
2. 拆分为多个子任务
3. 定期同步进度
"""
        else:
            output += """
---

💡 **提示**：
- 完成后使用 `testhub_complete_task` 标记完成
- 遇到问题可使用 `testhub_update_task_status` 更新状态为 blocked
"""
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 开始任务失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 开始任务失败: {str(e)}")]


async def handle_complete_task(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理快速完成任务"""
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
    
    create_review = args.get("create_review", True)
    completion_note = args.get("completion_note")
    
    try:
        # 调用完成任务 API
        result = await client.complete_task(
            task_code=task_code,
            create_review=create_review,
            completion_note=completion_note,
        )
        
        output = f"""✅ **任务已完成！**

**编号**：{task_code}
**状态**：已完成 ✅
"""
        
        if completion_note:
            output += f"**完成备注**：{completion_note}\n"
        
        # 如果创建了评审
        review = result.get("review")
        if review:
            output += f"""
---

📋 **评审已创建**

**评审 ID**：{review.get('id', '-')}
**状态**：{review.get('status', 'draft')}

下一步：
- 使用 `testhub_docs` 管理开发文档
"""
        else:
            output += """
---

💡 **下一步**：
- 如需管理文档，使用 `testhub_docs` 工具
- 查看更多任务，使用 `testhub_list_my_tasks`
"""
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 完成任务失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 完成任务失败: {str(e)}")]


async def handle_daily_summary(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理每日工作摘要"""
    limit = args.get("limit", 10)

    try:
        resp = await client.get_daily_summary(limit=int(limit))
        data = resp.get("data", resp) if isinstance(resp, dict) else resp

        tasks = (data.get("tasks") or {}) if isinstance(data, dict) else {}
        bugs = (data.get("bugs_to_verify") or {}) if isinstance(data, dict) else {}
        reviews = (data.get("reviews_to_check") or {}) if isinstance(data, dict) else {}
        date_str = data.get("date") if isinstance(data, dict) else None

        # 格式化输出（偏人类可读）
        lines: list[str] = []
        lines.append(f"📅 **每日工作摘要**（{date_str or '-'}）")
        lines.append("")

        # tasks
        lines.append("## 待处理任务")
        lines.append(f"- 总数：{tasks.get('total', 0)}")
        items = tasks.get("items") or []
        if items:
            for t in items:
                code = t.get("task_code") or f"#{t.get('id')}"
                lines.append(f"- [{code}] {t.get('title', '-')}" f"（{t.get('status', '-')}, P={t.get('priority', '-')}, L={t.get('complexity', '-')}" f"{', ' + t.get('module') if t.get('module') else ''}）")
        else:
            lines.append("- （暂无）")
        lines.append("")

        # bugs
        lines.append("## 待验证缺陷")
        lines.append(f"- 总数：{bugs.get('total', 0)}（展示范围：{bugs.get('scope', 'team')}）")
        bug_items = bugs.get("items") or []
        if bug_items:
            for b in bug_items:
                lines.append(
                    f"- [BUG-{b.get('id')}] {b.get('title', '-')}"
                    f"（{b.get('severity', '-')}, {b.get('status', '-')}"
                    f"{', 负责人=' + b.get('assignee') if b.get('assignee') else ''}）"
                )
        else:
            lines.append("- （暂无）")
        lines.append("")

        # reviews
        lines.append("## 待审阅评审")
        lines.append(f"- 总数：{reviews.get('total', 0)}（状态：{', '.join(reviews.get('statuses') or [])}）")
        review_items = reviews.get("items") or []
        if review_items:
            for r in review_items:
                task_code = r.get("task_code") or "-"
                lines.append(
                    f"- [REVIEW-{r.get('id')}] {task_code} {r.get('task_title', '-')}"
                    f"（{r.get('status', '-')}）"
                )
        else:
            lines.append("- （暂无）")

        return [TextContent(type="text", text="\n".join(lines))]

    except APIError as e:
        return [TextContent(type="text", text=f"❌ 获取每日摘要失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取每日摘要失败: {str(e)}")]


def get_context_tool() -> Tool:
    """定义获取上下文工具"""
    return Tool(
        name="testhub_get_context",
        description="获取当前 MCP 会话上下文，包括当前任务、会话统计等信息。用于了解当前工作状态。",
        inputSchema={
            "type": "object",
            "properties": {},
        }
    )


def switch_task_tool() -> Tool:
    """定义切换任务工具"""
    return Tool(
        name="testhub_switch_task",
        description="切换当前工作的任务。切换后，后续操作会自动关联到新任务。",
        inputSchema={
            "type": "object",
            "properties": {
                "task_code": {
                    "type": "string",
                    "description": "要切换到的任务编号"
                }
            },
            "required": ["task_code"]
        }
    )


async def handle_get_context(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理获取上下文"""
    from ..context import get_context
    
    try:
        ctx = get_context()
        output = ctx.to_display()
        
        # 如果有当前任务，尝试获取最新状态
        if ctx.current_task_code:
            try:
                task = await client.get_task_by_code(ctx.current_task_code)
                
                status_labels = {
                    "pending": "待开发 🔵",
                    "in_progress": "开发中 🟡",
                    "review": "待评审 🟠",
                    "testing": "测试中 🟣",
                    "completed": "已完成 ✅",
                    "blocked": "阻塞 🔴",
                }
                
                status = task.get("status", "pending")
                
                output += f"""

---

**当前任务状态**：
- 状态：{status_labels.get(status, status)}
- 优先级：{task.get('priority', 'medium')}
"""
                
                if task.get('acceptance_criteria'):
                    output += f"\n**验收标准**：\n{task.get('acceptance_criteria')}"
                    
            except Exception:
                pass  # 获取任务状态失败不影响显示上下文
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取上下文失败: {str(e)}")]


async def handle_switch_task(client: TestHubClient, args: dict) -> list[TextContent]:
    """处理切换任务"""
    from ..context import get_context
    
    task_code = args.get("task_code")
    if not task_code:
        return [TextContent(type="text", text="❌ 请提供任务编号")]
    
    try:
        # 先获取任务信息验证任务存在
        task_response = await client.get_task_by_code(task_code)
        
        # 解析响应数据
        if isinstance(task_response, dict):
            task = task_response.get("data", task_response) if task_response.get("success") else task_response
        else:
            task = task_response
        
        if not task:
            return [TextContent(type="text", text=f"❌ 任务 {task_code} 不存在")]
        
        # 更新上下文
        ctx = get_context()
        old_task = ctx.current_task_code
        ctx.set_current_task(task_code, task.get("title"))
        
        # 状态标签映射
        status_labels = {
            "pending": "待开发 🔵",
            "in_progress": "开发中 🟡",
            "review": "待评审 🟠",
            "testing": "测试中 🟣",
            "completed": "已完成 ✅",
            "blocked": "阻塞 🔴",
        }
        
        status = task.get("status", "pending")
        
        output = f"""🔄 **已切换任务**

"""
        if old_task:
            output += f"从：{old_task}\n"
        output += f"""到：**{task_code}** - {task.get('title', '')}

---

**任务状态**：{status_labels.get(status, status)}
**复杂度**：{task.get('complexity', 'M')}
**分类**：{task.get('category', '-')}

**描述**：
{task.get('description') or '（无）'}

---

💡 后续操作将自动关联到此任务。
"""
        
        return [TextContent(type="text", text=output)]
        
    except APIError as e:
        return [TextContent(type="text", text=f"❌ 切换任务失败: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 切换任务失败: {str(e)}")]


# 工具注册辅助函数
def get_all_suggest_tools() -> list[Tool]:
    """获取所有任务建议工具定义"""
    return [
        suggest_task_tool(),
        create_task_tool(),
        start_task_tool(),
        complete_task_tool(),
        daily_summary_tool(),
        get_context_tool(),
        switch_task_tool(),
    ]

