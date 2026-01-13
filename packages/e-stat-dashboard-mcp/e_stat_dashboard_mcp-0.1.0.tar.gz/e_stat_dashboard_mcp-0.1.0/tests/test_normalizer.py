import pytest
import json
from e_stat_dashboard_mcp.normalizer import normalize_indicator_list, normalize_stats_data, normalize_region_info

def test_normalize_indicator_list():
    sample_response = {
        "METADATA_INF": {
            "CLASS_INF": {
                "CLASS_OBJ": [
                    {"@code": "1001", "@name": "Indicator A", "@unit": "円"},
                    {"@code": "1002", "@name": "Indicator B", "@unit": "%"}
                ]
            }
        }
    }
    result = normalize_indicator_list(sample_response)
    assert len(result) == 2
    assert result[0] == {"code": "1001", "name": "Indicator A", "unit": "円"}

def test_normalize_stats_data_simple():
    sample_response = {
        "STATISTICAL_DATA": {
            "DATA_INF": {
                "DATA_OBJ": [
                    {
                        "VALUE": [
                            {"@time": "20230100", "$": "123.4", "@unit": "円", "@cycle": "1"},
                            {"@time": "20230200", "$": "125.0", "@unit": "円", "@cycle": "1"}
                        ]
                    }
                ]
            }
        }
    }
    result = normalize_stats_data(sample_response)
    assert len(result) == 2
    assert result[0]["date"] == "2023-01"
    assert result[0]["value"] == 123.4
    assert result[0]["cycle"] == "月次"

def test_normalize_stats_data_single_obj():
    # API sometimes returns a dict instead of list if only one item
    sample_response = {
        "STATISTICAL_DATA": {
            "DATA_INF": {
                "DATA_OBJ": {
                    "VALUE": {"@time": "20230100", "$": "100", "@unit": "%", "@cycle": "1"}
                }
            }
        }
    }
    result = normalize_stats_data(sample_response)
    assert len(result) == 1
    assert result[0]["value"] == 100.0

def test_normalize_stats_data_missing_value():
    sample_response = {
        "STATISTICAL_DATA": {
            "DATA_INF": {
                "DATA_OBJ": {
                    "VALUE": {"@time": "20230100", "$": "-", "@unit": "%", "@cycle": "1"}
                }
            }
        }
    }
    result = normalize_stats_data(sample_response)
    assert len(result) == 0

def test_normalize_region_info():
    sample_response = {
        "METADATA_INF": {
            "CLASS_INF": {
                "CLASS_OBJ": [
                    {"@code": "01000", "@name": "Hokkaido", "@parentCode": "00000"}
                ]
            }
        }
    }
    result = normalize_region_info(sample_response)
    assert len(result) == 1
    assert result[0]["name"] == "Hokkaido"
