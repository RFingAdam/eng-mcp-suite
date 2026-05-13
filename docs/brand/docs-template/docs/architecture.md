# Architecture

<!--
  How this MCP is built AND how it composes with the rest of eng-mcp-suite.
  Two halves:
    1. Internal architecture (modules, surfaces, kernels)
    2. External composition (which siblings does this MCP feed / consume)

  Use ASCII boxes or mermaid diagrams. No marketing graphics — this is
  for engineers and contributors.
-->

## Internal layout

```
┌──────────────────────────────────────────────────────────────────┐
│  User-facing surfaces                                            │
│  ┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  MCP server    │  │  CLI: <name>     │  │  Python API:     │ │
│  │  (FastMCP)     │  │  (Typer + Rich)  │  │  import <pkg>    │ │
│  └────────────────┘  └──────────────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────────┐
│  Orchestration                                                   │
│  • <!-- module -->                                               │
│  • <!-- module -->                                               │
│  • <!-- module -->                                               │
└──────────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────────┐
│  Kernels / backends                                              │
│  • <!-- kernel / external library / hardware backend -->         │
│  • <!-- kernel / external library / hardware backend -->         │
└──────────────────────────────────────────────────────────────────┘
```

<!-- 1–2 paragraphs explaining the layering. Mention any async patterns
     (e.g. SEP-1686 Tasks), caching, or hardware-locking conventions. -->

## Source layout

```
<!-- repo-name -->/
├── src/<!-- package_name -->/
│   ├── __init__.py
│   ├── <!-- module -->/
│   ├── mcp/         ← MCP server (FastMCP tool registrations)
│   ├── cli/         ← Typer commands
│   └── ...
├── tests/
├── docs/
└── assets/          ← logo-banner.svg, logo.svg
```

## Position in eng-mcp-suite

<!-- mcp-name --> sits in the **<!-- e.g. "inner loop / closed-form analysis" -->**
layer of the engineering MCP stack:

```
        ┌─────────────────────────────────────┐
        │   AI agent (Claude Code / Desktop)  │
        └──────┬──────────────┬───────────────┘
               │              │ via MCP
       ┌───────▼──────┐ ┌─────▼──────┐
       │ <!-- self --> │ │  sibling   │     ← which layer am I?
       └───────┬──────┘ └────────────┘
               │
       ┌───────▼──────────────────────┐
       │  downstream / consumer MCPs  │
       └──────────────────────────────┘
```

### Feeds (this MCP produces output that)…

- **<!-- sibling-mcp -->** — <!-- what artifact, what format -->
- **<!-- sibling-mcp -->** — <!-- what artifact, what format -->

### Consumes (this MCP accepts input from)…

- **<!-- sibling-mcp -->** — <!-- what artifact, what format -->
- **<!-- sibling-mcp -->** — <!-- what artifact, what format -->

### Workflow bundles that include this MCP

| Bundle                  | Role of this MCP                          |
| ----------------------- | ----------------------------------------- |
| `<!-- bundle-name -->`  | <!-- one-line role -->                    |
| `<!-- bundle-name -->`  | <!-- one-line role -->                    |

See the [suite manifest](https://github.com/RFingAdam/eng-mcp-suite/blob/main/manifest.yaml)
for full bundle definitions.

---

## Design decisions

<!--
  Brief log of non-obvious choices. Useful for contributors.
  Examples:
    - Why FastMCP over the official SDK
    - Why we chose <library> for <task>
    - Why <interface> is async / sync
    - Why we don't support <feature> (yet)
-->

- **<!-- decision -->** — <!-- one-paragraph rationale -->
- **<!-- decision -->** — <!-- one-paragraph rationale -->
