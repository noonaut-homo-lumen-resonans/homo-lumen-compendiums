# LP Manual Entry Guide - SMK #048 & #049

This guide provides structured data for manually entering 12 Learning Particles (LPs) into the SLL (Strategic Learning Library) Notion database.

**IMPORTANT:** Property names below match your exact Notion database schema.

## Summary
- **SMK #048**: 5 LPs (Redis Event Streaming)
- **SMK #049**: 7 LPs (Test Tasks + SMK V2.0)
- **Total**: 12 LPs
- **Category**: Technical
- **Half-life**: 60 days
- **Created**: Oct 28-29, 2025

---

## How to Use This Guide

For each LP below:
1. Create new entry in SLL database (click "+ New")
2. Fill in **Name** field (the title)
3. Copy-paste values from sections below into corresponding Notion properties
4. **Agent** = "Code" for all entries
5. After all 12 LPs are entered, run `compute_temporal_weights.py`

---

## SMK #048 Series (5 LPs)

### LP-048A: Upstash REST API RPUSH/LPOP Pattern

**Notion Properties:**
```
Name (Title): Upstash REST API RPUSH/LPOP Pattern

LP_ID: LP-2025-10-28-048A

Agent: Code

Category: Technical

Content: Use RPUSH (persistent queue) instead of PUBLISH (ephemeral) for reliable message delivery with Upstash Cloud REST API. Context: Redis event streaming between CSN Server and Ubuntu Playground using Upstash Cloud REST API.

Date: 2025-10-28

Source: CODE-SMK-2025-10-28-048

Tags: Redis, Upstash, Message Queue, RPUSH, LPOP

half_life_days: 60

related_ve: VE-048
```

---

### LP-048B: Python Windows Emoji Handling

**Notion Properties:**
```
Name (Title): Python Windows Emoji Handling

LP_ID: LP-2025-10-28-048B

Agent: Code

Category: Technical

Content: Replace all emoji characters (✅❌📥🚀) with ASCII text ([PASS], [FAIL], etc.) to prevent UnicodeEncodeError on Windows cp1252. Context: Windows cp1252 encoding crashes when printing emojis in Python console output.

Date: 2025-10-28

Source: CODE-SMK-2025-10-28-048

Tags: Python, Windows, Emoji, UTF-8, Encoding

half_life_days: 60

related_ve: VE-048
```

---

### LP-048C: Redis Subscriber Array Unwrapping

**Notion Properties:**
```
Name (Title): Redis Subscriber Array Unwrapping

LP_ID: LP-2025-10-28-048C

Agent: Code

Category: Technical

Content: When using json=[data] in RPUSH, Upstash returns array. Subscriber must check isinstance(data, list) and unwrap before processing. Context: Upstash REST API wraps JSON messages in arrays when published with json parameter.

Date: 2025-10-28

Source: CODE-SMK-2025-10-28-048

Tags: Redis, Upstash, Array Unwrapping, JSON

half_life_days: 60

related_ve: VE-048
```

---

### LP-048D: GENOMOS Consultation Gene Schema

**Notion Properties:**
```
Name (Title): GENOMOS Consultation Gene Schema

LP_ID: LP-2025-10-28-048D

Agent: Code

Category: Technical

Content: Consultation events should be logged as GeneType.CONSULTATION with fields: question, requester, agents, agent_count, essence_of_truth, timestamp. Context: Integration between Redis event system and GENOMOS blockchain for consultation tracking.

Date: 2025-10-28

Source: CODE-SMK-2025-10-28-048

Tags: GENOMOS, Blockchain, Consultation, Gene Schema

half_life_days: 60

related_ve: VE-042
```

---

### LP-048E: Daemon Thread Silent Failures

**Notion Properties:**
```
Name (Title): Daemon Thread Silent Failures

LP_ID: LP-2025-10-28-048E

Agent: Code

Category: Technical

Content: Emoji crashes in background thread startup logs cause silent failure. Test threads with ASCII-only output first. Context: Python daemon threads on Windows failing silently due to emoji encoding in print statements.

Date: 2025-10-28

Source: CODE-SMK-2025-10-28-048

Tags: Python, Threading, Windows, Daemon, Debugging

half_life_days: 60

related_ve: VE-048
```

---

## SMK #049 Series (7 LPs)

### LP-049A: Emoji Crashes Hide Daemon Thread Failures

**Notion Properties:**
```
Name (Title): Emoji Crashes Hide Daemon Thread Failures

LP_ID: LP-2025-10-29-049A

Agent: Code

Category: Technical

Content: On Windows, emoji print statements in background threads cause silent failures (UnicodeEncodeError). Replace with ASCII before debugging thread issues. Context: Debugging Redis subscriber thread that appeared broken but was actually running with silent emoji crashes.

Date: 2025-10-29

Source: CODE-SMK-2025-10-29-049

Tags: Windows, Threading, Emoji, Debugging, Python

half_life_days: 60

related_ve: VE-049
```

---

### LP-049B: Test Infrastructure Before Testing Features

