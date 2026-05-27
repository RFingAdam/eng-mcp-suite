"""Manifest model — parses manifest.yaml into Pydantic objects."""
from __future__ import annotations

from importlib import resources
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class MCPInstall(BaseModel):
    method: str  # pip | pipx | npm | git | manual
    package: str | None = None
    install_notes: str | None = None


class MCPEntry(BaseModel):
    name: str
    description: str
    categories: list[str]
    repo: str
    status: str  # public | private | commercial | hardware
    install: MCPInstall
    server_name: str
    docs: str | None = None
    min_version: str | None = None

    @property
    def is_installable(self) -> bool:
        """True if the entry can be installed by anyone right now."""
        return self.status == "public" and self.install.method != "manual"


class Manifest(BaseModel):
    mcps: list[MCPEntry] = Field(default_factory=list)

    def by_name(self, name: str) -> MCPEntry | None:
        for m in self.mcps:
            if m.name == name:
                return m
        return None

    def by_category(self, category: str) -> list[MCPEntry]:
        return [m for m in self.mcps if category in m.categories]

    def by_status(self, status: str) -> list[MCPEntry]:
        return [m for m in self.mcps if m.status == status]

    def public(self) -> list[MCPEntry]:
        return self.by_status("public")


# Workflow bundles — name -> list of MCP names in install order
WORKFLOWS: dict[str, list[str]] = {
    "rf-design": [
        "lineforge",
        "mcp-openems",
        "mcp-nec2-antenna",
        "mcp-ltspice-qucs",
        "mcp-emc-regulations",
    ],
    "emc-compliance": [
        "mcp-emc-regulations",
        "drawio-engineering-mcp",
        "mcp-pcb-emcopilot",
        "mcp-rs-spectrum-analyzer",
    ],
    "pcb-review": [
        "lineforge",
        "mcp-pcb-emcopilot",
        "drawio-engineering-mcp",
    ],
    "lab-automation": [
        "copper-mountain-vna-mcp",
        "mcp-rs-spectrum-analyzer",
        "mcp-rs-siggen",
        "mcp-rf-test",
        "mcp-remote-access",
    ],
    "starter-public": [
        "lineforge",
        "mcp-emc-regulations",
        "drawio-engineering-mcp",
        "mcp-blender",
        "mcp-remote-access",
        "copper-mountain-vna-mcp",
    ],
}


def load_manifest(path: Path | str | None = None) -> Manifest:
    """Load the manifest.

    If `path` is None, loads the vendored manifest from package data.
    """
    if path is None:
        with resources.files("eng_mcp_suite.data").joinpath("manifest.yaml").open() as f:
            data = yaml.safe_load(f)
    else:
        with open(path) as f:
            data = yaml.safe_load(f)
    return Manifest.model_validate(data)
