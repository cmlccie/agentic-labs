#!/usr/bin/env python3
"""Database Agent - query a SQLite database using natural language.

Requires a running local LLM server. Start one with:
    uv run agentic-labs local-llm

Requires a sample database. Create one with:
    uv run agentic-labs create-database
"""

import sqlite3
from pathlib import Path
from typing import Any

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

BASE_URL = "http://127.0.0.1:1234/v1"
API_KEY = "lite-llm"
MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are a helpful assistant that answers questions about a SQLite database.

- Use the `get_schema` tool first to understand the available tables and columns.
- Use the `query_database` tool to run SELECT queries and retrieve data.
- Only run read-only SELECT queries. Never modify the database.
- Present results in a clear, concise, human-readable format.
"""


here = Path(__file__).parent
db_path = here / "database.db"

# --------------------------------------------------------------------------------------
# Agent
# --------------------------------------------------------------------------------------

provider = OpenAIProvider(base_url=BASE_URL, api_key=API_KEY)
model = OpenAIChatModel(MODEL, provider=provider)

agent = Agent(model, system_prompt=SYSTEM_PROMPT)

# --------------------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------------------


@agent.tool()
def get_schema(ctx: RunContext) -> str:
    """Return the DDL schema of all tables in the database."""
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    return "\n\n".join(f"-- {name}\n{sql}" for name, sql in rows)


@agent.tool()
def query_database(ctx: RunContext, sql: str) -> list[dict[str, Any]]:
    """Run a read-only SELECT query against the database and return the results.

    Args:
        sql: A SQL SELECT query to execute.

    Returns:
        A list of rows, each represented as a dictionary of column names to values.
    """
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql).fetchall()
    return [dict(row) for row in rows]


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    agent.to_cli_sync(prog_name="database-agent")
