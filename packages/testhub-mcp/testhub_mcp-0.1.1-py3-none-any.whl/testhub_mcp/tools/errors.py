"""
统一错误输出格式

该模块仅负责将错误信息格式化为易读的中文文本，供 MCP 工具返回给用户。
"""


def format_error(error_type: str, message: str, suggestion: str | None = None) -> str:
    """
    统一格式化错误信息。

    Args:
        error_type: 错误类型（如 ParamMissing / APIError / NotFound）
        message: 详细错误信息
        suggestion: 可选的建议/下一步

    Returns:
        str: 格式化后的错误文本
    """
    output = f"错误：{error_type}\n详情：{message}"
    if suggestion:
        output += f"\n建议：{suggestion}"
    return output




