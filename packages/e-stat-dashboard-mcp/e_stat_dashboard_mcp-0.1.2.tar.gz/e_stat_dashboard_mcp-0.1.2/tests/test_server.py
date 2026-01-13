from mcp.server.fastmcp import FastMCP
from e_stat_dashboard_mcp.server import mcp

def test_mcp_name():
    assert mcp.name == "e-Stat Dashboard MCP"

def test_hello_tool():
    # This is a bit tricky to mock invoke without a client, but we can check if tool is registered
    tools = mcp._tool_manager.list_tools()
    assert any(t.name == "hello" for t in tools)
