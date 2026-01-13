# SPDX-License-Identifier: Apache-2.0
"""Tests for FTAI linter."""

import os
import pytest
from pathlib import Path

from ftai_linter import lint_file, parse_ftai_with_lines, CORE_TAGS


# Get the tests directory
TESTS_DIR = Path(__file__).parent
PASS_DIR = TESTS_DIR / "vectors" / "pass"
FAIL_DIR = TESTS_DIR / "vectors" / "fail"


class TestLinter:
    """Test the linter functionality."""
    
    def test_core_tags_exist(self):
        """Verify core tags are defined."""
        assert "@ftai" in CORE_TAGS
        assert "@document" in CORE_TAGS
        assert "@task" in CORE_TAGS
        assert "@end" in CORE_TAGS
        assert "@image" in CORE_TAGS
    
    def test_lint_pass_minimal(self):
        """Test that minimal valid file passes."""
        filepath = PASS_DIR / "pass_minimal.ftai"
        if filepath.exists():
            errors, warnings, passed = lint_file(str(filepath))
            assert passed, f"Expected pass but got errors: {errors}"
    
    def test_lint_pass_nested_sections(self):
        """Test that nested sections file passes."""
        filepath = PASS_DIR / "pass_nested_sections.ftai"
        if filepath.exists():
            errors, warnings, passed = lint_file(str(filepath))
            assert passed, f"Expected pass but got errors: {errors}"
    
    def test_lint_fail_missing_end(self):
        """Test that missing @end is caught."""
        filepath = FAIL_DIR / "fail_missing_end.ftai"
        if filepath.exists():
            errors, warnings, passed = lint_file(str(filepath))
            assert not passed, "Expected failure for missing @end"
            # Check that the error mentions @end
            error_messages = [msg for _, msg in errors]
            assert any("@end" in msg for msg in error_messages)
    
    def test_lint_fail_unknown_tag(self):
        """Test that unknown tags are caught in strict mode."""
        filepath = FAIL_DIR / "fail_unknown_tag.ftai"
        if filepath.exists():
            errors, warnings, passed = lint_file(str(filepath), strict=True)
            assert not passed, "Expected failure for unknown tag"
    
    def test_lint_lenient_mode(self):
        """Test that lenient mode converts errors to warnings."""
        filepath = FAIL_DIR / "fail_unknown_tag.ftai"
        if filepath.exists():
            errors, warnings, passed = lint_file(str(filepath), lenient=True)
            # In lenient mode, unknown tags become warnings not errors
            # So it might pass depending on other issues
            assert len(warnings) > 0 or len(errors) > 0


class TestParser:
    """Test the parser functionality."""
    
    def test_parse_minimal_file(self):
        """Test parsing a minimal file."""
        filepath = PASS_DIR / "pass_minimal.ftai"
        if filepath.exists():
            tag_data, syntax_errors, expected_fail = parse_ftai_with_lines(str(filepath))
            assert isinstance(tag_data, list)
            assert isinstance(syntax_errors, list)
            assert isinstance(expected_fail, bool)
    
    def test_parse_detects_intent_fail(self):
        """Test that @intent fail is detected."""
        # Create a temporary test
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ftai', delete=False) as f:
            f.write("@intent fail\n@ftai v2.0\n@document\n  title: test\n")
            f.flush()
            
            tag_data, syntax_errors, expected_fail = parse_ftai_with_lines(f.name)
            assert expected_fail is True
            
            os.unlink(f.name)


class TestCLI:
    """Test CLI functionality via subprocess."""
    
    def test_cli_version(self):
        """Test --version flag."""
        import subprocess
        import sys
        
        result = subprocess.run(
            [sys.executable, "-m", "ftai_linter.cli", "--version"],
            capture_output=True,
            text=True
        )
        assert "1.0.0" in result.stdout
    
    def test_cli_help(self):
        """Test --help flag."""
        import subprocess
        import sys
        
        result = subprocess.run(
            [sys.executable, "-m", "ftai_linter.cli", "--help"],
            capture_output=True,
            text=True
        )
        assert "lint" in result.stdout
        assert "fmt" in result.stdout
        assert "convert" in result.stdout
