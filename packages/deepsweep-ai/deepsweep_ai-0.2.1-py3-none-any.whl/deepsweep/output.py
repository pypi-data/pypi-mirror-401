"""
CLI output formatting for DeepSweep.

Design Standards:
- NO EMOJIS - ASCII symbols only
- Optimistic messaging (Wiz approach)
- NO_COLOR support (per no-color.org)
- Collaborative, enabling tone
"""

import os
import sys
from dataclasses import dataclass

from deepsweep.constants import (
    DOCS_URL,
    PRODUCT_NAME,
    REMEDIATION_URL,
    SLOGAN,
    SYMBOL_FAIL,
    SYMBOL_INFO,
    SYMBOL_PASS,
    SYMBOL_SKIP,
    SYMBOL_WARN,
    TAGLINE,
    Colors,
)
from deepsweep.models import Finding, Severity, ValidationResult


def supports_color() -> bool:
    """
    Check if terminal supports color output.

    Respects NO_COLOR spec: https://no-color.org/
    """
    # NO_COLOR takes absolute precedence
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("DEEPSWEEP_NO_COLOR"):
        return False

    # Check if stdout is a TTY
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False

    # Dumb terminals don't support color
    return os.environ.get("TERM") != "dumb"


@dataclass
class OutputConfig:
    """Configuration for output formatting."""

    use_color: bool = True
    verbose: bool = False

    def __post_init__(self) -> None:
        """Auto-detect color support if enabled."""
        if self.use_color:
            self.use_color = supports_color()


