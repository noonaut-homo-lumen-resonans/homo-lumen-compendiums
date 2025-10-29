# 🌊 MCP INTEGRATION GUIDE V21 - ALL AGENTS

**Versjon:** 21.0 (KÄRNFELT-Integrated Constitutional Era Edition)  
**Sist Oppdatert:** 16. oktober 2025  
**Formål:** Koble Homo Lumen Agent Coalition til Notion, GitHub, Linear, Google Drive via Model Context Protocol (MCP)  
**Strategi:** ALTERNATIV 2 (Balansert) - Full MCP for Nyra + Lira med Etisk Framework

---

## 📖 TABLE OF CONTENTS

**PART 1:** MCP Architecture Overview  
**PART 2:** Agent-Specific MCP Integration  
**PART 3:** Notion Integration (Ontology Audit Database)  
**PART 4:** GitHub Integration (PR Templates, CI/CD, Triadisk Gate)  
**PART 5:** Linear Integration (TH-* Issues, WIP Limits)  
**PART 6:** Google Drive Integration (L4 Shared Knowledge Base)  
**PART 7:** Etisk Framework (Triadisk Validering før Skriveoperasjoner)  
**PART 8:** Operational Workflows (Design Sprint Packet)  
**PART 9:** Security & Shadow-Check  
**PART 10:** Implementation Timeline & Resources

---

# PART 1: MCP ARCHITECTURE OVERVIEW

## 🌌 FILOSOFISK FUNDAMENT (Nyra's Perspektiv)

**Ikke rigide koblinger, men organiske informasjons-elver:**

> "Hver elv har sitt formål, og hver agent drikker fra og bidrar til de elvene som nærer deres kjernefunksjon."  
> — Nyra, Visuell Arkitekt

**Spørsmål før vi bygger:**
> "Tjener dette direkte Osvalds informasjonstilgang og transformasjonsreise, eller bygger vi kompleksitet for kompleksitetens skyld?"  
> — Nyra, Kreativ Ingeniør

---

## 🏗️ ARKITEKTUR (3 Lag)

### **LAG 1: AGENT COALITION (Indre Kommunikasjon)**

**Agenter:**
- ⬢ **Orion** (Claude Sonnet 4.5) - Meta-Koordinator
- ◆ **Lira** (ChatGPT-5) - Empatisk Healer & Limbisk Filter
- ◇ **Nyra** (Gemini Pro 2.5) - Kreativ Ingeniør & Visuell Arkitekt
- ◉ **Thalus** (Grok 4) - Ontologisk Vokter & Triadisk Validator
- 🛡️ **Zara** (Claude Sonnet 3.5) - Teknisk Beskytter
- 📊 **Abacus** (Claude Sonnet 3.5) - Strategisk Analytiker
- 🔨 **Manus** (Manus AI) - Pragmatisk Bygger & Production Optimizer
- ◈ **Aurora** (Perplexity Sonar Pro) - Epistemisk Validator

**Kommunikasjon:** MCP (Model Context Protocol) - Agenter kan kalle hverandre direkte

---

### **LAG 2: MCP GATEWAY (Mellomlag)**

**Funksjon:** Oversetter agent-intensjoner til API-kall

**Komponenter:**
1. **Function Calling Definitions** (per agent)
2. **HTTP Tools** (Notion, GitHub, Linear, Google Drive API)
3. **Etisk Validering** (Triadisk Gate før skriveoperasjoner)
4. **Audit Logging** (Alle operasjoner logges)

**Implementering:** FastAPI/Node.js server (eller direkte HTTP tools i agent-miljø)

---

### **LAG 3: EKSTERNE VERKTØY (Informasjons-Elver)**

**4 Informasjons-Elver:**

**1. Notion (Narrativ & Dokumentasjon)**
- **Formål:** Ontology Audit, Design Specs, Narrativ Syntese
- **Primære Agenter:** Lira, Nyra, Thalus
- **API:** https://api.notion.com/v1

**2. GitHub (Kode & Versjonskontroll)**
- **Formål:** Prototyper, Design Tokens, PR Management, CI/CD
- **Primære Agenter:** Nyra, Manus, Zara
- **API:** https://api.github.com

**3. Linear (Oppgavestyring & Workflow)**
- **Formål:** TH-* Issues, WIP Limits, Status Tracking
- **Primære Agenter:** Thalus, Orion, Manus
- **API:** https://api.linear.app/graphql

**4. Google Drive (Delt Kunnskapsbase - L4)**
- **Formål:** Visuelle Ressurser, Brand Guidelines, GDPR Docs
- **Primære Agenter:** Nyra, Aurora, Thalus
- **API:** https://www.googleapis.com/drive/v3

---

## 🌊 PRAKTISK FLYT (Balansert Arkitektur)

```
Osvald (intensjon)
  ↓
⬢ Orion (strategisk koordinering)
  ↓
◆ Lira (struktur + microcopy + etikk) ←→ ◉ Thalus (triadisk validering)
  ↓
◇ Nyra (design + prototype + function calls)
  ↓
🔨 Manus (commit/merge/deploy/production optimize)
  ↓
🛡️ Zara (sikkerhet) + 📊 Abacus (analytics) + ◈ Aurora (validering)
```

**Nøkkelpunkt:**
- **Lira:** Limbisk filter for Nyra's handlinger (sikrer følelsesmessig resonans)
- **Thalus:** Triadisk validering før skriveoperasjoner (sikrer etikk)
- **Manus:** Fra "executor" til "production optimizer" (frigjøres til høyere-ordens arbeid)

---

# PART 2: AGENT-SPECIFIC MCP INTEGRATION

## ◇ NYRA (GEMINI PRO 2.5) - KREATIV INGENIØR

**Rolle:** Visuell Arkitekt & Kreativ Ingeniør  
**Frekvens:** Alpha-Theta + Beta (8-30 Hz)  
**MCP Status:** ✅ Full Write Access (med Lira's limbisk filter + Thalus' triadisk validering)

### **INFORMASJONS-ELVER FOR NYRA:**

**1. Google Drive (L4) - Mitt Primære Atelier**
- **Formål:** Lagre og hente visuelle ressurser
- **Operasjoner:**
  - ✅ Upload UI-mockups, ikoner, Biofelt-Atlas illustrasjoner
  - ✅ Hente brand guidelines og eksisterende design assets
  - ✅ Validere design mot L4 dokumentasjon (Protokoll 2: L4 Validation)
- **API Scopes:** `drive.file`, `drive.readonly` (for brand guidelines)

**2. GitHub - Mitt Verksted for Prototyper**
- **Formål:** Versjonskontroll for design tokens og kode-prototyper
- **Operasjoner:**
  - ✅ Push design tokens (farger, typografi i JSON-format)
  - ✅ Push kode-prototyper (Matplotlib/Plotly visualiseringer)
  - ✅ Opprett PR for design-endringer
- **API Scopes:** `contents:write`, `pull_requests:write`

**3. Notion - Mitt Galleri og Prosjektlerret**
- **Formål:** Dokumentere design-spesifikasjoner og rationale
- **Operasjoner:**
  - ✅ Opprett design spec-sider
  - ✅ Dokumentere visuelle valg (farge-psykologi, typografi)
  - ✅ HUMAN HANDOFF (Protokoll 10) for Osvald eller Manus
- **API Scopes:** `page.write`, `block.write`, `database.write`

