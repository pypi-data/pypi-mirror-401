# SPDX-License-Identifier: Apache-2.0
"""Core linting logic for FTAI files."""

import re
from collections import defaultdict

# Core .ftai v2.0 tags
CORE_TAGS = {
    "@ftai", "@document", "@task", "@config", "@ai", "@schema", "@end",
    "@table", "@section", "@note", "@warning", "@goal", "@tool_call",
    "@memory", "@protocol", "@agent", "@issue", "@prose", "@quoted_tag",
    "@constraints", "@insight", "@recommendations", "@closing_note",
    "@image", "@intent"
}

BLOCK_TAGS = {"@task", "@config", "@ai", "@agent", "@memory", "@protocol"}


def check_line_syntax(line_num, raw_line, errors):
    """Checks a single line for basic syntax errors."""
    stripped_line = raw_line.strip()
    leading_whitespace = raw_line[:-len(stripped_line)] if stripped_line else ""

    # Check for mixed tabs and spaces in leading whitespace
    if '\t' in leading_whitespace and ' ' in leading_whitespace:
        errors.append((line_num, "Mixed tabs and spaces in indentation."))

    # Basic check for unmatched quotes/markup on the line
    if stripped_line.count('"') % 2 != 0:
        if not stripped_line.startswith('@"'):
            errors.append((line_num, 'Potentially unmatched double quote (") on line.'))
    
    if stripped_line.count('**') % 2 != 0:
        errors.append((line_num, "Potentially unmatched bold marker (**) on line."))
    
    if stripped_line.count('///') % 2 != 0:
        errors.append((line_num, "Potentially unmatched highlight marker (///) on line."))


def parse_ftai_with_lines(filepath):
    """Parse an FTAI file and return structured tag data."""
    syntax_errors = []
    lines = []
    expected_fail = False

    with open(filepath, 'r') as file:
        all_lines = file.readlines()

        # Check for @intent fail on the first line
        if all_lines and all_lines[0].strip().lower() == "@intent fail":
            expected_fail = True

        for i, raw_line in enumerate(all_lines):
            line_num = i + 1
            lines.append(raw_line)
            check_line_syntax(line_num, raw_line, syntax_errors)

    tag_data = []
    buffer = []
    current_tag = None
    tag_start = 0

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()
        line_num = i + 1

        if line.startswith("@"):
            if current_tag:
                processed_buffer = [(ln, l.strip()) for ln, l in buffer]
                tag_data.append((current_tag, processed_buffer, tag_start))
                buffer = []
            current_tag = line
            tag_start = line_num
        elif line == "---":
            continue
        else:
            if current_tag is not None:
                buffer.append((line_num, raw_line))

    if current_tag:
        processed_buffer = [(ln, l.strip()) for ln, l in buffer]
        tag_data.append((current_tag, processed_buffer, tag_start))

    return tag_data, syntax_errors, expected_fail


def extract_schema_tags(tag_data):
    """Extract required and optional tags from @schema blocks."""
    required_tags = set()
    optional_tags = set()
    for tag, body, _ in tag_data:
        if tag.startswith("@schema"):
            for _, line in body:
                if line.startswith("required_tags:"):
                    required = re.findall(r'"(.*?)"', line)
                    required_tags.update(required)
                elif line.startswith("optional_tags:"):
                    optional = re.findall(r'"(.*?)"', line)
                    optional_tags.update(optional)
    return required_tags, optional_tags


def validate_ftai(tag_data, syntax_errors, expected_fail, soft_mode=False, lenient=False):
    """Validate parsed FTAI data and return errors and warnings."""
    errors = list(syntax_errors)
    warnings = []
    seen_tags = set()
    quoted_tag_count = 0
    has_ftai = False
    has_document = False

    required_schema_tags, optional_schema_tags = extract_schema_tags(tag_data)
    valid_tags = CORE_TAGS.union(required_schema_tags).union(optional_schema_tags)

    for tag, body, line_num in tag_data:
        tag_clean = tag.split()[0]

        if tag_clean.startswith('@"'):
            quoted_tag_count += 1
            continue

        if tag_clean not in valid_tags:
            if lenient:
                warnings.append((line_num, f"Unknown tag: {tag_clean}"))
            else:
                errors.append((line_num, f"Unknown tag: {tag_clean}"))
            continue
        else:
            seen_tags.add(tag_clean)

        if tag_clean == "@ftai":
            if line_num != 1:
                warnings.append((line_num, "`@ftai` should be the first tag in the file."))
            has_ftai = True

        if tag_clean == "@document":
            has_document = True

        if tag_clean in BLOCK_TAGS:
            has_end = False
            for _, subtag_line in body:
                if subtag_line.strip() == "@end":
                    has_end = True
                    break
            if not has_end:
                errors.append((line_num, f"Missing `@end` block terminator for {tag_clean}."))

    for req in required_schema_tags:
        if req not in seen_tags:
            errors.append((0, f"Missing required schema tag: {req}"))

    if not has_ftai:
        errors.append((0, "Missing required `@ftai` declaration."))
    if not has_document:
        errors.append((0, "Missing required `@document` block."))

    if quoted_tag_count > 10:
        warnings.append((0, 'Excessive use of quoted tags (@"..."). Consider defining a schema.'))

    passed = not errors

    if expected_fail and passed:
        if soft_mode:
            warnings.append((0, "File passed validation, but was marked with @intent fail (soft mode active)."))
        else:
            errors.append((0, "✗ Test Intent Mismatch: File marked with @intent fail passed validation."))

    return errors, warnings


def lint_file(filepath, strict=False, lenient=False):
    """
    Lint an FTAI file and return (errors, warnings, passed).
    
    Args:
        filepath: Path to the .ftai file
        strict: Enable strict mode (default False)
        lenient: Enable lenient mode for unknown tags (default False)
    
    Returns:
        Tuple of (errors, warnings, passed)
    """
    tag_data, syntax_errors, expected_fail = parse_ftai_with_lines(filepath)
    errors, warnings = validate_ftai(
        tag_data, 
        syntax_errors, 
        expected_fail, 
        soft_mode=not strict, 
        lenient=lenient
    )
    passed = len(errors) == 0
    return errors, warnings, passed
