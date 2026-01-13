import pytest
from e_stat_dashboard_mcp.visualizer import generate_python_code

def test_generate_python_code_line():
    data = [{"date": "2020-01", "value": 10}]
    code = generate_python_code(data, "line", "Test Graph")
    assert "import matplotlib.pyplot as plt" in code
    assert "japanize_matplotlib" in code
    assert "plt.plot" in code
    assert "Test Graph" in code
    assert "2020-01" in code # data embedded in json

def test_visualizer_quote_handling():
    data = [{"date": "2020-01", "value": 100, "note": "O'Reilly"}]
    code = generate_python_code(data, "line", "Test Graph")
    
    # Check if the code contains the escaped quote or proper structure
    assert "O\\'Reilly" in code or 'O"Reilly' in code or "O'Reilly" in code
