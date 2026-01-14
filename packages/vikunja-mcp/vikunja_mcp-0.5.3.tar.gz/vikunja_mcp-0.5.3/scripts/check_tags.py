#!/usr/bin/env python3
"""
Verify all functions in server.py are tagged.

Exits with error if any function is missing a tag.

Usage:
    python scripts/check_tags.py
"""

import re
import sys
from pathlib import Path

PRIVATE_SERVER = Path(__file__).parent.parent / "src" / "vikunja_mcp" / "server.py"

VALID_TAGS = {'# @PUBLIC', '# @PUBLIC_HELPER', '# @PRIVATE'}


def check_tags(source: str) -> list[tuple[int, str]]:
    """Find untagged functions. Returns list of (line_num, func_name)."""
    lines = source.split('\n')
    untagged = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this line is a function definition
        match = re.match(r'^(?:async\s+)?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', stripped)

        if match:
            func_name = match.group(1)

            # Look back for a tag
            found_tag = False
            lookback = i - 1

            while lookback >= 0:
                prev_line = lines[lookback].strip()

                if prev_line in VALID_TAGS:
                    found_tag = True
                    break
                elif prev_line.startswith('@'):
                    # Decorator, keep looking
                    lookback -= 1
                    continue
                elif prev_line == '':
                    # Empty line, keep looking
                    lookback -= 1
                    continue
                elif prev_line.startswith('#') and prev_line not in VALID_TAGS:
                    # Comment that's not a tag, keep looking
                    lookback -= 1
                    continue
                else:
                    # Hit actual code without finding tag
                    break

            if not found_tag:
                untagged.append((i + 1, func_name))  # 1-indexed line number

    return untagged


def main():
    if not PRIVATE_SERVER.exists():
        print(f"Error: Server not found at {PRIVATE_SERVER}")
        return 1

    source = PRIVATE_SERVER.read_text()

    # Count existing tags
    public_count = source.count('# @PUBLIC\n')
    helper_count = source.count('# @PUBLIC_HELPER\n')
    private_count = source.count('# @PRIVATE\n')

    print(f"Tag counts: {public_count} @PUBLIC, {helper_count} @PUBLIC_HELPER, {private_count} @PRIVATE")
    print(f"Total tagged: {public_count + helper_count + private_count}")

    # Check for untagged
    untagged = check_tags(source)

    if untagged:
        print(f"\n❌ ERROR: {len(untagged)} untagged function(s) found:\n")
        for line_num, func_name in untagged:
            print(f"  Line {line_num}: {func_name}")
        print(f"\nRun: python scripts/tag_private.py  (to tag as private)")
        print(f"Or add # @PUBLIC before the function if it should be public")
        return 1
    else:
        print(f"\n✅ All functions are tagged")
        return 0


if __name__ == '__main__':
    sys.exit(main())
