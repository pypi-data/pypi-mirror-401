import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

def calculate_summary(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate basic summary statistics."""
    if not data:
        return {}
    
    df = pd.DataFrame(data)
    if "value" not in df.columns:
         return {}
         
    # Ensure value is numeric
    # Ensure value is numeric
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    
    if df["value"].dropna().empty:
         return {}
         
    stats = df["value"].describe()
    
    # Extended stats
    mean_val = stats["mean"]
    std_val = stats["std"]
    
    result = {
        "count": int(stats["count"]),
        "mean": float(mean_val),
        "median": float(df["value"].median()),
        "min": float(stats["min"]),
        "max": float(stats["max"]),
        "std_dev": float(std_val) if not pd.isna(std_val) else None,
        "variance": float(df["value"].var()) if len(df) > 1 else None,
        "percentile_25": float(stats["25%"]),
        "percentile_75": float(stats["75%"]),
        "skewness": float(df["value"].skew()) if len(df) > 2 and df["value"].std() > 0 else None,
        "kurtosis": float(df["value"].kurt()) if len(df) > 3 and df["value"].std() > 0 else None,
    }
    
    # Coefficient of Variation
    if mean_val and mean_val != 0 and std_val and not pd.isna(std_val):
         result["coefficient_of_variation"] = float(std_val / mean_val)
    else:
         result["coefficient_of_variation"] = None
         
    return result

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

def calculate_trend(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate linear trend (slope) and R-squared."""
    if not data:
        return {}
    
    df = pd.DataFrame(data)
    if "value" not in df.columns or "date" not in df.columns:
        return {}
        
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    
    if len(df) < 2:
         return {"error": "Not enough data points for trend analysis"}
         
    # Create simple numeric index for regression [0, 1, 2, ...]
    x = np.arange(len(df))
    y = df["value"].values
    
    # Linear regression: y = ax + b
    # np.polyfit returns [slope, intercept]
    slope, intercept = np.polyfit(x, y, 1)
    
    # Calculate R-squared
    y_pred = slope * x + intercept
    y_mean = np.mean(y)
    ss_tot = np.sum((y - y_mean) ** 2)
    ss_res = np.sum((y - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    
    trend_direction = "flat"
    if slope > 0: trend_direction = "up"
    elif slope < 0: trend_direction = "down"
    
    return {
        "slope": float(slope),
        "r_squared": float(r_squared),
        "intercept": float(intercept),
        "direction": trend_direction,
        "latest_value": float(y[-1])
    }

def calculate_anomaly(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate Z-score for the latest data point to detect anomaly."""
    if not data:
        return {}
        
    df = pd.DataFrame(data)
    if "value" not in df.columns:
        return {}
        
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    
    if len(df) < 3: # Need some history
         return {"error": "Not enough data points for anomaly detection"}

    latest = df.iloc[-1]
    history = df.iloc[:-1] # Compare latest against history? Or against whole distribution including valid self?
    # Standard Z-score usually uses mean/std of the population.
    # If detecting if *latest* is anomalous relative to *past*, use past stats.
    
    mean_val = history["value"].mean()
    std_val = history["value"].std()
    
    if std_val == 0:
        if latest["value"] != mean_val:
             # Infinite Z-score theoretically, but treat as anomaly
             z_score = 999.0 if latest["value"] > mean_val else -999.0
        else:
             z_score = 0.0
    else:
        z_score = (latest["value"] - mean_val) / std_val
        
    is_anomaly = abs(z_score) > 2.0 # Standard threshold > 2 sigma (approx 95%)
    
    return {
        "latest_date": str(latest["date"]),
        "latest_value": float(latest["value"]),
        "mean_history": float(mean_val),
        "std_history": float(std_val),
        "z_score": float(z_score),
        "is_anomaly": bool(is_anomaly)
    }