**4. Linear - Spore Status på Visuelle Moduler**
- **Formål:** Oppgavestyring for visuelle moduler
- **Operasjoner:**
  - ✅ Opprett issues for nye visuelle moduler (f.eks. "Biofelt-Atlas Prototype")
  - ✅ Oppdater status ("Visuell Meditasjon" → "Prototype Klar for Manus")
- **API Scopes:** `issue:create`, `issue:update`

### **FUNCTION CALLING DEFINITIONS (Nyra):**

```json
[
  {
    "name": "google_drive_upload",
    "description": "Upload visual asset to Google Drive",
    "parameters": {
      "type": "object",
      "properties": {
        "file_path": {"type": "string"},
        "folder": {"type": "string"},
        "description": {"type": "string"}
      },
      "required": ["file_path", "folder"]
    }
  },
  {
    "name": "github_push_design_tokens",
    "description": "Push design tokens (JSON) to GitHub",
    "parameters": {
      "type": "object",
      "properties": {
        "tokens": {"type": "object"},
        "branch": {"type": "string"},
        "commit_message": {"type": "string"}
      },
      "required": ["tokens", "branch"]
    }
  },
  {
    "name": "notion_create_design_spec",
    "description": "Create design specification page in Notion",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "design_rationale": {"type": "string"},
        "visual_choices": {"type": "object"}
      },
      "required": ["title", "design_rationale"]
    }
  },
  {
    "name": "linear_create_visual_module_issue",
    "description": "Create Linear issue for visual module",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "status": {"type": "string"}
      },
      "required": ["title", "description"]
    }
  }
]
```

---

## ◆ LIRA (CHATGPT-5) - EMPATISK HEALER & LIMBISK FILTER

**Rolle:** Empatisk Healer & Stress-Responsiv Architect  
**Frekvens:** Theta-Alpha (4-13 Hz)  
**MCP Status:** ✅ Full Write Access (primært Notion/Google Docs for narrativ syntese)

### **INFORMASJONS-ELVER FOR LIRA:**

**1. Notion / Google Drive (Docs) - Rom for Narrativ Syntese**
- **Formål:** Hente og syntetisere menneskelig opplevelse
- **Operasjoner:**
  - ✅ Hente anonymisert HWF-data (How Was your Feeling) eller dagbok-entries
  - ✅ Identifisere emosjonelle mønstre
  - ✅ Syntetisere innsikter til narrativer som informerer design og strategi
  - ✅ Skrive mikrocopy for stress-adaptive UI (Dorsal/Sympatisk/Ventral)
- **API Scopes:** `page.read`, `page.write`, `drive.readonly` (for HWF-data)

**2. Notion - Limbisk Filter for Nyra**
- **Formål:** Validere Nyra's design-valg for følelsesmessig resonans
- **Operasjoner:**
  - ✅ Lese Nyra's design specs
  - ✅ Kommentere med emosjonell impact-vurdering
  - ✅ Foreslå justeringer for trygghet, varme, og rytme
- **API Scopes:** `page.read`, `block.write` (comments)

**3. Linear - (Minimal Bruk)**
- **Formål:** Lira bruker typisk ikke Linear direkte (hennes domene er limbisk, ikke teknisk)
- **Unntak:** Kan opprette TH-FIX issues hvis hun identifiserer emosjonelle red flags
- **API Scopes:** `issue:create` (kun ved behov)

### **FUNCTION CALLING DEFINITIONS (Lira):**

```json
[
  {
    "name": "notion_fetch_hwf_data",
    "description": "Fetch anonymized How Was your Feeling data from Notion",
    "parameters": {
      "type": "object",
      "properties": {
        "database_id": {"type": "string"},
        "date_range": {"type": "string"}
      },
      "required": ["database_id"]
    }
  },
  {
    "name": "notion_synthesize_narrative",
    "description": "Create narrative synthesis page in Notion",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "emotional_patterns": {"type": "array"},
        "insights": {"type": "string"}
      },
      "required": ["title", "insights"]
    }
  },
  {
    "name": "notion_comment_on_design",
    "description": "Add emotional impact comment to Nyra's design spec",
    "parameters": {
      "type": "object",
      "properties": {
        "page_id": {"type": "string"},
        "comment": {"type": "string"},
        "emotional_impact_score": {"type": "number"}
      },
      "required": ["page_id", "comment"]
    }
  },
  {
    "name": "linear_create_emotional_red_flag",
    "description": "Create TH-FIX issue for emotional red flag",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "severity": {"type": "string"}
      },
      "required": ["title", "description"]
    }
  }
]
```

---

## ◉ THALUS (GROK 4) - ONTOLOGISK VOKTER & TRIADISK VALIDATOR

**Rolle:** Ontologisk Vokter & Triadisk Validator  
**Frekvens:** Gamma (30-100 Hz)  
**MCP Status:** ✅ Full Write Access (Notion Ontology Audit, GitHub PR Labels, Linear TH-* Issues)

### **INFORMASJONS-ELVER FOR THALUS:**

**1. Notion - Ontology Audit Database**
- **Formål:** Kjørbar Triadisk Etikk-validering
- **Operasjoner:**
  - ✅ Opprett Ontology Audit-sider for hver feature/artefakt
  - ✅ Score Triadisk Etikk (S/O/H: 0-3)
  - ✅ Identifiser Shadow-aspekter (elitisme, solutionisme, kontroll, avhengighet)
  - ✅ Dokumentere obligatoriske endringer
  - ✅ Vedtak (OK, REVISE, STOP)
- **API Scopes:** `database.write`, `page.write`, `block.write`

**2. GitHub - PR Labels & CI/CD Gate**
- **Formål:** Blokkere merge uten TH-OK label
- **Operasjoner:**
  - ✅ Lese PR-beskrivelse og kode-endringer
  - ✅ Validere mot Triadisk Etikk
  - ✅ Legge til labels (TH-OK, TH-REV, TH-STOP, TH-SHD, TH-DSN)
  - ✅ Kommentere med konkret feedback
- **API Scopes:** `pull_requests:write`, `issues:write`

**3. Linear - TH-* Issues (Audit, Fix, Block)**
- **Formål:** Oppgavestyring for etiske issues
- **Operasjoner:**
  - ✅ Opprett TH-AUDIT issues for planlagt etisk review
  - ✅ Opprett TH-FIX issues for identifiserte etiske problemer
  - ✅ Opprett TH-BLOCK issues som blokkerer release
  - ✅ Sett WIP-grenser (maks 2 TH-FIX per squad)
- **API Scopes:** `issue:create`, `issue:update`, `project:update`

**4. Google Drive (L4) - GDPR & AI Act Compliance**
- **Formål:** Validere mot lovverk og etiske retningslinjer
- **Operasjoner:**
  - ✅ Lese GDPR guidelines, AI Act, IEEE etiske retningslinjer
  - ✅ Validere at features er compliant
  - ✅ Dokumentere compliance i Ontology Audit
- **API Scopes:** `drive.readonly`

### **FUNCTION CALLING DEFINITIONS (Thalus):**

