import pytest
import respx
from httpx import Response
from e_stat_dashboard_mcp.api_client import EStatClient
from e_stat_dashboard_mcp.config import settings

@pytest.fixture
def client():
    return EStatClient()

@pytest.mark.asyncio
async def test_get_indicator_info_success(client):
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        respx_mock.get("/getIndicatorInfo").respond(
            status_code=200, json={"METADATA_INF": {"CLASS_INF": {"CLASS_OBJ": []}}}
        )
        
        response = await client.get_indicator_info("unemployment")
        assert "METADATA_INF" in response
        assert respx_mock.calls.call_count == 1
        request = respx_mock.calls.last.request
        assert request.url.params["SearchIndicatorWord"] == "unemployment"
        assert request.url.params["Lang"] == "JP"

@pytest.mark.asyncio
async def test_get_data_success(client):
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        respx_mock.get("/getData").respond(
            200, json={"STATISTICAL_DATA": {}}
        )
        
        await client.get_data("001", from_date="20200100")
        request = respx_mock.calls.last.request
        assert request.url.params["IndicatorCode"] == "001"
        assert request.url.params["TimeFrom"] == "20200100"

@pytest.mark.asyncio
async def test_retry_on_500(client):
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        # Fail twice, succeed third time
        route = respx_mock.get("/getIndicatorInfo")
        route.side_effect = [
            Response(500),
            Response(502),
            Response(200, json={"ok": True})
        ]
        
        response = await client.get_indicator_info("retry")
        assert response == {"ok": True}
        assert respx_mock.calls.call_count == 3

@pytest.mark.asyncio
async def test_no_retry_on_400(client):
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        respx_mock.get("/getIndicatorInfo").respond(400)
        
        with pytest.raises(Exception): # httpx.HTTPStatusError
            await client.get_indicator_info("error")
        
        assert respx_mock.calls.call_count == 1

@pytest.mark.asyncio
async def test_close(client):
    await client.close()
    # No assertion, just ensure no error
