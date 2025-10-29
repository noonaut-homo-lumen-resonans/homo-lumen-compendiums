# SMK Deduplication Package

**Version**: 1.0
**Date**: 2025-10-28
**Status**: ✅ READY TO USE

---

## Overview

This package provides tools to identify and remove duplicate entries from the SMK (Strategic Macro-Coordination) database in Notion.

**Problem**: SMK database has 100 entries, some of which are duplicates (same SMK Number, same title, etc.)

**Solution**: Automated scripts to analyze, deduplicate, and restore if needed.

---

## Files in This Package

### 1. `analyze_smk_duplicates.py`
**Purpose**: Analyze SMK database and identify all duplicates

**What it does**:
- Fetches all SMK entries from Notion
- Groups entries by SMK Number, Name, Commit SHA, Date+Agent
- Generates detailed report showing all duplicates
- Saves JSON report for reference

**Usage**:
```bash
python analyze_smk_duplicates.py
```

**Output**:
- Console report with statistics
- JSON file: `smk_duplicates_analysis_YYYYMMDD_HHMMSS.json`

**When to use**: Run this FIRST to see what duplicates exist

---

### 2. `deduplicate_smk.py`
**Purpose**: Remove duplicates from SMK database

**What it does**:
- Analyzes duplicates (same as analyze script)
- Automatically or manually chooses which entry to keep
- Creates backup before making changes
- Archives (soft deletes) duplicate entries
- Logs all changes

**Usage**:

**Dry run** (see what would happen, no changes):
```bash
python deduplicate_smk.py --dry-run --auto
```

**Automatic mode** (keeps "best" entry based on scoring):
```bash
python deduplicate_smk.py --auto
```

**Manual mode** (you choose which to keep):
```bash
python deduplicate_smk.py --manual
```

**Output**:
- Backup file: `smk_backup_YYYYMMDD_HHMMSS.json`
- Log file: `smk_deduplication_log_YYYYMMDD_HHMMSS.json`

**When to use**: After reviewing analyze output, use this to actually remove duplicates

---

### 3. `restore_smk_from_backup.py`
**Purpose**: Restore archived entries if something went wrong

**What it does**:
- Reads backup file
- Finds entries that were archived
- Unarchives them (restores to database)
- Verifies restoration

**Usage**:
```bash
python restore_smk_from_backup.py smk_backup_20251028_120000.json
```

**With log file** (more precise):
```bash
python restore_smk_from_backup.py smk_backup_20251028_120000.json --log smk_deduplication_log_20251028_120005.json
```

**Output**:
- Restore log: `smk_restore_log_YYYYMMDD_HHMMSS.json`

**When to use**: Only if you need to rollback the deduplication

---

## How the Scripts Work

### Duplicate Detection Logic

**Primary Key**: `SMK Number`
- If two entries have the same SMK Number, they are duplicates
- Example: Two entries both with "SMK #27" are duplicates

**Secondary checks**:
- Same Name (title)
- Same Commit SHA
- Same Date + Agent

### Scoring System (Auto Mode)

When `deduplicate_smk.py --auto` runs, it scores each entry to determine which is "best":

**Scoring criteria**:
1. **Filled fields** (40 points max): More complete entries score higher
2. **Relations** (30 points max): Entries with more links to other databases score higher
3. **Recency** (20 points max): Recently edited entries score higher
4. **Status** (10 points max):
   - COMPLETE: +10 points
   - IN_PROGRESS: +5 points
   - PLANNED: +0 points

**Example**:
```
Entry A: 85 points (7/8 fields, 3 relations, edited yesterday, COMPLETE)
Entry B: 45 points (4/8 fields, 0 relations, edited 2 weeks ago, IN_PROGRESS)
→ Entry A is kept, Entry B is archived
```

---

## Quick Start Guide

### Step 1: Analyze
```bash
cd "C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums"
set NOTION_API_KEY=your_api_key_here
python analyze_smk_duplicates.py
```

**Read the output carefully!**

---

### Step 2: Dry Run
```bash
python deduplicate_smk.py --dry-run --auto
```

**Check what would be deleted**. If it looks good, proceed. If not, use `--manual` mode.

---

### Step 3: Deduplicate
**Automatic**:
```bash
python deduplicate_smk.py --auto
```

**OR Manual** (recommended first time):
```bash
python deduplicate_smk.py --manual
```

The script will:
1. Create backup
2. Show you what will be archived
3. Ask for confirmation
4. Archive duplicates
5. Create log

---

### Step 4: Verify
```bash
python analyze_smk_duplicates.py
```

