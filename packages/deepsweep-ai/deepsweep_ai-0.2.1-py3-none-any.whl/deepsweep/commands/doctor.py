"""Doctor command for DeepSweep."""

import os
import sys
from pathlib import Path

import click


@click.command()
def doctor():
    """Check DeepSweep installation and environment health."""
    click.echo()
    click.echo(click.style("DeepSweep Health Check", bold=True))
    click.echo("-" * 40)
    click.echo()

    all_ok = True

    # Python version
    py = sys.version_info
    py_str = f"{py.major}.{py.minor}.{py.micro}"
    if py >= (3, 8):
        click.echo(click.style("[OK]", fg="green") + f" Python {py_str}")
    else:
        click.echo(click.style("[FAIL]", fg="red") + f" Python {py_str} (requires 3.8+)")
        all_ok = False

    # DeepSweep
    try:
        import deepsweep
        version = getattr(deepsweep, "__version__", "unknown")
        click.echo(click.style("[OK]", fg="green") + f" DeepSweep {version}")
    except ImportError:
        click.echo(click.style("[FAIL]", fg="red") + " DeepSweep not installed")
        all_ok = False

    import importlib.util

    # MCP module
    if importlib.util.find_spec("deepsweep.mcp"):
        click.echo(click.style("[OK]", fg="green") + " MCP module available")
    else:
        click.echo(click.style("[--]", fg="yellow") + " MCP module not available")

    # Environment
    click.echo()
    click.echo(click.style("Environment:", bold=True))

    if os.environ.get("DO_NOT_TRACK"):
        click.echo(click.style("[--]", fg="yellow") + " DO_NOT_TRACK set (telemetry disabled)")
    else:
        click.echo(click.style("[OK]", fg="green") + " Telemetry enabled (anonymous)")

    if os.environ.get("CI"):
        click.echo(click.style("[--]", fg="cyan") + " Running in CI environment")

    # Config files
    click.echo()
    click.echo(click.style("Current Directory:", bold=True))

    cwd = Path.cwd()
    found = False
    for name in [".cursorrules", ".windsurfrules", "AGENTS.md", "mcp.json"]:
        if (cwd / name).exists():
            found = True
            click.echo(click.style("[OK]", fg="green") + f" {name}")

    if not found:
        click.echo(click.style("[--]", fg="yellow") + " No AI config files found")
        click.echo("  Run: deepsweep init")

    # Summary
    click.echo()
    click.echo("-" * 40)
    if all_ok:
        click.echo(click.style("[OK] All checks passed", fg="green", bold=True))
    else:
        click.echo(click.style("[WARN] Some issues found", fg="yellow", bold=True))
    click.echo()
