# eng-mcp-suite

**An all-inclusive engineering MCP catalog for RF / EMC / PCB / SI / lab-test.**

A single installer that lets you bring up a Claude Desktop / Claude Code
environment with every engineering MCP server you need — pre-configured,
namespaced, and grouped by workflow.

## What's included

This suite catalogs **15 engineering MCP servers** across the simulation,
analysis, and lab-test stack.

| Category | MCP server | Status | What it does |
|---|---|---|---|
| **RF / Transmission lines** | `lineforge` | 🟢 public | Z₀, εeff, L, C, Rs, Gp for any 2D cross-section. Closed-form + bitmap. atlc2-compatible. |
| **EM simulation** | `mcp-openems` | 🟢 public | 3D FDTD via openEMS — antennas, transmission lines, vias |
| | `mcp-nec2-antenna` | 🟢 public | Wire-antenna method-of-moments |
| | `mcp-cst-studio` | 🟢 public | CST Studio Suite wrapper (170 tools; CST license required at runtime) |
| **PCB / SI** | `mcp-pcb-emcopilot` | 🟢 public | Layout review, return paths, decoupling, DDR/PCIe/USB SI, multi-market intake, schematic / layout / BOM 3-way cross-ref, KiCad parser |
| **Circuit simulation** | `mcp-ltspice-qucs` | 🟢 public | LTspice + Qucs-S + scikit-rf, all Touchstone-aware |
| **EMC regulatory** | `mcp-emc-regulations` | 🟢 public | FCC, CISPR, IEC, ISO, automotive OEM, medical EMC lookup |
| **Diagrams / docs** | `drawio-engineering-mcp` | 🟢 public | RF block diagrams, PCB stack-ups, EMC test setups |
| **3D modeling** | `mcp-blender` | 🟢 public | 218 tools for 3D, MSFS content, physics, rendering |
| **Remote access** | `mcp-remote-access` | 🟢 public | SSH + serial-port control for embedded devices |
| **Lab test gear** | `copper-mountain-vna-mcp` | 🟢 public | Copper Mountain VNA (S-params, calibration, sweeps) |
| | `mcp-rf-test` | 🔒 private | Wi-Fi / BLE / HaLow / LTE / LoRa compliance test automation |
| | `mcp-rs-spectrum-analyzer` | 🔧 hardware | R&S FSW / FSVA / FSV / FPL spectrum analyzers |
| | `mcp-rs-cmw500` | 🔧 hardware | R&S CMW500 comms tester |
| | `mcp-rs-siggen` | 🔧 hardware | R&S signal generators (SMW, SMBV, SGT, etc.) |

🟢 public = installable by anyone today
🔒 private = internal/access-restricted (not installable from public PyPI)
💼 commercial = requires commercial-software licenses
🔧 hardware = requires specific lab equipment

## Related tools (outside the MCP catalog)

Standalone engineering apps from the same author that aren't MCPs but
slot alongside the suite for the same workflows:

