"""eng-mcp-suite — engineering MCP catalog and installer."""
from __future__ import annotations

__version__ = "1.3.0"

from eng_mcp_suite.manifest import Manifest, MCPEntry, load_manifest
from eng_mcp_suite.private_manifest import (
    DEFAULT_PRIVATE_PATH,
    load_merged_manifest,
    load_private_manifest,
    merge_manifests,
    resolve_private_path,
)

__all__ = [
    "DEFAULT_PRIVATE_PATH",
    "MCPEntry",
    "Manifest",
    "__version__",
    "load_manifest",
    "load_merged_manifest",
    "load_private_manifest",
    "merge_manifests",
    "resolve_private_path",
]
