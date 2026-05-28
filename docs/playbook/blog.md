# Fifteen MCP servers for engineers, sharing one design language

*Draft blog announcement — adapt for personal blog, dev.to, Hacker News,
LinkedIn, or wherever you want to talk about the toolkit.*

---

I've spent the last year wrapping engineering tools as MCP servers
and quietly building them up into a coherent catalog. The catalog
just hit v1.0. This post is the public introduction.

If you're an RF or EE engineer who's stared down the daily friction
of moving between a transmission-line calculator, a 3D EM simulator,
a SPICE deck, a VNA, and a PCB review tool — and felt like the
high-leverage work always lived *between* the tools rather than
inside any one of them — this is for you.

## The problem worth solving

Engineering tools have been GUI-driven for thirty years. Every vendor
ships a desktop application with its own menus, its own scripting
language, its own file formats. The friction isn't in any single
tool — it's in the seams between them.

Concretely, here's the workflow I run a dozen times a week:

1. Compute a transmission line's Z₀ in a closed-form calculator.
2. Sweep the calculator across the stackup tolerance window.
3. Hand the worst case to a full-wave simulator to verify.
4. Wire the result into a circuit simulator to see how it interacts
   with neighboring nets.
5. (Sometimes) hand the final design to a VNA to actually measure
   it.

Each step lives in a different tool. Each tool has its own export
format. Each transition costs three minutes of manual file
shuffling. Multiply by the iteration count of a real RF design and
the time tax is enormous.

LLMs change this — but only if the tools are wired up in a way the
agent can actually use. A single mega-tool with three hundred
functions is unusable. Three hundred microscope-narrow tools spread
across a dozen integrations is also unusable. What you want is a
small set of focused tool surfaces, named consistently, sharing one
design vocabulary.

That's what the engineering MCP toolkit is.

## What's in v1.0

