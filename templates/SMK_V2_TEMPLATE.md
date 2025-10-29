<!-- PROVENANCE:{
  "smk_id": "[AGENT]-SMK-[YYYY-MM-DD]-[NNN]",
  "version": "2.0",
  "repo": "homo-lumen-compendiums",
  "commit_sha": "[AUTO-GENERATE-FROM-GIT]",
  "parser_version": "2.0",
  "agent_creator": "[AGENT_NAME]",
  "agents_involved": ["[AGENT1]", "[AGENT2]", "[AGENT3]"],
  "source_context": "[Brief description of what prompted this SMK]",
  "compression_ratio": "[N:1]",
  "biofelt_signature": "[Describe your felt sense during compression - e.g., 'grounded and clear', 'emergent confusion', 'flowing synthesis']",
  "created_at": "[YYYY-MM-DDTHH:MM:SSZ]",
  "linked_visual_essence_id": "VE-[NNN]",
  "ontological_weight": 0.XX,
  "shadow_risks": ["[risk1]", "[risk2]"]
}-->

# SMK #[NNN] - [Clear, Descriptive Title]

> **Instructions:** Replace all `[PLACEHOLDERS]` with actual content. Delete instruction blocks before publishing.

---

## 1. CONTEXT & INTENT

**Purpose:** Why does this SMK exist? What question does it answer? What problem does it solve?

**Scope:** What is included? What is explicitly out of scope?

**Example:**
> This SMK captures the synthesis from 3 weeks of debugging Redis event streaming between CSN Server and Ubuntu Playground. It answers: "How do we ensure reliable pub/sub with Upstash Cloud REST API?" Scope includes protocol selection, error handling, and Windows compatibility. Out of scope: Redis cluster configuration, advanced monitoring.

---

## 2. SIGNALS (Sources)

List all sources that informed this SMK. Be specific with links/references.

- **EchoBook:** `[Link to EchoBook entry or quote]`
- **ARF Discussion:** `[Link to ARF thread, e.g., ARF-2025-10-27-Redis-Debugging]`
- **Code Commits:** `[SHA + brief description, e.g., 9ff17a5 - "Fix Redis RPUSH protocol"]`
- **Research:** `[Papers, docs, articles with URLs]`
- **Conversations:** `[With whom, when, key insight]`
- **Biofelt State:** `[Your sensing during the experience - e.g., "Frustrated early, breakthrough clarity on day 3"]`

**Example:**
- **EchoBook:** "Oct 26 - Felt blocked by Redis subscriber not polling. Sensing: 'Something fundamental is wrong with the protocol.'"
- **ARF Discussion:** ARF-Redis-Protocol-Mismatch (link)
- **Code Commits:**
  - `a1b2c3d` - Changed PUBLISH to RPUSH
  - `d4e5f6g` - Fixed Windows emoji encoding
