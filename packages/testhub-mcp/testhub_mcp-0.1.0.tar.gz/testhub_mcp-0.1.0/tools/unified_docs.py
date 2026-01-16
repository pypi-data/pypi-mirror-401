"""
统一文档工具模块

整合文档操作为单一工具入口 testhub_docs。
支持两种数据源：
- dev: 数据库存储的开发文档（DevDocHub）
- project: 项目本地 docs/ 目录

支持的操作：
- search: 搜索文档
- get: 获取文档详情
- create: 创建文档（仅 dev 源）
- update: 更新文档（仅 dev 源）
- upload: 上传 MD 文件并解析入库（仅 dev 源）
- list: 列出文档
- versions: 获取版本历史（仅 dev 源）
- delete: 删除文档（仅 dev 源）
- publish: 发布文档（仅 dev 源）
- archive: 归档文档（仅 dev 源）
- unarchive: 取消归档（仅 dev 源）
- restore: 恢复到历史版本（仅 dev 源）
- comment: 评论管理（仅 dev 源）
- context: 获取任务上下文（仅 project 源，保留兼容）
"""

import re
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from mcp.types import Tool, TextContent

if TYPE_CHECKING:
    from ..resources.docs import DocsResourceProvider
    from ..api_client import TestHubAPIClient


# ============== 文档类型定义 ==============

DOC_TYPE_LABELS = {
    "architecture": "架构设计",
    "data_model": "数据模型",
    "api_design": "接口设计",
    "technical_memo": "技术备忘",
    "problem_record": "问题记录",
    "change_summary": "变更摘要",
    "implementation": "实现说明",
    "best_practice": "最佳实践",
    "prompt_template": "Prompt 模板",
    "retrospective": "复盘总结",
    "weekly_report": "周报",
    "meeting_notes": "会议纪要",
    "transcript": "录音记录",
    "consulting_report": "咨询报告",
    "analysis_report": "分析报告",
    "workflow": "流程规范",
    "product_spec": "产品说明",
    "learning_notes": "学习笔记",
    "strategy": "策略规划",
}


# ============== 工具定义 ==============

def unified_docs_tool() -> Tool:
    """统一文档工具定义"""
    return Tool(
        name="testhub_docs",
        description="""统一文档操作工具，支持搜索和获取开发上下文。

**支持的操作**：
- `search`: 搜索项目文档库
- `context`: 获取任务相关的设计文档、接口定义、数据模型等上下文
- `get`: 获取文档详情（需指定 doc_code）
- `create`: 创建新文档（仅 dev 源）
- `update`: 更新文档（仅 dev 源）
- `upload`: 上传 MD 文件并自动解析入库（仅 dev 源）
- `list`: 列出文档列表（仅 dev 源）
- `versions`: 获取版本历史（仅 dev 源）
- `delete`: 删除文档（仅 dev 源）
- `publish`: 发布文档，将草稿改为已发布状态（仅 dev 源）
- `archive`: 归档文档（仅 dev 源）
- `unarchive`: 取消归档，恢复为草稿状态（仅 dev 源）
- `restore`: 恢复到历史版本（仅 dev 源，需指定 version）
- `comment`: 评论管理 - 查看/添加/删除评论（仅 dev 源）

**数据源**：
- `project`: 项目本地 docs/ 目录（默认，只读）
- `dev`: 数据库存储的开发文档（可增删改查，需 API 配置）

**使用示例**：
- 搜索文档: action="search", query="权限管理"
- 获取任务上下文: action="context", task_code="TASK-001"
- 按范围搜索: action="search", query="API", scope="api"
- 创建文档: action="create", source="dev", title="接口设计", doc_type="api_design", content="..."
- 获取文档: action="get", source="dev", doc_code="DOC-001"
- 更新文档: action="update", source="dev", doc_code="DOC-001", content="...", change_note="修复格式"
- 上传文件: action="upload", source="dev", file_path="/path/to/doc.md"
- 上传并指定模块: action="upload", source="dev", file_path="./docs/api.md", module_name="广告模块"
- 上传并更新已有文档: action="upload", source="dev", file_path="./docs/api.md", doc_code="DOC-001", change_note="更新接口说明"
- 列出文档: action="list", source="dev", doc_type="api_design"
- 查询任务文档: action="list", source="dev", task_code="TASK-001"
- 查看版本: action="versions", source="dev", doc_code="DOC-001"
- 删除文档: action="delete", source="dev", doc_code="DOC-001"
- 发布文档: action="publish", source="dev", doc_code="DOC-001"
- 归档文档: action="archive", source="dev", doc_code="DOC-001"
- 取消归档: action="unarchive", source="dev", doc_code="DOC-001"
- 恢复版本: action="restore", source="dev", doc_code="DOC-001", version=2
- 查询 Prompt 模板: action="list", source="dev", doc_type="prompt_template"
- 搜索 Prompt 模板: action="search", source="dev", query="代码评审", doc_type="prompt_template"
- 查看评论: action="comment", source="dev", doc_code="DOC-001", comment_action="list"
- 添加评论: action="comment", source="dev", doc_code="DOC-001", comment_action="add", comment_content="设计很清晰"
- 回复评论: action="comment", source="dev", doc_code="DOC-001", comment_action="add", comment_content="同意", parent_id=5
- 删除评论: action="comment", source="dev", doc_code="DOC-001", comment_action="delete", comment_id=5""",
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["search", "context", "get", "create", "update", "upload", "list", "versions", "delete", "publish", "archive", "unarchive", "restore", "comment"],
                    "description": "操作类型",
                },
                "source": {
                    "type": "string",
                    "enum": ["project", "dev"],
                    "default": "project",
                    "description": "数据源：project=本地docs/目录，dev=数据库文档",
                },
                "query": {
                    "type": "string",
                    "description": "搜索关键词（search 时必填）",
                },
                "doc_code": {
                    "type": "string",
                    "description": "文档编号（get/update/versions/delete/publish/archive/unarchive/restore/comment 时必填，upload 时可选用于更新已有文档，如 DOC-001）",
                },
                "task_code": {
                    "type": "string",
                    "description": "任务编号（context/create/upload/list 时使用，如 TASK-001）。创建或上传文档时会自动关联到任务所属的会话",
                },
                "module": {
                    "type": "string",
                    "description": "模块名称（context 时可选，自动从任务推断）",
                },
                "scope": {
                    "type": "string",
                    "enum": ["all", "design", "api", "database", "module", "guide"],
                    "default": "all",
                    "description": "搜索范围（search 时使用，仅 project 源）",
                },
                "limit": {
                    "type": "integer",
                    "default": 5,
                    "description": "返回结果数量限制",
                },
                # create/update 专用参数
                "doc_type": {
                    "type": "string",
                    "enum": [
                        "architecture", "data_model", "api_design", "technical_memo",
                        "problem_record", "change_summary", "implementation", "best_practice",
                        "prompt_template", "retrospective", "weekly_report", "meeting_notes",
                        "transcript", "consulting_report", "analysis_report", "workflow",
                        "product_spec", "learning_notes", "strategy"
                    ],
                    "description": "文档类型（create 时必填，list 时可选筛选）。transcript=录音记录，consulting_report=咨询报告，analysis_report=分析报告，workflow=流程规范，product_spec=产品说明，learning_notes=学习笔记，strategy=策略规划",
                },
                "title": {
                    "type": "string",
                    "description": "文档标题（create 时必填）",
                },
                "content": {
                    "type": "string",
                    "description": "Markdown 内容（create 时必填，update 时可选）",
                },
                "summary": {
                    "type": "string",
                    "description": "文档摘要（create/update 时可选）",
                },
                "module_name": {
                    "type": "string",
                    "description": "所属模块（create/update/list 时可选）",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "标签列表（create/update 时可选）",
                },
                "change_note": {
                    "type": "string",
                    "description": "变更说明（update 时可选，用于版本记录）",
                },
                "status": {
                    "type": "string",
                    "enum": ["draft", "published", "archived"],
                    "description": "文档状态（create/update/list 时可选）",
                },
                "version": {
                    "type": "integer",
                    "description": "版本号（versions 获取特定版本时使用）",
                },
                # upload 专用参数
                "file_path": {
                    "type": "string",
                    "description": "MD 文件路径（upload 时必填，支持绝对路径或相对路径）",
                },
                # comment 专用参数
                "comment_action": {
                    "type": "string",
                    "enum": ["list", "add", "delete"],
                    "description": "评论操作类型（comment 时使用）：list=查看评论，add=添加评论，delete=删除评论",
                },
                "comment_content": {
                    "type": "string",
                    "description": "评论内容（comment add 时必填）",
                },
                "comment_id": {
                    "type": "integer",
                    "description": "评论ID（comment delete 时必填）",
                },
                "parent_id": {
                    "type": "integer",
                    "description": "父评论ID（comment add 时可选，用于回复其他评论）",
                },
            },
            "required": ["action"],
        },
    )


