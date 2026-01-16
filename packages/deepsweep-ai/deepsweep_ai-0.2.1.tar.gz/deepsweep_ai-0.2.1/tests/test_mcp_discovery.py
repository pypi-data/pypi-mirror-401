"""Tests for MCP discovery."""

from pathlib import Path

from deepsweep.mcp.discovery import (
    MCPConfig,
    _get_system_paths,
    discover,
    discover_with_servers,
)


class TestMCPDiscovery:
    """Test MCP configuration discovery."""

    def test_discover_returns_list(self):
        configs = discover()
        assert isinstance(configs, list)

    def test_discover_includes_standard_sources(self):
        configs = discover()
        sources = {c.source for c in configs}
        assert "claude-desktop" in sources
        assert "cursor" in sources
        assert "windsurf" in sources

    def test_mcpconfig_properties(self):
        config = MCPConfig(
            path=Path("/test/mcp.json"),
            source="test",
            exists=True,
            servers={"server1": {}, "server2": {}},
        )
        assert config.server_count == 2
        assert "server1" in config.server_names

    def test_mcpconfig_to_dict(self):
        config = MCPConfig(
            path=Path("/test"),
            source="test",
            exists=True,
            servers={"s": {}},
        )
        d = config.to_dict()
        assert d["source"] == "test"
        assert d["server_count"] == 1

    def test_project_config_discovered(self, tmp_path):
        mcp_file = tmp_path / "mcp.json"
        mcp_file.write_text('{"mcpServers": {"test-server": {"command": "node"}}}')

        configs = discover(tmp_path)
        project_configs = [c for c in configs if c.source == "project"]

        assert len(project_configs) == 1
        assert "test-server" in project_configs[0].servers

    def test_invalid_json_handled(self, tmp_path):
        mcp_file = tmp_path / "mcp.json"
        mcp_file.write_text("not valid json {{{")

        configs = discover(tmp_path)
        project_configs = [c for c in configs if c.source == "project"]

        assert len(project_configs) == 1
        assert project_configs[0].error is not None

    def test_missing_file_not_error(self, tmp_path):
        configs = discover(tmp_path)
        assert all(c.error is None for c in configs if not c.exists)

    def test_discover_with_servers_filters(self, tmp_path):
        mcp_file = tmp_path / "mcp.json"
        mcp_file.write_text('{"mcpServers": {"s": {}}}')

        all_configs = discover(tmp_path)
        with_servers = discover_with_servers(tmp_path)

        assert len(with_servers) <= len(all_configs)
        assert all(c.server_count > 0 for c in with_servers)

    def test_nested_cursor_config(self, tmp_path):
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()
        mcp_file = cursor_dir / "mcp.json"
        mcp_file.write_text('{"mcpServers": {"nested": {}}}')

        configs = discover(tmp_path)
        project_configs = [c for c in configs if c.source == "project"]
        assert any("nested" in c.servers for c in project_configs)


class TestSystemPaths:
    def test_system_paths_returns_dict(self):
        paths = _get_system_paths()
        assert isinstance(paths, dict)
        assert "claude-desktop" in paths

    def test_paths_are_path_objects(self):
        paths = _get_system_paths()
        assert all(isinstance(p, Path) for p in paths.values())
