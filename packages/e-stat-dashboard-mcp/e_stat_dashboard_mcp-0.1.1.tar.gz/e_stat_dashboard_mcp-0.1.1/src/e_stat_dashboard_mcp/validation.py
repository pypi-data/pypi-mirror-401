import re
from typing import Optional

class EStatValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_date(date_str: Optional[str], param_name: str = "date"):
    """
    Validate date format YYYYMMDD (or YYYYMM00 as required by API).
    The e-Stat API typically uses 'YYYYMM00' for monthly, 'YYYY0000' for annual?
    Actually API allows YYYYMMDD? 
    Walkthrough says 'YYYYMM00'.
    Let's enforce 8 digits.
    """
    if not date_str:
        return
        
    if not re.match(r"^\d{8}$", date_str):
        raise EStatValidationError(f"Invalid format for {param_name}: '{date_str}'. Expected 8 digits (YYYYMMDD or YYYYMM00).")

def validate_cycle(cycle: Optional[str]):
    """Validate cycle code."""
    if not cycle:
        return
        
    valid_cycles = {"1", "2", "3", "4"}
    if cycle not in valid_cycles:
        raise EStatValidationError(f"Invalid cycle: '{cycle}'. Expected one of {valid_cycles}.")

def validate_date_range(from_date: Optional[str], to_date: Optional[str]):
    """Ensure from_date <= to_date."""
    if from_date and to_date:
        if from_date > to_date:
            raise EStatValidationError(f"from_date '{from_date}' cannot be after to_date '{to_date}'.")
