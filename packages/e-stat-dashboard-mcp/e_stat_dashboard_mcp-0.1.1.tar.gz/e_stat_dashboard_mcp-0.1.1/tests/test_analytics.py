import pytest
import pandas as pd
from e_stat_dashboard_mcp.analytics import calculate_summary, calculate_growth_rate, calculate_correlation

def test_calculate_summary():
    data = [{"value": 10}, {"value": 20}, {"value": 30}]
    stats = calculate_summary(data)
    assert stats["count"] == 3
    assert stats["mean"] == 20
    assert stats["min"] == 10
    assert stats["max"] == 30

def test_calculate_growth_rate():
    data = [
        {"date": "2020-01-01", "value": 100},
        {"date": "2021-01-01", "value": 110}, # 10% growth
        {"date": "2022-01-01", "value": 121}  # 10% growth
    ]
    res = calculate_growth_rate(data)
    assert res["years_approx"] > 1.9 and res["years_approx"] < 2.1
    # CAGR should be approx 0.10
    assert abs(res["cagr"] - 0.10) < 0.01

def test_calculate_correlation():
    data1 = [{"date": "2020-01", "value": 1}, {"date": "2020-02", "value": 2}, {"date": "2020-03", "value": 3}]
    data2 = [{"date": "2020-01", "value": 2}, {"date": "2020-02", "value": 4}, {"date": "2020-03", "value": 6}]
    # Perfect linear correlation
    corr = calculate_correlation(data1, data2)
    assert abs(corr - 1.0) < 0.001

def test_calculate_yoy():
    # Setup data: 3 years of monthly data
    from e_stat_dashboard_mcp.analytics import calculate_yoy
    data = [
        {"date": "2020-01-01", "value": 100},
        {"date": "2021-01-01", "value": 110}, # 10% growth
    ]
    # Simple check
    result = calculate_yoy(data)
    assert result["yoy_growth"] == 0.1
    assert result["current_value"] == 110
    assert result["prev_value"] == 100

    # Case: No prev data
    data2 = [{"date": "2020-01-01", "value": 100}]
    result2 = calculate_yoy(data2)
    assert "error" in result2

def test_calculate_yoy_complex():
    from e_stat_dashboard_mcp.analytics import calculate_yoy
    data = [
        {"date": "2020-01-01", "value": 100},
        {"date": "2020-02-01", "value": 105},
        {"date": "2021-01-01", "value": 120}, # 20% vs 2020-01
        {"date": "2021-02-01", "value": 105}, # 0% vs 2020-02
    ]
    # Should compare last point (2021-02) with 2020-02
    result = calculate_yoy(data)
    assert result["yoy_growth"] == 0.0
    assert result["current_date"] == "2021-02-01"
    assert result["prev_date"] == "2020-02-01"
