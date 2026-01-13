import pytest
import respx
from mcp import CallToolRequest, types
from e_stat_dashboard_mcp.server import mcp
from e_stat_dashboard_mcp.config import settings

@pytest.mark.asyncio
async def test_tool_search_indicators():
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        respx_mock.get("/getIndicatorInfo").respond(
            200, 
            json={
                "METADATA_INF": {
                    "CLASS_INF": {
                        "CLASS_OBJ": [
                            {"@code": "1001", "@name": "Test Indicator", "@unit": "%"}
                        ]
                    }
                }
            }
        )
        
        # Call the tool function directly (FastMCP wraps it, but accessible?)
        # FastMCP tools are registered. We should use `mcp.call_tool`?
        # FastMCP provides `mcp._tool_manager.call_tool(...)` or similar.
        # But simpler is to import the function if it wasn't decorated away.
        # The decorator replaces the function with a wrapper.
        
        # Let's try invoking it via list_tools and call_tool emulation if possible.
        # Or just unit test the logic if I extracted it. 
        # Since I put logic inside the tool, I rely on FastMCP.
        
        result = await mcp.call_tool("search_indicators", arguments={"keyword": "test"})
        
        # Debug print
        print(f"DEBUG: result type={type(result)}, value={result}")
        if result and isinstance(result, list):
             print(f"DEBUG: item type={type(result[0])}")
        
        # FastMCP call_tool returns a list of types.TextContent or types.ImageContent
        # But if it returns the raw return value of the function in some versions?
        # Let's handle generic check
        content = str(result)
        assert "Test Indicator" in content
        assert "[1001]" in content

@pytest.mark.asyncio
async def test_tool_search_indicators_empty():
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        respx_mock.get("/getIndicatorInfo").respond(
            200, 
            json={}
        )
        
        result = await mcp.call_tool("search_indicators", arguments={"keyword": "nothing"})
        content = str(result)
        assert "No indicators found" in content

@pytest.mark.asyncio
async def test_tool_get_stats_data():
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        respx_mock.get("/getData").respond(
            200, 
            json={
                "STATISTICAL_DATA": {
                    "DATA_INF": {
                        "DATA_OBJ": [
                            {"VALUE": {"@time": "20230100", "$": "2.5", "@unit": "%", "@cycle": "1"}}
                        ]
                    }
                }
            }
        )
        
        result = await mcp.call_tool("get_stats_data", arguments={"indicator_code": "001", "from_date": "20230100"})
        content = str(result)
        assert "2023-01" in content
        assert "2.5" in content

@pytest.mark.asyncio
async def test_tool_list_regions():
    async with respx.mock(base_url=settings.API_BASE_URL) as respx_mock:
        respx_mock.get("/getRegionInfo").respond(
            200, 
            json={
                "METADATA_INF": {
                    "CLASS_INF": {
                        "CLASS_OBJ": [
                            {"@code": "01000", "@name": "Hokkaido", "@parentCode": "00000"}
                        ]
                    }
                }
            }
        )
        
        result = await mcp.call_tool("list_regions", arguments={"parent_region_code": "00000"})
        content = str(result)
        assert "Hokkaido" in content
        assert "01000" in content
