# Engineering MCP toolkit — workshop guide

A 2.5-hour hands-on workshop that takes a participant from zero to
running cross-tool RF design loops with an AI agent.

## Audience

RF / EE / SI engineers comfortable with:
- A terminal
- Reading Python
- Conceptually familiar with transmission lines, antennas, basic EMC

No prior MCP / Claude / LLM agent experience required.

## What you'll build

By the end of the workshop, you'll have:

1. A working Claude Desktop (or Claude Code) install with five engineering
   MCP servers wired in.
2. A microstrip design walked from analytical → FDTD validation.
3. An antenna design walked from formula → method-of-moments simulation.
4. A PCB layout walked through pre-compliance EMC review.
5. A clear mental model of where each tool fits in the four-layer
   inner-loop / outer-loop / validation pyramid.

## Prerequisites

Install before the workshop starts (10 min):

```bash
# 1. Have Python 3.10+ and pipx
pipx --version

# 2. Install Claude Desktop or Claude Code
# Claude Desktop: https://claude.ai/download
# Claude Code:    https://www.anthropic.com/claude-code

# 3. Install the suite installer
pipx install eng-mcp-suite

# 4. Install nec2c (the antenna solver binary)
# Linux:    sudo apt install nec2c
# macOS:    brew install nec2c
# Windows:  https://www.qsl.net/4nec2/  (Windows port)

# 5. (Optional) Install openEMS — heavier dependency, see openems.de.
#    Skip for the workshop if you're tight on time; we'll run the
#    closed-form-only version of the example.
```

## Section 0 — Install and verify (10 min)

```bash
eng-mcp-suite list                          # see all 15 MCPs
eng-mcp-suite list --status public          # only the open-source ones
eng-mcp-suite workflows                     # the curated bundles
```

Install the rf-design bundle:

```bash
eng-mcp-suite install --workflow rf-design
```

Generate a Claude config snippet:

```bash
eng-mcp-suite config --workflow rf-design --out /tmp/rf-design.json
cat /tmp/rf-design.json
```

Merge `mcpServers` from `/tmp/rf-design.json` into your existing
`claude_desktop_config.json`. Restart Claude Desktop. Verify the tools
appear by typing in Claude Desktop:

> List the MCP tools you have available right now.

You should see a list including `lineforge`, `mcp-nec2-antenna`,
`mcp-openems`, `mcp-ltspice-qucs`, `mcp-emc-regulations`. If not,
check the config path and restart Claude Desktop again.

## Section 1 — Microstrip design (30 min)

**Goal:** Design a 50-Ω microstrip on FR4, then validate the impedance.

### Exercise 1.1 — Ask for the geometry

Type in Claude Desktop:

> Design a 50-Ω microstrip for 2.4 GHz on 32-mil (0.787 mm) FR4
> (εr = 4.4). Tell me the trace width.

Expected: Claude calls `lineforge` (probably
`microstrip_impedance` or the dispatcher) → reports W ≈ 1.43 mm with
εeff ≈ 3.1.

### Exercise 1.2 — Sensitivity sweep

> If the FR4 sheet εr varies from 4.2 to 4.6 with manufacturing
> tolerance, what's the Z₀ range I'll see at 1.435 mm trace width?

Expected: Claude calls lineforge multiple times across the εr range
and reports a Z₀ band of roughly 49–51 Ω.

### Exercise 1.3 — Cross-validate against openEMS

If you installed openEMS:

> Set up the same microstrip in openEMS and report Z₀ from the FDTD
> sim.

Expected: Claude calls `openems_create_microstrip`, then prints the
geometry and the calculated Z₀ from the wrapper's HJ formula (the
script-generation step exports a Python file you'd run with the
openEMS engine separately). Compare to lineforge's number — within
2 %.

If you skipped openEMS, the calculator-only path in
`mcp-openems` still works — you just don't get the FDTD validation
step.

### Discussion

What did the agent do? It picked the right tool for the right
question. You didn't have to specify "use Wadell" or "use HJ"; the
agent made that choice. That's the value of the four-layer model
being legible to the agent.

## Section 2 — Wire antenna design (30 min)

**Goal:** Design a half-wave dipole, then design a 5-element Yagi.

### Exercise 2.1 — Half-wave dipole

> Design a half-wave dipole for 435 MHz (70-cm amateur band) and tell
> me the actual resonance, feedpoint impedance, and VSWR ≤ 2:1
> bandwidth.

