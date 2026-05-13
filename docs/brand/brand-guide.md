# eng-mcp-suite — Brand Guide

A restrained, technical visual identity for the eng-mcp-suite family of
engineering MCP servers. The palette and motifs are inherited from
[`lineforge`](https://github.com/RFingAdam/lineforge) — the first public
MCP in the family — so every sibling repo can carry the same family
resemblance without re-inventing it.

Aesthetic target: GitHub Docs / scikit-learn / Rust. Engineering tools,
not consumer products. Confident, dense, scannable.

---

## Palette

All colors are sourced from `lineforge/assets/logo-banner.svg`. Do not
introduce new hues at the suite level — domain accent slots inside the
logo template are the only place per-MCP color variance is permitted.

### Surface

| Token            | Hex       | Role                                                |
| ---------------- | --------- | --------------------------------------------------- |
| `--bg-deep`      | `#0B1220` | Banner background outer stops, badge fill           |
| `--bg-base`      | `#0F172A` | Banner background mid stop, surfaces, pills         |
| `--bg-rule`      | `#1E293B` | Banner field lines, pill backgrounds, hairline rule |

### Ink

| Token            | Hex       | Role                                                |
| ---------------- | --------- | --------------------------------------------------- |
| `--ink-bright`   | `#F8FAFC` | Wordmark, headings on dark surfaces                 |
| `--ink-muted`    | `#CBD5E1` | Body text on dark, conductor-edge highlight         |
| `--ink-soft`     | `#94A3B8` | Tagline text, conductor face, secondary metadata    |
| `--ink-faint`    | `#64748B` | Keyword-row text, tertiary metadata                 |

### Accents (palette, not free-for-all)

| Token            | Hex       | Used for                                            |
| ---------------- | --------- | --------------------------------------------------- |
| `--accent-cyan`  | `#22D3EE` | Primary glow — field-line emphasis, version pill, CLI accent |
| `--accent-sky`   | `#0EA5E9` | Dielectric / field gradient, secondary cyan tone    |
| `--accent-amber` | `#F59E0B` | Conductor strip gradient bottom, Python pill        |
| `--accent-gold`  | `#FBBF24` | Conductor strip gradient top                        |
| `--accent-emerald` | `#34D399` | License pill, "success" markers                   |
| `--accent-violet`  | `#A78BFA` | MCP pill, agent-surface marker                    |
| `--accent-rust`    | `#B45309` | Strip outline, deep-amber stroke                  |

### Per-MCP domain hint (optional, single slot)

Each MCP in the suite is allowed exactly **one** accent override at the
inset-glyph position in its logo. Pick from the existing accents above —
do not introduce a new hue. Suggested defaults:

| Domain                                       | Accent      | Hex       |
| -------------------------------------------- | ----------- | --------- |
| RF / transmission lines (lineforge, openems) | cyan        | `#22D3EE` |
| EMC regulatory (emc-regulations)             | violet      | `#A78BFA` |
| PCB / SI (pcb-emcopilot, drawio)             | amber       | `#F59E0B` |
| Antennas (nec2)                              | sky         | `#0EA5E9` |
| Circuit sim (ltspice-qucs)                   | emerald     | `#34D399` |
| Lab gear (vna, sa, siggen, rf-test, cmw500)  | gold        | `#FBBF24` |
| Remote / infrastructure (remote-access)      | ink-muted   | `#CBD5E1` |
| 3D / rendering (blender)                     | amber       | `#F59E0B` |

---

## Typography

System stacks only. No webfonts, no external dependencies. The logo SVGs
must render correctly when GitHub serves them inside a README.

| Use            | Stack                                                                                |
| -------------- | ------------------------------------------------------------------------------------ |
| Wordmark, UI   | `ui-sans-serif, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif`     |
| Code, mono     | `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace` |

Weights in use: `500` (tagline), `600` (keyword row), `700` (pill text,
version pill), `800` (wordmark). Letter-spacing on the wordmark is `-3`
at the 120px display size (proportional at other sizes).

---

## Voice & tone

| Do                                                | Don't                                       |
| ------------------------------------------------- | ------------------------------------------- |
| Open with what it solves, in one sentence         | "Welcome to..." or anything ceremonial      |
| State accuracy / tolerance numbers up front       | Hand-wave precision                         |
| Show a code block within the first scroll         | Bury install instructions below a feature list |
| Use tables for capability comparisons             | Bulleted-list walls                         |
| Cite reference formulas / standards by name       | Claim novelty without a citation            |
| Refer to the agent as "your assistant" or "the agent" | Anthropomorphize ("ask the AI")          |
| Say "MCP server", "MCP tool", "MCP client"        | "AI tool" or "GPT integration"              |

Length: a README in this family should fit in roughly the same density
as lineforge's — tight, table-heavy, no marketing fluff. If it crosses
~450 lines it's too long.

---

## When to use mark vs wordmark vs banner

| Asset                | Dimensions | Use                                                                 |
| -------------------- | ---------- | ------------------------------------------------------------------- |
| **Banner**           | 1280×320   | README header (full width), social card                             |
| **Logo template**    | 240×64     | Embedded references, navigation, docs sidebar header                |
| **Mark only**        | 64×64      | Favicon, package-manager icon, GitHub topic card, status badge      |

The mark (just the hex frame + domain glyph) carries the family
identity. The wordmark identifies the specific MCP. Use both together
in the banner; use mark alone where space is constrained.

Logo files for each MCP live at `<repo>/assets/logo-banner.svg`,
`<repo>/assets/logo.svg` (square mark), and optionally
`<repo>/assets/logo-mark.svg` (mark variant). The wordmark always
matches the package name (lowercase, monospace-friendly).

---

## Accessibility

The brand carries real contrast requirements because the README banners
are viewed on both light and dark GitHub themes.

- **Contrast.** Wordmark `#F8FAFC` on `#0B1220`/`#0F172A` is ≥17:1 —
  WCAG AAA. Tagline `#94A3B8` on the same background is ≥7:1 — AAA for
  large text, AA for normal. Don't drop below `#94A3B8` for any
  user-readable text on the deep-navy surface.
- **Color is never the only signal.** Pills always have both a colored
  text token and a labeled string. Status emoji prefixes
  (🟢 🔒 💼 🔧) are paired with the textual status.
- **Alt text.** Every banner `<img>` must carry a meaningful `alt=` that
  states what the MCP does — e.g. `alt="lineforge — open-source MCP
  transmission line calculator"`. Never `alt="logo"`.
- **No motion in static assets.** SVG `<animate>` and CSS animations
  are off-limits in README banners. Motion is opt-in inside docs sites
  only, and must respect `prefers-reduced-motion`.
- **`role="img"` + `<title>`.** Every logo SVG declares
  `role="img"` and includes a `<title>` element so screen readers
  announce a meaningful name instead of a flood of `<path>` nodes.

---

## Brand assets index

```
eng-mcp-suite/docs/brand/
├── brand-guide.md          ← this file (palette, voice, usage)
├── logo-template.svg       ← parametric SVG; fill the glyph + wordmark slots
├── mcp-icon-glyphs.svg     ← sprite sheet of 15 domain glyphs
├── README-template.md      ← README structure every family repo follows
└── docs-template/          ← mkdocs scaffold + page stubs
    ├── mkdocs.yml
    └── docs/
        ├── index.md
        ├── tools.md
        ├── usage.md
        └── architecture.md
```

Per-MCP repos copy these files in and replace the documented
`<!-- placeholders -->`. Target time per repo: ~5 minutes for the
README, ~30 minutes for a first-cut logo. The follow-up brand-rollout
wave (A6b) does this in parallel across the 12 public repos.
