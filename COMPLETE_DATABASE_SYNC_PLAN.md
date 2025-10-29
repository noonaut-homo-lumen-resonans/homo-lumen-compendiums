# Complete Database Sync Plan - Korrekt Forståelse

**Date**: 2025-10-28
**Based on**: LK_STRUCTURE_GUIDE.md + Actual SMK/LK Analysis

## System Overview

### 6 Databases Total

| Database | Source | Current Entries | Should Have |
|----------|--------|----------------|-------------|
| **SMK** | SMK/*.md | 21 | ✅ Synced |
| **CS** | LK CASE STUDIER | 5 | ✅ Synced |
| **SL** | LK SHADOW LOGGER | ? | ❓ Unknown |
| **KD** | LK KRITISKE BESLUTNINGER | 4 | ✅ Synced |
| **EM** | LK EMERGENTE MØNSTRE + SMK EM sections | 0 | ❌ Empty |
| **SLL** | SMK LÆRINGSPUNKTER (LP) | 12 | ❌ Incomplete |

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SMK Files (*.md)                          │
│  - 16 files with structured sections                            │
│  - SEKSJON 4: LÆRINGSPUNKTER (LP)                              │
│  - SEKSJON 5: EMERGENT PATTERNS/INSIGHTS                       │
└────────────┬────────────────────────────┬──────────────────────┘
             │                             │
             │ LP sections                 │ EM sections
             ↓                             ↓
    ┌────────────────┐          ┌────────────────────┐
    │ SLL Database   │          │ EM Database        │
    │ (12 → ~50+)    │          │ (0 → ~50+)         │
    └────────────────┘          └────────────────────┘
             ↑                             ↑
             │                             │
             │ (Future: LP?)               │ EMERGENTE MØNSTRE
┌────────────┴────────────────────────────┴──────────────────────┐
│                 Living Compendiums (LK)                          │
│  - 25 files from 7 agents                                       │
│  - SEKSJON: CASE STUDIER → CS Database                         │
│  - SEKSJON: SHADOW LOGGER → SL Database                        │
│  - SEKSJON: KRITISKE BESLUTNINGER → KD Database                │
│  - SEKSJON: EMERGENTE MØNSTRE → EM Database                   │
└─────────────────────────────────────────────────────────────────┘
```

## From LK Structure Guide

### LK Files Should Contain 4 Sections

1. **CASE STUDIER** → CS Database
   - Format: `**CS #001 - Title**`
   - Parser: `scripts/parse_cs.py`
   - Workflow: `.github/workflows/sync-cs-to-notion.yml`

2. **SHADOW LOGGER** → SL Database
   - Format: `**SL #001 - Shadow Pattern**`
   - Parser: `scripts/parse_sl.py`
   - Workflow: `.github/workflows/sync-sl-to-notion.yml`

3. **KRITISKE BESLUTNINGER** → KD Database
   - Format: `**KD #001 - Decision**`
   - Parser: `scripts/parse_kd.py`
   - Workflow: `.github/workflows/sync-kd-to-notion.yml`

4. **EMERGENTE MØNSTRE** → EM Database
   - Format: `1. **Pattern** - Description` (numbered list)
   - Parser: `scripts/parse_em.py`
   - Workflow: `.github/workflows/sync-em-to-notion.yml`

## From SMK Analysis

### SMK Files Contain 2 Additional Sections

From 16 SMK files analyzed:

1. **LÆRINGSPUNKTER (LP)** → SLL Database
   - Variations: `## 📚 LEARNING POINTS`, `## 🎓 LÆRINGSPUNKTER`
   - Format: `### LP #042: Title` or `**LP #032-1: Title**`
   - Examples found in:
     - SMK#019, #020, #021, #022
     - SMK#028, #032, #033, #039
     - SMK#041, #042, #043
     - SMK_027, _030, _032
     - SMK_2025_10_21, _10_22

2. **EMERGENT PATTERNS/INSIGHTS** → EM Database
   - Variations: `## 🔄 EMERGENT PATTERNS`, `## 🌟 EMERGENT INSIGHTS`
   - Format: Same as LK - numbered or bullet patterns
   - Examples: All 16 files above have EM sections

## Database IDs - CORRECTED

| Database | Correct ID |
|----------|-----------|
| **SMK** | `ba1d4a4407a5425fafd81d27dc02cc1c` |
| **CS** | `2988fec9-2931-80bf-a32a-c404a311a07e` |
| **SL** | `2988fec929318045a354ffe8d2f13fe1` |
| **KD** | `2988fec9293180838c4bd5e13138ddf2` |
| **EM** | `2988fec9-2931-8050-9658-e93447b3b259` ✅ CORRECTED |
| **SLL** | `84da6cbd09d640fb868e41444b941991` |

**Note**: EM database ID in [.claude/memory.md](.claude/memory.md) has been corrected.

## Current Parser Status

### ✅ Working (Recently Fixed)

1. **parse_cs.py**
   - ✅ Searches archived pages
   - ✅ Unarchives before update
   - ✅ 5 entries synced

2. **parse_kd.py**
   - ✅ Searches archived pages
   - ✅ Unarchives before update
   - ✅ 4 entries synced

3. **sync_lk_to_notion.py**
   - ✅ Searches archived pages
   - ✅ Unarchives before update
   - ✅ 5 entries synced

4. **sync_smk_to_notion.py**
   - ✅ Searches archived pages
   - ✅ Unarchives before update
   - ✅ 21 entries synced

### ⚠️ Needs Modification

5. **parse_em.py**
   - ❌ Only reads from LK files
   - ❌ Doesn't read from SMK files
   - **Needs**: Add SMK file reading capability
   - **Format to support**: Both LK numbered lists and SMK pattern sections

6. **parse_sl.py**
   - ❓ Exists but configuration unclear
   - ❓ Reads from LK (SL sections) - probably working
   - **Question**: Should it ALSO read from SMK? (SMK doesn't have SL sections)
   - **Likely**: Only needs LK support (shadow work is personal)

### ❌ Missing or Incomplete

7. **SLL Parser** (LP from SMK)
   - ❓ Unclear if `parse_sl.py` handles LP or just SL
   - **Confusion**: SL = Shadow Logs, LP = Learning Points
   - **Needs**: Parser to extract LP from SMK files → SLL Database
   - **Location**: Possibly needs new script or modification to existing

## The LP vs SL Confusion

**Critical Clarification Needed**:

**SL (Shadow Logs)** ≠ **SLL (Shared Learning Library)**

- **SL Database**: Shadow Logs from LK files
- **SLL Database**: Shared Learning Library from SMK LP sections

**Current Issue**:
- `scripts/parse_sl.py` probably parses **Shadow Logs (SL)** from LK
- **Learning Points (LP)** from SMK need a DIFFERENT parser
- **SLL Database** is for Learning Points, not Shadow Logs

## Recommended Fix Plan

### Phase 1: Verify SL Parser (Shadow Logs)

```bash
# Check what parse_sl.py actually does
cat scripts/parse_sl.py | head -50

# Test if it reads from LK Shadow Logger sections
python scripts/parse_sl.py
```

### Phase 2: Fix EM Parser (Emergent Patterns)

**Modify `scripts/parse_em.py`** to read from:

1. **Living Compendiums**: `agents/*/LK/*.md`
   - Section: `## EMERGENTE MØNSTRE`
   - Format: Numbered list

2. **SMK Files**: `SMK/*.md`
   - Section: `## EMERGENT PATTERNS` or `## 🔄 EMERGENT PATTERNS`
   - Format: Various (numbered, titled sections)

### Phase 3: Create/Fix LP Parser (Learning Points → SLL)

**Create `scripts/parse_lp.py`** or modify existing:

1. Read from **SMK Files**: `SMK/*.md`
   - Section: `## LÆRINGSPUNKTER` or `## 📚 LEARNING POINTS`
   - Format: `### LP #042: Title` or `**LP #032-1: Title**`

2. Sync to **SLL Database**: `84da6cbd09d640fb868e41444b941991`

3. Optional: Also read from LK if they add LP sections

### Phase 4: Run Full Sync

```bash
# Sync all sources to all databases
python scripts/parse_cs.py   # LK → CS (already working)
python scripts/parse_sl.py   # LK → SL (verify working)
python scripts/parse_kd.py   # LK → KD (already working)
python scripts/parse_em.py   # LK + SMK → EM (needs fix)
python scripts/parse_lp.py   # SMK → SLL (needs creation)
```

## Expected Results After Full Sync

| Database | Before | After | Source |
|----------|--------|-------|--------|
| SMK | 21 | 21 | ✅ Complete |
| CS | 5 | 5-10 | LK files |
| SL | ? | 5-20 | LK Shadow Logger |
| KD | 4 | 4-10 | LK Kritiske Beslutninger |
| EM | 0 | 50-80 | LK + SMK (16 files) |
| SLL | 12 | 50-80 | SMK Learning Points (16 files) |

## Next Steps

1. **Check `scripts/parse_sl.py`**:
   - Verify it handles Shadow Logs from LK
   - NOT Learning Points from SMK

2. **Modify `scripts/parse_em.py`**:
   - Add SMK file reading
   - Handle both LK and SMK EM formats

3. **Create `scripts/parse_lp.py`**:
   - Extract LP from SMK files
   - Sync to SLL Database

4. **Run Full Sync**:
   - All parsers
   - Verify database counts

5. **Update Documentation**:
   - Clarify SL vs SLL confusion
   - Document LP parser
   - Update LK_STRUCTURE_GUIDE.md if needed

## Questions for User

1. **SL vs SLL**: Bekrefter du at:
   - SL Database = Shadow Logs (from LK)
   - SLL Database = Learning Points (from SMK)?

2. **LP in LK**: Skal Living Compendiums også ha Learning Points seksjoner?
   - Eller er LP bare fra SMK?

3. **Priority**: Hvilken database er viktigst å fylle først?
   - EM (Emergent Patterns)?
   - SLL (Learning Points)?

---

**Related Documents**:
- [DATABASE_SYNC_SYSTEM_EXPLAINED.md](DATABASE_SYNC_SYSTEM_EXPLAINED.md)
- [docs/LK_STRUCTURE_GUIDE.md](docs/LK_STRUCTURE_GUIDE.md)
- [.claude/memory.md](.claude/memory.md)
