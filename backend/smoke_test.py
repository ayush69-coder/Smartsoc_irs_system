#!/usr/bin/env python3
"""
Smoke test for PhishGuard Pro backend
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=200):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - {response.status_code}")
            return True
        else:
            print(f"❌ {method} {endpoint} - Expected {expected_status}, got {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:100]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Connection failed (server not running?)")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False

def run_smoke_tests():
    """Run smoke tests for all major endpoints"""
    print("🔥 Running PhishGuard Pro Smoke Tests")
    print("=" * 50)
    
    tests = []
    
    # Health check
    tests.append(("GET", "/api/health", None, None, 200))
    
    # Authentication
    tests.append(("POST", "/api/auth/login", {
        "username": "analyst",
        "password": "analyst123"
    }, None, 200))
    
    # Get token for authenticated tests
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": "analyst", 
        "password": "analyst123"
    })
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Authenticated endpoints
        tests.append(("GET", "/api/auth/me", None, auth_headers, 200))
        tests.append(("GET", "/api/auth/permissions", None, auth_headers, 200))
    
    # Verdict endpoint
    tests.append(("POST", "/api/verdict", {
        "url": "https://fake-bank.com",
        "text": "Verify your account now!",
        "source": "email"
    }, None, 200))
    
    # URL features
    tests.append(("POST", "/api/url/features", {
        "url": "https://example.com"
    }, None, 200))
    
    # Live feed
    tests.append(("POST", "/api/live", {
        "limit": 10,
        "offset": 0
    }, None, 200))
    
    # Policies
    tests.append(("GET", "/api/policies", None, None, 200))
    tests.append(("POST", "/api/policies/evaluate", {
        "event": {
            "url": "https://test.com",
            "score": 0.5
        }
    }, None, 200))
    
    # Graph
    tests.append(("GET", "/api/graph/query?domain=example.com", None, None, 200))
    
    # Model status
    tests.append(("GET", "/api/model/status", None, None, 200))
    
    # Review queue
    tests.append(("GET", "/api/review/queue", None, None, 200))
    
    # Audit logs
    tests.append(("GET", "/api/audit/logs?limit=5", None, None, 200))
    
    # Demo orchestrator
    tests.append(("GET", "/api/demo/campaigns", None, None, 200))
    
    # Sandbox
    tests.append(("POST", "/api/sandbox/submit", {
        "url": "https://example.com"
    }, None, 200))
    
    # Run all tests
    passed = 0
    total = len(tests)
    
    for method, endpoint, data, headers, expected_status in tests:
        if test_endpoint(method, endpoint, data, headers, expected_status):
            passed += 1
        time.sleep(0.1)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All smoke tests passed!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)