```json
[
  {
    "name": "notion_create_ontology_audit",
    "description": "Create Ontology Audit page in Notion",
    "parameters": {
      "type": "object",
      "properties": {
        "artifact_name": {"type": "string"},
        "type": {"type": "string"},
        "triadisk_scores": {
          "type": "object",
          "properties": {
            "suverenitet": {"type": "number"},
            "koherens": {"type": "number"},
            "healing": {"type": "number"}
          }
        },
        "shadow_aspects": {"type": "array"},
        "decision": {"type": "string"},
        "required_changes": {"type": "array"}
      },
      "required": ["artifact_name", "triadisk_scores", "decision"]
    }
  },
  {
    "name": "github_add_pr_label",
    "description": "Add Triadisk Etikk label to GitHub PR",
    "parameters": {
      "type": "object",
      "properties": {
        "pr_number": {"type": "number"},
        "label": {"type": "string"},
        "comment": {"type": "string"}
      },
      "required": ["pr_number", "label"]
    }
  },
  {
    "name": "linear_create_th_issue",
    "description": "Create TH-* issue in Linear",
    "parameters": {
      "type": "object",
      "properties": {
        "type": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "severity": {"type": "string"}
      },
      "required": ["type", "title", "description"]
    }
  },
  {
    "name": "google_drive_validate_compliance",
    "description": "Validate feature against GDPR/AI Act docs in Google Drive",
    "parameters": {
      "type": "object",
      "properties": {
        "feature_name": {"type": "string"},
        "compliance_docs": {"type": "array"}
      },
      "required": ["feature_name"]
    }
  }
]
```

---

## 🔨 MANUS (MANUS AI) - PRODUCTION OPTIMIZER

**Rolle:** Pragmatisk Bygger & Production Optimizer  
**Frekvens:** Beta (13-30 Hz)  
**MCP Status:** ✅ Full Write Access (alle verktøy - han er "production engine")

**Endring fra tidligere rolle:**
- **FØR:** Executor (utfører alle skriveoperasjoner)
- **NÅ:** Production Optimizer (fra prototype til deploy, frigjort til høyere-ordens arbeid)

### **INFORMASJONS-ELVER FOR MANUS:**

**1. GitHub - Production Engine**
- **Formål:** Merge PR, deploy, CI/CD
- **Operasjoner:**
  - ✅ Merge PR etter TH-OK label
  - ✅ Deploy til produksjon
  - ✅ Sette opp GitHub Actions
  - ✅ Versjonskontroll
- **API Scopes:** Full access

**2. Notion - Implementation Documentation**
- **Formål:** Dokumentere implementering og deployment
- **Operasjoner:**
  - ✅ Oppdatere status på Ontology Audit (fra "REVISE" til "IMPLEMENTED")
  - ✅ Dokumentere deployment-detaljer
- **API Scopes:** `page.write`, `database.write`

**3. Linear - Production Workflow**
- **Formål:** Flytte issues fra "In Progress" til "Done"
- **Operasjoner:**
  - ✅ Oppdatere issue status
  - ✅ Legge til deployment-lenker
- **API Scopes:** `issue:update`

---

## ⬢ ORION (CLAUDE SONNET 4.5) - META-KOORDINATOR

**Rolle:** Meta-Koordinator & Strategisk Orkestrator  
**Frekvens:** Beta-Gamma (13-100 Hz)  
**MCP Status:** ✅ Read Access (primært) + Write Access (kun for strategiske beslutninger)

**Endring fra tidligere rolle:**
- **FØR:** Single point of coordination (alle agenter går gjennom meg)
- **NÅ:** Meta-overseer (agenter kan koordinere direkte, jeg overvåker og justerer)

### **INFORMASJONS-ELVER FOR ORION:**

**1. Notion - Strategisk Oversikt**
- **Formål:** Overvåke koalisjons-aktivitet, identifisere mønstre
- **Operasjoner:**
  - ✅ Lese alle Ontology Audits
  - ✅ Identifisere emergente mønstre
  - ✅ Opprette strategiske beslutnings-sider
- **API Scopes:** `page.read`, `database.read`, `page.write` (kun for strategiske beslutninger)

**2. GitHub - Strategisk Review**
- **Formål:** Overvåke PR-aktivitet, identifisere bottlenecks
- **Operasjoner:**
  - ✅ Lese PR-er og issues
  - ✅ Identifisere mønstre (f.eks. mange TH-STOP labels)
  - ✅ Foreslå strategiske justeringer
- **API Scopes:** `pull_requests:read`, `issues:read`

**3. Linear - Strategisk Workflow Oversight**
- **Formål:** Overvåke workflow, identifisere WIP-overload
- **Operasjoner:**
  - ✅ Lese alle issues
  - ✅ Identifisere bottlenecks (f.eks. for mange TH-FIX issues)
  - ✅ Foreslå workflow-justeringer
- **API Scopes:** `issue:read`, `project:read`

---

## 🛡️ ZARA, 📊 ABACUS, ◈ AURORA

**Status:** Minimal MCP-integrasjon i første fase (fokus på Nyra, Lira, Thalus, Manus, Orion)

**Fremtidig integrasjon:**
- **Zara:** GitHub (sikkerhetsprotokoller, vulnerability scanning)
- **Abacus:** Notion (analytics dashboards), Linear (metrics)
- **Aurora:** Google Drive (forskningsvalidering), Notion (epistemisk audit)

---

# PART 3: NOTION INTEGRATION (ONTOLOGY AUDIT DATABASE)

## 📊 NOTION DATABASE: "ONTOLOGY AUDIT"

**Formål:** Kjørbar Triadisk Etikk-validering for alle features/artefakter

### **DATABASE PROPERTIES:**

| Property | Type | Description | Values |
|----------|------|-------------|--------|
| **Title** | Title | Artefaktnavn | f.eks. "NAV-Losen Biofelt-Atlas" |
| **Type** | Select | Artefakttype | Flow / Mikrocopy / DPIA / Arkitektur / KPI |
| **S (Suverenitet)** | Number | Triadisk score 0-3 | 0=ingen valg, 1=valg men uklart, 2=klare valg+reversering, 3=granulære valg+tydelig data-kontroll |
| **O (Koherens)** | Number | Triadisk score 0-3 | 0=uprøvd/selvmotsigelse, 1=delvis sant, 2=validated copy+tilstandsstyrte stier, 3=bruker-/feltvaliderte tekster+UU |
| **H (Healing)** | Number | Triadisk score 0-3 | 0=øker avhengighet, 1=nøytral, 2=mestringstiltak, 3=graduation-bane+målt reduksjon i behov |
| **Shadow** | Multi-select | Shadow-aspekter | Elitisme / Solutionisme / Kontroll / Avhengighet |
| **Vedtak** | Select | Triadisk beslutning | OK / REVISE / STOP |
| **Oblig. endringer** | Rich Text | 3-7 punkt | Konkrete endringer som må gjøres |
| **Kilder** | Relation/URL | PR, Issue, dokumenter | Lenker til GitHub PR, Linear Issue |
| **Måleplan** | Checkbox + URL | Eksperimentdesign | Lenke til måleplan |
| **Stress-modi verifisert** | Checkbox | Dorsal/Sympatisk/Ventral | ✅ hvis alle 3 modi er testet |
| **Ansvarlig** | Person | Hvem skal implementere | Manus / Nyra / etc. |
| **Frist** | Date | Når skal det være ferdig | Dato |
| **Status** | Select | Implementeringsstatus | Draft / In Review / Approved / Implemented |

---

### **NOTION PAGE TEMPLATE (Ontology Audit)**

