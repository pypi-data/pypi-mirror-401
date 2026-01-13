"""mcp-contract-executor: minimal contract-first MCP server."""

__all__ = ["build_server", "run_server"]

# Package version (fallback if importlib.metadata is unavailable)
try:
    from importlib.metadata import version

    __version__ = version("mcp-contract-executor")
except Exception:  # pragma: no cover
    __version__ = "0.0.0"
