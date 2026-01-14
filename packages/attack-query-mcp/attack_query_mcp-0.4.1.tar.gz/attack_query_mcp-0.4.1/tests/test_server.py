"""Placeholder tests for MCP server."""

from __future__ import annotations


def test_import() -> None:
    """Verify attack-query-mcp can be imported."""
    from attack_query_mcp import __version__

    assert __version__  # Verify version is set


def test_attack_query_dependency() -> None:
    """Verify attack-query dependency is accessible."""
    from attack_query import __version__

    assert __version__  # Just verify it's importable
