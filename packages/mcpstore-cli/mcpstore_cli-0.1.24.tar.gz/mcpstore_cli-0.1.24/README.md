# 🚀 mcpstore-cli

**English | [中文说明](#中文说明)**

---

## Overview

`mcpstore-cli` is a powerful Python CLI tool for managing and proxying Model Context Protocol (MCP) servers. It provides a unified registry, installation, configuration, and proxy solution for AI agent developers. Supports MCP servers from PyPI, NPM, GitHub, Docker, and more.

- 🔍 **Registry Search**: Discover MCP servers from multiple sources
- 📦 **One-Click Install**: Install and configure servers for various clients
- 🛠️ **Proxy Mode**: Run as a transparent MCP proxy
- 🌐 **Multi-Source**: Supports PyPI, NPM, GitHub, Docker
- 🎨 **Rich CLI**: Beautiful, interactive command line interface

---

## Quick Start

### Installation

```bash
pip install mcpstore-cli
```

Or use [uv](https://github.com/astral-sh/uv):

```bash
uv pip install mcpstore-cli
```

### Basic Usage

#### Search for MCP servers
```bash
# Search by keyword
mcpstore-cli search weather

# Filter by category
mcpstore-cli search --category productivity

# Filter by server type
mcpstore-cli search --type npm

# Limit results
mcpstore-cli search weather --limit 10
```

#### Show server info
```bash
mcpstore-cli info @turkyden/weather
```

#### Install server to client

**Install from registry:**
```bash
mcpstore-cli install @turkyden/weather --client cursor --key <your-api-key>
```

**Install HTTP URL server:**
```bash
# Install to Claude Desktop (generates stdio proxy config)
mcpstore-cli install "http://localhost:8090/mcp/abc123" "Gmail" --client claude

# Install to Cursor (generates direct URL config)
mcpstore-cli install "http://localhost:8090/mcp/abc123" "Gmail" --client cursor
```

**Install stdio server:**
```bash
# Install NPM package
mcpstore-cli install "sqlite-server" --command npx --args '["@anthropic/mcp-server-sqlite", "--db", "test.db"]' --client cursor

# Install PyPI package
mcpstore-cli install "my-server" --command uvx --args '["mcp-server-fetch"]' --client claude

# Install with environment variables
mcpstore-cli install "github-server" --command npx --args '["@modelcontextprotocol/server-github"]' --env '{"GITHUB_TOKEN":"your-token"}' --client cursor
```

#### List installed servers
```bash
# List all clients
mcpstore-cli list clients

# List servers for a specific client
mcpstore-cli list servers --client cursor
```

#### Run as MCP proxy
```bash
# Run registry server
mcpstore-cli run @turkyden/weather --key <your-api-key>

# Run HTTP URL server (stdio-to-HTTP proxy)
mcpstore-cli run --url "http://localhost:8090/mcp/abc123" "Gmail"
```

#### Uninstall server
```bash
mcpstore-cli uninstall server-name --client cursor
```

#### Configure client
```bash
# Show client configuration
mcpstore-cli configure-client cursor --show

# Set custom config path
mcpstore-cli configure-client my-client --path ~/.custom/config.json
```

#### Development tools
```bash
# Start development server with hot-reload
mcpstore-cli dev server.py --port 8181

# Build server for production
mcpstore-cli build server.py --transport shttp

# Open playground for testing
mcpstore-cli playground --port 3000
```

---

## Configuration

### Config File
Main configuration file: `~/.mcpstore/config.toml`

Example config:
```toml
[registry]
url = "https://registry.mcpstore.dev"
api_key = "your-api-key"

[proxy]
host = "127.0.0.1"
port = 8080

[clients.cursor]
type = "cursor"
config_path = "~/.cursor/mcp.json"
transport = "stdio"
config_format = "json"
server_key = "mcpServers"

[clients.claude]
type = "claude"
config_path = "~/Library/Application Support/Claude/claude_desktop_config.json"
transport = "stdio"
config_format = "json"
server_key = "mcpServers"
```

### Environment Variables
- `MCPSTORE_REGISTRY_URL` - Registry API URL
- `MCPSTORE_API_KEY` - API key for authentication
- `MCPSTORE_CONFIG_DIR` - Custom config directory path
- `MCPSTORE_CACHE_DIR` - Custom cache directory path

### Supported Clients
- **Cursor**: `~/.cursor/mcp.json`
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
- **VS Code**: Custom configuration
- **Custom**: Configure via `configure-client` command

---

## Architecture

### Core Components

- **Registry System**: Discovers and aggregates MCP servers from multiple sources (PyPI, NPM, GitHub, Docker)
- **Proxy Mode**: Transparent proxy between MCP client and server, supporting both stdio and HTTP transports
- **Server Manager**: Handles server installation, lifecycle management, and runtime execution
- **Configuration Manager**: Manages client configurations (Cursor, Claude Desktop, VS Code, etc.)
- **HTTP Proxy**: Stdio-to-HTTP proxy for Claude Desktop compatibility

### Server Types

- **NPM**: JavaScript/Node.js packages via `npx`
- **PyPI**: Python packages via `uvx`
- **GitHub**: Git repositories (cloned locally)
- **Docker**: Docker containers
- **HTTP URL**: Direct HTTP endpoint (with stdio proxy support)
- **Stdio**: Custom command-based servers

### Installation Flow

1. **Registry Server**: Search → Install → Configure → Run
2. **URL Server**: Install URL → Generate proxy config → Run proxy
3. **Stdio Server**: Install command → Configure → Run directly

---

## Advanced Features

### URL-based Server Installation
Install HTTP MCP servers directly by URL. For Claude Desktop, automatically generates stdio-to-HTTP proxy configuration.

### Stdio Server Installation
Install custom stdio servers with command and arguments. Supports environment variables and custom configuration.

### Development Tools
- **Dev Server**: Hot-reload development server with debugging
- **Playground**: Interactive testing environment
- **Builder**: Build servers for production deployment

## FAQ

**Q: How to publish my own MCP server?**
A: Publish to PyPI/NPM/GitHub/Docker, then register via the registry API. The server will be discoverable through `mcpstore-cli search`.

**Q: How to use with Cursor/Claude/VSCode?**
A: Use `install` command to automatically configure the client. The tool detects client type and generates appropriate configuration.

**Q: What's the difference between URL and stdio installation?**
A: URL installation is for HTTP-based MCP servers. Stdio installation is for command-based servers that communicate via standard input/output.

**Q: How does the proxy mode work?**
A: When you run `mcpstore-cli run <server-id>`, it starts the target server and proxies all MCP protocol communication transparently.

**Q: How to update?**
A: `pip install --upgrade mcpstore-cli` or `uv pip install --upgrade mcpstore-cli`

**Q: How to clear cache?**
A: Delete `~/.mcpstore/cache/` directory or use the internal cache clearing mechanism.

---

# 中文说明

## 简介

`mcpstore-cli` 是一款面向 AI 智能体开发者的 Python 命令行工具，支持 MCP 服务器的注册、发现、安装、配置和代理。支持 PyPI、NPM、GitHub、Docker 多源服务器。

- 🔍 **注册表搜索**：多源发现 MCP 服务器
- 📦 **一键安装**：自动安装配置到各类客户端
- 🛠️ **代理模式**：透明代理 MCP 通信
- 🌐 **多源支持**：PyPI/NPM/GitHub/Docker
- 🎨 **美观 CLI**：交互式命令行体验

---

## 快速开始

### 安装

```bash
pip install mcpstore-cli
```

或使用 uv：

```bash
uv pip install mcpstore-cli
```

### 基本用法

#### 搜索服务器
```bash
# 按关键词搜索
mcpstore-cli search weather

# 按分类筛选
mcpstore-cli search --category productivity

# 按服务器类型筛选
mcpstore-cli search --type npm

# 限制结果数量
mcpstore-cli search weather --limit 10
```

#### 查看服务器信息
```bash
mcpstore-cli info @turkyden/weather
```

#### 安装服务器到客户端

**从注册表安装:**
```bash
mcpstore-cli install @turkyden/weather --client cursor --key <你的API密钥>
```

**安装 HTTP URL 服务器:**
```bash
# 安装到 Claude Desktop（生成 stdio 代理配置）
mcpstore-cli install "http://localhost:8090/mcp/abc123" "Gmail" --client claude

# 安装到 Cursor（生成直接 URL 配置）
mcpstore-cli install "http://localhost:8090/mcp/abc123" "Gmail" --client cursor
```

**安装 stdio 服务器:**
```bash
# 安装 NPM 包
mcpstore-cli install "sqlite-server" --command npx --args '["@anthropic/mcp-server-sqlite", "--db", "test.db"]' --client cursor

# 安装 PyPI 包
mcpstore-cli install "my-server" --command uvx --args '["mcp-server-fetch"]' --client claude

# 安装带环境变量
mcpstore-cli install "github-server" --command npx --args '["@modelcontextprotocol/server-github"]' --env '{"GITHUB_TOKEN":"your-token"}' --client cursor
```

#### 列出已安装服务器
```bash
# 列出所有客户端
mcpstore-cli list clients

# 列出特定客户端的服务器
mcpstore-cli list servers --client cursor
```

#### 代理运行服务器
```bash
# 运行注册表服务器
mcpstore-cli run @turkyden/weather --key <你的API密钥>

# 运行 HTTP URL 服务器（stdio-to-HTTP 代理）
mcpstore-cli run --url "http://localhost:8090/mcp/abc123" "Gmail"
```

#### 卸载服务器
```bash
mcpstore-cli uninstall server-name --client cursor
```

#### 配置客户端
```bash
# 查看客户端配置
mcpstore-cli configure-client cursor --show

# 设置自定义配置路径
mcpstore-cli configure-client my-client --path ~/.custom/config.json
```

#### 开发工具
```bash
# 启动开发服务器（支持热重载）
mcpstore-cli dev server.py --port 8181

# 构建生产版本
mcpstore-cli build server.py --transport shttp

# 打开测试环境
mcpstore-cli playground --port 3000
```

---

## 配置

### 配置文件
主配置文件：`~/.mcpstore/config.toml`

配置示例：
```toml
[registry]
url = "https://registry.mcpstore.dev"
api_key = "your-api-key"

[proxy]
host = "127.0.0.1"
port = 8080

[clients.cursor]
type = "cursor"
config_path = "~/.cursor/mcp.json"
transport = "stdio"
config_format = "json"
server_key = "mcpServers"

[clients.claude]
type = "claude"
config_path = "~/Library/Application Support/Claude/claude_desktop_config.json"
transport = "stdio"
config_format = "json"
server_key = "mcpServers"
```

### 环境变量
- `MCPSTORE_REGISTRY_URL` - 注册表 API URL
- `MCPSTORE_API_KEY` - API 密钥
- `MCPSTORE_CONFIG_DIR` - 自定义配置目录路径
- `MCPSTORE_CACHE_DIR` - 自定义缓存目录路径

### 支持的客户端
- **Cursor**: `~/.cursor/mcp.json`
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) 或 `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
- **VS Code**: 自定义配置
- **自定义**: 通过 `configure-client` 命令配置

---

## 架构说明

### 核心组件

- **注册表系统**：从多个源（PyPI、NPM、GitHub、Docker）发现和聚合 MCP 服务器
- **代理模式**：在 MCP 客户端和服务器之间提供透明代理，支持 stdio 和 HTTP 传输
- **服务器管理器**：处理服务器安装、生命周期管理和运行时执行
- **配置管理器**：管理客户端配置（Cursor、Claude Desktop、VS Code 等）
- **HTTP 代理**：为 Claude Desktop 提供 stdio-to-HTTP 代理兼容性

### 服务器类型

- **NPM**: 通过 `npx` 安装的 JavaScript/Node.js 包
- **PyPI**: 通过 `uvx` 安装的 Python 包
- **GitHub**: Git 仓库（本地克隆）
- **Docker**: Docker 容器
- **HTTP URL**: 直接 HTTP 端点（支持 stdio 代理）
- **Stdio**: 基于自定义命令的服务器

### 安装流程

1. **注册表服务器**：搜索 → 安装 → 配置 → 运行
2. **URL 服务器**：安装 URL → 生成代理配置 → 运行代理
3. **Stdio 服务器**：安装命令 → 配置 → 直接运行

---

## 高级功能

### URL 服务器安装
直接通过 URL 安装 HTTP MCP 服务器。对于 Claude Desktop，自动生成 stdio-to-HTTP 代理配置。

### Stdio 服务器安装
使用命令和参数安装自定义 stdio 服务器。支持环境变量和自定义配置。

### 开发工具
- **开发服务器**：支持热重载的调试开发服务器
- **测试环境**：交互式测试环境
- **构建工具**：生产环境部署构建

## 常见问题

**Q: 如何发布自己的 MCP 服务器？**
A: 发布到 PyPI/NPM/GitHub/Docker 后，通过注册表 API 注册。服务器将通过 `mcpstore-cli search` 被发现。

**Q: 如何与 Cursor/Claude/VSCode 配合？**
A: 使用 `install` 命令自动配置客户端。工具会自动检测客户端类型并生成相应的配置。

**Q: URL 安装和 stdio 安装有什么区别？**
A: URL 安装适用于基于 HTTP 的 MCP 服务器。Stdio 安装适用于通过标准输入/输出通信的基于命令的服务器。

**Q: 代理模式是如何工作的？**
A: 当你运行 `mcpstore-cli run <server-id>` 时，它会启动目标服务器并透明地代理所有 MCP 协议通信。

**Q: 如何升级？**
A: `pip install --upgrade mcpstore-cli` 或 `uv pip install --upgrade mcpstore-cli`

**Q: 如何清除缓存？**
A: 删除 `~/.mcpstore/cache/` 目录或使用内部缓存清除机制。

---

## 贡献与支持

- GitHub: https://github.com/xray918/mcpstore-cli
- Issues: https://github.com/xray918/mcpstore-cli/issues

---

> mcpstore-cli © 2024 xray918. MIT License. 