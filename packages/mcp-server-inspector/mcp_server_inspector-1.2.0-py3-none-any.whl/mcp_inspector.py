#!/usr/bin/env python3
"""
MCP Server Inspector - CLI工具
用于自动检测并连接MCP服务器（支持SSE和Streamable HTTP）
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from typing import Optional
import importlib.metadata

# 确保项目根目录在 Python 路径中
_project_root = Path(__file__).parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from client import MCPClient
from global_refer import (
    is_valid_url, detect_server_type, print_banner, 
    print_error, print_success
)
from mcp_auth import (
    OAuth2Config,
    FileTokenStorage,
    detect_auth_requirement,
    build_oauth_config_from_detection,
    build_oauth_config_from_args,
    auto_redirect_handler,
    auto_callback_handler_with_server,
    OAuthCallbackServer,
)
import shutil


async def clear_auth_cache() -> int:
    """
    清理所有缓存的认证信息
    
    Returns:
        0 表示成功，1 表示失败
    """
    auth_dir = Path(".mcp_auth")
    
    if not auth_dir.exists():
        print("✅ 没有找到认证缓存目录（.mcp_auth）")
        return 0
    
    try:
        print(f"🗑️  清理认证缓存目录: {auth_dir.absolute()}")
        
        # 列出所有缓存的服务器
        servers = [d for d in auth_dir.iterdir() if d.is_dir()]
        if servers:
            print(f"📦 发现 {len(servers)} 个服务器的认证缓存:")
            for server_dir in servers:
                print(f"   - {server_dir.name}")
        
        # 删除整个目录
        shutil.rmtree(auth_dir)
        print("✅ 认证缓存已清理")
        return 0
        
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        return 1


class MCPInspector:
    """MCP服务器检查器"""
    
    def __init__(self, headers: dict = None):
        """
        初始化检查器
        
        Args:
            headers: 自定义HTTP请求头（可选）
        """
        self.oauth_config = None
        self.headers = headers
        self.client = MCPClient(headers=headers)
        
    async def inspect_and_connect(self, url: str) -> bool:
        """检查URL并建立连接"""
        print_banner()
        
        # 1. 验证URL格式
        if not is_valid_url(url):
            print_error("invalid_url")
            return False
        
        # print(f"🔍 正在检测服务器: {url}")
        

        # 2.1 先检查是否已有该 server 的认证信息（优化：跳过检测）
        storage = FileTokenStorage(server_url=url)
        existing_tokens = await storage.get_tokens()
        existing_client_info = await storage.get_client_info()
        
        has_existing_auth = existing_tokens is not None or existing_client_info is not None
        
        if has_existing_auth:
            print(f"✅ 发现已有认证信息，跳过认证检测")
            # 直接使用已有的认证信息，创建基本的 OAuth 配置
            # 创建回调服务器（虽然可能不需要，但为了兼容性保留）
            callback_server = OAuthCallbackServer()
            callback_server.start()
            
            async def callback_handler():
                return await auto_callback_handler_with_server(callback_server)
            
            self.oauth_config = OAuth2Config(
                server_url=url,
                client_name="MCP Inspector",
                redirect_uris=[callback_server.get_redirect_uri()],
                redirect_handler=auto_redirect_handler,
                callback_handler=callback_handler,
            )
            self.client = MCPClient(oauth_config=self.oauth_config, headers=self.headers)
        else:
            # 2.2 没有认证信息，进行完整的检测流程
            print("🔍 检测认证需求...")
            auth_detection = await detect_auth_requirement(url)
            
            if auth_detection.requires_auth:
                # 使用检测到的元数据自动构建配置
                oauth_config = build_oauth_config_from_detection(
                    url, 
                    auth_detection,
                    interactive=True  # 允许交互式操作
                )
                if oauth_config:
                    self.oauth_config = oauth_config
                    self.client = MCPClient(oauth_config=oauth_config, headers=self.headers)
                    print("✅ 已自动配置 OAuth2 认证")
                else:
                    print("\n❌ 无法自动配置认证，请提供必要的认证信息")
                    return False
            elif auth_detection.error_message:
                print(f"⚠️  {auth_detection.error_message}")
        
        # 3. 检测服务器类型
        try:
            server_type = await detect_server_type(url, self.oauth_config, self.headers)
            
            if server_type is None:
                # print_error("not_mcp_server")
                return False
                
        except Exception as e:
            print_error("connection_failed", str(e))
            return False
        
        # 4. 根据检测结果建立连接
        # 在 client 内部已处理错误与清理，这里仅依据返回值判断
        if server_type == "sse":
            print_success("sse_detected")
            print("🔗 正在建立SSE连接...")
            ok = await self.client.connect_to_sse_server(url)
            if not ok:
                return False
        elif server_type == "http":
            print_success("http_detected")  
            print("🔗 正在建立Streamable HTTP连接...")
            ok = await self.client.connect_to_streamable_http_server(url)
            if not ok:
                return False

        print_success("connected")
        return True
    
    async def start_chat_loop(self):
        """开始聊天循环"""
        try:
            available_tools = await self.client.get_tools()
            print(f"\n📋 服务器提供了 {len(available_tools)} 个工具")
            
            # 打印工具名称和描述摘要（调试用）
            for tool in available_tools:
                name = tool["function"]["name"]
                desc = tool["function"].get("description") or "无描述"
                desc = desc[:80].replace("\n", " ")
                print(f"   - {name}: {desc}...")
            
            print("\n💬 开始聊天模式...")
            print("-" * 50)
            
            await self.client.chat_loop(available_tools)
            
        except Exception as e:
            print_error("unknown_error", str(e))
    
    async def cleanup(self):
        """清理资源"""
        try:
            await self.client.cleanup()
            print("\n👋 再见！")
        except Exception as e:
            print(f"清理资源时出错: {e}")


async def main():
    """主函数"""
    VERSION = importlib.metadata.version("mcp-server-inspector")
    parser = argparse.ArgumentParser(
        description="MCP Server Inspector - 自动检测并连接MCP服务器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  mcp_inspector http://localhost:8001/fetch/sse     # SSE类型服务器
  mcp_inspector http://localhost:8001/fetch/mcp     # HTTP类型服务器
  
支持的服务器类型:
  - SSE (Server-Sent Events)
  - Streamable HTTP
        """
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {VERSION}'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='清理所有缓存的认证信息（.mcp_auth目录）'
    )
    parser.add_argument(
        'url', 
        nargs='?',  # 使 url 参数变为可选
        help='MCP服务器的URL地址'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细输出'
    )
    parser.add_argument(
        '-H', '--header',
        action='append',
        metavar='KEY:VALUE',
        help='添加自定义HTTP请求头，格式为 KEY:VALUE，可多次使用（如 -H "XBY-APIKEY:xxx"）'
    )
    
    # 解析参数
    try:
        args = parser.parse_args()
        print(args)
    except SystemExit:
        return 1

    # 处理 --clear 参数
    if args.clear:
        return await clear_auth_cache()
    
    # 如果不是清理模式，URL 参数是必需的
    if not args.url:
        parser.error("需要提供 URL 参数（除非使用 --clear）")
        return 1

    # 解析自定义 headers
    headers = None
    if args.header:
        headers = {}
        for h in args.header:
            if ':' in h:
                key, value = h.split(':', 1)
                headers[key.strip()] = value.strip()
            else:
                print(f"⚠️ 忽略无效的 header 格式: {h}（正确格式: KEY:VALUE）")
        if headers:
            print(f"📋 使用自定义Headers: {list(headers.keys())}")

    # 创建检查器实例
    inspector = MCPInspector(headers=headers)
    
    try:
        # 检测并连接
        success = await inspector.inspect_and_connect(args.url)
        
        if not success:
            return 1
        
        # 开始聊天循环
        await inspector.start_chat_loop()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        return 0
        
    except Exception as e:
        print_error("unknown_error", str(e))
        return 1
        
    finally:
        await inspector.cleanup()


def cli_main():
    """CLI入口点（同步包装）"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ 程序被中断")



if __name__ == "__main__":
    import sys
    cli_main()
    sys.exit()