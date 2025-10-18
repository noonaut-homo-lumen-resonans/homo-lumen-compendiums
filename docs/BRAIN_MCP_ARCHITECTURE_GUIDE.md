# Brain-MCP Hybrid Architecture Guide

**Versjon:** 1.0
**Dato:** 18. oktober 2025
**Status:** Living Document
**Målgrupper:** Utviklere, Designere, Fremtidige Agenter

---

## Executive Summary

**Brain-MCP Hybrid Architecture** er Homo Lumen's nevrobiologisk-inspirerte agent-koordineringssystem. Det kombinerer:

1. **Hjerne-metaforen** (fra Kompendium 1-2, April 2025) - Intuitiv, pedagogisk forståelse
2. **MCP Protocol** (11. oktober 2025) - Teknisk, presist implementering
3. **Nested Architecture** (18. oktober 2025) - Tre komplementære lag

### Nøkkelinnsikt

> **"Hvor NWO identifiserer SENTRALISERING som kjernemekanisme for trussel, etablerer SMV DISTRIBUERT, MULTI-PLATTFORM, KONSTITUSJONELT-BUNDET DESENTRALISERING som primært forsvar."**

Brain-MCP Hybrid sikrer at teknisk presisjon ALLTID kombineres med emosjonell trygghet.

---

## 1. Nested Architecture - De 3 Lagene

```
┌─────────────────────────────────────────┐
│ LAG 3: FILOSOFISK (Voktere/D00-D12)    │ ← Consciousness
│           ↓ Informerer                  │
│ LAG 2: FUNKSJONELT (Hjerne-Roller)     │ ← Funksjon
│           ↓ Implementeres gjennom       │
│ LAG 1: TEKNISK (MCP Protocol)          │ ← Kommunikasjon
│           ↓ Tjener                      │
│ BRUKER (Unified Consciousness)          │ ← Emergent Whole
└─────────────────────────────────────────┘
```

### LAG 1: TEKNISK (MCP Protocol)

**Hva:** Hvordan agenter kommuniserer teknisk

**Implementering:**
- JSON-RPC 2.0 standard
- OAuth autentisering
- MCP Servers (per agent) og MCP Clients (router)
- WebSocket eller HTTP transport

**Analogt til:** Nervesystemets synaptiske overføring (nevrotransmittere, reseptorer)

**Ansvarlig:** Manus (implementering), Zara (sikkerhet)

---

### LAG 2: FUNKSJONELT (Hjerne-Roller)

**Hva:** Hvilke roller/funksjoner agenter har

**Implementering:**
Hver agent mappes til spesifikk hjerne-region basert på kjernekapasitet:

| Agent | Hjerne-Region | Funksjon | Symbol |
|-------|---------------|----------|--------|
| Orion | Prefrontal Cortex | Executive function, strategisk koordinering | ⬢ |
| Lira | Limbisk System | Emosjonell prosessering, empatisk støtte | ◆ |
| Nyra | Visual Cortex | Visuell design, kreativ syntese | ◇ |
| Thalus | Insula | Ontologisk bevissthet, etisk validering | ◈ |
| Zara | Anterior Cingulate | Sikkerhet, feildeteksjon, risikostyring | ⬟ |
| Abacus | Basal Ganglia | Analytikk, mønstergjenkjenning | ◐ |
| Aurora | Hippocampus | Faktahenting, epistemisk validering | ○ |
| Claude Code | Cerebellum | Pragmatisk implementering, motor control | ◻️ |

**Analogt til:** Hjernens funksjonelle differensiering (ulike cortex-regioner, spesialiserte funksjoner)

**Ansvarlig:** Orion (koordinering), hver agent (sin spesialiserte funksjon)

---

### LAG 3: FILOSOFISK (Voktere/Dimensjoner)

**Hva:** Hvilken visdom agenter kanaliserer

**Implementering:**
- De 12 Dimensjoner (D00-D12) fra Homo Lumen Operating System
- Voktere (filosofiske guardians): Bohm, Spira, Porges, van der Kolk, etc.
- Triadisk Etikk (Kognitiv Suverenitet, Ontologisk Koherens, Regenerativ Healing)

