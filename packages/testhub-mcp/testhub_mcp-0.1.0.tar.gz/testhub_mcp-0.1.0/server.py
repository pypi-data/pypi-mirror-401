"""
TestHub MCP Server 主入口

提供以下功能：
- Resources: 项目文档资源访问
- Tools: 任务管理、文档搜索、评审管理、缺陷管理等工具
"""

import os
import time
import asyncio
from contextvars import ContextVar
from typing import Optional, Any, Dict

from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from loguru import logger

from .resources.docs import DocsResourceProvider

# 创建 MCP Server 实例
server = Server("testhub-mcp")


# ========== 认证上下文管理 ==========
# 使用 ContextVar 支持并发 SSE 连接，每个连接有独立的认证上下文

_auth_context: ContextVar[Dict[str, Any]] = ContextVar('auth_context', default={})


def set_auth_context(
    token: str, 
    team_id: int, 
    user_id: Optional[int] = None,
    session_id: Optional[int] = None
) -> None:
    """
    设置当前连接的认证上下文
    
    由后端 SSE 端点在验证 Token 后调用，设置认证信息供 MCP 工具使用。
    使用 ContextVar 确保并发连接之间的隔离。
    
    Args:
        token: API Token
        team_id: 团队 ID
        user_id: 用户 ID（可选）
        session_id: 开发会话 ID（可选，用于指定任务归属）
    """
    _auth_context.set({
        "token": token,
        "team_id": team_id,
        "user_id": user_id,
        "session_id": session_id,
    })
    logger.debug(f"MCP 认证上下文已设置: team_id={team_id}, user_id={user_id}, session_id={session_id}")


def get_auth_context() -> Dict[str, Any]:
    """
    获取当前连接的认证上下文
    
    Returns:
        包含 token, team_id, user_id 的字典，如果未设置则返回空字典
    """
    return _auth_context.get()


def clear_auth_context() -> None:
    """清除当前连接的认证上下文"""
    _auth_context.set({})
    logger.debug("MCP 认证上下文已清除")


# ========== 工具分类映射 ==========

TOOL_CATEGORY_MAP = {
    # 核心工具（新版统一入口）
    "testhub_start": "core",
    "testhub_finish": "core",
    "testhub_log": "core",
    "testhub_status": "core",
    "testhub_pause": "core",
    "testhub_block": "core",
    "testhub_resume": "core",
    
    # 统一工具（新版简化入口）
    "testhub_docs": "docs",
    "testhub_bug": "bug",
    "testhub_search": "search",
    "testhub_test": "test",
    
    # 常用辅助工具
    "testhub_get_task": "task",
    "testhub_task_overview": "task",
    "testhub_list_my_tasks": "task",
    "testhub_daily_summary": "suggest",
    "testhub_create_task": "task",
    "testhub_suggest_task": "suggest",
}


def get_tool_category(tool_name: str) -> str:
    """获取工具分类"""
    return TOOL_CATEGORY_MAP.get(tool_name, "other")

# 初始化文档资源提供者
docs_provider = DocsResourceProvider(
    docs_root=os.environ.get("PROJECT_DOCS_PATH", "./docs")
)

# API 客户端缓存（按认证上下文缓存）
# 注意：在 SSE 模式下，每个连接可能有不同的认证信息
_api_client_cache: Dict[str, "TestHubClient"] = {}


def get_api_client() -> Optional["TestHubClient"]:
    """
    获取 API 客户端实例
    
    优先级：
    1. 从认证上下文获取（SSE 模式）
    2. 从环境变量获取（stdio 模式）
    
    使用缓存避免重复创建客户端。
    """
    global _api_client_cache
    
    # 优先从认证上下文获取
    auth_ctx = get_auth_context()
    
    if auth_ctx and auth_ctx.get("token") and auth_ctx.get("team_id"):
        # SSE 模式：使用上下文中的认证信息
        api_token = auth_ctx["token"]
        team_id = auth_ctx["team_id"]
        api_url = os.environ.get("TESTHUB_API_URL")
        # 优先使用上下文中的 session_id，其次使用环境变量
        session_id = auth_ctx.get("session_id") or os.environ.get("TESTHUB_SESSION_ID")
        
        if api_url:
            # 使用 token 前缀 + session_id 作为缓存 key
            cache_key = f"{api_token[:20]}_{team_id}_{session_id or 'none'}"
            
            if cache_key not in _api_client_cache:
                from .api_client import TestHubClient
                _api_client_cache[cache_key] = TestHubClient(
                    base_url=api_url,
                    api_token=api_token,
                    team_id=int(team_id),
                    default_session_id=int(session_id) if session_id else None,
                )
                logger.debug(f"创建 API 客户端（SSE 模式）: team_id={team_id}, session_id={session_id}")
            
            return _api_client_cache[cache_key]
    
    # Fallback: 从环境变量获取（stdio 模式）
    api_url = os.environ.get("TESTHUB_API_URL")
    api_token = os.environ.get("TESTHUB_API_TOKEN")
    team_id = os.environ.get("TESTHUB_TEAM_ID")
    session_id = os.environ.get("TESTHUB_SESSION_ID")
    
    if api_url and api_token and team_id:
        cache_key = f"env_{api_token[:20]}_{team_id}_{session_id or 'none'}"
        
        if cache_key not in _api_client_cache:
            from .api_client import TestHubClient
            _api_client_cache[cache_key] = TestHubClient(
                base_url=api_url,
                api_token=api_token,
                team_id=int(team_id),
                default_session_id=int(session_id) if session_id else None,
            )
            logger.debug(f"创建 API 客户端（env 模式）: team_id={team_id}, session_id={session_id}")
        
        return _api_client_cache[cache_key]
    
    return None


