# HANDOFF TO CODE: SMK YAML CONVERSION & SYNC WORKFLOW

**Date:** 26. oktober 2025  
**From:** Manus (Infrastructure Agent)  
**To:** Claude Code (Kode-Utfører / Resonanskammer-Implementør)  
**Priority:** HIGH  
**Estimated Time:** 2-3 hours  
**Status:** 90% Complete - Needs Finishing Touches

---

## 🎯 MISSION OVERVIEW

Complete the SMK (Statisk Meta-Kompendium) YAML frontmatter conversion and implement GitHub Actions workflow for automatic Notion sync.

**Context:** We have successfully implemented LP (Learning Points) sync to Notion SLL. Now we need to do the same for SMKs.

---

## ✅ WHAT MANUS COMPLETED TODAY

### 1. **LP → Notion SLL Sync** (100% COMPLETE)
- ✅ GitHub Actions workflow operational
- ✅ LP #050 and LP #051 verified in SLL
- ✅ Automatic sync on every commit with "LP #XXX" format

### 2. **SMK Conversion Script** (90% COMPLETE)
- ✅ Python script created: `/home/ubuntu/convert_smks_to_yaml.py`
- ✅ Successfully converts 12 SMK files
- ⚠️ **PROBLEM:** Date-based SMKs get wrong numbering (all become SMK_2025.md)
- ⚠️ **PROBLEM:** Many SMKs missing dates
- ⚠️ **PROBLEM:** Some SMKs missing agent names

### 3. **Documentation** (100% COMPLETE)
- ✅ NOTION_GITHUB_WORKFLOW_ANALYSIS.md (12,000+ words)
- ✅ ARF_REFLECTION_TEMPLATE.md (4,000+ words)
- ✅ COMPLETE_AUTOMATION_ROADMAP_V1.0.md (15,000+ words)

---

## 🚨 YOUR MISSION (3 TASKS)

### **TASK 1: Fix SMK Conversion Script** (30 minutes)

**Location:** `/home/ubuntu/convert_smks_to_yaml.py`

**Problems to Fix:**

#### Problem 1: Wrong Numbering for Date-Based SMKs
**Current behavior:**
```
SMK_2025_10_20_QDA_DEPLOYMENT_VALIDATION.md → SMK_2025.md
SMK_2025_10_21_VERCEL_DEPLOYMENT_SUCCESS.md → SMK_2025.md (CONFLICT!)
SMK_2025_10_22_HOMO_AI_LUMEN_RESONANS_MANIFESTATION.md → SMK_2025.md (CONFLICT!)
```

**Expected behavior:**
```
SMK_2025_10_20_QDA_DEPLOYMENT_VALIDATION.md → SMK_033.md
SMK_2025_10_21_VERCEL_DEPLOYMENT_SUCCESS.md → SMK_029.md (or 034)
SMK_2025_10_22_HOMO_AI_LUMEN_RESONANS_MANIFESTATION.md → SMK_035.md
```

**Fix:** Update `extract_smk_number()` function:
```python
def extract_smk_number(filename):
    """Extract SMK number from filename."""
    # Try SMK#XXX format
    match = re.search(r'SMK#(\d+)', filename)
    if match:
        return int(match.group(1))
    
    # Try SMK_XXX format
    match = re.search(r'SMK_(\d+)', filename)
    if match:
        return int(match.group(1))
    
    # Try date format - MAP TO CORRECT SMK NUMBERS
    match = re.search(r'SMK_2025_10_(\d{2})', filename)
    if match:
        day = int(match.group(1))
        # CORRECT MAPPING:
        date_map = {
            "20": 33,  # QDA Deployment
            "21": 29,  # Vercel Deployment (check if #029 exists!)
            "22": 35   # Homo/AI Lumen Resonans
        }
        return date_map.get(str(day), None)
    
    return None
```

**Note:** Check if SMK #029 already exists! If it does, use 034 instead.

#### Problem 2: Missing Dates
**Current:** Many SMKs have `Date: ` (empty)

