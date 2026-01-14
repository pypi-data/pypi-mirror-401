#!/usr/bin/env python3
"""
Test automatic Vikunja user provisioning and token generation.

This demonstrates the flow for "Take-Out" tier:
1. Register new Vikunja user
2. Create API token for that user
3. Test the token works
"""

import requests
import json
import secrets
import sys

VIKUNJA_URL = "https://vikunja.factumerit.app"

def create_vikunja_user_with_token(username=None, email=None, password=None):
    """
    Create a new Vikunja user and generate an API token.
    
    Returns: (user_id, api_token, jwt_token, password)
    """
    # Generate credentials if not provided
    if not username:
        username = f'test_{secrets.token_hex(4)}'
    if not email:
        email = f'{username}@test.factumerit.app'
    if not password:
        password = secrets.token_urlsafe(16)
    
    print(f'📝 Creating user: {username}')
    print(f'   Email: {email}')
    print()
    
    # Step 1: Register new user
    register_resp = requests.post(
        f'{VIKUNJA_URL}/api/v1/register',
        json={
            'username': username,
            'email': email,
            'password': password
        }
    )
    
    if register_resp.status_code != 200:
        print(f'❌ Registration failed: {register_resp.status_code}')
        print(register_resp.text)
        return None
    
    user_data = register_resp.json()
    jwt_token = user_data.get('token')
    user_id = user_data.get('id')
    
    print(f'✅ User created! ID: {user_id}')
    print(f'   JWT token: {jwt_token[:50]}...')
    print()
    
    # Step 2: Create API token
    print('🔑 Creating API token...')
    token_resp = requests.put(
        f'{VIKUNJA_URL}/api/v1/tokens',
        headers={'Authorization': f'Bearer {jwt_token}'},
        json={
            'title': 'Bot Token (auto-generated)',
            'permissions': {}  # Empty = all permissions
        }
    )
    
    if token_resp.status_code != 200:
        print(f'❌ Token creation failed: {token_resp.status_code}')
        print(token_resp.text)
        return None
    
    token_data = token_resp.json()
    api_token = token_data.get('token')
    
    print(f'✅ API token created!')
    print(f'   Token: {api_token}')
    print()
    
    # Step 3: Test the token
    print('🧪 Testing API token...')
    test_resp = requests.get(
        f'{VIKUNJA_URL}/api/v1/projects',
        headers={'Authorization': f'Bearer {api_token}'}
    )
    
    if test_resp.status_code == 200:
        projects = test_resp.json()
        print(f'✅ Token works! Found {len(projects)} projects')
    else:
        print(f'❌ Token test failed: {test_resp.status_code}')
        print(test_resp.text)
        return None
    
    print()
    print('=' * 60)
    print('SUCCESS! User provisioned with API token')
    print('=' * 60)
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'User ID: {user_id}')
    print(f'API Token: {api_token}')
    print('=' * 60)
    
    return {
        'user_id': user_id,
        'username': username,
        'email': email,
        'password': password,
        'jwt_token': jwt_token,
        'api_token': api_token
    }

if __name__ == '__main__':
    result = create_vikunja_user_with_token()
    if result:
        sys.exit(0)
    else:
        sys.exit(1)