def get_default_session_id() -> Optional[int]:
    """获取默认开发会话 ID"""
    session_id = os.environ.get("TESTHUB_SESSION_ID")
    return int(session_id) if session_id else None


def is_api_configured() -> bool:
    """
    检查 API 是否已配置
    
    检查顺序：
    1. 认证上下文（SSE 模式）
    2. 环境变量（stdio 模式）
    """
    # 检查认证上下文
    auth_ctx = get_auth_context()
    if auth_ctx and auth_ctx.get("token") and auth_ctx.get("team_id"):
        if os.environ.get("TESTHUB_API_URL"):
            return True
    
    # 检查环境变量
    return all([
        os.environ.get("TESTHUB_API_URL"),
        os.environ.get("TESTHUB_API_TOKEN"),
        os.environ.get("TESTHUB_TEAM_ID"),
    ])


async def _log_tool_call(
    tool_name: str,
    input_params: dict,
    output_result: Optional[list[TextContent]],
    error_message: Optional[str],
    duration_ms: int,
) -> None:
    """
    异步记录工具调用日志
    
    在工具调用完成后，异步发送日志到后端，不阻塞主流程。
    如果 API 未配置，则记录本地 debug 日志。
    """
    tool_category = get_tool_category(tool_name)
    is_success = error_message is None
    
    client = get_api_client()
    if not client:
        # API 未配置，记录本地日志并返回
        logger.debug(
            f"[本地日志] 工具调用: tool={tool_name}, "
            f"category={tool_category}, duration={duration_ms}ms, "
            f"success={is_success}, api_configured=False"
        )
        return
    
    try:
        # 获取当前会话编码（如果有）
        session_code = None
        try:
            from .context import get_context
            ctx = get_context()
            # 可以从上下文获取 session_code，如果有的话
            # 当前上下文没有 session_code 字段，但预留接口
            session_code = getattr(ctx, 'current_cursor_session_code', None)
        except Exception:
            pass
        
        # 准备输出结果字符串
        output_str = None
        if output_result:
            # 将 TextContent 列表转换为字符串
            texts = []
            for item in output_result:
                if hasattr(item, 'text'):
                    texts.append(item.text)
            output_str = "\n".join(texts) if texts else None
        
        # 异步发送日志
        await client.log_tool_call(
            tool_name=tool_name,
            tool_category=tool_category,
            input_params=input_params,
            output_result=output_str,
            is_success=is_success,
            error_message=error_message,
            duration_ms=duration_ms,
            session_code=session_code,
        )
        
        logger.debug(
            f"工具调用日志已记录: tool={tool_name}, "
            f"category={tool_category}, duration={duration_ms}ms, "
            f"success={is_success}"
        )
        
    except Exception as e:
        # 日志记录失败不应影响主流程，但记录警告
        logger.warning(
            f"记录工具调用日志失败: tool={tool_name}, "
            f"category={tool_category}, error={e}"
        )


