# Usage

<!--
  ONE practical end-to-end example. Not a feature catalog — the README and
  Tools page cover that. This is a story: "you have this problem, here is
  how this MCP fits, here's the conversation, here's the answer."

  Aim for ~150–250 lines. Include real numbers and real tool outputs.
-->

This page walks one realistic scenario from problem to result. For the
full tool reference, see [Tools](tools.md).

---

## Scenario: <!-- one-line problem statement -->

<!-- 1–2 paragraph setup. Who are you, what do you need to know, why does
     this MCP help. -->

## Setup

```bash
pip install <!-- package-name -->
```

Register the MCP server with Claude Desktop / Claude Code by adding to
`claude_desktop_config.json`:

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

Restart your MCP client.

## Step 1 — <!-- first action -->

Ask the assistant:

> *"<!-- realistic prompt -->"*

The agent calls `<!-- tool_name -->` with:

```json
{ "<!-- arg -->": "<!-- value -->" }
```

It returns:

```json
{ "<!-- field -->": "<!-- value -->" }
```

<!-- 1-paragraph interpretation of the result. -->

## Step 2 — <!-- second action -->

<!-- repeat for 3–5 steps that build on each other -->

## Step 3 — <!-- final action that closes the loop -->

<!-- end on a concrete answer or artifact -->

---

## What just happened

<!-- 1-paragraph recap of why this workflow matters and what to read next. -->

- For more tools: [Tool reference](tools.md)
- For how this fits in the suite: [Architecture](architecture.md)
- For sibling MCPs that compose with this one: [eng-mcp-suite catalog](https://github.com/RFingAdam/eng-mcp-suite#whats-included)
