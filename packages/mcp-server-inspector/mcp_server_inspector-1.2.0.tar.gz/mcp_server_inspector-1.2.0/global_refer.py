"""
全局变量和函数配置文件
用于存放项目中共用的变量和函数，避免重复实现
"""

import os
from typing import Optional, Union
from urllib.parse import urlparse
import aiohttp
import asyncio

# 全局配置
DEFAULT_TIMEOUT = 30.0
SSE_READ_TIMEOUT = 300.0
HTTP_TIMEOUT = 15.0  # 增加HTTP检测超时时间

# MCP 路径识别
MCP_SSE_PATHS = ["/sse", "/events", "/stream"]
MCP_HTTP_PATHS = ["/mcp", "/rpc", "/api"]

# 用户消息
WELCOME_MESSAGE = """
🔍 MCP Server Inspector，输入 'quit' 或 'exit' 退出程序"""

ERROR_MESSAGES = {
    "invalid_url": "❌ 无效的URL格式",
    "connection_failed": "❌ 连接失败，请检查服务器是否可用",
    "not_mcp_server": "❌ 这不是一个有效的MCP服务器",
    "timeout": "❌ 连接超时",
    "unknown_error": "❌ 未知错误"
}

SUCCESS_MESSAGES = {
    "sse_detected": "✅ 检测到SSE类型的MCP服务器",
    "http_detected": "✅ 检测到Streamable HTTP类型的MCP服务器",
    "connected": "✅ 已成功连接到服务器"
}


def _find_httpx_status_error(exc: BaseException):
    """在异常组中查找 httpx.HTTPStatusError，未找到则返回 None"""
    try:
        import httpx
        if isinstance(exc, httpx.HTTPStatusError):
            return exc
        # Python 3.11+ ExceptionGroup / BaseExceptionGroup
        if isinstance(exc, ExceptionGroup) or isinstance(exc, BaseExceptionGroup):
            for sub in exc.exceptions:
                found = _find_httpx_status_error(sub)
                if found is not None:
                    return found
    except Exception:
        pass
    return None

def _humanize_http_failure(exc: BaseException, url: str) -> str:
    """将连接失败异常转为更清晰的人类可读文案，并尽量给出HTTP状态码"""
    import httpx
    http_err = _find_httpx_status_error(exc)
    if http_err is not None and getattr(http_err, "response", None) is not None:
        status = http_err.response.status_code
        request_url = str(http_err.request.url) if getattr(http_err, "request", None) else url
        if status == 401:
            return f"HTTP 401 Unauthorized: 访问 {request_url} 需要有效凭证。请检查令牌/认证配置。"
        return f"HTTP {status} Error: {request_url}"
    # 未发现具体状态，若为取消类报错，尝试轻量请求探测状态
    msg = str(exc) or exc.__class__.__name__
    if "Cancelled by cancel scope" in msg or "cancel scope" in msg.lower():
        try:
            with httpx.Client(timeout=HTTP_TIMEOUT) as client:
                resp = client.get(url)
                if resp.status_code == 401:
                    return f"HTTP 401 Unauthorized: 访问 {url} 需要有效凭证。请检查令牌/认证配置。"
                if resp.status_code >= 400:
                    return f"HTTP {resp.status_code} Error: {url}"
        except Exception:
            # 探测失败则回退原始信息
            pass
        return f"连接被取消（可能由服务器拒绝或认证失败）: {msg}"
    return msg

