"""Badge generation for DeepSweep."""

import urllib.parse

import click

BADGE_COLORS = {"A": "brightgreen", "B": "green", "C": "yellow", "D": "orange", "F": "red"}


def generate_badge_url(score: int, grade: str) -> str:
    """Generate shields.io badge URL."""
    color = BADGE_COLORS.get(grade, "lightgrey")
    message = urllib.parse.quote(f"{grade} {score}/100")
    return f"https://img.shields.io/badge/DeepSweep-{message}-{color}"


def generate_markdown(score: int, grade: str) -> str:
    """Generate markdown badge."""
    return f"[![DeepSweep Validated]({generate_badge_url(score, grade)})](https://deepsweep.ai)"


def generate_html(score: int, grade: str) -> str:
    """Generate HTML badge."""
    url = generate_badge_url(score, grade)
    return f'<a href="https://deepsweep.ai"><img src="{url}" alt="DeepSweep Validated"></a>'


@click.command()
@click.option("--format", "output_format", type=click.Choice(["markdown", "html", "url"]), default="markdown")
@click.option("--score", type=int, default=100)
@click.option("--grade", type=str, default="A")
def badge(output_format: str, score: int, grade: str):
    """Generate a security badge for your repository."""
    if output_format == "markdown":
        output = generate_markdown(score, grade)
    elif output_format == "html":
        output = generate_html(score, grade)
    else:
        output = generate_badge_url(score, grade)

    click.echo(output)
    click.echo("", err=True)
    click.echo("Add this badge to your README.md", err=True)
