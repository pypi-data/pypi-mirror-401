# TestHub MCP Server

TestHub MCP Server 是一个 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 服务器，用于在 Cursor IDE 中集成 TestHub 开发管理系统。通过 MCP 协议，AI 助手可以直接与 TestHub 交互，实现任务管理、评审文档生成、会话同步等功能。

## 功能特性

- 📋 **任务管理**：获取任务详情、更新状态、查看待办列表
- 📝 **评审文档**：自动生成设计文档、代码评审文档
- 💾 **会话同步**：记录开发会话、关键决策、修改文件
- 🐛 **Bug 管理**：快速创建 Bug 报告
- 📚 **文档访问**：访问项目文档资源

## 快速开始

### 前置要求

- Python >= 3.10
- Cursor IDE
- TestHub 后端服务运行中

### 安装方式

#### 方式一：使用 uvx（推荐）

无需单独安装，直接在 Cursor 配置中使用：

```json
{
  "mcpServers": {
    "testhub": {
      "command": "uvx",
      "args": ["--from", "path/to/testhub_mcp", "testhub-mcp"],
      "env": {
        "TESTHUB_API_URL": "https://testhub.yourcompany.com/api/v1",
        "TESTHUB_API_TOKEN": "your-personal-api-token",
        "TESTHUB_TEAM_ID": "2",
        "TESTHUB_SESSION_ID": "15"
      }
    }
  }
}
```

#### 方式二：使用 pip 安装

```bash
# 进入 testhub_mcp 目录
cd testhub_mcp

# 安装到当前环境
pip install -e .

# 或使用 uv
uv pip install -e .
```

### 配置 Cursor

1. 创建或编辑 Cursor MCP 配置文件：

   **全局配置**（适用于所有项目）：
   ```
   ~/.cursor/mcp.json
   ```

   **项目配置**（仅适用于当前项目）：
   ```
   项目根目录/.cursor/mcp.json
   ```

2. 添加以下配置：

```json
{
  "mcpServers": {
    "testhub": {
      "command": "testhub-mcp",
      "env": {
        "TESTHUB_API_URL": "https://testhub.yourcompany.com/api/v1",
        "TESTHUB_API_TOKEN": "your-personal-api-token",
        "TESTHUB_TEAM_ID": "2",
        "TESTHUB_SESSION_ID": "15"
      }
    }
  }
}
```

### 配置 Cursor Rules

将 `cursor_rules/testhub-integration.mdc` 文件复制到项目的 `.cursor/rules/` 目录：

```bash
mkdir -p .cursor/rules
cp cursor_rules/testhub-integration.mdc .cursor/rules/
```

或者手动创建符号链接（推荐，便于更新）：

```bash
mkdir -p .cursor/rules
ln -s ../../cursor_rules/testhub-integration.mdc .cursor/rules/testhub-integration.mdc
```

### 环境变量

| 变量名 | 必填 | 说明 | 示例 |
|-------|------|------|------|
| `TESTHUB_API_URL` | ✅ | TestHub API 地址 | `https://testhub.yourcompany.com/api/v1` |
| `TESTHUB_API_TOKEN` | ✅ | 个人 API Token | `th_xxx_xxxxx` |
| `TESTHUB_TEAM_ID` | ✅ | 团队 ID | `2` |
| `TESTHUB_SESSION_ID` | ⚠️ 推荐 | 默认开发会话 ID，创建任务时自动关联 | `15` |
| `PROJECT_DOCS_PATH` | ⬜ | 项目文档路径 | `./docs` |

> **💡 提示**：`TESTHUB_SESSION_ID` 虽然不是必填，但强烈建议配置。它确保所有通过 MCP 创建的任务、会话等数据都能关联到正确的开发迭代。你可以在 TestHub 前端的"开发管理"中找到活跃会话的 ID。

## 使用说明

### 基本工作流

1. **开始任务**
   
   在 Cursor 中说：
   ```
   开始任务 TASK-042
   ```
   
   AI 助手会：
   - 调用 `testhub_get_task` 获取任务详情
   - 显示任务标题、描述、验收标准
   - 更新任务状态为"进行中"