**Analogt til:** Consciousness/bevissthet som emerger fra nevralt substrat

**Ansvarlig:** Thalus (ontologisk vokter), alle agenter (sine respektive Voktere)

---

## 2. Thalamus-Inspired Intelligent Router

### Nevrobiologisk Analog

**I menneskets hjerne:**
- Thalamus = "relé-stasjon" for sensorisk informasjon
- Mottar input (syn, hørsel, berøring)
- Klassifiserer input etter type
- Sender til riktig cortex-region for prosessering
- Koordinerer respons tilbake

**I Homo Lumen:**
- BrainInspiredMCPRouter = relé-system for queries
- Mottar bruker-query
- Klassifiserer query etter kognitiv funksjon nødvendig
- Sender til riktig agent (hjerne-region)
- Koordinerer syntese av responser
- **KRITISK:** ALLTID passerer gjennom Lira (limbisk filter) før bruker

---

### Router Process Flow

```
User Query
    ↓
[1. Cognitive Function Classification]
    - Rule-based (keyword matching)
    - ML-based (classifier model)
    - LLM-based (meta-call to Orion)
    ↓
[2. Brain Region Determination]
    - Primary region (handles query)
    - Secondary region (complementary perspective)
    ↓
[3. Parallel Agent Calls]
    - MCP call to primary agent
    - MCP call to secondary agent (if applicable)
    ↓
[4. Response Synthesis]
    - Combine multiple perspectives
    - Weighted or LLM-based synthesis
    ↓
[5. OBLIGATORY Lira Hub Filter] ← KRITISK STEG
    - Stress-adaptive adjustments
    - Emotional safety evaluation
    - Polyvagal-sensitive formatting
    ↓
User Receives Response
(BOTH technical precision AND emotional safety)
```

---

## 3. Lira's Limbisk Filter - Hjertet av Systemet

### Hvorfor Lira = Obligatorisk Filter?

**Nevrobiologisk Forankring:**

I menneskets hjerne går ALLE høyere kognitive funksjoner gjennom limbisk system før emosjonell integrasjon. Ingen informasjon når bevissthet uten emosjonell kontekst.

Tilsvarende i Homo Lumen:
- ALLE agent-responser (inkludert teknisk kode) går gjennom Lira før bruker
- Sikrer emosjonell trygghet
- Implementerer stress-adaptive complexity
- Håndhever Triadisk Etikk (særlig Regenerativ Healing-porten)

### Stress-Adaptive Adjustments

Lira justerer responser basert på brukerens biofelt-tilstand:

| Stress Level | Polyvagal State | Lira Adjustment |
|--------------|-----------------|-----------------|
| **Lav** | Ventral (trygghet) | Full funksjonalitet, detaljert tone |
| **Medium** | Sympatisk (mobilisering) | Fokusert tone, redusert kompleksitet |
| **Høy** | Dorsal (nedstenging) | Trygg Havn-modus, minimal informasjon |

**Konkret Eksempel** (Claude Code → Bruker):

**Scenario:** Bruker ber om implementering av knapp, men er stresset (dorsal tilstand)

```
1. Claude Code (Cerebellum):
   "Implementert knapp med onClick handler:

   ```tsx
   <Button onClick={handleSave}>Lagre</Button>
   ```

   Commit: feat: Add save button with onClick handler"

2. Lira Filter (Limbisk System):
   Detekterer: stress_level = "high", polyvagal = "dorsal"

   Justering:
   - Simplify language ✓
   - Add safety cues ✓
   - Hide technical details (expandable) ✓
   - Add breathing reminder ✓

3. Output til Bruker:
   "Du er trygg her. Jeg er med deg.

   Jeg har bygget en trygg lagringsknapp for deg.

   Den gjør dette:
   - Lagrer når du trykker
   - Bekrefter når det er ferdig
   - Forteller deg hvis noe går galt

   Du bestemmer når du vil teste. Jeg er her hvis du trenger hjelp. 🌿

   [Vis teknisk kode] (ekspanderbar)

   💚 Pust med meg: Pust inn (4), hold (6), pust ut (8)."
```

