#!/usr/bin/env python3
"""
Auto-tag functions in private server.py that exist in public server.py.

This script reads both server files, identifies functions that exist in public,
and adds # @PUBLIC or # @PUBLIC_HELPER tags to the private file.

Usage:
    python scripts/tag_public.py [--dry-run]
"""

import re
import sys
from pathlib import Path

PRIVATE_SERVER = Path(__file__).parent.parent / "src" / "vikunja_mcp" / "server.py"
PUBLIC_SERVER = Path.home() / "vikunja-mcp" / "src" / "vikunja_mcp" / "server.py"


def get_function_names(source: str) -> set:
    """Extract all function names from source code."""
    # Match 'def name(' or 'async def name('
    pattern = r'^(?:async\s+)?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    names = set()
    for line in source.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            names.add(match.group(1))
    return names


def tag_functions(private_source: str, public_functions: set) -> str:
    """Add @PUBLIC tags to functions that exist in public."""
    lines = private_source.split('\n')
    result = []
    i = 0

    tagged_count = 0
    skipped_count = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if this line is a function definition
        match = re.match(r'^(?:async\s+)?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', stripped)

        if match:
            func_name = match.group(1)

            if func_name in public_functions:
                # Check if already tagged (look back for @PUBLIC or decorator)
                already_tagged = False
                tag_line = None

                # Look back to find decorators or existing tags
                lookback_idx = len(result) - 1
                while lookback_idx >= 0:
                    prev_line = result[lookback_idx].strip()
                    if prev_line == '# @PUBLIC' or prev_line == '# @PUBLIC_HELPER':
                        already_tagged = True
                        break
                    elif prev_line.startswith('@'):
                        # It's a decorator, keep looking
                        lookback_idx -= 1
                        continue
                    elif prev_line == '' or prev_line.startswith('#'):
                        # Empty line or comment, keep looking
                        lookback_idx -= 1
                        continue
                    else:
                        # Hit actual code, stop looking
                        break

                if not already_tagged:
                    # Find where to insert the tag (before decorators)
                    insert_idx = len(result)
                    while insert_idx > 0 and result[insert_idx - 1].strip().startswith('@'):
                        insert_idx -= 1

                    # Determine tag type: helper functions start with _
                    if func_name.startswith('_'):
                        tag = '# @PUBLIC_HELPER'
                    else:
                        tag = '# @PUBLIC'

                    result.insert(insert_idx, tag)
                    tagged_count += 1
                else:
                    skipped_count += 1

        result.append(line)
        i += 1

    print(f"Tagged {tagged_count} functions, skipped {skipped_count} already tagged")
    return '\n'.join(result)


def main():
    dry_run = '--dry-run' in sys.argv

    if not PRIVATE_SERVER.exists():
        print(f"Error: Private server not found at {PRIVATE_SERVER}")
        return 1

    if not PUBLIC_SERVER.exists():
        print(f"Error: Public server not found at {PUBLIC_SERVER}")
        return 1

    print(f"Reading public server from: {PUBLIC_SERVER}")
    public_source = PUBLIC_SERVER.read_text()
    public_functions = get_function_names(public_source)
    print(f"Found {len(public_functions)} functions in public server")

    print(f"\nReading private server from: {PRIVATE_SERVER}")
    private_source = PRIVATE_SERVER.read_text()
    private_functions = get_function_names(private_source)
    print(f"Found {len(private_functions)} functions in private server")

    # Functions to tag = intersection
    to_tag = public_functions & private_functions
    print(f"\nFunctions to tag: {len(to_tag)}")

    # Functions only in public (might be renamed or missing in private)
    only_public = public_functions - private_functions
    if only_public:
        print(f"\nWarning: {len(only_public)} functions in public but not private:")
        for name in sorted(only_public)[:10]:
            print(f"  - {name}")
        if len(only_public) > 10:
            print(f"  ... and {len(only_public) - 10} more")

    # Tag the functions
    print("\nTagging functions...")
    tagged_source = tag_functions(private_source, to_tag)

    if dry_run:
        print("\n=== DRY RUN - Would write to private server ===")
        # Show a sample of tagged functions
        lines = tagged_source.split('\n')
        for i, line in enumerate(lines):
            if line.strip() in ('# @PUBLIC', '# @PUBLIC_HELPER'):
                print(f"\n{lines[i]}")
                if i + 1 < len(lines):
                    print(lines[i + 1][:80])
                if i + 2 < len(lines):
                    print(lines[i + 2][:80])
    else:
        PRIVATE_SERVER.write_text(tagged_source)
        print(f"\nWrote tagged server to: {PRIVATE_SERVER}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
