<!--
  README template for any MCP in the eng-mcp-suite family.
  ========================================================
  Fill in every `<!-- placeholder -->` block. Delete sections that don't
  apply (e.g. drop the "Accuracy" table for non-numerical MCPs, drop the
  three-surfaces table if the MCP doesn't ship a Python API or CLI).

  Reference: https://github.com/RFingAdam/lineforge/blob/main/README.md
  Keep the density and tone the same. Tables, code blocks, no fluff.
-->

<div align="center">

<img src="assets/logo-banner.svg" alt="<!-- mcp-name --> — <!-- one-line description -->" width="100%"/>

<br/>

[![CI](https://github.com/RFingAdam/<!-- repo-name -->/actions/workflows/ci.yml/badge.svg)](https://github.com/RFingAdam/<!-- repo-name -->/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-<!-- e.g. GPLv3 or Apache--2.0 -->-1E40AF.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-3776AB.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-server-A78BFA.svg)](https://modelcontextprotocol.io)
[![eng-mcp-suite](https://img.shields.io/badge/eng--mcp--suite-member-22D3EE.svg)](https://github.com/RFingAdam/eng-mcp-suite)

**<!-- One-sentence value prop in bold. -->**
**<!-- Second sentence: from your X, terminal, or AI agent. -->**

[Quick start](#quick-start) ·
[Tools](#tools) ·
[Workflows](#workflows) ·
[Documentation](#documentation)

</div>

---

## What is <!-- mcp-name -->?

<!--
  2–3 paragraphs. Lead with what it computes / controls / exposes.
  Cite the standard or formula it implements. Name the surfaces
  (MCP, CLI, Python, etc.) explicitly. End with the validation / source
  status line.
-->

<!-- mcp-name --> is a <!-- short description -->. It <!-- what it does -->.

Drive it from <!-- list surfaces -->. <!-- Mention any compatibility or
reference standards (e.g. atlc2-compatible, IPC-2141A-validated,
SCPI-compliant, etc.) -->.

**What <!-- mcp-name --> does well:**

- 🤖 **AI-native via MCP.** First-class [Model Context Protocol](https://modelcontextprotocol.io)
  server with <!-- N --> tools. Any Claude / LLM agent can drive it.
- 🐍 **Multiple surfaces.** <!-- describe MCP + CLI + Python availability -->
- ⚡ **<!-- distinctive technical strength: e.g. closed-form fast path, SCPI-streamed, etc. -->**
- ✅ **Validated.** <!-- against what reference / standard -->.
- 🔒 **<!-- license -->.** <!-- one-line license summary -->.

---

## Quick start

### Install

```bash
pip install <!-- package-name -->
```

<!-- If pre-alpha / not on PyPI yet, replace with: -->
<!--
> Pre-alpha: not yet on PyPI. Install from the repo:
> ```bash
> git clone https://github.com/RFingAdam/<!-- repo-name -->.git
> cd <!-- repo-name -->
> pip install -e ".[dev]"
> ```
-->

### Three surfaces, same answer

<!--
  If your MCP only exposes 1–2 surfaces, drop the others and reflow.
  Keep code blocks compact — one realistic call per surface.
-->

<table>
<tr>
<td valign="top" width="50%">

**Python**

```python
import <!-- package-name -->

# <!-- one-line usage example -->
result = <!-- package_name -->.<!-- function -->(
    <!-- args -->
)
print(result)
```

</td>
<td valign="top" width="50%">

**CLI**

```bash
<!-- cli-name --> <!-- subcommand --> \
  --<!-- arg --> <!-- value -->

# JSON output for piping
<!-- cli-name --> <!-- subcommand --> \
  --output json | jq '.<!-- field -->'
```

</td>
</tr>
<tr>
<td colspan="2" valign="top">

**MCP (Claude Desktop, Claude Code, any MCP client)**

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "<!-- mcp-name -->": {
      "command": "<!-- cli-name -->",
      "args": ["mcp-serve"]
    }
  }
}
```

Then ask your assistant in plain English:

> *"<!-- realistic example prompt the user would write -->"*

The agent will call `<!-- tool_name -->` with the right arguments and report
the result.

</td>
</tr>
</table>

---

## Tools

<!--
  Table format: tool name, what it does, one-line argument summary.
  Group by category if there are more than ~8 tools.
  See lineforge for the right density.
-->

| Tool                       | Purpose                                  | Key arguments                    |
| -------------------------- | ---------------------------------------- | -------------------------------- |
| `<!-- tool_one -->`        | <!-- one-line description -->            | `<!-- arg1, arg2 -->`            |
| `<!-- tool_two -->`        | <!-- one-line description -->            | `<!-- arg1, arg2 -->`            |
| `<!-- tool_three -->`      | <!-- one-line description -->            | `<!-- arg1, arg2 -->`            |

Full tool reference in [`docs/tools.md`](docs/tools.md).

---

## What it solves

<!--
  Optional. Use this when the MCP wraps a domain (geometries, standards,
  instruments) where a capability table is more useful than prose.
  Drop this section entirely if the Tools table already says everything.
-->

| <!-- Category -->          | <!-- Inputs / Range -->         | <!-- Source / Standard -->          |
| -------------------------- | ------------------------------- | ----------------------------------- |
| <!-- row -->               | <!-- row -->                    | <!-- row -->                        |
| <!-- row -->               | <!-- row -->                    | <!-- row -->                        |

---

## Workflows

<!-- mcp-name --> fits in the following [eng-mcp-suite](https://github.com/RFingAdam/eng-mcp-suite)
workflow bundles:

- **`<!-- workflow-name -->`** — <!-- one-line description -->
- **`<!-- workflow-name -->`** — <!-- one-line description -->

See the [suite manifest](https://github.com/RFingAdam/eng-mcp-suite/blob/main/manifest.yaml)
for the full list of sibling MCPs and bundle definitions.

---

## Documentation

- 📘 **[Quick Start](docs/index.md)** — install through first call.
- 🛠️ **[Tool reference](docs/tools.md)** — every MCP tool, every argument.
- 📐 **[Usage examples](docs/usage.md)** — practical end-to-end walkthroughs.
- 🏗️ **[Architecture](docs/architecture.md)** — how this MCP fits in eng-mcp-suite.
- 📝 **[Changelog](CHANGELOG.md)**

Built with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/);
deploys to GitHub Pages on every push to `main`.

---

## Part of eng-mcp-suite

<!--
  This block is CONSTANT across every repo in the family.
  Copy verbatim; only update the per-MCP row in the table if needed.
-->

<sub>This MCP server is part of</sub>

[![eng-mcp-suite](https://img.shields.io/badge/eng--mcp--suite-engineering%20MCP%20catalog-22D3EE?style=for-the-badge)](https://github.com/RFingAdam/eng-mcp-suite)

<sub>An open umbrella for engineering MCP servers across RF, EMC, PCB,
signal integrity, EM simulation, and lab test. Same brand, same docs
structure, designed to compose. See the
[full catalog](https://github.com/RFingAdam/eng-mcp-suite#whats-included)
or jump to a sibling:</sub>

| Domain                    | Sibling MCPs                                                                 |
| ------------------------- | ---------------------------------------------------------------------------- |
| **RF / Transmission lines** | [lineforge](https://github.com/RFingAdam/lineforge)                        |
| **EMC regulatory**        | [mcp-emc-regulations](https://github.com/RFingAdam/mcp-emc-regulations)      |
| **PCB / SI**              | mcp-pcb-emcopilot *(private — public soon)*                                  |
| **EM simulation**         | mcp-openems, mcp-nec2-antenna *(private — public soon)*                      |
| **Diagrams**              | [drawio-engineering-mcp](https://github.com/RFingAdam/drawio-engineering-mcp) |
| **3D / rendering**        | [mcp-blender](https://github.com/RFingAdam/mcp-blender)                      |
| **Remote access**         | [mcp-remote-access](https://github.com/RFingAdam/mcp-remote-access)          |
| **Lab gear**              | [copper-mountain-vna-mcp](https://github.com/RFingAdam/copper-mountain-vna-mcp), mcp-rs-spectrum-analyzer, mcp-rs-siggen, mcp-rs-cmw500 |

---

## Contributing

Contributions are welcome.

1. **Pick a [GitHub issue](https://github.com/RFingAdam/<!-- repo-name -->/issues)**.
2. **Fork + branch** (`feature/your-thing` or `fix/your-bug`).
3. **Run the local check suite**:
   ```bash
   ruff check . && black --check . && mypy src/<!-- package_name -->
   pytest --cov=<!-- package_name -->
   ```
4. **Open a PR** — link the issue, request review.

Full contributor guide in [`CONTRIBUTING.md`](CONTRIBUTING.md). Participation
is governed by the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

---

## License

[<!-- license name -->](LICENSE).

## Acknowledgments

- **<!-- upstream author / project -->** — <!-- short description -->.
- **<!-- library / standard -->** — <!-- short description -->.
- **The MCP working group** — for the [Model Context Protocol](https://modelcontextprotocol.io) specification.

<div align="center">

<sub>Part of <a href="https://github.com/RFingAdam/eng-mcp-suite">eng-mcp-suite</a> — built for RF engineers, PCB designers, EMC labs, and AI agents.</sub>

</div>
