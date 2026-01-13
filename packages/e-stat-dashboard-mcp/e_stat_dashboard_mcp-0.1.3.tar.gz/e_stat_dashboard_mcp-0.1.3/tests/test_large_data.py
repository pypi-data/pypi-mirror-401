import pytest
import json
from unittest.mock import AsyncMock, patch
from e_stat_dashboard_mcp.server import mcp, client

# Mock data
MOCK_INDICATOR_RESPONSE = {
    "GET_META_INDICATOR_INF": {
        "METADATA_INF": {
            "CLASS_INF": {
                "CLASS_OBJ": [
                    {"@code": "0301010000020020010", "@name": "Unemployment Rate", "@unit": "%"}
                ]
            }
        }
    }
}

MOCK_STATS_DATA = {
    "GET_STATS": {
        "STATISTICAL_DATA": {
            "DATA_INF": {
                "DATA_OBJ": [
                    {"VALUE": {"@time": "20230100", "$": "2.5", "@unit": "%", "@cycle": "1"}},
                    {"VALUE": {"@time": "20230200", "$": "2.6", "@unit": "%", "@cycle": "1"}},
                    {"VALUE": {"@time": "20230300", "$": "2.4", "@unit": "%", "@cycle": "1"}},
                    {"VALUE": {"@time": "20230400", "$": "2.5", "@unit": "%", "@cycle": "1"}},
                    {"VALUE": {"@time": "20230500", "$": "2.6", "@unit": "%", "@cycle": "1"}},
                ]
            }
        }
    }
}

@pytest.mark.asyncio
async def test_get_stats_data_limit():
    """Test get_stats_data with limit parameter."""
    with patch.object(client, 'get_data', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MOCK_STATS_DATA
        
        # Test with limit=3
        result = await mcp.call_tool("get_stats_data", {
            "indicator_code": "0301010000020020010",
            "limit": 3
        })
        
        # FastMCP call_tool returns a tuple (content_list, context)
        # content_list is a list of Content objects
        content_list = result[0]
        text = content_list[0].text
        wrapper = json.loads(text)
        
        # Verify wrapper structure
        assert "data" in wrapper
        assert "meta" in wrapper
        assert wrapper["resourceUri"] is None
        
        data = wrapper["data"]
        assert len(data) == 3
        # Should be latest 3 records (2023-05, 2023-04, 2023-03) sorted chronologically
        assert data[0]["date"] == "2023-03"
        assert data[2]["date"] == "2023-05"

@pytest.mark.asyncio
async def test_analyze_stats_server_side_fetch():
    """Test analyze_stats internal data fetching."""
    with patch.object(client, 'get_data', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MOCK_STATS_DATA
        
        # Test without data_json, but with indicator_code
        result = await mcp.call_tool("analyze_stats", {
            "analysis_type": "summary",
            "indicator_code": "0301010000020020010"
        })
        
        result_json = result[0][0].text
        result_data = json.loads(result_json)
        assert result_data["count"] == 5
        assert result_data["mean"] == 2.52
        assert "median" in result_data
        assert "variance" in result_data
        
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "0301010000020020010"

@pytest.mark.asyncio
async def test_analyze_stats_missing_args():
    """Test analyze_stats with missing required arguments."""
    result = await mcp.call_tool("analyze_stats", {
        "analysis_type": "summary"
    })
    
    # Expect error JSON
    # Expect error JSON
    data = json.loads(result[0][0].text)
    assert "error" in data
    assert data["error"]["code"] == "INVALID_INPUT"

@pytest.mark.asyncio
async def test_get_stats_data_resource():
    """Test get_stats_data returns resource URI for large data."""
    # Create large mock data
    large_data = []
    for i in range(1000): # Enough to exceed threshold? Maybe not for 1MB.
         large_data.append({"VALUE": {"@time": f"2023{i:04d}", "$": "1.0", "@unit": "%", "@cycle": "1"}})
         
    # We'll patch RESOURCE_THRESHOLD_BYTES in server.py to be small
    with patch('e_stat_dashboard_mcp.server.RESOURCE_THRESHOLD_BYTES', 100): # 100 bytes threshold
        with patch.object(client, 'get_data', new_callable=AsyncMock) as mock_get:
             
             mock_get.return_value = {
                "GET_STATS": {
                    "STATISTICAL_DATA": {
                        "DATA_INF": { "DATA_OBJ": large_data }
                    }
                }
             }

             result = await mcp.call_tool("get_stats_data", {
                 "indicator_code": "LARGE_DATA"
             })
             
             wrapper = json.loads(result[0][0].text)
             assert wrapper["data"] is None
             assert wrapper["resourceUri"] is not None
             assert wrapper["resourceUri"].startswith("resource://e-stat/temp/")
             assert wrapper["meta"]["is_resource"] is True
             
             # Now test reading it back
             read_result = await mcp.call_tool("read_resource", {
                 "uri": wrapper["resourceUri"]
             })
             
             content = read_result[0][0].text
             loaded_data = json.loads(content)
             assert len(loaded_data) == 1000

@pytest.mark.asyncio
async def test_analyze_stats_by_uri():
    """Test analyze_stats can read data from URI."""
    from e_stat_dashboard_mcp.server import save_to_temp_resource
    
    # Create temp resource
    data = [{"value": 10}, {"value": 20}, {"value": 30}]
    filename = save_to_temp_resource(json.dumps(data), "test_analyze")
    uri = f"resource://e-stat/temp/{filename}"
    
    result = await mcp.call_tool("analyze_stats", {
        "analysis_type": "summary",
        "data_uri": uri
    })
    
    result_data = json.loads(result[0][0].text)
    assert result_data["count"] == 3
    assert result_data["mean"] == 20

@pytest.mark.asyncio
async def test_generate_graph_by_uri():
    """Test generate_graph_code can read data from URI."""
    from e_stat_dashboard_mcp.server import save_to_temp_resource
    
    # Create temp resource
    data = [{"date": "2020-01", "value": 10}, {"date": "2020-02", "value": 20}]
    filename = save_to_temp_resource(json.dumps(data), "test_graph")
    uri = f"resource://e-stat/temp/{filename}"
    
    result = await mcp.call_tool("generate_graph_code", {
        "graph_type": "line",
        "data_uri": uri
    })
    
    code = result[0][0].text
    assert "plt.plot" in code
    assert "japanize_matplotlib" in code
