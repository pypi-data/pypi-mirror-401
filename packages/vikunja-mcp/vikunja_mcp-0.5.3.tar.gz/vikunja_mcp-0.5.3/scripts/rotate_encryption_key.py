#!/usr/bin/env python3
"""
Rotate TOKEN_ENCRYPTION_KEY by re-encrypting all encrypted data.

Handles TWO tables:
1. user_tokens - OAuth tokens (Matrix/Slack users)
2. personal_bots - Bot passwords (@eis, @eij, etc.)

Reads KEY_V1 (current) and KEY_V2 (new) from environment, then:
1. Fetches all encrypted data
2. Decrypts with KEY_V1, re-encrypts with KEY_V2
3. Updates encryption_version (user_tokens) or in-place (personal_bots)

Usage:
    # Dry run (no changes)
    TOKEN_ENCRYPTION_KEY=<v1> TOKEN_ENCRYPTION_KEY_V2=<v2> python rotate_encryption_key.py --dry-run

    # Live migration
    TOKEN_ENCRYPTION_KEY=<v1> TOKEN_ENCRYPTION_KEY_V2=<v2> python rotate_encryption_key.py

    # Skip orphaned user_tokens (can't decrypt, different key)
    TOKEN_ENCRYPTION_KEY=<v1> TOKEN_ENCRYPTION_KEY_V2=<v2> python rotate_encryption_key.py --skip-user-tokens

Bead: fa-aozp
Design: fa-r3i
"""

import argparse
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from psycopg_pool import ConnectionPool


# =============================================================================
# DATABASE CONNECTION (copied from token_broker to avoid import chain)
# =============================================================================

DATABASE_URL = os.environ.get("DATABASE_URL")
_pool: Optional[ConnectionPool] = None


def _get_pool() -> ConnectionPool:
    """Get or create connection pool."""
    global _pool
    if _pool is None:
        if not DATABASE_URL:
            print("ERROR: DATABASE_URL not configured")
            sys.exit(1)
        _pool = ConnectionPool(
            DATABASE_URL,
            min_size=1,
            max_size=5,
            timeout=30,
            open=True,
        )
    return _pool


@contextmanager
def get_db():
    """Get database connection from pool."""
    pool = _get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