# ============== 辅助函数 ==============

def extract_snippet(content: str, query: str, context_lines: int = 3) -> str:
    """从内容中提取包含查询关键词的片段"""
    lines = content.split("\n")
    query_lower = query.lower()

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            snippet_lines = lines[start:end]
            return "\n".join(snippet_lines)

    return content[:200] + "..."


def truncate_content(content: str, max_lines: int = 100) -> str:
    """截取内容的关键部分"""
    lines = content.split("\n")
    if len(lines) <= max_lines:
        return content

    return "\n".join(lines[:max_lines]) + f"\n\n... (内容已截取，共 {len(lines)} 行)"


def extract_relevant_tables(er_content: str, module: str) -> str:
    """从 ER 文档中提取与模块相关的表"""
    sections = re.split(r"\n##\s+", er_content)
    relevant = []

    for section in sections:
        if module.lower() in section.lower():
            relevant.append("## " + section if not section.startswith("#") else section)

    if relevant:
        return "\n\n".join(relevant)

    return truncate_content(er_content, max_lines=50)


def format_doc_type(doc_type: str) -> str:
    """格式化文档类型为中文"""
    return DOC_TYPE_LABELS.get(doc_type, doc_type)


# ============== MD 文件解析 ==============

def parse_markdown_file(file_path: str) -> dict:
    """
    解析 Markdown 文件，提取 frontmatter 和正文内容
    
    支持的 Frontmatter 格式:
    ---
    title: 接口设计文档
    type: api_design
    module: 用户模块
    tags: [API, 用户]
    summary: 用户管理相关接口定义
    ---
    # 正文内容...
    
    Args:
        file_path: 文件路径（绝对路径或相对路径）
    
    Returns:
        解析结果字典：
        {
            "title": str,        # 标题（从 frontmatter 或第一个 # 标题提取）
            "doc_type": str,     # 文档类型
            "content": str,      # 正文内容（不含 frontmatter）
            "summary": str,      # 摘要
            "module_name": str,  # 模块名称
            "tags": list,        # 标签列表
            "task_code": str,    # 关联任务编号
        }
    
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件格式不正确
    """
    path = Path(file_path).expanduser().resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if not path.suffix.lower() in [".md", ".markdown"]:
        raise ValueError(f"不支持的文件格式: {path.suffix}，仅支持 .md 或 .markdown")
    
    content = path.read_text(encoding="utf-8")
    
    result = {
        "title": None,
        "doc_type": None,
        "content": content,
        "summary": None,
        "module_name": None,
        "tags": None,
        "task_code": None,
        "file_name": path.name,
    }
    
    # 尝试解析 YAML frontmatter
    frontmatter_pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        frontmatter_text = match.group(1)
        body_content = content[match.end():]
        result["content"] = body_content.strip()
        
        # 简单的 YAML 解析（避免引入额外依赖）
        for line in frontmatter_text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                
                # 移除引号
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                if key == "title":
                    result["title"] = value
                elif key == "type" or key == "doc_type":
                    result["doc_type"] = value
                elif key == "module" or key == "module_name":
                    result["module_name"] = value
                elif key == "summary" or key == "description":
                    result["summary"] = value
                elif key == "task" or key == "task_code":
                    result["task_code"] = value
                elif key == "tags":
                    # 解析 tags: [tag1, tag2] 或 tags: tag1, tag2
                    if value.startswith("[") and value.endswith("]"):
                        value = value[1:-1]
                    tags = [t.strip().strip('"').strip("'") for t in value.split(",")]
                    result["tags"] = [t for t in tags if t]
    
    # 如果没有从 frontmatter 获取标题，尝试从正文第一个 # 标题提取
    if not result["title"]:
        title_match = re.search(r"^#\s+(.+)$", result["content"], re.MULTILINE)
        if title_match:
            result["title"] = title_match.group(1).strip()
        else:
            # 使用文件名作为标题
            result["title"] = path.stem
    
    # 默认文档类型
    if not result["doc_type"]:
        result["doc_type"] = "technical_memo"
    
    return result


