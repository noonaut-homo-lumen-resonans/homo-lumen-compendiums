# 🧬 GENOMOS Google Workspace Setup Guide

Complete guide for setting up Google Drive and Google Sheets integration with GENOMOS blockchain system.

**Time Required:** 15-20 minutes
**Prerequisites:** Google account, Google Cloud Console access

---

## 📋 Quick Checklist

- [ ] Step 1: Create Google Cloud Project
- [ ] Step 2: Enable APIs (Drive + Sheets)
- [ ] Step 3: Create OAuth 2.0 Credentials
- [ ] Step 4: Create Google Drive Folder
- [ ] Step 5: Create Google Sheets Spreadsheet
- [ ] Step 6: Configure .env file
- [ ] Step 7: Install Python dependencies
- [ ] Step 8: Run OAuth authentication flow
- [ ] Step 9: Test connectivity

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **NEW PROJECT**
3. **Project name:** `GENOMOS` (or similar)
4. Click **CREATE**
5. Wait for project creation (~30 seconds)
6. **Select your new project** from the dropdown

---

## Step 2: Enable APIs

### Enable Google Drive API

1. Go to: https://console.cloud.google.com/apis/library/drive.googleapis.com
2. Make sure your GENOMOS project is selected
3. Click **ENABLE**
4. Wait for confirmation

### Enable Google Sheets API

1. Go to: https://console.cloud.google.com/apis/library/sheets.googleapis.com
2. Make sure your GENOMOS project is selected
3. Click **ENABLE**
4. Wait for confirmation

---

## Step 3: Create OAuth 2.0 Credentials

### 3a. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
   - Link: https://console.cloud.google.com/apis/credentials/consent
2. Choose user type:
   - **External** (if personal Google account)
   - **Internal** (if using Google Workspace)
3. Click **CREATE**
4. Fill in **App information:**
   - App name: `GENOMOS`
   - User support email: (your email)
   - Developer contact: (your email)
5. Click **SAVE AND CONTINUE**
6. **Scopes** page:
   - Click **ADD OR REMOVE SCOPES**
   - Search for "drive" and select:
     - `https://www.googleapis.com/auth/drive.file` ✅
   - Search for "sheets" and select:
     - `https://www.googleapis.com/auth/spreadsheets` ✅
   - Click **UPDATE**
   - Click **SAVE AND CONTINUE**
7. **Test users** page (if External):
   - Click **+ ADD USERS**
   - Add your email address
   - Click **SAVE AND CONTINUE**
8. Review and click **BACK TO DASHBOARD**

### 3b. Create OAuth Client ID

1. Go to **APIs & Services** → **Credentials**
   - Link: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `GENOMOS Desktop Client`
5. Click **CREATE**
6. **Download JSON:**
   - Click the **Download** button (⬇️ icon)
   - Save file as `client_secret.json`
7. **Move the file:**
   ```bash
   mv ~/Downloads/client_secret_*.json ubuntu-playground/credentials/client_secret.json
   ```

---

## Step 4: Create Google Drive Folder

