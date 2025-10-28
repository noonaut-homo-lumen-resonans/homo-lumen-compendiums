"""
Test Upstash Redis Connection

This script verifies that your Upstash Redis configuration is working correctly.
Run this after setting up REDIS_URL and REDIS_TOKEN in ama-backend/.env
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="ama-backend/.env")

REDIS_URL = os.getenv("REDIS_URL")
REDIS_TOKEN = os.getenv("REDIS_TOKEN")

def test_upstash():
    """Test Upstash Redis connection with 4 tests"""

    print("="*60)
    print("🔍 UPSTASH REDIS CONNECTION TEST")
    print("="*60)

    # Check if credentials are set
    if not REDIS_URL or not REDIS_TOKEN:
        print("❌ ERROR: Redis credentials not found in .env file")
        print("\nPlease set these in ama-backend/.env:")
        print("  REDIS_URL=<your-upstash-url>")
        print("  REDIS_TOKEN=<your-upstash-token>")
        return False

    print(f"\n📍 URL: {REDIS_URL}")
    print(f"🔑 Token: {REDIS_TOKEN[:20]}...")
    print()

    headers = {"Authorization": f"Bearer {REDIS_TOKEN}"}

    # Test 1: PING
    print("✅ Test 1: PING")
    try:
        response = requests.post(f"{REDIS_URL}/ping", headers=headers, timeout=10)
        result = response.json()
        print(f"   Response: {result}")
        if result.get("result") != "PONG":
            print(f"   ❌ Expected PONG, got: {result}")
            return False
        print("   ✅ PING successful")
    except Exception as e:
        print(f"   ❌ PING failed: {e}")
        return False

    # Test 2: SET
    print("\n✅ Test 2: SET key")
    try:
        response = requests.post(
            f"{REDIS_URL}/set/test_key/homo_lumen",
            headers=headers,
            timeout=10
        )
        result = response.json()
        print(f"   Response: {result}")
        if result.get("result") != "OK":
            print(f"   ❌ SET failed: {result}")
            return False
        print("   ✅ SET successful")
    except Exception as e:
        print(f"   ❌ SET failed: {e}")
        return False

    # Test 3: GET
    print("\n✅ Test 3: GET key")
    try:
        response = requests.post(
            f"{REDIS_URL}/get/test_key",
            headers=headers,
            timeout=10
        )
        result = response.json()
        print(f"   Response: {result}")
        if result.get("result") != "homo_lumen":
            print(f"   ❌ Expected 'homo_lumen', got: {result}")
            return False
        print("   ✅ GET successful")
    except Exception as e:
        print(f"   ❌ GET failed: {e}")
        return False

    # Test 4: PUBLISH (pub/sub)
    print("\n✅ Test 4: PUBLISH (pub/sub)")
    try:
        response = requests.post(
            f"{REDIS_URL}/publish/test_channel/test_message",
            headers=headers,
            timeout=10
        )
        result = response.json()
        print(f"   Response: {result}")
        # result is number of subscribers (0 is OK for test)
        if "result" not in result:
            print(f"   ❌ PUBLISH failed: {result}")
            return False
        print(f"   ✅ PUBLISH successful (subscribers: {result.get('result')})")
    except Exception as e:
        print(f"   ❌ PUBLISH failed: {e}")
        return False

    # Cleanup: DELETE test key
    print("\n🧹 Cleanup: DELETE test_key")
    try:
        response = requests.post(
            f"{REDIS_URL}/del/test_key",
            headers=headers,
            timeout=10
        )
        result = response.json()
        print(f"   Response: {result}")
        print("   ✅ Cleanup successful")
    except Exception as e:
        print(f"   ⚠️  Cleanup warning: {e}")

    print("\n" + "="*60)
    print("🎉 ALL UPSTASH TESTS PASSED!")
    print("="*60)
    print("\n✅ Connection successful")
    print("✅ SET/GET working")
    print("✅ Pub/Sub working")
    print("\n🚀 Your Upstash Redis is ready for CSN Server integration!")
    print()

    return True

if __name__ == "__main__":
    success = test_upstash()
    exit(0 if success else 1)