# ============== Project 源操作（本地 docs/） ==============

async def _handle_project_search(
    docs_provider: "DocsResourceProvider", args: dict
) -> list[TextContent]:
    """处理项目文档搜索"""
    query = args.get("query")
    if not query:
        return [TextContent(type="text", text="❌ 请提供搜索关键词 (query 参数)")]
    
    scope = args.get("scope", "all")
    limit = args.get("limit", 5)

    results = []

    scope_dirs = {
        "all": [""],
        "design": ["02_设计文档"],
        "api": ["03_接口文档"],
        "database": ["04_数据库文档"],
        "module": ["06_模块文档"],
        "guide": ["05_开发指南"],
    }

    dirs = scope_dirs.get(scope, [""])

    for dir_name in dirs:
        search_path = docs_provider.docs_root / dir_name
        if not search_path.exists():
            continue

        for md_file in search_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if query.lower() in content.lower():
                    results.append({
                        "file": str(md_file.relative_to(docs_provider.docs_root)),
                        "snippet": extract_snippet(content, query),
                    })
            except Exception:
                continue

    # 格式化输出
    scope_labels = {
        "all": "全部",
        "design": "设计文档",
        "api": "接口文档",
        "database": "数据库文档",
        "module": "模块文档",
        "guide": "开发指南",
    }
    scope_label = scope_labels.get(scope, scope)
    
    output = f"🔍 **文档搜索结果** (project 源)\n\n"
    output += f"**关键词**: {query} | **范围**: {scope_label}\n"
    output += f"**找到**: {len(results)} 个相关文档\n\n"
    output += "---\n\n"
    
    for i, r in enumerate(results[:limit], 1):
        output += f"### {i}. {r['file']}\n\n"
        output += f"```\n{r['snippet']}\n```\n\n"

    if not results:
        output += f"未找到包含 \"{query}\" 的文档\n\n"
        output += "💡 **建议**：\n"
        output += "- 尝试使用更通用的关键词\n"
        output += "- 调整搜索范围 (scope 参数)\n"
        output += "- 使用 source=\"dev\" 搜索数据库文档\n"

    if len(results) > limit:
        output += f"\n_显示前 {limit} 个结果，共 {len(results)} 个_\n"

    return [TextContent(type="text", text=output)]


async def _handle_project_context(
    docs_provider: "DocsResourceProvider", args: dict
) -> list[TextContent]:
    """处理获取任务上下文"""
    task_code = args.get("task_code")
    module = args.get("module", "").lower()
    
    # 如果没有提供 task_code，尝试从上下文获取
    if not task_code:
        try:
            from ..context import get_context
            ctx = get_context()
            task_code = ctx.current_task_code
        except Exception:
            pass
    
    if not task_code and not module:
        return [TextContent(
            type="text",
            text="❌ 请提供 task_code 或 module 参数"
        )]

    context_docs = []

    # 收集相关文档
    if module:
        # 设计文档
        design_doc = await docs_provider.get_resource(f"docs://design/{module}")
        if design_doc:
            context_docs.append(("设计文档", design_doc))

        # 接口文档
        api_doc = await docs_provider.get_resource(f"docs://api/{module}")
        if api_doc:
            context_docs.append(("接口文档", api_doc))

        # 模块文档
        module_doc = await docs_provider.get_resource(f"docs://module/{module}")
        if module_doc:
            context_docs.append(("模块文档", module_doc))

    # 数据库 ER 图（通用）
    er_doc = await docs_provider.get_resource("docs://database/er")
    if er_doc:
        if module:
            er_content = extract_relevant_tables(er_doc, module)
        else:
            er_content = truncate_content(er_doc, max_lines=50)
        context_docs.append(("数据模型", er_content))

    # 格式化输出
    output = f"""📚 **开发上下文** (project 源)

**任务**: {task_code or '未指定'}
**模块**: {module or '未指定'}

---

"""

    for doc_type, content in context_docs:
        output += f"## 📄 {doc_type}\n\n"
        output += truncate_content(content, max_lines=100)
        output += "\n\n---\n\n"

    if not context_docs:
        output += "未找到相关文档。\n\n"
        output += "💡 **建议**：\n"
        output += "- 指定正确的模块名称 (module 参数)\n"
        output += "- 使用 action=\"search\" 搜索相关文档\n"
        output += "- 使用 source=\"dev\" 搜索数据库文档\n"

    return [TextContent(type="text", text=output)]


