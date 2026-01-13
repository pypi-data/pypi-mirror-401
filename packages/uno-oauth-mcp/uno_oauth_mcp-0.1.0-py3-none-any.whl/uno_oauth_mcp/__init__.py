"""
Uno OAuth MCP

让 MCP Server 快速接入 mcpmarket.cn OAuth 认证。

支持两种开发方式：

## 方式一：基于 FastMCP（推荐新手）

    from uno_oauth_mcp import UnoOAuthMCP

    mcp = UnoOAuthMCP(name="My Server")

    @mcp.tool()
    def hello(name: str) -> str:
        return f"Hello, {name}!"

    mcp.run(transport="streamable-http")

## 方式二：基于底层 Server（更灵活）

    from uno_oauth_mcp import UnoOAuthServer
    import mcp.types as types

    server = UnoOAuthServer(name="My Server")

    @server.list_tools()
    async def list_tools():
        return [types.Tool(name="hello", ...)]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        return [types.TextContent(type="text", text="Hello!")]

    server.run()

详细文档: https://mcpmarket.cn/docs/uno-oauth-mcp
"""

from .verifier import MCPMarketTokenVerifier
from .settings import mcpmarket_auth_settings, MCPMarketAuthSettings
from .fastmcp import UnoOAuthMCP
from .lowlevel import create_oauth_starlette_app, UnoOAuthServer

__version__ = "0.1.0"
__all__ = [
    # FastMCP 方式
    "UnoOAuthMCP",
    "MCPMarketTokenVerifier",
    "mcpmarket_auth_settings",
    "MCPMarketAuthSettings",
    # 底层 Server 方式
    "UnoOAuthServer",
    "create_oauth_starlette_app",
]
