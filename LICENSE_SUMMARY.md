# License summary

Per-MCP license for everything in the public catalog. The
eng-mcp-suite installer/catalog code itself is Apache-2.0; individual
MCP servers are licensed per their own repos.

## Tier 1 — open-source MCPs

| MCP | License | Notes |
|---|---|---|
| [lineforge](https://github.com/RFingAdam/lineforge) | **GPL-3.0** | atlc / atlc2 lineage; the historical GPL chain stays GPL |
| [mcp-emc-regulations](https://github.com/RFingAdam/mcp-emc-regulations) | Apache-2.0 | Original work; permissive |
| [drawio-engineering-mcp](https://github.com/RFingAdam/drawio-engineering-mcp) | Apache-2.0 | Original work |
| [mcp-blender](https://github.com/RFingAdam/mcp-blender) | Apache-2.0 | MCP wrapper code only; Blender itself is GPL but invoked at runtime, not redistributed |
| [mcp-remote-access](https://github.com/RFingAdam/mcp-remote-access) | Apache-2.0 | Original work |
| [mcp-openems](https://github.com/RFingAdam/mcp-openems) | Apache-2.0 (wrapper) | The underlying openEMS engine is **GPL-3.0**; this wrapper invokes the engine at runtime but does not include or redistribute it |
| [mcp-nec2-antenna](https://github.com/RFingAdam/mcp-nec2-antenna) | Apache-2.0 | NEC2 itself is public-domain US-government code |
| [mcp-pcb-emcopilot](https://github.com/RFingAdam/mcp-pcb-emcopilot) | Apache-2.0 | Original work |
| [mcp-ltspice-qucs](https://github.com/RFingAdam/mcp-ltspice-qucs) | Apache-2.0 (wrapper) | LTspice is Analog Devices proprietary (free-as-in-beer); Qucs-S is GPL; scikit-rf is BSD; this wrapper does not include them |

## Tier 2 — commercial / hardware-gated MCPs

| MCP | License | What you need |
|---|---|---|
| [copper-mountain-vna-mcp](https://github.com/RFingAdam/copper-mountain-vna-mcp) | Apache-2.0 | Copper Mountain VNA hardware on the network |
| [mcp-rs-spectrum-analyzer](https://github.com/RFingAdam/mcp-rs-spectrum-analyzer) | Apache-2.0 | R&S FSW / FSVA / FSV / FPL hardware (or Keysight / Rigol equivalent) |
| [mcp-rs-cmw500](https://github.com/RFingAdam/mcp-rs-cmw500) | Apache-2.0 | R&S CMW500 + enabled application licenses (LTE / WLAN / Bluetooth / GPRF) |
| [mcp-rs-siggen](https://github.com/RFingAdam/mcp-rs-siggen) | Apache-2.0 | R&S signal generator hardware + relevant option licenses (K71 for 5G NR, K81 for WLAN, etc.) |
| [mcp-cst-studio](https://github.com/RFingAdam/mcp-cst-studio) | Apache-2.0 (wrapper) | A licensed CST Studio Suite installation (Dassault Systèmes); wrapper currently private until at least one validated end-to-end run is possible |

## Why two licenses?

- **GPL-3.0** for lineforge: it descends from atlc / atlc2 which are
  GPL. Forking that lineage forward keeps it GPL.
- **GPL invocation, not inclusion** for mcp-openems and mcp-blender:
  the underlying GPL tool runs as a separate process when the user
  triggers it. The wrapper code in this catalog does not include or
  redistribute the GPL binary, so the wrapper stays Apache-2.0. If
  you redistribute openEMS or Blender bundled with the wrapper, GPL
  obligations attach to the bundle.
- **Apache-2.0** for everything else: permissive, modern, and the
  default for new original work in this toolkit.

## Contributing

Per-repo `CONTRIBUTING.md` files document each project's specifics.
By submitting a contribution to any repo, you agree the contribution
ships under that repo's existing license.
