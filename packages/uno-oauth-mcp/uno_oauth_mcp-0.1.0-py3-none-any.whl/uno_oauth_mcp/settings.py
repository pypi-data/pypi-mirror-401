"""
MCPMarket 认证配置
"""

from typing import Optional, List
from pydantic import AnyHttpUrl

from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions


MCPMARKET_DEFAULT_URL = "https://mcpmarket.cn"
DEFAULT_SCOPES = ["read", "write"]


class MCPMarketAuthSettings:
    """MCPMarket 认证配置辅助类"""
    
    def __init__(
        self,
        resource_server_url: str,
        mcpmarket_url: str = MCPMARKET_DEFAULT_URL,
        required_scopes: Optional[List[str]] = None,
        enable_client_registration: bool = True,
        enable_revocation: bool = True,
    ):
        self.resource_server_url = resource_server_url.rstrip("/")
        self.mcpmarket_url = mcpmarket_url.rstrip("/")
        self.required_scopes = required_scopes or DEFAULT_SCOPES
        self.enable_client_registration = enable_client_registration
        self.enable_revocation = enable_revocation
    
    def to_auth_settings(self) -> AuthSettings:
        return AuthSettings(
            issuer_url=AnyHttpUrl(self.mcpmarket_url),
            resource_server_url=AnyHttpUrl(self.resource_server_url),
            service_documentation_url=AnyHttpUrl(f"{self.mcpmarket_url}/docs"),
            required_scopes=self.required_scopes,
            client_registration_options=ClientRegistrationOptions(
                enabled=self.enable_client_registration,
                valid_scopes=self.required_scopes,
                default_scopes=self.required_scopes,
            ) if self.enable_client_registration else None,
            revocation_options=RevocationOptions(
                enabled=self.enable_revocation,
            ) if self.enable_revocation else None,
        )


def mcpmarket_auth_settings(
    resource_server_url: str,
    mcpmarket_url: str = MCPMARKET_DEFAULT_URL,
    required_scopes: Optional[List[str]] = None,
) -> AuthSettings:
    """创建 MCPMarket 认证配置"""
    settings = MCPMarketAuthSettings(
        resource_server_url=resource_server_url,
        mcpmarket_url=mcpmarket_url,
        required_scopes=required_scopes,
    )
    return settings.to_auth_settings()
