# The engineering MCP toolkit — playbook

A working playbook for using the engineering MCP suite — fifteen
servers across RF, EMC, PCB / signal integrity, EM simulation,
circuit simulation, 3D modeling, and lab-instrument control — to do
real engineering work with an AI agent in the loop.

This document is the reference. The [cheat sheet](cheat-sheet.md) is
the one-page summary; the [workshop](workshop.md) is the hands-on
walk; the [slides](slides.md) are the talk; the [blog post](blog.md)
is the introduction.

## Why this exists

Engineering tools have been driven by GUIs for thirty years. Each
vendor builds a desktop application; each application has its own
menu hierarchy, its own scripting language, its own file formats.
Workflow that spans three tools means three context switches, three
data exports, three import dialogs.

LLMs change that — but only if you wire each tool up to the agent in
a way that's reliable, composable, and consistent across vendors.
[Model Context Protocol](https://modelcontextprotocol.io) is the
wiring layer. The engineering MCP suite is **fifteen MCP servers
sharing one design language** so an AI agent can move between
analytical solver, 3D EM simulator, PCB review, and bench instrument
the same way it moves between files in a directory.

Concrete goals:

- **Lower the activation energy** for cross-tool workflows. Hand-off
  between solver and simulator should be one prompt, not three menu
  dialogs.
- **Make analytical the inner loop and full-wave the outer loop.**
  Closed-form is free; FDTD is expensive. Use closed-form to iterate,
  use FDTD to validate.
- **Treat measurement as the ground truth.** Lab gear (VNA, SA,
  signal gen) plugs into the same agent so simulation and measurement
  live side by side.
- **Stay open source where possible, license-gated where unavoidable.**
  Tier 1 of the catalog is fully open. Tier 2 wraps commercial /
  hardware-gated tools (HFSS-class simulators excluded for license
  reasons; R&S and Copper Mountain hardware drivers included as
  open-source wrappers that talk to the user's equipment).

## The four-layer model

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
       │  openEMS / NEC2 / CST        │     ← 3D EM validation
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

The layers are deliberate. Inner loops are fast and analytical. Outer
loops are slow and authoritative. The agent's job is to know which
loop to use for which question.

### Layer 1 — Analytical inner loop

[lineforge](https://github.com/RFingAdam/lineforge) is the heart.
Closed-form transmission-line solvers (microstrip, stripline, CPWG,
differential pairs, three-conductor), bitmap FD-Laplace for arbitrary
2D cross-sections, pad analytics, and a path-budget calculator.

When to reach for it: anything that's 2D quasi-TEM. Z₀, εeff, L, C,
Rs, Gp. Pad capacitance and return-loss budgeting. Sensitivity sweeps
across stackup parameters.

[mcp-pcb-emcopilot](https://github.com/RFingAdam/mcp-pcb-emcopilot)
is the other inner-loop tool. PCB layout review — return paths,
decoupling, plane resonances, DDR/PCIe/USB SI, EMI prediction. Parses
KiCad / ODB++ / Gerber / IPC-2581 / Altium.

### Layer 2 — Full-wave validation

[mcp-openems](https://github.com/RFingAdam/mcp-openems) for 3D FDTD.
[mcp-nec2-antenna](https://github.com/RFingAdam/mcp-nec2-antenna) for
wire-antenna method-of-moments. [mcp-cst-studio](https://github.com/RFingAdam/mcp-cst-studio)
(license-gated) for CST Studio Suite.

When to reach for them: closed-form is out of its envelope (3D
features, broadband S-params, near/far field, coupled radiating
structures).

### Layer 3 — Circuit / system

[mcp-ltspice-qucs](https://github.com/RFingAdam/mcp-ltspice-qucs)
bridges LTspice, Qucs-S, and scikit-rf. The workspace is four
packages — one common library, three MCP servers for the three
underlying tools. Touchstone (.s2p) is the lingua franca.

### Layer 4 — Measurement

[copper-mountain-vna-mcp](https://github.com/RFingAdam/copper-mountain-vna-mcp)
for VNA, [mcp-rs-spectrum-analyzer](https://github.com/RFingAdam/mcp-rs-spectrum-analyzer)
for spectrum analyzers, [mcp-rs-cmw500](https://github.com/RFingAdam/mcp-rs-cmw500)
and [mcp-rs-siggen](https://github.com/RFingAdam/mcp-rs-siggen) for
R&S communication testers and signal generators.

## Workflow walkthroughs

The catalog ships four named workflows. Each bundles the relevant
subset of the catalog.

### `rf-design`

For designing RF circuits and antennas.

- `lineforge` — transmission lines
- `mcp-openems` — 3D EM validation
- `mcp-nec2-antenna` — wire antennas
- `mcp-ltspice-qucs` — circuit + RF system simulation
- `mcp-emc-regulations` — frequency-band lookups

**Typical conversation:**

> "Design a 50-Ω microstrip for the 2.4 GHz Wi-Fi band on 32-mil FR4.
> Then validate the impedance with openEMS, and tell me the VSWR
> bandwidth if I'm fed by a 50-Ω port."

The agent walks: lineforge gives W/h ratio → openEMS confirms within
2 % → ltspice-qucs computes VSWR bandwidth.

### `emc-compliance`

For EMC certification work.

- `mcp-emc-regulations` — FCC / CISPR / IEC / ISO limit lookups
- `drawio-engineering-mcp` — test-setup diagrams
- `mcp-rs-spectrum-analyzer` — emissions measurement (if you have
  R&S gear)
- `mcp-pcb-emcopilot` — predictive layout review

**Typical conversation:**

> "Run a CISPR-25 Class 5 pre-compliance scan on this KiCad layout
> and tell me the top 3 emission risks before we send it to the lab."

The agent walks: pcb-emcopilot parses + classifies + analyzes →
emc-regulations supplies the limit lines → predicted-vs-limit
comparison comes back.

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
- `mcp-rf-test` — embedded device compliance (private; org access)
- `mcp-remote-access` — SSH + serial to DUTs

## Case study — lineforge ↔ openEMS cross-validation

The cleanest end-to-end demonstration of the four-layer model in
this toolkit is the L3 SIG1 stripline case study, in [lineforge's
examples directory](https://github.com/RFingAdam/lineforge/tree/main/examples/09_l3_sig1_em_validation).

The setup: an asymmetric stripline on an 8-layer PCB stackup, 800
MHz – 6 GHz triplexer common port. The narrow trace goes from 3.4 mil
to 2.92 mil to avoid voiding L4. Question: does the closed-form Wadell
asymmetric stripline solver agree with FDTD?

The walk:

1. **lineforge analytical** computes Z₀, εeff, S₁₁ from Wadell closed-
   form, plus a sensitivity sweep across stackup tolerances. Cost: ~50
   ms per configuration.
2. **mcp-openems** sets up the same geometry as an FDTD model. Cost:
   ~30 s per simulation. Runs in parallel to the analytical sweep.
3. **Cross-check**: closed-form vs FDTD across the band agrees to
   ±2 %. The lineforge analytical path is validated.

The takeaway: once the analytical solver is validated against full-
wave for the design space you care about, you can iterate with
analytical (50 ms per call) and validate selectively with FDTD (30 s
per call). The agent makes the loop tight.

## Bolting on private MCPs

Private engineering tools — org-internal automation, licensed
bolt-ons, R&D experiments — can join the catalog at runtime via a
user-local manifest file (`~/.config/eng_mcp_suite/private.yaml`).
The public catalog never names them; the user opts in with
`--include-private`.

See [`PRIVATE_BOLT_ON.md`](../PRIVATE_BOLT_ON.md) for the mechanism.

## FAQ

**Why MCP rather than custom integrations?**
MCP is the protocol Claude and most modern LLM agents already speak.
Building an MCP wrapper gives every agent client (Claude Desktop,
Claude Code, VS Code Copilot, OpenAI Agents SDK) the same access to
the same tool surface for free.

**Why a catalog rather than one mega-server?**
Each MCP has its own dependency tree (NEC2 needs `nec2c`, openEMS
needs the engine + Python bindings, LTspice needs the binary, R&S
gear needs `pyvisa`). A catalog lets users install only what they
need. The `eng-mcp-suite install --workflow rf-design` bundle handles
the per-workflow assembly.

**Why both Apache-2.0 and GPL-3.0 in the catalog?**
[lineforge](https://github.com/RFingAdam/lineforge) descends from
atlc / atlc2, which are GPL — keeping it GPL respects the lineage.
mcp-openems and mcp-blender wrappers are Apache while invoking GPL
engines at runtime (no redistribution, so the wrapper itself stays
permissive). Everything else is Apache. Per-MCP details are in
[`LICENSE_SUMMARY.md`](../../LICENSE_SUMMARY.md).

**Why isn't HFSS in the catalog?**
HFSS-class simulators (Ansys HFSS, etc.) require commercial licenses
that the maintainer of this toolkit doesn't currently have. The
wrapper code exists but can't be validated end-to-end. Per the
project's polish gate, an unvalidated wrapper doesn't go in the
public catalog. CST Studio is in the same boat — listed as `commercial`
but actually private until a license seat is available.

**Can I contribute a new MCP?**
Yes. The polish gate is 90+ on the audit script (README ≥ 200 chars,
LICENSE matches manifest, tests, pyproject.toml, latest release tag,
recent activity) plus four toolkit-fit checks (cross-link to catalog,
"when to use vs related tools" section, examples/ directory,
CHANGELOG.md). Open an issue on
[eng-mcp-suite](https://github.com/RFingAdam/eng-mcp-suite) with
your proposed MCP and the audit-score path.

## Where to go next

- **First time?** Read the [cheat sheet](cheat-sheet.md), then
  install via `pipx install git+https://github.com/RFingAdam/eng-mcp-suite.git && eng-mcp-suite list`.
- **Want hands-on practice?** Walk through the
  [workshop](workshop.md).
- **Giving a talk?** [Slides](slides.md) are pre-built Marp deck.
- **Writing a blog post?** Crib from [the blog draft](blog.md).
