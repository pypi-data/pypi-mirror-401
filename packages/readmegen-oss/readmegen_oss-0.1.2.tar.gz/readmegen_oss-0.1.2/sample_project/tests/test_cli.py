"""Tests for sample-project CLI."""

import pytest
from click.testing import CliRunner
from sample_project.cli import main


class TestCLI:
    """Test CLI commands."""

    @pytest.fixture
    def runner(self):
        """CLI runner fixture."""
        return CliRunner()

    def test_greet_command(self, runner):
        """Test greet command."""
        result = runner.invoke(main, ['greet', 'World'])
        assert result.exit_code == 0
        assert "Hello, World!" in result.output

    def test_version_command(self, runner):
        """Test version command."""
        result = runner.invoke(main, ['version'])
        assert result.exit_code == 0
        assert "v0.1.0" in result.output

    def test_main_help(self, runner):
        """Test main help command."""
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert "Sample Python project CLI" in result.output
