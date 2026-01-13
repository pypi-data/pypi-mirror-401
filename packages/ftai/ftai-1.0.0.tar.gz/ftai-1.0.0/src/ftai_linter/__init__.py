# SPDX-License-Identifier: Apache-2.0
"""FTAI Linter Package - Lint, format, and convert .ftai files."""

__version__ = "1.0.0"

from .linter import (
    parse_ftai_with_lines,
    validate_ftai,
    lint_file,
    CORE_TAGS,
    BLOCK_TAGS,
)

__all__ = [
    "__version__",
    "parse_ftai_with_lines",
    "validate_ftai",
    "lint_file",
    "CORE_TAGS",
    "BLOCK_TAGS",
]
