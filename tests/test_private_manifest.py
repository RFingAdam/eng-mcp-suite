"""Tests for the user-local private manifest extension."""
from __future__ import annotations

from textwrap import dedent

from eng_mcp_suite.manifest import Manifest
from eng_mcp_suite.private_manifest import (
    DEFAULT_PRIVATE_PATH,
    load_merged_manifest,
    load_private_manifest,
    merge_manifests,
    resolve_private_path,
)


class TestResolvePrivatePath:
    def test_default_when_nothing_set(self, monkeypatch):
        monkeypatch.delenv("ENG_MCP_SUITE_PRIVATE_MANIFEST", raising=False)
        assert resolve_private_path() == DEFAULT_PRIVATE_PATH

    def test_env_var_override(self, monkeypatch, tmp_path):
        target = tmp_path / "custom.yaml"
        monkeypatch.setenv("ENG_MCP_SUITE_PRIVATE_MANIFEST", str(target))
        assert resolve_private_path() == target

    def test_explicit_arg_wins_over_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("ENG_MCP_SUITE_PRIVATE_MANIFEST", str(tmp_path / "env.yaml"))
        explicit = tmp_path / "explicit.yaml"
        assert resolve_private_path(explicit) == explicit


class TestLoadPrivateManifest:
    def test_missing_file_returns_empty(self, tmp_path):
        result = load_private_manifest(tmp_path / "nope.yaml")
        assert isinstance(result, Manifest)
        assert result.mcps == []

    def test_empty_file_returns_empty(self, tmp_path):
        p = tmp_path / "empty.yaml"
        p.write_text("")
        result = load_private_manifest(p)
        assert result.mcps == []

    def test_loads_valid_yaml(self, tmp_path):
        p = tmp_path / "private.yaml"
        p.write_text(dedent("""
            mcps:
              - name: my-internal-tool
                description: Custom widget API
                categories: [lab-test]
                repo: https://internal.example.com/widget
                status: private
                install:
                  method: git
                  package: git+ssh://git@internal.example.com/widget.git
                server_name: widget
        """).strip())
        result = load_private_manifest(p)
        assert len(result.mcps) == 1
        assert result.mcps[0].name == "my-internal-tool"


class TestMergeManifests:
    def test_merge_disjoint(self):
        from eng_mcp_suite.manifest import MCPEntry, MCPInstall

        def _e(name: str) -> MCPEntry:
            return MCPEntry(
                name=name,
                description=f"desc for {name}",
                categories=["rf"],
                repo=f"https://example.com/{name}",
                status="public",
                install=MCPInstall(method="pip", package=name),
                server_name=name,
            )

        public = Manifest(mcps=[_e("a"), _e("b")])
        private = Manifest(mcps=[_e("c")])
        merged = merge_manifests(public, private)
        names = {e.name for e in merged.mcps}
        assert names == {"a", "b", "c"}

    def test_private_overrides_public_on_collision(self):
        from eng_mcp_suite.manifest import MCPEntry, MCPInstall

        public_entry = MCPEntry(
            name="shared",
            description="public version",
            categories=["rf"],
            repo="https://public",
            status="public",
            install=MCPInstall(method="pip", package="shared"),
            server_name="shared",
        )
        private_entry = MCPEntry(
            name="shared",
            description="private override",
            categories=["rf"],
            repo="https://private",
            status="private",
            install=MCPInstall(method="git", package="git+ssh://..."),
            server_name="shared",
        )
        merged = merge_manifests(
            Manifest(mcps=[public_entry]),
            Manifest(mcps=[private_entry]),
        )
        assert len(merged.mcps) == 1
        assert merged.mcps[0].description == "private override"
        assert merged.mcps[0].repo == "https://private"


class TestLoadMergedManifest:
    def test_public_only_by_default(self, tmp_path, monkeypatch):
        """Without --include-private, only public manifest is returned."""
        # Point at a non-existent private file just to be safe
        monkeypatch.setenv("ENG_MCP_SUITE_PRIVATE_MANIFEST", str(tmp_path / "nope.yaml"))
        public = load_merged_manifest(include_private=False)
        # Should equal load_manifest() exactly
        from eng_mcp_suite.manifest import load_manifest
        bundled = load_manifest()
        assert len(public.mcps) == len(bundled.mcps)

    def test_include_private_merges(self, tmp_path, monkeypatch):
        p = tmp_path / "private.yaml"
        p.write_text(dedent("""
            mcps:
              - name: zzz-private-only
                description: Only in private manifest
                categories: [lab-test]
                repo: https://internal.example/zzz
                status: private
                install:
                  method: git
                  package: git+ssh://internal.example/zzz.git
                server_name: zzz
        """).strip())
        monkeypatch.setenv("ENG_MCP_SUITE_PRIVATE_MANIFEST", str(p))
        merged = load_merged_manifest(include_private=True)
        assert any(e.name == "zzz-private-only" for e in merged.mcps)

    def test_include_private_with_no_file(self, tmp_path, monkeypatch):
        """--include-private with no private file just returns public."""
        monkeypatch.setenv("ENG_MCP_SUITE_PRIVATE_MANIFEST", str(tmp_path / "nope.yaml"))
        from eng_mcp_suite.manifest import load_manifest
        public = load_manifest()
        merged = load_merged_manifest(include_private=True)
        assert len(merged.mcps) == len(public.mcps)