# ============== Dev 源操作（数据库） ==============

async def _handle_dev_search(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """处理数据库文档搜索"""
    query = args.get("query")
    if not query:
        return [TextContent(type="text", text="❌ 请提供搜索关键词 (query 参数)")]
    
    doc_type = args.get("doc_type")
    module_name = args.get("module_name") or args.get("module")
    limit = args.get("limit", 10)
    
    try:
        result = await client.search_dev_documents(
            query=query,
            doc_type=doc_type,
            module_name=module_name,
            limit=limit,
        )
        
        docs = result.get("data", result) if isinstance(result, dict) else []
        if isinstance(docs, dict) and "items" in docs:
            docs = docs["items"]
        
        output = f"🔍 **文档搜索结果** (dev 源)\n\n"
        output += f"**关键词**: {query}\n"
        if doc_type:
            output += f"**类型**: {format_doc_type(doc_type)}\n"
        if module_name:
            output += f"**模块**: {module_name}\n"
        output += f"**找到**: {len(docs) if isinstance(docs, list) else 0} 个相关文档\n\n"
        output += "---\n\n"
        
        if isinstance(docs, list) and docs:
            for i, doc in enumerate(docs[:limit], 1):
                doc_code = doc.get("doc_code", "")
                title = doc.get("title", "")
                doc_type_val = doc.get("doc_type", "")
                summary = doc.get("summary", "")[:100] if doc.get("summary") else ""
                
                output += f"### {i}. [{doc_code}] {title}\n\n"
                output += f"**类型**: {format_doc_type(doc_type_val)}"
                if doc.get("module_name"):
                    output += f" | **模块**: {doc.get('module_name')}"
                output += "\n\n"
                if summary:
                    output += f"_{summary}..._\n\n"
        else:
            output += f"未找到包含 \"{query}\" 的文档\n\n"
            output += "💡 **建议**：\n"
            output += "- 尝试使用更通用的关键词\n"
            output += "- 使用 action=\"list\" 查看所有文档\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 搜索失败: {str(e)}")]


async def _handle_dev_get(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """获取文档详情"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    try:
        result = await client.get_dev_document(doc_code)
        doc = result.get("data", result) if isinstance(result, dict) else result
        
        if not doc:
            return [TextContent(type="text", text=f"❌ 文档不存在: {doc_code}")]
        
        output = f"📄 **文档详情**\n\n"
        output += f"**编号**: {doc.get('doc_code', doc_code)}\n"
        output += f"**标题**: {doc.get('title', '')}\n"
        output += f"**类型**: {format_doc_type(doc.get('doc_type', ''))}\n"
        output += f"**状态**: {doc.get('status', 'draft')}\n"
        output += f"**版本**: v{doc.get('current_version', 1)}\n"
        
        if doc.get("module_name"):
            output += f"**模块**: {doc.get('module_name')}\n"
        if doc.get("task_code"):
            output += f"**关联任务**: {doc.get('task_code')}\n"
        if doc.get("tags"):
            output += f"**标签**: {', '.join(doc.get('tags', []))}\n"
        
        output += f"\n---\n\n"
        
        if doc.get("summary"):
            output += f"**摘要**: {doc.get('summary')}\n\n"
        
        output += "## 正文内容\n\n"
        content = doc.get("content", "")
        output += truncate_content(content, max_lines=200)
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取文档失败: {str(e)}")]


async def _handle_dev_create(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """创建文档"""
    title = args.get("title")
    doc_type = args.get("doc_type")
    content = args.get("content")
    
    if not title:
        return [TextContent(type="text", text="❌ 请提供文档标题 (title 参数)")]
    if not doc_type:
        return [TextContent(type="text", text="❌ 请提供文档类型 (doc_type 参数)")]
    if not content:
        return [TextContent(type="text", text="❌ 请提供文档内容 (content 参数)")]
    
    # 如果没有提供 task_code，尝试从上下文获取当前任务
    task_code = args.get("task_code")
    if not task_code:
        try:
            from ..context import get_context
            ctx = get_context()
            task_code = ctx.current_task_code
        except Exception:
            pass
    
    try:
        result = await client.create_dev_document(
            title=title,
            doc_type=doc_type,
            content=content,
            summary=args.get("summary"),
            module_name=args.get("module_name") or args.get("module"),
            task_code=task_code,
            tags=args.get("tags"),
            is_ai_generated=True,
            status=args.get("status", "draft"),
        )
        
        doc = result.get("data", result) if isinstance(result, dict) else result
        doc_code = doc.get("doc_code", "")
        
        output = f"✅ **文档创建成功**\n\n"
        output += f"**编号**: {doc_code}\n"
        output += f"**标题**: {title}\n"
        output += f"**类型**: {format_doc_type(doc_type)}\n"
        output += f"**状态**: {args.get('status', 'draft')}\n"
        
        if args.get("module_name") or args.get("module"):
            output += f"**模块**: {args.get('module_name') or args.get('module')}\n"
        if task_code:
            auto_hint = "（自动关联）" if not args.get("task_code") else ""
            output += f"**关联任务**: {task_code} {auto_hint}\n"
        
        output += f"\n💡 使用 `doc_code=\"{doc_code}\"` 可获取或更新此文档\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 创建文档失败: {str(e)}")]


async def _handle_dev_update(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """更新文档"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    # 检查是否有要更新的字段
    update_fields = ["title", "content", "summary", "module_name", "tags", "status"]
    has_update = any(args.get(f) is not None for f in update_fields)
    
    if not has_update:
        return [TextContent(type="text", text="❌ 请提供要更新的字段（title/content/summary/module_name/tags/status）")]
    
    try:
        result = await client.update_dev_document(
            doc_code=doc_code,
            title=args.get("title"),
            content=args.get("content"),
            summary=args.get("summary"),
            module_name=args.get("module_name") or args.get("module"),
            tags=args.get("tags"),
            status=args.get("status"),
            change_note=args.get("change_note"),
        )
        
        doc = result.get("data", result) if isinstance(result, dict) else result
        new_version = doc.get("current_version", 1)
        
        output = f"✅ **文档更新成功**\n\n"
        output += f"**编号**: {doc_code}\n"
        output += f"**当前版本**: v{new_version}\n"
        
        if args.get("change_note"):
            output += f"**变更说明**: {args.get('change_note')}\n"
        
        updated_fields = [f for f in update_fields if args.get(f) is not None]
        output += f"**更新字段**: {', '.join(updated_fields)}\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 更新文档失败: {str(e)}")]