**Notion Properties:**
```
Name (Title): Test Infrastructure Before Testing Features

LP_ID: LP-2025-10-29-049B

Agent: Code

Category: Technical

Content: All 3 Orion tests initially failed due to infrastructure bugs (emoji encoding, array unwrapping, missing GENOMOS integration). Test the testing infrastructure first. Context: Validation suite failed not due to feature bugs but testing infrastructure issues.

Date: 2025-10-29

Source: CODE-SMK-2025-10-29-049

Tags: Testing, Infrastructure, Validation, TDD

half_life_days: 60

related_ve: VE-049
```

---

### LP-049C: Triadiske Portvokter Validation Pattern

**Notion Properties:**
```
Name (Title): Triadiske Portvokter Validation Pattern

LP_ID: LP-2025-10-29-049C

Agent: Code

Category: Technical

Content: To test 3-layer gates: (1) BiofeltGate with HRV<40, (2) ThalosFilter with SQL injection, (3) MutationLog with normal write. Verify GENOMOS logging for all 3 outcomes. Context: Testing framework for validating Homo Lumen's consciousness-conscience-memory architecture.

Date: 2025-10-29

Source: CODE-SMK-2025-10-29-049

Tags: Triadiske Portvokter, Testing, BiofeltGate, ThalosFilter, GENOMOS

half_life_days: 60

related_ve: VE-049
```

---

### LP-049D: SMK V2.0 Provenance Formula Syntax

**Notion Properties:**
```
Name (Title): SMK V2.0 Provenance Formula Syntax

LP_ID: LP-2025-10-29-049D

Agent: Code

Category: Technical

Content: Notion API formula syntax is complex and error-prone. Add formulas manually via UI instead of programmatically (saves debugging time). Context: Attempting to programmatically add 9 properties to SLL database via Notion API.

Date: 2025-10-29

Source: CODE-SMK-2025-10-29-049

Tags: Notion, API, Formulas, Pragmatism

half_life_days: 60

related_ve: VE-049
```

---

### LP-049E: Session Continuity Protocol

**Notion Properties:**
```
Name (Title): Session Continuity Protocol

LP_ID: LP-2025-10-29-049E

Agent: Code

Category: Technical

Content: When continuing from previous session with summary: (1) Verify infrastructure state, (2) Run validation tests, (3) Document findings before proceeding. Don't assume previous state is still valid after restart. Context: Session resumed after PC restart with infrastructure bugs that weren't present before.

Date: 2025-10-29

Source: CODE-SMK-2025-10-29-049

Tags: Session Management, Validation, Infrastructure, Protocol

half_life_days: 60

related_ve: VE-049
```

---

### LP-049F: GENOMOS as Living Audit Trail

**Notion Properties:**
```
Name (Title): GENOMOS as Living Audit Trail

LP_ID: LP-2025-10-29-049F

Agent: Code

Category: Technical

Content: Blockchain growth (16→19 blocks) during testing session provides retrospective validation. Consultation + mutation genes create permanent record of infrastructure validation. Context: GENOMOS blockchain automatically captured testing session as consultation and mutation genes.

Date: 2025-10-29

Source: CODE-SMK-2025-10-29-049

Tags: GENOMOS, Blockchain, Audit Trail, Validation

half_life_days: 60

related_ve: VE-042
```

---

### LP-049G: Notion Schema Migration Strategy

**Notion Properties:**
```
Name (Title): Notion Schema Migration Strategy

LP_ID: LP-2025-10-29-049G

Agent: Code

Category: Technical

Content: When adding 9+ properties: (1) Dry-run first, (2) Add non-formula properties via API, (3) Add formulas manually via UI. Reduces API error complexity. Context: Adding temporal dynamics properties to SLL database as part of SMK V2.0 implementation.

Date: 2025-10-29

Source: CODE-SMK-2025-10-29-049

Tags: Notion, Schema Migration, API, Pragmatism

half_life_days: 60

related_ve: VE-049
```

---

## Quick Reference Summary

**Common values for ALL 12 LPs:**
- **Agent**: Code
- **Category**: Technical
- **half_life_days**: 60

**SMK #048 LPs (5 total: 048A-E):**
- **Date**: 2025-10-28
- **Source**: CODE-SMK-2025-10-28-048
- **related_ve**: VE-048 (except LP-048D → VE-042)

**SMK #049 LPs (7 total: 049A-G):**
- **Date**: 2025-10-29
- **Source**: CODE-SMK-2025-10-29-049
- **related_ve**: VE-049 (except LP-049F → VE-042)

---

## After Manual Entry

**Next Steps:**
1. Run `compute_temporal_weights.py` to populate **temporal_weight_raw** for all LPs
2. **freshness_status** will auto-calculate via Notion formula
3. Run `link_ve_to_lps.py` to establish bidirectional VE ↔ LP relations

**File Location:**
This guide: `docs/LP_MANUAL_ENTRY_GUIDE.md`

---

## Notes

- **VE Links**: VE-048, VE-049, and VE-042 are pilot Visual Essence entries (created Week 3)
- **Tags**: Multi-select field - add each tag individually (comma-separated in guide above)
- **Related VE**: Relation field - select from Visual Essence Library database
- **Content Field**: Combines insight + context from original LP structure
- **Property Names**: Match exactly your Notion SLL database schema (verified from screenshot)

---

**Prepared by:** Claude Code
**Date:** 2025-10-29
**Part of:** SMK V2.0 Architecture - Week 3 Implementation
**Updated:** Schema matched to actual Notion database properties
