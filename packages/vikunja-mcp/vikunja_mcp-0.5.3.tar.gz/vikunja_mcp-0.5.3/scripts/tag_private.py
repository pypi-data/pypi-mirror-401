#!/usr/bin/env python3
"""
Tag remaining untagged functions as @PRIVATE.

This makes it unambiguous which functions are public vs private.

Usage:
    python scripts/tag_private.py [--dry-run]
"""

import re
import sys
from pathlib import Path

PRIVATE_SERVER = Path(__file__).parent.parent / "src" / "vikunja_mcp" / "server.py"


def tag_private_functions(source: str) -> str:
    """Add @PRIVATE tags to functions that aren't already tagged."""
    lines = source.split('\n')
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

            # Check if already tagged (look back for any tag or decorator)
            already_tagged = False

            # Look back to find existing tags
            lookback_idx = len(result) - 1
            while lookback_idx >= 0:
                prev_line = result[lookback_idx].strip()
                if prev_line in ('# @PUBLIC', '# @PUBLIC_HELPER', '# @PRIVATE'):
                    already_tagged = True
                    break
                elif prev_line.startswith('@'):
                    # It's a decorator, keep looking
                    lookback_idx -= 1
                    continue
                elif prev_line == '':
                    # Empty line, keep looking
                    lookback_idx -= 1
                    continue
                elif prev_line.startswith('#'):
                    # Comment that's not a tag, keep looking
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

                result.insert(insert_idx, '# @PRIVATE')
                tagged_count += 1
            else:
                skipped_count += 1

        result.append(line)
        i += 1

    print(f"Tagged {tagged_count} functions as @PRIVATE, skipped {skipped_count} already tagged")
    return '\n'.join(result)


def main():
    dry_run = '--dry-run' in sys.argv

    if not PRIVATE_SERVER.exists():
        print(f"Error: Private server not found at {PRIVATE_SERVER}")
        return 1

    print(f"Reading private server from: {PRIVATE_SERVER}")
    private_source = PRIVATE_SERVER.read_text()

    # Count existing tags
    public_count = private_source.count('# @PUBLIC\n')
    helper_count = private_source.count('# @PUBLIC_HELPER\n')
    private_count = private_source.count('# @PRIVATE\n')
    print(f"Existing tags: {public_count} @PUBLIC, {helper_count} @PUBLIC_HELPER, {private_count} @PRIVATE")

    # Tag remaining functions
    print("\nTagging remaining functions as @PRIVATE...")
    tagged_source = tag_private_functions(private_source)

    if dry_run:
        print("\n=== DRY RUN - Sample of tagged functions ===")
        lines = tagged_source.split('\n')
        sample_count = 0
        for i, line in enumerate(lines):
            if line.strip() == '# @PRIVATE' and sample_count < 10:
                print(f"\n{lines[i]}")
                if i + 1 < len(lines):
                    print(lines[i + 1][:80])
                sample_count += 1
    else:
        PRIVATE_SERVER.write_text(tagged_source)
        print(f"\nWrote tagged server to: {PRIVATE_SERVER}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
