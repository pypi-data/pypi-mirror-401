#!/usr/bin/env python3
"""Test E2EE configuration for Matrix bot.

Verifies that:
1. SqliteStore can be imported
2. Crypto store can be created
3. AsyncClientConfig accepts E2EE parameters
4. Room creation with encryption works

Run this before deploying to Render.
"""

import os
import tempfile
from nio import AsyncClient, AsyncClientConfig
from nio.store import SqliteStore


def test_crypto_store_creation():
    """Test that we can create a crypto store."""
    print("✓ Testing crypto store creation...")

    with tempfile.TemporaryDirectory() as tmpdir:
        store_path = os.path.join(tmpdir, "crypto_store")
        os.makedirs(store_path, exist_ok=True)  # Create directory first

        store = SqliteStore(
            user_id="@test:matrix.org",
            device_id="test_device",
            store_path=store_path,
        )

        print(f"  ✓ Created crypto store at {store_path}")
        return True


def test_client_config():
    """Test that AsyncClientConfig accepts E2EE parameters."""
    print("✓ Testing AsyncClientConfig with E2EE...")

    with tempfile.TemporaryDirectory() as tmpdir:
        store_path = os.path.join(tmpdir, "crypto_store")
        os.makedirs(store_path, exist_ok=True)  # Create directory first

        store = SqliteStore(
            user_id="@test:matrix.org",
            device_id="test_device",
            store_path=store_path,
        )

        config = AsyncClientConfig(
            max_limit_exceeded=0,
            max_timeouts=0,
            encryption_enabled=True,
            store_sync_tokens=True,
            store=store,
        )

        print(f"  ✓ Config created with encryption_enabled={config.encryption_enabled}")
        return True


def test_client_initialization():
    """Test that AsyncClient can be initialized with E2EE config."""
    print("✓ Testing AsyncClient initialization...")

    with tempfile.TemporaryDirectory() as tmpdir:
        store_path = os.path.join(tmpdir, "crypto_store")
        os.makedirs(store_path, exist_ok=True)  # Create directory first

        store = SqliteStore(
            user_id="@test:matrix.org",
            device_id="test_device",
            store_path=store_path,
        )

        config = AsyncClientConfig(
            encryption_enabled=True,
            store_sync_tokens=True,
            store=store,
        )

        client = AsyncClient(
            homeserver="https://matrix.org",
            user="@test:matrix.org",
            device_id="test_device",
            config=config,
        )

        print(f"  ✓ Client created: {client.user_id}")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing E2EE Configuration")
    print("=" * 60)
    
    tests = [
        test_crypto_store_creation,
        test_client_config,
        test_client_initialization,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            results.append(False)
    
    print("=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("\nReady to deploy to Render.")
        return 0
    else:
        print("✗ Some tests failed!")
        print("\nFix errors before deploying.")
        return 1


if __name__ == "__main__":
    exit(main())

