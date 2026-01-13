import httpx
import asyncio
import logging
from typing import Any, Dict, Optional
from .config import settings

logger = logging.getLogger(__name__)

class EStatClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.lang = settings.LANG
        self.client = httpx.AsyncClient(timeout=30.0)
        self.semaphore = asyncio.Semaphore(5) # Rate limit guard

    async def close(self):
        await self.client.aclose()

    async def _request(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{path}"
        default_params = {"Lang": self.lang}
        # Filter None values from params
        clean_params = {k: v for k, v in params.items() if v is not None}
        merged_params = {**default_params, **clean_params}
        
        retries = 3
        delay = 1.0
        
        async with self.semaphore:
            for attempt in range(retries):
                try:
                    response = await self.client.get(url, params=merged_params)
                    response.raise_for_status()
                    return response.json()
                except (httpx.RequestError, httpx.HTTPStatusError) as e:
                    should_retry = False
                    if isinstance(e, httpx.RequestError): # Network errors (timeouts, etc)
                         should_retry = True
                    elif isinstance(e, httpx.HTTPStatusError):
                        if e.response.status_code in [429, 500, 502, 503, 504]:
                            should_retry = True
                    
                    if not should_retry:
                         raise
                    
                    if attempt == retries - 1:
                        logger.error(f"Failed to fetch {url} after {retries} attempts: {e}")
                        raise
                    
                    logger.warning(f"Request failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                    delay *= 2
        return {} # Should not be reached

    async def get_indicator_info(self, keyword: str) -> Dict[str, Any]:
        return await self._request("getIndicatorInfo", {"SearchIndicatorWord": keyword})

    async def get_data(self, indicator_code: str, from_date: Optional[str] = None, to_date: Optional[str] = None, cycle: Optional[str] = None) -> Dict[str, Any]:
        params = {"IndicatorCode": indicator_code}
        if from_date:
            params["TimeFrom"] = from_date
        if to_date:
            params["TimeTo"] = to_date
        if cycle:
            params["Cycle"] = cycle
        return await self._request("getData", params)

    async def get_region_info(self, parent_region_code: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if parent_region_code:
            params["ParentRegionCode"] = parent_region_code
        return await self._request("getRegionInfo", params)