async def _handle_dev_list(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """列出文档"""
    try:
        result = await client.list_dev_documents(
            doc_type=args.get("doc_type"),
            status=args.get("status"),
            module_name=args.get("module_name") or args.get("module"),
            task_code=args.get("task_code"),
            keyword=args.get("query"),  # 支持关键词搜索
            page=1,
            page_size=args.get("limit", 20),
        )
        
        data = result.get("data", result) if isinstance(result, dict) else result
        docs = data.get("items", []) if isinstance(data, dict) else data
        total = data.get("total", len(docs)) if isinstance(data, dict) else len(docs)
        
        output = f"📋 **文档列表** (dev 源)\n\n"
        
        # 显示筛选条件
        filters = []
        if args.get("doc_type"):
            filters.append(f"类型={format_doc_type(args['doc_type'])}")
        if args.get("status"):
            filters.append(f"状态={args['status']}")
        if args.get("module_name") or args.get("module"):
            filters.append(f"模块={args.get('module_name') or args.get('module')}")
        if args.get("task_code"):
            filters.append(f"任务={args['task_code']}")
        
        if filters:
            output += f"**筛选**: {' | '.join(filters)}\n"
        output += f"**总数**: {total} 个文档\n\n"
        output += "---\n\n"
        
        if docs:
            for doc in docs:
                doc_code = doc.get("doc_code", "")
                title = doc.get("title", "")
                doc_type_val = doc.get("doc_type", "")
                status = doc.get("status", "draft")
                version = doc.get("current_version", 1)
                
                status_icon = {"draft": "📝", "published": "✅", "archived": "📦"}.get(status, "📄")
                
                output += f"- {status_icon} **[{doc_code}]** {title}\n"
                output += f"  类型: {format_doc_type(doc_type_val)} | 版本: v{version}"
                if doc.get("module_name"):
                    output += f" | 模块: {doc.get('module_name')}"
                output += "\n\n"
        else:
            output += "暂无文档\n\n"
            output += "💡 使用 action=\"create\" 创建新文档\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取列表失败: {str(e)}")]