1. Go to [Google Drive](https://drive.google.com/)
2. Click **+ New** → **New folder**
3. Name: `GENOMOS Backups`
4. Click **CREATE**
5. **Open the folder** (double-click)
6. **Copy the Folder ID** from URL:
   ```
   https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j
                                           ^^^^^^^^^^^^^^^^^^^^
                                           This is your FOLDER_ID
   ```
7. Save this ID for Step 6

---

## Step 5: Create Google Sheets Spreadsheet

### 5a. Create Spreadsheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Click **Blank** to create new spreadsheet
3. Name it: `GENOMOS Analytics`

### 5b. Create Required Sheets (Tabs)

You need to create **4 sheets** with specific columns:

#### Sheet 1: Consultations

1. Rename "Sheet1" → `Consultations`
2. Add header row:
   ```
   A1: Timestamp
   B1: ID
   C1: Question
   D1: Agents
   E1: SMK Refs
   F1: BiofeltContext
   G1: Status
   ```
3. **Optional:** Bold the header row, add freeze (View → Freeze → 1 row)

#### Sheet 2: Patterns

1. Click **+** to add new sheet
2. Name: `Patterns`
3. Add header row:
   ```
   A1: Timestamp
   B1: Pattern ID
   C1: Type
   D1: Confidence
   E1: Description
   F1: Data
   ```

#### Sheet 3: Agent Activity

1. Click **+** to add new sheet
2. Name: `Agent Activity`
3. Add header row:
   ```
   A1: Agent
   B1: Total Genes
   C1: SMK Count
   D1: Mutation Count
   E1: Last Activity
   ```

#### Sheet 4: Daily Metrics

1. Click **+** to add new sheet
2. Name: `Daily Metrics`
3. Add header row:
   ```
   A1: Date
   B1: Total Blocks
   C1: New Consultations
   D1: New Patterns
   E1: Active Agents
   ```

### 5c. Get Spreadsheet ID

1. **Copy the Spreadsheet ID** from URL:
   ```
   https://docs.google.com/spreadsheets/d/1H4ywZFm80_0697_jUrlwXmklV5I6Y8_o1KpB0XuAJ5M/edit
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                          This is your SPREADSHEET_ID
   ```
2. Save this ID for Step 6

---

## Step 6: Configure .env File

1. Navigate to ubuntu-playground directory:
   ```bash
   cd ubuntu-playground
   ```

2. Copy example file (if not done already):
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` file and update these variables:
   ```bash
   # Google Workspace Integration
   GOOGLE_CLIENT_SECRET_FILE=credentials/client_secret.json
   GOOGLE_TOKEN_FILE=credentials/token.json
   GOOGLE_DRIVE_FOLDER_ID=<PASTE_YOUR_DRIVE_FOLDER_ID>
   GOOGLE_SHEETS_SPREADSHEET_ID=<PASTE_YOUR_SPREADSHEET_ID>

   # Scheduling (optional, defaults shown)
   BACKUP_SCHEDULE_HOUR=2
   PATTERN_ANALYSIS_INTERVAL_HOURS=6

   # Database
   DATABASE_PATH=./data/genomos.db
   ```

4. Replace:
   - `<PASTE_YOUR_DRIVE_FOLDER_ID>` with the ID from Step 4
   - `<PASTE_YOUR_SPREADSHEET_ID>` with the ID from Step 5c

5. Save the file

---

## Step 7: Install Python Dependencies

```bash
cd ubuntu-playground
pip install -r requirements.txt
```

**Required packages:**
- `google-auth==2.23.4`
- `google-auth-oauthlib==1.1.0`
- `google-api-python-client==2.108.0`
- `gspread==5.12.0`
- `apscheduler==3.10.4`
- `scikit-learn==1.3.2`

---

## Step 8: Run OAuth Authentication Flow

### 8a. Start API Server

```bash
cd ubuntu-playground/api
uvicorn main:app --reload
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 8b. Trigger OAuth Flow

Open a **new terminal** and run:

```bash
curl http://localhost:8000/api/dna/drive/status
```

### 8c. Authorize in Browser

1. **Browser window will open automatically**
2. Sign in with your Google account
3. You'll see: "Google hasn't verified this app"
   - Click **Advanced** → **Go to GENOMOS (unsafe)**
   - (This is normal for development apps)
4. Grant permissions:
   - ✅ See and download files from Google Drive
   - ✅ View and manage spreadsheets in Google Sheets
5. Click **Continue**
6. Browser will show: "The authentication flow has completed. You may close this window."

### 8d. Verify Token Created

```bash
ls -la ubuntu-playground/credentials/
```

You should see:
```
client_secret.json  ← You created this
token.json          ← Auto-generated! ✅
```

---

## Step 9: Test Connectivity

Run these tests to verify everything works:

### Test 1: Google Drive Status

```bash
curl http://localhost:8000/api/dna/drive/status
```

Expected response:
```json
{
  "status": "connected",
  "authenticated": true,
  "folder_id": "1a2b3c4d5e6f7g8h9i0j"
}
```

### Test 2: Google Sheets Status

```bash
curl http://localhost:8000/api/dna/sheets/status
```

Expected response:
```json
{
  "status": "connected",
  "spreadsheet_id": "1H4ywZFm80_0697_jUrlwXmklV5I6Y8_o1KpB0XuAJ5M",
  "spreadsheet_name": "GENOMOS Analytics",
  "sheets": ["Consultations", "Patterns", "Agent Activity", "Daily Metrics"]
}
```

### Test 3: Create Backup

```bash
curl -X POST http://localhost:8000/api/dna/drive/backup
```

Expected response:
```json
{
  "success": true,
  "file_id": "1xyz...",
  "file_name": "genomos_backup_20251029_133000.db",
  "size_bytes": 24576
}
```

### Test 4: List Backups

```bash
curl http://localhost:8000/api/dna/drive/backups
```

Expected response:
```json
{
  "backups": [
    {
      "file_id": "1xyz...",
      "name": "genomos_backup_20251029_133000.db",
      "created": "2025-10-29T13:30:00Z",
      "size_bytes": 24576
    }
  ],
  "count": 1
}
```

### Test 5: Scheduler Status

```bash
curl http://localhost:8000/api/dna/scheduler/status
```

Expected response:
```json
{
  "scheduler_running": true,
  "jobs": [
    {
      "id": "daily_backup",
      "name": "Daily Blockchain Backup",
      "next_run": "2025-10-30T02:00:00",
      "trigger": "cron"
    },
    {
      "id": "pattern_analysis",
      "name": "Pattern Recognition Analysis",
      "next_run": "2025-10-29T18:00:00",
      "trigger": "interval"
    },
    {
      "id": "daily_metrics",
      "name": "Daily Metrics Logger",
      "next_run": "2025-10-29T23:55:00",
      "trigger": "cron"
    }
  ]
}
```

---

## ✅ Success Checklist

If all tests pass, you have successfully:

- ✅ Created Google Cloud Project
- ✅ Enabled Drive and Sheets APIs
- ✅ Created OAuth 2.0 credentials
- ✅ Created Drive backup folder
- ✅ Created Sheets analytics spreadsheet
- ✅ Configured environment variables
- ✅ Installed Python dependencies
- ✅ Completed OAuth authentication
- ✅ Verified connectivity to Drive and Sheets

**Your GENOMOS system now has:**
- 🔄 **Automatic daily backups** to Google Drive (2 AM)
- 📊 **Real-time logging** to Google Sheets
- 🔍 **Pattern analysis** every 6 hours
- 📈 **Daily metrics** dashboard (23:55)

---

## 🔍 Troubleshooting

### Error: "client_secret.json not found"

**Cause:** OAuth credentials file not in correct location

**Fix:**
```bash
# Check if file exists
ls ubuntu-playground/credentials/client_secret.json

# If not, download from Google Cloud Console:
# 1. Go to APIs & Services → Credentials
# 2. Find your OAuth 2.0 Client ID
# 3. Click download button (⬇️)
# 4. Move to credentials folder
mv ~/Downloads/client_secret_*.json ubuntu-playground/credentials/client_secret.json
```

### Error: "invalid_grant" or "Token has been expired or revoked"

**Cause:** Token expired or corrupted

**Fix:**
```bash
# Delete old token
rm ubuntu-playground/credentials/token.json

# Restart server
# Re-run: curl http://localhost:8000/api/dna/drive/status
# Browser will open for re-authorization
```

### Error: "Access not configured"

**Cause:** APIs not enabled in Google Cloud Console

**Fix:**
1. Enable Drive API: https://console.cloud.google.com/apis/library/drive.googleapis.com
2. Enable Sheets API: https://console.cloud.google.com/apis/library/sheets.googleapis.com
3. Make sure correct project is selected

### Error: "The caller does not have permission"

**Cause:** OAuth scopes missing or insufficient

**Fix:**
1. Delete `token.json`
2. Go to Google Cloud Console → OAuth consent screen
3. Add scopes:
   - `https://www.googleapis.com/auth/drive.file`
   - `https://www.googleapis.com/auth/spreadsheets`
4. Re-authenticate (browser will open)

### Error: "Spreadsheet not found"

**Cause:** Wrong spreadsheet ID or no access

**Fix:**
1. Double-check Spreadsheet ID in `.env`
2. Make sure spreadsheet is created with your Google account
3. Try accessing: `https://docs.google.com/spreadsheets/d/<YOUR_ID>/edit`

---

## 📚 Next Steps

After successful setup:

1. **Test Consultation Logging**
   ```bash
   curl -X POST http://localhost:8000/api/store-consultation \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Test question",
       "agents": ["manus", "orion"],
       "response": "Test response",
       "smk_references": ["SMK#001"],
       "biofelt_context": {"hrv_ms": 45}
     }'
   ```
   - Check "Consultations" sheet in Google Sheets ✅

2. **Trigger Manual Pattern Analysis**
   ```bash
   curl -X POST http://localhost:8000/api/dna/patterns/analyze \
     -H "Content-Type: application/json" \
     -d '{"min_confidence": 0.5, "lookback_days": 30}'
   ```
   - Check "Patterns" sheet in Google Sheets ✅

3. **Monitor Scheduled Jobs**
   - Daily backup runs at 2 AM
   - Pattern analysis runs every 6 hours
   - Daily metrics logged at 23:55

4. **Explore API Documentation**
   - Visit: http://localhost:8000/docs
   - Browse all 60+ API endpoints
   - Test endpoints interactively

---

## 🔐 Security Best Practices

1. **Never commit secrets to git:**
   - `client_secret.json` ✅ Already in .gitignore
   - `token.json` ✅ Already in .gitignore
   - `.env` ✅ Already in .gitignore

2. **Rotate OAuth credentials periodically:**
   - Delete old OAuth Client ID in Google Cloud Console
   - Create new credentials
   - Update `client_secret.json`
   - Re-authenticate

3. **Monitor API usage:**
   - Check quotas: https://console.cloud.google.com/apis/dashboard
   - Drive API: 20,000 requests/100 seconds
   - Sheets API: 500 requests/100 seconds

4. **Backup your backups:**
   - Google Drive backups are your primary backup
   - Consider periodic exports to local storage
   - Test restore procedures regularly

---

## 📖 Related Documentation

- [GENOMOS_ENHANCEMENTS_COMPLETE.md](../GENOMOS_ENHANCEMENTS_COMPLETE.md) - Full implementation details
- [SMK#045](../SMK/SMK#045_GENOMOS-Google-Workspace-Pattern-Mobile-Integration.md) - Strategic documentation
- [credentials/README.md](credentials/README.md) - Credentials folder guide
- [Google Drive Manager](api/blockchain/google_drive_manager.py) - Source code
- [Google Sheets Manager](api/blockchain/google_sheets_manager.py) - Source code

---

**Questions or issues?** Check the troubleshooting section or review the source code documentation.

**Setup complete!** 🎉 Your GENOMOS system is now integrated with Google Workspace.
