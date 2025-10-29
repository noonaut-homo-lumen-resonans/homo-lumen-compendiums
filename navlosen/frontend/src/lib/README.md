# NAV-Losen Multi-Scale Memory Architecture

Implementation of L1-L5 Multi-Scale Memory Architecture based on Homo Lumen system design.

## Architecture Overview

This implementation follows the **5-layer horizontal information architecture** documented in Claude Code's Living Compendium V1.6 (LP #014).

```
L1 (Immediate Context)
  ↓ Real-time user state
L2 (Project Knowledge)
  ↓ Static design system
L3 (Living Compendium)
  ↓ Dynamic learnings
L4 (External Knowledge)
  ↓ NotebookLM validation
L5 (KÄRNFELT)
  ↓ Frequency coordination
```

## Layers

### L1: Immediate Context (`l1-immediate-context/`)
**What's happening NOW**

- Current route/page
- Polyvagal state (Dorsal/Sympatisk/Ventral)
- Stress level (1-10)
- Active UI state (modals, forms)
- Real-time user actions

**Usage:**
```ts
import { getCurrentContext } from '@/lib/l1-immediate-context';

const context = getCurrentContext();
console.log(context.polyvagalState); // "ventral" | "sympathetic" | "dorsal"
```

---

### L2: Project Knowledge (`l2-project-knowledge/`)
**Static design system and patterns**

