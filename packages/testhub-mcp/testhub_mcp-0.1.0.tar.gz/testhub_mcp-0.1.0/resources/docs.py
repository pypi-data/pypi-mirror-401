"""
文档资源提供者

负责解析文档 URI 并提供文档内容访问。

URI 格式：
- docs://project/overview     → 项目简介
- docs://project/tech-stack   → 技术栈说明
- docs://project/glossary     → 术语表
- docs://design/{module}      → 设计文档
- docs://api/{module}         → 接口文档
- docs://database/er          → ER 图
- docs://module/{name}        → 模块文档
- docs://template/{type}      → 文档模板
"""

from pathlib import Path
from typing import Optional


class DocsResourceProvider:
    """文档资源提供者"""

    def __init__(self, docs_root: str):
        self.docs_root = Path(docs_root)

        # URI 到文件路径的静态映射
        self.uri_mapping = {
            "project/overview": "00_项目总览/项目简介.md",
            "project/tech-stack": "00_项目总览/技术栈说明.md",
            "project/glossary": "00_项目总览/术语表.md",
            "database/er": "04_数据库文档/数据库ER设计.md",
        }

    def resolve_uri(self, uri: str) -> Optional[Path]:
        """
        解析 URI 到文件路径

        Args:
            uri: 文档资源 URI，如 "docs://design/campaign"

        Returns:
            Path: 文件路径，如果无法解析则返回 None
        """
        # 移除 docs:// 前缀
        path = uri.replace("docs://", "")

        # 直接映射
        if path in self.uri_mapping:
            return self.docs_root / self.uri_mapping[path]

        # 动态解析
        parts = path.split("/")

        if parts[0] == "design" and len(parts) == 2:
            module = parts[1]
            return self.docs_root / f"02_设计文档/详细设计/DDS-{module}.md"

        if parts[0] == "architecture" and len(parts) == 2:
            name = parts[1]
            return self.docs_root / f"02_设计文档/架构设计/{name}.md"

        if parts[0] == "api" and len(parts) == 2:
            module = parts[1]
            return self.docs_root / f"03_接口文档/{module}接口.md"

        if parts[0] == "module" and len(parts) == 2:
            name = parts[1]
            return self.docs_root / f"06_模块文档/{name}模块.md"

        if parts[0] == "guide" and len(parts) == 2:
            name = parts[1]
            return self.docs_root / f"05_开发指南/{name}.md"

        if parts[0] == "template" and len(parts) == 2:
            template_type = parts[1]
            return self.docs_root / f"_templates/{template_type}_template.md"

        if parts[0] == "database" and len(parts) == 2 and parts[1] == "tables":
            # 表结构文档需要进一步解析
            return None

        return None

    async def get_resource(self, uri: str) -> Optional[str]:
        """
        获取资源内容

        Args:
            uri: 文档资源 URI

        Returns:
            str: 文档内容，如果文件不存在则返回 None
        """
        file_path = self.resolve_uri(uri)
        if file_path and file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return None

    def list_resources(self) -> list[dict]:
        """
        列出所有可用资源

        Returns:
            list[dict]: 资源列表，每个资源包含 uri, name, description
        """
        resources = []

        # 静态资源
        for uri, path in self.uri_mapping.items():
            file_path = self.docs_root / path
            if file_path.exists():
                resources.append(
                    {
                        "uri": f"docs://{uri}",
                        "name": file_path.stem,
                        "description": f"文档: {path}",
                    }
                )

        # 动态扫描设计文档
        design_dir = self.docs_root / "02_设计文档/详细设计"
        if design_dir.exists():
            for f in design_dir.glob("DDS-*.md"):
                module = f.stem.replace("DDS-", "")
                resources.append(
                    {
                        "uri": f"docs://design/{module}",
                        "name": f"设计文档: {module}",
                        "description": f"模块 {module} 的详细设计文档",
                    }
                )

        # 动态扫描架构设计
        arch_dir = self.docs_root / "02_设计文档/架构设计"
        if arch_dir.exists():
            for f in arch_dir.glob("*.md"):
                name = f.stem
                resources.append(
                    {
                        "uri": f"docs://architecture/{name}",
                        "name": f"架构设计: {name}",
                        "description": f"{name} 架构设计文档",
                    }
                )

        # 动态扫描接口文档
        api_dir = self.docs_root / "03_接口文档"
        if api_dir.exists():
            for f in api_dir.glob("*接口.md"):
                module = f.stem.replace("接口", "")
                resources.append(
                    {
                        "uri": f"docs://api/{module}",
                        "name": f"接口文档: {module}",
                        "description": f"{module}模块的 API 接口文档",
                    }
                )

        # 动态扫描模块文档
        module_dir = self.docs_root / "06_模块文档"
        if module_dir.exists():
            for f in module_dir.glob("*模块.md"):
                name = f.stem.replace("模块", "")
                resources.append(
                    {
                        "uri": f"docs://module/{name}",
                        "name": f"模块文档: {name}",
                        "description": f"{name}模块的实现说明",
                    }
                )

        # 动态扫描开发指南
        guide_dir = self.docs_root / "05_开发指南"
        if guide_dir.exists():
            for f in guide_dir.glob("*.md"):
                name = f.stem
                resources.append(
                    {
                        "uri": f"docs://guide/{name}",
                        "name": f"开发指南: {name}",
                        "description": f"{name} 开发指南",
                    }
                )

        # 动态扫描文档模板
        template_dir = self.docs_root / "_templates"
        if template_dir.exists():
            for f in template_dir.glob("*_template.md"):
                template_type = f.stem.replace("_template", "")
                resources.append(
                    {
                        "uri": f"docs://template/{template_type}",
                        "name": f"模板: {template_type}",
                        "description": f"{template_type} 文档模板",
                    }
                )

        return resources

