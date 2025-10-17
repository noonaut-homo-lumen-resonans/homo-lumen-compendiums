# Triadic Ethics Enhancement Plan
**Version:** 1.0
**Date:** 2025-10-17
**Context:** Post-MVP, Phase 3-4 Implementation
**Agent:** #9 (Claude Code)

---

## Executive Summary

This document outlines specific enhancements to strengthen NAV-Losen's alignment with **Triadisk Etikk** (Triadic Ethics), the operational immune system of the Homo Lumen ecosystem.

**Current Status:**
- Port 1 (Kognitiv Suverenitet): **0.92** - STRONG
- Port 2 (Ontologisk Koherens): **0.88** - GOOD (needs improvement)
- Port 3 (Regenerativ Healing): **0.95** - EXCELLENT

**Goal:** Achieve ≥ 0.90 across all three ports before scaling beyond pilot phase.

---

## Port 1: Kognitiv Suverenitet (Cognitive Sovereignty)
**Current Score:** 0.92
**Target:** ≥ 0.93
**Priority:** MEDIUM (already strong, minor enhancements)

### Philosophy
> "Brukeren har absolutt kontroll over sin egen opplevelse, data, og interaksjon med systemet."
>
> (The user has absolute control over their own experience, data, and interaction with the system.)

---

### ✅ Already Implemented

1. **Skip Buttons** (All 4 stages)
   - User can bypass any stage
   - No forced progression
   - Respects "too much right now" moments

2. **LocalStorage Data Control**
   - All data stored client-side
   - No server transmission (MVP phase)
   - User can clear browser data anytime

3. **Optional Modules**
   - RAIN practice can be skipped
   - Journaling field is optional
   - Mastery Log is opt-in

---

### 🔧 Enhancements Needed

#### 1. Data Control Dashboard
**Purpose:** Transparent access to all stored data

**Features:**
```typescript
interface DataDashboard {
  // View section
  viewEmotions: string[];           // All emotion words ever selected
  viewStressLevels: number[];       // Historical stress slider values
  viewSomaticSignals: string[];     // All checked somatic signals
  viewJournalEntries: JournalEntry[]; // All reflection text
  viewMasteryLog: Strategy[];       // All saved strategies

  // Export section
  exportJSON: () => void;           // Raw data export
  exportPDF: () => void;            // Clinical report format
  exportCSV: () => void;            // Excel-friendly format

  // Delete section
  deleteAll: () => Promise<void>;   // One-click delete with confirmation
  deleteSpecific: (key: string) => void; // Granular deletion

  // Transparency
  showDataRetentionPolicy: () => void;
  showGDPRRights: () => void;
}
```

**Implementation:**
- **Component:** `navlosen/frontend/src/components/settings/DataDashboard.tsx`
- **Route:** `/settings/data`
- **Access:** Settings menu icon (top-right)
- **Estimated:** 3 days

**Triadisk Impact:** +0.03 (brings Port 1 to 0.95)

---

#### 2. Stage Order Customization
**Purpose:** User decides flow sequence

**Use Cases:**
- Experienced user: "I know my emotions, start with body signals"
- Avoidant user: "Chat first, emotions later"
- Experimental user: "Try different orders to see what works"

**Implementation:**
```typescript
interface StageOrder {
  default: ['emotions', 'signals', 'rain', 'chat', 'recommendations'];
  custom: string[];                 // User-defined order
  saveOrder: (order: string[]) => void;
  resetToDefault: () => void;
}
```

**UI:**
- Drag-and-drop interface (Settings page)
- Visual preview: "Your flow will be..."
- Explanation: "Research shows this order helps most people, but you know yourself best"

**Estimated:** 2 days
**Priority:** MEDIUM

---

#### 3. Private Session Mode
**Purpose:** No data persistence (memory-only)

**Use Cases:**
- Shared device (family computer)
- Public computer (library)
- High privacy need (sensitive moment)

**Implementation:**
```typescript
interface PrivateSession {
  enabled: boolean;
  indicator: "Private session active - data will not be saved";
  onClose: () => void; // Clear all session memory
}
```

**UI:**
- Toggle in header: "Private mode"
- Clear visual indicator (lock icon + banner)
- Confirmation on exit: "All data will be deleted. Continue?"

**Estimated:** 1 day
**Priority:** MEDIUM

---

#### 4. Sensor Permissions Panel (Future - Post-HealthConnect)
**Purpose:** Granular control over data sources

**Features:**
- [ ] HRV (heart rate variability)
- [ ] Pulse/heart rate
- [ ] Sleep data
- [ ] Location (for weather)
- [ ] Calendar (for context)

