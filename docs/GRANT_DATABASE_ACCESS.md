# Grant API Access to Discovered Databases

This guide will help you grant your Notion integration access to the 14 discovered databases.

---

## Prerequisites

You need:
- Admin access to the Notion workspace containing these databases
- The Notion integration that created the current API key

---

## Step 1: Identify Your Notion Integration

First, we need to find which integration is currently being used.

### Find Integration Name

1. Go to **https://www.notion.so/my-integrations**
2. Look for an integration with the API key: `4dcd1dce-c52d-43df-9505-ed0b3061f9f2`
3. Note the integration name (likely something like "Homo Lumen Compendiums" or similar)

**Tip:** You can verify which integration by checking which one has access to your current working databases:
- CS Database (2988fec9-2931-803a-8703-000bb973304e)
- SL Database (2988fec929318045a354ffe8d2f13fe1)
- KD Database (2988fec9293180838c4bd5e13138ddf2)
- EM Database (2988fec9-2931-80f4-8961-000b8710e0a5)

---

## Step 2: Option A - Grant Access via Database Settings (Recommended)

This is the easiest method if all databases are in the same workspace as your existing databases.

### For Each Database:

#### 1. Spektral Dimensjoner
1. Open: https://www.notion.so/Spektral-Dimensjoner-1d48fec9293180929092f2553a9f85aa
2. Click the **"..."** menu (top-right corner)
3. Select **"Connections"** or **"Add connections"**
4. Find and click your integration name (from Step 1)
5. Click **"Confirm"** to grant access

#### 2. Phoenix-syklus
1. Open: https://www.notion.so/Phoenix-syklus-1d48fec92931807b9e27c445b9840539
2. Click **"..."** → **"Connections"**
3. Select your integration
4. Confirm

#### 3. How we feel
1. Open: https://www.notion.so/How-we-feel-1d48fec9293180b393c5c62a002280d0
2. Click **"..."** → **"Connections"**
3. Select your integration
4. Confirm

#### 4. Dagbok 2020 EchoLog
1. Open: https://www.notion.so/Dagbok-2020-EchoLog-1db8fec9293180caa349fbe34ba1097e
2. Click **"..."** → **"Connections"**
3. Select your integration
4. Confirm

#### 5-14. Remaining Databases

Repeat the same process for these URLs:

5. https://www.notion.so/1dd8fec9293180298d8bd2c5d5330563
6. https://www.notion.so/1dd8fec92931808ebc38ce8fc988b1a0
7. https://www.notion.so/1dd8fec929318061be62facd8439da53
8. https://www.notion.so/1e68fec9293180ba9264dd5dafbf53b6
9. https://www.notion.so/1e68fec929318052afe2fe6ee282108e
10. https://www.notion.so/1e68fec929318069bd61e2a8f22221f7
11. https://www.notion.so/28e8fec9293180cbaa57d99549147b97
12. https://www.notion.so/28e8fec929318056a2dcc2bb28fd166d
13. https://www.notion.so/8b18dd1769ab48a6a70ec38b74e5140f
14. https://www.notion.so/2988fec9293180509658e93447b3b259

For each:
- Click **"..."** → **"Connections"**
- Select your integration
- Confirm

---

## Step 2: Option B - Create New Integration (If Different Workspace)

If the discovered databases are in a **different Notion workspace** than your current databases, you'll need a second integration.

### Create New Integration

1. **Go to:** https://www.notion.so/my-integrations
2. **Click:** "New integration"
3. **Name:** "Homo Lumen Personal Data" (or any name you prefer)
4. **Select workspace:** Choose the workspace containing the discovered databases
5. **Click:** "Submit"
6. **Copy the API key** (starts with `secret_`)

### Share Databases with New Integration

1. Open each of the 14 database URLs
2. Click **"..."** → **"Connections"**
3. Select **"Homo Lumen Personal Data"** (your new integration)
4. Confirm

### Add Second API Key to Project

After creating the new integration:

1. Add to your environment variables:
   ```bash
   # In your .env or environment
   NOTION_PERSONAL_API_KEY=secret_YOUR_NEW_KEY_HERE
   ```

2. Update GitHub secrets (if using GitHub Actions):
   - Go to your repository settings
   - Secrets and variables → Actions
   - Add new secret: `NOTION_PERSONAL_API_KEY`

