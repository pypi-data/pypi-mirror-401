"""
MCPMarket Token 验证器

实现官方 MCP SDK 的 TokenVerifier 协议。
"""

from datetime import datetime
from typing import Optional, Dict, Any
from collections import OrderedDict
import asyncio

import httpx

from mcp.server.auth.provider import AccessToken


class TokenCache:
    """LRU Token 缓存"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._lock = asyncio.Lock()
    
    async def get(self, token: str) -> Optional[AccessToken]:
        async with self._lock:
            if token not in self._cache:
                return None
            
            entry = self._cache[token]
            if (datetime.now() - entry["cached_at"]).total_seconds() > self.ttl:
                del self._cache[token]
                return None
            
            self._cache.move_to_end(token)
            return entry["access_token"]
    
    async def set(self, token: str, access_token: AccessToken):
        async with self._lock:
            if token in self._cache:
                del self._cache[token]
            
            while len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
            
            self._cache[token] = {
                "access_token": access_token,
                "cached_at": datetime.now()
            }
    
    async def delete(self, token: str):
        async with self._lock:
            self._cache.pop(token, None)
    
    async def clear(self):
        async with self._lock:
            self._cache.clear()


class MCPMarketTokenVerifier:
    """
    MCPMarket Token 验证器
    
    实现官方 MCP SDK 的 TokenVerifier 协议，
    通过 mcpmarket.cn API 验证 access token。
    
    Args:
        mcpmarket_url: MCPMarket 服务地址，默认 https://mcpmarket.cn
        cache_ttl: Token 缓存 TTL（秒），默认 300
        cache_max_size: Token 缓存最大条目数，默认 1000
        http_timeout: HTTP 请求超时时间（秒），默认 10
    """
    
    def __init__(
        self,
        mcpmarket_url: str = "https://mcpmarket.cn",
        cache_ttl: int = 300,
        cache_max_size: int = 1000,
        http_timeout: float = 10.0,
    ):
        self.mcpmarket_url = mcpmarket_url.rstrip("/")
        self.http_timeout = http_timeout
        self._cache = TokenCache(max_size=cache_max_size, ttl=cache_ttl)
    
    @property
    def verify_token_url(self) -> str:
        return f"{self.mcpmarket_url}/api/uno/verify-token"
    
    async def verify_token(self, token: str) -> Optional[AccessToken]:
        """验证 access token（实现官方 TokenVerifier 协议）"""
        if not token:
            return None
        
        cached = await self._cache.get(token)
        if cached:
            return cached
        
        try:
            async with httpx.AsyncClient(timeout=self.http_timeout) as client:
                response = await client.get(
                    self.verify_token_url,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid"):
                        access_token = AccessToken(
                            token=token,
                            client_id=data.get("client_id", "mcpmarket"),
                            scopes=data.get("scopes", ["read", "write"]),
                            expires_at=data.get("expires_at"),
                        )
                        await self._cache.set(token, access_token)
                        return access_token
                
                return None
                
        except Exception:
            return None
    
    async def invalidate_cache(self, token: str):
        await self._cache.delete(token)
    
    async def clear_cache(self):
        await self._cache.clear()
