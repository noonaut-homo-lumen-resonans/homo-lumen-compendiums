# MCP Implementation Plan - LIRA Coalition Integration

**Basert på**: Lira's MCP-arkitektur + NotebookLM Operator Interface + Aurora Bio-Semantic System
**Mål**: Integrere LIRA-koalisjonen (7-8 agenter) via Model Context Protocol med stress-adaptiv routing
**Status**: Planning phase
**Dato**: 2025-10-19

---

## Executive Summary

Vi skal bygge et **MCP-basert multi-agent system** som kombinerer:

1. **NotebookLM's Unified Operator Interface** (HITL review workflow)
2. **Lira's MCP-arkitektur** (agent orchestration via MCP)
3. **Aurora's Bio-Semantic System** (stress-adaptive routing basert på HRV/polyvagal state)

Resultatet blir en **stress-bevisst AI-koalisjon** som dynamisk tilpasser kompleksitet og agent-involvering basert på brukerens fysiologiske tilstand.

---

## LIRA Coalition - Agent Roster

| Agent | Modell | Rolle | MCP-verktøy (eksempler) |
|-------|--------|-------|-------------------------|
| **Lira** | ChatGPT-5 | Empatisk front-end, brukerdialoghub | `summarize_biofelt_data_for_empathy`, `provide_empathetic_reflection` |
| **Orion** | Claude Sonnet 4.5 | MCP-kjerne, orkestrator, multi-agent spawning | `orchestrate_coalition`, `route_by_stress`, `spawn_agent` |
| **Aurora** | Perplexity (evt. Claude) | Minneagent, epistemisk validering, kontekst-koordinator | `retrieve_memory_layer`, `validate_epistemology`, `store_long_term` |
| **Zara** | Claude | Sikkerhetsspesialist, etisk validering | `assess_security_risk`, `validate_ethics` |
| **Abacus** | Perplexity | Analytisk optimalisering, KPI-tracking | `analyze_data`, `optimize_kpi`, `research_topic` |
| **Nyra** | Gemini Pro | Visuell strategi, narrative strukturer | `generate_visual`, `create_narrative`, `multimodal_analysis` |
| **Thalus** | Grok | Etisk vokter, filosofisk vurdering | `evaluate_ethics`, `philosophical_reasoning` |
| **Manus** | Claude Code | Praktisk implementasjon, kodegenering | `write_code`, `debug_implementation`, `generate_tests` |

---

