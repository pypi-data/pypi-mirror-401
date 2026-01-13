from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple, Union
import time
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .config import settings
from .api_client import EStatClient
from .normalizer import normalize_indicator_list, normalize_stats_data
from .logging_config import configure_logging
from .validation import validate_date, validate_cycle, validate_date_range, EStatValidationError
import json
import uuid
import tempfile
from pathlib import Path
from .logging_config import logger

# Configuration for Resource URI
RESOURCE_THRESHOLD_BYTES = 1024 * 1024  # 1MB
TEMP_RESOURCE_DIR = Path(tempfile.gettempdir()) / "e-stat-dashboard-resources"
TEMP_RESOURCE_DIR.mkdir(parents=True, exist_ok=True)

def save_to_temp_resource(data_str: str, prefix: str = "stat_data") -> str:
    """Save data to temp file and return filename."""
    filename = f"{prefix}_{uuid.uuid4().hex}.json"
    file_path = TEMP_RESOURCE_DIR / filename
    file_path.write_text(data_str, encoding="utf-8")
    return filename

def _load_resource_by_uri(uri: str) -> str:
    """Helper to load resource content by URI."""
    if not uri.startswith("resource://e-stat/temp/"):
        raise ValueError("Invalid resource URI format.")
    
    filename = uri.split("/")[-1]
    file_path = TEMP_RESOURCE_DIR / filename
    
    if not file_path.exists():
        raise ValueError("Resource file not found or expired.")
        
    return file_path.read_text(encoding="utf-8")
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
            return format_error("DATA_NOT_FOUND", "No indicators found matching the keyword.")
        
        # Limit results to top 20 to avoid token explosion
        limited_results = clean_results[:20]
        
        # Format as Markdown list
        md_lines = ["Found the following indicators (showing top 20):"]
        for item in limited_results:
            md_lines.append(f"- `[{item['code']}]` **{item['name']}** ({item.get('unit', '-')})")
        if len(clean_results) > 20:
            md_lines.append("")
            md_lines.append(f"Note: {len(clean_results) - 20} more results not shown. Try refining your keyword.")
            
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
    cycle: Optional[str] = Field(None, description="1:Month, 2:Quarter, 3:Year, 4:Fiscal Year"),
    limit: Optional[int] = Field(None, description="Max number of records to return (returns latest data)")
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
            return format_error("DATA_NOT_FOUND", "No data found for the specified criteria.")
            
        # Apply limit if specified
        if limit and len(data) > limit:
            data = sorted(data, key=lambda x: x['date'], reverse=True)[:limit]
            data = sorted(data, key=lambda x: x['date'])

        # Prepare response data
        json_str = json.dumps(data, ensure_ascii=False)
        size_bytes = len(json_str.encode("utf-8"))
        is_large = size_bytes > RESOURCE_THRESHOLD_BYTES

        response_wrapper = {
            "meta": {
                "size_bytes": size_bytes,
                "is_resource": is_large,
                "record_count": len(data)
            }
        }

        if is_large:
            filename = save_to_temp_resource(json_str, prefix=f"estat_{indicator_code}")
            response_wrapper["resourceUri"] = f"resource://e-stat/temp/{filename}"
            response_wrapper["data"] = None
            logger.info(f"Data too large ({size_bytes} bytes), saved as resource: {filename}")
        else:
            response_wrapper["data"] = data
            response_wrapper["resourceUri"] = None

        return json.dumps(response_wrapper, ensure_ascii=False, indent=2)
        
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
            return format_error("DATA_NOT_FOUND", "No regions found.")
            
        result_str = json.dumps(data, ensure_ascii=False, indent=2)
        region_cache.set(cache_key, result_str)
        return result_str
    except Exception as e:
        return format_error("REGION_ERROR", str(e))

