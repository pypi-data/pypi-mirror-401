# Ai_Indeed_mcp_server 项目文档

[实在RPA](https://www.ai-indeed.com/)
## 项目概述

**Ai_Indeed_mcp_server** 是一个基于 FastMCP 框架的 MCP（Model Context Protocol）服务器，为 Z-Bot 机器人提供流程和任务管理功能。该服务器通过 MCP 协议与 AI 助手集成，允许 AI 通过标准化的工具调用来查询和执行机器人流程。

## 功能特性

- **流程查询**: 通过 `queryAppParam` 和 `queryAppList` 工具查询机器人流程信息
- **流程执行**: 通过 `runApp` 工具执行机器人流程
- **任务查询**: 通过 `queryTaskList` 工具查询机器人任务信息
- **任务管理**: 通过 `createTask`、`startTask` 工具创建任务和执行任务
- **日志记录**: 日志记录在 `%APPDATA%/Z-Factory/logs` 目录下

## 安装方式

### 使用 uvx (推荐)

```bash
uvx Ai_Indeed_mcp_server --bot-path "path/to/your/Z-Bot.exe"
```

**Python 环境初始化（Windows 示例）**

1. 安装 Python（建议安装官方 3.12+）

2. 创建并激活虚拟环境：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1    # PowerShell
# 或者使用 cmd:
.venv\Scripts\activate.bat
```

3. 更新打包工具并安装项目依赖：

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install Ai_Indeed_mcp_server
```
---

**安装 uv / uvx（如果尚未安装）**

```powershell
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
https://uv.oaix.tech/getting-started/installation/

注：`uv` 用于构建/打包站点，`uvx` 可用于在本地或服务器上启动/管理站点实例。

---
- 使用虚拟环境启动服务（示例）：
```cmd
py -m sz_mcp_server.sz_server --bot-path "C:\path\to\Z-Bot.exe"
```

---
- 使用 uvx 启动服务（示例）：

```powershell
uvx Ai_Indeed_mcp_server --bot-path "C:\path\to\Z-Bot.exe"
```

---
- 配置 uvx 启动项

```JSON
{
  "sz_mcp_server": {
    "command": "uvx",
    "args": [
      "Ai_Indeed_mcp_server",
      "--bot-path",
      "C:\\path\\to\\your\\Z-Bot.exe"
    ]
  }
}
```

---


