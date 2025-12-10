#!/usr/bin/env python
import json
import time
import sys

import requests

BASE = "http://127.0.0.1:8000"

def pretty(obj):
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception:
        return str(obj)

email = "e2e_user1@example.com"
username = "e2e_user1"
password = "StrongP@ss1"

print("Testing backend auth and analysis endpoints...")

# 1) Health
try:
    r = requests.get(f"{BASE}/health", timeout=5)
    print("Health:", r.status_code, r.text)
except Exception as e:
    print("Health request failed:", e)
    sys.exit(1)

# 2) Signup (ignore if already exists)
try:
    payload = {"email": email, "username": username, "password": password}
    r = requests.post(f"{BASE}/auth/signup", json=payload, timeout=10)
    print("Signup:", r.status_code, r.text)
    if r.status_code not in (200, 400):
        sys.exit(1)
except Exception as e:
    print("Signup failed:", e)
    sys.exit(1)

# 3) Login
try:
    payload = {"email": email, "password": password}
    r = requests.post(f"{BASE}/auth/login", json=payload, timeout=10)
    print("Login:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        sys.exit(1)
    tokens = r.json()
    access = tokens.get("access_token")
    if not access:
        print("No access token returned")
        sys.exit(1)
except Exception as e:
    print("Login failed:", e)
    sys.exit(1)

# 4) Quick analyze
try:
    headers = {"Authorization": f"Bearer {access}"}
    payload = {
        "code": "print('hello world')",
        "language": "python",
        "region": "usa",
        "filename": "hello.py",
    }
    r = requests.post(f"{BASE}/submissions/quick-analyze", json=payload, headers=headers, timeout=20)
    print("Quick Analyze:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        sys.exit(1)
except Exception as e:
    print("Quick analyze failed:", e)
    sys.exit(1)

print("All tests passed.")
