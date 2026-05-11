"""Tests for manifest loading and queries."""
from __future__ import annotations

import pytest

from eng_mcp_suite.manifest import WORKFLOWS, load_manifest


def test_manifest_loads():
    mf = load_manifest()
    assert len(mf.mcps) > 0


def test_manifest_has_lineforge():
    mf = load_manifest()
    e = mf.by_name("lineforge")
    assert e is not None
    assert "rf" in e.categories
    assert e.install.method == "pip"
    assert e.install.package == "lineforge"


def test_manifest_by_status():
    mf = load_manifest()
    public = mf.public()
    assert len(public) > 0
    assert all(e.status == "public" for e in public)


def test_manifest_by_category():
    mf = load_manifest()
    rf = mf.by_category("rf")
    assert len(rf) > 0
    assert all("rf" in e.categories for e in rf)


@pytest.mark.parametrize("workflow_name", list(WORKFLOWS.keys()))
def test_workflow_members_exist(workflow_name):
    """Every name listed in a workflow must exist in the manifest."""
    mf = load_manifest()
    for member_name in WORKFLOWS[workflow_name]:
        assert mf.by_name(member_name) is not None, (
            f"workflow '{workflow_name}' references unknown MCP '{member_name}'"
        )


def test_all_entries_have_install_method():
    """Every entry must have a valid install method."""
    mf = load_manifest()
    valid_methods = {"pip", "pipx", "npm", "git", "manual"}
    for e in mf.mcps:
        assert e.install.method in valid_methods, (
            f"{e.name}: install.method='{e.install.method}' not in {valid_methods}"
        )


def test_public_entries_are_installable():
    """Public entries with non-manual install methods are claimed installable."""
    mf = load_manifest()
    for e in mf.public():
        if e.install.method != "manual":
            assert e.is_installable