class OutputFormatter:
    """
    Format CLI output with optimistic messaging.

    Design principles:
    - NO EMOJIS - ASCII symbols only
    - Collaborative tone ("let's" not "you must")
    - Focus on path forward, not doom
    - Celebrate success, don't just confirm
    """

    def __init__(self, config: OutputConfig | None = None) -> None:
        self.config = config or OutputConfig()

    def _colorize(self, text: str, severity: Severity) -> str:
        """Apply color to text if supported."""
        if not self.config.use_color:
            return text

        color_map = {
            Severity.CRITICAL: Colors.CRITICAL,
            Severity.HIGH: Colors.HIGH,
            Severity.MEDIUM: Colors.MEDIUM,
            Severity.LOW: Colors.LOW,
            Severity.INFO: Colors.INFO,
        }

        color = color_map.get(severity, "")
        return f"{color}{text}{Colors.RESET}"

    def _colorize_pass(self, text: str) -> str:
        """Apply pass (green) color."""
        if not self.config.use_color:
            return text
        return f"{Colors.PASS}{text}{Colors.RESET}"

    def format_header(self, version: str) -> str:
        """
        Format CLI header with branding.

        This is the first thing users see - set the optimistic tone.
        """
        return f"""
{PRODUCT_NAME} v{version}
{TAGLINE}
{SLOGAN}
"""

    def format_validation_start(self, path: str, pattern_count: int) -> str:
        """Format validation initialization message."""
        return f"""Validating {path}...
  {SYMBOL_INFO} Loaded {pattern_count} detection patterns
  {SYMBOL_INFO} Checking AI assistant configurations
"""

    def format_file_pass(self, file_path: str) -> str:
        """Format a passing file check."""
        text = f"{SYMBOL_PASS} {file_path}"
        return self._colorize_pass(text)

    def format_file_skip(self, file_path: str, reason: str) -> str:
        """Format a skipped file."""
        return f"{SYMBOL_SKIP} {file_path} ({reason})"

    def format_finding(self, finding: Finding) -> str:
        """
        Format a single finding.

        Note: We say "How to address" not "Fix this vulnerability"
        """
        symbol = (
            SYMBOL_FAIL if finding.severity in (Severity.CRITICAL, Severity.HIGH) else SYMBOL_WARN
        )

        header = f"{symbol} {finding.file_path}:{finding.line}"
        header = self._colorize(header, finding.severity)

        lines = [header]
        lines.append(f"  {finding.message}")
        lines.append(f"  > Pattern: {finding.pattern_id}")

        if finding.cve:
            lines.append(f"  > CVE: {finding.cve}")

        if finding.owasp:
            lines.append(f"  > OWASP: {finding.owasp}")

        if finding.remediation:
            # Optimistic framing: "How to address" not "Fix this"
            lines.append(f"  > How to address: {finding.remediation}")

        return "\n".join(lines)

    def format_summary(self, result: ValidationResult) -> str:
        """
        Format summary with optimistic messaging.

        Key decisions:
        - "items to review" NOT "vulnerabilities"
        - Grade with encouraging context
        - Focus on path forward
        """
        score = result.score
        grade = result.grade
        total = result.finding_count

        # Determine severity for coloring
        if score >= 90:
            status = "Your setup is validated"
            severity = Severity.INFO  # Will use pass color below
        elif score >= 70:
            status = "A few items to review"
            severity = Severity.MEDIUM
        else:
            status = "Some items need attention"
            severity = Severity.HIGH

        # Build score line
        score_text = f"Score: {score}/100 ({grade})"
        if score >= 90:
            score_line = self._colorize_pass(score_text)
        else:
            score_line = self._colorize(score_text, severity)

        # Optimistic finding count - "items to review" not "vulnerabilities"
        if total == 0:
            findings_line = "No items to review - ship with confidence!"
        elif total == 1:
            findings_line = "1 item to review"
        else:
            findings_line = f"{total} items to review"

        return f"""
---
{score_line}
{status}

{findings_line}
---"""

    def format_next_steps(self, result: ValidationResult) -> str:
        """
        Format next steps with encouraging guidance.

        Messaging:
        - Collaborative ("let's" not "you must")
        - Specific actions
        - Positive framing
        """
        if not result.has_findings:
            return f"""
Your AI assistant setup is secure. Here's what's next:

  * Add to CI/CD to keep it that way:
    deepsweep validate . --fail-on high

  * Generate a badge for your README:
    deepsweep badge --output badge.svg

  * Learn more: {DOCS_URL}
"""

        score = result.score
        if score < 50:
            intro = "Let's address the critical items first:"
        elif score < 70:
            intro = "Here's how to improve your score:"
        else:
            intro = "A few quick fixes will get you to 90+:"

        return f"""
{intro}

  * Review each finding above
  * Apply the suggested remediations
  * Re-run: deepsweep validate .

Need help? {REMEDIATION_URL}
"""

    def format_json_output(self, result: ValidationResult) -> str:
        """Format result as JSON."""
        import json

        data = {
            "version": "1.0.0",
            "score": result.score,
            "grade": result.grade_letter,
            "findings_count": result.finding_count,
            "pattern_count": result.pattern_count,
            "findings": [
                {
                    "severity": f.severity.value,
                    "file": f.file_path,
                    "line": f.line,
                    "message": f.message,
                    "pattern_id": f.pattern_id,
                    "cve": f.cve,
                    "owasp": f.owasp,
                    "remediation": f.remediation,
                }
                for f in result.all_findings
            ],
        }

        return json.dumps(data, indent=2)

    def format_sarif_output(self, result: ValidationResult) -> str:
        """Format result as SARIF 2.1.0 for GitHub Security tab."""
        import json

        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": PRODUCT_NAME,
                            "version": "1.0.0",
                            "informationUri": DOCS_URL,
                            "rules": [
                                {
                                    "id": f.pattern_id,
                                    "name": f.pattern_id,
                                    "shortDescription": {"text": f.message.split(":")[0]},
                                    "defaultConfiguration": {
                                        "level": self._sarif_level(f.severity)
                                    },
                                }
                                for f in result.all_findings
                            ],
                        }
                    },
                    "results": [
                        {
                            "ruleId": f.pattern_id,
                            "level": self._sarif_level(f.severity),
                            "message": {"text": f.message},
                            "locations": [
                                {
                                    "physicalLocation": {
                                        "artifactLocation": {"uri": f.file_path},
                                        "region": {"startLine": f.line},
                                    }
                                }
                            ],
                        }
                        for f in result.all_findings
                    ],
                }
            ],
        }

        return json.dumps(sarif, indent=2)

    def _sarif_level(self, severity: Severity) -> str:
        """Convert severity to SARIF level."""
        if severity in (Severity.CRITICAL, Severity.HIGH):
            return "error"
        elif severity == Severity.MEDIUM:
            return "warning"
        else:
            return "note"


# Additional utility functions for simplified CLI output