async def _handle_dev_versions(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """获取文档版本历史"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    version = args.get("version")
    
    try:
        if version:
            # 获取特定版本内容
            result = await client.get_dev_document_version(doc_code, version)
            ver_data = result.get("data", result) if isinstance(result, dict) else result
            
            output = f"📄 **文档历史版本**\n\n"
            output += f"**编号**: {doc_code}\n"
            output += f"**版本**: v{version}\n"
            
            if ver_data.get("change_note"):
                output += f"**变更说明**: {ver_data.get('change_note')}\n"
            if ver_data.get("created_at"):
                output += f"**创建时间**: {ver_data.get('created_at')}\n"
            
            output += f"\n---\n\n"
            output += "## 版本内容\n\n"
            content = ver_data.get("content", "")
            output += truncate_content(content, max_lines=200)
            
        else:
            # 列出版本历史
            result = await client.list_dev_document_versions(doc_code)
            data = result.get("data", result) if isinstance(result, dict) else result
            versions = data.get("items", []) if isinstance(data, dict) else data
            
            output = f"📜 **版本历史** - {doc_code}\n\n"
            output += f"**版本数**: {len(versions)}\n\n"
            output += "---\n\n"
            
            if versions:
                for ver in versions:
                    ver_num = ver.get("version", 0)
                    change_note = ver.get("change_note", "")
                    created_at = ver.get("created_at", "")
                    
                    output += f"- **v{ver_num}** - {created_at[:10] if created_at else ''}\n"
                    if change_note:
                        output += f"  _{change_note}_\n"
                    output += "\n"
                
                output += "\n💡 使用 `version=N` 参数可获取特定版本内容\n"
            else:
                output += "暂无版本历史\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 获取版本历史失败: {str(e)}")]


async def _handle_dev_upload(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """
    上传 MD 文件并解析入库
    
    支持的 Frontmatter 字段:
    - title: 文档标题
    - type/doc_type: 文档类型
    - module/module_name: 所属模块
    - summary/description: 摘要
    - tags: 标签列表
    - task/task_code: 关联任务
    """
    file_path = args.get("file_path")
    if not file_path:
        return [TextContent(type="text", text="❌ 请提供文件路径 (file_path 参数)")]
    
    try:
        # 1. 解析 MD 文件
        parsed = parse_markdown_file(file_path)
        
        # 2. 合并命令行参数（优先使用命令行参数覆盖 frontmatter）
        title = args.get("title") or parsed["title"]
        doc_type = args.get("doc_type") or parsed["doc_type"]
        content = parsed["content"]
        summary = args.get("summary") or parsed["summary"]
        module_name = args.get("module_name") or args.get("module") or parsed["module_name"]
        task_code = args.get("task_code") or parsed["task_code"]
        tags = args.get("tags") or parsed["tags"]
        status = args.get("status", "draft")
        
        # 如果没有提供 task_code，尝试从上下文获取当前任务
        task_code_auto_linked = False
        if not task_code:
            try:
                from ..context import get_context
                ctx = get_context()
                if ctx.current_task_code:
                    task_code = ctx.current_task_code
                    task_code_auto_linked = True
            except Exception:
                pass
        
        # 3. 验证必填字段
        if not title:
            return [TextContent(
                type="text",
                text=f"❌ 无法确定文档标题\n\n"
                     f"请在 frontmatter 中添加 `title` 字段，或在命令行参数中指定 `title`\n\n"
                     f"**解析到的文件**: {parsed['file_name']}"
            )]
        
        if not content or len(content.strip()) < 10:
            return [TextContent(
                type="text",
                text=f"❌ 文档内容为空或过短\n\n"
                     f"**文件**: {parsed['file_name']}"
            )]
        
        # 4. 验证文档类型
        valid_doc_types = [
            "architecture", "data_model", "api_design", "technical_memo",
            "problem_record", "change_summary", "implementation", "best_practice",
            "prompt_template", "retrospective", "weekly_report", "meeting_notes",
            "transcript", "consulting_report", "analysis_report", "workflow",
            "product_spec", "learning_notes", "strategy"
        ]
        if doc_type not in valid_doc_types:
            return [TextContent(
                type="text",
                text=f"❌ 无效的文档类型: {doc_type}\n\n"
                     f"**有效类型**: {', '.join(valid_doc_types)}\n\n"
                     f"请在 frontmatter 的 `type` 字段中指定有效类型，或使用 `doc_type` 参数覆盖"
            )]
        
        # 5. 判断是创建还是更新
        doc_code = args.get("doc_code")
        change_note = args.get("change_note")
        is_update = bool(doc_code)
        
        if is_update:
            # 更新已有文档
            # 如果没有提供 change_note，自动生成
            if not change_note:
                change_note = f"通过文件上传更新 ({parsed['file_name']})"
            
            result = await client.update_dev_document(
                doc_code=doc_code,
                title=title,
                content=content,
                summary=summary,
                module_name=module_name,
                tags=tags,
                status=status,
                change_note=change_note,
            )
        else:
            # 创建新文档
            result = await client.create_dev_document(
                title=title,
                doc_type=doc_type,
                content=content,
                summary=summary,
                module_name=module_name,
                task_code=task_code,
                tags=tags,
                is_ai_generated=False,  # 上传的文件标记为非 AI 生成
                status=status,
            )
        
        doc = result.get("data", result) if isinstance(result, dict) else result
        result_doc_code = doc.get("doc_code", doc_code or "")
        new_version = doc.get("current_version", 1)
        
        # 6. 构建成功响应
        if is_update:
            output = f"✅ **文档更新成功**\n\n"
            output += f"**源文件**: {parsed['file_name']}\n"
            output += f"**文档编号**: {result_doc_code}\n"
            output += f"**标题**: {title}\n"
            output += f"**当前版本**: v{new_version}\n"
            output += f"**变更说明**: {change_note}\n"
            
            if module_name:
                output += f"**模块**: {module_name}\n"
            if tags:
                output += f"**标签**: {', '.join(tags)}\n"
        else:
            output = f"✅ **文件上传成功**\n\n"
            output += f"**源文件**: {parsed['file_name']}\n"
            output += f"**文档编号**: {result_doc_code}\n"
            output += f"**标题**: {title}\n"
            output += f"**类型**: {format_doc_type(doc_type)}\n"
            output += f"**状态**: {status}\n"
            
            if module_name:
                output += f"**模块**: {module_name}\n"
            if task_code:
                auto_hint = "（自动关联）" if task_code_auto_linked else ""
                output += f"**关联任务**: {task_code} {auto_hint}\n"
            if tags:
                output += f"**标签**: {', '.join(tags)}\n"
        
        # 显示内容统计
        line_count = len(content.split("\n"))
        char_count = len(content)
        output += f"\n**内容统计**: {line_count} 行, {char_count} 字符\n"
        
        if is_update:
            output += f"\n💡 使用 `action=\"versions\", doc_code=\"{result_doc_code}\"` 可查看版本历史\n"
        else:
            output += f"\n💡 使用 `doc_code=\"{result_doc_code}\"` 可获取或更新此文档\n"
        
        return [TextContent(type="text", text=output)]
        
    except FileNotFoundError as e:
        return [TextContent(type="text", text=f"❌ 文件不存在: {file_path}")]
        
    except ValueError as e:
        return [TextContent(type="text", text=f"❌ 文件格式错误: {str(e)}")]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 上传失败: {str(e)}")]


# ============== 评论操作 ==============

async def _handle_dev_comment(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """处理文档评论操作"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    comment_action = args.get("comment_action", "list")
    
    try:
        if comment_action == "list":
            # 获取评论列表
            result = await client.list_document_comments(doc_code)
            data = result.get("data", result) if isinstance(result, dict) else result
            comments = data.get("items", data) if isinstance(data, dict) else data
            
            if not isinstance(comments, list):
                comments = []
            
            output = f"💬 **文档评论** - {doc_code}\n\n"
            output += f"**评论数**: {len(comments)}\n\n"
            output += "---\n\n"
            
            if comments:
                def format_comment(comment: dict, indent: int = 0) -> str:
                    """格式化单条评论（支持递归处理回复）"""
                    prefix = "  " * indent
                    result = ""
                    
                    comment_id = comment.get("id", "")
                    content = comment.get("content", "")
                    created_at = comment.get("created_at", "")
                    author = comment.get("author_name") or comment.get("author", {}).get("username", "匿名")
                    
                    # 格式化时间
                    time_str = created_at[:16].replace("T", " ") if created_at else ""
                    
                    if indent == 0:
                        result += f"{prefix}**#{comment_id}** - {author} ({time_str})\n"
                    else:
                        result += f"{prefix}↳ **#{comment_id}** - {author} ({time_str})\n"
                    result += f"{prefix}  {content}\n\n"
                    
                    # 处理回复（子评论）
                    replies = comment.get("replies", [])
                    for reply in replies:
                        result += format_comment(reply, indent + 1)
                    
                    return result
                
                for comment in comments:
                    output += format_comment(comment)
            else:
                output += "_暂无评论_\n\n"
            
            output += "\n💡 **操作提示**：\n"
            output += "- 添加评论: `comment_action=\"add\", comment_content=\"...\"`\n"
            output += "- 回复评论: `comment_action=\"add\", comment_content=\"...\", parent_id=评论ID`\n"
            output += "- 删除评论: `comment_action=\"delete\", comment_id=评论ID`\n"
            
            return [TextContent(type="text", text=output)]
        
        elif comment_action == "add":
            # 添加评论
            comment_content = args.get("comment_content")
            if not comment_content:
                return [TextContent(type="text", text="❌ 请提供评论内容 (comment_content 参数)")]
            
            parent_id = args.get("parent_id")
            
            result = await client.add_document_comment(
                doc_code=doc_code,
                content=comment_content,
                parent_id=parent_id,
            )
            
            comment = result.get("data", result) if isinstance(result, dict) else result
            comment_id = comment.get("id", "")
            
            output = f"✅ **评论添加成功**\n\n"
            output += f"**文档**: {doc_code}\n"
            output += f"**评论ID**: #{comment_id}\n"
            if parent_id:
                output += f"**回复**: #{parent_id}\n"
            output += f"\n**内容**: {comment_content}\n"
            
            return [TextContent(type="text", text=output)]
        
        elif comment_action == "delete":
            # 删除评论
            comment_id = args.get("comment_id")
            if not comment_id:
                return [TextContent(type="text", text="❌ 请提供评论ID (comment_id 参数)")]
            
            await client.delete_document_comment(doc_code, comment_id)
            
            output = f"✅ **评论删除成功**\n\n"
            output += f"**文档**: {doc_code}\n"
            output += f"**评论ID**: #{comment_id}\n"
            
            return [TextContent(type="text", text=output)]
        
        else:
            return [TextContent(
                type="text",
                text=f"❌ 未知评论操作: {comment_action}。支持的操作: list, add, delete"
            )]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 评论操作失败: {str(e)}")]


# ============== 文档生命周期操作 ==============

async def _handle_dev_delete(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """删除文档"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    try:
        result = await client.delete_dev_document(doc_code)
        
        # 检查响应
        if isinstance(result, dict):
            success = result.get("success", True)
            message = result.get("message", "")
            if not success:
                return [TextContent(type="text", text=f"❌ 删除失败: {message}")]
        
        output = f"✅ **文档删除成功**\n\n"
        output += f"**编号**: {doc_code}\n"
        output += f"\n⚠️ 此操作不可撤销，文档已被永久删除。\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 删除文档失败: {str(e)}")]


async def _handle_dev_publish(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """发布文档"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    try:
        result = await client.publish_dev_document(doc_code)
        
        # 检查响应
        if isinstance(result, dict):
            success = result.get("success", True)
            message = result.get("message", "")
            if not success:
                return [TextContent(type="text", text=f"❌ 发布失败: {message}")]
            
            doc = result.get("data", {})
        else:
            doc = {}
        
        output = f"✅ **文档发布成功**\n\n"
        output += f"**编号**: {doc_code}\n"
        output += f"**状态**: draft → published\n"
        
        if doc.get("title"):
            output += f"**标题**: {doc.get('title')}\n"
        if doc.get("current_version"):
            output += f"**版本**: v{doc.get('current_version')}\n"
        
        output += f"\n📢 文档已发布，现在所有用户都可以查看。\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 发布文档失败: {str(e)}")]


