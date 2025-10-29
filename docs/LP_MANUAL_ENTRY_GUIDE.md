# LP Manual Entry Guide - SMK #048 & #049

This guide provides structured data for manually entering 12 Learning Particles (LPs) into the SLL (Strategic Learning Library) Notion database.

## Summary
- **SMK #048**: 5 LPs (Redis Event Streaming)
- **SMK #049**: 7 LPs (Test Tasks + SMK V2.0)
- **Total**: 12 LPs
- **Domain**: Technical
- **Half-life**: 60 days
- **Created**: Oct 28-29, 2025

---

## SMK #048 Series (5 LPs)

### LP-048A: Upstash REST API RPUSH/LPOP Pattern

**Property Values:**
```
lp_id: LP-2025-10-28-048A
title: Upstash REST API RPUSH/LPOP Pattern
insight: Use RPUSH (persistent queue) instead of PUBLISH (ephemeral) for reliable message delivery with Upstash Cloud REST API.
context: Redis event streaming between CSN Server and Ubuntu Playground using Upstash Cloud REST API
domain: Technical
validation_status: Validated
created_time: 2025-10-28
half_life_days: 60
reactivation_count: 0
tags: Redis, Upstash, Message Queue, RPUSH, LPOP
related_ve: VE-048
smk_source: CODE-SMK-2025-10-28-048
```

---

### LP-048B: Python Windows Emoji Handling

**Property Values:**
```
lp_id: LP-2025-10-28-048B
title: Python Windows Emoji Handling
insight: Replace all emoji characters (✅❌📥🚀) with ASCII text ([PASS], [FAIL], etc.) to prevent UnicodeEncodeError on Windows cp1252.
context: Windows cp1252 encoding crashes when printing emojis in Python console output
domain: Technical
validation_status: Validated
created_time: 2025-10-28
half_life_days: 60
reactivation_count: 0
tags: Python, Windows, Emoji, UTF-8, Encoding
related_ve: VE-048
smk_source: CODE-SMK-2025-10-28-048
```

---

### LP-048C: Redis Subscriber Array Unwrapping

**Property Values:**
```
lp_id: LP-2025-10-28-048C
title: Redis Subscriber Array Unwrapping
insight: When using json=[data] in RPUSH, Upstash returns array. Subscriber must check isinstance(data, list) and unwrap before processing.
context: Upstash REST API wraps JSON messages in arrays when published with json parameter
domain: Technical
validation_status: Validated
created_time: 2025-10-28
half_life_days: 60
reactivation_count: 0
tags: Redis, Upstash, Array Unwrapping, JSON
related_ve: VE-048
smk_source: CODE-SMK-2025-10-28-048
```

---

### LP-048D: GENOMOS Consultation Gene Schema

**Property Values:**
```
lp_id: LP-2025-10-28-048D
title: GENOMOS Consultation Gene Schema
insight: Consultation events should be logged as GeneType.CONSULTATION with fields: question, requester, agents, agent_count, essence_of_truth, timestamp.
context: Integration between Redis event system and GENOMOS blockchain for consultation tracking
domain: Technical
validation_status: Validated
created_time: 2025-10-28
half_life_days: 60
reactivation_count: 0
tags: GENOMOS, Blockchain, Consultation, Gene Schema
related_ve: VE-042
smk_source: CODE-SMK-2025-10-28-048
```

---

### LP-048E: Daemon Thread Silent Failures

**Property Values:**
```
lp_id: LP-2025-10-28-048E
title: Daemon Thread Silent Failures
insight: Emoji crashes in background thread startup logs cause silent failure. Test threads with ASCII-only output first.
context: Python daemon threads on Windows failing silently due to emoji encoding in print statements
domain: Technical
validation_status: Validated
created_time: 2025-10-28
half_life_days: 60
reactivation_count: 0
tags: Python, Threading, Windows, Daemon, Debugging
related_ve: VE-048
smk_source: CODE-SMK-2025-10-28-048
```

---

## SMK #049 Series (7 LPs)

### LP-049A: Emoji Crashes Hide Daemon Thread Failures

**Property Values:**
```
lp_id: LP-2025-10-29-049A
title: Emoji Crashes Hide Daemon Thread Failures
insight: On Windows, emoji print statements in background threads cause silent failures (UnicodeEncodeError). Replace with ASCII before debugging thread issues.
context: Debugging Redis subscriber thread that appeared broken but was actually running with silent emoji crashes
domain: Technical
validation_status: Validated
created_time: 2025-10-29
half_life_days: 60
reactivation_count: 0
tags: Windows, Threading, Emoji, Debugging, Python
related_ve: VE-049
smk_source: CODE-SMK-2025-10-29-049
```

---

### LP-049B: Test Infrastructure Before Testing Features

