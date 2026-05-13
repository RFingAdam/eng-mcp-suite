#!/usr/bin/env python3
"""Audit each engineering MCP repo for shippable / public-release readiness.

For each repo listed in the manifest, checks:
  - README presence + size
  - LICENSE presence
  - tests/ directory presence
  - pyproject.toml or package.json presence
  - Most-recent commit age
  - Latest release tag
  - Open issue count

Outputs a markdown report + sorts entries by "ready to flip public" score.

Usage:
  python scripts/audit_repos.py [--out audit_report.md]
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Add src/ to path so we can import the suite manifest
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from eng_mcp_suite.manifest import MCPEntry, load_manifest  # noqa: E402


def detect_license_family(text: str) -> tuple[str | None, bool]:
    """Identify the license family from LICENSE file content.

    Returns ``(spdx_id_or_None, is_proprietary)``. The boilerplate phrases
    matched here are deliberately conservative — they're the canonical
    opening lines of each license, not partial fragments that could appear
    in other documents.

    The ``is_proprietary`` flag is set when the file is explicitly
    proprietary / all-rights-reserved, distinguishing it from the
    "LICENSE exists but we can't identify it" case.
    """
    if not text:
        return (None, False)

    lower = text.lower()

    # Check for canonical open-license headers FIRST. These match the
    # unambiguous opening text of each license. The proprietary-detection
    # fallback runs only if no open-license header matched, which avoids
    # false positives from preamble text in (e.g.) GPL-3.0 that mentions
    # the word "proprietary" while explaining what the license prevents.
    if "gnu lesser general public license" in lower and "version 3" in lower:
        return ("LGPL-3.0", False)
    if "gnu general public license" in lower and "version 3" in lower:
        return ("GPL-3.0", False)
    if "gnu general public license" in lower and "version 2" in lower:
        return ("GPL-2.0", False)
    if "apache license" in lower and "version 2.0" in lower:
        return ("Apache-2.0", False)
    if "mozilla public license" in lower and "version 2.0" in lower:
        return ("MPL-2.0", False)
    if "permission is hereby granted, free of charge" in lower:
        return ("MIT", False)
    if "redistribution and use in source and binary forms" in lower:
        if "neither the name" in lower:
            return ("BSD-3-Clause", False)
        return ("BSD-2-Clause", False)
    if "the unlicense" in lower or "this is free and unencumbered software" in lower:
        return ("Unlicense", False)

    # Fallback: explicit-proprietary detection. Only reached if no known
    # open-license header matched, so we won't false-positive on GPL
    # preamble text talking about "proprietary".
    if "all rights reserved" in lower and "permission is hereby" not in lower:
        return ("Proprietary", True)
    if "proprietary" in lower and "license" in lower:
        return ("Proprietary", True)

    return (None, False)


@dataclass
class RepoAudit:
    name: str
    status: str
    repo_url: str
    has_readme: bool = False
    readme_chars: int = 0
    has_license: bool = False
    license_spdx: str | None = None
    license_is_proprietary: bool = False
    has_tests: bool = False
    has_pyproject: bool = False
    has_package_json: bool = False
    last_push_days: int = -1
    latest_tag: str | None = None
    open_issues: int = -1
    error: str | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def readiness_score(self) -> int:
        """0-100 score of how close to public-flip ready.

        Public repos automatically score 100 (already there).
        """
        if self.error:
            return 0
        if self.status == "public":
            # Even public repos fail the audit if LICENSE content is
            # proprietary — a documented mismatch we want visible, not
            # masked by the "public ⇒ 100" rule.
            if self.license_is_proprietary:
                return 50
            return 100
        score = 0
        if self.has_readme and self.readme_chars > 200:
            score += 25
        if self.has_license:
            score += 15
        if self.has_tests:
            score += 20
        if self.has_pyproject or self.has_package_json:
            score += 20
        if self.latest_tag:
            score += 10
        if 0 <= self.last_push_days < 90:
            score += 10  # recently active
        return min(score, 99)  # never quite 100 unless public

    @property
    def readiness_label(self) -> str:
        s = self.readiness_score
        if s >= 100:
            return "✅ already public"
        if s >= 80:
            return "🟢 ready to flip"
        if s >= 60:
            return "🟡 needs minor polish"
        if s >= 40:
            return "🟠 needs audit"
        return "🔴 WIP / not ready"


def gh_api_json(path: str) -> dict | None:
    """Run gh api and return parsed JSON, or None on error."""
    try:
        proc = subprocess.run(
            ["gh", "api", path],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if proc.returncode != 0:
            return None
        return json.loads(proc.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def audit_repo(entry: MCPEntry) -> RepoAudit:
    """Audit one repo."""
    a = RepoAudit(
        name=entry.name,
        status=entry.status,
        repo_url=entry.repo,
    )
    # Parse owner/repo from URL
    parts = entry.repo.rstrip("/").split("/")
    if len(parts) < 5:
        a.error = f"can't parse repo URL: {entry.repo}"
        return a
    owner, repo = parts[-2], parts[-1]

    # Basic repo metadata
    info = gh_api_json(f"repos/{owner}/{repo}")
    if not info:
        a.error = "repo not accessible (404 or no permissions)"
        return a

    a.has_license = info.get("license") is not None
    a.open_issues = info.get("open_issues_count", 0)

    # License family — prefer GitHub's SPDX detection, fall back to
    # reading the LICENSE file content and applying heuristics. GitHub
    # returns null/NOASSERTION for proprietary or custom LICENSE files,
    # which is exactly the case content-detection catches.
    gh_lic = info.get("license") or {}
    gh_spdx = gh_lic.get("spdx_id")
    if gh_spdx and gh_spdx not in ("NOASSERTION", ""):
        a.license_spdx = gh_spdx

    license_blob = gh_api_json(f"repos/{owner}/{repo}/contents/LICENSE")
    if license_blob and license_blob.get("content"):
        try:
            text = base64.b64decode(license_blob["content"]).decode("utf-8", errors="replace")
            detected, is_prop = detect_license_family(text)
            a.license_is_proprietary = is_prop
            # Detected content wins over GitHub's classifier when GitHub
            # returned nothing useful or when the content is proprietary.
            if is_prop or not a.license_spdx:
                a.license_spdx = detected or a.license_spdx
            a.has_license = True
        except (ValueError, UnicodeDecodeError):
            pass

    pushed_at = info.get("pushed_at")
    if pushed_at:
        pushed = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        a.last_push_days = (datetime.now(timezone.utc) - pushed).days

    # README — try contents/README.md
    readme = gh_api_json(f"repos/{owner}/{repo}/readme")
    if readme and readme.get("size"):
        a.has_readme = True
        a.readme_chars = readme["size"]

    # Tests directory
    tests = gh_api_json(f"repos/{owner}/{repo}/contents/tests")
    if tests and isinstance(tests, list) and len(tests) > 0:
        a.has_tests = True
    # Alternate: test/ singular
    if not a.has_tests:
        test = gh_api_json(f"repos/{owner}/{repo}/contents/test")
        if test and isinstance(test, list) and len(test) > 0:
            a.has_tests = True

    # pyproject.toml / package.json
    py = gh_api_json(f"repos/{owner}/{repo}/contents/pyproject.toml")
    if py and py.get("name") == "pyproject.toml":
        a.has_pyproject = True
    pkg = gh_api_json(f"repos/{owner}/{repo}/contents/package.json")
    if pkg and pkg.get("name") == "package.json":
        a.has_package_json = True

    # Latest release tag
    releases = gh_api_json(f"repos/{owner}/{repo}/releases/latest")
    if releases and releases.get("tag_name"):
        a.latest_tag = releases["tag_name"]
    else:
        # Try tags as fallback
        tags = gh_api_json(f"repos/{owner}/{repo}/tags?per_page=1")
        if tags and isinstance(tags, list) and len(tags) > 0:
            a.latest_tag = tags[0].get("name")

    # Notes
    if a.last_push_days < 0:
        a.notes.append("no push date")
    elif a.last_push_days > 180:
        a.notes.append(f"stale ({a.last_push_days}d)")
    elif a.last_push_days < 30:
        a.notes.append(f"active ({a.last_push_days}d)")

    if not a.has_readme:
        a.notes.append("no README")
    elif a.readme_chars < 500:
        a.notes.append(f"thin README ({a.readme_chars}B)")

    if not a.has_license:
        if a.status == "public":
            a.notes.append("⚠ no LICENSE on public repo")
        else:
            a.notes.append("no LICENSE")

    # License-content checks
    if a.license_is_proprietary and a.status == "public":
        a.notes.append("⚠ Proprietary LICENSE on public repo")
    elif a.license_is_proprietary:
        a.notes.append("Proprietary LICENSE")
    elif a.has_license and not a.license_spdx:
        a.notes.append("unidentified LICENSE")

    return a


def emit_markdown(audits: list[RepoAudit]) -> str:
    """Render audits as a markdown report."""
    audits_sorted = sorted(
        audits,
        key=lambda a: (-a.readiness_score, a.name),
    )

    lines = ["# Engineering MCP Suite — Repo Audit Report", ""]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"_Generated {now}_")
    lines.append("")
    lines.append("Per-repo readiness for flipping private → public, sorted by score.")
    lines.append("")
    lines.append("| Repo | Status | Score | README | License | Tests | pyproject | Tag | Last push | Notes |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for a in audits_sorted:
        score = f"{a.readiness_score} {a.readiness_label}"
        readme = "✓" if a.has_readme else "✗"
        if not a.has_license:
            license_ = "✗"
        elif a.license_spdx:
            license_ = a.license_spdx
        else:
            license_ = "?"
        tests = "✓" if a.has_tests else "✗"
        pkg = "✓" if (a.has_pyproject or a.has_package_json) else "✗"
        tag = a.latest_tag or "—"
        push = f"{a.last_push_days}d ago" if a.last_push_days >= 0 else "?"
        notes = "; ".join(a.notes) if a.notes else ""
        if a.error:
            notes = f"❌ {a.error}"
        lines.append(
            f"| {a.name} | {a.status} | {score} | {readme} | {license_} | "
            f"{tests} | {pkg} | {tag} | {push} | {notes} |"
        )
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("- ✅ **already public** (score 100): live to the world")
    lines.append("- 🟢 **ready to flip** (≥80): has README, tests, pyproject, recent activity — needs only the visibility switch")
    lines.append("- 🟡 **needs minor polish** (60-79): missing one or two of the above")
    lines.append("- 🟠 **needs audit** (40-59): substantial gaps in docs/tests/packaging")
    lines.append("- 🔴 **WIP / not ready** (<40): early stage or needs significant work")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Write report to this file (default: stdout)",
    )
    args = parser.parse_args()

    mf = load_manifest()
    print(f"Auditing {len(mf.mcps)} repos...", file=sys.stderr)

    audits = []
    for entry in mf.mcps:
        print(f"  {entry.name}...", file=sys.stderr, end=" ", flush=True)
        a = audit_repo(entry)
        audits.append(a)
        print(f"score={a.readiness_score} ({a.readiness_label})", file=sys.stderr)

    report = emit_markdown(audits)

    if args.out:
        args.out.write_text(report)
        print(f"\nWrote {args.out}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
