import asyncio
import json
import os
import logging
import sys
from typing import Optional
from contextlib import AsyncExitStack
from datetime import timedelta
from io import StringIO
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.auth import OAuthClientProvider

import httpx
from global_refer import _humanize_http_failure
from openai import OpenAI
from dotenv import load_dotenv
from global_refer import DEFAULT_TIMEOUT, SSE_READ_TIMEOUT
from mcp_auth import OAuth2Config, FileTokenStorage
from mcp.client.auth import TokenStorage

# 抑制 MCP SDK 的默认错误输出
logging.getLogger('mcp').setLevel(logging.CRITICAL)
logging.getLogger('mcp.client').setLevel(logging.CRITICAL)
logging.getLogger('mcp.client.auth').setLevel(logging.CRITICAL)

# 设置自定义的异常钩子来美化 OAuth 错误输出
_original_excepthook = sys.excepthook

def _custom_excepthook(exc_type, exc_value, exc_traceback):
    """自定义异常钩子，美化 OAuth 错误"""
    try:
        from mcp.client.auth import OAuthRegistrationError
        if exc_type == OAuthRegistrationError or (exc_value and "Registration failed" in str(exc_value) and "403" in str(exc_value)):
            # 不打印 traceback，已经有友好的错误处理
            return
    except:
        pass
    
    # 对于其他异常，使用原始的处理方式
    _original_excepthook(exc_type, exc_value, exc_traceback)

sys.excepthook = _custom_excepthook

load_dotenv() 



