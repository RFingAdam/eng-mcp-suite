# Private MCP bolt-on

The eng-mcp-suite catalog ships only the **public** engineering MCPs plus
**commercial-software-gated** ones (HFSS, CST, R&S, etc. where the wrapper
is public but the underlying tool requires a license).

If you have your own private MCPs — internal company tools, licensed
bolt-ons, R&D experiments — you can add them via a **user-local manifest
file**. The suite merges your local additions with the public catalog at
runtime, only when you opt in.

## Quick start

1. Create the file:

   ```bash
   mkdir -p ~/.config/eng_mcp_suite
   $EDITOR ~/.config/eng_mcp_suite/private.yaml
   ```

2. Use the same schema as the bundled catalog. Minimal example:

   ```yaml
   mcps:
     - name: my-internal-tool
       description: Custom widget API for our internal CI.
       categories: [lab-test]
       repo: https://github.internal.example.com/myorg/widget-mcp
       status: private
       install:
         method: git
         package: git+ssh://git@github.internal.example.com/myorg/widget-mcp.git
       server_name: widget
   ```

   See [`private.yaml.example`](private.yaml.example) for a more complete
   template.

3. Opt in when listing or installing:

   ```bash
   eng-mcp-suite list   --include-private
   eng-mcp-suite install --workflow rf-design --include-private
   eng-mcp-suite config  --include-private --out ~/claude_desktop_config.json
   ```

That's it. Your private MCPs appear in the catalog only with the
`--include-private` flag — they are not visible by default and the public
suite documentation never references them.

## Resolution order

The suite finds your private manifest in this order:

1. `--private-manifest path/to/file.yaml` CLI flag (explicit override)
2. `ENG_MCP_SUITE_PRIVATE_MANIFEST=path/to/file.yaml` environment variable
3. `~/.config/eng_mcp_suite/private.yaml` (default)

## Schema

The private manifest uses the **same schema** as the bundled `manifest.yaml`:

```yaml
mcps:
  - name: <string, required, unique>
    description: |
      <multi-line free text>
    categories: [<rf | emc | pcb | em-sim | circuit-sim | mechanical | lab-test | docs>, ...]
    repo: <URL or git remote, required>
    status: <public | private | commercial | hardware>
    install:
      method: <pip | pipx | npm | git | manual>
      package: <package name or git URL, optional for "manual">
      install_notes: |
        <free text shown to user, optional>
    server_name: <string for Claude Desktop's mcpServers key>
```

## Override semantics

If your private manifest contains an entry with the **same `name`** as a
public catalog entry, the private entry **wins**. This is useful for:

- Pinning a specific version of an upstream MCP
- Pointing at a fork instead of upstream
- Adding install credentials/auth flags not appropriate for the public catalog

If you want to coexist, give your local fork a different name (e.g.
`mcp-openems-myfork`).

## What stays out of public documentation

The public catalog and this documentation never name specific private
MCPs. The example in [`private.yaml.example`](private.yaml.example) uses
generic placeholder names (`my-internal-tool`, `our-test-bench-mcp`, etc.)
so it never reveals internal tooling by reference.

If you're building public-facing documentation that mentions your bolt-on
MCPs, that documentation lives in your own private repo, not here.

## Sharing private manifests within a team

The CLI accepts a custom path:

```bash
eng-mcp-suite install --workflow rf-design \
  --include-private \
  --private-manifest /shared/team/eng-mcp-private.yaml
```

A team can commit a `private.yaml` to a shared private repo and each team
member points the CLI at it (via the env var or CLI flag). Updates flow
the same way you update any shared config — `git pull` then re-run the
install command.