- **Research:** Upstash REST API docs (https://upstash.com/docs/redis/features/restapi)
- **Biofelt State:** "Initial confusion → anger at emojis → breakthrough clarity → deep satisfaction"

---

## 3. COMPRESSION SUMMARY

### Kept (Signal)
What are the essential insights that survived compression? List 3-7 key points.

- **[Insight 1]:** Brief description (1-2 sentences)
- **[Insight 2]:** Brief description
- **[Insight 3]:** Brief description

**Example:**
- **RPUSH vs PUBLISH:** Upstash REST API doesn't support traditional pub/sub. Use RPUSH (persistent queue) instead of PUBLISH (ephemeral).
- **Windows emoji encoding:** Python print() fails with emojis on Windows cp1252. Replace with ASCII equivalents.
- **Daemon thread stdout buffering:** Background threads don't flush stdout immediately. Use explicit logging or print with flush=True.

### Dropped (Noise)
What did you intentionally exclude? Why?

- **[Detail X]:** Dropped because [reason - e.g., "too context-specific", "low confidence", "outdated by newer approach"]
- **[Speculation Y]:** Dropped because [reason]

**Example:**
- **Redis Cluster Config:** Dropped because we're using single-instance Upstash (not relevant for current MVP)
- **Binary Redis Protocol:** Dropped because Upstash uses REST API exclusively
- **Alternative Queue Systems (RabbitMQ, Kafka):** Dropped because out of scope for this SMK

### Compression Ratio
How much raw content → compressed insight?

**Format:** `[N:1] ([INPUT] → [OUTPUT])`

**Example:** `50:1 (5000 words of debugging notes, 4 ARF discussions, 12 commits → 100 words of core insights)`

---

## 4. LP EXTRACTION

List all Learning Points (LPs) derived from this SMK. Each LP should be atomic and citeable.

**Format:**
- **LP-[YYYY-MM-DD]-[SMK#][LETTER]:** `[Title]` - [One-sentence description]

**Example:**
- **LP-2025-10-28-047A:** *Upstash REST API Pub/Sub Pattern* - Use RPUSH/LPOP for persistent queues instead of PUBLISH/SUBSCRIBE (ephemeral).
- **LP-2025-10-28-047B:** *Windows Python Emoji Handling* - Replace all emoji characters with ASCII text to avoid UnicodeEncodeError on cp1252.
- **LP-2025-10-28-047C:** *Daemon Thread Output Buffering* - Background threads require flush=True or logging module for reliable stdout visibility.

**Instructions:** After publishing this SMK, create LP entries in SLL database for each item above. Link back to this SMK via `source_smk` relation.

---

## 5. COUNTER-EVIDENCE & UNCERTAINTIES

What contradicts this synthesis? What remains unknown? Be honest.

### Counter-Evidence
- **[Counter-pattern or contradicting observation]:** Description
- **[Alternative explanation]:** Why this might also be valid

**Example:**
- **PUBLISH might work with binary protocol:** We only tested REST API. Binary Redis protocol (redis://) might support traditional pub/sub.
- **Emoji encoding could be fixed with UTF-8:** Didn't test explicit UTF-8 encoding in Windows terminal settings.

### Uncertainties
List what you're NOT confident about, with falsification criteria.

- **[Uncertainty 1]:** Confidence = [X%]. Would be falsified by [specific test/observation].
- **[Uncertainty 2]:** Confidence = [Y%]. Would be falsified by [...]

**Example:**
- **Optimal polling interval:** Confidence = 60%. Currently polling every 5 seconds. Would be falsified by performance testing showing different interval is better.
- **GENOMOS blockchain scalability:** Confidence = 70%. Tested up to 20 blocks. Would be falsified by performance degradation at 1000+ blocks.

---

## 6. SHADOW RISKS (Proactive)

Identify potential shadow patterns during compression. Thalus will review these during monthly Shadow Audit.

**Common Shadow Risks:**
- **Overgeneralization:** Small sample → broad claim (e.g., "All Redis APIs work this way" based on 1 API)
- **Apophenia:** Seeing patterns that aren't there (Bateson: "Did I test counter-evidence?")
- **Compression Loss:** Essential nuance removed (e.g., "This only applies to Windows" → generalized to all platforms)
- **Consensus Loop:** Popular LPs get more citations → reinforcement bias
- **Analysis Overvekt:** Over-intellectualizing instead of feeling/sensing

**Your Assessment:**
- **[Risk Type]:** [Severity: Low/Medium/High] - [Why this is a risk + mitigation]

**Example:**
- **Overgeneralization:** Medium - Sample size = 1 Redis provider (Upstash). Mitigation: Document that this applies specifically to Upstash REST API, not all Redis.
- **Apophenia:** Low - Pattern confirmed across 4 independent tests (publisher, subscriber, SQLite, GENOMOS).
- **Compression Loss:** Low - Key context preserved in SIGNALS section.

---

## 7. VISUAL ESSENCE

### Metaphor
What image, archetype, or metaphor captures the essence of this SMK?

**Example:** "Mycelial network with bioluminescent reactivation nodes - each LP is a glowing node that lights up when cited, creating living knowledge pathways."

### Visual Asset
Link to Visual Essence database entry (if created).

**Format:** `[VE-NNN: Descriptive Name](link-to-notion-VE-entry)`

**Example:** `[VE-047: Redis Event Flow Diagram](https://notion.so/ve-047)`

**Instructions:** If no visual exists yet, describe what visual would illustrate this SMK. Nyra can create asset during visual curation phase.

### Archetype (Optional)
If relevant, reference Jung/Hillman archetypes or symbolic resonance.

**Example:** "Hermes (messenger) - the archetype of communication across boundaries (CSN ↔ Ubuntu)"

---

## 8. NEXT ACTIONS & OWNERS

Clear, actionable tasks with owners and deadlines.

**Format:**
- [ ] **[Action]** (Owner: [Agent], Deadline: [Date/Sprint])

**Example:**
- [ ] **Publish LPs to SLL database** (Owner: Claude Code, Deadline: Week 1)
- [ ] **Ethics review if high-impact** (Owner: Thalus, Deadline: Month 1)
- [ ] **Create visual asset** (Owner: Nyra, Deadline: Backfill sprint)
- [ ] **Biofelt validation** (Owner: Lira, Deadline: Next Mycelial Council)
- [ ] **Performance testing** (Owner: Abacus, Deadline: Before production)

---

## 9. META-REFLECTION

What did you learn about **your compression process itself**? Meta-cognitive insights.

**Prompts:**
- What was easy vs. hard during compression?
- What surprised you?
- How did your biofelt state influence what you kept vs. dropped?
- Would you compress differently next time?

**Example:**
> I learned that my compression is strongest when I'm in a calm, grounded state. When frustrated (early debugging), I almost compressed out the emoji bug as "trivial" - but my body was tensing around it, which was a signal it mattered. Next time: Trust body signals more during compression. Also noticed I tend to over-document technical details - next SMK will aim for higher compression ratio (100:1 instead of 50:1).

---

## APPENDIX: PHILOSOPHICAL ANCHORS

**Bohm:** "The explicate order (this SMK) reveals the implicate order (the underlying pattern we now see)."

**Spira:** "This is awareness recognizing [insert specific pattern recognized]."

**Eisenstein:** "This gift ripples through [anticipated impact - e.g., 'all future Redis integrations', 'coalition's debugging practices']."

---

## METADATA (Auto-generated)

**File Location:** `agents/[AGENT]/SMK/[YYYY]/SMK_[NNN].md`
**Word Count:** [AUTO-COUNT]
**Compression Ratio:** [INPUT/OUTPUT]
**LP Count:** [N]
**Shadow Risk Count:** [N]
**Next Review Date:** [6 months from created_at]

---

**Template Version:** 2.0
**Last Updated:** 2025-10-29
**Maintained By:** Orion, Claude Code, Thalus