Expected: Claude calls `nec2_create_dipole` → `nec2_simulate` with a
frequency sweep across 420–450 MHz. Reports:
- Length per leg: ~17.25 cm
- Resonance: ~433 MHz (slight pull-down from formula)
- Z = ~71 + j0 Ω
- VSWR ≤ 2:1 bandwidth: ~16.5 MHz

### Exercise 2.2 — 5-element Yagi

> Now design a 5-element Yagi for the 2-meter band at 146 MHz. I want
> at least 9 dBi gain and 20 dB front-to-back. Use the DL6WU template.

Expected: Claude calls `nec2_create_yagi`. Reports boom length ≈
2.41 m, gain ≈ 10 dBi, F/B ≈ 23 dB. Feedpoint impedance ≈ 29 + j8 Ω
(low, needs matching).

### Exercise 2.3 — Match to 50 Ω

> The feedpoint is 29 Ω. What's the easiest match to 50-Ω coax?

This one is a knowledge question, not a tool call — Claude should
suggest a gamma match or hairpin and roughly estimate the component
value.

### Discussion

The agent moved smoothly between tool calls and knowledge questions.
The tool surface didn't force every decision through a function call;
it let the agent reason.

## Section 3 — PCB review (40 min)

**Goal:** Take a PCB layout and get a pre-compliance EMC review.

### Setup

You'll need a PCB layout to test against. If you don't have one
handy, mcp-pcb-emcopilot ships with example boards under its
`examples/` directory in the repo — clone and use one.

### Exercise 3.1 — Stack-up review

> Here's a KiCad layout at /path/to/board.kicad_pcb. Parse it and
> tell me about the stack-up.

Expected: Claude calls `pcb_parse_layout` → `pcb_get_stackup` →
reports layer count, dielectric thicknesses, copper weights.

### Exercise 3.2 — Return-path analysis

> Find every signal trace that crosses a plane split. Severity?

Expected: Claude calls `pcb_analyze_return_paths` → reports any nets
where the return current would have to detour across a split. Each
finding gets a severity badge.

### Exercise 3.3 — CISPR-25 pre-compliance

> Run a CISPR-25 Class 5 pre-compliance scan and flag the top 5 EMC
> risks. Generate a DOCX report.

Expected: Claude walks classifier → analyzers (return path,
decoupling, smps EMI, clock EMI) → predict emissions → report. Final
output: a DOCX file you can hand to your EMC engineer.

### Discussion

This is where the cross-tool story really pays off. Without an agent,
this workflow is parser-CLI → stack-up viewer → spreadsheet for
return paths → custom script for decoupling check → ... etc. The agent
collapses six steps into one prompt.

## Section 4 — Capstone: a tight design loop (25 min)

**Goal:** Run an actual iteration: lineforge inner loop, openEMS
outer loop validation, on a real RF design choice.

Choose ONE of:

### Capstone A — Stripline narrow-section fix

You have a stripline that needs to neck down from 4 mil to 3 mil over
a short section without voiding the GND below. Use lineforge to:

- Compute Z₀ before and after the necking
- Sweep across the necking length to find where the impedance
  excursion becomes a problem (Γ > 0.1 say)
- Then have Claude generate the openEMS sim file for the worst case

This is the L3 SIG1 case study from the lineforge repo. Read its
README before starting.

### Capstone B — Diff-pair tolerance budget

You have a 100-Ω differential pair on a stackup with ±10 % εr and
±5 % copper-weight tolerance. Use lineforge to:

- Compute the differential Z₀ at nominal
- Sweep both tolerances simultaneously
- Find the worst-case impedance excursion

Pure analytical, no FDTD needed. But the inner-loop sweep is exactly
where the agent earns its keep.

## Section 5 — Reflection (15 min)

Group discussion:

- What's the cheapest workflow you could automate next?
- Which tool did the agent reach for that surprised you?
- Where did the agent struggle? (Honest answer: anything that needs
  domain judgment without explicit cues. Be specific so we can
  improve prompts and tool descriptions.)

## After the workshop

- Bookmark the [cheat sheet](cheat-sheet.md).
- Skim [playbook.md](playbook.md) for the broader strategy / FAQ.
- File issues on individual MCPs as you find rough edges.
- Star [eng-mcp-suite](https://github.com/RFingAdam/eng-mcp-suite)
  to follow updates.
