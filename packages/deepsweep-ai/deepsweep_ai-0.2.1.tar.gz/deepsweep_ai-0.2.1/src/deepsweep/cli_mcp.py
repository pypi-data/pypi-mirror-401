"""
MCP CLI commands for DeepSweep.

These are NEW commands that don't affect existing behavior.
Import and register in main cli.py.
"""

import json
from pathlib import Path

import click

from deepsweep.mcp import discovery, validator


@click.group()
def mcp():
    """MCP security commands (Model Context Protocol)."""
    pass


@mcp.command("list")
def mcp_list():
    """List discovered MCP configurations."""
    configs = discovery.discover(Path.cwd())

    click.echo()
    click.echo(click.style("MCP Configuration Discovery", bold=True))
    click.echo("─" * 45)

    found_any = False

    for config in configs:
        if config.exists:
            found_any = True
            status = click.style("✓ FOUND", fg="green")
            click.echo(f"\n{config.source}: {status}")
            click.echo(f"  Path: {config.path}")

            if config.error:
                click.echo(click.style(f"  Error: {config.error}", fg="red"))
            elif config.servers:
                click.echo(f"  Servers ({config.server_count}):")
                for name in list(config.server_names)[:5]:
                    click.echo(f"    • {name}")
                if config.server_count > 5:
                    click.echo(f"    ... and {config.server_count - 5} more")
            else:
                click.echo(click.style("  No servers configured", dim=True))
        else:
            status = click.style("not found", dim=True)
            click.echo(f"\n{config.source}: {status}")

    click.echo()

    if not found_any:
        click.echo("No MCP configurations found.")
        click.echo("\nMCP configs are typically located at:")
        click.echo("  • ~/.cursor/mcp.json")
        click.echo("  • ./mcp.json (project level)")
        click.echo("  • ~/Library/Application Support/Claude/claude_desktop_config.json")


@mcp.command("validate")
@click.option("--fix", is_flag=True, help="Show fix suggestions")
@click.option("--format", "output_format",
              type=click.Choice(["text", "json"]), default="text",
              help="Output format")
def mcp_validate(fix: bool, output_format: str):
    """Validate MCP configurations for security issues.

    Checks for 7 security patterns including unverified servers,
    dangerous arguments, and shell command execution.
    """
    configs = discovery.discover_with_servers(Path.cwd())

    if not configs:
        if output_format == "json":
            click.echo(json.dumps({"results": [], "total_findings": 0}))
        else:
            click.echo("No MCP configurations with servers found.")
        return

    results = validator.validate_all(configs)

    if output_format == "json":
        output = {
            "results": [r.to_dict() for r in results],
            "total_findings": sum(len(r.findings) for r in results),
        }
        click.echo(json.dumps(output, indent=2))
        return

    total_findings = 0

    for result in results:
        config = result.config

        click.echo(f"\n{config.source}: {config.path}")
        click.echo(f"  Servers: {config.server_count}")

        score_color = "green" if result.score >= 80 else ("yellow" if result.score >= 60 else "red")
        click.echo("  Score: " + click.style(f"{result.score}/100 ({result.grade})", fg=score_color))

        if result.findings:
            click.echo(f"  Issues: {len(result.findings)}")

            for finding in result.findings:
                color = {"critical": "red", "high": "yellow", "medium": "cyan", "low": "white"}.get(finding.severity, "white")
                icon = "●" if finding.severity in ("critical", "high") else "○"
                click.echo(click.style(f"    {icon} [{finding.severity.upper()}] {finding.message}", fg=color))

                if fix:
                    click.echo(click.style(f"      → {finding.fix_suggestion}", fg="green"))

            total_findings += len(result.findings)
        else:
            click.echo(click.style("  ✓ No issues found", fg="green"))

    click.echo()
    click.echo("─" * 45)

    if total_findings == 0:
        click.echo(click.style("✓ All MCP configurations secure", fg="green", bold=True))
    else:
        click.echo(f"Total: {total_findings} issue(s) across {len(results)} config(s)")
        if not fix:
            click.echo("\nRun with --fix to see remediation suggestions")

    click.echo()
