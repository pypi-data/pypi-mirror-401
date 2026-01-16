"""
MCP configuration discovery.

Automatically finds MCP configs across all standard locations.
Supports Claude Desktop, Cursor, Windsurf on macOS/Linux/Windows.
"""

import json
import os
import platform
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MCPConfig:
    """A discovered MCP configuration."""

    path: Path
    source: str
    exists: bool
    servers: dict[str, dict] = field(default_factory=dict)
    error: str | None = None

    @property
    def server_count(self) -> int:
        return len(self.servers)

    @property
    def server_names(self) -> list[str]:
        return list(self.servers.keys())

    def to_dict(self) -> dict:
        return {
            "path": str(self.path),
            "source": self.source,
            "exists": self.exists,
            "servers": self.servers,
            "server_count": self.server_count,
            "error": self.error,
        }


def _get_home() -> Path:
    """Get user home directory."""
    return Path.home()


def _get_system_paths() -> dict[str, Path]:
    """Get standard MCP config paths for current OS."""
    home = _get_home()
    system = platform.system()

    if system == "Darwin":
        return {
            "claude-desktop": home / "Library/Application Support/Claude/claude_desktop_config.json",
            "cursor": home / ".cursor/mcp.json",
            "windsurf": home / ".windsurf/mcp.json",
        }
    elif system == "Windows":
        appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
        return {
            "claude-desktop": appdata / "Claude/claude_desktop_config.json",
            "cursor": home / ".cursor/mcp.json",
            "windsurf": home / ".windsurf/mcp.json",
        }
    else:
        config_home = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        return {
            "claude-desktop": config_home / "Claude/claude_desktop_config.json",
            "cursor": home / ".cursor/mcp.json",
            "windsurf": home / ".windsurf/mcp.json",
        }


def _parse_mcp_file(path: Path) -> tuple[dict[str, dict], str | None]:
    """Parse MCP config file and extract servers."""
    try:
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)
        servers = data.get("mcpServers", data.get("mcp_servers", {}))
        return servers, None
    except FileNotFoundError:
        return {}, None
    except json.JSONDecodeError as e:
        return {}, f"Invalid JSON at line {e.lineno}"
    except PermissionError:
        return {}, "Permission denied"
    except Exception as e:
        return {}, str(e)


def _find_project_configs(project_path: Path) -> list[Path]:
    """Find project-level MCP configs."""
    candidates = [
        project_path / "mcp.json",
        project_path / ".mcp/config.json",
        project_path / ".cursor/mcp.json",
        project_path / ".mcp.json",
    ]
    return [p for p in candidates if p.exists()]


def discover(project_path: Path | None = None) -> list[MCPConfig]:
    """
    Discover all MCP configurations.

    Args:
        project_path: Optional project directory to search

    Returns:
        List of MCPConfig objects (both found and not found)
    """
    configs: list[MCPConfig] = []

    for source, path in _get_system_paths().items():
        exists = path.exists()
        servers, error = _parse_mcp_file(path) if exists else ({}, None)
        configs.append(MCPConfig(
            path=path,
            source=source,
            exists=exists,
            servers=servers,
            error=error,
        ))

    if project_path:
        project_path = Path(project_path)
        for path in _find_project_configs(project_path):
            servers, error = _parse_mcp_file(path)
            configs.append(MCPConfig(
                path=path,
                source="project",
                exists=True,
                servers=servers,
                error=error,
            ))

    return configs


def discover_with_servers(project_path: Path | None = None) -> list[MCPConfig]:
    """Discover only configs that have servers defined."""
    return [c for c in discover(project_path) if c.exists and c.servers]
