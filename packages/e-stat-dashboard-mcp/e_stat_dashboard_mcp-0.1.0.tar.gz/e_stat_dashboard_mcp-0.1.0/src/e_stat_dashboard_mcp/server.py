from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple
import time
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .config import settings
from .api_client import EStatClient
from .normalizer import normalize_indicator_list, normalize_stats_data
from .logging_config import configure_logging
from .validation import validate_date, validate_cycle, validate_date_range, EStatValidationError
import json

# Configure logging
configure_logging()

def format_error(code: str, message: str, details: Optional[str] = None) -> str:
    """Format error as JSON."""
    return json.dumps({
        "error": {
            "code": code,
            "message": message,
            "details": details
        }
    }, ensure_ascii=False)

# Initialize Client
# Note: We should handle cleanup, but FastMCP doesn't strictly require it for simple http clients.
# We'll stick to a global client for simplicity or instantiate per request if needed (but global is better for connection pooling).
client = EStatClient()

class SimpleCache:
    def __init__(self, ttl_seconds: int):
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self.ttl = ttl_seconds
        
    def get(self, key: str) -> Any:
        if key in self._cache:
            ts, val = self._cache[key]
            if time.time() - ts < self.ttl:
                return val
            else:
                del self._cache[key]
        return None
        
    def set(self, key: str, value: Any):
        self._cache[key] = (time.time(), value)

# Caches
search_cache = SimpleCache(86400) # 24h
region_cache = SimpleCache(604800) # 7 days

mcp = FastMCP("e-Stat Dashboard MCP")

@lru_cache(maxsize=100)
async def _cached_search(keyword: str) -> List[Dict[str, Any]]:
    """Cached search helper"""
    response = await client.get_indicator_info(keyword)
    return normalize_indicator_list(response)

@mcp.tool()
async def search_indicators(keyword: str = Field(..., description="Search keyword (e.g. 'unemployment', 'CPI')")) -> str:
    """
    Search for statistical indicators by keyword. 
    Returns a list of matching indicators with their codes, names, and units.
    This is best used when you don't know the exact indicator code.
    """
    try:
        cached = search_cache.get(keyword)
        if cached:
            return cached
            
        response = await client.get_indicator_info(keyword)
        clean_results = normalize_indicator_list(response)
        
        if not clean_results:
            return format_error("NO_DATA", "No indicators found matching the keyword.")
        
        # Limit results to top 20 to avoid token explosion
        limited_results = clean_results[:20]
        
        # Format as Markdown list
        md_lines = ["Found the following indicators (showing top 20):"]
        for item in limited_results:
            md_lines.append(f"- `[{item['code']}]` **{item['name']}** ({item.get('unit', '-')})")
            
        result_str = "\n".join(md_lines)
        search_cache.set(keyword, result_str)
        return result_str
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return format_error("SEARCH_ERROR", str(e))

@mcp.tool()
async def get_stats_data(
    indicator_code: str = Field(..., description="Indicator Code (e.g. '0301010000020020010')"),
    from_date: Optional[str] = Field(None, description="Start date in YYYYMM00 format (e.g. '20200100')"),
    to_date: Optional[str] = Field(None, description="End date in YYYYMM00 format"),
    cycle: Optional[str] = Field(None, description="1:Month, 2:Quarter, 3:Year, 4:Fiscal Year")
) -> str:
    """
    Get statistical data for a specific indicator.
    Returns a list of data points with date, value, and unit.
    """
    try:
        # Validation
        validate_date(from_date, "from_date")
        validate_date(to_date, "to_date")
        validate_date_range(from_date, to_date)
        validate_cycle(cycle)

        response = await client.get_data(
            indicator_code, 
            from_date=from_date, 
            to_date=to_date, 
            cycle=cycle
        )
        data = normalize_stats_data(response)
        
        if not data:
            return format_error("NO_DATA", "No data found for the specified criteria.")
            
        return json.dumps(data, ensure_ascii=False, indent=2)
        
    except EStatValidationError as e:
        return format_error("VALIDATION_ERROR", str(e))
    except Exception as e:
        logger.error(f"Get stats failed: {e}")
        return format_error("API_ERROR", str(e))

@mcp.tool()
async def list_regions(parent_region_code: Optional[str] = Field(None, description="Parent Region Code (e.g. '00000' for Japan)")) -> str:
    """
    List regions (e.g. prefectures, cities).
    If parent_region_code is omitted, it might return top level.
    Use '00000' for Japan to list prefectures likely.
    """
    try:
        cache_key = parent_region_code or "ROOT"
        cached = region_cache.get(cache_key)
        if cached:
            return cached
            
        # We also need normalizer for regions
        from .normalizer import normalize_region_info
        
        response = await client.get_region_info(parent_region_code)
        data = normalize_region_info(response)
        
        if not data:
            return format_error("NO_DATA", "No regions found.")
            
        result_str = json.dumps(data, ensure_ascii=False, indent=2)
        region_cache.set(cache_key, result_str)
        return result_str
    except Exception as e:
        return format_error("REGION_ERROR", str(e))

@mcp.tool()
async def analyze_stats(
    data_json: str = Field(..., description="JSON string of data returned by get_stats_data"),
    analysis_type: str = Field(..., description="Analysis type: 'summary', 'cagr', 'yoy', 'growth' (alias for cagr)")
) -> str:
    """
    Analyze statistical data.
    Supported types:
    - summary: Basic statistics (count, mean, min, max)
    - cagr (or growth): Compound Annual Growth Rate and Total Growth
    - yoy: Year-over-Year growth
    """
    try:
        from .analytics import calculate_summary, calculate_growth_rate, calculate_yoy
        
        data = json.loads(data_json)
        if not isinstance(data, list):
             return format_error("INVALID_INPUT", "data_json must be a list of records.")
             
        result = {}
        if analysis_type == "summary":
            result = calculate_summary(data)
        elif analysis_type in ["growth", "cagr"]:
            result = calculate_growth_rate(data)
        elif analysis_type == "yoy":
            result = calculate_yoy(data)
        else:
            return format_error("INVALID_INPUT", f"Unknown analysis type '{analysis_type}'")
            
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return format_error("ANALYSIS_ERROR", str(e))

@mcp.tool()
async def generate_graph_code(
    data_payload: str = Field(..., description="JSON string of data"),
    graph_type: str = Field(..., description="Type of graph: 'line', 'bar', 'scatter'"),
    title: str = Field("Graph", description="Title of the graph"),
    x_label: str = Field("Date", description="X-axis label"),
    y_label: str = Field("Value", description="Y-axis label")
) -> str:
    """
    Generate Python code to visualize the data using matplotlib.
    The code includes imports for japanize-matplotlib.
    """
    try:
        from .visualizer import generate_python_code
        
        data = json.loads(data_payload)
        if not isinstance(data, list):
             return format_error("INVALID_INPUT", "data_payload must be a list of records.")
             
        code = generate_python_code(data, graph_type, title, x_label, y_label)
        return code
    except Exception as e:
        return format_error("VISUALIZATION_ERROR", str(e))

@mcp.tool()
def hello() -> str:
    """Returns a greeting message to verify server is running."""
    return "Hello from e-Stat Dashboard MCP!"

if __name__ == "__main__":
    mcp.run()
