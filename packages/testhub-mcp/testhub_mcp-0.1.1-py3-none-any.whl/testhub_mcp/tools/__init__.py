"""
MCP Tools 模块

提供各种开发辅助工具。

工具分类：
- 核心工具 (7): testhub_start, testhub_finish, testhub_log, testhub_status,
                testhub_pause, testhub_block, testhub_resume
- 统一工具 (4): testhub_docs, testhub_bug, testhub_search, testhub_test
- 辅助工具 (6): testhub_get_task, testhub_task_overview, testhub_list_my_tasks,
                testhub_daily_summary, testhub_create_task, testhub_suggest_task
"""

# 核心工具
from .core import (
    get_all_core_tools,
    handle_core_tool,
    CORE_TOOL_HANDLERS,
)

# 统一工具
from .unified_docs import (
    get_unified_docs_tool,
    handle_unified_docs,
)

from .unified_bug import (
    get_unified_bug_tool,
    handle_unified_bug,
)

from .unified_search import (
    get_unified_search_tool,
    handle_unified_search,
)

from .unified_test import (
    get_unified_test_tool,
    handle_unified_test,
)

# 辅助工具 - 任务相关
from .task import (
    get_task_tool,
    task_overview_tool,
    list_my_tasks_tool,
    handle_get_task,
    handle_task_overview,
    handle_list_my_tasks,
)

# 辅助工具 - 建议相关
from .suggest import (
    suggest_task_tool,
    create_task_tool,
    daily_summary_tool,
    handle_suggest_task,
    handle_create_task,
    handle_daily_summary,
)

__all__ = [
    # 核心工具
    "get_all_core_tools",
    "handle_core_tool",
    "CORE_TOOL_HANDLERS",
    # 统一工具
    "get_unified_docs_tool",
    "handle_unified_docs",
    "get_unified_bug_tool",
    "handle_unified_bug",
    "get_unified_search_tool",
    "handle_unified_search",
    "get_unified_test_tool",
    "handle_unified_test",
    # 辅助工具 - 任务
    "get_task_tool",
    "task_overview_tool",
    "list_my_tasks_tool",
    "handle_get_task",
    "handle_task_overview",
    "handle_list_my_tasks",
    # 辅助工具 - 建议
    "suggest_task_tool",
    "create_task_tool",
    "daily_summary_tool",
    "handle_suggest_task",
    "handle_create_task",
    "handle_daily_summary",
]