Expected output:
```
✅ NO DUPLICATES FOUND!
   SMK database is clean.
```

---

## Safety Features

### 1. Backup
Every deduplication creates a full backup of all SMK entries:
- File: `smk_backup_YYYYMMDD_HHMMSS.json`
- Contains: All entries with full data
- Keep this file until you're sure deduplication was correct

### 2. Logging
All changes are logged:
- File: `smk_deduplication_log_YYYYMMDD_HHMMSS.json`
- Contains:
  - Which entries were kept
  - Which entries were archived
  - Why each decision was made

### 3. Soft Delete
Entries are **archived**, not permanently deleted:
- They're removed from database views
- But still exist in Notion
- Can be unarchived easily

### 4. Rollback
If anything goes wrong:
```bash
python restore_smk_from_backup.py smk_backup_20251028_120000.json
```

---

## Troubleshooting

### Problem: "NOTION_API_KEY not found"
**Solution**:
```bash
set NOTION_API_KEY=your_notion_api_key_here
```

Get your API key from: https://www.notion.so/my-integrations

---

### Problem: Script finds no duplicates, but I see them
**Diagnosis**: Duplicates might not have same SMK Number

**Solution**: Check the entries manually - if they have different SMK Numbers, they're not counted as duplicates

---

### Problem: Automatic mode would delete the wrong entry
**Solution**: Use manual mode instead:
```bash
python deduplicate_smk.py --manual
```

---

### Problem: I want to test more before deleting
**Solution**: Use `--dry-run` as many times as you want:
```bash
python deduplicate_smk.py --dry-run --auto
```

No changes are made in dry-run mode.

---

### Problem: Script is slow
**Diagnosis**: Fetching 100 entries takes time

**Solution**: This is normal. Wait for it to complete (usually 30-60 seconds).

---

### Problem: I accidentally deleted the wrong entries
**Solution**: Restore from backup:
```bash
python restore_smk_from_backup.py smk_backup_YYYYMMDD_HHMMSS.json
```

---

## Integration with Phase 1

This deduplication is **Step 1.3** in the Phase 1 implementation guide ([FASE_1_MANUELL_IMPLEMENTERING.md](FASE_1_MANUELL_IMPLEMENTERING.md)).

**Phase 1 Steps**:
1. DEL 1.1: Delete duplicate EM database
2. DEL 1.2: Delete duplicate SLL database
3. **DEL 1.3: Remove duplicates in SMK database** ← THIS PACKAGE
4. DEL 2: Add 8 relations to ARF
5. DEL 3: Add 7 relations to LK
6. DEL 4: Set up EM database
7. DEL 5: Create test entries

---

## Verification

After deduplication, run the Phase 1 verification script:

```bash
python verify_phase1_implementation.py
```

It will check:
- ✅ Duplicate databases are deleted
- ✅ **SMK has no duplicates** ← Will verify this
- ✅ ARF has correct relations
- ✅ LK has correct relations
- ✅ EM is set up correctly

---

## Technical Details

### Database Structure

**SMK Properties**:
- Name (title) - SMK decision title
- SMK Number (number) - Sequential number (1, 2, 3, ...)
- Agent (select) - Responsible agent
- Date (date) - Decision date
- Status (select) - COMPLETE, IN_PROGRESS, PLANNED
- Tags (multi_select) - deployment, vercel, etc.
- GitHub URL (url) - Link to commit/PR
- Commit SHA (rich_text) - Git commit hash
- 3 relation properties (to Critical Decisions, Shadow Logs, Case Studies)

### How Archiving Works

In Notion API:
- `pages.update(page_id, archived=True)` → Archives the page
- `pages.update(page_id, archived=False)` → Unarchives the page

Archived pages:
- Don't appear in database views
- Still exist in Notion
- Can be found in "..." menu → "Show archived pages"
- Can be unarchived manually or via API

---

## Support

If you encounter issues:

1. **Check the logs**: `smk_deduplication_log_*.json`
2. **Review the backup**: `smk_backup_*.json`
3. **Run analyze again**: `python analyze_smk_duplicates.py`
4. **Check this README**: Look for your issue in Troubleshooting

---

## Version History

**v1.0** (2025-10-28)
- Initial release
- 3 scripts: analyze, deduplicate, restore
- Auto and manual modes
- Dry-run support
- Full backup and logging
- Integration with Phase 1

---

**🧬 Part of Michael Levin Framework Implementation**

This package helps maintain data quality in the Notion database ecosystem by ensuring each SMK entry is unique, supporting the emergent intelligence patterns we're building.

---

*Generated: 2025-10-28*
*Status: ✅ READY TO USE*
