"""Install machinery — runs pip / pipx / npm based on manifest entry."""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

from eng_mcp_suite.manifest import MCPEntry


@dataclass
class InstallResult:
    name: str
    success: bool
    message: str
    method: str
    package: str | None = None


def install_entry(entry: MCPEntry, dry_run: bool = False) -> InstallResult:
    """Install a single MCP entry. Returns InstallResult."""
    method = entry.install.method
    pkg = entry.install.package

    if method == "manual":
        return InstallResult(
            name=entry.name,
            success=False,
            message=f"manual install required: {entry.install.install_notes}",
            method=method,
        )

    if entry.status != "public" and method == "pip":
        # Can't pip-install a private package
        return InstallResult(
            name=entry.name,
            success=False,
            message=f"{entry.name} is not public — skipping (status={entry.status})",
            method=method,
        )

    if method == "pip":
        cmd = ["pip", "install", pkg]
    elif method == "pipx":
        if not shutil.which("pipx"):
            return InstallResult(
                name=entry.name,
                success=False,
                message="pipx not found on PATH — `python -m pip install pipx` then `pipx ensurepath`",
                method=method,
                package=pkg,
            )
        cmd = ["pipx", "install", pkg]
    elif method == "npm":
        if not shutil.which("npm"):
            return InstallResult(
                name=entry.name,
                success=False,
                message="npm not found on PATH",
                method=method,
                package=pkg,
            )
        cmd = ["npm", "install", "-g", pkg]
    elif method == "git":
        cmd = ["pip", "install", pkg]
    else:
        return InstallResult(
            name=entry.name,
            success=False,
            message=f"unknown install method '{method}'",
            method=method,
        )

    if dry_run:
        return InstallResult(
            name=entry.name,
            success=True,
            message=f"DRY RUN: would run `{' '.join(cmd)}`",
            method=method,
            package=pkg,
        )

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        return InstallResult(
            name=entry.name,
            success=True,
            message=f"installed via {method}: {pkg}",
            method=method,
            package=pkg,
        )
    else:
        return InstallResult(
            name=entry.name,
            success=False,
            message=f"failed: {proc.stderr.strip()[:200]}",
            method=method,
            package=pkg,
        )


def generate_claude_desktop_config(entries: list[MCPEntry]) -> dict:
    """Generate a Claude Desktop `mcpServers` config snippet for the given MCPs.

    Returns a dict with `mcpServers` key matching Claude Desktop's expected format.
    Users merge this into their existing claude_desktop_config.json.
    """
    servers = {}
    for e in entries:
        # Convention: server is launched via its console_script (which exists if
        # the MCP is pip-installed) or via npx if npm-installed.
        if e.install.method in ("pip", "pipx", "git"):
            servers[e.server_name] = {
                "command": e.server_name,
                # Most servers expose themselves as the same name as their
                # console script; override per-server if not.
            }
        elif e.install.method == "npm":
            servers[e.server_name] = {
                "command": "npx",
                "args": ["-y", e.install.package],
            }
        else:
            # Manual install — record placeholder
            servers[e.server_name] = {
                "command": "<configure-manually>",
                "comment": e.install.install_notes or "see repo README",
            }
    return {"mcpServers": servers}