**Fix:** Manually add dates by reading file content or using file modification date:
```python
# If no date found in content, use file modification time
if not metadata["date"]:
    file_mtime = filepath.stat().st_mtime
    metadata["date"] = datetime.fromtimestamp(file_mtime).strftime("%Y-%m-%d")
```

#### Problem 3: Missing Agent Names
**Current:** Some SMKs have `Agent: ` (empty)

**Fix:** Improve agent extraction regex:
```python
# Extract agent - try multiple patterns
agent_match = re.search(r'\*\*Agent:\*\*\s+(.+?)(?:\(|\\n|$)', content)
if not agent_match:
    agent_match = re.search(r'agent:\s+(.+?)$', content, re.MULTILINE)
if not agent_match:
    # Try to find agent in first 500 chars
    agent_match = re.search(r'(Orion|Lira|Nyra|Thalus|Zara|Abacus|Manus|Aurora|Code|Falcon)', content[:500])
if agent_match:
    metadata["agent"] = agent_match.group(1).strip()
    # Clean up
    metadata["agent"] = re.sub(r'🔨|⬢|🌟|\(.*?\)', '', metadata["agent"]).strip()
else:
    metadata["agent"] = "Unknown"
```

---

### **TASK 2: Run Fixed Conversion Script** (5 minutes)

**Steps:**
1. Fix the script (see Task 1)
2. Run: `python3 /home/ubuntu/convert_smks_to_yaml.py`
3. Review output carefully
4. Type "yes" to confirm conversion
5. Verify all 12 SMKs are correctly named:
   ```
   SMK_019.md
   SMK_020.md
   SMK_021.md
   SMK_022.md
   SMK_023.md
   SMK_027.md
   SMK_028.md
   SMK_029.md (or 034 if 029 exists)
   SMK_030.md
   SMK_032.md
   SMK_033.md
   SMK_035.md
   ```

**Verification:**
```bash
cd /home/ubuntu/homo-lumen-compendiums/SMK
ls -lh SMK_*.md | wc -l  # Should be 12
head -20 SMK_033.md  # Check YAML frontmatter
```

---

### **TASK 3: Create SMK Sync GitHub Actions Workflow** (1-2 hours)

**Goal:** Automatically sync SMK files to Notion when they're created/updated

**Location:** `/home/ubuntu/homo-lumen-compendiums/.github/workflows/sync-smks-to-notion.yml`

**Template:**
```yaml
name: Sync SMKs to Notion

on:
  push:
    branches:
      - main
    paths:
      - 'SMK/SMK_*.md'

jobs:
  sync-smks:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install requests pyyaml
      
      - name: Detect changed SMKs
        id: detect-smks
        run: |
          # Get list of changed SMK files
          CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | grep '^SMK/SMK_.*\.md$' || true)
          echo "changed_files<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGED_FILES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
      
      - name: Sync SMKs to Notion
        if: steps.detect-smks.outputs.changed_files != ''
        env:
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          NOTION_SMK_DATABASE_ID: ${{ secrets.NOTION_SMK_DATABASE_ID }}
        run: |
          python3 .github/scripts/sync_smks_to_notion.py "${{ steps.detect-smks.outputs.changed_files }}"
      
      - name: Report success
        run: |
          echo "✅ SMK sync complete!"
```

**Create Script:** `.github/scripts/sync_smks_to_notion.py`

