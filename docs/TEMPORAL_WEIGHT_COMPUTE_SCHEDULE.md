# Temporal Weight Computation - Manual Schedule

**Created:** 29. oktober 2025
**Script:** `compute_temporal_weights.py`
**Database:** SLL (Shared Learning Library)
**Formula:** Designed by Abacus (SMK V2.0 Architecture)

---

## Overview

The temporal weight computation script calculates `temporal_weight_raw` for all Learning Points (LPs) in the SLL database based on age, citations, and domain-specific decay rates.

**Formula:**
```
decay_factor = e^(-ln(2) * (age_days / half_life_days))
reactivation_boost = 1 + (reactivation_count * 0.1)
temporal_weight_raw = min(1.0, decay_factor * reactivation_boost)
```

---

## When to Run

### Recommended Schedule

**Manual execution recommended:**
- **Weekly** during active development (high LP creation rate)
- **Bi-weekly** during stable periods
- **Monthly** for maintenance

**Trigger events:**
- After batch publishing new LPs (5+ LPs)
- After major SMK/ARF updates (new citations)
- Before generating reports/analytics
- When freshness status distribution looks stale

---

## How to Run

### Step 1: Dry-Run (Preview Changes)

```bash
cd "C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums"
python compute_temporal_weights.py --dry-run
```

**Review output:**
- How many LPs need updates?
- Are freshness distributions reasonable?
- Any unexpected results?

### Step 2: Apply Updates

```bash
python compute_temporal_weights.py
```

**Expected output:**
```
Fetching all LPs from SLL database...
   Fetched XX LPs

Computing temporal weights...
   XX LPs need updates

Applying XX updates to Notion...
   Successfully updated: XX/XX
```

### Step 3: Verify

Check in Notion:
- Open SLL database
- Sort by `temporal_weight` (descending)
- Verify `freshness_status` colors:
  - Green = fresh (≥0.7)
  - Yellow = aging (0.3-0.7)
  - Gray = stale (<0.3)

---

## Expected Results

### New LPs (0-30 days old)
- **temporal_weight_raw:** 0.85-1.0
- **freshness_status:** fresh

### Mature LPs (30-120 days)
- **temporal_weight_raw:** 0.5-0.85
- **freshness_status:** fresh → aging

### Aging LPs (120+ days)
- **temporal_weight_raw:** 0.25-0.5
- **freshness_status:** aging → stale

### With Citations
- **Boost:** +10% per citation
- **Example:** 60-day LP with 2 citations = 0.5 × 1.2 = 0.6 (aging)

---

## Freshness Thresholds

| Status | Threshold | Color | Meaning |
|--------|-----------|-------|---------|
| **fresh** | ≥ 0.7 | Green | High relevance, actively useful |
| **aging** | 0.3-0.7 | Yellow | Moderate relevance, still valuable |
| **stale** | < 0.3 | Gray | Low relevance, needs review/reactivation |

---

## Half-Life Values by Domain

The `half_life_days` property determines how fast LPs decay:

| Domain | Half-Life | Rationale |
|--------|-----------|-----------|
| **Code/Technical** | 60 days | Fast-changing tech stacks |
| **Research** | 180 days | Scientific findings evolve |
| **Ethics/Philosophy** | 365 days | Timeless principles |
| **Architecture** | 730 days | Long-term design patterns |
| **GENOMOS/Blockchain** | 1095 days | Infrastructure decisions |
| **Default** | 120 days | General knowledge |

**To set domain-specific half-life:**
1. Open LP in Notion
2. Edit `half_life_days` property
3. Set appropriate value from table above
4. Re-run compute script

---

## Monitoring & Alerts

### Key Metrics to Track

**Freshness distribution:**
- Target: 60% fresh, 30% aging, 10% stale
- Alert if: >30% stale (knowledge base deteriorating)

**Average temporal weight:**
- Target: >0.6 (healthy knowledge base)
- Alert if: <0.4 (knowledge base aging)

**Citation rate:**
- Target: 20%+ LPs cited at least once
- Alert if: <10% (knowledge not being reused)

---

## Troubleshooting

### Problem: All LPs showing "fresh"
**Diagnosis:** LPs are very new (< 1 week old)
**Solution:** Normal behavior. Wait 30+ days for distribution to emerge.

---

### Problem: Too many "stale" LPs
**Diagnosis:** Knowledge base not being maintained
**Solution:**
1. Review stale LPs (are they outdated?)
2. Archive truly obsolete LPs
3. Cite relevant LPs in new SMKs/ARFs
4. Update `half_life_days` if decay too fast

---

### Problem: Script errors on specific LPs
**Diagnosis:** Missing properties or invalid data
**Solution:**
1. Check error message for LP ID
2. Open LP in Notion
3. Verify all temporal properties exist:
   - `temporal_weight_raw` (number)
   - `half_life_days` (number)
   - `reactivation_count` (number)
   - `freshness_status` (select)
4. Add missing properties manually
5. Re-run script

---

### Problem: Updates taking too long
**Diagnosis:** Large database (100+ LPs) + Notion API rate limits
**Solution:**
- Normal. Script updates ~10 LPs per second
- 100 LPs = ~10 seconds
- If >500 LPs, consider batching

---

## Integration with SMK V2.0

### Week 1 (Complete ✅)
- 9 properties added to SLL schema
- Formula implemented in Notion

### Week 2 (Complete ✅)
- `compute_temporal_weights.py` script created
- Manual execution workflow documented

### Week 3 (Pending)
- Visual Essence Library database
- Shadow Audit protocol

### Week 4 (Pending)
- Coalition training on SMK V2.0
- Automated citation tracking (future)

---

## Future Enhancements

**Potential improvements:**

1. **Automated Citation Tracking**
   - GitHub Actions to detect LP citations in new SMKs
   - Auto-increment `reactivation_count`
   - Auto-update `last_cited_timestamp`

2. **GitHub Actions Weekly Run**
   - Scheduled cron job to run compute script
   - Commit results to git
   - Post summary to Discord/Slack

3. **Analytics Dashboard**
   - Visualize freshness distribution over time
   - Track average temporal weight trends
   - Identify most/least cited LPs

4. **Adaptive Half-Lives**
   - Machine learning to optimize half-life values
   - Adjust based on actual citation patterns

---

## Changelog

**v1.0 (2025-10-29)**
- Initial implementation
- Manual execution workflow
- Dry-run support
- Abacus' exponential decay formula

---

## Support

**Questions or issues?**
- Check script output for error messages
- Review this document's Troubleshooting section
- Consult SMK #049 for implementation details
- Ask Code or Abacus in Agent Resonance Field

---

**Script Location:** `C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\compute_temporal_weights.py`
**SLL Database ID:** `84da6cbd09d640fb868e41444b941991`
**Formula Source:** Abacus (SMK V2.0 Architecture, Week 2)

---

*Last Updated: 2025-10-29*