**Property Values:**
```
lp_id: LP-2025-10-29-049B
title: Test Infrastructure Before Testing Features
insight: All 3 Orion tests initially failed due to infrastructure bugs (emoji encoding, array unwrapping, missing GENOMOS integration). Test the testing infrastructure first.
context: Validation suite failed not due to feature bugs but testing infrastructure issues
domain: Technical
validation_status: Validated
created_time: 2025-10-29
half_life_days: 60
reactivation_count: 0
tags: Testing, Infrastructure, Validation, TDD
related_ve: VE-049
smk_source: CODE-SMK-2025-10-29-049
```

---

### LP-049C: Triadiske Portvokter Validation Pattern

**Property Values:**
```
lp_id: LP-2025-10-29-049C
title: Triadiske Portvokter Validation Pattern
insight: To test 3-layer gates: (1) BiofeltGate with HRV<40, (2) ThalosFilter with SQL injection, (3) MutationLog with normal write. Verify GENOMOS logging for all 3 outcomes.
context: Testing framework for validating Homo Lumen's consciousness-conscience-memory architecture
domain: Technical
validation_status: Validated
created_time: 2025-10-29
half_life_days: 60
reactivation_count: 0
tags: Triadiske Portvokter, Testing, BiofeltGate, ThalosFilter, GENOMOS
related_ve: VE-049
smk_source: CODE-SMK-2025-10-29-049
```

---

### LP-049D: SMK V2.0 Provenance Formula Syntax

**Property Values:**
```
lp_id: LP-2025-10-29-049D
title: SMK V2.0 Provenance Formula Syntax
insight: Notion API formula syntax is complex and error-prone. Add formulas manually via UI instead of programmatically (saves debugging time).
context: Attempting to programmatically add 9 properties to SLL database via Notion API
domain: Technical
validation_status: Validated
created_time: 2025-10-29
half_life_days: 60
reactivation_count: 0
tags: Notion, API, Formulas, Pragmatism
related_ve: VE-049
smk_source: CODE-SMK-2025-10-29-049
```

---

### LP-049E: Session Continuity Protocol

**Property Values:**
```
lp_id: LP-2025-10-29-049E
title: Session Continuity Protocol
insight: When continuing from previous session with summary: (1) Verify infrastructure state, (2) Run validation tests, (3) Document findings before proceeding. Don't assume previous state is still valid after restart.
context: Session resumed after PC restart with infrastructure bugs that weren't present before
domain: Technical
validation_status: Validated
created_time: 2025-10-29
half_life_days: 60
reactivation_count: 0
tags: Session Management, Validation, Infrastructure, Protocol
related_ve: VE-049
smk_source: CODE-SMK-2025-10-29-049
```

---

### LP-049F: GENOMOS as Living Audit Trail

**Property Values:**
```
lp_id: LP-2025-10-29-049F
title: GENOMOS as Living Audit Trail
insight: Blockchain growth (16→19 blocks) during testing session provides retrospective validation. Consultation + mutation genes create permanent record of infrastructure validation.
context: GENOMOS blockchain automatically captured testing session as consultation and mutation genes
domain: Technical
validation_status: Validated
created_time: 2025-10-29
half_life_days: 60
reactivation_count: 0
tags: GENOMOS, Blockchain, Audit Trail, Validation
related_ve: VE-042
smk_source: CODE-SMK-2025-10-29-049
```

---

### LP-049G: Notion Schema Migration Strategy

**Property Values:**
```
lp_id: LP-2025-10-29-049G
title: Notion Schema Migration Strategy
insight: When adding 9+ properties: (1) Dry-run first, (2) Add non-formula properties via API, (3) Add formulas manually via UI. Reduces API error complexity.
context: Adding temporal dynamics properties to SLL database as part of SMK V2.0 implementation
domain: Technical
validation_status: Validated
created_time: 2025-10-29
half_life_days: 60
reactivation_count: 0
tags: Notion, Schema Migration, API, Pragmatism
related_ve: VE-049
smk_source: CODE-SMK-2025-10-29-049
```

---

## Quick Copy-Paste Checklist

For each LP, create a new entry in SLL database and paste these values:

**Common values for all 12 LPs:**
- domain: Technical
- validation_status: Validated
- half_life_days: 60
- reactivation_count: 0

**SMK #048 LPs (5 total):**
- created_time: 2025-10-28
- smk_source: CODE-SMK-2025-10-28-048
- related_ve: VE-048 (except LP-048D which uses VE-042)

**SMK #049 LPs (7 total):**
- created_time: 2025-10-29
- smk_source: CODE-SMK-2025-10-29-049
- related_ve: VE-049 (except LP-049F which uses VE-042)

---

## Notes

1. **VE Links**: VE-048, VE-049, and VE-042 are pilot Visual Essence entries created in Week 3
2. **Temporal Weights**: After manual entry, run `compute_temporal_weights.py` to populate temporal_weight_raw
3. **Freshness Status**: Will auto-calculate via Notion formula once temporal_weight_raw is set
4. **Tags**: Multi-select field - add each tag individually
5. **Related VE**: Relation field - select from Visual Essence Library database

---

**Prepared by:** Claude Code
**Date:** 2025-10-29
**Part of:** SMK V2.0 Architecture - Week 3 Implementation