def execute(query: str, params: tuple = None) -> list:
    """Execute query and return results."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                return cur.fetchall()
            return []


def get_keys() -> tuple[str, str]:
    """Get encryption keys from environment."""
    key_v1 = os.environ.get("TOKEN_ENCRYPTION_KEY")
    key_v2 = os.environ.get("TOKEN_ENCRYPTION_KEY_V2")

    if not key_v1:
        print("ERROR: TOKEN_ENCRYPTION_KEY (v1) not set")
        sys.exit(1)
    if not key_v2:
        print("ERROR: TOKEN_ENCRYPTION_KEY_V2 (v2) not set")
        sys.exit(1)

    # Validate keys are valid Fernet keys
    try:
        Fernet(key_v1.encode())
    except Exception as e:
        print(f"ERROR: TOKEN_ENCRYPTION_KEY is not a valid Fernet key: {e}")
        sys.exit(1)

    try:
        Fernet(key_v2.encode())
    except Exception as e:
        print(f"ERROR: TOKEN_ENCRYPTION_KEY_V2 is not a valid Fernet key: {e}")
        sys.exit(1)

    if key_v1 == key_v2:
        print("ERROR: KEY_V1 and KEY_V2 are identical - nothing to rotate")
        sys.exit(1)

    return key_v1, key_v2


def fetch_v1_tokens() -> list[tuple]:
    """Fetch all tokens with encryption_version=1."""
    return execute(
        """
        SELECT user_id, vikunja_instance, encrypted_token
        FROM user_tokens
        WHERE encryption_version = 1 AND revoked = FALSE
        ORDER BY user_id
        """
    )


def rotate_token(
    user_id: str,
    instance: str,
    encrypted_v1: bytes,
    fernet_v1: Fernet,
    fernet_v2: Fernet,
    dry_run: bool,
) -> tuple[bool, str]:
    """
    Rotate a single token from v1 to v2 encryption.

    Returns:
        (success, message)
    """
    try:
        # Decrypt with old key
        plaintext = fernet_v1.decrypt(encrypted_v1).decode()

        # Encrypt with new key
        encrypted_v2 = fernet_v2.encrypt(plaintext.encode())

        if dry_run:
            return True, "would migrate"

        # Update in database
        execute(
            """
            UPDATE user_tokens
            SET encrypted_token = %s, encryption_version = 2
            WHERE user_id = %s AND vikunja_instance = %s
            """,
            (encrypted_v2, user_id, instance),
        )

        return True, "migrated"

    except InvalidToken:
        return False, "decrypt failed (wrong key or corrupted)"
    except Exception as e:
        return False, f"error: {e}"


def verify_migration() -> dict:
    """Verify migration status by counting tokens per version."""
    rows = execute(
        """
        SELECT
            encryption_version,
            COUNT(*) as count
        FROM user_tokens
        WHERE revoked = FALSE
        GROUP BY encryption_version
        ORDER BY encryption_version
        """
    )

    result = {"v1": 0, "v2": 0}
    for version, count in rows:
        if version == 1:
            result["v1"] = count
        elif version == 2:
            result["v2"] = count

    return result


# =============================================================================
# PERSONAL BOTS (bot passwords)
# =============================================================================


def fetch_personal_bots() -> list[tuple]:
    """Fetch all personal bot credentials."""
    return execute(
        """
        SELECT user_id, bot_username, vikunja_instance, encrypted_password
        FROM personal_bots
        ORDER BY user_id
        """
    )


def rotate_bot_password(
    user_id: str,
    bot_username: str,
    instance: str,
    encrypted_v1: bytes,
    fernet_v1: Fernet,
    fernet_v2: Fernet,
    dry_run: bool,
) -> tuple[bool, str]:
    """
    Rotate a bot password from v1 to v2 encryption.

    Returns:
        (success, message)
    """
    try:
        # Decrypt with old key
        plaintext = fernet_v1.decrypt(encrypted_v1).decode()

        # Encrypt with new key
        encrypted_v2 = fernet_v2.encrypt(plaintext.encode())

        if dry_run:
            return True, "would migrate"

        # Update in database
        execute(
            """
            UPDATE personal_bots
            SET encrypted_password = %s
            WHERE user_id = %s AND vikunja_instance = %s
            """,
            (encrypted_v2, user_id, instance),
        )

        return True, "migrated"

    except InvalidToken:
        return False, "decrypt failed (wrong key or corrupted)"
    except Exception as e:
        return False, f"error: {e}"


def verify_bots_status() -> int:
    """Count personal bots."""
    rows = execute("SELECT COUNT(*) FROM personal_bots")
    return rows[0][0] if rows else 0


def main():
    parser = argparse.ArgumentParser(
        description="Rotate TOKEN_ENCRYPTION_KEY by re-encrypting all encrypted data"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify current migration status",
    )
    parser.add_argument(
        "--skip-user-tokens",
        action="store_true",
        help="Skip user_tokens table entirely",
    )
    parser.add_argument(
        "--revoke-orphans",
        action="store_true",
        help="Revoke user_tokens that can't be decrypted (lost key)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("TOKEN ENCRYPTION KEY ROTATION")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    if args.verify_only:
        print("\nVerification mode - checking current status...")

        # user_tokens
        token_status = verify_migration()
        print(f"\nuser_tokens (OAuth tokens):")
        print(f"  v1 (old key): {token_status['v1']}")
        print(f"  v2 (new key): {token_status['v2']}")

        # personal_bots
        bot_count = verify_bots_status()
        print(f"\npersonal_bots (bot passwords):")
        print(f"  total: {bot_count}")

        return

    # Get and validate keys
    key_v1, key_v2 = get_keys()
    fernet_v1 = Fernet(key_v1.encode())
    fernet_v2 = Fernet(key_v2.encode())

    print(f"\nMode: {'DRY RUN' if args.dry_run else 'LIVE MIGRATION'}")
    if args.dry_run:
        print("(No changes will be made)")

    total_migrated = 0
    total_errors = []

    # =========================================================================
    # PERSONAL BOTS (bot passwords) - these use the current key
    # =========================================================================
    print("\n" + "-" * 60)
    print("PERSONAL BOTS (bot passwords)")
    print("-" * 60)

    bots = fetch_personal_bots()
    print(f"Found {len(bots)} bot credentials")

    if bots:
        bot_migrated = 0
        print("\nProcessing bots:")
        for user_id, bot_username, instance, encrypted in bots:
            success, message = rotate_bot_password(
                user_id, bot_username, instance, encrypted, fernet_v1, fernet_v2, args.dry_run
            )

            if success:
                bot_migrated += 1
                total_migrated += 1
                print(f"  ✓ {bot_username} ({user_id}): {message}")
            else:
                total_errors.append((f"bot:{bot_username}", user_id, message))
                print(f"  ✗ {bot_username} ({user_id}): {message}")

        print(f"\nBots {'would migrate' if args.dry_run else 'migrated'}: {bot_migrated}/{len(bots)}")

    # =========================================================================
    # USER TOKENS (OAuth tokens) - may be encrypted with lost key
    # =========================================================================
    print("\n" + "-" * 60)
    print("USER TOKENS (OAuth tokens)")
    print("-" * 60)

    orphaned_tokens = []  # Tokens that can't be decrypted (lost key)

    if args.skip_user_tokens:
        print("Skipped (--skip-user-tokens flag)")
        token_status = verify_migration()
        if token_status['v1'] > 0:
            print(f"\n⚠ {token_status['v1']} tokens remain on v1")
    else:
        tokens = fetch_v1_tokens()
        print(f"Found {len(tokens)} tokens with encryption_version=1")

        if tokens:
            token_migrated = 0
            print("\nProcessing tokens:")
            for user_id, instance, encrypted in tokens:
                success, message = rotate_token(
                    user_id, instance, encrypted, fernet_v1, fernet_v2, args.dry_run
                )

                if success:
                    token_migrated += 1
                    total_migrated += 1
                    print(f"  ✓ {user_id}/{instance}: {message}")
                elif "decrypt failed" in message:
                    # Orphaned token - encrypted with different/lost key
                    orphaned_tokens.append((user_id, instance))
                    print(f"  ⚠ {user_id}/{instance}: orphaned (lost key)")
                else:
                    total_errors.append((f"token:{user_id}", instance, message))
                    print(f"  ✗ {user_id}/{instance}: {message}")

            print(f"\nTokens {'would migrate' if args.dry_run else 'migrated'}: {token_migrated}/{len(tokens)}")

            if orphaned_tokens:
                print(f"Orphaned (lost key): {len(orphaned_tokens)}")

    # Handle orphaned tokens
    if orphaned_tokens and args.revoke_orphans and not args.dry_run:
        print("\nRevoking orphaned tokens...")
        for user_id, instance in orphaned_tokens:
            execute(
                """
                UPDATE user_tokens
                SET revoked = TRUE, revoked_at = NOW(), revoked_reason = 'Key rotation - original key lost'
                WHERE user_id = %s AND vikunja_instance = %s
                """,
                (user_id, instance),
            )
            print(f"  ✓ Revoked {user_id}/{instance}")
    elif orphaned_tokens and not args.revoke_orphans:
        print(f"\n⚠ {len(orphaned_tokens)} orphaned tokens (lost key) - run with --revoke-orphans to clean up")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total {'would migrate' if args.dry_run else 'migrated'}: {total_migrated}")
    print(f"Orphaned (lost key): {len(orphaned_tokens)}")
    print(f"Errors: {len(total_errors)}")

    if total_errors:
        print("\nFailed items:")
        for item, context, message in total_errors:
            print(f"  - {item} ({context}): {message}")

    if not args.dry_run and total_migrated > 0:
        print("\n✓ Migration complete!")
        print("\nNext steps:")
        print("  1. Update Render: TOKEN_ENCRYPTION_KEY=<v2_key>")
        print("  2. Remove TOKEN_ENCRYPTION_KEY_V2 from Render")
        print("  3. Restart service")
        print("  4. Delete old key from password manager after 7 days")
        if orphaned_tokens and not args.revoke_orphans:
            print(f"  5. Run again with --revoke-orphans to clean up {len(orphaned_tokens)} orphaned tokens")

    print(f"\nCompleted: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
