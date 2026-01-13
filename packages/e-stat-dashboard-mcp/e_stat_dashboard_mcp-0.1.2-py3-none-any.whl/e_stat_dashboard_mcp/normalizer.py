from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

CYCLE_MAP = {
    "1": "月次",
    "2": "四半期",
    "3": "年次",
    "4": "年度"
}

def normalize_indicator_list(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize the response from getIndicatorInfo.
    """
    try:
        # Unwrap root key if present
        if "GET_META_INDICATOR_INF" in api_response:
            api_response = api_response["GET_META_INDICATOR_INF"]

        class_inf = api_response.get("METADATA_INF", {}).get("CLASS_INF", {}).get("CLASS_OBJ", [])
        if isinstance(class_inf, dict):
            class_inf = [class_inf] # Handle single item as list
            
        results = []
        for item in class_inf:
            # We only care about the indicator level, not categories usually found in CLASS_OBJ?
            # Actually getIndicatorInfo structure for SearchIndicatorWord usually returns CLASS_OBJ.
            # But we need to look for @code and @name.
            
            # The structure might vary, but let's assume standard Class object.
            # Depending on API, it might meet 'CLASS' inside.
            
            # Let's handle the case where it's a direct list of classes
            code = item.get("@code")
            name = item.get("@name")
            unit = item.get("@unit")
            
            if code and name:
                results.append({
                    "code": code,
                    "name": name,
                    "unit": unit
                })
        return results
    except Exception as e:
        logger.error(f"Error normalizing indicator list: {e}")
        return []

def normalize_stats_data(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize getData response."""
    try:
        # Unwrap root key if present
        if "GET_STATS" in api_response:
            api_response = api_response["GET_STATS"]

        data_inf = api_response.get("STATISTICAL_DATA", {}).get("DATA_INF", {})
        
        # Notes: Sometimes DATA_INF might rely on NOTES or be empty.
        if "DATA_OBJ" not in data_inf:
            return []
            
        data_obj = data_inf["DATA_OBJ"]
        if isinstance(data_obj, dict):
            data_obj = [data_obj]
            
        results = []
        for item in data_obj:
            values = item.get("VALUE", [])
            if isinstance(values, dict):
                values = [values]
            
            # Extract common attributes from item (Class info if present)
            # But usually getData returns values directly with attributes in VALUE usually?
            # Actually, VALUE has @time, $, @unit, @cycle? 
            # Or are they in the VALUE list items? Yes.
            
            # The item might contain CLASS info, but VALUE contains the time series.
            
            for val in values:
                original_time = val.get("@time")
                value_str = val.get("$")
                unit = val.get("@unit")
                cycle_code = val.get("@cycle")
                
                # Format time to easier read if possible?
                # YYYYMM00 -> YYYY-MM
                date_str = original_time
                if original_time and len(original_time) == 8:
                    if original_time.endswith("00"):
                         # Monthly or Yearly (if YYYY1000??)
                         # Simple format: YYYY-MM
                         d = original_time
                         date_str = f"{d[:4]}-{d[4:6]}"
                
                # Convert value
                value = None
                try:
                    if value_str is not None and value_str != "-":
                         value = float(value_str)
                except ValueError:
                    pass
                
                if value is not None:
                     results.append({
                         "date": date_str,
                         "value": value,
                         "unit": unit,
                         "cycle": CYCLE_MAP.get(cycle_code, cycle_code),
                         "original_time": original_time,
                         "indicator_code": item.get("CLASS", {}).get("@code") # Might not appear here
                     })
                     
        return results

    except Exception as e:
        logger.error(f"Error normalizing stats data: {e}")
        return []

def normalize_region_info(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize getRegionInfo response."""
    try:
        # Unwrap root key if present
        if "GET_META_REGION_INF" in api_response:
            api_response = api_response["GET_META_REGION_INF"]

        class_inf = api_response.get("METADATA_INF", {}).get("CLASS_INF", {}).get("CLASS_OBJ", [])
        if isinstance(class_inf, dict):
             class_inf = [class_inf]
             
        results = []
        for item in class_inf:
             results.append({
                 "code": item.get("@code"),
                 "name": item.get("@name"),
                 "parent_code": item.get("@parentCode")
             })
        return results
    except Exception as e:
        logger.error(f"Error normalizing region info: {e}")
        return []
