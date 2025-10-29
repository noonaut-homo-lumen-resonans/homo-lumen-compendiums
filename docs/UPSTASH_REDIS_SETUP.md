# Upstash Redis Setup Guide

## Overview

This guide shows you how to set up **Upstash Redis Cloud** for real-time event streaming between CSN Server (port 8001) and Ubuntu Playground (port 8002).

**Why Upstash?**
- Free tier: 10,000 commands/day (sufficient for development)
- Global distribution with low latency
- REST API (no need for Redis client binaries on Windows)
- Zero configuration

**Architecture:**
```
CSN Server (port 8001) → Upstash Redis Cloud → Ubuntu Playground (port 8002)
                              ↓
                    Real-time pub/sub events
                    (globally accessible)
```

---

## Step 1: Create Upstash Account

1. Go to: https://upstash.com
2. Click **"Sign Up"**
3. Sign up with:
   - GitHub account (recommended)
   - OR email + password

4. Verify your email if using email signup

**Free Tier Includes:**
- 10,000 commands/day
- Global replication
- TLS encryption
- No credit card required

---

## Step 2: Create Redis Database

1. After logging in, click **"Create Database"**

2. **Configure Database:**
   - **Name**: `homo-lumen-csn`
   - **Type**: Select **"Global"** (for low latency worldwide)
   - **Primary Region**: Select **"Europe"**
     - Recommended: `eu-west-1` (Ireland) or `eu-central-1` (Frankfurt)
     - Choose closest to Norway for lowest latency
   - **Read Regions**: Leave empty for now (can add later)
   - **TLS**: Keep enabled (default)
   - **Eviction**: Keep default (`noeviction`)

3. Click **"Create"**

**Creation takes ~30 seconds**

---

## Step 3: Get Connection Details

Once the database is created:

1. **Click on your database** (`homo-lumen-csn`)

2. **Find the "REST API" section** (scroll down)

3. **Copy these 2 values:**

   **a) UPSTASH_REDIS_REST_URL**
   ```
   Example: https://eu1-caring-dog-12345.upstash.io
   ```

   **b) UPSTASH_REDIS_REST_TOKEN**
   ```
   Example: AYX5ASQgMmE5ZjE2ZTAtODRhYi00NDRjLTk5ZTUtN2Y5MjQ5MjYxNWJhZGUyNTk3NGI3ZDY4NGI3ODlhOWY2Y2RmYmZiN2ZkYTU=
   ```

**Important:** Keep these secret! Do NOT commit to GitHub.

---

## Step 4: Configure Environment Variables

### 4.1 CSN Server Configuration

**File:** `ama-backend/.env`

**Add these lines** (replace with your actual values):
```bash
# Redis (Upstash Cloud) - Real-time event streaming
REDIS_URL=https://eu1-caring-dog-12345.upstash.io
REDIS_TOKEN=AYX5ASQgMmE5ZjE2ZTAtODRhYi00NDRjLTk5ZTUtN2Y5MjQ5MjYxNWJhZGUyNTk3NGI3ZDY4NGI3ODlhOWY2Y2RmYmZiN2ZkYTU=
```

**Exact location in `.env` file:**
- Line 42-43 (after Perplexity API key)
- Replace `<LEGG-INN-UPSTASH-REDIS-URL-HER>` with your URL
- Replace `<LEGG-INN-UPSTASH-REDIS-TOKEN-HER>` with your token

---

### 4.2 Ubuntu Playground Configuration

**File:** `ubuntu-playground/.env.local`

**Create this file if it doesn't exist:**
```bash
# Redis (Upstash Cloud) - Real-time event streaming
REDIS_URL=https://eu1-caring-dog-12345.upstash.io
REDIS_TOKEN=AYX5ASQgMmE5ZjE2ZTAtODRhYi00NDRjLTk5ZTUtN2Y5MjQ5MjYxNWJhZGUyNTk3NGI3ZDY4NGI3ODlhOWY2Y2RmYmZiN2ZkYTU=

# Agent API Keys (for workspace access)
AURORA_API_KEY=aurora-dev-key
```

**If `.env.local` already exists:**
- Just add the REDIS_URL and REDIS_TOKEN lines at the top

---

## Step 5: Test Connection

### 5.1 Test with Python

**Create test file:** `test_upstash_connection.py`

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="ama-backend/.env")

REDIS_URL = os.getenv("REDIS_URL")
REDIS_TOKEN = os.getenv("REDIS_TOKEN")

print(f"🔍 Testing Upstash Redis connection...")
print(f"📍 URL: {REDIS_URL}")
print(f"🔑 Token: {REDIS_TOKEN[:20]}...")

# Test 1: PING
print("\n✅ Test 1: PING")
response = requests.post(
    f"{REDIS_URL}/ping",
    headers={"Authorization": f"Bearer {REDIS_TOKEN}"}
)
print(f"Response: {response.text}")
assert response.json()["result"] == "PONG", "Ping failed!"

