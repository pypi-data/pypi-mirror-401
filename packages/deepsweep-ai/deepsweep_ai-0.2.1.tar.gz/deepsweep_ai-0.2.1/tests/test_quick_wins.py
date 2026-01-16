"""Tests for CLI quick wins."""

from pathlib import Path

import pytest
from click.testing import CliRunner


class TestOutputUtils:
    def test_score_bar(self):
        from deepsweep.output import score_bar
        assert "100/100" in score_bar(100)
        assert "0/100" in score_bar(0)

    def test_format_grade(self):
        from deepsweep.output import format_grade
        for g in ["A", "B", "C", "D", "F"]:
            assert g in format_grade(g)


class TestInitCommand:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_init_creates_cursorrules(self, runner, tmp_path):
        from deepsweep.commands.init import init
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(init)
            assert result.exit_code == 0
            assert Path(".cursorrules").exists()

    def test_init_with_mcp(self, runner, tmp_path):
        from deepsweep.commands.init import init
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(init, ["--include-mcp"])
            assert Path("mcp.json").exists()

    def test_init_no_overwrite(self, runner, tmp_path):
        from deepsweep.commands.init import init
        with runner.isolated_filesystem(temp_dir=tmp_path):
            Path(".cursorrules").write_text("existing")
            runner.invoke(init)
            assert Path(".cursorrules").read_text() == "existing"

    def test_init_force(self, runner, tmp_path):
        from deepsweep.commands.init import init
        with runner.isolated_filesystem(temp_dir=tmp_path):
            Path(".cursorrules").write_text("existing")
            runner.invoke(init, ["--force"])
            assert Path(".cursorrules").read_text() != "existing"


class TestDoctorCommand:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_doctor_runs(self, runner):
        from deepsweep.commands.doctor import doctor
        result = runner.invoke(doctor)
        assert result.exit_code == 0
        assert "Health Check" in result.output


class TestBadgeCommand:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_badge_markdown(self, runner):
        from deepsweep.commands.badge import badge
        result = runner.invoke(badge, ["--score", "100", "--grade", "A"])
        assert "shields.io" in result.output
        assert "DeepSweep" in result.output

    def test_badge_html(self, runner):
        from deepsweep.commands.badge import badge
        result = runner.invoke(badge, ["--format", "html"])
        assert "<a href" in result.output
