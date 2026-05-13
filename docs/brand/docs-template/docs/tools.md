# Tools

<!--
  This page is the authoritative MCP tool reference. One H2 per tool.
  Document EVERY argument, including defaults and units. Be terse;
  this page is read while debugging, not while browsing.

  Structure for each tool:
    ## tool_name
    One-line purpose statement.
    **Arguments:** table
    **Returns:** table
    **Example call:** code block (JSON or Python)
    **Notes:** any caveats / standards / accuracy bounds
-->

This page documents every MCP tool the server exposes. Tools are
registered under the `<!-- mcp-name -->` namespace when the server is
loaded by an MCP client.

## Tool index

| Tool                       | Purpose                                  |
| -------------------------- | ---------------------------------------- |
| [`<!-- tool_one -->`](#-- tool_one --)        | <!-- one-line description -->  |
| [`<!-- tool_two -->`](#-- tool_two --)        | <!-- one-line description -->  |
| [`<!-- tool_three -->`](#-- tool_three --)    | <!-- one-line description -->  |

---

## <!-- tool_one -->

<!-- One-line purpose. -->

**Arguments**

| Name                | Type                  | Default     | Description                          |
| ------------------- | --------------------- | ----------- | ------------------------------------ |
| `<!-- arg -->`      | `<!-- type -->`       | `<!-- d -->` | <!-- description -->                |
| `<!-- arg -->`      | `<!-- type -->`       | `<!-- d -->` | <!-- description -->                |

**Returns**

| Field               | Type                  | Description                          |
| ------------------- | --------------------- | ------------------------------------ |
| `<!-- field -->`    | `<!-- type -->`       | <!-- description -->                 |

**Example call**

```json
{
  "method": "tools/call",
  "params": {
    "name": "<!-- tool_one -->",
    "arguments": { "<!-- arg -->": "<!-- value -->" }
  }
}
```

**Notes**

- <!-- caveat, accuracy bound, citation, or "none" -->

---

## <!-- tool_two -->

<!-- repeat the same block structure for every tool -->

---

## Long-running tools (async)

<!--
  If your MCP has tools that take >5s and use SEP-1686 Tasks, list them
  here with their expected runtime. Otherwise delete this section.
-->

| Tool                       | Typical runtime    | Polled via                       |
| -------------------------- | ------------------ | -------------------------------- |
| `<!-- async_tool -->`      | <!-- e.g. 5–60s --> | `tasks_get` per [SEP-1686](https://modelcontextprotocol.io/seps/1686-tasks.md) |