# Test 2: SET
print("\n✅ Test 2: SET key")
response = requests.post(
    f"{REDIS_URL}/set/test_key/homo_lumen",
    headers={"Authorization": f"Bearer {REDIS_TOKEN}"}
)
print(f"Response: {response.json()}")

# Test 3: GET
print("\n✅ Test 3: GET key")
response = requests.post(
    f"{REDIS_URL}/get/test_key",
    headers={"Authorization": f"Bearer {REDIS_TOKEN}"}
)
print(f"Response: {response.json()}")
assert response.json()["result"] == "homo_lumen", "Get failed!"

# Test 4: PUBLISH (pub/sub)
print("\n✅ Test 4: PUBLISH")
response = requests.post(
    f"{REDIS_URL}/publish/test_channel/test_message",
    headers={"Authorization": f"Bearer {REDIS_TOKEN}"}
)
print(f"Response: {response.json()}")

print("\n🎉 All Upstash tests passed!")
print("✅ Connection successful")
print("✅ SET/GET working")
print("✅ Pub/Sub working")
```

**Run test:**
```bash
cd "C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums"
python test_upstash_connection.py
```

**Expected output:**
```
🔍 Testing Upstash Redis connection...
📍 URL: https://eu1-caring-dog-12345.upstash.io
🔑 Token: AYX5ASQgMmE5ZjE2ZTAt...

✅ Test 1: PING
Response: {"result":"PONG"}

✅ Test 2: SET key
Response: {"result":"OK"}

✅ Test 3: GET key
Response: {"result":"homo_lumen"}

✅ Test 4: PUBLISH
Response: {"result":0}

🎉 All Upstash tests passed!
✅ Connection successful
✅ SET/GET working
✅ Pub/Sub working
```

---

## Step 6: Integration with CSN Server & Ubuntu Playground

Once connection is verified, the Redis publisher and subscriber will be integrated:

**CSN Server (port 8001):**
- Publishes consultation events to `csn:consultations`
- Publishes agent responses to `csn:agent:{agent_name}`

**Ubuntu Playground (port 8002):**
- Subscribes to all `csn:*` channels
- Logs events to SQLite database
- Triggers workspace actions based on events

**Event Flow Example:**
```
1. User asks collective intelligence consultation
2. CSN Server publishes event → Redis channel: "csn:consultations"
3. Ubuntu Playground subscriber receives event
4. Ubuntu Playground logs event to SQLite
5. Real-time dashboard updates (future feature)
```

---

## Troubleshooting

### Problem: "Invalid token" error

**Solution:**
1. Go back to Upstash dashboard
2. Regenerate REST API token
3. Update `.env` files with new token

### Problem: "Connection timeout"

**Solution:**
1. Check firewall settings (allow HTTPS outbound)
2. Try changing region (create new database in different region)
3. Verify internet connection

### Problem: "Module not found: requests"

**Solution:**
```bash
pip install requests python-dotenv
```

### Problem: "Can't find .env file"

**Solution:**
- Make sure you're running from project root
- Check file path in `load_dotenv()`
- Use absolute path if needed

---

## Monitoring & Limits

### View Usage

1. Go to Upstash dashboard
2. Click on your database
3. Scroll to **"Metrics"** section
4. See:
   - Commands/day usage
   - Request latency
   - Error rate

### Free Tier Limits

- **10,000 commands/day**
- **Max connections:** 1,000 concurrent
- **Max request size:** 1 MB
- **Max data size:** 256 MB

**If you hit limits:**
- Upgrade to Pay-as-you-go ($0.2 per 100K commands)
- OR optimize code to reduce commands

---

## Security Best Practices

1. **Never commit `.env` files** to GitHub
   - `.env` is already in `.gitignore`
   - Double-check before committing

2. **Rotate tokens regularly**
   - Every 3-6 months
   - Or immediately if exposed

3. **Use TLS** (enabled by default)
   - All connections encrypted

4. **IP Allowlist** (optional)
   - In Upstash dashboard → Settings → Allowed IPs
   - Only for production

---

## Next Steps

After setup is complete:

1. ✅ Redis publisher implemented in CSN Server
2. ✅ Redis subscriber implemented in Ubuntu Playground
3. ✅ Real-time event streaming active
4. ✅ Events logged to SQLite

**Test with:**
```bash
# Terminal 1: Start CSN Server
cd ama-backend
python -m uvicorn minimal_server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Start Ubuntu Playground
cd ubuntu-playground/api
python -m uvicorn main.local:app --host 0.0.0.0 --port 8002 --reload

# Terminal 3: Send test consultation
curl -X POST http://localhost:8001/collective-intelligence/consultation \
  -H "Content-Type: application/json" \
  -d '{"question": "Test Redis integration", "requester": "Osvald"}'

# Check Ubuntu Playground logs for received event
```

---

**Setup Time:** 10-15 minutes
**Cost:** Free (10K commands/day)
**Difficulty:** Easy

**Status:** ✅ Ready to implement

---

*Generated: 2025-10-28*
*Last Updated: 2025-10-28*
