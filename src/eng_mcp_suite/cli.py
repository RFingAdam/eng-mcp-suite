"""eng-mcp-suite CLI."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from eng_mcp_suite import __version__
from eng_mcp_suite.installer import generate_claude_desktop_config, install_entry
from eng_mcp_suite.manifest import WORKFLOWS, load_manifest
from eng_mcp_suite.private_manifest import (
    DEFAULT_PRIVATE_PATH,
    load_merged_manifest,
)

app = typer.Typer(
    name="eng-mcp-suite",
    help="All-inclusive engineering MCP installer and catalog.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


STATUS_STYLE = {
    "public": "[green]public[/green]",
    "private": "[yellow]private[/yellow]",
    "commercial": "[blue]commercial[/blue]",
    "hardware": "[magenta]hardware[/magenta]",
}


def _status_str(status: str) -> str:
    return STATUS_STYLE.get(status, status)


@app.command()
def version() -> None:
    """Show eng-mcp-suite version."""
    console.print(f"eng-mcp-suite {__version__}")


@app.command(name="list")
def list_cmd(
    status: Annotated[str | None, typer.Option(help="Filter by status: public, private, commercial, hardware")] = None,
    category: Annotated[str | None, typer.Option(help="Filter by category: rf, emc, pcb, em-sim, circuit-sim, mechanical, lab-test, docs")] = None,
    workflow: Annotated[str | None, typer.Option(help=f"Filter by workflow bundle: {', '.join(WORKFLOWS.keys())}")] = None,
    include_private: Annotated[bool, typer.Option("--include-private", help=f"Also include entries from {DEFAULT_PRIVATE_PATH}")] = False,
    private_manifest: Annotated[Path | None, typer.Option(help="Override path to the private manifest file")] = None,
) -> None:
    """List MCPs in the catalog."""
    mf = load_merged_manifest(include_private=include_private, private_path=private_manifest)
    entries = mf.mcps

    if workflow:
        if workflow not in WORKFLOWS:
            console.print(f"[red]Unknown workflow:[/red] {workflow}")
            console.print(f"Available: {', '.join(WORKFLOWS.keys())}")
            raise typer.Exit(2)
        wanted = WORKFLOWS[workflow]
        entries = [e for e in entries if e.name in wanted]

    if status:
        entries = [e for e in entries if e.status == status]

    if category:
        entries = [e for e in entries if category in e.categories]

    table = Table(title=f"eng-mcp-suite catalog ({len(entries)} entries)", show_lines=False)
    table.add_column("Name", style="bold")
    table.add_column("Status")
    table.add_column("Method")
    table.add_column("Categories")
    table.add_column("Description", overflow="fold")

    for e in entries:
        table.add_row(
            e.name,
            _status_str(e.status),
            e.install.method,
            ", ".join(e.categories),
            e.description.strip().splitlines()[0],
        )

    console.print(table)


@app.command()
def show(name: str) -> None:
    """Show detail for one MCP."""
    mf = load_manifest()
    e = mf.by_name(name)
    if not e:
        console.print(f"[red]Not in catalog:[/red] {name}")
        raise typer.Exit(1)

    console.print(
        Panel.fit(
            f"[bold]{e.name}[/bold]  ({_status_str(e.status)})\n"
            f"Repo: {e.repo}\n"
            f"Categories: {', '.join(e.categories)}\n"
            f"Server name in Claude Desktop: [cyan]{e.server_name}[/cyan]\n"
            f"Install: {e.install.method}"
            + (f" {e.install.package}" if e.install.package else "")
            + "\n\n"
            + e.description.strip(),
            title="MCP detail",
        )
    )


@app.command()
def install(
    names: Annotated[list[str] | None, typer.Argument(help="MCP names to install")] = None,
    workflow: Annotated[str | None, typer.Option(help=f"Install a workflow bundle: {', '.join(WORKFLOWS.keys())}")] = None,
    public_only: Annotated[bool, typer.Option(help="Only install public MCPs")] = True,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print install commands without running them")] = False,
    include_private: Annotated[bool, typer.Option("--include-private", help=f"Also include entries from {DEFAULT_PRIVATE_PATH}")] = False,
    private_manifest: Annotated[Path | None, typer.Option(help="Override path to the private manifest file")] = None,
) -> None:
    """Install one or more MCPs."""
    mf = load_merged_manifest(include_private=include_private, private_path=private_manifest)
    wanted_names: list[str] = []

    if workflow:
        if workflow not in WORKFLOWS:
            console.print(f"[red]Unknown workflow:[/red] {workflow}")
            raise typer.Exit(2)
        wanted_names.extend(WORKFLOWS[workflow])

    if names:
        wanted_names.extend(names)

    if not wanted_names:
        console.print("[red]Specify --workflow or pass MCP names as arguments.[/red]")
        raise typer.Exit(2)

    entries = [mf.by_name(n) for n in wanted_names]
    missing = [n for n, e in zip(wanted_names, entries, strict=False) if e is None]
    if missing:
        console.print(f"[red]Unknown MCPs:[/red] {', '.join(missing)}")
        raise typer.Exit(2)

    entries = [e for e in entries if e is not None]

    if public_only:
        skipped = [e.name for e in entries if e.status != "public"]
        entries = [e for e in entries if e.status == "public"]
        if skipped:
            console.print(
                f"[yellow]Skipping non-public:[/yellow] {', '.join(skipped)} "
                f"(use --no-public-only to attempt anyway)"
            )

    if not entries:
        console.print("[yellow]Nothing public to install.[/yellow]")
        return

    console.print(f"[bold]Installing {len(entries)} MCP(s)...[/bold]")
    results = [install_entry(e, dry_run=dry_run) for e in entries]

    table = Table(show_lines=False)
    table.add_column("Name", style="bold")
    table.add_column("Result")
    table.add_column("Detail", overflow="fold")
    for r in results:
        marker = "[green]✓[/green]" if r.success else "[red]✗[/red]"
        table.add_row(r.name, marker, r.message)
    console.print(table)

    failed = [r for r in results if not r.success]
    if failed and not dry_run:
        raise typer.Exit(1)


@app.command()
def config(
    workflow: Annotated[str | None, typer.Option(help=f"Generate config for a workflow: {', '.join(WORKFLOWS.keys())}")] = None,
    public_only: Annotated[bool, typer.Option(help="Only include public MCPs")] = True,
    output: Annotated[Path | None, typer.Option("--out", "-o", help="Write to file instead of stdout")] = None,
    include_private: Annotated[bool, typer.Option("--include-private", help=f"Also include entries from {DEFAULT_PRIVATE_PATH}")] = False,
    private_manifest: Annotated[Path | None, typer.Option(help="Override path to the private manifest file")] = None,
) -> None:
    """Generate a Claude Desktop mcpServers config snippet for the chosen MCPs.

    Output goes to stdout by default, or --out path for a file. Merge into
    your existing ~/Library/Application Support/Claude/claude_desktop_config.json
    or ~/.config/claude/claude_desktop_config.json.
    """
    mf = load_merged_manifest(include_private=include_private, private_path=private_manifest)

    if workflow:
        if workflow not in WORKFLOWS:
            console.print(f"[red]Unknown workflow:[/red] {workflow}")
            raise typer.Exit(2)
        entries = [mf.by_name(n) for n in WORKFLOWS[workflow]]
        entries = [e for e in entries if e is not None]
    else:
        entries = mf.mcps

    if public_only:
        entries = [e for e in entries if e.status == "public"]

    snippet = generate_claude_desktop_config(entries)
    text = json.dumps(snippet, indent=2)

    if output:
        output.write_text(text + "\n")
        console.print(f"[green]Wrote {len(entries)} MCP entries to[/green] {output}")
    else:
        console.print(text)


@app.command()
def workflows() -> None:
    """List available workflow bundles."""
    table = Table(title="Workflow bundles")
    table.add_column("Workflow", style="bold")
    table.add_column("Includes")
    for name, members in WORKFLOWS.items():
        table.add_row(name, ", ".join(members))
    console.print(table)


if __name__ == "__main__":
    app()
