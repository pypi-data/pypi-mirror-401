# MCP Server Inspector

🔍 MCP服务器检查和连接工具 - 支持自动检测SSE和Streamable HTTP类型的MCP服务器并建立连接。

## 特性

- ✅ **自动检测**: 智能识别MCP服务器类型（SSE或Streamable HTTP）
- 🔗 **自动连接**: 根据检测结果自动选择合适的连接方式
- 💬 **交互式聊天**: 建立连接后进入AI聊天模式，可以调用服务器提供的工具
- 🔐 **自动认证检测**: 自动检测服务器是否需要OAuth2认证（符合MCP规范）
- 🔑 **完整OAuth2支持**: Authorization Code Flow、JWT Bearer Grant等多种认证方式
- ✨ **自动授权流程**: 自动打开浏览器、自动捕获授权码，无需手动输入
- 🎨 **友好界面**: 中文界面，丰富的emoji提示
- ⚡ **快速启动**: 一条命令即可连接和使用MCP服务器
- 🚀 **CLI工具**: 支持 `mcp-cli` 指令，可全局使用

## 安装

### 使用uv（推荐）

```bash
# 克隆项目
git clone https://github.com/xray918/mcp-server-inspector.git
cd mcp-server-inspector

# 使用uv安装依赖
uv sync

# 安装为CLI工具
uv pip install -e .
```

### 使用pip

```bash
pip install -e .
```

## 配置

### 1. 环境变量配置

在项目根目录创建 `.env` 文件，配置OpenAI API密钥：

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. OAuth2 认证配置（自动检测）

**✨ 新特性：工具会自动检测服务器是否需要认证！**

当连接到需要认证的服务器时，工具会：
1. 自动检测认证需求（通过 HTTP 401 响应）
2. 从 WWW-Authenticate header 或 well-known 端点获取认证信息
3. 提示你需要提供的认证配置
4. 支持从环境变量或命令行参数读取配置

**配置方式：**

```bash
# 方式1: 环境变量（推荐）
# JWT Bearer Grant（服务对服务）
export MCP_OAUTH_JWT_ISSUER=your-client-id
export MCP_OAUTH_JWT_SUBJECT=your-service-account
export MCP_OAUTH_JWT_KEY_FILE=/path/to/private-key.pem
export MCP_OAUTH_SCOPE=api.access

# 或 Authorization Code Flow（需要用户授权）
export MCP_OAUTH_REDIRECT_URIS=http://localhost:28081/callback
export MCP_OAUTH_SCOPE="read write"

# 方式2: 命令行参数
mcp-cli https://your-server.com/mcp \
  --oauth-jwt-issuer your-client-id \
  --oauth-jwt-subject your-service \
  --oauth-jwt-key-file /path/to/key.pem
```

**无需认证的服务器可以直接连接，无需任何配置。**

查看完整的 OAuth2 认证文档: [OAUTH2_AUTH.md](OAUTH2_AUTH.md)

### 3. 全局CLI配置（推荐）

安装完成后，配置全局使用 `mcp-cli` 指令：

```bash
# 将虚拟环境bin目录添加到PATH
echo 'export PATH="/root/xray918/mcp_server_inspector/.venv/bin:$PATH"' >> ~/.bashrc

# 重新加载配置
source ~/.bashrc

# 验证配置
which mcp-cli
mcp-cli --version
```

**注意**: 请将路径 `/root/xray918/mcp_server_inspector` 替换为你实际的项目路径。

## 使用方法

### 基本用法

#### 方式1：使用mcp-cli指令（推荐）

```bash
# 自动检测并连接MCP服务器
mcp-cli <服务器URL>

# 查看帮助信息
mcp-cli --help

# 查看版本信息
mcp-cli --version
```

#### 方式2：使用完整命令名

```bash
# 自动检测并连接MCP服务器
mcp_server_inspect <服务器URL>

# 或者使用
mcp-inspector <服务器URL>
```

#### 方式3：使用uv运行

```bash
# 在项目目录下运行
uv run mcp-cli <服务器URL>
```

### 示例

