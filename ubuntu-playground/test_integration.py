#!/usr/bin/env python3
"""
Test script for CSN Server → Ubuntu Playground integration
"""

import requests
import json
import sys

# Ensure UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
UBUNTU_PLAYGROUND_URL = "http://localhost:8002"
CSN_SERVER_URL = "http://localhost:8001"
API_KEY = "lira-local-dev-key"  # Using Lira's dev key

def test_health():
    """Test Ubuntu Playground health endpoint"""
    print("\n🏥 Testing Ubuntu Playground /health...")
    response = requests.get(f"{UBUNTU_PLAYGROUND_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_workspace_write():
    """Test writing a file to Ubuntu Playground workspace"""
    print("\n✍️ Testing /api/workspace/write...")

    headers = {"X-API-Key": API_KEY}
    payload = {
        "path": "shared/test_integration.txt",
        "content": "🌟 Genesis Moment: CSN Server ↔ Ubuntu Playground Integration Test\n\nTimestamp: 2025-10-28\nTest: First successful write from Lira agent\n"
    }

    response = requests.post(
        f"{UBUNTU_PLAYGROUND_URL}/api/workspace/write",
        headers=headers,
        json=payload
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_workspace_read():
    """Test reading a file from Ubuntu Playground workspace"""
    print("\n📖 Testing /api/workspace/read...")

    headers = {"X-API-Key": API_KEY}
    payload = {"path": "shared/test_integration.txt"}

    response = requests.post(
        f"{UBUNTU_PLAYGROUND_URL}/api/workspace/read",
        headers=headers,
        json=payload
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_execute_action():
    """Test CSN Server → Ubuntu Playground action execution"""
    print("\n🎯 Testing /api/execute-action...")

    headers = {"X-API-Key": API_KEY}
    payload = {
        "agent": "lira",
        "action_type": "create_document",
        "payload": {
            "title": "Genesis Integration Test",
            "content": "This is the first action from CSN Server to Ubuntu Playground",
            "tags": ["integration", "genesis", "csn-server"]
        }
    }

    response = requests.post(
        f"{UBUNTU_PLAYGROUND_URL}/api/execute-action",
        headers=headers,
        json=payload
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_csn_server_health():
    """Verify CSN Server is running"""
    print("\n🌐 Checking CSN Server health...")
    try:
        response = requests.get(f"{CSN_SERVER_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"CSN Server: ✅ Running")
        return True
    except requests.exceptions.ConnectionError:
        print("CSN Server: ❌ Not reachable")
        return False

def main():
    print("=" * 60)
    print("🚀 CSN SERVER ↔ UBUNTU PLAYGROUND INTEGRATION TEST")
    print("=" * 60)

    tests = [
        ("CSN Server Health", test_csn_server_health),
        ("Ubuntu Playground Health", test_health),
        ("Workspace Write", test_workspace_write),
        ("Workspace Read", test_workspace_read),
        ("Execute Action", test_execute_action),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(1 for _, result in results if result)
    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Integration successful!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
