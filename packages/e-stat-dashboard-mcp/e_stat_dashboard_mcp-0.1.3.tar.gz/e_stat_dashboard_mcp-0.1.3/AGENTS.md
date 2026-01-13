# Repository Guidelines

## Project Structure & Module Organization
- `src/e_stat_dashboard_mcp/`: core code — `server.py` (FastMCP server), `api_client.py` (httpx client), `normalizer.py`, `analytics.py`, `visualizer.py`, `validation.py`, `config.py`, `logging_config.py`.
- `tests/`: pytest suite (includes asyncio + respx for HTTP mocking). Files follow `test_*.py`.
- `docs/`: project plan and spec (`PLAN.md`, `SPEC.md`).
- `.github/workflows/`: CI (tests) and release (PyPI) pipelines.

## Build, Test, and Development Commands
- Install deps (uv): `uv sync`
- Run server locally: `uv run python -m e_stat_dashboard_mcp.server`
- MCP Inspector: `npx @modelcontextprotocol/inspector uv run python -m e_stat_dashboard_mcp.server`
- Run tests: `uv run env PYTHONPATH=src python -m pytest -q`
- Lint (Ruff): `uv run ruff check .`  |  Format: `uv run ruff format`
- Build wheel/sdist: `uv build`

## Coding Style & Naming Conventions
- Python ≥ 3.10, 4‑space indent, line length 88.
- Ruff rules enabled: `E,F,B,I` (includes import sorting). Keep code lint‑clean.
- Naming: modules/files `snake_case.py`; functions `snake_case`; classes `PascalCase`; constants `UPPER_SNAKE_CASE`.
- Use type hints and small, focused functions. Log via `logging` (stderr configured in `logging_config.py`).

## Testing Guidelines
- Frameworks: `pytest`, `pytest-asyncio`; HTTP mocking with `respx` (no live API calls).
- Place tests under `tests/`; name files and test functions `test_*`.
- Cover: tool behaviors, validation errors, large-data resource URIs, analytics calculations, visualizer output.
- Run locally with `PYTHONPATH=src` (see command above).

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat: …`, `fix: …`, `docs: …`, `chore: …` (see Git history).
- PRs must include: clear description, linked issues, validation steps (commands/logs), and updated tests/docs when applicable.
- CI must pass on 3.10–3.12; no lint errors.

## Security & Configuration Tips
- Do not commit secrets. Configure via `.env` using `ESTAT_` prefix (e.g., `ESTAT_API_BASE_URL`, `ESTAT_LANG`).
- Network access is via `httpx.AsyncClient` with retries; always mock in tests.

## Architecture Overview
- FastMCP server exposing tools; responses normalized before analytics/visualization. Large responses may be returned as resource URIs like `resource://e-stat/temp/<file>`, retrievable via the `read_resource` tool.

