#!/usr/bin/env python3
"""
Extract @PUBLIC tagged tools from private server.py to generate public vikunja-mcp.

Usage:
    python scripts/extract_public.py [--dry-run]

Tags supported:
    # @PUBLIC           - Tag the next function as public (place before @mcp.tool())
    # @PUBLIC_HELPER    - Tag a helper function needed by public tools
    # @PUBLIC_SECTION   - Tag a section of code (constants, config blocks)
    # @END_PUBLIC_SECTION - End a public section

The script:
1. Extracts the module docstring
2. Extracts all imports
3. Extracts code between @PUBLIC_SECTION markers
4. Extracts functions tagged with @PUBLIC or @PUBLIC_HELPER
5. Extracts the main() function and mcp initialization
6. Writes to ~/vikunja-mcp/src/vikunja_mcp/server.py
"""

import ast
import re
import sys
from pathlib import Path

# Paths
PRIVATE_SERVER = Path(__file__).parent.parent / "src" / "vikunja_mcp" / "server.py"
PUBLIC_SERVER = Path.home() / "vikunja-mcp" / "src" / "vikunja_mcp" / "server.py"

# Public docstring for the generated file
PUBLIC_DOCSTRING = '''"""
Vikunja MCP Server

MCP server that gives Claude full access to your Vikunja task management instance.
Works with any Vikunja instance - self-hosted, cloud, or local.

This file is AUTO-GENERATED from the private factumerit server.
Do not edit directly - edit the private server and run:
    python scripts/extract_public.py

Source: https://github.com/ivantohelpyou/vikunja-mcp
PyPI: https://pypi.org/project/vikunja-mcp/
"""
'''


def extract_public_content(source_code: str) -> str:
    """Extract all @PUBLIC tagged content from source code."""
    lines = source_code.split('\n')

    # Track what to extract
    imports = []
    public_sections = []
    public_functions = []

    # State tracking
    in_public_section = False
    current_section = []
    next_is_public = False
    next_is_helper = False

    # First pass: collect imports and identify tagged content
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track imports (always include)
        if stripped.startswith('import ') or stripped.startswith('from '):
            imports.append(line)
            i += 1
            continue

        # Track public section markers
        if '# @PUBLIC_SECTION' in stripped:
            in_public_section = True
            current_section = []
            i += 1
            continue

        if '# @END_PUBLIC_SECTION' in stripped:
            in_public_section = False
            if current_section:
                public_sections.append('\n'.join(current_section))
            current_section = []
            i += 1
            continue

        # Collect content in public sections
        if in_public_section:
            current_section.append(line)
            i += 1
            continue

        # Track @PUBLIC and @PUBLIC_HELPER tags
        if stripped == '# @PUBLIC':
            next_is_public = True
            i += 1
            continue

        if stripped == '# @PUBLIC_HELPER':
            next_is_helper = True
            i += 1
            continue

        # If we hit a decorator or function def after a tag, extract the function
        if (next_is_public or next_is_helper) and (stripped.startswith('@') or stripped.startswith('def ') or stripped.startswith('async def ')):
            func_lines = []

            # Collect decorators
            while i < len(lines) and lines[i].strip().startswith('@'):
                func_lines.append(lines[i])
                i += 1

            # Collect function definition and body
            if i < len(lines) and (lines[i].strip().startswith('def ') or lines[i].strip().startswith('async def ')):
                func_lines.append(lines[i])
                i += 1

                # Get the indentation of the function body
                base_indent = 0
                if i < len(lines):
                    match = re.match(r'^(\s*)', lines[i])
                    if match and lines[i].strip():
                        base_indent = len(match.group(1))

                # Collect function body (everything indented more than function def, or blank lines)
                while i < len(lines):
                    current_line = lines[i]
                    current_stripped = current_line.strip()

                    # Empty line - include it
                    if not current_stripped:
                        func_lines.append(current_line)
                        i += 1
                        continue

                    # Check indentation
                    match = re.match(r'^(\s*)', current_line)
                    current_indent = len(match.group(1)) if match else 0

                    # If we're back to base level (or less), we're done with this function
                    if current_indent < base_indent and current_stripped:
                        break

                    func_lines.append(current_line)
                    i += 1

                # Remove trailing blank lines from function
                while func_lines and not func_lines[-1].strip():
                    func_lines.pop()

                public_functions.append('\n'.join(func_lines))

            next_is_public = False
            next_is_helper = False
            continue

        # Reset tags if we hit something else
        if next_is_public or next_is_helper:
            next_is_public = False
            next_is_helper = False

        i += 1

    # Build output
    output_parts = [PUBLIC_DOCSTRING.strip(), '']

    # Add imports (deduplicated, sorted)
    seen_imports = set()
    sorted_imports = []
    for imp in imports:
        if imp not in seen_imports:
            seen_imports.add(imp)
            sorted_imports.append(imp)

    # Group stdlib imports, then third-party
    stdlib_imports = []
    third_party_imports = []
    for imp in sorted_imports:
        # Simple heuristic: if it's 'from' an installed package or 'import' a package
        if any(pkg in imp for pkg in ['fastmcp', 'pydantic', 'requests', 'yaml', 'icalendar', 'markdown', 'cryptography']):
            third_party_imports.append(imp)
        else:
            stdlib_imports.append(imp)

    if stdlib_imports:
        output_parts.extend(stdlib_imports)
        output_parts.append('')
    if third_party_imports:
        output_parts.extend(third_party_imports)
        output_parts.append('')

    # Add public sections
    for section in public_sections:
        output_parts.append(section)
        output_parts.append('')

    # Add public functions
    for func in public_functions:
        output_parts.append(func)
        output_parts.append('')
        output_parts.append('')

    return '\n'.join(output_parts)


def main():
    dry_run = '--dry-run' in sys.argv

    if not PRIVATE_SERVER.exists():
        print(f"Error: Private server not found at {PRIVATE_SERVER}")
        sys.exit(1)

    print(f"Reading private server from: {PRIVATE_SERVER}")
    source = PRIVATE_SERVER.read_text()

    # Count tags before extraction
    public_count = source.count('# @PUBLIC\n')
    helper_count = source.count('# @PUBLIC_HELPER\n')
    section_count = source.count('# @PUBLIC_SECTION')

    print(f"Found: {public_count} @PUBLIC tools, {helper_count} @PUBLIC_HELPER functions, {section_count} @PUBLIC_SECTION blocks")

    if public_count == 0 and section_count == 0:
        print("\nNo @PUBLIC tags found! Tag tools in server.py first.")
        print("Example:")
        print("    # @PUBLIC")
        print("    @mcp.tool()")
        print("    def list_tasks(...):")
        sys.exit(1)

    # Extract public content
    output = extract_public_content(source)

    if dry_run:
        print("\n=== DRY RUN - Would generate: ===\n")
        print(output[:2000])
        print(f"\n... ({len(output)} total characters)")
    else:
        PUBLIC_SERVER.parent.mkdir(parents=True, exist_ok=True)
        PUBLIC_SERVER.write_text(output)
        print(f"\nWrote public server to: {PUBLIC_SERVER}")
        print(f"Output size: {len(output):,} characters")

    return 0


if __name__ == '__main__':
    sys.exit(main())
