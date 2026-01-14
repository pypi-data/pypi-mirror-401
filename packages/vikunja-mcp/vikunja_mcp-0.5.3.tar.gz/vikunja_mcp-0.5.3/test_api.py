#!/usr/bin/env python3
"""Test Vikunja API directly to debug why project 153 returns 0 tasks."""

import os
import sys
import psycopg2
from cryptography.fernet import Fernet
import requests
import json

# Database connection
DATABASE_URL = "postgresql://factumerit:ZR2gEnBwHaABuyZt1HcjJp92vAUvWEfS@dpg-d54tgckhg0os739oddpg-a.oregon-postgres.render.com/matrix_jfmr"

# Get encryption key from environment
FERNET_KEY = os.environ.get("FERNET_KEY")
if not FERNET_KEY:
    print("ERROR: FERNET_KEY not set")
    sys.exit(1)

cipher = Fernet(FERNET_KEY.encode())

# Get token from database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("""
    SELECT encrypted_token, instance_url 
    FROM user_tokens 
    WHERE user_id = '@i2:matrix.factumerit.app' 
    AND vikunja_instance = 'personal'
""")
row = cur.fetchone()
conn.close()

if not row:
    print("ERROR: No token found")
    sys.exit(1)

encrypted_token = bytes(row[0])
instance_url = row[1]

# Decrypt token
token = cipher.decrypt(encrypted_token).decode()

print(f"Instance URL: {instance_url}")
print(f"Token: {token[:20]}...")
print()

# Test API endpoints
headers = {"Authorization": f"Bearer {token}"}

# 1. Test /api/v1/projects (list all projects)
print("=" * 60)
print("TEST 1: GET /api/v1/projects")
print("=" * 60)
response = requests.get(f"{instance_url}/api/v1/projects", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    projects = response.json()
    print(f"Found {len(projects)} projects:")
    for p in projects[:10]:  # Show first 10
        print(f"  - ID {p['id']}: {p['title']}")
    
    # Check if project 153 exists
    project_153 = next((p for p in projects if p['id'] == 153), None)
    if project_153:
        print(f"\n✓ Project 153 found: {project_153['title']}")
    else:
        print(f"\n✗ Project 153 NOT found in project list!")
else:
    print(f"Error: {response.text}")

print()

# 2. Test /api/v1/projects/153 (get specific project)
print("=" * 60)
print("TEST 2: GET /api/v1/projects/153")
print("=" * 60)
response = requests.get(f"{instance_url}/api/v1/projects/153", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    project = response.json()
    print(f"Project: {project['title']}")
    print(f"Description: {project.get('description', 'N/A')}")
else:
    print(f"Error: {response.text}")

print()

# 3. Test /api/v1/projects/153/tasks (get tasks in project)
print("=" * 60)
print("TEST 3: GET /api/v1/projects/153/tasks")
print("=" * 60)
response = requests.get(f"{instance_url}/api/v1/projects/153/tasks", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response body length: {len(response.text)}")
if response.status_code == 200:
    tasks = response.json()
    print(f"Tasks returned: {len(tasks)}")
    if tasks:
        print("First 5 tasks:")
        for task in tasks[:5]:
            print(f"  - #{task['id']}: {task['title']}")
    else:
        print("Empty array returned!")
        print(f"Raw response: {response.text}")
else:
    print(f"Error: {response.text}")

print()

# 4. Test /api/v1/tasks/all (get all tasks)
print("=" * 60)
print("TEST 4: GET /api/v1/tasks/all?filter_by=project&filter_value=153")
print("=" * 60)
response = requests.get(
    f"{instance_url}/api/v1/tasks/all",
    headers=headers,
    params={"filter_by": "project", "filter_value": "153"}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    tasks = data if isinstance(data, list) else data.get("tasks", [])
    print(f"Tasks returned: {len(tasks)}")
    if tasks:
        print("First 5 tasks:")
        for task in tasks[:5]:
            print(f"  - #{task['id']}: {task['title']}")
else:
    print(f"Error: {response.text}")