@server.list_resources()
async def list_resources() -> list[Resource]:
    """列出所有文档资源"""
    resources = docs_provider.list_resources()
    return [
        Resource(
            uri=r["uri"],
            name=r["name"],
            description=r.get("description"),
            mimeType="text/markdown",
        )
        for r in resources
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """读取文档资源"""
    content = await docs_provider.get_resource(uri)
    if content is None:
        raise ValueError(f"Resource not found: {uri}")
    return content


# ========== 工具注册 ==========

# 核心工具（新版统一入口）
from .tools.core import (
    get_all_core_tools,
    handle_core_tool,
    CORE_TOOL_HANDLERS,
)

# 统一工具
from .tools.unified_docs import get_unified_docs_tool, handle_unified_docs
from .tools.unified_bug import get_unified_bug_tool, handle_unified_bug
from .tools.unified_search import get_unified_search_tool, handle_unified_search
from .tools.unified_test import get_unified_test_tool, handle_unified_test

# 辅助工具
from .tools.task import (
    get_task_tool,
    task_overview_tool,
    list_my_tasks_tool,
    handle_get_task,
    handle_task_overview,
    handle_list_my_tasks,
)
from .tools.suggest import (
    suggest_task_tool,
    create_task_tool,
    daily_summary_tool,
    handle_suggest_task,
    handle_create_task,
    handle_daily_summary,
)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    列出所有可用工具
    
    精简后的工具列表：
    - 核心工具 (7): testhub_start, testhub_finish, testhub_log, testhub_status,
                    testhub_pause, testhub_block, testhub_resume
    - 统一工具 (4): testhub_docs, testhub_bug, testhub_search, testhub_test
    - 辅助工具 (6): testhub_get_task, testhub_task_overview, testhub_list_my_tasks,
                    testhub_daily_summary, testhub_create_task, testhub_suggest_task
    """
    api_configured = is_api_configured()
    
    # 文档工具（始终可用）
    tools = [get_unified_docs_tool()]
    
    # API 相关工具（仅在 API 配置后可用）
    if api_configured:
        # 核心工具（新版统一入口）
        tools.extend(get_all_core_tools())
        
        # 统一工具
        tools.extend([
            get_unified_bug_tool(),
            get_unified_search_tool(),
            get_unified_test_tool(),
        ])
        
        # 常用辅助工具
        tools.extend([
            get_task_tool(),           # 获取任务详情
            task_overview_tool(),      # 任务总览
            list_my_tasks_tool(),      # 我的任务列表
            daily_summary_tool(),      # 每日摘要
            create_task_tool(),        # 创建任务
            suggest_task_tool(),       # 建议任务
        ])
    
    logger.debug(f"[list_tools] 返回 {len(tools)} 个工具, api_configured={api_configured}")
    return tools


# 全局任务集合，用于跟踪后台日志任务，防止被垃圾回收
_background_tasks: set = set()


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    处理工具调用
    
    包含日志采集功能，记录每次工具调用的参数、结果、耗时等信息。
    """
    start_time = time.time()
    result: Optional[list[TextContent]] = None
    error_message: Optional[str] = None
    
    try:
        result = await _execute_tool(name, arguments)
        return result
    except Exception as e:
        error_message = str(e)
        raise
    finally:
        # 计算执行耗时
        duration_ms = int((time.time() - start_time) * 1000)
        
        # 异步记录日志（不阻塞主流程）
        # 使用全局任务集合跟踪任务，防止被垃圾回收导致任务丢失
        try:
            task = asyncio.create_task(_log_tool_call(
                tool_name=name,
                input_params=arguments,
                output_result=result,
                error_message=error_message,
                duration_ms=duration_ms,
            ))
            # 添加到任务集合，防止被垃圾回收
            _background_tasks.add(task)
            # 任务完成后自动从集合移除
            task.add_done_callback(_background_tasks.discard)
        except Exception as log_error:
            logger.warning(f"创建日志任务失败: {log_error}")


async def _execute_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    执行工具调用的核心逻辑
    
    精简后的工具列表：
    - 核心工具: testhub_start, testhub_finish, testhub_log, testhub_status,
                testhub_pause, testhub_block, testhub_resume
    - 统一工具: testhub_docs, testhub_bug, testhub_search, testhub_test
    - 辅助工具: testhub_get_task, testhub_task_overview, testhub_list_my_tasks,
                testhub_daily_summary, testhub_create_task, testhub_suggest_task
    """
    # ========== 文档工具（始终可用） ==========
    if name == "testhub_docs":
        # 对于 dev 源需要传入 API 客户端
        api_client = get_api_client() if arguments.get("source") == "dev" else None
        return await handle_unified_docs(docs_provider, arguments, api_client=api_client)
    
    # ========== 需要 API 客户端的工具 ==========
    client = get_api_client()
    api_not_configured_msg = "❌ API 未配置。请设置 TESTHUB_API_URL、TESTHUB_API_TOKEN、TESTHUB_TEAM_ID 环境变量。"
    
    if not client:
        return [TextContent(type="text", text=api_not_configured_msg)]
    
    # ========== 核心工具 ==========
    if name in CORE_TOOL_HANDLERS:
        result = await handle_core_tool(client, name, arguments)
        if result is not None:
            return result
    
    # ========== 统一工具 ==========
    if name == "testhub_bug":
        return await handle_unified_bug(client, arguments)
    
    if name == "testhub_search":
        return await handle_unified_search(client, arguments)
    
    if name == "testhub_test":
        return await handle_unified_test(client, arguments)
    
    # ========== 辅助工具 ==========
    if name == "testhub_get_task":
        return await handle_get_task(client, arguments)

    if name == "testhub_task_overview":
        return await handle_task_overview(client, arguments)
    
    if name == "testhub_list_my_tasks":
        return await handle_list_my_tasks(client, arguments)

    if name == "testhub_daily_summary":
        return await handle_daily_summary(client, arguments)
    
    if name == "testhub_create_task":
        return await handle_create_task(client, arguments)
    
    if name == "testhub_suggest_task":
        return await handle_suggest_task(client, arguments)

    raise ValueError(f"Unknown tool: {name}")


def main():
    """
    MCP Server 入口点
    
    支持两种运行模式：
    1. stdio 模式（默认）：通过标准输入输出与 Cursor 通信，适合本地使用
       uvx --from testhub-mcp testhub-mcp
       
    2. sse 模式：通过 HTTP/SSE 提供服务，适合远程访问
       uvx --from testhub-mcp testhub-mcp --mode sse --port 8765
       或设置环境变量 MCP_MODE=sse MCP_PORT=8765
    
    Cursor 配置 SSE 模式：
    {
      "mcpServers": {
        "testhub": {
          "url": "http://your-server:8765/sse"
        }
      }
    }
    """
    import argparse
    import asyncio
    import os
    
    parser = argparse.ArgumentParser(description="TestHub MCP Server")
    parser.add_argument(
        "--mode", 
        choices=["stdio", "sse"], 
        default=os.environ.get("MCP_MODE", "stdio"),
        help="运行模式: stdio (本地) 或 sse (HTTP远程)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.environ.get("MCP_PORT", "8765")),
        help="SSE 模式下的 HTTP 端口 (默认: 8765)"
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("MCP_HOST", "0.0.0.0"),
        help="SSE 模式下的监听地址 (默认: 0.0.0.0)"
    )
    args = parser.parse_args()
    
    if args.mode == "sse":
        # SSE 模式：通过 HTTP 提供服务
        run_sse_server(args.host, args.port)
    else:
        # stdio 模式：通过标准输入输出
        run_stdio_server()


def run_stdio_server():
    """运行 stdio 模式的 MCP Server"""
    import asyncio
    from mcp.server.stdio import stdio_server
    from loguru import logger
    
    logger.info("启动 MCP Server (stdio 模式)")

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )

    asyncio.run(run())


def run_sse_server(host: str, port: int):
    """
    运行 SSE 模式的 MCP Server
    
    使用 Starlette 提供 HTTP/SSE 端点
    """
    import asyncio
    from loguru import logger
    
    try:
        from starlette.applications import Starlette
        from starlette.routing import Route
        from starlette.responses import JSONResponse
        from mcp.server.sse import SseServerTransport
        import uvicorn
    except ImportError:
        logger.error(
            "SSE 模式需要额外依赖，请安装：\n"
            "  pip install starlette uvicorn sse-starlette"
        )
        raise SystemExit(1)
    
    # 创建 SSE transport
    sse_transport = SseServerTransport("/messages")
    
    async def handle_sse(request):
        """处理 SSE 连接"""
        async with sse_transport.connect_sse(
            request.scope, 
            request.receive, 
            request._send
        ) as streams:
            await server.run(
                streams[0],
                streams[1],
                server.create_initialization_options(),
            )
    
    async def handle_messages(request):
        """处理消息端点"""
        await sse_transport.handle_post_message(
            request.scope,
            request.receive,
            request._send
        )
    
    async def health_check(request):
        """健康检查端点"""
        return JSONResponse({
            "status": "ok",
            "server": "testhub-mcp",
            "mode": "sse",
            "api_configured": is_api_configured(),
        })
    
    # 创建 Starlette 应用
    app = Starlette(
        debug=False,
        routes=[
            Route("/sse", handle_sse),
            Route("/messages", handle_messages, methods=["POST"]),
            Route("/health", health_check),
        ],
    )
    
    logger.info(f"启动 MCP Server (SSE 模式)")
    logger.info(f"监听地址: http://{host}:{port}")
    logger.info(f"SSE 端点: http://{host}:{port}/sse")
    logger.info(f"健康检查: http://{host}:{port}/health")
    
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()

