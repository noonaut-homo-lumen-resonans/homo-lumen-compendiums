# GitHub Secrets Setup Guide

## Problem: CS #004 Not Appearing in Notion

**Diagnosis:** GitHub Actions workflow likely ran but **failed due to missing secrets**.

---

## Required Secrets (5 total)

You need to add these secrets to your GitHub repository:

| Secret Name | Value |
|-------------|-------|
| `NOTION_API_KEY` | Your Notion API key (starts with `ntn_` or `secret_`) |
| `CS_DATABASE_ID` | `2988fec9-2931-803a-8703-000bb973304e` |
| `SL_DATABASE_ID` | `2988fec929318045a354ffe8d2f13fe1` |
| `KD_DATABASE_ID` | `2988fec9293180838c4bd5e13138ddf2` |
| `EM_DATABASE_ID` | `2988fec9-2931-80f4-8961-000b8710e0a5` |

---

## How to Add Secrets (Step-by-Step)

### Step 1: Go to Repository Settings
1. Open: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums
2. Click **"Settings"** (tab at top)
3. In left sidebar, scroll to **"Secrets and variables"**
4. Click **"Actions"**

### Step 2: Add NOTION_API_KEY
1. Click **"New repository secret"**
2. Name: `NOTION_API_KEY`
3. Value: Your Notion API key
   - Get it from "Homo Lumen MCP Automation" integration
   - Or get it from: https://www.notion.so/my-integrations
4. Click **"Add secret"**

### Step 3: Add CS_DATABASE_ID
1. Click **"New repository secret"**
2. Name: `CS_DATABASE_ID`
3. Value: `2988fec9-2931-803a-8703-000bb973304e`
4. Click **"Add secret"**

### Step 4: Add SL_DATABASE_ID
1. Click **"New repository secret"**
2. Name: `SL_DATABASE_ID`
3. Value: `2988fec929318045a354ffe8d2f13fe1`
4. Click **"Add secret"**

### Step 5: Add KD_DATABASE_ID
1. Click **"New repository secret"**
2. Name: `KD_DATABASE_ID`
3. Value: `2988fec9293180838c4bd5e13138ddf2`
4. Click **"Add secret"**

### Step 6: Add EM_DATABASE_ID
1. Click **"New repository secret"**
2. Name: `EM_DATABASE_ID`
3. Value: `2988fec9-2931-80f4-8961-000b8710e0a5`
4. Click **"Add secret"**

---

## Step 7: Verify Secrets Were Added

After adding all 5 secrets, you should see:

```
NOTION_API_KEY         Updated now
CS_DATABASE_ID         Updated now
SL_DATABASE_ID         Updated now
KD_DATABASE_ID         Updated now
EM_DATABASE_ID         Updated now
```

---

## Step 8: Manually Trigger Workflow

Since the workflow already ran (and likely failed), you need to trigger it again:

### Option A: Re-run Failed Workflow
1. Go to: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/actions
2. Look for **"Sync Case Studies to Notion"** workflow
3. Click on the most recent run (probably has a red ❌)
4. Click **"Re-run all jobs"**
5. Wait for it to complete (should turn green ✅)

### Option B: Manual Trigger
1. Go to: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/actions
2. Click **"Sync Case Studies to Notion"** in left sidebar
3. Click **"Run workflow"** (button on right)
4. Select branch: **main**
5. Click green **"Run workflow"** button
6. Wait for it to complete

### Option C: Push Small Change (Easiest)
Make a tiny change to the LK file and push:

```bash
# Add a space or newline somewhere in the file
git add agents/claude-code/LK/CODE_LIVING_COMPENDIUM_V1.4.md
git commit -m "test: Trigger CS sync workflow"
git push
```

This will automatically trigger all 4 workflows.

---

## Step 9: Verify CS #004 Appears in Notion

1. Open Notion
2. Go to CS Database: https://www.notion.so/2988fec9293180a8703000bb973304e
3. Look for entry: **"CS #004 - 17-Database Ecosystem Discovery..."**
4. If it appears → ✅ SUCCESS!

---

## Troubleshooting

### Workflow Still Fails After Adding Secrets
**Check workflow logs:**
1. Go to: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/actions
2. Click on the failed workflow run
3. Click **"sync-cs"** job
4. Expand **"Sync CS to Notion"** step
5. Read error message

**Common errors:**
- `401 Unauthorized` → Wrong NOTION_API_KEY
- `404 Not Found` → Wrong CS_DATABASE_ID
- `400 Bad Request` → Database not shared with integration

### Database Not Shared with Integration
If you get `400 Bad Request`:
1. Open CS Database in Notion
2. Click **"..."** menu (top right)
3. Click **"Connections"**
4. Add **"Homo Lumen MCP Automation"** integration
5. Re-run workflow

### Still Not Working?
**Test parser locally:**
```bash
# Set environment variables
$env:NOTION_API_KEY = "your-notion-api-key-here"
$env:CS_DATABASE_ID = "2988fec9-2931-803a-8703-000bb973304e"

# Run parser
python scripts/parse_cs.py
```

If this works locally but fails in GitHub Actions → secrets not configured correctly in GitHub.

---

## Quick Verification Checklist

- [ ] All 5 secrets added to GitHub repository
- [ ] Workflow re-run (manually or via push)
- [ ] Workflow shows green ✅ (not red ❌)
- [ ] CS #004 visible in Notion CS Database
- [ ] Same test for SL/KD/EM workflows

---

## Next Steps After Verification

Once CS #004 appears in Notion:
1. ✅ **Week 1 complete** - Data flow activated!
2. Add more CS/SL/KD/EM entries to agent LKs
3. Start Week 2: SLL enrichment (Visual_Essence + Archetype_Tags)
4. Nyra can begin 3D data integration design

---

**Created:** 27. oktober 2025
**For:** Osvald
**Purpose:** Enable GitHub Actions → Notion sync
**Status:** Awaiting secret configuration
