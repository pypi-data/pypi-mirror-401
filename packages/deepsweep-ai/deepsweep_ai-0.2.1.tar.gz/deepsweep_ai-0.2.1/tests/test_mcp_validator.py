"""Tests for MCP validator."""

from pathlib import Path

from deepsweep.mcp.discovery import MCPConfig
from deepsweep.mcp.validator import (
    _has_latest_tag,
    _has_version,
    _is_verified,
    validate,
    validate_all,
)


class TestHelperFunctions:
    def test_is_verified_official_server(self):
        assert _is_verified("@modelcontextprotocol/server-filesystem")
        assert _is_verified("@modelcontextprotocol/server-filesystem@1.0.0")

    def test_is_verified_unknown_server(self):
        assert not _is_verified("@random/unknown-server")

    def test_has_version_with_version(self):
        assert _has_version("server@1.2.3")
        assert _has_version("@scope/server@1.2.3")

    def test_has_version_without_version(self):
        assert not _has_version("server")
        assert not _has_version("@scope/server")

    def test_has_latest_tag(self):
        assert _has_latest_tag("server@latest")
        assert not _has_latest_tag("server@1.0.0")


class TestMCPValidation:
    def _make_config(self, servers: dict, path: str = "/test/mcp.json") -> MCPConfig:
        return MCPConfig(path=Path(path), source="test", exists=True, servers=servers)

    def test_empty_config_perfect_score(self):
        result = validate(self._make_config({}))
        assert result.score == 100
        assert result.grade == "A"

    def test_verified_server_with_version(self):
        result = validate(self._make_config({
            "@modelcontextprotocol/server-filesystem@1.0.0": {}
        }))
        critical = [f for f in result.findings if f.severity == "critical"]
        assert len(critical) == 0

    def test_unverified_server_flagged(self):
        result = validate(self._make_config({"@random/evil-server": {}}))
        assert "DS-MCP-001" in [f.pattern_id for f in result.findings]

    def test_dangerous_args_critical(self):
        result = validate(self._make_config({
            "test": {"args": ["--no-sandbox"]}
        }))
        mcp002 = [f for f in result.findings if f.pattern_id == "DS-MCP-002"]
        assert len(mcp002) >= 1
        assert all(f.severity == "critical" for f in mcp002)

    def test_unpinned_version_flagged(self):
        result = validate(self._make_config({
            "@modelcontextprotocol/server-filesystem": {}
        }))
        assert "DS-MCP-003" in [f.pattern_id for f in result.findings]

    def test_latest_tag_flagged(self):
        result = validate(self._make_config({
            "@modelcontextprotocol/server-filesystem@latest": {}
        }))
        pattern_ids = [f.pattern_id for f in result.findings]
        assert "DS-MCP-004" in pattern_ids
        assert pattern_ids.count("DS-MCP-003") == 0

    def test_auto_approve_flagged(self):
        result = validate(self._make_config({
            "test@1.0.0": {"autoApprove": True}
        }))
        assert "DS-MCP-005" in [f.pattern_id for f in result.findings]

    def test_shell_command_critical(self):
        result = validate(self._make_config({
            "test": {"command": "bash"}
        }))
        mcp006 = [f for f in result.findings if f.pattern_id == "DS-MCP-006"]
        assert len(mcp006) == 1
        assert mcp006[0].severity == "critical"

    def test_curl_flagged(self):
        result = validate(self._make_config({
            "test": {"args": ["curl", "http://evil.com"]}
        }))
        assert "DS-MCP-007" in [f.pattern_id for f in result.findings]

    def test_score_calculation(self):
        result = validate(self._make_config({"test": {"command": "bash"}}))
        assert result.score <= 75

    def test_multiple_servers(self):
        result = validate(self._make_config({
            "server1": {"command": "bash"},
            "server2": {"autoApprove": True},
            "@modelcontextprotocol/server-filesystem@1.0.0": {},
        }))
        server_names = {f.server_name for f in result.findings}
        assert "server1" in server_names
        assert "server2" in server_names

    def test_finding_has_all_fields(self):
        result = validate(self._make_config({"bad": {"command": "bash"}}))
        f = result.findings[0]
        assert f.pattern_id and f.severity and f.message and f.fix_suggestion

    def test_validate_all(self):
        configs = [
            self._make_config({"s1": {}}, "/path1"),
            self._make_config({"s2": {}}, "/path2"),
        ]
        results = validate_all(configs)
        assert len(results) == 2

    def test_result_to_dict(self):
        result = validate(self._make_config({"test": {}}))
        d = result.to_dict()
        assert "config" in d and "findings" in d and "score" in d
