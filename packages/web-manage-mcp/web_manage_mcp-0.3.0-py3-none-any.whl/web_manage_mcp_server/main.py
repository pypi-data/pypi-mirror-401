import asyncio
import json
import os
from typing import Any, List
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Tool, TextContent

from web_manage_mcp_server.tools.java_tools import JavaTools
from web_manage_mcp_server.utils.config import config_manager

server = Server("web-manage-mcp")
java_tools = JavaTools()

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """列出可用工具"""
    return java_tools.get_tools()

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    return await java_tools.handle_tool_call(name, arguments)

async def run_server():
    """启动MCP服务器"""
    from mcp.server.stdio import stdio_server
    
    # 从环境变量或配置文件获取配置
    cookie_name = os.environ.get("MCP_COOKIE_AUTH_NAME") or config_manager.get("server.cookie_auth_name", "satoken")
    cookie_token = os.environ.get("MCP_COOKIE_AUTH_TOKEN") or config_manager.get("server.cookie_auth_token", "")
    
    config_manager.set("server.cookie_auth_name", cookie_name)
    config_manager.set("server.cookie_auth_token", cookie_token)
    
    print(f"MCP服务器启动 - Cookie: {cookie_name}, Token已配置: {'是' if cookie_token else '否'}")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="web-manage-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def main():
    asyncio.run(run_server())

if __name__ == "__main__":
    main()
