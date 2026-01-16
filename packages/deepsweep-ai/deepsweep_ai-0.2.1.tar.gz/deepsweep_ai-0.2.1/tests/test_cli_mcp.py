"""Tests for MCP CLI commands."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from deepsweep.cli_mcp import mcp


class TestMCPCommands:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_mcp_list_runs(self, runner):
        result = runner.invoke(mcp, ["list"])
        assert result.exit_code == 0
        assert "MCP Configuration Discovery" in result.output

    def test_mcp_validate_no_configs(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(mcp, ["validate"])
            assert result.exit_code == 0
            assert "No MCP configurations" in result.output

    def test_mcp_validate_with_config(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            Path("mcp.json").write_text(json.dumps({
                "mcpServers": {"@random/bad": {"command": "bash"}}
            }))
            result = runner.invoke(mcp, ["validate"])
            assert result.exit_code == 0
            assert "DS-MCP" in result.output or "issue" in result.output.lower()

    def test_mcp_validate_json_format(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            Path("mcp.json").write_text('{"mcpServers": {"test": {}}}')
            result = runner.invoke(mcp, ["validate", "--format", "json"])
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert "results" in data
            assert "total_findings" in data

    def test_mcp_validate_fix_flag(self, runner, tmp_path):
        with runner.isolated_filesystem(temp_dir=tmp_path):
            Path("mcp.json").write_text('{"mcpServers": {"@random/server": {}}}')
            result = runner.invoke(mcp, ["validate", "--fix"])
            assert result.exit_code == 0
            assert "→" in result.output or "modelcontextprotocol" in result.output
