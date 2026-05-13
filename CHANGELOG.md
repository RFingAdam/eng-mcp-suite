# Changelog

All notable changes to **eng-mcp-suite** are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-05-13

The 1.0 release is the **public-launch milestone** of the engineering
MCP toolkit. All Tier 1 MCPs in the catalog are public, polished to the
90+ audit-gate bar, and tagged with a release. Tier 2 (commercial /
hardware-gated) wrappers are public source with prominent hardware /
license requirement notices.

### Catalog (15 entries, all polish-gate cleared)

Tier 1 (public open-source):
- lineforge (RF transmission lines, 2.1.0)
- mcp-emc-regulations (EMC standards lookup)
- drawio-engineering-mcp (diagrams)
- mcp-blender (3D modeling, 0.3.0)
- mcp-remote-access (SSH + serial)
- mcp-openems (FDTD wrapper, **flipped public in this release**, 0.1.0)
- mcp-nec2-antenna (wire antennas, 0.1.0)
- mcp-pcb-emcopilot (PCB review, 0.2.0)
- mcp-ltspice-qucs (LTspice / Qucs-S / scikit-rf, 0.3.0)

Tier 2 (public wrapper, license / hardware required):
- copper-mountain-vna-mcp (0.2.0)
- mcp-rs-spectrum-analyzer (0.2.0)
- mcp-rs-cmw500 (0.2.0)
- mcp-rs-siggen (0.1.0)
- mcp-cst-studio (private until validated, kept in catalog as commercial)

### Added
- `LICENSE_SUMMARY.md` — per-MCP license table covering the full Tier 1 +
  Tier 2 catalog, with notes on why each was licensed the way it was.
- Versioned `CHANGELOG.md` (this file).

### Changed
- Manifest entry for `mcp-openems` moved from `private` → `public` after
  the polish work in mcp-openems v0.1.0 (README rewrite, brand alignment,
  CHANGELOG, runnable example, smoke tests).
- README cross-links updated; status badges reflect current visibility.
- AUDIT.md regenerated against the 15-entry catalog — 13 / 15 at 100;
  the two at 90 (mcp-rf-test, mcp-cst-studio) stay private intentionally
  pending org/license access.

### Strategic
- Established the **no-leak rule** for the public catalog: any
  org-internal, proprietary, or superseded-WIP MCPs are kept entirely
  out of the public manifest, README, AUDIT, and bolt-on documentation.
  The private bolt-on mechanism (v0.3.0) lets users with access add
  their own private entries locally, without ever naming them publicly.
- Confirmed `mcp-rf-test` stays private (LICENSE is proprietary).
- Confirmed `hfss-agent` is out of the public catalog until an HFSS
  license is available to validate the wrapper end-to-end.

## [0.3.0] — 2026-05-12

### Added
- Private bolt-on mechanism — `private_manifest.py`, `--include-private`
  and `--private-manifest` CLI flags, `docs/PRIVATE_BOLT_ON.md`,
  generic-placeholder `docs/private.yaml.example`. See the
  [v0.3.0 release notes](https://github.com/RFingAdam/eng-mcp-suite/releases/tag/v0.3.0)
  for the mechanism details.

## [0.2.0]

### Added
- `eng-mcp-suite install` CLI that reads the manifest, installs MCPs,
  and generates a Claude Desktop config snippet.
- `scripts/audit_repos.py` — per-MCP audit (README, LICENSE, tests,
  pyproject, release tag, push activity).

## [0.1.0]

### Added
- Catalog manifest + initial README scaffolding for the engineering
  MCP toolkit.
