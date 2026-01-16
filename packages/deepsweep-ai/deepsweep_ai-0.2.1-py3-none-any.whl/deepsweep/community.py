"""Community engagement for DeepSweep."""

import random

import click

# Suggestions shown occasionally after successful scans
SUGGESTIONS = [
    "Like DeepSweep? Star us on GitHub: https://github.com/deepsweep-ai/deepsweep-cli",
    "Add a badge to your README: deepsweep badge >> README.md",
    "Join the discussion: https://github.com/deepsweep-ai/deepsweep-cli/discussions",
]

# Show suggestions occasionally, not every time
SUGGESTION_FREQUENCY = 0.3


def maybe_show_suggestion(_score: int, grade: str):
    """Occasionally show a community suggestion after successful validation."""
    if grade not in ("A", "B"):
        return
    if random.random() > SUGGESTION_FREQUENCY:
        return

    click.echo()
    click.echo(click.style("-" * 50, dim=True))
    click.echo(random.choice(SUGGESTIONS))
