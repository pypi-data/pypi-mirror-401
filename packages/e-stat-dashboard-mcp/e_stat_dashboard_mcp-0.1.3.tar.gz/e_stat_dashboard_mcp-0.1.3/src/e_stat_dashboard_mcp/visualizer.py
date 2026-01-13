from typing import List, Dict, Any

def generate_python_code(
    data: List[Dict[str, Any]], 
    graph_type: str, 
    title: str = "Graph",
    x_label: str = "Date",
    y_label: str = "Value"
) -> str:
    """
    Generate Python code to visualize the data.
    """
    # Simple templates
    
    # We should embed the data into the script safely.
    import json
    # Use repr to properly escape quote characters in the string representation of the JSON
    data_json_str = json.dumps(data, ensure_ascii=False)
    
    header = f"""
import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import json

data = json.loads({repr(data_json_str)})
df = pd.DataFrame(data)

# Ensure numeric and date
if "value" in df.columns:
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

plt.figure(figsize=(10, 6))
plt.title("{title}")
"""

    footer = """
plt.tight_layout()
plt.show()
"""

    plot_code = ""
    if graph_type == "line":
        plot_code = f"""
plt.plot(df["date"], df["value"], marker="o")
plt.xlabel("{x_label}")
plt.ylabel("{y_label}")
plt.grid(True)
"""
    elif graph_type == "bar":
        plot_code = f"""
plt.bar(df["date"], df["value"])
plt.xlabel("{x_label}")
plt.ylabel("{y_label}")
"""
    elif graph_type == "scatter":
        plot_code = f"""
plt.scatter(df["date"], df["value"])
plt.xlabel("{x_label}")
plt.ylabel("{y_label}")
plt.grid(True)
"""
    else:
        # Default line
        plot_code = f"""
plt.plot(df.index, df["value"])
plt.xlabel("{x_label}")
plt.ylabel("{y_label}")
"""
    
    return header + plot_code + footer
