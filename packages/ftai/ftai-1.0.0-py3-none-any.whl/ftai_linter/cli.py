# SPDX-License-Identifier: Apache-2.0
"""FTAI CLI tool for linting, formatting, and converting .ftai files."""

import argparse
import sys
import json
from pathlib import Path

from .linter import lint_file, parse_ftai_with_lines

# Terminal color codes
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


def print_report(errors, warnings, use_color=True):
    """Print validation report with optional color."""
    red = RED if use_color else ""
    yellow = YELLOW if use_color else ""
    green = GREEN if use_color else ""
    reset = RESET if use_color else ""
    
    if errors:
        print(f"{red}❌ FATAL ERRORS:{reset}")
        for line, msg in errors:
            print(f"{red}[Line {line}] {msg}{reset}")
    if warnings:
        print(f"{yellow}⚠️  WARNINGS:{reset}")
        for line, msg in warnings:
            print(f"{yellow}[Line {line}] {msg}{reset}")
    if not errors:
        print(f"{green}✅ PASS: .ftai document is valid.{reset}")


def cmd_lint(args):
    """Handle the lint subcommand."""
    filepath = Path(args.filepath)
    
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return 1
    
    if not filepath.suffix == '.ftai':
        print(f"Warning: File does not have .ftai extension: {filepath}", file=sys.stderr)
    
    errors, warnings, passed = lint_file(
        str(filepath),
        strict=args.strict,
        lenient=args.lenient
    )
    
    # Check file length warning
    with open(filepath, 'r') as f:
        line_count = sum(1 for _ in f)
    if line_count > 500:
        yellow = YELLOW if args.color else ""
        reset = RESET if args.color else ""
        print(f"{yellow}⚠️  Warning: file exceeds recommended line count (500+){reset}")
    
    print_report(errors, warnings, use_color=args.color)
    
    return 0 if passed else 1


def cmd_fmt(args):
    """Handle the format subcommand."""
    print("Format command not yet implemented.")
    print("Contribution welcome: https://github.com/FolkTechAI/ftai-spec")
    return 0


def cmd_convert(args):
    """Handle the convert subcommand (JSON to FTAI)."""
    filepath = Path(args.json_file)
    
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return 1
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return 1
    
    # Basic JSON to FTAI conversion
    output = json_to_ftai(data)
    print(output)
    return 0


def json_to_ftai(data, indent=0):
    """Convert JSON data to FTAI format."""
    lines = []
    prefix = "  " * indent
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}@section {key}")
                lines.append(json_to_ftai(value, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(json_to_ftai(item, indent))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        lines.append(f"{prefix}{data}")
    
    return "\n".join(lines)


def main():
    """Main entry point for the FTAI CLI."""
    parser = argparse.ArgumentParser(
        prog='ftai',
        description='FTAI CLI tool for linting, formatting, and converting .ftai files.'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s 1.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Lint subcommand
    lint_parser = subparsers.add_parser('lint', help='Lint an FTAI file')
    lint_parser.add_argument('filepath', help='Path to the .ftai file to lint')
    lint_parser.add_argument('--strict', action='store_true', help='Enable strict mode')
    lint_parser.add_argument('--lenient', action='store_true', help='Enable lenient mode for unknown tags')
    color_group = lint_parser.add_mutually_exclusive_group()
    color_group.add_argument('--color', dest='color', action='store_true', default=True, help='Enable color output (default)')
    color_group.add_argument('--no-color', dest='color', action='store_false', help='Disable color output')

    # Format subcommand
    fmt_parser = subparsers.add_parser('fmt', help='Format an FTAI file')
    fmt_parser.add_argument('filepath', help='Path to the .ftai file to format')

    # Convert subcommand
    convert_parser = subparsers.add_parser('convert', help='Convert JSON to FTAI')
    convert_parser.add_argument('json_file', help='Path to the JSON file to convert')

    args = parser.parse_args()

    if args.command == 'lint':
        sys.exit(cmd_lint(args))
    elif args.command == 'fmt':
        sys.exit(cmd_fmt(args))
    elif args.command == 'convert':
        sys.exit(cmd_convert(args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
