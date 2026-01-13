"""
基于 FastMCP 的 OAuth 封装

为使用官方 FastMCP 的开发者提供 MCPMarket OAuth 支持。
"""

from typing import Optional, List, Any

from mcp.server.fastmcp import FastMCP

from .verifier import MCPMarketTokenVerifier
from .settings import mcpmarket_auth_settings


def UnoOAuthMCP(
    name: str,
    resource_server_url: Optional[str] = None,
    mcpmarket_url: str = "https://mcpmarket.cn",
    required_scopes: Optional[List[str]] = None,
    cache_ttl: int = 300,
    host: str = "0.0.0.0",
    port: int = 8000,
    **fastmcp_kwargs: Any,
) -> FastMCP:
    """
    创建带 MCPMarket 认证的 FastMCP 实例
    
    使用示例::
    
        from uno_oauth_mcp import UnoOAuthMCP
        
        mcp = UnoOAuthMCP(name="My Server")
        
        @mcp.tool()
        def hello(name: str) -> str:
            return f"Hello, {name}!"
        
        mcp.run(transport="streamable-http")
    
    Args:
        name: MCP Server 名称
        resource_server_url: 外部访问 URL（可选，自动生成）
        mcpmarket_url: MCPMarket 认证服务器地址
        required_scopes: 必需的 OAuth scopes
        cache_ttl: Token 缓存 TTL（秒）
        host: 监听地址
        port: 监听端口
        **fastmcp_kwargs: 传递给 FastMCP 的其他参数
        
    Returns:
        配置好认证的 FastMCP 实例
    """
    if resource_server_url is None:
        display_host = "localhost" if host in ("0.0.0.0", "::") else host
        resource_server_url = f"http://{display_host}:{port}"
    
    auth = mcpmarket_auth_settings(
        resource_server_url=resource_server_url,
        mcpmarket_url=mcpmarket_url,
        required_scopes=required_scopes,
    )
    
    verifier = MCPMarketTokenVerifier(
        mcpmarket_url=mcpmarket_url,
        cache_ttl=cache_ttl,
    )
    
    return FastMCP(
        name=name,
        auth=auth,
        token_verifier=verifier,
        host=host,
        port=port,
        **fastmcp_kwargs,
    )
