"""
TestHub MCP Server 配置管理

通过环境变量配置 MCP Server 连接参数。
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class MCPConfig:
    """MCP Server 配置"""
    
    api_url: str
    api_token: str
    team_id: int
    session_id: Optional[int] = None
    
    @classmethod
    def from_env(cls) -> "MCPConfig":
        """从环境变量加载配置"""
        api_url = os.environ.get("TESTHUB_API_URL")
        api_token = os.environ.get("TESTHUB_API_TOKEN")
        team_id = os.environ.get("TESTHUB_TEAM_ID")
        session_id = os.environ.get("TESTHUB_SESSION_ID")
        
        # 验证必填参数
        if not api_url:
            raise ValueError("缺少环境变量: TESTHUB_API_URL")
        if not api_token:
            raise ValueError("缺少环境变量: TESTHUB_API_TOKEN")
        if not team_id:
            raise ValueError("缺少环境变量: TESTHUB_TEAM_ID")
        
        return cls(
            api_url=api_url.rstrip("/"),
            api_token=api_token,
            team_id=int(team_id),
            session_id=int(session_id) if session_id else None,
        )
    
    def validate(self) -> tuple[bool, str]:
        """验证配置是否有效"""
        if not self.api_url.startswith(("http://", "https://")):
            return False, "TESTHUB_API_URL 必须以 http:// 或 https:// 开头"
        
        if not self.api_token.startswith("th_"):
            return False, "TESTHUB_API_TOKEN 格式无效，应以 th_ 开头"
        
        if self.team_id <= 0:
            return False, "TESTHUB_TEAM_ID 必须是正整数"
        
        return True, ""


# 全局配置实例（懒加载）
_config: Optional[MCPConfig] = None


def get_config() -> MCPConfig:
    """获取配置实例（单例模式）"""
    global _config
    if _config is None:
        _config = MCPConfig.from_env()
    return _config


def reset_config():
    """重置配置（主要用于测试）"""
    global _config
    _config = None

