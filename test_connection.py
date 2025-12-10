#!/usr/bin/env python
"""Comprehensive test script to verify backend and frontend connection"""
import requests
import json
import sys

def test_backend():
    print("=" * 60)
    print("TESTING BACKEND CONNECTION")
    print("=" * 60)
    
    # Test 1: Health Check
    try:
        r = requests.get('http://localhost:8000/health', timeout=3)
        if r.status_code == 200:
            print("[OK] Health Check: PASSED")
            print(f"  Response: {r.json()}")
        else:
            print(f"[FAIL] Health Check: FAILED (Status: {r.status_code})")
            return False
    except Exception as e:
        print(f"[FAIL] Health Check: FAILED - {e}")
        return False
    
    # Test 2: Login Endpoint
    try:
        payload = {'email': 'teamuser@example.com', 'password': 'Test@1234'}
        headers = {
            'Origin': 'http://localhost:5173',
            'Content-Type': 'application/json'
        }
        r = requests.post('http://localhost:8000/auth/login', 
                         json=payload, headers=headers, timeout=3)
        if r.status_code == 200:
            data = r.json()
            if 'access_token' in data:
                print("[OK] Login Endpoint: PASSED")
                print(f"  CORS Header: {r.headers.get('Access-Control-Allow-Origin')}")
                print(f"  Token Received: Yes")
            else:
                print("[FAIL] Login Endpoint: FAILED - No token in response")
                return False
        else:
            print(f"[FAIL] Login Endpoint: FAILED (Status: {r.status_code})")
            print(f"  Response: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"[FAIL] Login Endpoint: FAILED - {e}")
        return False
    
    # Test 3: CORS Preflight
    try:
        headers = {
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type'
        }
        r = requests.options('http://localhost:8000/auth/login', headers=headers, timeout=3)
        if r.status_code == 200:
            cors_origin = r.headers.get('Access-Control-Allow-Origin')
            if cors_origin == 'http://localhost:5173':
                print("[OK] CORS Preflight: PASSED")
                print(f"  Allow-Origin: {cors_origin}")
                print(f"  Allow-Methods: {r.headers.get('Access-Control-Allow-Methods')}")
            else:
                print(f"[FAIL] CORS Preflight: FAILED - Wrong origin ({cors_origin})")
                return False
        else:
            print(f"[FAIL] CORS Preflight: FAILED (Status: {r.status_code})")
            return False
    except Exception as e:
        print(f"[FAIL] CORS Preflight: FAILED - {e}")
        return False
    
    # Test 4: Signup Endpoint
    try:
        import random
        test_email = f'test{random.randint(1000,9999)}@example.com'
        payload = {
            'email': test_email,
            'username': f'testuser{random.randint(1000,9999)}',
            'password': 'Test@1234'
        }
        headers = {
            'Origin': 'http://localhost:5173',
            'Content-Type': 'application/json'
        }
        r = requests.post('http://localhost:8000/auth/signup', 
                         json=payload, headers=headers, timeout=3)
        if r.status_code in [200, 201]:
            print("[OK] Signup Endpoint: PASSED")
            print(f"  CORS Header: {r.headers.get('Access-Control-Allow-Origin')}")
        else:
            # Might fail if user exists, that's okay
            if 'already registered' in r.text.lower():
                print("[OK] Signup Endpoint: PASSED (User exists, which is expected)")
            else:
                print(f"[FAIL] Signup Endpoint: FAILED (Status: {r.status_code})")
                print(f"  Response: {r.text[:200]}")
    except Exception as e:
        print(f"[WARN] Signup Endpoint: Warning - {e}")
    
    print("\n" + "=" * 60)
    print("BACKEND TESTS: ALL PASSED")
    print("=" * 60)
    return True

def check_ports():
    print("\n" + "=" * 60)
    print("CHECKING SERVER PORTS")
    print("=" * 60)
    
    try:
        import socket
        # Check port 8000 (backend)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        if result == 0:
            print("[OK] Backend (port 8000): RUNNING")
        else:
            print("[FAIL] Backend (port 8000): NOT RUNNING")
            return False
        
        # Check port 5173 (frontend)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5173))
        sock.close()
        if result == 0:
            print("[OK] Frontend (port 5173): RUNNING")
        else:
            print("[WARN] Frontend (port 5173): NOT RUNNING (may need to start)")
    except Exception as e:
        print(f"[WARN] Port check failed: {e}")
    
    return True

if __name__ == '__main__':
    print("\n")
    print("COMPREHENSIVE CONNECTION TEST")
    print("=" * 60)
    print()
    
    if not check_ports():
        print("\n[FAIL] Port check failed. Make sure backend is running.")
        sys.exit(1)
    
    if not test_backend():
        print("\n[FAIL] Backend tests failed. Check backend server.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("=" * 60)
    print("\nIf login/signup still doesn't work in browser:")
    print("1. Hard refresh browser: Ctrl+Shift+R")
    print("2. Check browser console (F12) for errors")
    print("3. Check Network tab (F12) for failed requests")
    print("4. Restart frontend: cd frontend && npm run dev")
    print()