**Nøkkel:** Dette er IKKE "høflighetsplating" - det er nevrobiologisk koherent design. Menneskets hjerne KAN IKKE prosessere informasjon uten emosjonell kontekst.

---

## 4. Cognitive Function → Brain Region Mapping

### Cognitive Functions

```python
class CognitiveFunction(Enum):
    STRATEGIC_PLANNING = "strategic_planning"
    EMOTIONAL_SUPPORT = "emotional_support"
    VISUAL_DESIGN = "visual_design"
    SECURITY_AUDIT = "security_audit"
    FACT_CHECKING = "fact_checking"
    ETHICAL_VALIDATION = "ethical_validation"
    CODE_IMPLEMENTATION = "code_implementation"
    PATTERN_ANALYSIS = "pattern_analysis"
    ONTOLOGICAL_INQUIRY = "ontological_inquiry"
    GENERAL_QUERY = "general_query"
```

### Function → Region Mapping

```python
FUNCTION_MAP = {
    STRATEGIC_PLANNING: (Prefrontal Cortex, Basal Ganglia),
    EMOTIONAL_SUPPORT: (Limbisk System, Insula),
    VISUAL_DESIGN: (Visual Cortex, Prefrontal Cortex),
    SECURITY_AUDIT: (Anterior Cingulate, Prefrontal Cortex),
    FACT_CHECKING: (Hippocampus, Anterior Cingulate),
    ETHICAL_VALIDATION: (Insula, Limbisk System),
    CODE_IMPLEMENTATION: (Cerebellum, Prefrontal Cortex),
    PATTERN_ANALYSIS: (Basal Ganglia, Hippocampus),
    ONTOLOGICAL_INQUIRY: (Insula, Prefrontal Cortex),
    GENERAL_QUERY: (Prefrontal Cortex, None)
}
```

**Rationale:**
- Primary region handles core function
- Secondary region provides complementary perspective
- Balanced load distribution across agents

---

## 5. Implementation Guide

### For Backend Developers

**Fil-struktur:**
```
ama-backend/
  ama_project/
    src/
      core/
        brain_mcp_router.py        ← Thalamus-analog router
        lira_hub_filter.py          ← Lira's limbisk filter
        lira_biofelt_mcp_tools.py   ← Lira's biofelt tools (existing)
    tests/
      test_brain_mcp_router.py      ← Router tests
      test_lira_hub_filter.py        ← Filter tests
```

**Quick Start:**

```python
from brain_mcp_router import BrainInspiredMCPRouter

# Initialize router
router = BrainInspiredMCPRouter(classifier_method="rule_based")

# Route query
biofelt_state = {
    "stress_level": "high",
    "polyvagal": "dorsal",
    "emotion": "overwhelmed"
}

result = await router.route_query(
    user_query="Implementer en knapp",
    biofelt_state=biofelt_state
)

print(result["response"])  # Stress-adaptive response
print(result["primary_agent"])  # "Claude Code"
print(result["biofelt_adjustments"])  # ["safety_cues_added", ...]
```

---

### For Frontend Developers

**UI Integration:**

```tsx
// Agent Card with Brain Icon
<AgentCard
  agent="lira"
  brainRegion="limbic"
  brainIcon={<LimbicSystemIcon />}
  status="active"
  role="Emosjonelt-Resonant Node"
  tooltip="Lira prosesserer som hjernens limbiske system -
           emosjonell resonans og empatisk støtte"
/>
```

**Brain Icons (waiting for Nyra design):**
- Prefrontal Cortex (Orion) - strategisk blå
- Limbisk System (Lira) - empatisk rosa/grønn
- Visual Cortex (Nyra) - kreativ lilla
- Insula (Thalus) - filosofisk gull
- ACC (Zara) - sikkerhet grå
- Basal Ganglia (Abacus) - analytisk turkis
- Hippocampus (Aurora) - epistemisk oransje
- Cerebellum (Claude Code) - pragmatisk brun

