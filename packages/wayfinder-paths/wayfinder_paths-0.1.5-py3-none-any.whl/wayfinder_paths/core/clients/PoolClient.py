"""
Pool Client
Provides read-only access to pool metadata and analytics via public endpoints.
"""

from __future__ import annotations

from typing import Any, NotRequired, Required, TypedDict

from wayfinder_paths.core.clients.AuthClient import AuthClient
from wayfinder_paths.core.clients.WayfinderClient import WayfinderClient
from wayfinder_paths.core.settings import settings


class PoolData(TypedDict):
    """Individual pool data structure"""

    id: Required[str]
    name: Required[str]
    symbol: Required[str]
    address: Required[str]
    chain_id: Required[int]
    chain_code: Required[str]
    apy: NotRequired[float]
    tvl: NotRequired[float]
    llama_apy_pct: NotRequired[float | None]
    llama_tvl_usd: NotRequired[float | None]
    llama_stablecoin: NotRequired[bool | None]
    llama_il_risk: NotRequired[str | None]
    network: NotRequired[str | None]


class PoolList(TypedDict):
    """Pool list response structure"""

    pools: Required[list[PoolData]]
    total: NotRequired[int | None]


class LlamaMatch(TypedDict):
    """Llama match data structure"""

    id: Required[str]
    llama_apy_pct: Required[float]
    llama_tvl_usd: Required[float]
    llama_stablecoin: Required[bool]
    llama_il_risk: Required[str]
    network: Required[str]


class LlamaReport(TypedDict):
    """Llama report data structure"""

    identifier: Required[str]
    apy: NotRequired[float | None]
    tvl: NotRequired[float | None]


class PoolClient(WayfinderClient):
    """Client for pool-related read operations"""

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key=api_key)
        self.api_base_url = f"{settings.WAYFINDER_API_URL}"
        self._auth_client: AuthClient | None = AuthClient(api_key=api_key)

    async def get_pools_by_ids(
        self,
        *,
        pool_ids: str,
        merge_external: bool | None = None,
    ) -> PoolList:
        """
        Fetch pools by comma-separated pool ids.

        Example:
        GET /api/v1/public/pools/?pool_ids=a,b&merge_external=false
        """
        url = f"{self.api_base_url}/public/pools/"
        params: dict[str, Any] = {"pool_ids": pool_ids}
        if merge_external is not None:
            params["merge_external"] = "true" if merge_external else "false"
        response = await self._request("GET", url, params=params, headers={})
        response.raise_for_status()
        data = response.json()
        return data.get("data", data)

    async def get_all_pools(self, *, merge_external: bool | None = None) -> PoolList:
        """
        Fetch all pools.

        Example:
        GET /api/v1/public/pools/?merge_external=false
        """
        url = f"{self.api_base_url}/public/pools/"
        params: dict[str, Any] = {}
        if merge_external is not None:
            params["merge_external"] = "true" if merge_external else "false"
        response = await self._request("GET", url, params=params, headers={})
        response.raise_for_status()
        data = response.json()
        return data.get("data", data)

    async def get_llama_matches(self) -> dict[str, LlamaMatch]:
        """
        Fetch Llama matches for pools.

        GET /api/v1/public/pools/llama/matches/
        """
        url = f"{self.api_base_url}/public/pools/llama/matches/"
        response = await self._request("GET", url, headers={})
        response.raise_for_status()
        data = response.json()
        return data.get("data", data)

    async def get_llama_reports(self, *, identifiers: str) -> dict[str, LlamaReport]:
        """
        Fetch Llama reports using identifiers (token ids, address_network, or pool ids).

        Example:
        GET /api/v1/public/pools/llama/reports/?identifiers=pool-1,usd-coin
        """
        url = f"{self.api_base_url}/public/pools/llama/reports/"
        params = {"identifiers": identifiers}
        response = await self._request("GET", url, params=params, headers={})
        response.raise_for_status()
        data = response.json()
        return data.get("data", data)
