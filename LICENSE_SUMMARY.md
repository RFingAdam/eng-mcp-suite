# License summary

The engineering MCP toolkit is licensed under **AGPL-3.0-or-later**
across the board — for every public MCP, this catalog, and lineforge.

## Why AGPL

The toolkit's intent is straightforward: **share back, don't freeload**.
We want contributions to flow upstream, and we want to keep people from
wrapping the work in a closed-source paid SaaS while contributing
nothing. The AGPL is the OSI-approved license that maps to that intent.

- **GPL-3.0** (which lineforge previously used) extends copyleft to
  distribution but leaves the SaaS exit open: someone can host your
  code as a service without releasing changes.
- **AGPL-3.0** closes the SaaS exit. Network use also triggers the
  share-back requirement (§13). This is the same license MongoDB,
  Grafana, MinIO, Mastodon, and Sentry chose for the same reason.
- **Apache-2.0** (which most wrappers previously used) is permissive
  and explicitly allows closed-source forks. It maximizes adoption
  but gives no protection against value extraction.

The trade-off is real: AGPL is banned at Google, Amazon, Apple, and
many large enterprises. That's the cost we accept in exchange for the
protection. The user we're optimizing for is the working RF / EE
engineer who'll find the toolkit, use it, contribute improvements
back, and share with peers — not the BigCo legal team gating
permissive-license-only dependencies.

## Per-MCP licenses

| Repo | License | Underlying tool (separate) |
|---|---|---|
| [lineforge](https://github.com/RFingAdam/lineforge) | AGPL-3.0-or-later | (none — original work, atlc / atlc2 lineage was already GPL-3.0) |
| [eng-mcp-suite](https://github.com/RFingAdam/eng-mcp-suite) (this repo) | AGPL-3.0-or-later | (none — catalog + installer) |
| [mcp-emc-regulations](https://github.com/RFingAdam/mcp-emc-regulations) | AGPL-3.0-or-later | (none — original data + tools) |
| [drawio-engineering-mcp](https://github.com/RFingAdam/drawio-engineering-mcp) | AGPL-3.0-or-later | upstream draw.io MCP foundation is Apache-2.0; engineering extensions are AGPL |
| [mcp-blender](https://github.com/RFingAdam/mcp-blender) | AGPL-3.0-or-later | Blender (GPL-3.0+), invoked at runtime, not bundled |
| [mcp-remote-access](https://github.com/RFingAdam/mcp-remote-access) | AGPL-3.0-or-later | (none — original work) |
| [mcp-openems](https://github.com/RFingAdam/mcp-openems) | AGPL-3.0-or-later | openEMS engine (GPL-3.0), invoked at runtime |
| [mcp-nec2-antenna](https://github.com/RFingAdam/mcp-nec2-antenna) | AGPL-3.0-or-later | NEC2 (public-domain US-government code), invoked at runtime |
| [mcp-pcb-emcopilot](https://github.com/RFingAdam/mcp-pcb-emcopilot) | AGPL-3.0-or-later | (none — original work) |
| [mcp-ltspice-qucs](https://github.com/RFingAdam/mcp-ltspice-qucs) | AGPL-3.0-or-later (all 4 workspace packages) | LTspice (proprietary, Analog Devices), Qucs-S (GPL), scikit-rf (BSD) — all invoked at runtime |
| [copper-mountain-vna-mcp](https://github.com/RFingAdam/copper-mountain-vna-mcp) | AGPL-3.0-or-later | Copper Mountain VNA hardware (commercial), SCPI driver |
| [mcp-rs-spectrum-analyzer](https://github.com/RFingAdam/mcp-rs-spectrum-analyzer) | AGPL-3.0-or-later | R&S analyzer hardware (FSW / FSVA / FSV / FPL), SCPI driver |
| [mcp-rs-cmw500](https://github.com/RFingAdam/mcp-rs-cmw500) | AGPL-3.0-or-later | R&S CMW500 hardware + application licenses |
| [mcp-rs-siggen](https://github.com/RFingAdam/mcp-rs-siggen) | AGPL-3.0-or-later | R&S signal-generator hardware + option licenses |
| [mcp-cst-studio](https://github.com/RFingAdam/mcp-cst-studio) | AGPL-3.0-or-later | CST Studio Suite (Dassault Systèmes commercial license) |

## What AGPL means for you as a user

- **Run it locally?** No copyleft obligations beyond keeping the
  LICENSE file with the code. Use it freely.
- **Wrap it in a script and run it on your own bench?** Same — no
  obligations.
- **Modify it for your own internal use?** Same.
- **Distribute the modified code, or host it as a service for other
  users to query over a network?** Then you must make your
  modifications available under AGPL-3.0-or-later. This is the
  "share-back" requirement that prevents the closed-source SaaS
  workaround.

## What AGPL means for the underlying tools

The wrappers in this toolkit invoke external tools at runtime
(openEMS, NEC2, Blender, LTspice, Qucs-S, scikit-rf, CST, R&S
firmware, etc.). The wrappers don't bundle or redistribute those
tools, so the wrappers' AGPL license is independent of whatever
license the underlying tool ships under. If you bundle one of the
underlying tools alongside the wrapper for distribution, you'll
need to follow that tool's redistribution requirements separately.

## Relicensing history

The catalog was originally a mix:

- `lineforge`: GPL-3.0 (from atlc / atlc2 lineage)
- Everything else: Apache-2.0, with one MIT (`mcp-blender`)

In May 2026 the toolkit moved to AGPL-3.0-or-later across the board.
GPL-3.0 → AGPL-3.0 is explicitly permitted by GPL-3.0 §13. Existing
permissively-licensed forks remain valid under their original terms;
the relicense applies to future commits and tagged releases from the
upstream repos.

## Contributing

By submitting a contribution to any toolkit repo, you agree the
contribution ships under AGPL-3.0-or-later — the same license as the
rest of the repo. No CLA is required at this scale, but the project
may add a DCO ("signed-off-by") requirement as contributor count
grows.
