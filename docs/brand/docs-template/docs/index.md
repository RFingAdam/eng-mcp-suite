# <!-- mcp-name -->

<!--
  This is the docs landing page. It should mirror the top of the README —
  one-line hero, value-prop paragraph, quick install, link to Tools page.
  Keep it tighter than the README; this is the menu, not the meal.
-->

**<!-- One-sentence value prop. -->**
**<!-- Second sentence: from your X, terminal, or AI agent. -->**

---

## What it is

<!-- 2-3 sentence elevator pitch. Same paragraph as the README's "What is" section. -->

## Install

```bash
pip install <!-- package-name -->
```

## First call

=== "MCP"

    Add to `claude_desktop_config.json`:

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

    Then ask your assistant:

    > *"<!-- realistic prompt -->"*

=== "Python"

    ```python
    import <!-- package_name -->

    result = <!-- package_name -->.<!-- function -->(<!-- args -->)
    print(result)
    ```

=== "CLI"

    ```bash
    <!-- cli-name --> <!-- subcommand --> --<!-- arg --> <!-- value -->
    ```

## Where to next

- [Tool reference](tools.md) — every MCP tool with arguments
- [Usage examples](usage.md) — one practical end-to-end walkthrough
- [Architecture](architecture.md) — how this MCP fits inside eng-mcp-suite

---

!!! note "Part of eng-mcp-suite"
    This MCP server is part of [eng-mcp-suite](https://github.com/RFingAdam/eng-mcp-suite) —
    an umbrella of engineering MCP servers across RF, EMC, PCB, signal
    integrity, EM simulation, and lab test. Same brand, same docs
    structure, designed to compose.
