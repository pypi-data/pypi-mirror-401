"""
基于底层 Server 的 OAuth 封装

为使用官方底层 mcp.server.lowlevel.Server 类的开发者提供 MCPMarket OAuth 支持。
"""

from typing import Optional, List

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp.server.lowlevel import Server
from mcp.server.auth.middleware.auth_context import AuthContextMiddleware
from mcp.server.auth.middleware.bearer_auth import BearerAuthBackend, RequireAuthMiddleware
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from .verifier import MCPMarketTokenVerifier
from .settings import mcpmarket_auth_settings


def create_oauth_starlette_app(
    server: Server,
    resource_server_url: Optional[str] = None,
    mcpmarket_url: str = "https://mcpmarket.cn",
    required_scopes: Optional[List[str]] = None,
    mcp_path: str = "/mcp",
    host: str = "0.0.0.0",
    port: int = 8000,
    debug: bool = False,
    cache_ttl: int = 300,
) -> Starlette:
    """
    为底层 Server 创建带 MCPMarket OAuth 的 Starlette 应用
    
    使用示例::
    
        from mcp.server.lowlevel import Server
        from uno_oauth_mcp import create_oauth_starlette_app
        
        server = Server("my-server")
        
        @server.list_tools()
        async def list_tools():
            return [...]
        
        app = create_oauth_starlette_app(server)
        
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    """
    if resource_server_url is None:
        display_host = "localhost" if host in ("0.0.0.0", "::") else host
        resource_server_url = f"http://{display_host}:{port}"
    
    verifier = MCPMarketTokenVerifier(
        mcpmarket_url=mcpmarket_url,
        cache_ttl=cache_ttl,
    )
    
    session_manager = StreamableHTTPSessionManager(
        app=server,
        json_response=False,
        stateless=False,
    )
    
    async def mcp_handler(scope, receive, send):
        await session_manager.handle_request(scope, receive, send)
    
    resource_metadata_url = f"{resource_server_url}/.well-known/oauth-protected-resource"
    
    async def wellknown_protected_resource(request: Request):
        return JSONResponse({
            "resource": resource_server_url,
            "authorization_servers": [mcpmarket_url],
            "bearer_methods_supported": ["header"],
            "scopes_supported": required_scopes or ["read", "write"],
        })
    
    async def wellknown_oauth_server(request: Request):
        return JSONResponse({
            "issuer": mcpmarket_url,
            "authorization_endpoint": f"{mcpmarket_url}/oauth/authorize",
            "token_endpoint": f"{mcpmarket_url}/oauth/token",
            "registration_endpoint": f"{mcpmarket_url}/oauth/register",
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token"],
            "code_challenge_methods_supported": ["S256"],
        })
    
    async def health_check(request: Request):
        return JSONResponse({"status": "healthy", "server": server.name})
    
    async def index(request: Request):
        return JSONResponse({
            "name": server.name,
            "mcp_endpoint": mcp_path,
            "authentication": {
                "type": "OAuth 2.0",
                "provider": mcpmarket_url,
            },
        })
    
    routes = [
        Route("/.well-known/oauth-protected-resource", endpoint=wellknown_protected_resource, methods=["GET"]),
        Route("/.well-known/oauth-authorization-server", endpoint=wellknown_oauth_server, methods=["GET"]),
        Route("/health", endpoint=health_check, methods=["GET"]),
        Route("/", endpoint=index, methods=["GET"]),
        Route(
            mcp_path,
            endpoint=RequireAuthMiddleware(
                mcp_handler,
                required_scopes or ["read", "write"],
                resource_metadata_url,
            ),
        ),
    ]
    
    middleware = [
        Middleware(AuthenticationMiddleware, backend=BearerAuthBackend(verifier)),
        Middleware(AuthContextMiddleware),
    ]
    
    async def lifespan(app):
        async with session_manager.run():
            yield
    
    return Starlette(debug=debug, routes=routes, middleware=middleware, lifespan=lifespan)


class UnoOAuthServer:
    """
    带 MCPMarket OAuth 的底层 Server 封装
    
    使用示例::
    
        from uno_oauth_mcp import UnoOAuthServer
        import mcp.types as types
        
        server = UnoOAuthServer(name="My Server", port=8080)
        
        @server.list_tools()
        async def list_tools():
            return [types.Tool(name="hello", description="Say hello", inputSchema={...})]
        
        @server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name == "hello":
                return [types.TextContent(type="text", text="Hello!")]
        
        server.run()
    """
    
    def __init__(
        self,
        name: str,
        version: str = None,
        instructions: str = None,
        resource_server_url: Optional[str] = None,
        mcpmarket_url: str = "https://mcpmarket.cn",
        required_scopes: Optional[List[str]] = None,
        host: str = "0.0.0.0",
        port: int = 8000,
        mcp_path: str = "/mcp",
        debug: bool = False,
        cache_ttl: int = 300,
    ):
        self._server = Server(name=name, version=version, instructions=instructions)
        self._resource_server_url = resource_server_url
        self._mcpmarket_url = mcpmarket_url
        self._required_scopes = required_scopes
        self._host = host
        self._port = port
        self._mcp_path = mcp_path
        self._debug = debug
        self._cache_ttl = cache_ttl
    
    @property
    def name(self) -> str:
        return self._server.name
    
    def list_tools(self):
        return self._server.list_tools()
    
    def call_tool(self, *, validate_input: bool = True):
        return self._server.call_tool(validate_input=validate_input)
    
    def list_resources(self):
        return self._server.list_resources()
    
    def read_resource(self):
        return self._server.read_resource()
    
    def list_resource_templates(self):
        return self._server.list_resource_templates()
    
    def list_prompts(self):
        return self._server.list_prompts()
    
    def get_prompt(self):
        return self._server.get_prompt()
    
    def completion(self):
        return self._server.completion()
    
    def get_starlette_app(self) -> Starlette:
        return create_oauth_starlette_app(
            server=self._server,
            resource_server_url=self._resource_server_url,
            mcpmarket_url=self._mcpmarket_url,
            required_scopes=self._required_scopes,
            mcp_path=self._mcp_path,
            host=self._host,
            port=self._port,
            debug=self._debug,
            cache_ttl=self._cache_ttl,
        )
    
    def run(self):
        import uvicorn
        
        app = self.get_starlette_app()
        
        print("=" * 60)
        print(f"🚀 {self.name} with MCPMarket OAuth")
        print("=" * 60)
        print(f"Server: http://{self._host}:{self._port}")
        print(f"MCP Endpoint: http://{self._host}:{self._port}{self._mcp_path}")
        print(f"Auth Server: {self._mcpmarket_url}")
        print("=" * 60)
        
        uvicorn.run(app, host=self._host, port=self._port)
    
    async def run_async(self):
        import uvicorn
        
        app = self.get_starlette_app()
        config = uvicorn.Config(app, host=self._host, port=self._port)
        server = uvicorn.Server(config)
        await server.serve()
