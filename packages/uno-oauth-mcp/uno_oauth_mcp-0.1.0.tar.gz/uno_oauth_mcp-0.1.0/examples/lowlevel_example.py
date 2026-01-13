"""
底层 Server 示例 - 基于 mcp.server.lowlevel.Server

更灵活，完全控制 MCP 协议细节。
"""

import mcp.types as types
from uno_oauth_mcp import UnoOAuthServer


# 创建带 OAuth 的底层 Server
server = UnoOAuthServer(
    name="Lowlevel Example Server",
    port=8080,
)


@server.list_tools()
async def list_tools():
    """列出所有工具"""
    return [
        types.Tool(
            name="hello",
            description="向用户问好",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "用户名字"}
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="calculate",
            description="计算两个数的和",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """调用工具"""
    if name == "hello":
        user_name = arguments.get("name", "World")
        return [types.TextContent(type="text", text=f"Hello, {user_name}!")]
    
    elif name == "calculate":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        return [types.TextContent(type="text", text=f"{a} + {b} = {a + b}")]
    
    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


if __name__ == "__main__":
    print("Lowlevel Example - 基于底层 Server 的完整控制")
    server.run()
