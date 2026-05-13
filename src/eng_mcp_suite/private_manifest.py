"""User-local private manifest extension.

The eng-mcp-suite catalog ships only public + commercial/hardware-gated
MCPs. Users who have access to private MCPs (their own org-internal tools,
licensed bolt-ons, etc.) can add them via a local manifest file:

    ~/.config/eng-mcp-suite/private.yaml

The schema is identical to the bundled ``manifest.yaml``. At runtime the
suite merges both, exposing the local additions only when the user opts
in with ``--include private``.

This module never names specific private MCPs — it only describes the
mechanism. The example file (in docs/private.yaml.example) uses generic
placeholder names so the documentation never inadvertently references
real internal tools.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from eng_mcp_suite.manifest import Manifest


DEFAULT_PRIVATE_PATH = Path.home() / ".config" / "eng_mcp_suite" / "private.yaml"


def resolve_private_path(override: Path | str | None = None) -> Path:
    """Return the path to the user's private manifest.

    Resolution order:
      1. ``override`` argument (if given)
      2. ``ENG_MCP_SUITE_PRIVATE_MANIFEST`` env var
      3. ``~/.config/eng_mcp_suite/private.yaml`` (default)
    """
    if override is not None:
        return Path(override)
    env = os.environ.get("ENG_MCP_SUITE_PRIVATE_MANIFEST")
    if env:
        return Path(env)
    return DEFAULT_PRIVATE_PATH


def load_private_manifest(path: Path | str | None = None) -> Manifest:
    """Load the user-local private manifest.

    Returns an empty :class:`Manifest` if the file does not exist or is
    empty. Raises if the file is malformed.
    """
    p = resolve_private_path(path)
    if not p.exists():
        return Manifest(mcps=[])
    with p.open("r") as f:
        data = yaml.safe_load(f)
    if not data:
        return Manifest(mcps=[])
    return Manifest.model_validate(data)


def merge_manifests(public: Manifest, private: Manifest) -> Manifest:
    """Merge public + private manifests.

    Private entries override public on name collision (so a local override
    of an upstream entry — e.g. pinning a specific version — works).
    """
    by_name: dict[str, object] = {entry.name: entry for entry in public.mcps}
    for entry in private.mcps:
        by_name[entry.name] = entry
    return Manifest(mcps=list(by_name.values()))


def load_merged_manifest(
    *,
    include_private: bool = False,
    private_path: Path | str | None = None,
) -> Manifest:
    """Load the public manifest, optionally merging in the local private file.

    Parameters
    ----------
    include_private
        If True, also load and merge ``~/.config/eng_mcp_suite/private.yaml``
        (or the path resolved per :func:`resolve_private_path`).
    private_path
        Override for the private-manifest file location.
    """
    from eng_mcp_suite.manifest import load_manifest

    public = load_manifest()
    if not include_private:
        return public
    private = load_private_manifest(private_path)
    return merge_manifests(public, private)


__all__ = [
    "DEFAULT_PRIVATE_PATH",
    "load_merged_manifest",
    "load_private_manifest",
    "merge_manifests",
    "resolve_private_path",
]
