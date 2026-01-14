#!/usr/bin/env python3
"""
Inspect Vikunja Database - API Tokens

This script connects to the Vikunja PostgreSQL database and inspects
the api_tokens table to understand how tokens are stored and validated.

This will help us understand:
1. Token format and structure in the database
2. How tokens are hashed/encrypted
3. What fields are required for a valid token
4. Differences between working and non-working tokens
"""

import argparse
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Database connection from environment
DB_HOST = os.environ.get("VIKUNJA_DB_HOST", "localhost")
DB_PORT = os.environ.get("VIKUNJA_DB_PORT", "5432")
DB_NAME = os.environ.get("VIKUNJA_DB_NAME", "vikunja")
DB_USER = os.environ.get("VIKUNJA_DB_USER", "vikunja")
DB_PASSWORD = os.environ.get("VIKUNJA_DB_PASSWORD", "")


def connect_db():
    """Connect to Vikunja database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None


def inspect_api_tokens_table(conn):
    """Show structure of api_tokens table."""
    print("\n" + "="*60)
    print("API TOKENS TABLE STRUCTURE")
    print("="*60)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Get table structure
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'api_tokens'
            ORDER BY ordinal_position
        """)
        
        columns = cur.fetchall()
        if not columns:
            print("❌ Table 'api_tokens' not found")
            return
        
        print("\nColumns:")
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"  {col['column_name']:20} {col['data_type']:20} {nullable}{default}")


def list_all_tokens(conn, user_id: int = None):
    """List all API tokens (or for specific user)."""
    print("\n" + "="*60)
    print("API TOKENS IN DATABASE")
    print("="*60)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if user_id:
            cur.execute("""
                SELECT id, user_id, title, token_hash, token_last_eight,
                       permissions, expires_at, created, updated
                FROM api_tokens
                WHERE user_id = %s
                ORDER BY created DESC
            """, (user_id,))
        else:
            cur.execute("""
                SELECT id, user_id, title, token_hash, token_last_eight,
                       permissions, expires_at, created, updated
                FROM api_tokens
                ORDER BY created DESC
                LIMIT 20
            """)
        
        tokens = cur.fetchall()
        
        if not tokens:
            print("No tokens found")
            return
        
        print(f"\nFound {len(tokens)} token(s):\n")
        for token in tokens:
            print(f"ID: {token['id']}")
            print(f"  User ID: {token['user_id']}")
            print(f"  Title: {token['title']}")
            print(f"  Token Hash: {token.get('token_hash', 'N/A')[:50]}...")
            print(f"  Last 8 chars: {token.get('token_last_eight', 'N/A')}")
            print(f"  Permissions: {token.get('permissions', 'N/A')}")
            print(f"  Expires: {token.get('expires_at', 'Never')}")
            print(f"  Created: {token['created']}")
            print()


def check_token_validation_logic(conn):
    """Check if there are any triggers or constraints on api_tokens."""
    print("\n" + "="*60)
    print("TOKEN VALIDATION LOGIC")
    print("="*60)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Check for triggers
        cur.execute("""
            SELECT trigger_name, event_manipulation, action_statement
            FROM information_schema.triggers
            WHERE event_object_table = 'api_tokens'
        """)
        
        triggers = cur.fetchall()
        if triggers:
            print("\nTriggers:")
            for trigger in triggers:
                print(f"  {trigger['trigger_name']} ({trigger['event_manipulation']})")
                print(f"    {trigger['action_statement']}")
        else:
            print("\nNo triggers found")
        
        # Check for constraints
        cur.execute("""
            SELECT constraint_name, constraint_type
            FROM information_schema.table_constraints
            WHERE table_name = 'api_tokens'
        """)
        
        constraints = cur.fetchall()
        if constraints:
            print("\nConstraints:")
            for constraint in constraints:
                print(f"  {constraint['constraint_name']}: {constraint['constraint_type']}")
        else:
            print("\nNo constraints found")


def main():
    parser = argparse.ArgumentParser(description="Inspect Vikunja database tokens")
    parser.add_argument("--user-id", type=int, help="Filter tokens by user ID")
    parser.add_argument("--show-structure", action="store_true", help="Show table structure")
    parser.add_argument("--show-validation", action="store_true", help="Show validation logic")
    
    args = parser.parse_args()
    
    print("Vikunja Database Token Inspector")
    print(f"Database: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    conn = connect_db()
    if not conn:
        return 1
    
    try:
        if args.show_structure:
            inspect_api_tokens_table(conn)
        
        list_all_tokens(conn, args.user_id)
        
        if args.show_validation:
            check_token_validation_logic(conn)
        
    finally:
        conn.close()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

