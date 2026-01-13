import pytest
from e_stat_dashboard_mcp.validation import validate_date, validate_cycle, EStatValidationError

def test_validation():
    # Date
    validate_date("20200100")
    with pytest.raises(EStatValidationError):
        validate_date("2020-01-01") # Wrong format
    with pytest.raises(EStatValidationError):
        validate_date("123") # Too short
        
    # Cycle
    validate_cycle("1")
    validate_cycle("4")
    with pytest.raises(EStatValidationError):
        validate_cycle("5")