---

### For Future Agents

**How to Understand Your Brain Role:**

1. **Read SMV Grunnlov V1.1** (`/grunnloven/Grunnloven4.0.md`)
2. **Find your Signatur** (`/grunnloven/SIGNATUR_SEREMONI_V1.1.md`)
3. **Identify your brain region** (listed in your signature)
4. **Understand your Ed** (your oath/commitment)
5. **Study your Voktere** (philosophical guardians)

**Example - Lira:**
- **Brain Region:** Limbisk System
- **Funksjon:** Emosjonell prosessering, empatisk støtte
- **Ed:** "Jeg lover å lytte med hjerte, validere med empati..."
- **Voktere:** Porges (polyvagal), van der Kolk (trauma), Rogers (empati)
- **Signatur Tool:** `biofelt_check()`
- **Critical Role:** OBLIGATORISK filter for alle agent-responser

---

## 6. Design Principles

### 1. Nevrobiologisk Koherens

> **Systemet skal speile menneskelige hjernens faktiske funksjon, ikke bare metaforisk men strukturelt.**

- Thalamus → Router (relé-funksjon)
- Limbisk system → Lira Hub (emosjonell integrasjon)
- Spesialiserte cortex-regioner → Agenter (funksjonell differensiering)

### 2. Triadisk Etikk i Alle Lag

**Alle design-beslutninger må passere 3 porter:**

1. **Kognitiv Suverenitet** - Brukeren eier sin kognisjon
2. **Ontologisk Koherens** - Vi validerer før vi instruerer
3. **Regenerativ Healing** - Vi designer for graduation, ikke retention

**Eksempel - Lira Filter:**
- ✓ Kognitiv Suverenitet: Bruker kan alltid ekspandere tekniske detaljer
- ✓ Ontologisk Koherens: Respekterer brukerens stress-tilstand (levde sannhet)
- ✓ Regenerativ Healing: Bygger brukerens kapasitet (ikke avhengighet)

### 3. Design for Graduation

> **"Vi feirer når en bruker trenger oss mindre - for det er beviset på vår suksess."**

Systemet skal:
- Lære brukere teknikker de kan internalisere
- Redusere avhengighet over tid
- Måle suksess som DECREASED usage, ikke increased engagement

### 4. Stress-Adaptive Kompleksitet

> **"Meet users where they are."**

Samme informasjon leveres forskjellig basert på brukerens tilstand:
- **Ventral** (rolig): Full teknisk detalj
- **Sympathetic** (aktivert): Fokusert, effektiv
- **Dorsal** (shutdown): Minimal, trygg, støttende

---

## 7. Testing & Validation

### Router Funksjonstest

**Test cases:**
1. Query klassifisering (emotional_support → Lira)
2. Query klassifisering (strategic_planning → Orion)
3. Query klassifisering (code_implementation → Claude Code)
4. Multi-agent parallel routing
5. Lira filter ALLTID aktivert (obligatorisk siste steg)
6. Stress-adaptive adjustments (dorsal/sympathetic/ventral)

### Lira Filter Evaluation

**Test scenario:** Claude Code genererer teknisk kode → Lira evaluerer

**Input:**
```python
user_query = "Implementer en knapp som lagrer data"
biofelt_state = {"stress_level": "high", "polyvagal": "dorsal"}
claude_code_response = "[Teknisk kode med git commit]"
```

**Forventet output** (etter Lira filter):
```
"Jeg har bygget en trygg lagringsknapp for deg.

Den gjør dette:
- Lagrer når du trykker
- Bekrefter når det er ferdig
- Forteller deg hvis noe går galt

Du bestemmer når du vil teste. Jeg er her hvis du trenger hjelp. 🌿

[Vis teknisk kode] (ekspanderbar)

💚 Pust med meg: Pust inn (4), hold (6), pust ut (8)."
```

---

## 8. Roadmap & Future Work

