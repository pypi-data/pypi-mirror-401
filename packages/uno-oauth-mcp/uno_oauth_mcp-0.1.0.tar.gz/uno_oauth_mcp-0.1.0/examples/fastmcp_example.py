"""
FastMCP 示例 - 基于 FastMCP 的 MCP Server

推荐新手使用，API 更简洁。
"""

from uno_oauth_mcp import UnoOAuthMCP


# 创建带 OAuth 的 FastMCP 实例
mcp = UnoOAuthMCP(
    name="FastMCP Example Server",
    port=8080,
)


@mcp.tool()
def hello(name: str) -> str:
    """向用户问好"""
    return f"Hello, {name}!"


@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b


@mcp.resource("config://app")
def get_config() -> str:
    """获取应用配置"""
    return '{"version": "1.0.0", "auth": "MCPMarket OAuth"}'


if __name__ == "__main__":
    print("FastMCP Example - 基于 FastMCP 的简洁 API")
    mcp.run(transport="streamable-http")