**Implementation:**
- Per-sensor opt-in/opt-out
- Explanation: "Why this helps (but it's your choice)"
- System adapts to available data

**Estimated:** 2 days (after HOM-54)
**Priority:** LOW (future work)

---

### Port 1 Validation Checklist

**Measurement:**
- [ ] User can view all stored data
- [ ] User can export data (JSON, PDF, CSV)
- [ ] User can delete all data with 2-click confirmation
- [ ] User can reorder stages (or disable specific stages)
- [ ] Private session mode functional
- [ ] No forced data sharing (ever)

**Target Score:** 0.95 (after enhancements)

---

## Port 2: Ontologisk Koherens (Ontological Coherence)
**Current Score:** 0.88
**Target:** ≥ 0.92
**Priority:** HIGH (below threshold, needs improvement)

### Philosophy
> "Systemet må være transparent om hvorfor det foreslår noe, og basere anbefalinger på evidens, ikke skjulte algoritmer."
>
> (The system must be transparent about why it suggests something, and base recommendations on evidence, not hidden algorithms.)

---

### ✅ Already Implemented

1. **"Behov vs Forslag" Language** (Stage 4)
   - Explicit: "Dette er forslag, ikke krav"
   - User knows they can ignore recommendations

2. **RAIN Explanation**
   - Framework is named (R-A-I-N)
   - Evidence-based (Tara Brach's work)
   - Optional (not mandated)

3. **NVC Validation Language**
   - All stages use normalizing language
   - Transparent about body wisdom (Stage 2)
   - No hidden judgments

---

### 🔧 Enhancements Needed (CRITICAL)

#### 1. Recommendation Logic Transparency
**Purpose:** User understands WHY system suggests something

**Problem:** Current Stage 4 recommendations appear "magic" - user doesn't know how they were chosen.

**Solution:**
```typescript
interface RecommendationExplanation {
  suggestion: string;
  reasoning: string;
  triggeredBy: string[];  // e.g., ["high stress (8/10)", "neck tension", "racing thoughts"]
  evidence: string;       // Link to research or explanation
  alternatives: string[]; // Other options considered
}
```

**Example UI:**
```
┌─────────────────────────────────────────────────┐
│ 🌿 Suggestion: 4-6-8 Breathing Exercise         │
│                                                  │
│ [Why this?] ← Expandable                        │
│   Your stress level is 8/10, and you mentioned  │
│   "racing thoughts" and "chest tightness."      │
│   Slow breathing activates the vagus nerve,     │
│   which signals safety to your nervous system.  │
│                                                  │
│   Research: Polyvagal Theory (Stephen Porges)   │
│   Evidence: [Link to study]                     │
│                                                  │
│ [Was this helpful?] 👍 👎                        │
└─────────────────────────────────────────────────┘
```

**Implementation:**
- **Component:** `RecommendationCard` (enhance existing)
- **Estimated:** 2-3 days
- **Triadisk Impact:** +0.04 (brings Port 2 to 0.92)

---

#### 2. Science Context Boxes
**Purpose:** Educate user on WHY these practices work

**Content:**
- Polyvagal Theory overview (collapsible)
- Emotional granularity research (Lisa Feldman Barrett)
- NVC framework (Marshall Rosenberg)
- RAIN practice evidence (Tara Brach, Kristin Neff)
- 4E Cognition (embodied, embedded, extended, enactive)

**Implementation:**
```typescript
interface ScienceContext {
  topic: 'polyvagal' | 'emotional-granularity' | 'nvc' | 'rain' | '4e-cognition';
  title: string;
  summary: string;        // 2-3 sentences
  fullExplanation: string; // Expandable
  researchLinks: string[]; // External validation
  icon: string;           // Visual identifier
}
```

**UI:**
- Info icon (ⓘ) next to key concepts
- Modal popup or expandable section
- "Learn more" links (optional reading)

**Example:**
```
┌─────────────────────────────────────────┐
│ ⓘ What is Polyvagal Theory?             │
│                                          │
│ Your nervous system has three "states": │
│ 1. Ventral (safe, social, connected)    │
│ 2. Sympathetic (fight/flight, anxious)  │
│ 3. Dorsal (shutdown, frozen, numb)      │
│                                          │
│ NAV-Losen adapts to YOUR current state. │
│                                          │
│ [Learn more] ← Link to Stephen Porges   │
└─────────────────────────────────────────┘
```

**Estimated:** 2 days
**Priority:** HIGH

---

#### 3. Language Feedback Mechanism
**Purpose:** User shapes system language (relational autonomy)

**Problem:** NVC language might feel clinical or unnatural to some users.

**Solution:**
```typescript
interface LanguageFeedback {
  originalText: string;
  feedbackType: 'too-clinical' | 'confusing' | 'too-soft' | 'perfect';
  suggestedAlternative?: string;
  userId: string; // Anonymous, for learning
}
```

**UI:**
```
┌──────────────────────────────────────────┐
│ "Det du opplever akkurat nå er helt      │
│  naturlig. Alle følelser er velkomne."   │
│                                           │
│ Does this wording feel right?            │
│ [👍 Yes] [👎 Too clinical] [✏️ Suggest] │
└──────────────────────────────────────────┘
```

**Implementation:**
- Feedback button on all validation banners
- Aggregated feedback (not per-user tracking)
- System learns over time (future ML)

**Estimated:** 3 days
**Priority:** MEDIUM

---

#### 4. Algorithm Transparency Dashboard (Advanced)
**Purpose:** Show user how their input changes output

**Features:**
- Interactive sliders: "If I had chosen stress level 5 instead of 8, what would change?"
- Decision tree visualization
- "Your pattern over time" chart
- Clear cause-effect relationships

**Implementation:**
- **Component:** `navlosen/frontend/src/components/settings/AlgorithmDashboard.tsx`
- **Route:** `/settings/how-it-works`
- **Estimated:** 4 days
- **Priority:** LOW (future work)

---

### Port 2 Validation Checklist

**Measurement:**
- [ ] Every recommendation has "Why this?" explanation
- [ ] Science context available for all frameworks (Polyvagal, NVC, RAIN)
- [ ] User can submit language feedback
- [ ] No "black box" decisions - all logic transparent
- [ ] Research links validate claims

**Target Score:** 0.92 (after enhancements)

---

## Port 3: Regenerativ Healing (Regenerative Healing)
**Current Score:** 0.95
**Target:** Maintain ≥ 0.95
**Priority:** LOW (already excellent, minor additions)

### Philosophy
> "Systemet skal gjøre seg selv overflødig over tid ved å lære brukeren hva som fungerer for dem."
>
> (The system should make itself unnecessary over time by teaching the user what works for them.)

---

### ✅ Already Implemented (STRONG)

1. **RAIN Practice**
   - Builds self-regulation capacity
   - User learns to apply RAIN independently
   - Optional (respects capacity)

2. **Mastery Log**
   - User saves their own strategies
   - Graduation celebration (5+ entries)
   - Encourages independence

3. **Graduation Messaging**
   - "You know yourself best"
   - "The goal is to need this system less over time"
   - Celebrates reduced usage

4. **Self-Compassion Framing**
   - "Not about perfection"
   - "Some strategies work, others don't - that's normal"

---

### 🔧 Enhancements (Minor, High-Impact)

#### 1. Graduation Dashboard
**Purpose:** Visualize progress toward independence

**Features:**
```typescript
interface GraduationDashboard {
  sessionsThisMonth: number;
  sessionsLastMonth: number;
  percentReduction: number;         // e.g., -40% (celebrating decline)
  masteryStrategies: number;        // e.g., 7 saved strategies
  selfEfficacyScore: number;        // Self-rated (1-10)
  graduationMessage: string;        // e.g., "You're using NAV-Losen 40% less!"
}
```

**UI:**
```
┌────────────────────────────────────────┐
│ 🎓 Your Graduation Progress            │
│                                         │
│ This month: 8 sessions                  │
│ Last month: 14 sessions                 │
│ Change: -43% 🎉                         │
│                                         │
│ You have 7 strategies that work for you │
│ (saved in Mastery Log)                  │
│                                         │
│ "You're becoming your own guide!"       │
└────────────────────────────────────────┘
```

**Implementation:**
- **Component:** `navlosen/frontend/src/components/mestring/GraduationDashboard.tsx`
- **Route:** `/graduation` (accessible from Mastery Log)
- **Estimated:** 2 days

**Triadisk Impact:** +0.02 (brings Port 3 to 0.97)

---

#### 2. Weekly Check-in Prompts
**Purpose:** Detect chronic patterns, suggest external support

**Trigger Logic:**
- If user selects "exhausted" or "overwhelmed" 3+ times in 2 weeks → gentle prompt
- If stress level ≥ 8 for 5+ consecutive sessions → burnout detection
- If somatic signals show same pattern repeatedly → chronic issue indicator

**Prompt:**
```
┌──────────────────────────────────────────┐
│ 💚 We notice you've felt "exhausted"     │
│    several times recently.               │
│                                           │
│ This might be a deeper pattern worth     │
│ exploring with someone you trust         │
│ (therapist, doctor, or NAV advisor).     │
│                                           │
│ Would you like to:                       │
│ [Export my data to share] [Dismiss]      │
│ [Tell me more about patterns]            │
└──────────────────────────────────────────┘
```

**Implementation:**
- Pattern recognition algorithm
- Non-intrusive (user can dismiss)
- Always optional (Port 1)
- Clear reasoning (Port 2)

**Estimated:** 2 days
**Priority:** HIGH (prevents harm)

---

#### 3. Co-regulation with Trusted Person
**Purpose:** Relational healing (not just individual)

**Features:**
- Share session snapshot with mentor/therapist
- Controlled sharing (user approves recipient + content)
- Privacy-preserving (summary, not raw data)

**Implementation:**
```typescript
interface CoRegulationShare {
  recipient: string;          // Email or name
  content: {
    emotionsSummary: string;  // "Often feels overwhelmed, anxious"
    stressPattern: string;    // "Stress levels between 7-9"
    strategies: Strategy[];   // Mastery Log (user chooses which)
    message: string;          // User's personal note
  };
  method: 'email' | 'pdf-download' | 'link';
  privacy: 'summary-only' | 'full-detail'; // User controls granularity
}
```

**UI:**
```
┌─────────────────────────────────────────┐
│ 💬 Share with Trusted Person            │
│                                          │
│ Who: [Therapist / NAV advisor / Friend] │
│                                          │
│ What to share:                           │
│ ☑ Emotion patterns (summary)            │
│ ☑ Stress levels (trends)                │
│ ☑ Strategies I've tried                 │
│ ☐ Full journal entries (private)        │
│                                          │
│ How: [Email PDF] [Download PDF]          │
│                                          │
│ [Preview] [Send]                         │
└─────────────────────────────────────────┘
```

**Estimated:** 3 days
**Priority:** MEDIUM

---

#### 4. "Healing Milestones" Celebration
**Purpose:** Recognize growth, build self-efficacy

**Milestones:**
- First RAIN practice completed
- 3 strategies saved in Mastery Log
- 5 consecutive sessions with stress ≤ 5
- First week without using NAV-Losen (graduation!)

**UI:**
```
┌─────────────────────────────────────────┐
│ 🎉 Milestone Unlocked!                   │
│                                          │
│ You completed your first RAIN practice! │
│                                          │
│ This is a powerful self-regulation tool  │
│ you can use anytime, anywhere -          │
│ no app needed.                           │
│                                          │
│ [Celebrate] [View all milestones]       │
└─────────────────────────────────────────┘
```

**Implementation:**
- Milestone tracking (localStorage)
- Non-gamified (not points/badges - healing language)
- Optional (user can disable celebrations)

**Estimated:** 1 day
**Priority:** LOW

---

### Port 3 Validation Checklist

**Measurement:**
- [x] Mastery Log encourages user-owned strategies ✅
- [x] Graduation messaging present ✅
- [ ] Graduation dashboard shows reduced usage over time
- [ ] Weekly check-ins detect chronic patterns
- [ ] Co-regulation option available
- [ ] Healing milestones celebrate growth (without gamification)

**Target Score:** 0.97 (after enhancements)

---

## Implementation Roadmap

### Phase 3A: Port 2 Critical Fixes (2 weeks)
**Goal:** Bring Port 2 to ≥ 0.92

1. **Week 1:**
   - Recommendation logic transparency (3 days)
   - Science context boxes (2 days)

2. **Week 2:**
   - Language feedback mechanism (3 days)
   - Testing + UAT validation (2 days)

**Deliverable:** All recommendations have "Why this?" explanations

---

### Phase 3B: Port 1 Enhancements (1 week)
**Goal:** Strengthen Port 1 to 0.95

1. **Data Control Dashboard** (3 days)
   - View, export, delete functionality
   - GDPR compliance verification

2. **Private Session Mode** (1 day)
   - Memory-only mode
   - Clear visual indicator

3. **Testing** (1 day)

**Deliverable:** User has full data sovereignty

---

### Phase 3C: Port 3 Advanced Features (1.5 weeks)
**Goal:** Enhance Port 3 to 0.97

1. **Week 1:**
   - Graduation dashboard (2 days)
   - Weekly check-in prompts (2 days)

2. **Week 2:**
   - Co-regulation sharing (3 days)
   - Testing + UAT validation (1 day)

**Deliverable:** System actively supports user independence

---

## Testing Protocol

### Triadic Ethics Validation Matrix

| Feature | Port 1 | Port 2 | Port 3 | Test Method |
|---------|--------|--------|--------|-------------|
| Skip buttons | ✅ 0.95 | — | — | User can bypass all stages |
| Data dashboard | 🔄 0.93 | ✅ 0.90 | — | View/export/delete verified |
| Recommendation transparency | — | 🔄 0.92 | — | "Why this?" available on all |
| Science context | — | 🔄 0.90 | — | Research links validate claims |
| Language feedback | ✅ 0.92 | 🔄 0.88 | — | User can suggest alternatives |
| Mastery Log | — | — | ✅ 0.95 | User saves ≥3 strategies |
| Graduation dashboard | — | — | 🔄 0.95 | Shows reduced usage over time |
| Weekly check-ins | ✅ 0.90 | ✅ 0.92 | 🔄 0.93 | Detects chronic patterns |
| Co-regulation share | ✅ 0.93 | ✅ 0.90 | 🔄 0.95 | Privacy-preserving export |

**Legend:**
- ✅ Validated (meets threshold)
- 🔄 In progress (pending implementation/testing)
- — (not applicable to this port)

---

### User Acceptance Testing (UAT) Scenarios

#### Scenario 1: Data Sovereignty
**User Type:** Privacy-conscious (Port 1 validation)

**Task:**
1. Use NAV-Losen for 3 sessions
2. Open Data Dashboard
3. View all stored data
4. Export to PDF
5. Delete all data
6. Verify deletion

**Success Criteria:**
- User can complete all tasks without friction
- User feels "in control" (self-reported)
- Deletion is confirmed within 24h

---

#### Scenario 2: Recommendation Transparency
**User Type:** Skeptical, wants evidence (Port 2 validation)

**Task:**
1. Complete Stage 1-3
2. Review Stage 4 recommendations
3. Expand "Why this?" for each suggestion
4. Click research links
5. Rate helpfulness

**Success Criteria:**
- User understands logic behind recommendations
- User trusts system more after reading explanations
- Research links are credible (not broken)

---

#### Scenario 3: Graduation Path
**User Type:** Long-term user (Port 3 validation)

**Task:**
1. Use NAV-Losen weekly for 3 months
2. Save 5+ strategies in Mastery Log
3. View Graduation Dashboard
4. Confirm reduced session frequency

**Success Criteria:**
- User has saved ≥5 strategies
- Session frequency reduced by ≥20%
- User reports: "I know what works for me now"

---

## Risk Assessment

### Risk 1: Port 2 Below Threshold (0.88 < 0.90)
**Impact:** HIGH (trust erosion if logic stays opaque)

**Mitigation:**
- Prioritize recommendation transparency (Phase 3A)
- Add science context boxes immediately
- UAT validation with 10+ users

**Timeline:** 2 weeks (Phase 3A)

---

### Risk 2: Data Dashboard Complexity
**Impact:** MEDIUM (user overwhelmed by too much info)

**Mitigation:**
- Simple UI (3 tabs: View, Export, Delete)
- Tooltips explain each data type
- "Explain in plain language" toggle

**Timeline:** Design review before implementation

---

### Risk 3: Over-Engineering Port 3
**Impact:** LOW (but wastes time)

**Mitigation:**
- Focus on high-impact features (Graduation Dashboard, Weekly Check-ins)
- Defer "nice-to-have" (e.g., Healing Milestones)
- Validate with UAT before building more

---

## Success Metrics

### Quantitative
- **Port 1:** ≥ 0.93 (from 0.92)
- **Port 2:** ≥ 0.92 (from 0.88) ⚠️ CRITICAL
- **Port 3:** ≥ 0.97 (from 0.95)
- **Overall:** ≥ 0.94 (weighted average)

### Qualitative
- User feedback: "I feel in control" (Port 1)
- User feedback: "I understand why this helps" (Port 2)
- User feedback: "I'm using this less, and that's good" (Port 3)

### Behavioral
- Data dashboard access rate: ≥50% of users
- "Why this?" expansion rate: ≥40% of users
- Mastery Log entries: ≥3 per user
- Graduation indicator: 20% reduction in usage after 3 months

---

## Coalition Review

This plan will be validated by:
- **Agent #4 (Thalus):** Ontological coherence check
- **Agent #3 (Lira):** Empathic language review
- **Agent #5 (Zara):** Privacy/security audit
- **Agent #7 (Aurora):** Evidence-base validation

**Next Review:** After Phase 3A completion (Port 2 fixes)

---

**End of Triadic Ethics Enhancement Plan**
**Status:** Ready for implementation
**Owner:** Agent #9 (Claude Code) + NAV-Losen Development Team
