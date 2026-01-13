import pandas as pd
from typing import List, Dict, Any, Optional

def calculate_summary(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate basic summary statistics."""
    if not data:
        return {}
    
    df = pd.DataFrame(data)
    if "value" not in df.columns:
         return {}
         
    # Ensure value is numeric
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    stats = df["value"].describe()
    return stats.to_dict()

def calculate_growth_rate(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate CAGR and YoY growth."""
    if not data:
        return {}
        
    df = pd.DataFrame(data)
    if "value" not in df.columns or "date" not in df.columns:
        return {}
        
    # Sort by date
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    
    # YoY
    # Assuming monthly or yearly data.
    # pct_change(periods=1) typically if consistent freq.
    # But let"s just do simplistic calc: (last - first) / first for total growth
    
    if len(df) < 2:
        return {"error": "Not enough data points"}
        
    first_val = df["value"].iloc[0]
    last_val = df["value"].iloc[-1]
    
    total_growth = (last_val - first_val) / first_val if first_val != 0 else None
    
    # CAGR
    # (Last/First)^(1/N) - 1
    # N in years.
    delta_days = (df["date"].iloc[-1] - df["date"].iloc[0]).days
    years = delta_days / 365.25
    
    cagr = None
    if years > 0 and first_val > 0 and last_val > 0:
        cagr = (last_val / first_val) ** (1/years) - 1
        
    return {
        "start_date": str(df["date"].iloc[0].date()),
        "end_date": str(df["date"].iloc[-1].date()),
        "total_growth": total_growth,
        "cagr": cagr,
        "years_approx": years
    }

def calculate_yoy(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate Year-Over-Year growth for the latest period."""
    if not data:
        return {}
    
    df = pd.DataFrame(data)
    if "value" not in df.columns or "date" not in df.columns:
        return {}
        
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    
    if len(df) < 2:
        return {"error": "Not enough data points for YoY calculation"}
        
    # Attempt to find the value from 1 year ago
    last_date = df["date"].iloc[-1]
    last_val = df["value"].iloc[-1]
    
    # Target date: 1 year ago
    # Handling leap years simply
    try:
        target_date = last_date.replace(year=last_date.year - 1)
    except ValueError:
        target_date = last_date.replace(year=last_date.year - 1, day=28)
        
    # Find closest date or exact match? Exact match is safer for stats.
    # But dates might be '2020-01-01' so standard comparison works.
    
    prev_row = df[df["date"] == target_date]
    if prev_row.empty:
         # Try to be flexible if day doesn't match exactly (e.g. end of month differences)?
         # For now strict match.
         return {"error": f"No data point found for 1 year ago ({target_date.date()})"}
         
    prev_val = prev_row["value"].iloc[0]
    
    yoy_growth = (last_val - prev_val) / prev_val if prev_val != 0 else None
    
    return {
        "current_date": str(last_date.date()),
        "prev_date": str(target_date.date()),
        "current_value": last_val,
        "prev_value": prev_val,
        "yoy_growth": yoy_growth
    }

def calculate_correlation(data1: List[Dict[str, Any]], data2: List[Dict[str, Any]]) -> Optional[float]:
    """Calculate correlation between two time series matched by date."""
    if not data1 or not data2:
        return None
        
    df1 = pd.DataFrame(data1)[["date", "value"]].rename(columns={"value": "v1"})
    df2 = pd.DataFrame(data2)[["date", "value"]].rename(columns={"value": "v2"})
    
    # Normalize dates if needed (string vs datetime)
    df1["date"] = pd.to_datetime(df1["date"])
    df2["date"] = pd.to_datetime(df2["date"])
    
    merged = pd.merge(df1, df2, on="date", how="inner")
    
    if len(merged) < 2:
        return None
        
    return float(merged["v1"].corr(merged["v2"]))