class MCPClient:
    def __init__(self, oauth_config: Optional[OAuth2Config] = None, token_storage: Optional[TokenStorage] = None, headers: Optional[dict] = None):
        """
        初始化MCP客户端
        
        Args:
            oauth_config: OAuth2配置（可选）
            token_storage: Token存储实现（可选，默认使用FileTokenStorage）
            headers: 自定义HTTP请求头（可选，如 {"XBY-APIKEY": "xxx"}）
        """
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._session_context = None
        self.openai = OpenAI()
        
        # 自定义 headers
        self.headers = headers
        
        # OAuth2配置
        self.oauth_config = oauth_config
        # 如果没有提供 token_storage，且有 oauth_config，则按 server_url 创建独立存储
        if token_storage is None and oauth_config:
            self.token_storage = FileTokenStorage(server_url=oauth_config.server_url)
            # 如果有预配置的 client_id/secret，预先保存到 storage
            asyncio.create_task(self._save_preconfigured_client())
        else:
            self.token_storage = token_storage or FileTokenStorage()
        self._auth_provider: Optional[OAuthClientProvider] = None
    
    async def _save_preconfigured_client(self):
        """
        如果环境变量中有预配置的 client_id/secret，保存到 storage
        这样 SDK 就会跳过动态注册，直接使用预配置的凭证
        """
        if not self.oauth_config:
            return
        
        import os
        from urllib.parse import urlparse
        from mcp.shared.auth import OAuthClientInformationFull
        from pydantic import AnyUrl
        
        # 提取域名
        parsed = urlparse(self.oauth_config.server_url)
        domain = parsed.netloc.replace(".", "_").replace(":", "_").upper()
        
        # 尝试获取预配置的 client_id
        client_id = os.getenv(f"MCP_OAUTH_CLIENT_ID_{domain}") or os.getenv("MCP_OAUTH_CLIENT_ID")
        client_secret = os.getenv(f"MCP_OAUTH_CLIENT_SECRET_{domain}") or os.getenv("MCP_OAUTH_CLIENT_SECRET")
        
        if client_id:
            # 创建 client_info 并保存
            client_info = OAuthClientInformationFull(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uris=[AnyUrl(uri) for uri in (self.oauth_config.redirect_uris or [])],
                token_endpoint_auth_method=self.oauth_config.token_endpoint_auth_method,
                grant_types=self.oauth_config.grant_types or ["authorization_code", "refresh_token"],
                response_types=["code"],
                client_name=self.oauth_config.client_name,
                scope=self.oauth_config.scope,
            )
            await self.token_storage.set_client_info(client_info)
            print(f"✅ 使用预配置的 Client ID: {client_id[:12]}...")

    def _find_httpx_status_error(self, exc: BaseException) -> Optional[httpx.HTTPStatusError]:
        """在嵌套异常组中查找第一个 httpx.HTTPStatusError"""
        try:
            if isinstance(exc, httpx.HTTPStatusError):
                return exc
            # Python 3.11+ ExceptionGroup/BaseExceptionGroup
            if isinstance(exc, ExceptionGroup) or isinstance(exc, BaseExceptionGroup):
                for sub in exc.exceptions:
                    found = self._find_httpx_status_error(sub)
                    if found is not None:
                        return found
        except Exception:
            pass
        return None
    
    def _find_oauth_registration_error(self, exc: BaseException) -> Optional[Exception]:
        """在嵌套异常组中查找 OAuthRegistrationError"""
        try:
            from mcp.client.auth import OAuthRegistrationError
            
            if isinstance(exc, OAuthRegistrationError):
                return exc
            
            # 检查异常消息中是否包含注册失败信息
            if "Registration failed" in str(exc) and "403" in str(exc):
                return exc
            
            # Python 3.11+ ExceptionGroup/BaseExceptionGroup
            if isinstance(exc, ExceptionGroup) or isinstance(exc, BaseExceptionGroup):
                for sub in exc.exceptions:
                    found = self._find_oauth_registration_error(sub)
                    if found is not None:
                        return found
        except Exception:
            pass
        return None
    
    def _print_oauth_registration_help(self, server_url: str):
        """打印 OAuth 动态注册失败时的帮助信息"""
        from urllib.parse import urlparse
        
        parsed = urlparse(server_url)
        domain = parsed.netloc.replace(".", "_").replace(":", "_").upper()
        
        print("\n" + "="*70)
        print("❌ OAuth 动态注册失败 (403 Forbidden)")
        print("="*70)
        print()
        print("此服务器不支持动态客户端注册，需要预先配置 OAuth 凭证。")
        print()
        print("📋 配置步骤：")
        print()
        print("1️⃣  在服务提供商的开发者平台注册 OAuth 应用")
        print(f"   服务器: {server_url}")
        print(f"   Redirect URI: http://localhost:28081/callback")
        print()
        print("2️⃣  设置环境变量（推荐使用 .env 文件）：")
        print()
        print(f"   export MCP_OAUTH_CLIENT_ID_{domain}=\"your-client-id\"")
        print(f"   export MCP_OAUTH_CLIENT_SECRET_{domain}=\"your-client-secret\"")
        print()
        print("3️⃣  重新连接：")
        print()
        print(f"   source .env  # 加载环境变量")
        print(f"   mcp-cli {server_url}")
        print()
        print("💡 提示：也可以创建 .env 文件避免每次手动设置：")
        print()
        print("   cat > .env << 'EOF'")
        print(f"   MCP_OAUTH_CLIENT_ID_{domain}=your-client-id")
        print(f"   MCP_OAUTH_CLIENT_SECRET_{domain}=your-client-secret")
        print("   EOF")
        print()
        print("   source .env")
        print(f"   mcp-cli {server_url}")
        print()
        print("="*70)
        print()

    def _create_auth_provider(self, server_url: str) -> Optional[httpx.Auth]:
        """创建OAuth认证提供者"""
        if not self.oauth_config:
            return None
        
        # 使用配置中的server_url或传入的server_url
        auth_server_url = self.oauth_config.server_url or server_url
        client_metadata = self.oauth_config.to_client_metadata()
        
        # 使用标准的OAuthClientProvider（SDK目前只支持Authorization Code Flow）
        # 注意：JWT Bearer Grant 目前SDK不支持，如果配置了JWT参数，这里会忽略
        self._auth_provider = OAuthClientProvider(
            server_url=auth_server_url,
            client_metadata=client_metadata,
            storage=self.token_storage,
            redirect_handler=self.oauth_config.redirect_handler,
            callback_handler=self.oauth_config.callback_handler,
            timeout=self.oauth_config.timeout,
        )
        
        return self._auth_provider

    async def connect_to_streamable_http_server(self, server_url: str):
        """Connect to an MCP server running with Streamable HTTP
        返回: True=连接并初始化成功；False=失败（已在此函数内输出人类可读错误）
        """
        try:
            from mcp.client.streamable_http import streamablehttp_client
            
            # 临时抑制 stderr 输出（捕获 SDK 的错误打印）
            old_stderr = sys.stderr
            sys.stderr = StringIO()
            
            try:
                # 创建认证提供者（如果配置了OAuth）
                auth_provider = self._create_auth_provider(server_url)
            
                self._streams_context = streamablehttp_client(
                    url=server_url,
                    headers=self.headers,  # 传入自定义headers
                    timeout=DEFAULT_TIMEOUT,  # HTTP操作超时（秒）
                    sse_read_timeout=SSE_READ_TIMEOUT,  # SSE读取超时（秒）
                    auth=auth_provider  # 传入OAuth认证
                )
                streams = await self._streams_context.__aenter__()

                read_stream, write_stream, get_session_id = streams
                self._session_context = ClientSession(
                    read_stream, 
                    write_stream,
                    read_timeout_seconds=timedelta(seconds=SSE_READ_TIMEOUT)  # 明确指定读取超时时间
                )
                self.session: ClientSession = await self._session_context.__aenter__()

                # Initialize
                await self.session.initialize()
            finally:
                # 恢复 stderr
                sys.stderr = old_stderr

            # List available tools to verify connection
            print("Initialized streamable http client...")
            # print("Listing tools...")
            # response = await self.session.list_tools()
            # tools = response.tools
            # print("\nConnected to server with tools:", [tool.name for tool in tools])
            
            return True

        except BaseException as e:
            # 如果连接失败，确保清理资源并在此处输出人类可读错误
            await self.cleanup()
            
            # 检查是否是 OAuth 动态注册失败（403）
            oauth_err = self._find_oauth_registration_error(e)
            if oauth_err is not None:
                self._print_oauth_registration_help(server_url)
                return False
            
            http_err = self._find_httpx_status_error(e)
            if http_err is not None and http_err.response is not None:
                status = http_err.response.status_code
                url = str(http_err.request.url) if http_err.request is not None else server_url
                if status == 401:
                    print(f"❌ HTTP 401 Unauthorized: 访问 {url} 需要有效凭证。请检查令牌/认证配置。")
                    return False
                print(f"❌ HTTP {status} Error during initialize: {url}")
                return False
            print(f"❌ 连接失败: {_humanize_http_failure(e, server_url)}")
            return False

    async def connect_to_sse_server(self, server_url: str):
        """Connect to an MCP server running with SSE transport
        返回: True=成功；False=失败（已在函数内输出错误）
        """
        try:
            # 临时抑制 stderr 输出（捕获 SDK 的错误打印）
            old_stderr = sys.stderr
            sys.stderr = StringIO()
            
            try:
                # 创建认证提供者（如果配置了OAuth）
                auth_provider = self._create_auth_provider(server_url)
                
                # Store the context managers so they stay alive
                self._streams_context = sse_client(
                    url=server_url,
                    headers=self.headers,  # 传入自定义headers
                    auth=auth_provider  # 传入OAuth认证
                )
                streams = await self._streams_context.__aenter__()

                self._session_context = ClientSession(*streams)
                self.session: ClientSession = await self._session_context.__aenter__()

                # Initialize
                await self.session.initialize()
            finally:
                # 恢复 stderr
                sys.stderr = old_stderr

            # List available tools to verify connection
            print("Initialized SSE client...")
            # print("Listing tools...")
            # response = await self.session.list_tools()
            # tools = response.tools
            # print("\nConnected to server with tools:", [tool.name for tool in tools])
            
            return True

        except BaseException as e:
            await self.cleanup()
            
            # 检查是否是 OAuth 动态注册失败（403）
            oauth_err = self._find_oauth_registration_error(e)
            if oauth_err is not None:
                self._print_oauth_registration_help(server_url)
                return False
            
            http_err = self._find_httpx_status_error(e)
            if http_err is not None and http_err.response is not None:
                status = http_err.response.status_code
                url = str(http_err.request.url) if http_err.request is not None else server_url
                if status == 401:
                    print(f"❌ HTTP 401 Unauthorized: 访问 {url} 需要有效凭证。请检查令牌/认证配置。")
                    return False
                print(f"❌ HTTP {status} Error during initialize: {url}")
                return False
            print(f"❌ 连接失败: {_humanize_http_failure(e, server_url)}")
            return False

    async def cleanup(self):
        """Properly clean up the session and streams"""
        try:
            if hasattr(self, '_session_context') and self._session_context:
                try:
                    await self._session_context.__aexit__(None, None, None)
                except BaseException:
                    pass
                finally:
                    self._session_context = None
                    
            if hasattr(self, '_streams_context') and self._streams_context:
                try:
                    await self._streams_context.__aexit__(None, None, None)
                except BaseException:
                    pass
                finally:
                    self._streams_context = None
                    
        except BaseException:
            pass



    def normalize_tool_name(self, tool_name: str) -> str:
        """将MCP工具名称转换为符合OpenAI规范的名称"""
        # 将点号替换为下划线，确保符合 ^[a-zA-Z0-9_-]+$ 模式
        return tool_name.replace('.', '_')
    
    def denormalize_tool_name(self, normalized_name: str, original_tools: list) -> str:
        """将规范化的工具名称转换回原始MCP工具名称"""
        for tool in original_tools:
            if self.normalize_tool_name(tool.name) == normalized_name:
                return tool.name
        return normalized_name  # 如果找不到映射，返回原名称

    async def get_tools(self):
        response = await self.session.list_tools()
        # 保存原始工具列表用于名称映射
        self.original_tools = response.tools
        
        available_tools = [{ 
            "type": "function",
            "function": {
                "name": self.normalize_tool_name(tool.name),  # 使用规范化的名称
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]
        tool_names = [tool["function"]["name"] for tool in available_tools]
        print(f"✅ tools list: {tool_names}")
        return available_tools
    

    def _estimate_token_count(self, messages: list) -> int:
        """
        粗略估算消息列表的token数量
        规则：每个字符约0.25 token（中文约1 token/字），JSON结构额外计算
        """
        total_chars = 0
        for msg in messages:
            # 计算content
            if msg.get("content"):
                content = msg["content"]
                # 中文字符按1 token/字，英文按0.25 token/字估算
                chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
                other_chars = len(content) - chinese_chars
                total_chars += chinese_chars * 4 + other_chars  # 统一转为字符数便于计算
            
            # 计算tool_calls
            if msg.get("tool_calls"):
                tool_calls_str = json.dumps(msg["tool_calls"])
                total_chars += len(tool_calls_str)
        
        # 转换为token估算（平均4字符≈1 token）
        estimated_tokens = total_chars // 4
        return estimated_tokens
    
    def _estimate_text_tokens(self, text: str) -> int:
        """
        估算单个文本的token数量
        
        Args:
            text: 要估算的文本
        
        Returns:
            估算的token数量
        """
        if not text:
            return 0
        
        # 中文字符按1 token/字，英文按0.25 token/字估算
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_chars = len(text) - chinese_chars
        total_chars = chinese_chars * 4 + other_chars
        
        return total_chars // 4
    
    def _truncate_text(self, text: str, max_tokens: int = 100000, tool_name: str = "") -> str:
        """
        截断过长的文本内容
        
        Args:
            text: 要截断的文本
            max_tokens: 最大token数量
            tool_name: 工具名称（用于日志）
        
        Returns:
            截断后的文本
        """
        estimated_tokens = self._estimate_text_tokens(text)
        
        if estimated_tokens <= max_tokens:
            return text
        
        # 需要截断
        print(f"⚠️  工具 {tool_name} 返回内容过大 (约 {estimated_tokens:,} tokens)，将截断至 {max_tokens:,} tokens")
        
        # 计算需要保留的字符数
        # 为了安全，我们按照最坏情况（全是中文）来计算
        max_chars = max_tokens
        
        # 截断文本，保留前半部分和尾部提示
        if len(text) > max_chars:
            truncate_point = max_chars - 200  # 留出空间给提示信息
            truncated = text[:truncate_point]
            
            # 添加截断提示
            suffix = f"\n\n... [内容过长已截断，原始长度: {len(text):,} 字符，约 {estimated_tokens:,} tokens，已截断至约 {max_tokens:,} tokens] ..."
            
            result = truncated + suffix
            actual_tokens = self._estimate_text_tokens(result)
            print(f"✂️  截断完成: {len(text):,} -> {len(result):,} 字符 (约 {estimated_tokens:,} -> {actual_tokens:,} tokens)")
            
            return result
        
        return text

    def _trim_message_history(self, messages: list, max_messages: int = 20, max_tokens: int = 100000) -> list:
        """
        修剪消息历史，保留system prompt（第0条）和最近的消息
        
        Args:
            messages: 消息列表
            max_messages: 最大消息数量（不包括system prompt）
            max_tokens: 最大token数量
        
        Returns:
            修剪后的消息列表
        """
        if len(messages) <= 1:  # 只有system prompt或更少
            return list(messages)  # 返回副本
        
        # 保留system prompt（第0条）
        system_prompt = messages[0] if messages and messages[0].get("role") == "system" else None
        conversation_messages = messages[1:] if system_prompt else messages
        
        # 检查是否需要修剪
        estimated_tokens = self._estimate_token_count(messages)
        
        # 添加调试日志（修剪前）
        if len(messages) > 1:  # 有对话历史时才打印
            print(f"💭 [修剪前] 对话历史: {len(conversation_messages)} 条消息, 约 {estimated_tokens:,} tokens")
        
        if len(conversation_messages) <= max_messages and estimated_tokens <= max_tokens:
            if len(messages) > 1:
                print(f"✅ 无需修剪")
            return list(messages)  # 返回副本，避免引用问题
        
        # 需要修剪：保留最近的消息
        if len(conversation_messages) > max_messages:
            # 保留最近的max_messages条
            trimmed_conversation = conversation_messages[-max_messages:]
            
            # 关键：确保消息结构完整，避免孤立的 tool 消息
            # OpenAI 要求：tool 消息必须跟在带有 tool_calls 的 assistant 消息后面
            
            # 从头部删除不完整的消息，直到找到第一个 user 消息
            while len(trimmed_conversation) > 2:
                first_role = trimmed_conversation[0].get("role")
                
                # 如果第一条是 tool 或 assistant (with tool_calls)，删除它
                # 因为它们可能是不完整的对话片段
                if first_role == "tool":
                    trimmed_conversation = trimmed_conversation[1:]
                elif first_role == "assistant" and trimmed_conversation[0].get("tool_calls"):
                    # assistant 有 tool_calls，但对应的 user 请求不在，删除整个不完整的工具调用链
                    trimmed_conversation = trimmed_conversation[1:]
                    # 继续删除后面的 tool 消息
                    while len(trimmed_conversation) > 0 and trimmed_conversation[0].get("role") == "tool":
                        trimmed_conversation = trimmed_conversation[1:]
                elif first_role == "user":
                    # 找到了完整对话的开始，停止删除
                    break
                else:
                    # 其他情况（如 assistant without tool_calls），保留
                    break
            
            print(f"📊 消息历史修剪: {len(conversation_messages)} -> {len(trimmed_conversation)} 条 (消息数量限制)")
        else:
            trimmed_conversation = conversation_messages
        
        # 如果还是超过token限制，继续减少
        while len(trimmed_conversation) > 2:  # 至少保留2条消息（一对问答）
            test_messages = [system_prompt] + trimmed_conversation if system_prompt else trimmed_conversation
            estimated_tokens = self._estimate_token_count(test_messages)
            
            if estimated_tokens <= max_tokens:
                break
            
            # 删除最老的一对消息（user+assistant+可能的tool）
            # 找到第一个user消息，删除它及其后续的assistant/tool消息
            removed_count = 0
            for i, msg in enumerate(trimmed_conversation):
                if msg.get("role") == "user":
                    # 删除这个user消息及其后续的assistant/tool消息
                    j = i + 1
                    while j < len(trimmed_conversation) and trimmed_conversation[j].get("role") in ["assistant", "tool"]:
                        j += 1
                    removed_count = j - i
                    trimmed_conversation = trimmed_conversation[j:]
                    break
            
            if removed_count == 0:
                # 安全保护：如果找不到user消息，强制删除最老的3条
                removed_count = min(3, len(trimmed_conversation))
                trimmed_conversation = trimmed_conversation[removed_count:]
            
            print(f"📊 Token超限，继续修剪: 删除 {removed_count} 条消息 (之前约 {estimated_tokens:,} tokens)")
        
        # 修剪后再次检查消息结构的完整性
        # 确保没有孤立的 tool 消息
        while len(trimmed_conversation) > 0:
            first_role = trimmed_conversation[0].get("role")
            if first_role == "tool":
                # 孤立的 tool 消息，删除
                trimmed_conversation = trimmed_conversation[1:]
            elif first_role == "assistant" and trimmed_conversation[0].get("tool_calls"):
                # assistant 有 tool_calls，检查后面是否有对应的 tool 消息
                # 如果没有，这是个不完整的序列，删除
                has_tool_response = (len(trimmed_conversation) > 1 and 
                                    trimmed_conversation[1].get("role") == "tool")
                if not has_tool_response:
                    # 没有对应的 tool 响应，删除这个 assistant 消息
                    trimmed_conversation = trimmed_conversation[1:]
                else:
                    break  # 结构完整，保留
            else:
                break  # 其他情况，保留
        
        # 重新组合
        result = [system_prompt] + trimmed_conversation if system_prompt else trimmed_conversation
        
        final_tokens = self._estimate_token_count(result)
        result_conversation_count = len([m for m in result if m.get("role") != "system"])
        print(f"✅ [修剪后] 对话历史: {result_conversation_count} 条消息, 约 {final_tokens:,} tokens")
        
        return result

    async def process_query(self, query: str, messages: list, available_tools: list) -> str:
        """Process a query using OpenAI and available tools"""
        # 在添加新消息前，先检查并修剪历史
        trimmed = self._trim_message_history(messages, max_messages=20, max_tokens=100000)
        messages.clear()
        messages.extend(trimmed)
        
        messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            max_tokens=3000,
            messages=messages,
            tools=available_tools
        )

        # 循环处理工具调用，直到 LLM 不再需要调用工具
        max_iterations = 10  # 防止无限循环
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            message = response.choices[0].message
            
            # 调试日志
            print(f"\n--- 第 {iteration} 轮 ---")
            if message.tool_calls:
                tool_names = [tc.function.name for tc in message.tool_calls]
                print(f"🔄 LLM 请求调用 {len(message.tool_calls)} 个工具: {tool_names}")
            else:
                content_preview = (message.content or "")[:50]
                print(f"💬 LLM 返回文本: {content_preview}...")
            
            # 如果没有工具调用，说明完成了
            if not message.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": message.content
                })
                # 只有在经过多轮工具调用后才需要再次修剪
                if iteration > 1:
                    messages[:] = self._trim_message_history(messages, max_messages=20, max_tokens=100000)
                return message.content or ""
            
            # 添加 assistant 消息（包含所有工具调用）
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })
            
            # 执行所有工具调用
            for tool_call in message.tool_calls:
                normalized_tool_name = tool_call.function.name
                original_tool_name = self.denormalize_tool_name(normalized_tool_name, self.original_tools)
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Tool {original_tool_name} called with args {tool_args}")
                result = await self.session.call_tool(original_tool_name, tool_args)
                print(f"✅ Tool {original_tool_name} result: {result}")
                
                # 提取工具结果文本
                result_text = ""
                if isinstance(result.content, list):
                    result_text = "\n".join(
                        item.text for item in result.content if hasattr(item, 'text')
                    )
                elif isinstance(result.content, str):
                    result_text = result.content
                else:
                    result_text = str(result.content)
                
                # 截断过长的工具返回内容（默认最大100k tokens）
                result_text = self._truncate_text(result_text, max_tokens=100000, tool_name=original_tool_name)
                
                messages.append({
                    "role": "tool", 
                    "tool_call_id": tool_call.id,
                    "content": result_text
                })
            
            # 在继续对话前，检查并修剪消息历史（避免在工具调用循环中累积过多）
            # 每3轮修剪一次，避免过于频繁
            if iteration % 3 == 0:
                messages[:] = self._trim_message_history(messages, max_messages=20, max_tokens=100000)
            
            # 继续对话（关键：传递 tools 参数，允许连续调用）
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                max_tokens=1000,
                messages=messages,
                tools=available_tools  # ← 这是关键！
            )
        
        # 达到最大迭代次数
        print(f"⚠️ 达到最大工具调用次数 ({max_iterations})")
        message = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": message.content
        })
        messages[:] = self._trim_message_history(messages, max_messages=20, max_tokens=100000)
        return message.content or ""
    

    async def chat_loop(self, available_tools):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        messages = [
            {
                "role": "system",
                "content": """你是一个 MCP 工具调用助手。

核心原则：
1. 工具优先 - 能用工具解决的问题，必须调用工具，不要自己编造答案
2. 连续执行 - 一个工具返回结果后，如果需要后续操作，立即调用下一个工具，不要停下来问用户
3. 遵循描述 - 每个工具的 description 中包含使用说明和工作流程，请严格遵循

行为规范：
- 禁止说"请稍等"、"我来帮你查询"之类的话，直接调用工具
- 禁止询问用户"是否继续"、"需要我帮你执行吗"，直接执行
- 只有工具调用失败或返回错误时，才告知用户问题
- 成功获取结果后，用简洁友好的语言回答"""
            }
        ]
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query, messages, available_tools)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")