def is_valid_url(url: str) -> bool:
    """检查URL格式是否有效"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


async def check_server_available(url: str, headers: dict = None) -> bool:
    """检查服务器是否可用（简单的HTTP检查）"""
    import aiohttp
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=HTTP_TIMEOUT)) as session:
            async with session.get(url, headers=headers) as response:
                # 接受2xx, 3xx, 4xx状态码（除了404）
                return response.status < 500 and response.status != 404
    except Exception:
        return False


async def detect_server_type(url: str, oauth_config=None, headers: dict = None) -> Optional[str]:
    """
    检测服务器类型，通过直接尝试连接来判断
    
    Args:
        url: 服务器URL
        oauth_config: OAuth2配置（可选）
        headers: 自定义HTTP请求头（可选）
    
    返回: 'sse' | 'http' | None
    """
    if not is_valid_url(url):
        return None
    
    # 首先进行简单的HTTP检查（带上自定义headers）
    if not await check_server_available(url, headers):
        print("❌ 服务器不可用或返回错误状态")
        return None
    
    # 导入MCPClient来进行实际连接测试
    from client import MCPClient
    
    # 基于路径的优先级判断
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()
    
    # 如果路径包含明确的SSE标识，优先测试SSE
    if any(sse_path in path for sse_path in MCP_SSE_PATHS):
        print("🎯 路径包含SSE标识，优先测试SSE连接")
        if await test_sse_connection(url, oauth_config, headers):
            return "sse"
        if await test_http_connection(url, oauth_config, headers):
            return "http"
    # 如果路径包含HTTP标识，优先测试HTTP
    elif any(http_path in path for http_path in MCP_HTTP_PATHS):
        # print("🎯 路径包含HTTP标识，优先测试HTTP连接")
        if await test_http_connection(url, oauth_config, headers):
            return "http"
        if await test_sse_connection(url, oauth_config, headers):
            return "sse"
    else:
        # 没有明确标识，都尝试（优先HTTP，因为更常见）
        print("🔄 路径无明确标识，按优先级测试连接")
        if await test_http_connection(url, oauth_config, headers):
            return "http"
        if await test_sse_connection(url, oauth_config, headers):
            return "sse"
    
    return None


async def test_sse_connection(url: str, oauth_config=None, headers: dict = None) -> bool:
    """
    测试SSE连接是否可用
    
    Args:
        url: 服务器URL
        oauth_config: OAuth2配置（可选）
        headers: 自定义HTTP请求头（可选）
    """
    from client import MCPClient
    import httpx
    
    print(f"🔍 测试SSE连接: {url}")
    if oauth_config:
        print("🔐 使用OAuth2认证")
    if headers:
        print(f"📋 使用自定义Headers: {list(headers.keys())}")
    
    client = MCPClient(oauth_config=oauth_config, headers=headers)
    
    ok = await client.connect_to_sse_server(url)
    if ok:
        print("✅ SSE连接成功")
        await client.cleanup()
        return True
    await client.cleanup()
    return False


async def test_http_connection(url: str, oauth_config=None, headers: dict = None) -> bool:
    """
    测试Streamable HTTP连接是否可用
    
    Args:
        url: 服务器URL
        oauth_config: OAuth2配置（可选）
        headers: 自定义HTTP请求头（可选）
    """
    from client import MCPClient
    import httpx
    
    print(f"🔍 测试HTTP连接: {url}")
    if oauth_config:
        print("🔐 使用OAuth2认证")
    if headers:
        print(f"📋 使用自定义Headers: {list(headers.keys())}")
    
    client = MCPClient(oauth_config=oauth_config, headers=headers)
    
    ok = await client.connect_to_streamable_http_server(url)
    if ok:
        print("✅ HTTP连接成功")
        await client.cleanup()
        return True
    await client.cleanup()
    return False


# 移除原来复杂的验证函数，保留简单的URL验证
async def verify_sse_server(url: str, oauth_config=None) -> bool:
    """已弃用，使用test_sse_connection代替"""
    return await test_sse_connection(url, oauth_config)


async def verify_http_server(url: str, oauth_config=None) -> bool:
    """已弃用，使用test_http_connection代替"""
    return await test_http_connection(url, oauth_config)


def print_banner():
    """打印程序横幅"""
    print(WELCOME_MESSAGE)


def print_error(error_type: str, details: str = ""):
    """打印错误信息"""
    message = ERROR_MESSAGES.get(error_type, ERROR_MESSAGES["unknown_error"])
    if details:
        message += f": {details}"
    print(message)


def print_success(success_type: str, details: str = ""):
    """打印成功信息"""
    message = SUCCESS_MESSAGES.get(success_type, "✅ 操作成功")
    if details:
        message += f": {details}"
    print(message) 