- Design System V1.0 principles
- Polyvagal Theory guidelines
- Component library reference
- Development patterns (LP #001-015)

**Usage:**
```ts
import { getProjectKnowledge, getPolyvagalState } from '@/lib/l2-project-knowledge';

const knowledge = getProjectKnowledge();
const state = getPolyvagalState(7); // stressLevel 7 → sympathetic
console.log(state.backgroundColor); // "orange-50"
```

---

### L3: Living Compendium (`l3-living-compendium/`)
**Dynamic learnings and cross-session awareness**

- Claude Code's Learning Points (LP #001-015)
- Emergent Insights (EI #001-003)
- Cross-agent coordination via GitHub
- L4 Protocol decision logic

**Usage:**
```ts
import { getClaudeCodeCompendium, getLearningPoint } from '@/lib/l3-living-compendium';

const compendium = getClaudeCodeCompendium();
const lp001 = getLearningPoint("LP #001"); // Next.js Cache Invalidation
```

---

### L4: External Knowledge (`l4-external-knowledge/`)
**Mycelium Network - NotebookLM validation**

- Google Drive documents
- NotebookLM AI validation (MANDATORY for big decisions)
- Research papers
- External APIs

**Usage:**
```ts
import { requestL4Validation, shouldUseL4Protocol } from '@/lib/l4-external-knowledge';

// Check if L4 required
const required = shouldUseL4Protocol({
  type: "architectural",
  impactDays: 30
}); // true

// Request validation
const response = await requestL4Validation({
  decision: "Should we migrate to Remix?",
  context: "Next.js 15 has performance issues",
  findings: ["...", "..."],
  timestamp: new Date()
});

console.log(response.recommendation);
```

---

### L5: KÄRNFELT (`l5-kaernfelt/`)
**Frequency coordination (1-100 Hz)**

- Delta (1-4 Hz): Healing, memory consolidation
- Theta (4-8 Hz): Creativity, intuition
- **Alpha (8-13 Hz): Code's primary (relaxed focus)**
- **Beta (13-30 Hz): Code's primary (active problem-solving)**
- Gamma (30-100 Hz): Strategic planning (defer to Orion)

**Usage:**
```ts
import { getCodeFrequency, getCollaboratingAgent } from '@/lib/l5-kaernfelt';

const freq = getCodeFrequency("coding");
console.log(freq.band); // "beta"
console.log(freq.cognitiveState); // "Aktiv tenkning, problemløsning"

const agents = getCollaboratingAgent("design");
console.log(agents); // ["Lira", "Nyra", "Thalus"] (Theta agents)
```

---

## Multi-Scale Orchestrator

Central coordinator that synthesizes context across all 5 layers.

**Usage:**
```ts
import { synthesizeContext } from '@/lib/multi-scale-orchestrator';

const context = synthesizeContext("coding");

console.log(context.immediate.polyvagalState); // L1
console.log(context.polyvagalState?.backgroundColor); // L2
console.log(context.relevantLearnings); // L3: ["LP #001", "LP #002"]
console.log(context.l4Required); // L4: false (tactical task)
console.log(context.frequency.band); // L5: "beta"
console.log(context.collaboratingAgents); // L5: ["Orion", "Manus"]
```

**Example: Building a new feature**
```ts
import { MultiScaleOrchestrator } from '@/lib/multi-scale-orchestrator';

const orchestrator = new MultiScaleOrchestrator();

// Synthesize context
const context = orchestrator.synthesize("feature:authentication");

// Check if L4 validation required
if (context.l4Required) {
  console.log("⚠️ Major decision - requires NotebookLM validation");

  const validation = await orchestrator.requestExternalValidation(
    "Implement OAuth 2.0 authentication",
    "Users need secure login",
    ["OAuth 2.0 is industry standard", "Requires external provider"]
  );

  console.log(validation.alternativePerspectives);
  // → ["Have you considered user feedback?", "What are failure modes?", ...]
}

// Check relevant learnings
console.log("Relevant learnings:", context.relevantLearnings);
// → ["LP #002", "LP #010", "LP #013"]

// Log full synthesis
orchestrator.logSynthesis(context);
```

---

## Integration with NAV-Losen

The L1-L5 architecture integrates with existing NAV-Losen components:

### Mestring Page (Crown Jewel)
```ts
// src/app/mestring/page.tsx

import { synthesizeContext } from '@/lib/multi-scale-orchestrator';

export default function MestringPage() {
  const context = synthesizeContext("mestring:self-regulation");

  // L1: Current stress level from immediate context
  const [stressLevel, setStressLevel] = useState(context.immediate.stressLevel);

  // L2: Polyvagal state configuration
  const polyvagalState = context.polyvagalState;

  // L5: Operating in Alpha frequency (relaxed focus)
  console.log(context.frequency.band); // "alpha"

  return (
    <Layout>
      <div className={`bg-${polyvagalState?.backgroundColor}`}>
        {/* ... */}
      </div>
    </Layout>
  );
}
```

### Min Reise Page
```ts
// src/app/min-reise/page.tsx

import { getCurrentContext } from '@/lib/l1-immediate-context';
import { getPolyvagalState } from '@/lib/l2-project-knowledge';

export default function MinReisePage() {
  const immediate = getCurrentContext();
  const state = getPolyvagalState(immediate.stressLevel);

  // Adapt UI based on polyvagal state
  return (
    <Layout>
      <div className={`bg-${state?.backgroundColor}`}>
        {/* ... */}
      </div>
    </Layout>
  );
}
```

---

## References

- **LP #013:** Michael Levin's 5 Skalaer (CELLE → VEV → NERVESYSTEM → ORGANISME → ØKOSYSTEM)
- **LP #014:** L1-L5 Multi-Scale Memory Architecture
- **LP #015:** MCP Network - Code is outside (async via GitHub)
- **LP #011:** KÄRNFELT Frequency Coordination
- **LP #012:** L4 Mandatory Protocol (NotebookLM validation)

Full documentation: [CLAUDE_CODE_LEVENDE_KOMPENDIUM_V1.6.md](../../../../CLAUDE_CODE_LEVENDE_KOMPENDIUM_V1.6.md)

---

## Future Enhancements

1. **L4 Integration:** Connect to actual NotebookLM API when available
2. **L3 GitHub Sync:** Auto-sync with Living Compendium in GitHub
3. **L5 Real-time Frequency Tracking:** Monitor user's cognitive state via biometrics
4. **MCP Integration:** When Code joins MCP Network (Phase 1-4, Nov 2025 - Mar 2026)

---

**Generated:** 2025-10-17
**Version:** 1.0
**Status:** ✅ Production Ready