Fifteen [Model Context Protocol](https://modelcontextprotocol.io)
servers covering:

- **RF / transmission lines** — `lineforge` (closed-form solvers,
  bitmap FD-Laplace, pad analytics, path-budget)
- **3D EM simulation** — `mcp-openems` (FDTD via openEMS),
  `mcp-nec2-antenna` (wire-antenna method-of-moments),
  `mcp-cst-studio` (CST license-gated)
- **PCB / signal integrity / EMC** — `mcp-pcb-emcopilot` (layout
  review, return paths, decoupling, plane resonances, DDR/PCIe/USB
  SI, EMI prediction)
- **Circuit / system simulation** — `mcp-ltspice-qucs` (LTspice +
  Qucs-S + scikit-rf, all Touchstone-aware)
- **EMC regulatory** — `mcp-emc-regulations` (FCC / CISPR / IEC /
  ISO / automotive / medical)
- **Diagrams + 3D + remote access** — `drawio-engineering-mcp`,
  `mcp-blender`, `mcp-remote-access`
- **Lab instruments** — `copper-mountain-vna-mcp`,
  `mcp-rs-spectrum-analyzer`, `mcp-rs-cmw500`, `mcp-rs-siggen`

All open source. Most Apache-2.0; `lineforge` is GPL-3.0 because it
descends from the venerable `atlc` / `atlc2` lineage.

The hardware-driver MCPs (R&S, Copper Mountain) are open-source
wrappers — the *code* is free, you bring your own hardware. There's
no built-in simulator and no GUI; the wrapper is a thin SCPI driver
that exposes the instrument's tool surface to the agent.

## The catalog is wired together

Critically, the toolkit is a *catalog*, not a monorepo. Each MCP is
its own repo, its own Python package, its own release cadence. But
they all share:

- **One installer** (`eng-mcp-suite`) that reads a manifest and
  installs whatever subset of MCPs you ask for.
- **One audit script** that scores every repo on the same polish
  gate before it's allowed in the public catalog.
- **One README template** so every repo has the same "Part of the
  engineering toolkit" cross-link section.
- **One brand system** — palette, logos, badges, docs — so the
  ecosystem looks like one ecosystem instead of fifteen drive-by
  GitHub projects.

If you've ever opened a GitHub organization and seen fifty
inconsistently-styled repos that all claim to "work together", you
know the failure mode. The polish gate is how this catalog avoids
that.

To clear the gate, a repo needs:

- README ≥ 200 chars, standardized to the toolkit template
- LICENSE that matches the manifest declaration
- `tests/` with a passing CI
- `pyproject.toml` (or `package.json`) installable
- A release tag
- Recent push activity (last 90 days)
- "Part of the engineering toolkit" section linking to the catalog
- An `examples/` directory with at least one runnable case study
- A `CHANGELOG.md` in Keep-a-Changelog format
- Brand assets (logo + banner) aligned with the design system

Score 90 or above on the audit script. Otherwise: it stays private
until polish is done. The catalog has two MCPs at 90 right now that
will stay private indefinitely — `mcp-rf-test` (proprietary org-
internal LICENSE) and `mcp-cst-studio` (no CST license to validate
end-to-end). Out of the public catalog by design.

## What the agent actually does

Here's a real conversation, abbreviated:

> "Design a 50-Ω microstrip for 2.4 GHz on 32-mil FR4."

Claude calls `lineforge.microstrip` → reports W = 1.435 mm,
Z₀ = 50.0 Ω, εeff = 3.10.

> "What's the Z₀ range if FR4 sheet εr varies between 4.2 and 4.6?"

Claude calls `lineforge.microstrip` four more times with εr swept →
reports Z₀ band of 49.0–51.2 Ω.

> "Validate the nominal design with openEMS. Just generate the sim
> file — don't actually run it, I'll run it on my workstation."

Claude calls `openems_create_microstrip` → produces a Python sim
script that drops into `openEMS_run.py`. Reports the wrapper's HJ-
calculator Z₀ (51.5 Ω; agrees with lineforge to ±3 %) and notes the
expected FDTD result will land in the same window.

> "If I want VSWR ≤ 1.5:1 across the full 2.4 GHz Wi-Fi band — what's
> my Z₀ tolerance budget?"

Claude does the math itself (no tool call needed) → reports the band
that keeps |Γ| ≤ 0.2 with a 50-Ω port reference: roughly 33 → 75 Ω,
much wider than the εr tolerance band.

Three prompts. Five tool calls. Forty-five seconds, including reading
time. The agent did the right thing at every layer of the four-layer
model — closed-form for sweep, FDTD setup for validation, math in
its head for the system question. No file-shuffling. No menu
dialogs.

## The four-layer model

The catalog is structured around four layers:

1. **Analytical inner loop** — closed-form solvers. Cheap, fast,
   correct within their assumptions. `lineforge`, `mcp-pcb-emcopilot`.
2. **Full-wave validation outer loop** — 3D EM. Slow, accurate, used
   sparingly to validate the inner loop. `mcp-openems`,
   `mcp-nec2-antenna`, `mcp-cst-studio`.
3. **Circuit / system** — network-level simulation, filter design,
   coexistence. `mcp-ltspice-qucs`.
4. **Measurement** — bench instruments. The ground truth.
   `copper-mountain-vna-mcp`, R&S drivers.

The agent's job is to know which loop to use for which question. The
shared design language across the catalog makes that legible.

## What's not in here (and why)

A few things I get asked about that aren't in the catalog:

- **Ansys HFSS.** I built a wrapper privately but I don't currently
  have an HFSS license to validate it. Per the polish gate, an
  unvalidated wrapper doesn't go in the public catalog. It'll come
  back when there's a license seat to test against.
- **CST Studio.** Same story — wrapper exists, no current CST seat
  to validate. Listed in the catalog as `commercial` but actually
  private until validation is possible.
- **Org-internal automation tools.** These don't get a public listing.
  The catalog ships with a *private bolt-on mechanism* — users with
  their own private MCPs put them in
  `~/.config/eng_mcp_suite/private.yaml` and opt in with
  `--include-private`. Their private stuff stays private; the public
  catalog never references it.

## What it's *not*

A few clarifications:

- **It's not a paid SaaS.** It's open source, community-driven. No
  cloud component, no telemetry, no license server. Apache-2.0 (or
  GPL-3.0 for `lineforge`).
- **It's not vendor lock-in.** Every MCP is replaceable. The catalog
  is a curation, not a moat.
- **It's not "AI replaces engineers".** This is *agent + engineer*,
  always. The agent is the wiring layer. You're still doing the
  engineering.
- **It's not a simulator.** The wrappers don't reimplement openEMS
  or NEC2 or LTspice. They expose those existing best-in-class
  solvers via MCP. If the upstream tool gets better, the wrapper
  gets better.

## Getting started

```bash
pipx install git+https://github.com/RFingAdam/eng-mcp-suite.git

# See what's in the catalog
eng-mcp-suite list

# Install a workflow bundle
eng-mcp-suite install --workflow rf-design

# Generate a Claude Desktop config snippet
eng-mcp-suite config --workflow rf-design --out config.json

# Merge config.json's mcpServers into your existing
# claude_desktop_config.json
```

Then open Claude Desktop and ask:

> "What MCP tools do I have for RF design?"

You should see `lineforge`, `mcp-openems`, `mcp-nec2-antenna`,
`mcp-ltspice-qucs`, `mcp-emc-regulations`.

## Where this is going

v1.0 is the public-launch milestone. Future work:

- **PyPI publish for the suite installer** (currently install from
  source).
- **More worked examples** — every Tier 1 MCP has at least one
  runnable example, but there's room for deeper case studies that
  walk full cross-tool flows.
- **Better polish-gate enforcement** — the audit script currently
  scores presence-of-LICENSE without checking content. There's an
  open issue to add license-content detection.
- **Tier 2 polish** — the R&S MCPs and CM VNA driver land at v0.1–
  v0.2 today; they'll get richer test coverage and better mock-
  hardware modes for CI as users push them.
- **More MCPs.** If you have an engineering tool that would benefit
  from being agent-driveable, open an issue on the catalog repo and
  let's talk.

## Thanks to the upstreams

The toolkit only exists because the upstream projects do.
`mcp-openems` wraps **openEMS** (Thorsten Liebig and contributors).
`mcp-nec2-antenna` wraps **NEC2** (LLNL, public domain).
`mcp-ltspice-qucs` wraps **Qucs-S** (Mike Brinson, Vadim Kuznetsov),
scikit-rf (Alex Arsenovic), and Analog Devices LTspice. `lineforge`
extends the **atlc / atlc2** lineage (David Kirkby).

If the toolkit is useful, the credit goes upstream first. The
catalog is the wiring; the upstreams are the substance.

## Links

- **GitHub**: <https://github.com/RFingAdam/eng-mcp-suite>
- **Lineforge** (the heart of the toolkit): <https://rfingadam.github.io/lineforge/>
- **Workshop guide**: [`workshop.md`](workshop.md)
- **Cheat sheet**: [`cheat-sheet.md`](cheat-sheet.md)
- **Playbook**: [`playbook.md`](playbook.md)

If you build something with the toolkit, open an issue or send a
note. I want to hear about it.
