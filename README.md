# Arett Agent

End-to-end AI operations agent for S2K ERP + marketplace automation.

## Quickstart

1. Create a Python 3.11+ virtualenv
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill credentials
4. Run tests: `pytest -q`
5. Start MCP server: `python -m src.mcp_server.server`
6. Start scheduler: `python -m src.scheduler.cron`
