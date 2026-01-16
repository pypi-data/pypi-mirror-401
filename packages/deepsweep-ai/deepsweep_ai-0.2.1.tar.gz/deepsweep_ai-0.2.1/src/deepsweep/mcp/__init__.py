"""
DeepSweep MCP Security Module.

Provides discovery and validation of MCP configurations.

Usage in CLI:
- `deepsweep mcp list` - List discovered configs
- `deepsweep mcp validate` - Validate MCP configs
- `deepsweep validate --include-mcp` - Include MCP in main validation

Note: MCP is opt-in for v0.2.0, becomes default in v0.3.0.
"""

from .discovery import MCPConfig, discover, discover_with_servers
from .validator import MCPFinding, MCPValidationResult, validate, validate_all

__all__ = [
    "MCPConfig",
    "MCPFinding",
    "MCPValidationResult",
    "discover",
    "discover_with_servers",
    "validate",
    "validate_all",
]
