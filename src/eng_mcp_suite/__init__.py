"""eng-mcp-suite — engineering MCP catalog and installer."""
from __future__ import annotations

__version__ = "0.2.0"

from eng_mcp_suite.manifest import Manifest, MCPEntry, load_manifest

__all__ = ["__version__", "Manifest", "MCPEntry", "load_manifest"]
