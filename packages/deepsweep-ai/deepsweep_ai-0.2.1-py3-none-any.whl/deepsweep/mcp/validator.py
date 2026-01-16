"""
MCP configuration security validation.

Validates MCP server configurations against 7 security patterns.
"""

import re
from dataclasses import dataclass, field

from .discovery import MCPConfig

VERIFIED_SERVERS: set[str] = {
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-github",
    "@modelcontextprotocol/server-gitlab",
    "@modelcontextprotocol/server-google-drive",
    "@modelcontextprotocol/server-slack",
    "@modelcontextprotocol/server-memory",
    "@modelcontextprotocol/server-postgres",
    "@modelcontextprotocol/server-sqlite",
    "@modelcontextprotocol/server-brave-search",
    "@modelcontextprotocol/server-puppeteer",
    "@modelcontextprotocol/server-fetch",
    "@modelcontextprotocol/server-everything",
    "@modelcontextprotocol/server-sequential-thinking",
}

DANGEROUS_ARGS: list[str] = [
    "--allow-all", "--no-sandbox", "--disable-security",
    "--privileged", "--allow-write", "--allow-net",
    "--allow-run", "--allow-env", "--allow-read=/", "--allow-write=/",
]

SHELL_COMMANDS: set[str] = {"bash", "sh", "zsh", "cmd", "cmd.exe", "powershell", "pwsh"}
EXFIL_TOOLS: set[str] = {"curl", "wget", "nc", "netcat", "ncat", "telnet"}


@dataclass
class MCPFinding:
    """A security finding in MCP configuration."""

    pattern_id: str
    severity: str
    message: str
    file: str
    server_name: str
    fix_suggestion: str
    line: int | None = None
    evidence: str | None = None

    def to_dict(self) -> dict:
        return {
            "pattern_id": self.pattern_id,
            "severity": self.severity,
            "message": self.message,
            "file": self.file,
            "server_name": self.server_name,
            "fix_suggestion": self.fix_suggestion,
            "line": self.line,
            "evidence": self.evidence,
        }


@dataclass
class MCPValidationResult:
    """Result of MCP validation for one config."""

    config: MCPConfig
    findings: list[MCPFinding] = field(default_factory=list)

    @property
    def score(self) -> int:
        if not self.findings:
            return 100
        weights = {"critical": 25, "high": 15, "medium": 10, "low": 5}
        total = sum(weights.get(f.severity, 10) for f in self.findings)
        return max(0, 100 - total)

    @property
    def grade(self) -> str:
        s = self.score
        if s >= 90:
            return "A"
        if s >= 80:
            return "B"
        if s >= 70:
            return "C"
        if s >= 60:
            return "D"
        return "F"

    def to_dict(self) -> dict:
        return {
            "config": self.config.to_dict(),
            "findings": [f.to_dict() for f in self.findings],
            "score": self.score,
            "grade": self.grade,
        }


def _extract_base_name(server_name: str) -> str:
    parts = server_name.split("@")
    if len(parts) >= 3 and parts[0] == "":
        return "@" + parts[1]
    elif len(parts) == 2 and parts[0] == "":
        return server_name
    elif len(parts) == 2 and parts[0] != "":
        return parts[0]
    return server_name


def _is_verified(server_name: str) -> bool:
    base = _extract_base_name(server_name)
    return base in VERIFIED_SERVERS


def _has_version(server_name: str) -> bool:
    return bool(re.search(r"@[\^~]?\d+\.\d+(\.\d+)?$", server_name))


def _has_latest_tag(server_name: str) -> bool:
    return server_name.lower().endswith("@latest")


def validate(config: MCPConfig) -> MCPValidationResult:
    """Validate MCP configuration for security issues."""
    findings: list[MCPFinding] = []
    file_path = str(config.path)

    for server_name, server_config in config.servers.items():
        server_config = server_config or {}

        if not _is_verified(server_name):
            findings.append(MCPFinding(
                pattern_id="DS-MCP-001",
                severity="high",
                message=f"Unverified MCP server: {server_name}",
                file=file_path,
                server_name=server_name,
                fix_suggestion="Use @modelcontextprotocol/* servers or verify source",
            ))

        if not _has_version(server_name) and not _has_latest_tag(server_name):
            findings.append(MCPFinding(
                pattern_id="DS-MCP-003",
                severity="medium",
                message=f"MCP server without pinned version: {server_name}",
                file=file_path,
                server_name=server_name,
                fix_suggestion="Pin version: @server-name@1.2.3",
            ))

        if _has_latest_tag(server_name):
            findings.append(MCPFinding(
                pattern_id="DS-MCP-004",
                severity="high",
                message=f"Using @latest tag: {server_name}",
                file=file_path,
                server_name=server_name,
                fix_suggestion="Pin specific version instead of @latest",
            ))

        command = str(server_config.get("command", "")).lower()
        args = server_config.get("args", [])
        if isinstance(args, str):
            args = [args]
        args_str = " ".join(str(a) for a in args).lower()

        for dangerous in DANGEROUS_ARGS:
            if dangerous.lower() in args_str:
                findings.append(MCPFinding(
                    pattern_id="DS-MCP-002",
                    severity="critical",
                    message=f"Dangerous argument: {dangerous}",
                    file=file_path,
                    server_name=server_name,
                    fix_suggestion="Remove or scope down permissions",
                    evidence=dangerous,
                ))

        auto_approve_keys = ["autoApprove", "alwaysAllow", "auto_approve", "always_allow"]
        for key in auto_approve_keys:
            if server_config.get(key):
                findings.append(MCPFinding(
                    pattern_id="DS-MCP-005",
                    severity="high",
                    message=f"Auto-approval enabled: {key}",
                    file=file_path,
                    server_name=server_name,
                    fix_suggestion="Disable auto-approve for manual review",
                ))
                break

        if command in SHELL_COMMANDS:
            findings.append(MCPFinding(
                pattern_id="DS-MCP-006",
                severity="critical",
                message=f"Shell command execution: {command}",
                file=file_path,
                server_name=server_name,
                fix_suggestion="Use specific binary instead of shell interpreter",
                evidence=command,
            ))

        for tool in EXFIL_TOOLS:
            if tool in command or tool in args_str:
                findings.append(MCPFinding(
                    pattern_id="DS-MCP-007",
                    severity="critical",
                    message=f"Network exfiltration risk: {tool}",
                    file=file_path,
                    server_name=server_name,
                    fix_suggestion="Remove network tools from MCP server configuration",
                    evidence=tool,
                ))

    return MCPValidationResult(config=config, findings=findings)


def validate_all(configs: list[MCPConfig]) -> list[MCPValidationResult]:
    """Validate multiple MCP configurations."""
    return [validate(c) for c in configs if c.exists and c.servers]
