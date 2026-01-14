"""
attack-query MCP Server

Provides ATT&CK query capabilities to AI assistants via the Model Context Protocol.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server import Server

from attack_query import ATTACKDataStore, ATTACKQueryEngine, NLQueryParser

if TYPE_CHECKING:
    pass

# Global instances (loaded once at startup)
_store: ATTACKDataStore | None = None
_engine: ATTACKQueryEngine | None = None
_parser: NLQueryParser | None = None


def get_store() -> ATTACKDataStore:
    """Get or initialize the data store."""
    global _store
    if _store is None:
        _store = ATTACKDataStore(quiet=True)
        _store.load()
    return _store


def get_engine() -> ATTACKQueryEngine:
    """Get or initialize the query engine."""
    global _engine
    if _engine is None:
        store = get_store()
        _engine = ATTACKQueryEngine(store)
    return _engine


def get_parser() -> NLQueryParser:
    """Get or initialize the NL parser."""
    global _parser
    if _parser is None:
        engine = get_engine()
        _parser = NLQueryParser(engine)
    return _parser


def reset_globals() -> None:
    """Reset global instances (for testing)."""
    global _store, _engine, _parser
    _store = None
    _engine = None
    _parser = None


# Create the MCP server
app = Server("attack-query-mcp")

# Import tools and resources to register them with the app
from attack_query_mcp.resources import register_resources  # noqa: E402
from attack_query_mcp.tools import register_tools  # noqa: E402

register_resources(app)
register_tools(app)


def main() -> None:
    """Run the MCP server."""
    import asyncio

    from mcp.server.stdio import stdio_server

    async def run_server() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