@mcp.tool()
async def analyze_stats(
    analysis_type: str = Field(..., description="Analysis type: 'summary', 'cagr', 'yoy', 'trend', 'anomaly', 'growth' (alias for cagr)"),
    data_json: Optional[Union[str, List[Dict[str, Any]]]] = Field(None, description="JSON string or list of data returned by get_stats_data. If omitted, MUST provide indicator_code or data_uri."),
    indicator_code: Optional[str] = Field(None, description="Indicator Code to fetch data for (if data_json is not provided)"),
    data_uri: Optional[str] = Field(None, description="Resource URI returned by get_stats_data for large datasets"),
    from_date: Optional[str] = Field(None, description="Start date (if fetching data)"),
    to_date: Optional[str] = Field(None, description="End date (if fetching data)"),
    cycle: Optional[str] = Field(None, description="Cycle (if fetching data)"),
    # Optional second dataset for correlation analysis
    data_json_b: Optional[Union[str, List[Dict[str, Any]]]] = Field(None, description="Second dataset JSON or list for correlation analysis"),
    indicator_code_b: Optional[str] = Field(None, description="Second indicator code for correlation analysis"),
    data_uri_b: Optional[str] = Field(None, description="Second dataset resource URI for correlation analysis"),
    from_date_b: Optional[str] = Field(None, description="Start date for second dataset (if fetching)"),
    to_date_b: Optional[str] = Field(None, description="End date for second dataset (if fetching)"),
    cycle_b: Optional[str] = Field(None, description="Cycle for second dataset (if fetching)")
) -> str:
    """
    Analyze statistical data.
    Supported types:
    - summary: Basic statistics (count, mean, min, max)
    - cagr (or growth): Compound Annual Growth Rate and Total Growth
    - yoy: Year-over-Year growth
    """
    try:
        from .analytics import (
            calculate_summary,
            calculate_growth_rate,
            calculate_yoy,
            calculate_trend,
            calculate_anomaly,
            calculate_correlation,
        )

        async def load_dataset(
            dj: Optional[Union[str, List[Dict[str, Any]]]],
            uri: Optional[str],
            code: Optional[str],
            f: Optional[str],
            t: Optional[str],
            c: Optional[str],
        ) -> List[Dict[str, Any]]:
            data_: List[Dict[str, Any]] = []
            if dj is not None:
                if isinstance(dj, str):
                    data_ = json.loads(dj)
                else:
                    data_ = dj
            elif uri:
                try:
                    json_str_ = _load_resource_by_uri(uri)
                    data_ = json.loads(json_str_)
                except Exception as e:
                    raise EStatValidationError(str(e))
            elif code:
                validate_date(f, "from_date")
                validate_date(t, "to_date")
                validate_date_range(f, t)
                validate_cycle(c)
                response_ = await client.get_data(
                    code,
                    from_date=f,
                    to_date=t,
                    cycle=c,
                )
                data_ = normalize_stats_data(response_)
            return data_

        # Validate presence of a primary data source
        has_source_a = (data_json is not None) or (data_uri is not None) or (indicator_code is not None)
        if not has_source_a:
            return format_error("INVALID_INPUT", "Either data_json, data_uri, or indicator_code must be provided.")

        # Load primary dataset
        data = await load_dataset(data_json, data_uri, indicator_code, from_date, to_date, cycle)
        if data is None or not isinstance(data, list):
            return format_error("INVALID_INPUT", "data_json must be a list of records.")
        if not data:
            return format_error("DATA_NOT_FOUND", "No data found for the specified indicator/criteria.")
             
        result = {}
        if analysis_type == "summary":
            result = calculate_summary(data)
        elif analysis_type in ["growth", "cagr"]:
            result = calculate_growth_rate(data)
        elif analysis_type == "yoy":
            result = calculate_yoy(data)
        elif analysis_type == "trend":
            result = calculate_trend(data)
        elif analysis_type == "anomaly":
            result = calculate_anomaly(data)
        elif analysis_type == "correlation":
            # Load second dataset
            # Validate presence of a second data source
            has_source_b = (data_json_b is not None) or (data_uri_b is not None) or (indicator_code_b is not None)
            if not has_source_b:
                return format_error(
                    "INVALID_INPUT",
                    "For correlation, provide a second dataset via data_json_b, data_uri_b, or indicator_code_b.",
                )

            data_b = await load_dataset(
                data_json_b, data_uri_b, indicator_code_b, from_date_b, to_date_b, cycle_b
            )
            if data_b is None or not isinstance(data_b, list) or not data_b:
                return format_error(
                    "DATA_NOT_FOUND",
                    "Second dataset not found or empty for correlation.",
                )
            corr = calculate_correlation(data, data_b)
            if corr is None:
                return format_error("INVALID_INPUT", "Insufficient overlapping data for correlation.")
            result = {"correlation": corr}
        else:
            return format_error("INVALID_INPUT", f"Unknown analysis type '{analysis_type}'")
            
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return format_error("ANALYSIS_ERROR", str(e))

@mcp.tool()
async def generate_graph_code(
    data_payload: Optional[Union[str, List[Dict[str, Any]], Dict[str, Any]]] = Field(
        None,
        description="Data payload as JSON string OR already-parsed list/dict (Optional if data_uri provided)",
    ),
    data_uri: Optional[str] = Field(None, description="Resource URI of data (Optional if data_payload provided)"),
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
        
        if data_payload is not None:
            if isinstance(data_payload, str):
                data = json.loads(data_payload)
            else:
                # Already parsed list/dict
                data = data_payload
        elif data_uri:
            try:
                json_str = _load_resource_by_uri(data_uri)
                data = json.loads(json_str)
            except Exception as e:
                return format_error("INVALID_URI", str(e))
        else:
            return format_error("INVALID_INPUT", "Either data_payload or data_uri must be provided.")

        if not isinstance(data, list):
            return format_error("INVALID_INPUT", "data must be a list of records.")
        
        code = generate_python_code(data, graph_type, title, x_label, y_label)
        return code
    except Exception as e:
        return format_error("VISUALIZATION_ERROR", str(e))

@mcp.tool()
async def read_resource(uri: str = Field(..., description="Resource URI (e.g. resource://e-stat/temp/...)")) -> str:
    """
    Read a resource file by URI.
    Use this to retrieve large datasets returned as a resource URI.
    """
    try:
        return _load_resource_by_uri(uri)
    except Exception as e:
        return format_error("READ_ERROR", str(e))

@mcp.tool()
def hello() -> str:
    """Returns a greeting message to verify server is running."""
    return "Hello from e-Stat Dashboard MCP!"

def main():
    """Entry point for the package script."""
    mcp.run()

if __name__ == "__main__":
    main()
