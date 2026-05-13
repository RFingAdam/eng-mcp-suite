---
marp: true
theme: default
paginate: true
backgroundColor: "#0F172A"
color: "#F8FAFC"
style: |
  section {
    font-family: 'Inter', 'Segoe UI', sans-serif;
  }
  h1 { color: #22D3EE; }
  h2 { color: #22D3EE; }
  code { color: #34D399; background: #1E293B; }
  strong { color: #F8FAFC; }
  blockquote { border-left: 4px solid #22D3EE; color: #CBD5E1; }
  table { font-size: 0.7em; }
  a { color: #22D3EE; }
---

# Engineering MCP toolkit

**Fifteen MCP servers for RF, EMC, PCB, EM simulation, circuit
simulation, and lab-instrument control — sharing one design language.**

Open source · Apache-2.0 / GPL-3.0 · Adam Engelbrecht · 2026

---

## The problem

Engineering tools have been GUI-driven for thirty years.

- Each vendor: own application, own scripting, own file formats
- Cross-tool workflow: three context switches, three exports, three
  import dialogs
- The high-leverage workflow lives *between* the tools — and nobody
  builds it

LLMs can collapse this. **But only if the tools are wired up
consistently.**

---

## The wiring layer

[Model Context Protocol](https://modelcontextprotocol.io) — the
protocol Claude and other modern LLM agents already speak.

One MCP server per engineering tool, exposing a typed tool surface
the agent can call.

Build the MCP wrappers once, and every agent (Claude Desktop, Claude
Code, VS Code Copilot, OpenAI Agents SDK) can drive every tool.

---

## The four-layer model

```
┌─ AI agent ─────────────────────────────────┐
└─────┬──────────────┬───────────────────────┘
      │              │  ← MCP
┌─────▼─────┐  ┌─────▼─────┐
│ lineforge │  │ pcb-em..  │  fast inner loop
└─────┬─────┘  └───────────┘    (closed-form)
      │ Touchstone (.s2p)
┌─────▼──────────────────┐
│ openEMS / NEC2 / CST   │   3D EM outer loop
└────────────────────────┘    (full-wave)
      │
┌─────▼──────────────────┐
│ LTspice / Qucs-S       │   circuit / system
└────────────────────────┘
      │
┌─────▼──────────────────┐
│ VNA / SA / Sig-gen     │   measurement
└────────────────────────┘    (ground truth)
```

---

## Inner loop = closed-form (cheap, fast)

**`lineforge`** — the heart of the toolkit.

- Microstrip, stripline (sym + asym), CPWG, differential, three-conductor
- Closed-form Wadell / Hammerstad-Jensen / IPC-2141
- 2D bitmap FD-Laplace for arbitrary cross-sections
- Pad analytics, path budget, design rule classification
- atlc2-compatible

Closed-form gives you a Z₀ in 50 ms. Iterate freely.

---

## Outer loop = full-wave EM (slow, authoritative)

**`mcp-openems`** — 3D FDTD via openEMS (open-source).
**`mcp-nec2-antenna`** — wire-antenna MoM (NEC2).
**`mcp-cst-studio`** — CST Studio Suite (license required).

Use to validate the inner loop for a specific design point. Don't
sweep here — sweep with closed-form, validate with FDTD.

---

## Circuit / system layer

**`mcp-ltspice-qucs`** — three MCP servers in one workspace:

- `mcp-ltspice` — Analog Devices LTspice
- `mcp-qucs-s` — Qucs-S (GPL)
- `mcp-rf-analysis` — scikit-rf

Touchstone (`.s2p`) is the lingua franca. RF system design, filter
design, multi-radio coexistence.

---

## Measurement layer

The bench is the ground truth.

| Hardware | MCP |
|---|---|
| Copper Mountain VNA | `copper-mountain-vna-mcp` |
| R&S FSW / FSVA / FSV / FPL spectrum analyzers | `mcp-rs-spectrum-analyzer` |
| R&S CMW500 comms tester | `mcp-rs-cmw500` |
| R&S signal generators (SMW / SMBV / SGT / ...) | `mcp-rs-siggen` |

All open-source wrappers. You bring the hardware.

---

## Plus EMC, PCB, diagrams, 3D

- **`mcp-emc-regulations`** — FCC / CISPR / IEC / ISO / automotive
  OEM / medical EMC lookup
- **`mcp-pcb-emcopilot`** — PCB review, return paths, decoupling,
  DDR / PCIe / USB SI, EMI prediction
- **`drawio-engineering-mcp`** — RF block diagrams, stack-ups, EMC
  test setups
- **`mcp-blender`** — 3D modeling, enclosure visualization
- **`mcp-remote-access`** — SSH + serial to DUTs

---

## Workflows ship as bundles

```bash
eng-mcp-suite install --workflow rf-design
eng-mcp-suite install --workflow emc-compliance
eng-mcp-suite install --workflow pcb-review
eng-mcp-suite install --workflow lab-automation
```

Each bundle: a curated subset of the catalog. Install only what you
need; generate a merged Claude config in one command.

---

## Demo — a tight RF design loop

> "Design a 50-Ω microstrip for 2.4 GHz on 32-mil FR4."

`lineforge` → W = 1.435 mm, Z₀ = 50.0 Ω

> "Validate with openEMS."

`mcp-openems` → FDTD agrees to ±2 %

> "What's the impedance excursion if εr varies ±5 %?"

`lineforge` sweep → Z₀ band: 49–51 Ω. Margin is adequate.

**Three prompts. Three tool calls each. Done in 90 seconds.**

---

## Case study — L3 SIG1 stripline

An 8-layer PCB. 800 MHz – 6 GHz triplexer common port. Asymmetric
stripline necks down 3.4 → 2.92 mil to avoid voiding L4.

Question: does the Wadell closed-form agree with FDTD?

Answer: yes, ±2 % across the band. Now the closed-form is
*validated*. Sweep freely.

Full case study: `lineforge/examples/09_l3_sig1_em_validation/`.

---

## Bolt-on for private MCPs

Your own org-internal MCPs go in
`~/.config/eng_mcp_suite/private.yaml`, same schema as the public
catalog. Opt in:

```bash
eng-mcp-suite list   --include-private
eng-mcp-suite install --workflow rf-design --include-private
```

The public catalog never sees them. Your private stuff stays private.

---

## Polish gate — what gets in the catalog

To be public-Tier-1 in eng-mcp-suite, an MCP must clear **all of**:

- README ≥ 200 chars, standardized template
- LICENSE matches manifest declaration
- `tests/` + passing CI
- `pyproject.toml` (or `package.json`)
- Latest release tag, pushed in last 90 days
- "Part of the engineering toolkit" cross-link
- `examples/` with one runnable case study
- `CHANGELOG.md` (Keep a Changelog)
- Brand assets aligned with toolkit design system

Score 90+ on `scripts/audit_repos.py`. Otherwise: not public.

---

## Open source vs license-gated

**Tier 1 — open source.** Free as in freedom. Lineforge GPL-3.0 (atlc
lineage); everything else Apache-2.0. Per-MCP details in
[`LICENSE_SUMMARY.md`](../../LICENSE_SUMMARY.md).

**Tier 2 — license / hardware-gated.** Wrapper code is public; the
underlying tool (HFSS, CST, R&S, CM VNA) is the user's responsibility.

**Tier 3 — strictly private.** Org-internal tools, never named in the
public catalog. Bolt-on mechanism only.

---

## What this is *not*

- Not a paid SaaS — community-driven open source
- Not vendor lock-in — every MCP is replaceable
- Not "AI does engineering for you" — agent + engineer, not agent
  alone
- Not a simulator itself — wrappers around best-in-class solvers
  that already exist

---

## Getting started in 60 seconds

```bash
pipx install eng-mcp-suite
eng-mcp-suite install --workflow rf-design
eng-mcp-suite config --workflow rf-design --out config.json
# merge config.json mcpServers into your Claude Desktop config
```

Then open Claude Desktop and ask:

> What MCP tools do I have for RF design?

You should see lineforge, mcp-openems, mcp-nec2-antenna,
mcp-ltspice-qucs, mcp-emc-regulations.

---

## Where to go next

| Audience | Doc |
|---|---|
| Just want commands | [`cheat-sheet.md`](cheat-sheet.md) |
| Want the full story | [`playbook.md`](playbook.md) |
| Want hands-on practice | [`workshop.md`](workshop.md) |
| Want to write about it | [`blog.md`](blog.md) |

GitHub: <https://github.com/RFingAdam/eng-mcp-suite>

---

## Thanks

The toolkit only exists because the upstream projects do:

- **openEMS** (Thorsten Liebig and contributors)
- **NEC2** (Lawrence Livermore National Laboratory; public domain)
- **Qucs-S** (Mike Brinson, Vadim Kuznetsov, contributors)
- **scikit-rf** (Alex Arsenovic and contributors)
- **atlc / atlc2** (David Kirkby; the lineage `lineforge` extends)

If the toolkit is useful, the credit goes upstream.

**Questions?** Issues on
[eng-mcp-suite](https://github.com/RFingAdam/eng-mcp-suite).