```bash
# 连接SSE类型的MCP服务器
mcp-cli http://localhost:8001/fetch/sse

# 连接Streamable HTTP类型的MCP服务器  
mcp-cli http://localhost:8001/fetch/mcp

# 显示详细输出
mcp-cli http://localhost:8001/fetch/sse -v

# 检查本地MCP网关服务器
mcp-cli http://localhost:3001/mcp
```

### 支持的服务器类型

- **SSE (Server-Sent Events)**: 通常路径包含 `/sse`, `/events`, `/stream`
- **Streamable HTTP**: 通常路径包含 `/mcp`, `/rpc`, `/api`

## 工作流程

1. **URL验证**: 检查输入的URL格式是否正确
2. **认证检测**: 自动检测服务器是否需要OAuth2认证
3. **服务器类型检测**: 智能识别服务器类型（SSE或Streamable HTTP）
4. **自动连接**: 根据检测结果选择合适的连接方式
5. **工具获取**: 获取服务器提供的所有工具列表
6. **聊天模式**: 进入交互式AI聊天，可以调用服务器工具

### 认证流程详解

当连接到需要认证的服务器时：

```
1. 尝试连接 → 收到 401 Unauthorized
2. 检查 WWW-Authenticate header
3. 获取 Protected Resource Metadata (RFC 9728)
4. 获取 OAuth Authorization Server Metadata (RFC 8414)
5. 确定认证方法（JWT Bearer / Authorization Code）
6. 检查环境变量或命令行参数
7. 如果配置完整 → 自动完成认证
8. 如果配置缺失 → 提示需要的配置
```

## 命令参数

### 基本参数

- `url`: MCP服务器的URL地址（必需参数）
- `-v, --verbose`: 显示详细输出（可选）
- `-h, --help`: 显示帮助信息
- `--version`: 显示版本信息

### OAuth2 认证参数（可选）

**注意：工具会自动检测认证需求，以下参数仅在需要认证时使用。**

- `--oauth-redirect-uri`: OAuth2重定向URI（用于Authorization Code Flow）
- `--oauth-jwt-issuer`: JWT签发者（用于JWT Bearer Grant）
- `--oauth-jwt-subject`: JWT主题（用于JWT Bearer Grant）
- `--oauth-jwt-key-file`: JWT签名私钥文件路径（PEM格式）
- `--oauth-scope`: OAuth2权限范围

**使用示例：**

```bash
# 示例1: 连接公开服务器（无需认证配置）
mcp-cli http://localhost:3000/

# 示例2: 连接需要JWT认证的服务器
# 工具会自动检测认证需求，然后使用提供的配置
mcp-cli https://your-server.com/mcp \
  --oauth-jwt-issuer your-client-id \
  --oauth-jwt-subject your-service \
  --oauth-jwt-key-file /path/to/key.pem

# 示例3: 使用环境变量（推荐）
# 设置环境变量后，工具会自动使用
export MCP_OAUTH_JWT_ISSUER=your-client-id
export MCP_OAUTH_JWT_KEY_FILE=/path/to/key.pem
mcp-cli https://your-server.com/mcp

# 示例4: 使用Authorization Code认证
mcp-cli https://your-server.com/mcp \
  --oauth-redirect-uri http://localhost:28081/callback
```

**自动检测示例：**

```bash
# 连接到需要认证的服务器
$ mcp-cli https://secure-server.com/mcp

🔍 检测认证需求...
🔐 检测到服务器需要 OAuth2 认证
   检测到认证方法: jwt_bearer
   支持的权限范围: api.read, api.write

💡 服务器需要 OAuth2 认证
请配置认证信息：

方法 1: 使用 JWT Bearer Grant（服务对服务）
  export MCP_OAUTH_JWT_ISSUER=your-client-id
  export MCP_OAUTH_JWT_SUBJECT=your-service-account
  export MCP_OAUTH_JWT_KEY_FILE=/path/to/private-key.pem

方法 2: 使用命令行参数
  --oauth-jwt-issuer your-client-id \
  --oauth-jwt-subject your-service \
  --oauth-jwt-key-file /path/to/key.pem
```