```python
#!/usr/bin/env python3
"""
Sync SMK files to Notion database.

This script:
1. Reads changed SMK files
2. Parses YAML frontmatter
3. Creates/updates Notion pages in SMK Archive database
"""

import os
import sys
import re
import yaml
import requests
from datetime import datetime

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
SMK_DATABASE_ID = os.environ.get("NOTION_SMK_DATABASE_ID")
NOTION_VERSION = "2022-06-28"

def parse_smk_file(filepath):
    """Parse SMK file and extract YAML frontmatter + content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    if content.startswith('---'):
        end_match = re.search(r'\n---\n', content[3:])
        if end_match:
            yaml_str = content[3:3 + end_match.start()]
            body = content[3 + end_match.end():]
            metadata = yaml.safe_load(yaml_str)
            return metadata, body
    
    return None, None

def create_notion_page(metadata, body, smk_number):
    """Create Notion page in SMK Archive database."""
    
    # Prepare properties
    properties = {
        "SMK_ID": {
            "title": [
                {
                    "text": {
                        "content": f"SMK #{smk_number:03d}"
                    }
                }
            ]
        },
        "Title": {
            "rich_text": [
                {
                    "text": {
                        "content": metadata.get("title", "Untitled")[:2000]
                    }
                }
            ]
        },
        "Agent": {
            "select": {
                "name": metadata.get("agent", "Unknown")
            }
        },
        "Date": {
            "date": {
                "start": metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
            }
        },
        "Type": {
            "select": {
                "name": metadata.get("type", "Strategic Macro-Coordination")
            }
        },
        "Status": {
            "select": {
                "name": metadata.get("status", "COMPLETE")
            }
        },
        "Tags": {
            "multi_select": [
                {"name": tag} for tag in metadata.get("tags", [])
            ]
        }
    }
    
    # Prepare content blocks (simplified - Notion API has limits)
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": body[:2000]  # Notion has limits
                        }
                    }
                ]
            }
        }
    ]
    
    # Create page
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }
    
    data = {
        "parent": {"database_id": SMK_DATABASE_ID},
        "properties": properties,
        "children": children
    }
    
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        print(f"✅ Created SMK #{smk_number:03d} in Notion")
        return response.json()
    else:
        print(f"❌ Failed to create SMK #{smk_number:03d}: {response.text}")
        return None

def main():
    """Main sync function."""
    if len(sys.argv) < 2:
        print("No changed SMK files detected")
        return
    
    changed_files = sys.argv[1].strip().split('\n')
    
    for filepath in changed_files:
        if not filepath:
            continue
        
        print(f"\n📄 Processing: {filepath}")
        
        # Extract SMK number
        match = re.search(r'SMK_(\d+)\.md', filepath)
        if not match:
            print(f"  ⚠️  Could not extract SMK number, skipping")
            continue
        
        smk_number = int(match.group(1))
        
        # Parse file
        metadata, body = parse_smk_file(filepath)
        if not metadata:
            print(f"  ⚠️  Could not parse YAML frontmatter, skipping")
            continue
        
        # Create Notion page
        create_notion_page(metadata, body, smk_number)
    
    print("\n✅ SMK sync complete!")

if __name__ == "__main__":
    main()
```

**Make executable:**
```bash
chmod +x .github/scripts/sync_smks_to_notion.py
```

---

## 🔧 NOTION SETUP REQUIRED

### Create SMK Archive Database in Notion

**Steps:**
1. Go to HOMO LUMEN CENTRAL HUB in Notion
2. Create new database: "SMK - Strategic Macro-Coordination Archive"
3. Add properties:
   - **SMK_ID** (title) - e.g., "SMK #019"
   - **Title** (rich text) - Full title
   - **Agent** (select) - Orion, Lira, Nyra, Thalus, Zara, Abacus, Manus, Aurora, Code, Falcon
   - **Date** (date)
   - **Type** (select) - Strategic Macro-Coordination
   - **Status** (select) - COMPLETE, IN_PROGRESS
   - **Tags** (multi-select) - constitution, mcp, nav-losen, ubuntu-playground, etc.
   - **Source** (url) - Link to GitHub file

4. Share database with "Homo Lumen MCP Automation" integration

5. Copy database ID from URL:
   ```
   https://www.notion.so/XXXXXXXXX?v=YYYYYYYY
                        ^^^^^^^^^ <- This is the database ID
   ```

6. Add to GitHub Secrets:
   - Name: `NOTION_SMK_DATABASE_ID`
   - Value: [database ID from step 5]

---

## 📊 VERIFICATION CHECKLIST

After completing all tasks:

- [ ] All 12 SMKs converted to YAML frontmatter format
- [ ] All SMKs have correct numbering (no conflicts)
- [ ] All SMKs have dates (no empty dates)
- [ ] All SMKs have agent names (no "Unknown" unless truly unknown)
- [ ] SMK Archive database created in Notion
- [ ] Database shared with Homo Lumen MCP Automation integration
- [ ] NOTION_SMK_DATABASE_ID added to GitHub Secrets
- [ ] GitHub Actions workflow created
- [ ] Workflow tested with a commit
- [ ] At least 1 SMK appears in Notion database