2. **开发完成后提交评审**
   
   在 Cursor 中说：
   ```
   功能完成了，帮我提交评审
   ```
   
   AI 助手会：
   - 分析修改的代码
   - 自动生成评审文档（数据模型设计、API 设计、代码评审等）
   - 上传文档到 TestHub
   - 提交评审

3. **结束会话**
   
   在 Cursor 中说：
   ```
   今天先到这，同步一下
   ```
   
   AI 助手会：
   - 整理本次会话的工作摘要
   - 记录修改的文件、关键决策
   - 同步到 TestHub

### 可用命令

| 触发语句 | 功能 |
|---------|------|
| "开始任务 TASK-XXX" | 获取任务详情并开始任务 |
| "我的任务" | 查看待办任务列表 |
| "功能完成了" | 生成评审文档并提交 |
| "同步一下" | 同步当前会话记录 |
| "这里有个 bug" | 创建 Bug 报告 |

## 可用工具

### 任务管理

| 工具 | 说明 | 参数 |
|-----|------|------|
| `testhub_get_task` | 获取任务详情 | `task_code` (必填) |
| `testhub_update_task_status` | 更新任务状态 | `task_code`, `status` |
| `testhub_list_my_tasks` | 获取我的待办任务 | `status`, `limit` |
| `testhub_create_task` | 创建新任务 | `title`, `description`, `complexity` |
| `testhub_start_task` | 开始任务 | `task_code` |
| `testhub_complete_task` | 完成任务 | `task_code` |

### 评审管理

| 工具 | 说明 | 参数 |
|-----|------|------|
| `testhub_create_review` | 创建功能评审 | `task_code` |
| `testhub_add_review_document` | 添加评审文档 | `task_code`, `doc_type`, `title`, `content` |
| `testhub_submit_review` | 提交评审 | `task_code` |

### 会话管理

| 工具 | 说明 | 参数 |
|-----|------|------|
| `testhub_sync_dev_session` | 同步开发会话 | `session_summary`, `files_changed`, `key_decisions` |
| `testhub_list_sessions` | 列出开发会话 | `limit` |
| `testhub_switch_session` | 切换开发会话 | `session_id` |

### Bug 管理

| 工具 | 说明 | 参数 |
|-----|------|------|
| `testhub_create_bug` | 创建 Bug | `title`, `description`, `severity`, `related_task_code` |

### 上下文管理

| 工具 | 说明 | 参数 |
|-----|------|------|
| `testhub_get_context` | 获取当前上下文 | - |
| `testhub_switch_task` | 切换当前任务 | `task_code` |

## 开发

### 本地开发

```bash
# 克隆仓库
git clone <repo-url>
cd TestHub/testhub_mcp

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

### 测试 MCP Server

使用 MCP Inspector 进行测试：

```bash
# 安装 MCP Inspector
npm install -g @modelcontextprotocol/inspector

# 启动测试
npx @modelcontextprotocol/inspector testhub-mcp
```

## 目录结构

```
testhub_mcp/
├── __init__.py          # 包初始化
├── server.py            # MCP Server 主入口
├── config.py            # 配置管理
├── api_client.py        # TestHub API 客户端
├── tools/               # MCP 工具实现
│   ├── __init__.py
│   ├── task.py          # 任务管理工具
│   ├── review.py        # 评审管理工具
│   ├── session.py       # 会话同步工具
│   ├── bug.py           # Bug 管理工具
│   └── docs.py          # 文档工具
├── resources/           # MCP 资源提供者
│   ├── __init__.py
│   └── docs.py          # 文档资源
├── pyproject.toml       # 项目配置
└── README.md            # 本文件
```

## 故障排除

### MCP Server 无法启动

1. 检查 Python 版本 >= 3.10
2. 确认环境变量已正确配置
3. 查看 Cursor 日志：`Help > Toggle Developer Tools > Console`

### 无法连接 TestHub

1. 检查 `TESTHUB_API_URL` 是否正确
2. 确认 API Token 有效
3. 确认网络可访问 TestHub 服务

### 工具调用失败

1. 检查必填参数是否提供
2. 查看错误信息中的详细说明
3. 确认对应的后端 API 已实现

## 许可证

MIT

## 相关链接

- [Model Context Protocol 官方文档](https://modelcontextprotocol.io/)
- [Cursor MCP 配置指南](https://docs.cursor.com/mcp)
- [TestHub 项目主页](../README.md)