## 在聊天模式中

- 输入任何问题或请求，AI会智能选择合适的工具来处理
- 输入 `quit` 或 `exit` 退出程序
- 支持中文对话
- AI会友好地提示工具调用过程和结果

## 常见使用场景

### 1. 连接本地MCP服务器
```bash
# 连接本地端口8001的MCP服务器
mcp-cli http://localhost:8001/mcp
```

### 2. 连接远程MCP服务器
```bash
# 连接远程MCP服务器
mcp-cli https://your-mcp-server.com/mcp
```

### 3. 调试和测试
```bash
# 使用详细模式连接，查看更多调试信息
mcp-cli http://localhost:8001/mcp -v
```

## 项目结构

```
mcp_server_inspector/
├── mcp_inspector.py      # CLI主入口文件
├── client.py            # MCP客户端核心实现
├── global_refer.py      # 全局配置和工具函数
├── auth_config.py       # OAuth2配置管理
├── auth_storage.py      # Token存储实现
├── auth_detector.py     # 自动认证检测（新）
├── chat.py             # 聊天功能（备用实现）
├── mcp_sse_client.py   # SSE客户端示例
├── mcp_http_client.py  # HTTP客户端示例
├── examples/           # 示例代码
│   ├── oauth_jwt_bearer.py        # JWT Bearer认证示例
│   ├── oauth_authorization_code.py # Authorization Code示例
│   ├── oauth_with_llm.py          # OAuth + LLM完整示例
│   └── README.md                   # 示例说明
├── pyproject.toml      # 项目配置文件
├── OAUTH2_AUTH.md      # OAuth2认证详细文档
└── README.md           # 项目说明
```

## 开发

### 安装开发依赖

```bash
uv sync --dev
```

### 代码格式化

```bash
uv run black .
uv run isort .
```

### 运行测试

```bash
uv run pytest
```

### 类型检查

```bash
uv run mypy .
```

## 故障排除

### 1. mcp-cli指令找不到
```bash
# 检查是否已安装
uv pip list | grep mcp-server-inspector

# 重新安装
uv pip install -e .

# 检查PATH配置
echo $PATH | grep mcp-server-inspector
```

### 2. 权限问题
```bash
# 确保有执行权限
chmod +x .venv/bin/mcp-cli
```

### 3. 虚拟环境问题
```bash
# 重新创建虚拟环境
rm -rf .venv
uv sync
uv pip install -e .
```

## 技术栈

- **Python 3.10+**: 主要开发语言
- **MCP SDK**: Model Context Protocol客户端
- **OpenAI**: AI聊天功能
- **aiohttp**: HTTP客户端和SSE支持
- **asyncio**: 异步IO支持
- **argparse**: 命令行参数解析

## 许可证

MIT License

## 作者

xray918

## 贡献

欢迎提交Issues和Pull Requests！

## SDK 使用说明

本项目充分利用了 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 的内置功能：

- ✅ 使用 SDK 的 `OAuthClientProvider` 处理 OAuth2 认证流程
- ✅ 使用 SDK 的发现机制（RFC 9728, RFC 8414）
- ✅ 使用 SDK 的动态客户端注册（RFC 7591）
- ✅ 使用 SDK 的 Token 自动刷新机制

**我们的增强：**
- 🆕 自动检测服务器是否需要认证
- 🆕 根据检测结果自动构建配置
- 🆕 自动回调捕获（无需手动输入授权码）
- 🆕 用户友好的 CLI 和提示

详细说明请参阅：
- [SDK_USAGE.md](SDK_USAGE.md) - SDK 使用说明
- [AUTO_CALLBACK.md](AUTO_CALLBACK.md) - 自动回调捕获说明

## 相关链接

- [Model Context Protocol 官方文档](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Authorization 规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- [OAuth2 认证文档](OAUTH2_AUTH.md)
- [SDK 使用说明](SDK_USAGE.md)
- [自动回调捕获](AUTO_CALLBACK.md)
- [OAuth2 示例代码](examples/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [uv 包管理器](https://docs.astral.sh/uv/) 