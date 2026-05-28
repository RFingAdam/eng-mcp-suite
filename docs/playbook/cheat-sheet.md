# Engineering MCP toolkit — cheat sheet

One page. Keep it open while you work.

## Install

```bash
pipx install git+https://github.com/RFingAdam/eng-mcp-suite.git

eng-mcp-suite list                          # see the catalog
eng-mcp-suite install --workflow rf-design  # install a bundle
eng-mcp-suite config  --workflow rf-design --out claude_desktop_config.json
```

Merge the generated snippet into your existing Claude config:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/claude/claude_desktop_config.json`

## Workflows

| Workflow | Includes |
|---|---|
| `rf-design` | lineforge, mcp-openems, mcp-nec2-antenna, mcp-ltspice-qucs, mcp-emc-regulations |
| `emc-compliance` | mcp-emc-regulations, drawio-engineering-mcp, mcp-rs-spectrum-analyzer, mcp-pcb-emcopilot |
| `pcb-review` | lineforge, mcp-pcb-emcopilot, drawio-engineering-mcp |
| `lab-automation` | copper-mountain-vna-mcp, mcp-rs-spectrum-analyzer, mcp-rs-siggen, mcp-remote-access |

## Catalog at a glance

```
RF / TX lines        →  lineforge
PCB / SI / EMC       →  mcp-pcb-emcopilot
3D EM (FDTD)         →  mcp-openems
Wire antennas (MoM)  →  mcp-nec2-antenna
Circuit + RF sys     →  mcp-ltspice-qucs
EMC regulatory       →  mcp-emc-regulations
Diagrams / docs      →  drawio-engineering-mcp
3D modeling          →  mcp-blender
Remote / SSH         →  mcp-remote-access
VNA                  →  copper-mountain-vna-mcp
Spectrum analyzer    →  mcp-rs-spectrum-analyzer
Comms tester         →  mcp-rs-cmw500          (hardware)
Signal generators    →  mcp-rs-siggen          (hardware)
```

## Pick the right inner / outer loop

| Question | Inner loop | Outer loop |
|---|---|---|
| What's my Z₀? | lineforge | mcp-openems |
| Does this layout pass CISPR-25? | mcp-pcb-emcopilot | (chamber) |
| What's my antenna pattern? | mcp-nec2-antenna | mcp-openems |
| What's my filter response? | mcp-ltspice-qucs | VNA |
| Does this 50-Ω trace actually measure 50 Ω? | lineforge | VNA |

Rule of thumb: **closed-form first**, full-wave for validation,
measurement for ground truth.

## Common prompts

```text
"Design a 50-Ω microstrip for 2.4 GHz on 32-mil FR4."
"What's the VSWR ≤ 2:1 bandwidth of a half-wave dipole at 435 MHz?"
"Run a CISPR-25 Class 5 pre-compliance scan on /tmp/board.kicad_pcb."
"Sweep this circuit from 100 MHz to 6 GHz and plot S₂₁."
"Calibrate the VNA, then sweep my filter from 800 MHz to 6 GHz."
```

## Private MCPs

Your own private MCPs go in `~/.config/eng_mcp_suite/private.yaml`,
identical schema to the public manifest. Use:

```bash
eng-mcp-suite list   --include-private
eng-mcp-suite install --include-private --workflow rf-design
```

The public catalog never sees these. See
[PRIVATE_BOLT_ON.md](../PRIVATE_BOLT_ON.md) for the full mechanism.

## Polish gate (if you're contributing an MCP)

For a new MCP to land in the public catalog it must score 90+ on:

- README ≥ 200 chars, standardized to the toolkit template
- LICENSE matches manifest declaration
- `tests/` directory with passing CI
- `pyproject.toml` (or `package.json`) installable
- Latest release tag exists
- Pushed in the last 90 days
- Has "Part of the engineering toolkit" cross-link
- Has `examples/` with at least one runnable case study
- Has `CHANGELOG.md` (Keep a Changelog format)
- Has brand assets aligned with eng-mcp-suite design system

Run `python scripts/audit_repos.py` (in the eng-mcp-suite repo) to see
where your repo lands.

## Links

- Catalog repo: <https://github.com/RFingAdam/eng-mcp-suite>
- lineforge: <https://rfingadam.github.io/lineforge/>
- LICENSE summary: [`LICENSE_SUMMARY.md`](../../LICENSE_SUMMARY.md)
- Playbook: [`playbook.md`](playbook.md)
- Workshop: [`workshop.md`](workshop.md)
- Slides: [`slides.md`](slides.md)
- Blog: [`blog.md`](blog.md)
