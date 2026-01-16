"""
TestHub MCP Server

一个用于 Cursor IDE 的 MCP (Model Context Protocol) 服务器，
提供 TestHub 开发任务管理和项目文档集成功能。

功能:
- Resources: 项目文档资源访问
- Tools: 
  - 任务管理（获取、更新状态、列表）
  - 文档搜索和上下文获取

配置环境变量:
- TESTHUB_API_URL: TestHub 后端 API 地址
- TESTHUB_API_TOKEN: 用户 API Token
- TESTHUB_TEAM_ID: 团队 ID
- TESTHUB_SESSION_ID: 默认开发会话 ID（可选）
- PROJECT_DOCS_PATH: 项目文档目录路径（可选，默认 ./docs）
"""

__version__ = "0.2.0"
__author__ = "TestHub Team"

from .server import (
    server,
    main,
    set_auth_context,
    get_auth_context,
    clear_auth_context,
    is_api_configured,
)
from .config import MCPConfig, get_config
from .api_client import TestHubClient, APIError

__all__ = [
    "server",
    "main",
    "set_auth_context",
    "get_auth_context",
    "clear_auth_context",
    "is_api_configured",
    "MCPConfig",
    "get_config",
    "TestHubClient",
    "APIError",
    "__version__",
]