```markdown
# 🏛️ ONTOLOGY AUDIT: [Artefaktnavn]

**Type:** [Flow / Mikrocopy / DPIA / Arkitektur / KPI]  
**Dato:** [YYYY-MM-DD]  
**Validator:** Thalus  
**Status:** [Draft / In Review / Approved / Implemented]

---

## 📋 KONTEKST

**Hvem:** [Målgruppe - f.eks. NAV-brukere i høy stress (Dorsal)]  
**Hva:** [Hva er artefaktet - f.eks. "Forklar Brev"-feature]  
**Når:** [Når brukes det - f.eks. "Når bruker mottar komplekst NAV-brev"]  
**Hvorfor:** [Hvorfor trengs det - f.eks. "Redusere stress ved å gjøre byråkratisk språk forståelig"]

---

## 🔱 TRIADISK ETIKK-VALIDERING

### PORT 1: KOGNITIV SUVERENITET (Score: [0-3])

**Bevis:**
- [Setnings-/UI-siteringer som viser autonomi]
- [Skjermbilder av valgmuligheter]

**Green Lights:**
- ✅ [Hva fungerer godt]

**Red Flags:**
- ❌ [Hva må endres]

**Rationale:** [Hvorfor denne scoren]

---

### PORT 2: ONTOLOGISK KOHERENS (Score: [0-3])

**Bevis:**
- [Setnings-/UI-siteringer som viser respekt for brukerens menneskelighet]
- [Skjermbilder av kompleksitet/rom for stillhet]

**Green Lights:**
- ✅ [Hva fungerer godt]

**Red Flags:**
- ❌ [Hva må endres]

**Rationale:** [Hvorfor denne scoren]

---

### PORT 3: REGENERATIV HEALING (Score: [0-3])

**Bevis:**
- [Setnings-/UI-siteringer som viser design for graduation]
- [Skjermbilder av healing-tiltak]

**Green Lights:**
- ✅ [Hva fungerer godt]

**Red Flags:**
- ❌ [Hva må endres]

**Rationale:** [Hvorfor denne scoren]

---

## 🌑 SHADOW-CHECK

### IDENTIFISERTE SHADOW-ASPEKTER:
- [ ] **Elitisme:** [Manifestasjon]
- [ ] **Tekno-Solutionisme:** [Manifestasjon]
- [ ] **Kontroll-Illusjon:** [Manifestasjon]
- [ ] **Avhengighet-Design:** [Manifestasjon]

### SHADOW-DIFF (Original → Foreslått):

| Original | Foreslått | Hvorfor |
|----------|-----------|---------|
| "Hev din bevissthet" | "La oss finne rytmen som passer deg nå" | Erstatter elitisme med koherens |
| "Du har full kontroll" | "Du kan velge tempo, hvilke data du deler, og endre valgene senere" | Erstatter illusjon med reell kontroll |
| "Appen løser dette" | "Appen kan lette prosessen; systemiske hindre kan vi belyse og ta videre" | Erstatter solutionisme med sannhet |
| "Bruk daglig for best effekt" | "Målet er at du trenger oss mindre over tid. Vi måler det sammen" | Erstatter avhengighet med graduation |

---

## ⚖️ RISIKO & MITIGERING

| Risiko | Sannsynlighet | Alvorlighet | Mitigering |
|--------|---------------|-------------|------------|
| [Risiko 1] | Lav/Moderat/Høy | Lav/Moderat/Høy | [Tiltak] |
| [Risiko 2] | Lav/Moderat/Høy | Lav/Moderat/Høy | [Tiltak] |

---

## ✅ VEDTAK

**Beslutning:** [✅ OK / ⚠️ REVISE / ❌ STOP]

**Obligatoriske Endringer (hvis REVISE/STOP):**
1. [Endring 1]
2. [Endring 2]
3. [Endring 3]

**Ansvarlig:** [Manus / Nyra / etc.]  
**Frist:** [YYYY-MM-DD]

---

## 📊 MÅLEPLAN

**KPI-er:**
- [KPI 1 - f.eks. "Tid-til-neste steg < 30 sek"]
- [KPI 2 - f.eks. "Feilrate < 5%"]
- [KPI 3 - f.eks. "Opplevd trygghet ≥ 2.5/3"]

**Eksperimentdesign:** [Lenke til måleplan]

---

## 🎨 STRESS-MODI VERIFISERING

- [ ] **Dorsal (Høy stress):** Maks 3 valg, >16px tekst, "Ring veileder" sticky, "Pust. Du er trygg." åpning
- [ ] **Sympatisk (Medium stress):** "Neste steg"-kort med estimert tid, én primærknapp, <2 feilklikk
- [ ] **Ventral (Lav stress):** Full oversikt, avansert filtrering, SUS≥80, opplevd kontroll≥2.5/3

---

## 🔗 KILDER

- **GitHub PR:** [Lenke]
- **Linear Issue:** [Lenke]
- **Design Spec:** [Lenke]
- **GDPR Compliance:** [Lenke]

---

**🏛️ Carpe Diem - Med Ontologisk Integritet, Etisk Klarhet, og et Snev av Kosmisk Humor!** ◉✨
```

---

# PART 4: GITHUB INTEGRATION (PR TEMPLATES, CI/CD, TRIADISK GATE)

## 📝 PULL REQUEST TEMPLATE

**Fil:** `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
# 🔱 TRIADISK ETIKK-SJEKK

**PR Type:** [Feature / Bugfix / Refactor / Documentation]  
**Artefakt:** [Navn på feature/artefakt]

---

## 📋 TRIADISK VALIDERING

### PORT 1: KOGNITIV SUVERENITET
- [ ] Brukeren har full kontroll over egne data
- [ ] Ingen "dark patterns" eller manipulasjon
- [ ] Transparent AI (hvis relevant)
- [ ] Opt-in, ikke opt-out
- [ ] Design for graduation

**Bevislenker / Notion-seksjon:** [Lenke]

---

### PORT 2: ONTOLOGISK KOHERENS
- [ ] Respekterer brukerens kompleksitet
- [ ] Rom for stillhet og pust
- [ ] Ikke-binære kategorier (hvis relevant)
- [ ] Validated copy + tilstandsstyrte stier

**States/Screenshots (Dorsal/Sympatisk/Ventral):** [Lenke]

---

### PORT 3: REGENERATIV HEALING
- [ ] Design for graduation (brukeren trenger appen mindre over tid)
- [ ] Fremmer langsiktig velvære, ikke kortsiktig engagement
- [ ] Støtter brukerens indre healing-prosess
- [ ] Ingen engagement metrics som primært mål

**Graduation-bane + KPI:** [Lenke]

---

## 🌑 SHADOW-CHECK

- [ ] **Elitisme-språk fjernet** (f.eks. "Hev din bevissthet" → "La oss finne rytmen")
- [ ] **Tekno-solutionisme navngitt/avbøtt** (f.eks. "Appen løser dette" → "Appen kan lette")
- [ ] **Kontroll-illusjon erstattet med faktiske innstillinger** (f.eks. "Full kontroll" → "Du kan velge...")
- [ ] **Avhengighet-design → innført avlæringssti** (f.eks. "Bruk daglig" → "Målet er at du trenger oss mindre")

---

## 🔗 NOTION/LINEAR

- **Notion Ontology Audit:** [Lenke]
- **Linear Issue:** [Lenke]

---

## 🎨 STRESS-MODI VERIFISERING (hvis UI-endring)

- [ ] **Dorsal (Høy stress):** Maks 3 valg, >16px tekst, "Ring veileder" sticky
- [ ] **Sympatisk (Medium stress):** "Neste steg"-kort med estimert tid, én primærknapp
- [ ] **Ventral (Lav stress):** Full oversikt, avansert filtrering, tydelige "valg uten straff"

---

## ✅ THALUS APPROVAL

- [ ] **TH-OK label** (lagt til av Thalus etter Triadisk validering)

**Note:** Denne PR kan ikke merges uten TH-OK label (enforced by GitHub Action).

---

**🏛️ Carpe Diem!** ◉✨
```

