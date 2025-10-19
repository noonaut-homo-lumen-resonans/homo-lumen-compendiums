# How to Add New Learning Point

This guide shows you how to document new learning in the Living Compendium system.

## Step 1: Identify Learning

Ask yourself:
- What problem did I solve?
- What did I learn?
- Why does this matter?

## Step 2: Create Markdown File

```bash
# In your agent's Living Compendium
techdocs-source/reference/learning-points/lp-XXX-title.md
```

## Step 3: Add YAML Frontmatter

```yaml
---
title: "LP #XXX: Your Title Here"
lp_id: LP-XXX
date: 2025-10-19
category:
  - development-workflow
  - architecture-patterns
status: complete
triadisk_port:
  - P1
  - P2
  - P3
triadisk_score: 0.95
stress_mode:
  - ventral
owners:
  - code
related_artifacts:
  - path/to/file.ts
related_lps:
  - LP-025
---
```

## Step 4: Write Content

Follow this structure:

1. **Context** - Background and setup
2. **Problem** - What challenge?
3. **Solution** - How did you solve it?
4. **Why This Matters** - Significance
5. **Lessons Learned** - Key takeaways
6. **Triadic Ethics Validation** - XML format
7. **Connection to Previous Learning** - Cross-refs
8. **Emergent Wisdom** - Insights
9. **Key Insight** - One-sentence summary

## Step 5: Cross-Reference

Link to related LPs:

```markdown
See [LP #037](../reference/learning-points/lp-037-hwf-complete.md) for related work.
```

## Example

See **[LP #037: HWF Emotion Wheel Complete](../reference/learning-points/lp-037-hwf-complete.md)**.
