# e-Stat Dashboard MCP Server

An MCP (Model Context Protocol) server to interact with the e-Stat Dashboard API, providing Japanese statistical data to LLMs.

## Installation & Usage

### Using `uv` (Recommended)
You can run the server directly without installing it using `uvx`:

```bash
uvx e-stat-dashboard-mcp
```

### via Claude Desktop config
Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "e-stat-dashboard": {
      "command": "uvx",
      "args": ["e-stat-dashboard-mcp"]
    }
  }
}
```

### Manual Installation (pip)

```bash
pip install e-stat-dashboard-mcp
python -m e_stat_dashboard_mcp.server
```

### Local Development
Clone the repository and install dependencies:

```bash
git clone https://github.com/takurot/e-stat-dashboard-mcp.git
cd e-stat-dashboard-mcp
uv sync
```

## Running the Server (Local)

```bash
uv run python -m e_stat_dashboard_mcp.server
```

Or via MCP Inspector:
```bash
npx @modelcontextprotocol/inspector uv run python -m e_stat_dashboard_mcp.server
```

## Tools

### `search_indicators(keyword: str) -> str`
Search for statistical indicators.
- **Example**: `search_indicators(keyword="失業率")`
- Returns a Markdown list of matching indicators with codes.

### `get_stats_data(indicator_code: str, from_date: str = None, to_date: str = None, cycle: str = None) -> str`
Get statistical data for a specific indicator.
- **Example**: `get_stats_data(indicator_code="0301010000020020010", from_date="20230100")`
- Returns a JSON string of flattened data points.

### `analyze_stats(data_json: str, analysis_type: str, ...) -> str`
Analyze the retrieved data.
- **Types**:
  - `summary`: Basic stats (mean, median, variance, quartiles, CV)
  - `cagr` (or `growth`): Compound Annual Growth Rate
  - `yoy`: Year-Over-Year growth
  - `trend`: Linear trend (slope, R², direction)
  - `anomaly`: Latest-point anomaly detection (Z-score)
  - `correlation`: Correlation between two series
- **Examples**:
  - `analyze_stats(data_json=..., analysis_type="cagr")`
  - `analyze_stats(analysis_type="correlation", data_json=[{...}], data_json_b=[{...}])`
    - Or server-side fetch: `analyze_stats(analysis_type="correlation", indicator_code="CODE_A", indicator_code_b="CODE_B")`

### `generate_graph_code(data_payload, graph_type: str, title: str, x_label: str = "Date", y_label: str = "Value") -> str`
Generate Python code to visualize data using Matplotlib (with Japanese font support).
- **Types**: `line`, `bar`, `scatter`
- **data_payload**: JSON string or already-parsed list of records (e.g., `[{"date": "2020-01", "value": 10}]`). If omitted, use `data_uri`.
- **Examples**:
  - `generate_graph_code(data_payload=[{"date": "2020-01", "value": 10}], graph_type="line", title="Unemployment Rate")`
  - `generate_graph_code(data_uri=..., graph_type="line", title="Unemployment Rate")`

### `list_regions(parent_region_code: str = None) -> str`
List regions (Prefectures, etc).
- **Example**: `list_regions(parent_region_code="00000")` (Lists prefectures)

## Configuration

Environment variables can be set in `.env` or passed directly. Prefix is `ESTAT_`.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `ESTAT_API_BASE_URL` | `https://dashboard.e-stat.go.jp/api/1.0/Json` | API Endpoint |
| `ESTAT_LANG` | `JP` | Language |

## Development

Run tests:
```bash
uv run pytest
```

Run linter:
```bash
uv run ruff check .
```