---

## Step 3: Verify Access

After granting access (via Option A or B), verify it worked:

### Run Check Script

```bash
# If using Option A (same integration)
python check_discovered_databases.py

# If using Option B (new integration)
# First, update the script to use the new API key for these databases
# Then run:
python check_discovered_databases.py
```

### Expected Output

If successful, you should see:

```
Checking discovered Notion databases...

================================================================================
DATABASE: Spektral Dimensjoner
================================================================================
ID: 1d48fec9293180929092f2553a9f85aa
Title: Spektral Dimensjoner
Description: [Database description if any]

Properties:
  - Name: title
  - [Other properties...]

[Repeat for all 14 databases]

================================================================================
Successfully retrieved 14/14 database schemas
================================================================================

Schemas saved to: discovered_database_schemas.json
```

---

## Troubleshooting

### "Integration not found in Connections menu"

**Cause:** Integration doesn't have access to the workspace containing the database.

**Solution:**
1. Verify which workspace the database is in (check workspace name in Notion sidebar)
2. Go to https://www.notion.so/my-integrations
3. Edit your integration
4. Make sure it's in the same workspace as the database

### "Still getting 401 Unauthorized"

**Cause:** Access not properly granted or wrong API key.

**Solution:**
1. Double-check you clicked "Confirm" after adding the connection
2. Refresh the Notion page and verify the integration appears in Connections
3. Verify the API key in your environment matches the integration
4. Try Option B (create separate integration)

### "Database opens but I can't see the '...' menu"

**Cause:** Insufficient permissions in the workspace.

**Solution:**
1. Ask the workspace admin to grant you full access
2. Or ask the admin to share the databases with the integration themselves

### "Some databases work, others don't"

**Cause:** Databases are in different workspaces.

**Solution:**
- Use Option B to create a second integration for the different workspace
- Or migrate all databases to the same workspace

---

## Quick Reference: All 14 Database URLs

For easy access while granting connections:

1. [Spektral Dimensjoner](https://www.notion.so/Spektral-Dimensjoner-1d48fec9293180929092f2553a9f85aa)
2. [Phoenix-syklus](https://www.notion.so/Phoenix-syklus-1d48fec92931807b9e27c445b9840539)
3. [How we feel](https://www.notion.so/How-we-feel-1d48fec9293180b393c5c62a002280d0)
4. [Dagbok 2020 EchoLog](https://www.notion.so/Dagbok-2020-EchoLog-1db8fec9293180caa349fbe34ba1097e)
5. [Database 5](https://www.notion.so/1dd8fec9293180298d8bd2c5d5330563)
6. [Database 6](https://www.notion.so/1dd8fec92931808ebc38ce8fc988b1a0)
7. [Database 7](https://www.notion.so/1dd8fec929318061be62facd8439da53)
8. [Database 8](https://www.notion.so/1e68fec9293180ba9264dd5dafbf53b6)
9. [Database 9](https://www.notion.so/1e68fec929318052afe2fe6ee282108e)
10. [Database 10](https://www.notion.so/1e68fec929318069bd61e2a8f22221f7)
11. [Database 11](https://www.notion.so/28e8fec9293180cbaa57d99549147b97)
12. [Database 12](https://www.notion.so/28e8fec929318056a2dcc2bb28fd166d)
13. [Database 13](https://www.notion.so/8b18dd1769ab48a6a70ec38b74e5140f)
14. [Database 14](https://www.notion.so/2988fec9293180509658e93447b3b259)

---

## What to Do After Granting Access

Once access is verified and schemas are retrieved:

1. **Review schemas** in `discovered_database_schemas.json`
2. **Identify integration opportunities** (see DISCOVERED_DATABASES.md)
3. **Prioritize** which databases to integrate first
4. **Let Code know** which integrations you want, and I'll create the parsers

---

## Need Help?

- **Can't find integration:** Check https://www.notion.so/my-integrations
- **Can't access databases:** Verify workspace permissions
- **Databases in multiple workspaces:** Use Option B (multiple integrations)
- **Technical issues:** Run `python check_discovered_databases.py` and share the error

---

**Created:** 27. oktober 2025
**Author:** Code (Claude Code Agent)
**Related:** LAG 4 Mycelial Intelligence System