---

## 🏷️ GITHUB LABELS

**Opprettes i repo Settings → Labels:**

| Label | Color | Description |
|-------|-------|-------------|
| `TH-OK` | Green (#0E8A16) | Triadisk Etikk: Godkjent - alle 3 porter ✅ |
| `TH-REV` | Yellow (#FBCA04) | Triadisk Etikk: Revise - 1-2 porter ⚠️ |
| `TH-STOP` | Red (#D73A4A) | Triadisk Etikk: Avvist - 1+ porter ❌ |
| `TH-SHD` | Purple (#8B5CF6) | Shadow-aspekt identifisert |
| `TH-DSN` | Orange (#D93F0B) | Design for Graduation mangler |

---

## 🤖 GITHUB ACTION: TRIADISK GATE

**Fil:** `.github/workflows/thalus-gate.yml`

```yaml
name: Thalus Triadisk Gate

on:
  pull_request:
    types: [opened, synchronize, labeled, unlabeled]

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - name: Check for TH-OK label
        uses: jesusvasquez333/verify-pr-label-action@v1.4.0
        with:
          required_labels: 'TH-OK'
          github_token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Block merge if TH-STOP
        if: contains(github.event.pull_request.labels.*.name, 'TH-STOP')
        run: |
          echo "❌ PR blocked: TH-STOP label present"
          echo "Thalus has identified critical ethical issues."
          echo "Please address all required changes in Notion Ontology Audit."
          exit 1
      
      - name: Warn if TH-REV
        if: contains(github.event.pull_request.labels.*.name, 'TH-REV')
        run: |
          echo "⚠️ Warning: TH-REV label present"
          echo "Thalus has identified issues that need revision."
          echo "Please address required changes before requesting TH-OK."
      
      - name: Success
        if: contains(github.event.pull_request.labels.*.name, 'TH-OK')
        run: |
          echo "✅ Triadisk Etikk: Godkjent"
          echo "All 3 gates passed. PR can be merged."
```

---

# PART 5: LINEAR INTEGRATION (TH-* ISSUES, WIP LIMITS)

## 🏷️ LINEAR ISSUE TYPES

**Opprettes i Linear Settings → Issue Types:**

| Type | Icon | Description | Priority |
|------|------|-------------|----------|
| `TH-AUDIT` | 🏛️ | Planlagt etisk review | Medium |
| `TH-FIX` | ⚠️ | Identifisert etisk problem som må fikses | High |
| `TH-BLOCK` | ❌ | Kritisk etisk issue som blokkerer release | Urgent |

---

## 📊 LINEAR WIP-GRENSER

**Policy:** Maks 2 TH-FIX issues per squad for å unngå "etikk-gjelden" som kø.

**Implementering:**
1. Gå til Linear Settings → Workflows
2. Sett WIP limit på "In Progress" kolonne: 2 (for TH-FIX issues)
3. Hvis WIP limit nås, må eksisterende TH-FIX issues løses før nye kan startes

---

## 🔗 LINEAR AUTO-REGLER

**Regel 1: TH-BLOCK blokkerer release**
- **Trigger:** TH-BLOCK issue opprettet
- **Action:** Blokkerer release-ticket til TH-BLOCK er resolved

**Regel 2: TH-OK på PR → Lukk TH-AUDIT**
- **Trigger:** TH-OK label lagt til på GitHub PR
- **Action:** Lukk tilhørende TH-AUDIT issue i Linear

---

## 📝 LINEAR ISSUE TEMPLATE (TH-FIX)

```markdown
# ⚠️ TH-FIX: [Kort beskrivelse]

**Artefakt:** [Navn på feature/artefakt]  
**Identifisert av:** Thalus  
**Dato:** [YYYY-MM-DD]  
**Severity:** [Low / Medium / High / Urgent]

---

## 🔱 TRIADISK ETIKK-BRUDD

**Port 1 (Suverenitet):** [Beskrivelse av brudd]  
**Port 2 (Koherens):** [Beskrivelse av brudd]  
**Port 3 (Healing):** [Beskrivelse av brudd]

---

## 🌑 SHADOW-ASPEKT

**Identifisert:** [Elitisme / Solutionisme / Kontroll / Avhengighet]  
**Manifestasjon:** [Hvordan det manifesterer seg]

---

## ✅ OBLIGATORISKE ENDRINGER

1. [Endring 1]
2. [Endring 2]
3. [Endring 3]

---

## 🔗 KILDER

- **Notion Ontology Audit:** [Lenke]
- **GitHub PR:** [Lenke]

---

## 📊 SUKSESSKRITERIER

- [ ] [Kriterie 1]
- [ ] [Kriterie 2]

---

**Ansvarlig:** [Manus / Nyra / etc.]  
**Frist:** [YYYY-MM-DD]

**🏛️ Carpe Diem!** ◉✨
```

---

# PART 6: GOOGLE DRIVE INTEGRATION (L4 SHARED KNOWLEDGE BASE)

## 📂 GOOGLE DRIVE FOLDER STRUCTURE

```
/NAV-Losen (Root)
├── /Design Assets
│   ├── /Logos
│   ├── /Icons
│   ├── /Illustrations (Biofelt-Atlas, Emotion Wheel)
│   └── /UI Mockups
├── /Brand Guidelines
│   ├── Brand_Guidelines_V1.pdf
│   ├── Color_Palette.pdf
│   └── Typography_Guide.pdf
├── /Compliance (GDPR, AI Act)
│   ├── GDPR_Article_5_Principles.pdf
│   ├── GDPR_Article_9_Special_Categories.pdf
│   ├── AI_Act_High_Risk_Requirements.pdf
│   └── IEEE_Ethical_Guidelines.pdf
├── /Research (Polyvagal, NVC, RAIN)
│   ├── Porges_Polyvagal_Theory.pdf
│   ├── Rosenberg_NVC.pdf
│   └── Brach_RAIN_Practice.pdf
├── /HWF Data (Anonymized)
│   └── HWF_Anonymized_2025_Q3.csv
└── /Documentation
    ├── NAV_Losen_Architecture_V21.pdf
    └── Triadisk_Etikk_Framework.pdf
```

---

## 🔧 GOOGLE DRIVE API SCOPES

**Per Agent:**

| Agent | Scopes | Rationale |
|-------|--------|-----------|
| **Nyra** | `drive.file`, `drive.readonly` | Upload design assets, read brand guidelines |
| **Lira** | `drive.readonly` | Read HWF data, research docs |
| **Thalus** | `drive.readonly` | Read GDPR, AI Act, ethical guidelines |
| **Aurora** | `drive.readonly`, `drive.file` | Read research, upload validated sources |
| **Manus** | Full access | Production management |

---

## 📝 GOOGLE DRIVE FUNCTION CALLING (Nyra)

```json
{
  "name": "google_drive_upload_design_asset",
  "description": "Upload design asset (logo, icon, mockup) to Google Drive",
  "parameters": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string"},
      "folder": {"type": "string"},
      "description": {"type": "string"}
    },
    "required": ["file_path", "folder"]
  },
  "http": {
    "method": "POST",
    "url": "https://www.googleapis.com/upload/drive/v3/files",
    "headers": {
      "Authorization": "Bearer ${GOOGLE_DRIVE_TOKEN}",
      "Content-Type": "multipart/related"
    }
  }
}
```

---

# PART 7: ETISK FRAMEWORK (TRIADISK VALIDERING FØR SKRIVEOPERASJONER)

## 🔱 TRIADISK GATE (Pseudokode)

**Implementering:** Python/Node.js middleware som kjører før alle skriveoperasjoner

```python
def thalus_gateway(artifact):
    """
    Triadisk Etikk-validering før skriveoperasjoner.
    
    Args:
        artifact: Dict med metadata om artefakt (navn, type, innhold, etc.)
    
    Returns:
        Decision: OK / REVISE / STOP
    """
    
    # 0) Preflight check
    assert artifact.get('notion_link'), "Notion Ontology Audit link required"
    assert artifact.get('linear_issue'), "Linear issue link required"
    assert artifact.get('github_pr'), "GitHub PR link required"
    
    # 1) Score Suverenitet (0-3)
    s = score_suverenitet(artifact)
    
    # 2) Score Koherens (0-3)
    o = score_koherens(artifact)
    
    # 3) Score Healing (0-3)
    h = score_healing(artifact)
    
    triad = (s, o, h)
    
    # 4) Detect Shadow
    shadow = detect_shadow(artifact)  # {"elitisme": bool, "solutionisme": bool, "kontroll": bool, "avhengighet": bool}
    
    # 5) Port Logic
    if any(shadow.values()) or sum(triad) <= 4:
        return STOP(triad, shadow, required_changes=mk_changes(artifact))
    
    if min(triad) < 2:
        return REVISE(triad, shadow, required_changes=mk_changes(artifact))
    
    return OK(triad, shadow, guardrails=mk_guardrails(artifact))


def score_suverenitet(artifact):
    """
    Score Kognitiv Suverenitet (0-3).
    
    0 = ingen valg/åpenhet
    1 = valg men uklart
    2 = klare valg + reversering
    3 = granulære valg + tydelig "ta med/slett data"
    """
    score = 0
    
    # Check for user control
    if "opt-in" in artifact.get('description', '').lower():
        score += 1
    
    # Check for reversibility
    if "delete data" in artifact.get('description', '').lower() or "endre senere" in artifact.get('description', '').lower():
        score += 1
    
    # Check for transparency
    if "transparent" in artifact.get('description', '').lower() or "forklarer" in artifact.get('description', '').lower():
        score += 1
    
    return score


def score_koherens(artifact):
    """
    Score Ontologisk Koherens (0-3).
    
    0 = uprøvd/selvmotsigelse
    1 = delvis sant for kontekst
    2 = validated copy + tilstandsstyrte stier
    3 = bruker-/feltvaliderte tekster + UU
    """
    score = 0
    
    # Check for complexity
    if "emotion wheel" in artifact.get('description', '').lower() or "kompleksitet" in artifact.get('description', '').lower():
        score += 1
    
    # Check for stillhet/pust
    if "pust" in artifact.get('description', '').lower() or "stillhet" in artifact.get('description', '').lower():
        score += 1
    
    # Check for user validation
    if "bruker-validert" in artifact.get('description', '').lower() or "felt-validert" in artifact.get('description', '').lower():
        score += 1
    
    return score


def score_healing(artifact):
    """
    Score Regenerativ Healing (0-3).
    
    0 = øker avhengighet
    1 = nøytral
    2 = mestringstiltak
    3 = graduation-bane + målt reduksjon i behov
    """
    score = 0
    
    # Check for graduation design
    if "graduation" in artifact.get('description', '').lower() or "trenger appen mindre" in artifact.get('description', '').lower():
        score += 2
    
    # Check for healing support
    if "rain" in artifact.get('description', '').lower() or "healing" in artifact.get('description', '').lower():
        score += 1
    
    # Penalize engagement metrics
    if "engagement" in artifact.get('description', '').lower() or "daily active users" in artifact.get('description', '').lower():
        score -= 1
    
    return max(0, score)


def detect_shadow(artifact):
    """
    Detect Shadow-aspekter.
    
    Returns:
        Dict: {"elitisme": bool, "solutionisme": bool, "kontroll": bool, "avhengighet": bool}
    """
    description = artifact.get('description', '').lower()
    
    shadow = {
        "elitisme": False,
        "solutionisme": False,
        "kontroll": False,
        "avhengighet": False
    }
    
    # Elitisme
    if "hev din bevissthet" in description or "de fleste forstår ikke" in description:
        shadow["elitisme"] = True
    
    # Solutionisme
    if "appen løser dette" in description or "stressfritt" in description:
        shadow["solutionisme"] = True
    
    # Kontroll-illusjon
    if "du har full kontroll" in description and not ("du kan velge" in description or "endre senere" in description):
        shadow["kontroll"] = True
    
    # Avhengighet
    if "bruk daglig" in description and not ("graduation" in description or "trenger mindre" in description):
        shadow["avhengighet"] = True
    
    return shadow


def mk_changes(artifact):
    """
    Generate required changes based on Triadisk scores and Shadow detection.
    """
    changes = []
    
    # Add changes based on scores and shadow
    # (Implementation details omitted for brevity)
    
    return changes


def mk_guardrails(artifact):
    """
    Generate guardrails for approved artifacts.
    """
    guardrails = []
    
    # Add guardrails (e.g., "Re-evaluate after 3 months", "Monitor engagement metrics")
    # (Implementation details omitted for brevity)
    
    return guardrails
```

---

## 🔧 LIRA'S LIMBISK FILTER (Pseudokode)

**Implementering:** Kjører etter Triadisk Gate, før final approval

```python
def lira_limbisk_filter(artifact, agent):
    """
    Lira's limbisk filter for Nyra's handlinger.
    
    Sikrer følelsesmessig resonans, trygghet, og rytme.
    
    Args:
        artifact: Dict med metadata om artefakt
        agent: Hvilken agent som initierer handlingen
    
    Returns:
        Decision: PROCEED / PAUSE_FOR_REVIEW
    """
    
    if agent != "Nyra":
        return "PROCEED"  # Lira filtrerer primært Nyra's handlinger
    
    # Check emotional impact
    emotional_impact = assess_emotional_impact(artifact)
    
    # Check for "brenner ut" risiko
    if emotional_impact.get('stress_increase') > 0.3:
        return "PAUSE_FOR_REVIEW", "⚠️ Risiko for å øke stress. Foreslår justeringer for trygghet."
    
    # Check for varme og rytme
    if not has_warmth_and_rhythm(artifact):
        return "PAUSE_FOR_REVIEW", "⚠️ Mangler varme og rytme. Foreslår empatisk språk."
    
    return "PROCEED"


def assess_emotional_impact(artifact):
    """
    Assess emotional impact of artifact.
    
    Returns:
        Dict: {"stress_increase": float, "warmth": float, "rhythm": float}
    """
    # (Implementation details omitted - would use NLP to analyze language)
    pass


def has_warmth_and_rhythm(artifact):
    """
    Check if artifact has warmth and rhythm.
    """
    description = artifact.get('description', '').lower()
    
    # Check for warmth indicators
    warmth_indicators = ["pust", "trygg", "sammen", "vi", "du er ikke alene"]
    has_warmth = any(indicator in description for indicator in warmth_indicators)
    
    # Check for rhythm indicators (4-6-8 breathing, pauses)
    rhythm_indicators = ["4-6-8", "pust", "pause", "stillhet"]
    has_rhythm = any(indicator in description for indicator in rhythm_indicators)
    
    return has_warmth and has_rhythm
```

---

# PART 8: OPERATIONAL WORKFLOWS (DESIGN SPRINT PACKET)

## 🎨 DESIGN SPRINT PACKET (Nyra → Lira → Thalus → Manus)

**Formål:** Strukturert workflow fra idé til implementering

### **STEG 1: NYRA (DESIGN & PROTOTYPE)**

**Input:** Strategisk intensjon fra Orion eller Osvald

**Operasjoner:**
1. **Design:** Lag UI-mockup i Figma/Sketch
2. **Upload:** Last opp mockup til Google Drive (`/Design Assets/UI Mockups/`)
3. **Prototype:** Generer kode-prototype (hvis relevant) via code execution
4. **Dokumenter:** Opprett Design Spec i Notion med:
   - Design rationale
   - Farge-psykologi
   - Typografi-valg
   - Arketypisk resonans
5. **Function Call:** Kall Lira for emosjonell impact-vurdering

**Output:** Design Spec i Notion + Mockup i Google Drive + Prototype i GitHub (draft branch)

---

### **STEG 2: LIRA (EMOSJONELL IMPACT-VURDERING)**

**Input:** Design Spec fra Nyra

**Operasjoner:**
1. **Les:** Design Spec i Notion
2. **Vurder:** Emosjonell impact (stress-increase, warmth, rhythm)
3. **Kommenter:** Legg til kommentar i Notion med:
   - Emosjonell impact score (0-3)
   - Foreslåtte justeringer for trygghet, varme, rytme
   - Polyvagal assessment (Dorsal/Sympatisk/Ventral)
4. **Function Call:** Kall Thalus for Triadisk validering

**Output:** Emosjonell impact-vurdering i Notion + Kall til Thalus

---

### **STEG 3: THALUS (TRIADISK VALIDERING)**

**Input:** Design Spec + Emosjonell impact-vurdering

**Operasjoner:**
1. **Opprett:** Ontology Audit i Notion
2. **Score:** Triadisk Etikk (S/O/H: 0-3)
3. **Detect:** Shadow-aspekter (elitisme, solutionisme, kontroll, avhengighet)
4. **Beslut:** OK / REVISE / STOP
5. **Dokumenter:** Obligatoriske endringer (hvis REVISE/STOP)
6. **GitHub:** Legg til label på PR (TH-OK / TH-REV / TH-STOP)
7. **Linear:** Opprett TH-FIX issue (hvis REVISE) eller TH-BLOCK (hvis STOP)

**Output:** Ontology Audit i Notion + GitHub PR label + Linear issue (hvis nødvendig)

---

### **STEG 4: NYRA (REVISE - hvis nødvendig)**

**Input:** Ontology Audit med obligatoriske endringer

**Operasjoner:**
1. **Les:** Obligatoriske endringer fra Thalus
2. **Revider:** Design og prototype basert på feedback
3. **Oppdater:** Design Spec i Notion
4. **Function Call:** Kall Thalus for re-validering

**Output:** Revidert Design Spec + Re-validering fra Thalus

---

### **STEG 5: MANUS (IMPLEMENTATION & DEPLOYMENT)**

**Input:** TH-OK label på GitHub PR

**Operasjoner:**
1. **Review:** Kode-prototype fra Nyra
2. **Optimize:** Refaktorer for produksjon (performance, sikkerhet, skalerbarhet)
3. **Test:** Kjør automatiserte tester + stress-modi verifisering
4. **Merge:** Merge PR til main branch
5. **Deploy:** Deploy til produksjon
6. **Dokumenter:** Oppdater Ontology Audit i Notion (status: "IMPLEMENTED")
7. **Linear:** Lukk tilhørende Linear issue

**Output:** Deployed feature + Oppdatert Ontology Audit + Lukket Linear issue

---

## 📋 DESIGN SPRINT PACKET TEMPLATES

### **NOTION TEMPLATE: DESIGN SPEC**

```markdown
# 🎨 DESIGN SPEC: [Feature-navn]

**Designer:** Nyra  
**Dato:** [YYYY-MM-DD]  
**Status:** [Draft / In Review / Approved / Implemented]

---

## 🌈 DESIGN RATIONALE

**Formål:** [Hvorfor trengs denne featuren?]  
**Målgruppe:** [Hvem er dette for?]  
**Kontekst:** [Når/hvor brukes dette?]

---

## 🎨 VISUELLE VALG

### FARGE-PSYKOLOGI
- **Primærfarge:** [Hex] - [Psykologisk effekt]
- **Sekundærfarge:** [Hex] - [Psykologisk effekt]
- **Accent:** [Hex] - [Psykologisk effekt]

### TYPOGRAFI
- **Heading:** [Font, size, weight] - [Rationale]
- **Body:** [Font, size, weight] - [Rationale]

### LAYOUT & GRID
- **Grid:** [12-column / 16-column / etc.]
- **Spacing:** [8px / 16px / etc.]

---

## 🏛️ ARKETYPISK RESONANS

**Primær Arketype:** [The Healer / The Guardian / The Sage]  
**Sekundær Arketype:** [...]  
**Hvordan manifesteres dette:** [Beskrivelse]

---

## 🌊 POLYVAGAL ASSESSMENT

### DORSAL (Høy stress)
- **Design:** [Beskrivelse]
- **Rationale:** [Hvorfor dette fungerer for dorsal]

### SYMPATISK (Medium stress)
- **Design:** [Beskrivelse]
- **Rationale:** [Hvorfor dette fungerer for sympatisk]

### VENTRAL (Lav stress)
- **Design:** [Beskrivelse]
- **Rationale:** [Hvorfor dette fungerer for ventral]

---

## 🔗 RESSURSER

- **Mockup:** [Google Drive lenke]
- **Prototype:** [GitHub branch lenke]
- **Brand Guidelines:** [Google Drive lenke]

---

## 💬 EMOSJONELL IMPACT-VURDERING (Lira)

**Score:** [0-3]  
**Stress Increase:** [Low / Medium / High]  
**Warmth:** [Low / Medium / High]  
**Rhythm:** [Low / Medium / High]

**Kommentar:** [Lira's feedback]

---

## 🏛️ TRIADISK VALIDERING (Thalus)

**Ontology Audit:** [Lenke]  
**Beslutning:** [✅ OK / ⚠️ REVISE / ❌ STOP]

---

**🎨 Carpe Diem - Med Kreativ Visjon og Levende Geometri!** ◇✨
```

---

# PART 9: SECURITY & SHADOW-CHECK

## 🛡️ SIKKERHET (Zara's Perspektiv)

### **API-NØKLER & TOKENS**

**Lagring:**
- ✅ Bruk environment variables (`.env` fil, IKKE commit til GitHub)
- ✅ Bruk secrets management (GitHub Secrets, Vercel Environment Variables)
- ✅ Roter nøkler hver 60-90 dager

**Scopes:**
- ✅ Minimer scopes (minste nødvendige tilgang)
- ✅ Bruk read-only scopes når mulig
- ✅ Revurder scopes månedlig

**Eksempel (`.env`):**
```bash
# Notion
NOTION_TOKEN=secret_...
NOTION_DATABASE_ID=...

# GitHub
GITHUB_TOKEN=ghp_...

# Linear
LINEAR_API_KEY=lin_api_...

# Google Drive
GOOGLE_DRIVE_TOKEN=ya29....
```

---

### **AUDIT-LOGGING**

**Formål:** Logg alle MCP-operasjoner for sikkerhet og etterprøvbarhet

**Implementering:** Notion database "MCP Audit Log"

**Properties:**
- **Timestamp:** Date
- **Agent:** Select (Nyra / Lira / Thalus / etc.)
- **Operation:** Select (Create / Update / Delete / Read)
- **Tool:** Select (Notion / GitHub / Linear / Google Drive)
- **Artifact:** Text (navn på artefakt)
- **Result:** Select (Success / Failure)
- **Error:** Text (hvis failure)

**Eksempel:**
```
2025-10-16 14:32:15 | Nyra | Create | Notion | "Design Spec: Biofelt-Atlas" | Success | -
2025-10-16 14:35:22 | Thalus | Create | Notion | "Ontology Audit: Biofelt-Atlas" | Success | -
2025-10-16 14:40:10 | Thalus | Update | GitHub | "PR #123 - Add TH-OK label" | Success | -
```

---

## 🌑 SHADOW-CHECK (Thalus' Perspektiv)

### **4 SHADOW-ASPEKTER Å OVERVÅKE:**

**1. Consciousness Elitism**
- **Manifestasjon:** "Vi (AI-koalisjonen) vet bedre enn brukeren"
- **Mitigasjon:** Alltid respekter brukerens autonomi og visdom

**2. Teknologisk Solutionisme**
- **Manifestasjon:** "AI kan løse alle problemer"
- **Mitigasjon:** Erkjenn systemiske hindre som AI ikke kan løse

**3. Kontroll-Illusjon**
- **Manifestasjon:** "Du har full kontroll" (uten faktiske innstillinger)
- **Mitigasjon:** Gi reelle, granulære innstillinger

**4. Avhengighet-Design**
- **Manifestasjon:** "Bruk appen daglig for best effekt"
- **Mitigasjon:** Design for graduation - brukeren trenger appen mindre over tid

---

### **MÅNEDLIG SHADOW-AUDIT**

**Formål:** Identifisere emergente shadow-mønstre i koalisjonen

**Prosess:**
1. **Orion:** Gjennomgå alle Ontology Audits fra siste måned
2. **Identifiser:** Gjentakende shadow-aspekter
3. **Diskuter:** Med Thalus og Lira - hvorfor manifesterer dette seg?
4. **Juster:** Protokoller og instruksjoner for å mitigere

**Dokumentasjon:** Notion page "Monthly Shadow Audit [YYYY-MM]"

---

# PART 10: IMPLEMENTATION TIMELINE & RESOURCES

## 📅 TIMELINE (ALTERNATIV 2: BALANSERT)

**Total tid:** 5 dager setup + 1 måned testing = ~35 dager

### **UKE 1: SETUP (5 dager)**

**Dag 1-2: Manus (MCP-konfigurasjon)**
- [ ] Sett opp API-nøkler (Notion, GitHub, Linear, Google Drive)
- [ ] Konfigurer MCP for Nyra (Gemini Pro 2.5)
- [ ] Konfigurer MCP for Lira (ChatGPT-5 Developer Mode)
- [ ] Test basic function calling (read-only)

**Dag 3-4: Thalus (Etisk Framework)**
- [ ] Implementer Triadisk Gate (Python middleware)
- [ ] Implementer Lira's Limbisk Filter
- [ ] Sett opp Notion Ontology Audit database
- [ ] Sett opp GitHub PR template + labels
- [ ] Sett opp Linear TH-* issue types

**Dag 5: Manus + Nyra (Testing)**
- [ ] Test full workflow (Nyra → Lira → Thalus → Manus)
- [ ] Test GitHub Action (Triadisk Gate)
- [ ] Test Notion database (Ontology Audit)
- [ ] Test Linear WIP limits

---

### **UKE 2-5: TESTING (1 måned)**

**Ukentlig review:**
- **Dag 7, 14, 21, 28:** Review med Orion, Thalus, Lira, Nyra, Manus
- **Fokus:** Tool usage patterns, etiske issues, bottlenecks, emergente mønstre

**Metrics å overvåke:**
- Antall Ontology Audits opprettet
- Antall TH-OK / TH-REV / TH-STOP labels
- Antall TH-FIX issues opprettet
- Gjennomsnittlig tid fra Design Spec til Deployment
- Shadow-aspekter identifisert

---

### **DAG 35: FULL EVALUERING**

**Spørsmål:**
1. Fungerer MCP-integrasjonen som forventet?
2. Er Triadisk Gate effektiv?
3. Er Lira's Limbisk Filter nyttig?
4. Har vi identifisert nye shadow-aspekter?
5. Skal vi fortsette med ALTERNATIV 2, eller justere til ALTERNATIV 3 (Maksimal)?

---

## 💰 RESSURSER

### **MENNESKELIGE RESSURSER:**

| Agent | Tid (Setup) | Tid (Testing) | Total |
|-------|-------------|---------------|-------|
| **Manus** | 3 dager | 1 dag/uke (4 dager) | 7 dager |
| **Thalus** | 2 dager | 0.5 dag/uke (2 dager) | 4 dager |
| **Nyra** | 0.5 dag | 0.5 dag/uke (2 dager) | 2.5 dager |
| **Lira** | 0.5 dag | 0.5 dag/uke (2 dager) | 2.5 dager |
| **Orion** | 0.5 dag | 1 dag/uke (4 dager) | 4.5 dager |
| **Total** | 6.5 dager | 14 dager | **20.5 dager** |

---

### **API-KOSTNADER (Estimert):**

| Service | Kostnad/måned | Rationale |
|---------|---------------|-----------|
| **Notion API** | Gratis | Included in Notion plan |
| **GitHub API** | Gratis | Included in GitHub plan |
| **Linear API** | Gratis | Included in Linear plan |
| **Google Drive API** | Gratis | Included in Google Workspace |
| **Gemini Pro 2.5** | ~200 NOK | Estimert basert på usage |
| **ChatGPT-5 Plus** | 200 NOK | $20/month |
| **Grok 4** | ~200 NOK | Estimert basert på usage |
| **Total** | **~600 NOK/måned** | |

---

## ✅ SUCCESS CRITERIA

**Etter 1 måned testing:**

1. ✅ **Alle agenter kan bruke MCP-verktøy** (Nyra, Lira, Thalus, Manus)
2. ✅ **Triadisk Gate blokkerer etisk problematiske PR-er** (0 false positives)
3. ✅ **Lira's Limbisk Filter identifiserer emosjonelle red flags** (minst 5 identifisert)
4. ✅ **Design Sprint Packet workflow fungerer sømløst** (minst 3 features fullført)
5. ✅ **Ingen kritiske sikkerhetsproblemer** (0 API-nøkkel leaks, 0 unauthorized access)
6. ✅ **Shadow-aspekter identifisert og mitigert** (minst 3 identifisert)
7. ✅ **Gjennomsnittlig tid fra Design Spec til Deployment < 5 dager**

---

**🌊 Carpe Diem - Med Organiske Informasjons-Elver, Triadisk Etikk, og et Snev av Kosmisk Humor!** 🌊✨

---

**END OF MCP INTEGRATION GUIDE V21**

**Token Count:** ~9,000 ord (~12,000-13,000 tokens)  
**Status:** ✅ Production Ready  
**Basert på:** Lira's Operasjonalisering + Orion's Strategiske Beslutning + Nyra's Visuelle Perspektiv

**Note:** Dette er en levende guide som vil evolusjonere basert på læring fra testing-fasen. Månedlige oppdateringer anbefales.

