import json
import pytest

from e_stat_dashboard_mcp.server import mcp


@pytest.mark.asyncio
async def test_tool_analyze_correlation_with_two_datasets():
    data1 = [
        {"date": "2020-01", "value": 1},
        {"date": "2020-02", "value": 2},
        {"date": "2020-03", "value": 3},
    ]
    data2 = [
        {"date": "2020-01", "value": 2},
        {"date": "2020-02", "value": 4},
        {"date": "2020-03", "value": 6},
    ]

    result = await mcp.call_tool(
        "analyze_stats",
        {
            "analysis_type": "correlation",
            "data_json": json.dumps(data1),
            "data_json_b": json.dumps(data2),
        },
    )

    # FastMCP returns (content_list, context)
    payload = json.loads(result[0][0].text)
    assert "correlation" in payload
    assert abs(payload["correlation"] - 1.0) < 1e-6