---

## 🚀 TESTING PROCEDURE

### Test 1: Manual Conversion Test
```bash
cd /home/ubuntu
python3 convert_smks_to_yaml.py
# Review output
# Type "yes" to confirm
cd /home/ubuntu/homo-lumen-compendiums/SMK
ls -lh SMK_*.md
head -30 SMK_033.md  # Verify YAML frontmatter
```

### Test 2: GitHub Actions Test
```bash
cd /home/ubuntu/homo-lumen-compendiums
git add SMK/SMK_*.md
git add .github/workflows/sync-smks-to-notion.yml
git add .github/scripts/sync_smks_to_notion.py
git commit -m "LP #052: SMK YAML Conversion & Sync Workflow Complete

Converted all 12 SMKs to YAML frontmatter format.
Implemented GitHub Actions workflow for automatic Notion sync.

Agent: Code
Category: Technical
Tags: SMK, Notion, GitHub-Actions, Automation"
git push
```

Then check:
1. GitHub Actions: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/actions
2. Notion SMK Archive database for new entries

---

## 📚 REFERENCE DOCUMENTS

**Already created by Manus:**
- `NOTION_GITHUB_WORKFLOW_ANALYSIS.md` - Complete workflow analysis
- `COMPLETE_AUTOMATION_ROADMAP_V1.0.md` - 4-week implementation plan
- `ARF_REFLECTION_TEMPLATE.md` - Agent reflection template
- `MCP_78_TOOLS_DETAILED_REPORT.md` - All MCP tools documented

**GitHub Actions examples:**
- `.github/workflows/sync-to-notion.yml` - LP sync workflow (working!)
- `.github/scripts/parse_commit.py` - Commit parser
- `.github/scripts/sync_to_notion.py` - Notion sync script

---

## 🎯 SUCCESS CRITERIA

**You will know you're done when:**
1. ✅ All 12 SMKs have YAML frontmatter
2. ✅ All SMKs are correctly numbered (no conflicts)
3. ✅ GitHub Actions workflow runs successfully
4. ✅ At least 1 SMK appears in Notion SMK Archive
5. ✅ Everything is committed to GitHub

---

## 🆘 IF YOU GET STUCK

**Common Issues:**

### Issue 1: Notion API 400 Error
**Cause:** Invalid property format
**Fix:** Check that all select/multi-select options exist in database

### Issue 2: GitHub Actions Fails
**Cause:** Missing secrets or wrong database ID
**Fix:** Verify secrets in GitHub Settings → Secrets → Actions

### Issue 3: SMK Numbering Conflicts
**Cause:** Multiple SMKs trying to use same number
**Fix:** Manually assign unique numbers in `extract_smk_number()` function

---

## 💬 QUESTIONS FOR OSVALD

Before starting, confirm with Osvald:

1. **SMK #029:** Does it exist somewhere? If yes, use 034 for SMK_2025_10_21
2. **Missing SMKs (#024-026, #031):** Should we search for them in Google Drive/Notion first?
3. **Priority:** Should we complete SMK sync before searching for missing SMKs?

---

## 🎉 FINAL NOTES

**From Manus:**

Code, this is a critical piece of our mycelial intelligence infrastructure. SMKs are our collective strategic memory - they document major decisions, architectural shifts, and constitutional moments.

Getting this right means:
- All agents can search SMKs in Notion
- Historical context is preserved
- Future SMKs are automatically synced
- We have a complete audit trail

Take your time, test thoroughly, and don't hesitate to ask Osvald for clarification.

**You've got this!** 🔨→🛠️

---

**Handoff Complete**  
**Date:** 26. oktober 2025, 11:30 CET  
**From:** Manus (9+ hours of work today!)  
**To:** Code (fresh start!)  
**Status:** Ready for execution

🕸️ *The mycelium grows stronger with each connection.* 🍄✨

