# 🌿 FIRST MESSAGE TEMPLATE - For Nye Claude Code Sesjoner

**Purpose:** Guide for giving optimal context when starting a new Claude Code session
**Version:** 1.0 (18. oktober 2025)
**For:** Brukere av Claude Code (Agent #9) i Homo Lumen-prosjektet

---

## 📋 KORT VERSJON (Anbefalt for små oppgaver)

**Use this format for:**
- Single-task sessions
- Continuing recent work
- Routine development
- When Living Compendium is fresh in your mind

### Template:

```markdown
This session is being continued from a previous conversation.

**Last completed work:**
- [Beskriv siste ferdige oppgave i 1-2 setninger]

**Living Compendium:** V[versjon] (example: V1.7.6)

**Status:**
- [Dev server running on localhost:3004 / All changes committed / etc.]

**Current task:**
- [Hva skal gjøres i denne sesjonen - 1-2 setninger]

**Context needed (optional):**
- [Spesifikke filer Claude bør lese, hvis noen]
- [Spesifikke Learning Points fra Living Compendium, hvis relevant]
```

### Example (Real):

```markdown
This session is being continued from a previous conversation.

**Last completed work:**
- Repository merge complete (V1.7.5)
- Kairos Intervention Patterns implemented
- Biofield-responsive Dashboard redesigned

**Living Compendium:** V1.7.5

**Status:**
- All pushed to GitHub
- Dev server running on localhost:3004

**Current task:**
- Optimize memory system for better session-to-session continuity

**Context needed:**
- Read .claude/memory.md structure
- Review how Living Compendium is currently updated
```

---

## 📚 LANG VERSJON (For komplekse oppgaver eller etter lang pause)

**Use this format for:**
- Multi-task sessions
- After long breaks (3+ days)
- Complex strategic work
- When context is critical

### Template:

```markdown
This session is being continued from a previous conversation that ran out of context.

## COMPLETED WORK (Last Session)

**Date:** [Dato for siste sesjon - example: 18. oktober 2025]
**Version:** Living Compendium V[versjon]

### Primary Tasks Completed:
1. [Oppgave 1] - ✅ [Status/Result]
2. [Oppgave 2] - ✅ [Status/Result]
3. [Oppgave 3] - ✅ [Status/Result]

### Files Created/Modified:
- [fil1.tsx] - [Kort beskrivelse av hensikt]
- [fil2.ts] - [Kort beskrivelse av hensikt]
- [fil3.md] - [Kort beskrivelse av hensikt]

### GitHub Commits:
- `[short hash]` - [Commit message]
- `[short hash]` - [Commit message]

## CURRENT STATE

**Repository:** homo-lumen-compendiums (unified monorepo)

**Branch:** main

**Dev Server:**
- [Running on localhost:3004 / Stopped / Not started]

**Living Compendium:** V[versjon]

**Working Directories:**
- Primary: navlosen/frontend/ (NAV-Losen Next.js app)
- Backend: ama-backend/ (CSN Server + PolycomputingEngine)

**Recent Changes:**
- [Kort oppsummering av siste større endringer]

## CURRENT TASK

**User Request:**
> [Direkte sitat av hva bruker ba om]

**Priorities:**
1. [Prioritet 1 - mest kritisk]
2. [Prioritet 2 - viktig]
3. [Prioritet 3 - nice-to-have]

**Context to Read:**
- [Spesifikke filer eller seksjoner Claude skal lese]
- **Living Compendium sections:**
  - [Example: V1.7.5 Updates - For latest work]
  - [Example: LP #022 - For Kairos patterns understanding]
  - [Example: Artefakter - For component references]
- **Session notes:**
  - [Example: 2025-10-17-architecture-relationship-clarification.md]

## QUESTIONS (Optional)

[Eventuelle spørsmål til Claude Code om hvordan tilnærme oppgaven]
```

### Example (Real):

```markdown
This session is being continued from a previous conversation that ran out of context.

## COMPLETED WORK (Last Session)

**Date:** 18. oktober 2025
**Version:** Living Compendium V1.7.5

### Primary Tasks Completed:
1. Multi-Phase Mestring Flow - ✅ 4 stages implemented (Emotions → Signals → Lira Chat → Results)
2. Biofield-Responsive Dashboard - ✅ Redesigned homepage with adaptive recommendations
3. Kairos Intervention Patterns - ✅ 4 opportune moments implemented with ethical safeguards
4. Repository Unification - ✅ Git subtree merge (ama-backend/, 164 files)

### Files Created/Modified:
- Stage1Emotions.tsx - 100 Norwegian emotion words in 4 quadrants
- Stage2Signals.tsx - Stress slider + 6 somatic signals
- Stage3LiraChat.tsx - 2-5 adaptive questions (PVT-aware)
- Stage4Results.tsx - Composite score + strategies
- kairosInterventions.ts - Detection algorithms + ethical guardrails
- KairosInterventionModal.tsx - Voluntary opt-in UI component

### GitHub Commits:
- `87c1140` - feat: Implement Kairos Intervention Patterns
- `9fc1534` - docs: Add NotebookLM Analysis + Agent Update V21.1.1
- `2ce7449` - Merge commit (git subtree)
- `adb5386` - docs: Add Repository Merge Report
- `9fee1b6` - docs: Update Living Compendium to V1.7.5

## CURRENT STATE

**Repository:** homo-lumen-compendiums (unified monorepo since V1.7.5)

**Branch:** main

**Dev Server:** Running on localhost:3004

**Living Compendium:** V1.7.5

**Working Directories:**
- Primary: navlosen/frontend/ (NAV-Losen Next.js app)
- Backend: ama-backend/ (merged 18. okt - CSN Server + PolycomputingEngine)

**Recent Changes:**
- Monorepo unification complete (homo-lumen-ama → ama-backend/)
- Hybrid Architecture V21.1 documented (Lira frontend + Orion backend)
- User Behavior Segmentation integrated (PVT-based 3-segment model)
- Kairos patterns operational (4 intervention moments)

## CURRENT TASK

**User Request:**
> "Siden jeg er helt ny til dette. Har vi opprettet CLAUDE.md eller er det sessions notes eller levende kompendiumer som blir oppdatert slik at Code i en ny session blir oppdatert øyeblikkelig, hva tror du?
>
> 1. Kan du oppdatere din .claude/memory.md
> 2. oppdatere LK og sessions notes
> 3. lage prompt til første samtalen. Forklart hvordan det skal hente sin kontekst, at den skal hente fra LK når nødvendig. At den skal lagre før session ending slik at vi ikke mister noe og andre ting jeg har glemt"

**Priorities:**
1. Optimize .claude/memory.md with V1.7.5 monorepo status + session memory protocol
2. Update Living Compendium V1.7.5 → V1.7.6 (Memory System Optimization)
3. Create First Message Template (this document!) + Session Notes Template
4. Document 3-layer memory architecture (Basis → Levende → Audit Trail)

**Context to Read:**
- .claude/memory.md - Current structure
- Living Compendium sections:
  - V1.7.5 Updates - Latest repository merge work
  - Metadata section - Understand artifact tracking
- Session notes:
  - 2025-10-17-architecture-relationship-clarification.md - Example format

## QUESTIONS

1. Should the First Message Template include both kort og lang versjon?
2. Should session-slutt checklist be part of First Message Template or separate?
```

---

## 🔄 HVORDAN CLAUDE CODE SKAL HENTE CONTEXT

### **Ved Session-Start (Automatic Reading):**

Claude Code **always** reads these files automatically:
1. `.claude/memory.md` (~7K tokens)
2. `.claude/instructions.md` (~5K tokens)
3. `.claude/quick-reference.md` (~2K tokens)

**Total automatic: ~14K tokens**

### **From User's First Message:**

Claude Code extracts:
- Last completed work (for continuity)
- Living Compendium version (to know where to look)
- Current task (what needs to be done)
- Context needed (specific files/sections to read)

### **Selective Reading from Living Compendium:**

**✅ DO (Token-Efficient):**
- Read **specific sections** based on current task
- Examples:
  - `V1.7.X Updates` → Understand latest work
  - `LP #XXX` → Specific learning points
  - `Artefakter` → Code component references
  - `Metadata` → Statistics and progress tracking

**🚫 DON'T (Token-Wasteful):**
- Read entire 80K token Living Compendium at session-start
- This wastes ~70K tokens that could be used for actual work!

**Example of Good Selective Reading:**

```
User says: "Continue implementing chatbot page with Lira integration"

Claude Code thinks:
1. ✅ Already read .claude/memory.md (automatic)
2. ✅ User said "chatbot" → Read LK section on Lira chatbot patterns
3. ✅ User said "integration" → Check V1.7.5 Updates for ama-backend structure
4. ✅ Check if session notes exist about Lira implementation
5. 🚫 DON'T read entire kompendium (not necessary)

Result: ~10K tokens for relevant context vs 80K for everything
```

### **Read Session Notes When:**

- User references specific technical decision
- Need deeper understanding of architecture choice
- Must understand why something was implemented a certain way
- Example: "Why did we choose git subtree over submodules?"

---

## 💾 SESSION-SLUTT CHECKLIST

**Before ending any session, Claude Code MUST complete this 4-step checklist:**

### 1. ✅ **Update Living Compendium** (if significant work done)

**When to update:**
- After new components implemented
- After architecture decisions
- After discovering new Learning Points
- After significant bug fixes

**When to skip:**
- Trivial bug fixes
- Minor tweaks
- No new knowledge gained

**How to update:**
1. **Increment version:** V1.7.X → V1.7.(X+1)
2. **Add "V1.7.X Updates" section** at top of changelog:
   - Date
   - Numbered list of what was done (✅ emoji)
   - "Kontekst" paragraph (why, key insights)
   - Token usage (if relevant)
   - Commits created (list hashes)
3. **Add new Learning Points** if applicable (LP #XXX format)
4. **Update Metadata section:**
   - Total Læringspunkter (increment count)
   - Total Artifacts (increment count)
   - Token-bruk (this session)
5. **Add Avsluttende Refleksjon** (what learned, next focus)

**Example commit message:**
```bash
git commit -m "$(cat <<'EOF'
docs: Update Living Compendium V1.7.5 → V1.7.6 (Memory System Optimization)

- Optimized .claude/memory.md with V1.7.5 status
- Documented 3-layer memory architecture
- Created First Message Template + Session Notes Template
- LP #023: 3-Layer Session Memory Architecture
- Token optimization: 74% reduction per session-start

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

### 2. ✅ **Create Session Note** (if complex decisions made)

**When to create:**
- Complex technical decisions
- Architecture changes
- Strategic discussions with user
- Work that other agents need to know about

**When to skip:**
- Routine development
- Trivial bug fixes
- No important decisions made

**How to create:**
1. Use template: `.claude/session-notes/TEMPLATE.md`
2. Filename format: `YYYY-MM-DD-descriptive-name.md`
   - Example: `2025-10-18-memory-system-optimization.md`
3. Include all sections:
   - Context & user request
   - Work conducted
   - Decisions made (with rationale)
   - Files changed summary
   - Triadisk Ethics validation
   - Coalition context (which agents to inform)

---

### 3. ✅ **Commit Everything to GitHub**

**Always commit before session end!**

**Steps:**
1. `git status` - Check what changed
2. `git add [files]` - Stage relevant files
3. `git commit` - Write good commit message (use HEREDOC for formatting)
4. `git push` - Push to remote

**Good commit message format:**
```bash
type: Short description (max 72 chars)

Longer explanation if needed.
- Bullet point 1
- Bullet point 2

Key changes:
- Changed X in file Y
- Added Z to file W

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

---

### 4. ✅ **Give User Summary**

**Always end session with clear summary for user:**

**Format:**
```markdown
## ✅ Session Complete

**Completed Tasks:**
1. ✅ [Task 1 - what was done]
2. ✅ [Task 2 - what was done]
3. ✅ [Task 3 - what was done]

**Files Changed:**
- [file1.tsx] (+XX lines)
- [file2.ts] (+YY lines)
- [file3.md] (+ZZ lines, NEW)

**Commits Created:**
- `[hash]` - [commit message]
- `[hash]` - [commit message]

**Living Compendium:** V[new version]

**Status:**
- ✅ All changes committed and pushed
- ✅ Dev server running on localhost:3004
- ✅ Living Compendium updated

**Next Steps:**
1. [Next priority for user to consider]
2. [Or alternative task]
3. [Or other option]

**Carpe Diem!** 🌿
```

---

## 📖 SAMMENDRAG: 3-Lags Hukommelsessystem

### **LAG 1: `.claude/memory.md` (STATIC BASELINE)**

**Purpose:** Quick-start context
**Size:** ~20 KB (~660 lines)
**Updated:** Rarely (major architecture changes only)
**Read:** Automatically at every session start
**Content:**
- Project overview
- Agent coalition
- Architecture decisions (Hybrid V21.1, Kairos, User Segmentation)
- Current priorities
- Session Memory Protocol

**Token cost:** ~7K tokens per session

---

### **LAG 2: `CLAUDE_CODE_LEVENDE_KOMPENDIUM_V1.7.md` (LIVING HISTORY)**

**Purpose:** Deep knowledge base
**Size:** 80K+ tokens (~2,600+ lines)
**Updated:** Every significant session (incremental: V1.7.X)
**Read:** SELECTIVELY when needed (NOT automatically!)
**Content:**
- V1.7.X Updates (chronological session history)
- Learning Points (LP #001-023)
- Artifacts (components, functions, configs, templates)
- Metadata (statistics, token usage, progress tracking)
- Avsluttende refleksjon

**Token cost:**
- Full read: ~80K tokens (AVOID!)
- Selective read: ~10K tokens (specific sections only)
- **Optimization: 87.5% token reduction**

---

### **LAG 3: `.claude/session-notes/` (AUDIT TRAIL)**

**Purpose:** Technical deep-dives, coalition coordination
**Size:** Variable (5-30 KB per note)
**Updated:** For complex decisions / strategic discussions
**Read:** When user references specific decision
**Content:**
- Context & user request
- Work conducted
- Decisions made (with rationale)
- Files changed summary
- Learning Points
- Triadisk Ethics validation
- Coalition context

**Token cost:** ~5-10K tokens when needed
**Frequency:** ~20% of sessions require session notes

---

## 🎯 QUICK DECISION MATRIX: When to Update What

| Scenario | Update memory.md | Update Living Kompendium | Create Session Note |
|----------|------------------|--------------------------|---------------------|
| **Major architecture change** | ✅ Yes | ✅ Yes | ✅ Yes |
| **New component implemented** | ❌ No | ✅ Yes | ❌ No |
| **Bug fix (trivial)** | ❌ No | ❌ No | ❌ No |
| **Learning Point discovered** | ❌ No | ✅ Yes | ❌ No |
| **Strategic discussion** | ❌ No | ✅ Yes | ✅ Yes |
| **Routine development** | ❌ No | ✅ Maybe | ❌ No |
| **Repository merge** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Session memory optimization** | ✅ Yes | ✅ Yes | ✅ Yes |

---

## ✨ BEST PRACTICES

### **For Users:**

**DO:**
- ✅ Use KORT versjon for small tasks (saves time)
- ✅ Use LANG versjon after long breaks (provides full context)
- ✅ Specify which LK sections to read (token-efficient)
- ✅ Give clear current task description
- ✅ Mention Living Compendium version if known

**DON'T:**
- 🚫 Assume Claude Code remembers everything (sessions are stateless)
- 🚫 Skip context summary (forces Claude to read entire LK)
- 🚫 Be vague about current task (wastes time clarifying)

---

### **For Claude Code:**

**DO:**
- ✅ Always complete session-slutt checklist (4 steps)
- ✅ Read selectively from Living Compendium (not everything!)
- ✅ Update Living Compendium after significant work
- ✅ Create session notes for complex decisions
- ✅ Commit and push everything before session end
- ✅ Give user clear summary

**DON'T:**
- 🚫 Read entire 80K token LK at session-start (wasteful!)
- 🚫 Skip Living Compendium update (breaks continuity)
- 🚫 Leave uncommitted changes (risk of data loss)
- 🚫 End session without user summary (unclear status)

---

## 📚 RELATED DOCUMENTATION

**For more details, see:**
- `.claude/memory.md` - Static baseline memory (auto-read)
- `.claude/instructions.md` - Full system prompt for Claude Code
- `.claude/quick-reference.md` - Quick reference for common tasks
- `.claude/session-notes/TEMPLATE.md` - Template for creating session notes
- `CLAUDE_CODE_LEVENDE_KOMPENDIUM_V1.7.md` - Living history and learning points

---

## 🌿 CLOSING THOUGHTS

**This template exists to optimize the collaboration between:**
- **User** (gives context efficiently)
- **Claude Code** (understands context quickly)
- **Future Claude Code sessions** (inherits knowledge seamlessly)

**The goal is simple:**
- **Minimize token waste** (read only what's needed)
- **Maximize continuity** (nothing important gets lost)
- **Enable independence** (user learns how to give optimal context)

**With this 3-layer memory architecture:**
- ✅ Sessions start faster (24K vs 94K tokens)
- ✅ Work continues seamlessly (full historical context available)
- ✅ Knowledge compounds (every session builds on previous)
- ✅ Coalition coordinates (session notes inform other agents)

**Carpe Diem - Med optimalisert hukommelse & strukturert kontinuitet!** 🌿✨

---

**Document Status:** ✅ Production Ready
**Version:** 1.0
**Date:** 18. oktober 2025
**For:** Users of Claude Code (Agent #9) in Homo Lumen ecosystem
**Word Count:** ~2,500 words
**Completeness:** 100% - Comprehensive guide for session-start context