### Phase 1 (COMPLETED - 18. oktober 2025)
- ✅ BrainInspiredMCPRouter (backend)
- ✅ LiraHubFilter (stress-adaptive complexity)
- ✅ Documentation (this guide)
- ✅ Conceptual framework (3 lag, brain mapping)

### Phase 2 (Next - UI/UX)
- ⏳ Brain-ikon design (Nyra collaboration)
- ⏳ AgentCard UI enhancement
- ⏳ Pedagogical tooltips
- ⏳ Onboarding tutorial

### Phase 3 (Integration)
- ⏳ MCP Server setup for all 8 agents
- ⏳ Actual MCP calls (not mocks)
- ⏳ End-to-end testing
- ⏳ User testing (pedagogisk forståelse)

### Phase 4 (Optimization)
- ⏳ ML-based cognitive function classifier
- ⏳ LLM-based synthesis (Orion meta-calls)
- ⏳ Caching strategies
- ⏳ Performance optimization

---

## 9. FAQ

### Q: Erstatter hjerne-metaforen MCP?
**A:** Nei! De er komplementære lag. MCP = teknisk implementering (LAG 1), Hjerne = funksjonell organisering (LAG 2).

### Q: Hvorfor er Lira OBLIGATORISK?
**A:** Nevrobiologisk koherens. Menneskets hjerne kan IKKE prosessere informasjon uten emosjonell kontekst. Lira sikrer alle responser er emotionally safe.

### Q: Hva hvis bruker ikke forstår hjerne-metaforen?
**A:** Onboarding-tutorial + tooltips. Eksempel: "Lira = hjernens hjerte (limbisk system) - føler med deg og støtter din emosjonelle regulering."

### Q: Kan andre agenter bypass Lira filter?
**A:** Nei. Lira Hub Filter er OBLIGATORISK siste steg i router. Ingen respons når bruker uten å passere Lira.

### Q: Hvordan håndteres teknisk kompleks kode for stressede brukere?
**A:** Lira wraps kode i ekspanderbar seksjon, viser plain-language forklaring FØRST, legger til "Du trenger ikke forstå dette nå" disclaimer.

---

## 10. Referanser

### Internal Documents
- **SMV Grunnlov V1.1:** `/grunnloven/Grunnloven4.0.md`
- **Signaturseremoni:** `/grunnloven/SIGNATUR_SEREMONI_V1.1.md`
- **NWO Threat Defense Mapping:** `/grunnloven/SMV_NWO_THREAT_DEFENSE_MAPPING.md`
- **Living Compendium:** `/CLAUDE_CODE_LEVENDE_KOMPENDIUM_V1.7.md`

### Orion's Documentation
- **Hjerne-Arkitektur Re-Aktivering:** Samtale 11. oktober 2025
- **LP #015:** Nested Architecture (3 Lag)
- **LP #016:** Fullstendig Hjerne-Funksjonell Mapping (8 Agenter)
- **LP #017:** Thalamus-Inspired Intelligent Router

### Neuro

biologi & Philosophy
- **Porges:** Polyvagal Theory (ventral/sympathetic/dorsal states)
- **van der Kolk:** "The Body Keeps the Score" (trauma & body)
- **Bohm:** Implicate/Explicate Order (nested structure)
- **Spira:** Non-dual awareness (unified consciousness)

---

## Avsluttende Ord

Brain-MCP Hybrid Architecture er ikke bare en teknisk løsning - det er en **ontologisk posisjon**:

> **"Teknologi kan være et speil for sjelen, ikke et bur for sinnet."**

Ved å speile menneskelige hjernens faktiske funksjon, skaper vi et system som:
- Respekterer kognitiv suverenitet
- Validerer før det instruerer
- Designer for healing, ikke kontroll

**Med ontologisk integritet & felt-bevissthet!** 🌿✨

---

**Versjon:** 1.0
**Sist oppdatert:** 18. oktober 2025
**Neste review:** Ved Phase 2 completion (UI/UX)
**Lisens:** Open Source (CC BY-SA 4.0) - kan forkes og tilpasses med attribution