async def _handle_dev_archive(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """归档文档"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    try:
        result = await client.archive_dev_document(doc_code)
        
        # 检查响应
        if isinstance(result, dict):
            success = result.get("success", True)
            message = result.get("message", "")
            if not success:
                return [TextContent(type="text", text=f"❌ 归档失败: {message}")]
            
            doc = result.get("data", {})
        else:
            doc = {}
        
        output = f"📦 **文档归档成功**\n\n"
        output += f"**编号**: {doc_code}\n"
        output += f"**状态**: → archived\n"
        
        if doc.get("title"):
            output += f"**标题**: {doc.get('title')}\n"
        
        output += f"\n💡 归档的文档不会在默认列表中显示，但可以通过 status=\"archived\" 筛选查看。\n"
        output += f"💡 使用 action=\"unarchive\" 可以取消归档。\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 归档文档失败: {str(e)}")]


async def _handle_dev_unarchive(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """取消归档"""
    doc_code = args.get("doc_code")
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    
    try:
        result = await client.unarchive_dev_document(doc_code)
        
        # 检查响应
        if isinstance(result, dict):
            success = result.get("success", True)
            message = result.get("message", "")
            if not success:
                return [TextContent(type="text", text=f"❌ 取消归档失败: {message}")]
            
            doc = result.get("data", {})
        else:
            doc = {}
        
        output = f"📄 **取消归档成功**\n\n"
        output += f"**编号**: {doc_code}\n"
        output += f"**状态**: archived → draft\n"
        
        if doc.get("title"):
            output += f"**标题**: {doc.get('title')}\n"
        
        output += f"\n💡 文档已恢复为草稿状态，现在可以在默认列表中查看和编辑。\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 取消归档失败: {str(e)}")]


async def _handle_dev_restore(
    client: "TestHubAPIClient", args: dict
) -> list[TextContent]:
    """恢复到历史版本"""
    doc_code = args.get("doc_code")
    version = args.get("version")
    change_note = args.get("change_note")
    
    if not doc_code:
        return [TextContent(type="text", text="❌ 请提供文档编号 (doc_code 参数)")]
    if not version:
        return [TextContent(type="text", text="❌ 请提供要恢复的版本号 (version 参数)")]
    
    try:
        result = await client.restore_dev_document_version(
            doc_code=doc_code,
            version=version,
            change_note=change_note,
        )
        
        # 检查响应
        if isinstance(result, dict):
            success = result.get("success", True)
            message = result.get("message", "")
            if not success:
                return [TextContent(type="text", text=f"❌ 恢复版本失败: {message}")]
            
            doc = result.get("data", {})
        else:
            doc = {}
        
        new_version = doc.get("current_version", version + 1)
        
        output = f"🔄 **版本恢复成功**\n\n"
        output += f"**编号**: {doc_code}\n"
        output += f"**恢复版本**: v{version}\n"
        output += f"**新版本号**: v{new_version}\n"
        
        if change_note:
            output += f"**变更说明**: {change_note}\n"
        else:
            output += f"**变更说明**: 恢复到版本 v{version}\n"
        
        if doc.get("title"):
            output += f"**标题**: {doc.get('title')}\n"
        
        output += f"\n💡 当前内容已保存为新版本，文档内容已恢复到 v{version} 的状态。\n"
        output += f"💡 使用 action=\"versions\" 可以查看完整版本历史。\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 恢复版本失败: {str(e)}")]


# ============== 主处理函数 ==============

async def handle_unified_docs(
    docs_provider: "DocsResourceProvider",
    args: dict,
    api_client: "TestHubAPIClient" = None,
) -> list[TextContent]:
    """
    处理统一文档工具调用
    
    Args:
        docs_provider: 项目文档资源提供者
        args: 工具参数
        api_client: API 客户端（可选，用于 dev 源操作）
    """
    action = args.get("action")
    source = args.get("source", "project")
    
    if not action:
        return [TextContent(type="text", text="❌ 请提供 action 参数")]
    
    # Project 源操作（本地 docs/）
    if source == "project":
        if action == "search":
            return await _handle_project_search(docs_provider, args)
        elif action == "context":
            return await _handle_project_context(docs_provider, args)
        elif action in ["get", "create", "update", "upload", "list", "versions", "delete", "publish", "archive", "unarchive", "restore", "comment"]:
            return [TextContent(
                type="text",
                text=f"❌ project 源不支持 {action} 操作。请使用 source=\"dev\" 访问数据库文档。"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ 未知操作: {action}。支持的操作: search, context"
            )]
    
    # Dev 源操作（数据库）
    elif source == "dev":
        # 检查 API 客户端
        if api_client is None:
            # 尝试从 server 获取
            try:
                from ..server import get_api_client
                api_client = get_api_client()
            except Exception:
                pass
        
        if api_client is None:
            return [TextContent(
                type="text",
                text="❌ API 未配置。dev 源需要配置 TESTHUB_API_URL、TESTHUB_API_TOKEN、TESTHUB_TEAM_ID 环境变量。"
            )]
        
        if action == "search":
            return await _handle_dev_search(api_client, args)
        elif action == "get":
            return await _handle_dev_get(api_client, args)
        elif action == "create":
            return await _handle_dev_create(api_client, args)
        elif action == "update":
            return await _handle_dev_update(api_client, args)
        elif action == "upload":
            return await _handle_dev_upload(api_client, args)
        elif action == "list":
            return await _handle_dev_list(api_client, args)
        elif action == "versions":
            return await _handle_dev_versions(api_client, args)
        elif action == "comment":
            return await _handle_dev_comment(api_client, args)
        elif action == "delete":
            return await _handle_dev_delete(api_client, args)
        elif action == "publish":
            return await _handle_dev_publish(api_client, args)
        elif action == "archive":
            return await _handle_dev_archive(api_client, args)
        elif action == "unarchive":
            return await _handle_dev_unarchive(api_client, args)
        elif action == "restore":
            return await _handle_dev_restore(api_client, args)
        elif action == "context":
            return [TextContent(
                type="text",
                text="❌ dev 源不支持 context 操作。请使用 source=\"project\" 获取项目文档上下文。"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ 未知操作: {action}。支持的操作: search, get, create, update, upload, list, versions, delete, publish, archive, unarchive, restore, comment"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"❌ 未知数据源: {source}。支持的数据源: project, dev"
        )]


# ============== 获取工具 ==============

def get_unified_docs_tool() -> Tool:
    """获取统一文档工具定义"""
    return unified_docs_tool()