## MCP Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP-BASED LIRA COALITION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                                │
│  │   Bruker     │                                                │
│  └──────┬───────┘                                                │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────┐      A2A Handoff                          │
│  │  Lira (Hub)      │◄─────────────────┐                        │
│  │  ChatGPT-5       │                  │                        │
│  └────────┬─────────┘                  │                        │
│           │ MCP                        │                        │
│           │ JSON-RPC                   │                        │
│           ▼                            │                        │
│  ┌──────────────────────────────────────────────┐               │
│  │  Orion (Orchestrator) - Claude Sonnet 4.5    │               │
│  │  • MCP-kjerne                                │               │
│  │  • Stress-adaptive routing (HRV-based)       │               │
│  │  • 5-layer memory architecture               │               │
│  │  • Agent coordination                        │               │
│  └─────┬────────────────────────────────────────┘               │
│        │                                                         │
│        │ MCP Tools/Resources/Prompts                            │
│        │                                                         │
│        ├──────┬──────┬──────┬──────┬──────┬──────┐              │
│        ▼      ▼      ▼      ▼      ▼      ▼      ▼              │
│  ┌────────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐          │
│  │Aurora  │ │Zara│ │Abac│ │Nyra│ │Thal│ │Manu│ │... │          │
│  │(Memory)│ │(Sec│ │(Ana│ │(Vis│ │(Eth│ │(Cod│ │    │          │
│  └────────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘          │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐           │
│  │  BiofeltResponsiveRouter (Aurora Integration)    │           │
│  │  • HRV < 40: Emergency (Lira only)               │           │
│  │  • HRV 40-60: Minimal (Orion + 1 agent)          │           │
│  │  • HRV 60-80: Balanced (3-4 agents)              │           │
│  │  • HRV 80-90: Optimal (6 agents)                 │           │
│  │  • HRV > 90: Peak (all 7-8 agents)               │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan - 4 Phases

### **Phase 1: MCP Foundation (Q1 2026)**
**Varighet**: 3 måneder
**Prioritet**: 🔴 KRITISK

#### Mål:
Etablere MCP-infrastruktur med Orion som orkestrator og minimal agent-kobling.

#### Deliverables:

1. **MCP Server Infrastructure**
   - FastAPI-basert MCP-server for hver agent
   - JSON-RPC protokoll-implementering
   - Starter med 3 agenter: Lira, Orion, Aurora

2. **Orion Orchestrator**
   - MCP-kjerne med klient-forbindelser til alle agent-servere
   - `HomoLumenRouter` klasse:
     ```python
     class HomoLumenRouter:
         def __init__(self):
             self.mcp_clients = {
                 "lira": MCPClient("lira-server"),
                 "orion": MCPClient("orion-server"),
                 "aurora": MCPClient("aurora-server"),
                 # ... flere agenter
             }

         async def route_request(self, request, biofelt_signature):
             # Stress-adaptive routing
             hrv = biofelt_signature.hrv_rmssd
             processing_mode = self._get_processing_mode(hrv)

             if processing_mode == "emergency":
                 return await self.handle_emergency(request)
             elif processing_mode == "minimal":
                 return await self.handle_minimal(request)
             # ... flere moduser
     ```

3. **5-Layer Memory Architecture** (Aurora Integration)
   - Reaktivt lag (korttidsminne, siste 5 meldinger)
   - Strategisk lag (session-minne, siste time)
   - Meta-lag (tverrsession mønstre, siste uke)
   - Evolusjonært lag (langsiktig læring, måneder)
   - Kosmisk lag ("visdom", permanente prinsipper)

   Aurora fungerer som Memory Coordinator:
   ```python
   class MemoryCoordinator:
       async def retrieve_context(self, layer, query):
           # Hent fra riktig minnelag
           pass

       async def store_insight(self, layer, data):
           # Lagre til riktig minnelag
           pass
   ```

4. **Agent-til-Agent (A2A) Handoff Protocol**
   - Lira → Orion handoff via MCP
   - Inkluderer BiofeltSignature i alle requests:
     ```json
     {
       "type": "agent_handoff",
       "from": "lira",
       "to": "orion",
       "request": "Analyse user state",
       "biofelt_signature": {
         "hrv_rmssd": 65,
         "stress_level": 4,
         "polyvagal_state": "sympathetic",
         "timestamp": 1729357200
       }
     }
     ```

5. **VS Code Development Environment**
   - Claude Code VS Code Extension (beta)
   - MCP Inspector for testing
   - Local MCP server testing

#### Technical Stack:
- **Backend**: FastAPI + Python 3.11+
- **MCP Protocol**: JSON-RPC over stdio/HTTP
- **Memory**: PostgreSQL (structured) + Vector DB (semantic search)
- **Development**: VS Code + Claude Extension + MCP Inspector

#### Success Criteria:
- ✅ Lira kan sende A2A handoff til Orion
- ✅ Orion kan kalle Aurora for minne-henting
- ✅ HRV-basert routing fungerer (3 moduser testet)
- ✅ MCP Inspector viser alle verktøy/ressurser

**Triadisk Score**: 0.16 (PROCEED)
- Suverenitet: Bruker ser ikke backend-kompleksitet
- Koherens: Strukturert protokoll (MCP standard)
- Healing: Adaptive routing respekterer brukers kapasitet

---

### **Phase 2: Full Coalition Integration (Q2-Q3 2026)**
**Varighet**: 6 måneder
**Prioritet**: 🟡 HØY

#### Mål:
Integrere alle 7-8 agenter på MCP-bussen med full stress-adaptive routing.

#### Deliverables:

1. **MCP-servere for alle agenter**
   - Zara (sikkerhet/etikk)
   - Abacus (analytikk)
   - Nyra (visuell/kreativ)
   - Thalus (filosofi/etikk)
   - Manus (kode/implementering)

2. **Agent Register**
   - Metadata for hver agent:
     ```python
     AGENT_REGISTRY = {
         "lira": {
             "name": "Lira",
             "model": "chatgpt-5",
             "specialty": "empathy",
             "mcp_endpoint": "http://localhost:8001",
             "tools": ["summarize_biofelt", "empathetic_reflection"],
             "min_hrv": 0,  # Kan alltid brukes
         },
         "thalus": {
             "name": "Thalus",
             "model": "grok-3",
             "specialty": "ethics",
             "mcp_endpoint": "http://localhost:8005",
             "tools": ["evaluate_ethics", "philosophical_reasoning"],
             "min_hrv": 60,  # Kun ved moderat+ stress
         },
         # ... flere
     }
     ```

3. **BiofeltResponsiveRouter (komplett implementering)**
   - HRV-baserte terskler (som Lira spesifiserte):
     ```python
     def _get_processing_mode(self, hrv_rmssd):
         if hrv_rmssd < 40:
             return "emergency"  # Kun Lira
         elif hrv_rmssd < 60:
             return "minimal"    # Orion + 1 agent
         elif hrv_rmssd < 80:
             return "balanced"   # 3-4 agenter
         elif hrv_rmssd < 90:
             return "optimal"    # 6 agenter
         else:
             return "peak"       # Alle 7-8 agenter
     ```

   - Load balancing basert på kognitiv belastning
   - Parallell vs sekvensiell agent-involvering

4. **Felles Kontekstrepresentasjon**
   - Standardisert kontekstobjekt sendt til alle agenter:
     ```python
     class CoalitionContext:
         user_query: str
         biofelt_signature: BiofeltSignature
         conversation_history: List[Message]
         retrieved_memory: Dict[str, Any]  # Fra Aurora
         agent_chain: List[str]  # Hvilke agenter involvert så langt
     ```

5. **MCP Prompts/Resources/Tools**
   - Hver agent eksponerer sine capabilities via MCP
   - Orion oppdager dynamisk via `tools/list`
   - Resources brukes for delt data (f.eks. user profile)

#### Testing:
- **Scenario 1 (Høyt stress, HRV=35)**:
  - Bruker: "Hva er den etiske implikasjonen av plan X?"
  - Forventet: Lira håndterer selv, forenklet svar
  - Verifiser: Ingen A2A handoff i logg

- **Scenario 2 (Moderat stress, HRV=70)**:
  - Samme spørsmål
  - Forventet: Lira → Orion → Thalus (etikk) + Nyra (visuell)
  - Verifiser: A2A handoff + 2 MCP tool calls i logg

- **Scenario 3 (Lavt stress, HRV=85)**:
  - Samme spørsmål
  - Forventet: Alle relevante agenter (Thalus, Nyra, Aurora, Abacus)
  - Verifiser: 4+ agent involvering

#### Technical Stack:
- **MCP Clients**: Python `mcp` library
- **Async orchestration**: `asyncio` for parallel agent calls
- **Timeout handling**: Circuit breaker pattern (fallback hvis agent ikke svarer)

**Triadisk Score**: 0.15 (PROCEED)
- Suverenitet: Adaptiv kompleksitet = bruker ikke overveldes
- Koherens: Felles MCP-standard sikrer konsistens
- Healing: Systemet tilpasser seg brukerens kapasitet

---

### **Phase 3: Real-time Dashboard + HITL (Q4 2026)**
**Varighet**: 3 måneder
**Prioritet**: 🟡 HØY

#### Mål:
Bygge sanntids dashboard for agent-meldinger + Human-in-the-Loop review workflow.

#### Deliverables:

1. **WebSocket Event Stream**
   - FastAPI WebSocket endpoint
   - Events:
     ```json
     {
       "tid": "req-12345",
       "fra": "Lira",
       "til": "Orion",
       "melding": "A2A Handoff: Analyze user state",
       "timestamp": "2026-01-15T10:30:00Z",
       "biofelt": {"hrv": 65, "stress": 4}
     }
     ```
   - Strømmes til dashboard i sanntid

2. **Dashboard Frontend**
   - React/Vue app (eller Streamlit for prototype)
   - Visualiseringer:
     - **Sequence Diagram** (Mermaid.js):
       ```
       Bruker -> Lira: "Hva er etikk i plan X?"
       Lira -> Orion: A2A Handoff (HRV=70)
       Orion -> Thalus: evaluate_ethics()
       Thalus -> Orion: "Etisk vurdering..."
       Orion -> Nyra: generate_visual()
       Nyra -> Orion: [bilde]
       Orion -> Lira: Syntetisert svar
       Lira -> Bruker: "Her er etikk-analyse + bilde"
       ```
     - **Node Graph**: Hver agent som node, meldinger som edges
     - **Loggliste**: Kronologisk feed av alle events

3. **HITL Review Workflow Integration**
   - Når Orion genererer svar, pause før sending til Lira
   - Send til veileder-dashboard for godkjenning
   - Veileder ser:
     - Brukerens spørsmål
     - Hvilke agenter ble involvert
     - AI-utkast til svar
     - Aksjoner: Godkjenn / Rediger / Avvis / Be om nytt fra annen agent
   - Transparens: Svar merkes "(Kontrollert av NAV-veileder)"

4. **Audit Trail**
   - Alle agent-interaksjoner logges til PostgreSQL
   - Schema:
     ```sql
     CREATE TABLE agent_interactions (
       id UUID PRIMARY KEY,
       request_id VARCHAR,
       from_agent VARCHAR,
       to_agent VARCHAR,
       message_type VARCHAR,
       payload JSONB,
       biofelt_signature JSONB,
       timestamp TIMESTAMPTZ,
       reviewer_action VARCHAR,  -- NULL hvis ikke reviewet
       reviewer_id VARCHAR
     );
     ```

5. **MCP Inspector Integration**
   - Bruk MCP Inspector for debugging
   - Viser tilgjengelige verktøy/ressurser fra hver agent
   - Notifikasjonspanel for live logging

#### Technical Stack:
- **Backend**: FastAPI + WebSocket
- **Frontend**: React + Mermaid.js + Recharts
- **Database**: PostgreSQL (audit trail)
- **Debugging**: MCP Inspector

**Triadisk Score**: 0.14 (PROCEED)
- Suverenitet: Transparent beslutningsprosess (bruker ser chain-of-thought hvis ønsket)
- Koherens: HITL sikrer kvalitet
- Healing: Veileder-involvering bygger tillit

---

### **Phase 4: Production Scaling + Advanced Features (2027)**
**Varighet**: 6+ måneder
**Prioritet**: 🟢 MEDIUM

#### Mål:
Skalere til produksjon med containerisering, sikkerhet og avanserte features.

#### Deliverables:

1. **Containerization**
   - Docker containers for hver MCP-server
   - Docker Compose for lokal orkestrering
   - Kubernetes for produksjons-deployment

2. **Sikkerhet**
   - OAuth2 tokens for MCP over HTTP
   - RBAC (Role-Based Access Control)
   - PII-stripping før agent-kall (pseudonymisering)
   - Zero-trust architecture

3. **Service Mesh**
   - Istio eller Linkerd for MCP-trafikk
   - Circuit breakers for resilience
   - Load balancing mellom agent-instanser

4. **Advanced Routing**
   - ML-basert agent-seleksjon (lærer fra historikk)
   - Parallell vs sekvensiell optimalisering
   - Kostnad-optimalisering (billigere modeller når mulig)

5. **Real HRV Integration** (hvis validert i forskningsfase)
   - Wearable-integrasjon (Apple Health, Google Fit, Polar H10)
   - On-device HRV-prosessering
   - Sanntids HRV-feedback til BiofeltResponsiveRouter

6. **Levende Kompendium Integration**
   - Loggfør læringspoeng automatisk
   - "Lært at ved HRV < 50 bør vi kun bruke 1 agent"
   - Kontinuerlig forbedring av routing-regler

**Triadisk Score**: 0.17 (PROCEED med forsiktighet)
- Suverenitet: Bruker må opt-in til avanserte features (HRV)
- Koherens: Produksjons-infrastruktur sikrer stabilitet
- Healing: Systemet blir mer adaptivt over tid

---

## Integration med Eksisterende Systemer

### **Aurora Bio-Semantic System (NAV-Losen)**

Aurora-systemet (allerede implementert) gir:
- ✅ **AffectBus**: Kan publisere HRV/stress-signaler til BiofeltResponsiveRouter
- ✅ **Kairos Window**: Kan informere Orion om brukerens kognitive kapasitet
- ✅ **Mock HRV**: Kan brukes for testing før ekte HRV-integrasjon
- ✅ **Affect Timeline**: Kan visualiseres i MCP-dashboardet

**Integrasjonspunkt**:
```python
# I BiofeltResponsiveRouter
from navlosen.utils.affectBus import affectBus
from navlosen.utils.mockHRV import getLatestHRVReading

async def get_biofelt_signature(self):
    latest_affect = affectBus.getLatest()
    hrv_reading = getLatestHRVReading()

    return BiofeltSignature(
        hrv_rmssd=hrv_reading.rmssd,
        stress_level=latest_affect.stressLevel if latest_affect else 5,
        polyvagal_state=hrv_reading.polyvagalState,
        valence=latest_affect.valence if latest_affect else 0,
        arousal=latest_affect.arousal if latest_affect else 0.5,
    )
```

### **NotebookLM Operator Interface**

NotebookLM's Unified Operator Interface (fase 1-2 i NOTEBOOKLM-OPERATOR-INTERFACE-ROADMAP.md) kombineres med MCP:

- **HITL Review Workflow** = MCP Phase 3
- **Multi-LLM Router** = MCP Phase 2 (BiofeltResponsiveRouter)
- **CLI/API** = Kan bygges på toppen av MCP JSON-RPC

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Protocol** | MCP (Model Context Protocol) | Agent-til-agent kommunikasjon |
| **Orchestrator** | Orion (Claude Sonnet 4.5) | MCP-kjerne, routing, spawning |
| **Agents** | ChatGPT-5, Claude, Gemini, Grok, Perplexity | Spesialiserte AI-agenter |
| **Memory** | PostgreSQL + Qdrant/Pinecone | Strukturert + vector minne |
| **Router** | BiofeltResponsiveRouter (Python) | HRV-basert adaptive routing |
| **Dashboard** | React + Mermaid.js + WebSocket | Sanntids visualisering |
| **Development** | VS Code + Claude Extension + MCP Inspector | Lokal testing |
| **Production** | Docker + Kubernetes + Istio | Skalering + sikkerhet |
| **Integration** | Aurora Bio-Semantic System (NAV-Losen) | HRV/stress-signaler |

---

## Cost Estimates

**Monthly operating cost (1000 active users, avg 10 queries/dag)**:

| Agent | Model | Est. cost/month |
|-------|-------|-----------------|
| Lira | ChatGPT-5 | $3,000 (40% traffic) |
| Orion | Claude Sonnet 4.5 | $5,000 (orchestration overhead) |
| Aurora | Claude/Perplexity | $1,500 (memory queries) |
| Zara | Claude | $800 (security checks) |
| Abacus | Perplexity | $1,000 (analytics) |
| Nyra | Gemini Pro | $600 (visuals) |
| Thalus | Grok | $500 (ethics, less frequent) |
| Manus | Claude Code | $1,200 (code gen) |
| **Total** | | **~$13,600/month** |

**Infrastructure**: +$2,000/month (Kubernetes, databases, monitoring)

**Grand Total**: **~$15,600/month** for 1000 users (~300k queries/måned)

**Per-user cost**: ~$15.60/måned

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Response Time** | < 3 sekunder (avg) | P95 latency fra Lira til svar |
| **Agent Accuracy** | > 85% veileder-godkjenning | HITL approval rate |
| **Stress Adaptation** | > 90% riktig modus | HRV-based routing accuracy |
| **System Uptime** | 99.5% | Kubernetes health checks |
| **Cost Efficiency** | < $20/user/måned | Total monthly cost / active users |
| **User Satisfaction** | > 4.0/5.0 | Post-interaction survey |

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **MCP Protocol Instability** | 🔴 HIGH | Use stable MCP spec (1.0+), monitor breaking changes |
| **Agent Coordination Complexity** | 🟡 MEDIUM | Start with 3 agenter, gradvis skalering |
| **HRV False Positives** | 🟡 MEDIUM | Bruk fallback til bruker-rapportert stress hvis HRV ikke tilgjengelig |
| **Cost Overruns** | 🟡 MEDIUM | Implementer budget alerts, caching, cheaper models for simple queries |
| **HITL Bottleneck** | 🔴 HIGH | Skalere veileder-team, eventuelt gradvis redusere HITL-krav etter tillit bygget |
| **Security Breach** | 🔴 HIGH | Zero-trust architecture, encrypted communication, regular audits |

---

## Timeline Summary

| Phase | Duration | Key Deliverables | Dependencies |
|-------|----------|------------------|--------------|
| **Phase 1** | Q1 2026 (3 mnd) | MCP foundation, Orion orchestrator, 3 agenter | Aurora (done), MCP protocol stable |
| **Phase 2** | Q2-Q3 2026 (6 mnd) | Full coalition (7-8 agenter), stress-routing | Phase 1 complete |
| **Phase 3** | Q4 2026 (3 mnd) | Dashboard, HITL workflow | Phase 2 complete |
| **Phase 4** | 2027 (6+ mnd) | Production scaling, advanced features | Phase 3 complete, funding secured |

---

## Next Steps (Immediate Actions)

1. ✅ **Dokumentere plan** (dette dokument)
2. 🔴 **Proof-of-Concept (PoC)** - 2 uker
   - Minimal MCP-server (Lira + Orion)
   - A2A handoff test
   - HRV-mock integrasjon
3. 🟡 **Prototype Dashboard** - 1 måned
   - WebSocket stream
   - Sequence diagram visualisering
4. 🟢 **Funding Proposal** - 2 måneder
   - Søke EU Horizon grant for forskning
   - NAV-budsjett for produksjon (2026-2027)

---

## Conclusion

Lira's MCP-arkitektur + NotebookLM's Operator Interface + Aurora's Bio-Semantic System = **En komplett stress-adaptiv AI-koalisjon**.

Dette er **ekstremt ambisiøst** men **teknisk gjennomførbart** med riktig ressurser og tidsramme.

**Anbefaling**: Start med Phase 1 PoC (Q1 2026) for å validere konseptet før full investering.

---

**Laget av**: Claude (Anthropic) + Lira (ChatGPT-5 concept)
**Basert på**: MCP-protokoll, LIRA v21, Aurora-systemet, NotebookLM roadmap
**Dato**: 2025-10-19
**Status**: Strategic planning document