SEVERITY_STYLES = {
    "critical": {"fg": "red", "bold": True},
    "high": {"fg": "yellow", "bold": True},
    "medium": {"fg": "cyan", "bold": False},
    "low": {"fg": "white", "bold": False},
}

GRADE_COLORS = {"A": "green", "B": "green", "C": "yellow", "D": "red", "F": "red"}


def score_bar(score: int, width: int = 30) -> str:
    """Create a visual score bar."""
    try:
        import click
        filled = int((score / 100) * width)
        empty = width - filled
        color = "green" if score >= 80 else ("yellow" if score >= 60 else "red")
        bar = click.style("█" * filled, fg=color) + click.style("░" * empty, dim=True)
        return f"{bar} {score}/100"
    except ImportError:
        # Fallback if click is not available
        filled = int((score / 100) * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"{bar} {score}/100"


def format_grade(grade: str) -> str:
    """Format grade with color."""
    try:
        import click
        color = GRADE_COLORS.get(grade, "white")
        return click.style(grade, fg=color, bold=True)
    except ImportError:
        return grade


def format_finding(
    pattern_id: str,
    severity: str,
    message: str,
    file: str | None = None,
    line: int | None = None,
    fix_suggestion: str | None = None,
    show_fix: bool = False,
) -> list[str]:
    """Format a finding for display."""
    try:
        import click
        style = SEVERITY_STYLES.get(severity, SEVERITY_STYLES["medium"])
        lines = []

        severity_text = click.style(f"[{severity.upper()}]", fg=style["fg"], bold=style["bold"])
        location = f" ({file}:{line})" if file and line else (f" ({file})" if file else "")
        lines.append(f"  {severity_text} {pattern_id}: {message}{location}")

        if show_fix and fix_suggestion:
            lines.append(click.style(f"    > {fix_suggestion}", fg="green"))

        return lines
    except ImportError:
        lines = []
        severity_text = f"[{severity.upper()}]"
        location = f" ({file}:{line})" if file and line else (f" ({file})" if file else "")
        lines.append(f"  {severity_text} {pattern_id}: {message}{location}")
        if show_fix and fix_suggestion:
            lines.append(f"    > {fix_suggestion}")
        return lines


def print_summary(score: int, grade: str, finding_count: int, **_kwargs):
    """Print validation summary."""
    try:
        import click
        click.echo()
        click.echo(click.style("DEEPSWEEP Security Report", bold=True))
        click.echo("-" * 50)
        click.echo()
        click.echo(f"Score: {score_bar(score)}")
        click.echo(f"Grade: {format_grade(grade)}")
        click.echo()

        if finding_count == 0:
            click.echo(click.style("No security issues found", fg="green", bold=True))
        else:
            click.echo(f"Found {finding_count} issue(s)")
    except ImportError:
        print()
        print("DEEPSWEEP Security Report")
        print("-" * 50)
        print()
        print(f"Score: {score_bar(score)}")
        print(f"Grade: {format_grade(grade)}")
        print()
        if finding_count == 0:
            print("No security issues found")
        else:
            print(f"Found {finding_count} issue(s)")


def print_next_steps(score: int, has_fix_flag: bool = False):
    """Print next steps based on score."""
    try:
        import click
        click.echo()
        click.echo("-" * 50)

        if score == 100:
            click.echo(click.style("Your AI assistant configuration is secure.", fg="green"))
        elif score >= 80:
            click.echo("Good security posture. Address remaining issues when possible.")
        elif score >= 60:
            click.echo("Some issues need attention. Run with --fix for suggestions.")
        else:
            click.echo(click.style("Critical issues found. Address immediately.", fg="red"))

        if not has_fix_flag and score < 100:
            click.echo()
            click.echo("Run with " + click.style("--fix", bold=True) + " for remediation suggestions")
        click.echo()
    except ImportError:
        print()
        print("-" * 50)
        if score == 100:
            print("Your AI assistant configuration is secure.")
        elif score >= 80:
            print("Good security posture. Address remaining issues when possible.")
        elif score >= 60:
            print("Some issues need attention. Run with --fix for suggestions.")
        else:
            print("Critical issues found. Address immediately.")
        if not has_fix_flag and score < 100:
            print()
            print("Run with --fix for remediation suggestions")
        print()
