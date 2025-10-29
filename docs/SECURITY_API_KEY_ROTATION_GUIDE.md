# API Key Rotation Guide - CRITICAL SECURITY
**Date:** October 29, 2025
**Priority:** CRITICAL (Complete within 24 hours)
**Context:** Orion's Infrastructure Audit revealed exposed credentials in documentation

---

## Executive Summary

**Exposed Credentials (5 categories):**
1. GitHub Personal Access Token
2. Google OAuth Client Secret
3. Upstash Redis Token
4. ClickUp API Key
5. Slack Workspace Credentials

**Risk Level:** HIGH - Credentials exposed in Google Drive documentation accessible to multiple agents
**Action Required:** Rotate ALL keys within 24 hours, implement secrets management

---

## Rotation Checklist

### 1. GitHub Personal Access Token ✅ PRIORITY 1

**Exposed Token:**
```
ghp_[REDACTED] (See Orion's Infrastructure Audit for details)
```

**Account:** noonaut-homo-lumen-resonans

**Steps to Rotate:**

1. **Revoke Old Token:**
   - Go to: https://github.com/settings/tokens
   - Find token: `ghp_[YOUR_OLD_TOKEN]` (see Orion's audit for actual value)
   - Click "Delete" or "Revoke"

2. **Generate New Token:**
   - Click "Generate new token (classic)"
   - Name: `Homo Lumen Resonans - Oct 2025`
   - Expiration: 90 days (set reminder for rotation)
   - Scopes needed:
     - ✅ `repo` (full repository access)
     - ✅ `workflow` (GitHub Actions)
     - ✅ `write:packages` (if using GitHub Packages)
   - Click "Generate token"
   - **COPY TOKEN IMMEDIATELY** (shown only once)

3. **Update GitHub Secrets:**
   - Repository: homo-lumen-compendiums
   - Go to: Settings → Secrets and variables → Actions
   - Update `GITHUB_TOKEN` (if exists) or create new secret
   - Paste new token

4. **Update Local Environment:**
   - File: `.env` (if exists)
   - Update: `GITHUB_TOKEN=<new_token>`
   - DO NOT commit `.env` to git

5. **Test Workflows:**
   - Go to: Actions tab
   - Manually trigger "Sync Learning Points" workflow
   - Verify success

**Verification:**
```bash
# Test new token (replace <new_token>)
curl -H "Authorization: token <new_token>" https://api.github.com/user
# Should return your user info, not 401 error
```

---

### 2. Google OAuth Client Secret ✅ PRIORITY 1

**Exposed Credentials:**
```
Project: Homo Lumen Resonans
Project ID: dotted-stage-476513-r4
OAuth Client ID: 818306373939-[REDACTED]
OAuth Client Secret: GOCSPX-[REDACTED]
```

**Steps to Rotate:**

1. **Delete Old OAuth Client:**
   - Go to: https://console.cloud.google.com/apis/credentials?project=dotted-stage-476513-r4
   - Find: OAuth 2.0 Client ID `818306373939-fm5p5hem7trphtfc9asm2mvb22dotf4g`
   - Click "DELETE" (trash icon)
   - Confirm deletion

2. **Create New OAuth Client:**
   - Click "+ CREATE CREDENTIALS" → "OAuth client ID"
   - Application type: "Web application"
   - Name: `Homo Lumen Resonans - Oct 2025`
   - Authorized redirect URIs:
     - `http://localhost:8001/oauth2callback`
     - `http://localhost:8002/oauth2callback`
     - (Add production URIs if deployed)
   - Click "CREATE"
   - **COPY Client ID and Client Secret** (shown once)

3. **Update Backend Configuration:**
   - File: `ubuntu-playground/api/blockchain/.env` (or similar)
   - Update:
     ```
     GOOGLE_CLIENT_ID=<new_client_id>
     GOOGLE_CLIENT_SECRET=<new_client_secret>
     ```

4. **Delete Old Token:**
   - File: `ubuntu-playground/api/blockchain/token.json`
   - Delete file (will force re-authentication)

5. **Re-authenticate:**
   - Start Ubuntu Playground: `python ubuntu-playground/api/main.py`
   - Browser popup will appear
   - Approve OAuth consent
   - Verify: `/api/dna/drive/status` and `/api/dna/sheets/status` return `connected: true`

**Verification:**
```bash
# After re-authentication
curl http://localhost:8001/api/dna/drive/status
# Should return: {"success": true, "connected": true, ...}
```

---

### 3. Upstash Redis Token ✅ PRIORITY 2

**Exposed Credentials:**
```
URL: https://eminent-mallard-35273.upstash.io
Token: AYnJAAI[REDACTED]
```

**Steps to Rotate:**

1. **Revoke Old Token (if possible):**
   - Go to: https://console.upstash.com/redis
   - Select database: `eminent-mallard-35273`
   - Navigate to: "REST API" or "Tokens" section
   - Look for token management options
   - Revoke/Delete old token if UI allows

2. **Generate New Token:**
   - In Upstash Console → Database → REST API
   - Click "Create New Token" or "Regenerate Token"
   - Copy new token

3. **Update Environment Variables:**
   - File: `ama-backend/.env` or similar
   - Update:
     ```
     UPSTASH_REDIS_REST_URL=https://eminent-mallard-35273.upstash.io
     UPSTASH_REDIS_REST_TOKEN=<new_token>
     ```

4. **Update GitHub Secrets (if used in workflows):**
   - Repository: homo-lumen-compendiums
   - Settings → Secrets → Actions
   - Update `UPSTASH_REDIS_TOKEN`

5. **Test Connection:**
   - Restart server
   - Verify Redis operations work (RPUSH/LPOP queue)

**Verification:**
```bash
# Test new token
curl https://eminent-mallard-35273.upstash.io/ping \
  -H "Authorization: Bearer <new_token>"
# Should return: {"result":"PONG"}
```

---

### 4. ClickUp API Key ✅ PRIORITY 2

**Exposed Credentials:**
```
API Key: pk_248656880_[REDACTED]
Project URL: https://app.clickup.com/90151846710/v/li/901516847618
```

**Steps to Rotate:**

1. **Revoke Old API Key:**
   - Go to: https://app.clickup.com/settings/apps
   - Find: API Token `pk_248656880_9ZNZH19JIPA7JNWWR34FC51QVKRFS44O`
   - Click "Revoke" or "Delete"

2. **Generate New API Key:**
   - In ClickUp Settings → Apps
   - Click "Generate" under "API Token"
   - **COPY TOKEN IMMEDIATELY**

3. **Update Environment Variables:**
   - File: `.env` (wherever ClickUp is configured)
   - Update: `CLICKUP_API_KEY=<new_token>`

4. **Update GitHub Secrets (if used):**
   - Repository settings
   - Update `CLICKUP_API_KEY`

**Verification:**
```bash
# Test new token
curl https://api.clickup.com/api/v2/user \
  -H "Authorization: <new_token>"
# Should return user info
```

---

### 5. Slack Workspace ✅ PRIORITY 3

**Exposed Credentials:**
```
Workspace: homolumenslack
Invite Link: https://join.slack.com/t/homolumenslack/shared_invite/zt-3gtmd7te8-w4...
```

**Risk Assessment:**
- Invite link has limited exposure risk (can be regenerated)
- Bot tokens (if any) are higher risk

**Steps:**

1. **Regenerate Invite Link:**
   - Go to: Slack workspace → Settings & administration → Invite people
   - Click "Copy invite link" → "Regenerate link"
   - Old link becomes invalid

2. **Check for Bot Tokens:**
   - Go to: https://api.slack.com/apps
   - Find: Homo Lumen app (if exists)
   - Navigate to: "OAuth & Permissions"
   - If bot tokens exist → Reinstall app (generates new tokens)

3. **Update Configurations:**
   - Update any stored Slack bot tokens in `.env` files
   - Update GitHub Secrets if Slack integration is automated

---

## Post-Rotation Actions

### 1. Implement Secrets Management ✅ HIGH PRIORITY

**Option A: Google Secret Manager (Recommended)**
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Store secret
gcloud secrets create github-token --data-file=- <<< "new_token_here"

# Retrieve in code (Python example)
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
name = "projects/dotted-stage-476513-r4/secrets/github-token/versions/latest"
response = client.access_secret_version(request={"name": name})
token = response.payload.data.decode("UTF-8")
```

**Option B: Environment Variables Only (Simpler)**
- Use `.env` files (NEVER commit to git)
- Ensure `.gitignore` includes `.env`
- Use `python-dotenv` package to load

**Option C: HashiCorp Vault (Advanced)**
- Requires Vault server setup
- Overkill for current scale

**Recommendation:** Use Google Secret Manager (already using Google Cloud Project)

---

### 2. Remove Credentials from Documentation ✅ CRITICAL

**Files to Audit:**

1. **Google Drive Documents:**
   - Search all docs for: "ghp_", "GOCSPX-", "pk_248656880"
   - Replace with: `[STORED IN GOOGLE SECRET MANAGER]`
   - Or: `[SEE .env FILE - NOT IN GIT]`

2. **Local Files:**
   ```bash
   # Search for exposed credentials (replace with actual exposed tokens)
   cd "C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums"
   grep -r "ghp_YOUR_TOKEN" .
   grep -r "GOCSPX-YOUR_SECRET" .
   ```

3. **GitHub Repository:**
   - Check commit history (use `git log -S "ghp_YOUR_TOKEN_PREFIX"`)
   - If found in history → use `git filter-repo` (NOT filter-branch)

---

### 3. Enable Automated Alerts ✅ MEDIUM PRIORITY

**GitHub Secret Scanning:**
1. Go to: Repository Settings → Code security and analysis
2. Enable: "Secret scanning"
3. Enable: "Push protection" (prevents accidental commits)

**Notifications:**
- GitHub will email if secrets detected in commits
- Upstash/ClickUp may offer similar features

---

### 4. Set Rotation Schedule ✅ MEDIUM PRIORITY

**Recommended Schedule:**
- **GitHub Token:** Rotate every 90 days (built-in expiration)
- **Google OAuth:** Rotate every 6 months (or on team member departure)
- **Redis/ClickUp:** Rotate every 12 months (or on security incident)

**Calendar Reminders:**
- January 28, 2026: Rotate GitHub token
- April 29, 2026: Rotate Google OAuth
- October 29, 2026: Annual security audit + all rotations

---

## Verification Checklist

After completing all rotations:

- [ ] GitHub workflows still run successfully
- [ ] Google Drive/Sheets API endpoints return `connected: true`
- [ ] Redis RPUSH/LPOP operations work
- [ ] ClickUp API calls succeed (if used)
- [ ] Slack integrations functional (if used)
- [ ] All exposed credentials removed from Google Drive docs
- [ ] `.gitignore` includes `.env` files
- [ ] GitHub secret scanning enabled
- [ ] Calendar reminders set for next rotation

---

## Emergency Contacts

**If Credentials Compromised:**
1. Rotate immediately (don't wait 24 hours)
2. Check audit logs:
   - GitHub: Settings → Security log
   - Google: https://myaccount.google.com/security
   - Upstash: Console → Logs
3. Document incident in `docs/SECURITY_INCIDENTS.md`
4. Notify team (Orion, Thalus, Zara)

---

## Documentation Updates Required

After rotation, update these files:

1. **This file:** Mark rotation date completed
2. **README.md:** Add section on secrets management
3. **`.env.example`:** Update with new variable names (not values!)
4. **Setup guides:** Update any onboarding docs

---

**Generated:** October 29, 2025
**Author:** Code (Agent #9) + Orion's Infrastructure Audit
**Next Review:** January 28, 2026 (90 days)