| Tool | What it does |
|---|---|
| [**RFlect**](https://github.com/RFingAdam/RFlect) | Antenna visualization GUI — chamber measurements, VNA S-parameters, 2D/3D gain patterns, efficiency, TRP, group delay, S11/VSWR. Pairs with `copper-mountain-vna-mcp` and `mcp-nec2-antenna` outputs. |

## Quick start (public starter pack)

```bash
# Install the suite CLI straight from GitHub (PyPI packaging planned)
pipx install git+https://github.com/RFingAdam/eng-mcp-suite.git
eng-mcp-suite install --workflow rf-design

# Or pick a workflow bundle
eng-mcp-suite install --workflow emc-compliance   # emc-regulations + drawio + remote-access
eng-mcp-suite install --workflow pcb-review       # lineforge + drawio + (pcb-emcopilot when public)
eng-mcp-suite install --workflow lab-automation   # vna + remote-access + (rs-* when hardware available)
```

`eng-mcp-suite` generates a merged `claude_desktop_config.json` snippet
that wires every installed MCP into one running Claude Desktop instance.

## Workflows

These are curated bundles for common engineering tasks. Each bundle is a
list of MCPs from the manifest that work well together.

### `rf-design`
For designing RF circuits and antennas.
- `lineforge` — transmission lines
- `mcp-openems` — 3D EM validation
- `mcp-nec2-antenna` — wire antennas
- `mcp-ltspice-qucs` — circuit + RF system simulation
- `mcp-emc-regulations` — frequency-band lookups

### `emc-compliance`
For EMC certification work.
- `mcp-emc-regulations` — FCC / CISPR / IEC / ISO limit lookups
- `drawio-engineering-mcp` — test-setup diagrams
- `mcp-rs-spectrum-analyzer` — emissions measurement (if you have R&S gear)
- `mcp-pcb-emcopilot` — predictive layout review

### `pcb-review`
For PCB design review with EMC/SI focus.
- `lineforge` — Z₀ and tolerance windows
- `mcp-pcb-emcopilot` — return paths, decoupling, plane resonances
- `drawio-engineering-mcp` — stack-up diagrams

### `lab-automation`
For test bench automation.
- `copper-mountain-vna-mcp` — VNA control
- `mcp-rs-spectrum-analyzer` — spectrum analyzer (if hardware)
- `mcp-rs-siggen` — signal generators (if hardware)
- `mcp-rf-test` — embedded device compliance
- `mcp-remote-access` — SSH + serial to DUTs

## How the MCPs tie together

These aren't competing tools — they're **layers of the same stack**:

```
        ┌─────────────────────────────────────┐
        │   AI agent (Claude Code / Desktop)  │
        └──────┬──────────────┬───────────────┘
               │              │ via MCP
       ┌───────▼──────┐ ┌─────▼──────┐
       │  lineforge   │ │  pcb-em…   │     ← fast inner loop:
       │   (2D TEM)   │ │ (PCB/EMC)  │       closed-form + analysis
       └───────┬──────┘ └────────────┘
               │ Touchstone (.s2p)
       ┌───────▼──────────────────────┐
       │  openEMS / NEC2 / HFSS / CST │     ← 3D EM validation
       │  (full-wave)                 │       where closed-form runs out
       └──────────────────────────────┘
               │
       ┌───────▼──────────────────────┐
       │  LTspice / Qucs-S / scikit-rf│     ← system-level circuit
       │  (network-level)             │       integration
       └──────────────────────────────┘
               │
       ┌───────▼──────────────────────┐
       │  VNA / SA / Sig-gen / rf-test│     ← physical measurement
       │  (lab hardware)              │       closes the loop
       └──────────────────────────────┘
```

The lineforge L3 SIG1 case study
([`examples/09_l3_sig1_em_validation/`](https://github.com/RFingAdam/lineforge/tree/main/examples/09_l3_sig1_em_validation))
is exactly this pattern: closed-form lineforge ↔ openEMS FDTD cross-validation
on a real RF design point.

## Status

Current version: **v1.3.0**. All 15 catalog entries are public-readiness
score 100 except the intentionally-private `mcp-rf-test`. The
[manifest](src/eng_mcp_suite/data/manifest.yaml) is the source of truth
for what the suite knows about. Use `eng-mcp-suite list` to see all
catalog entries and their status.

### Roadmap

- [x] v0.1: catalog manifest + README
- [x] v0.2: `eng-mcp-suite install` CLI + per-MCP audit script
- [x] v0.3: private bolt-on mechanism — see [docs/PRIVATE_BOLT_ON.md](docs/PRIVATE_BOLT_ON.md)
- [x] v1.0: all Tier 1 public MCPs at 90+ polish score, public launch
- [x] v1.1: toolkit-wide relicense to AGPL-3.0-or-later
- [x] v1.2: `mcp-cst-studio` public
- [x] v1.3: git-based install for every catalog entry + CI
- [ ] future: publish `eng-mcp-suite` and the public MCPs to PyPI for `pipx install eng-mcp-suite`

## License

[AGPL-3.0-or-later](LICENSE) — for this catalog/installer and every
public MCP in the toolkit. See [`LICENSE_SUMMARY.md`](LICENSE_SUMMARY.md)
for the per-repo table and the rationale (share back, don't freeload).
