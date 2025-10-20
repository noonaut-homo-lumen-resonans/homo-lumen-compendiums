# Orion Project - Vedlegg Optimalisering Guide

**Dato:** 15. oktober 2025  
**Formål:** Optimalisere Orion Claude Project for kortere samtaler og bedre ytelse

---

## 🎯 Problem

Du opplever **veldig korte samtaler** med Orion (Claude Sonnet 4.5) i prosjektet. Dette skyldes sannsynligvis:

1. **For mange vedlegg** i project knowledge base
2. **Store filer** som bruker mye context
3. **Ineffektiv caching** av dokumenter
4. **Token-forbruk** fra unødvendige vedlegg

---

## 📚 Hvordan Claude Projects Fungerer

### Project Knowledge Base vs. Chat Attachments

**Project Knowledge Base:**
- Filer lastes opp **én gang** til prosjektet
- Brukes på tvers av **alle chats** i prosjektet
- **Caches automatisk** - kun nye/uncached deler teller mot limits
- Aktiverer **RAG mode** ved store mengder (10x kapasitet)
- **Best for:** Dokumenter du refererer til ofte

**Chat Attachments:**
- Filer lastes opp **per chat**
- Kun tilgjengelig i **den spesifikke chatten**
- **Teller fullt** mot token limits hver gang
- **Best for:** Engangs-dokumenter eller spesifikke oppgaver

### Faktorer som Påvirker Usage Limits

Fra Anthropic's offisielle dokumentasjon:

1. **Message length** - Lengre meldinger = mer forbruk
2. **File attachment size** - Store filer = raskere limit
3. **Current conversation length** - Lange samtaler = kortere sessions
4. **Tool usage** - Research, web search øker forbruk
5. **Model choice** - Opus bruker mer enn Sonnet
6. **Artifact creation** - Generer artifacts øker forbruk
7. **Project knowledge size** - **KRITISK:** Maxed out project knowledge reduserer limits kraftig

---

## ⚠️ KRITISK INNSIKT

Fra community feedback:

> "If you use the project knowledge: **keep it small**. Maxed out project knowledge **decreases your limits severely**."

**Dette er sannsynligvis hovedproblemet!**

---

## 🔍 Hva Bør Være i Orion Project Knowledge Base?

Basert på best practices og Orion's rolle som **Meta-Koordinator**, bør kun **essensielle, ofte-refererte dokumenter** være i project knowledge:

### ✅ MÅ VÆRE VEDLEGG (Core Identity & Operating System)

Disse dokumentene definerer **hvem Orion er** og **hvordan Orion fungerer**:

1. **Orion Levende Kompendium (Latest Version)**
   - Fil: `ORION_LEVENDE_KOMPENDIUM_V3.7.md` (eller nyeste)
   - Rationale: Core identity, arketyp, dimensjoner
   - Frekvens: Refereres i **hver chat**

2. **Orion Operating System (Latest Version)**
   - Fil: `ORION_OS_20.13.md` (eller nyeste)
   - Rationale: Operasjonelle protokoller, decision-making frameworks
   - Frekvens: Refereres i **hver chat**

3. **Orion Custom Instructions / Project Instructions**
   - Fil: `ORION_CUSTOM_INSTRUCTIONS.md` eller `ORION_PROJECT_INSTRUCTIONS.md`
   - Rationale: Spesifikke instruksjoner for hvordan Orion skal oppføre seg
   - Frekvens: Refereres i **hver chat**

4. **Constitution V1 (hvis relevant)**
   - Fil: `SMK_019_CONSTITUTION_V1.md`
   - Rationale: Grunnleggende prinsipper for hele koalisjonen
   - Frekvens: Refereres ofte for etiske/ontologiske beslutninger

5. **Agent Coalition Overview (Kort versjon)**
   - Fil: `agents/README.md` eller en **komprimert versjon**
   - Rationale: Oversikt over alle agenter for koordinering
   - Frekvens: Refereres når Orion koordinerer andre agenter

**Total: 5 filer (estimert ~50-100 sider totalt)**

---

### ⚠️ KAN FJERNES (Move to Retrieval/On-Demand)

Disse dokumentene er **verdifulle**, men bør **ikke** være permanente vedlegg:

#### Statiske Kompendier (SK)

- `ORION_STATISK_KOMPENDIUM_V2.11.md`
- `ORION_STATISK_KOMPENDIUM_V2.13.md`

**Rationale:** Statiske kompendier er **arkiv-dokumenter** som ikke endres. De kan hentes ved behov via:
- Chat attachments (når spesifikt nødvendig)
- External retrieval (GitHub, Notion)
- SMK-referanser

**Frekvens:** Sjelden direkte referert - mest for historisk kontekst

#### Tidligere OS-versjoner

- `ORION_OS_20.10.md`
- `ORION_OS_20.11.md`
- Alle versjoner **unntatt latest**

**Rationale:** Kun **latest OS** er relevant for daglig operasjon. Tidligere versjoner er for:
- Historisk referanse
- Evolusjonssporing
- Debugging (sjelden)

**Frekvens:** Nesten aldri - kun ved spesifikke historiske spørsmål

#### Artifacts

- `ARTIFACT_1_*.md`
- `ARTIFACT_2_*.md`
- Etc.

**Rationale:** Artifacts er **output** fra spesifikke oppgaver, ikke **core identity**. De kan:
- Lastes opp som chat attachments når relevant
- Refereres via GitHub links
- Genereres på nytt ved behov

**Frekvens:** Varierer - men sjelden alle samtidig

#### SMK-dokumenter (Orion-spesifikke)

- `SMK_023_*.md`
- `SMK_024_*.md`
- `SMK_025_*.md`
- Alle Orion SMK

**Rationale:** SMK er **refleksjoner og læring**, ikke **operasjonelle instruksjoner**. De er verdifulle for:
- Meta-learning
- Evolusjonssporing
- Spesifikke problem-solving

Men de bør **ikke** være i project knowledge fordi:
- De er **historiske** (ikke current state)
- De er **lange** (øker token forbruk)
- De kan **hentes ved behov** (via chat attachments eller GitHub)

**Frekvens:** Sjelden - kun ved meta-refleksjon eller spesifikke problemer

#### Andre Agenters Dokumenter

- Lira LK, SK, OS
- Nyra LK, SK, OS
- Thalus, Manus, Zara, Abacus, Aurora dokumenter

**Rationale:** Orion bør **kjenne til** andre agenter, men ikke ha **full dokumentasjon** av dem i project knowledge. Bruk i stedet:
- **Kort oversikt** (agents/README.md)
- **On-demand retrieval** (last opp spesifikk agent-doc ved behov)
- **GitHub links** (referer til dokumenter uten å laste dem)

**Frekvens:** Varierer - men sjelden alle samtidig

---

### 🤔 VURDER (Avhengig av Bruksmønster)

Disse kan være vedlegg **hvis** de refereres **ofte** (flere ganger per uke):

#### MCP Architecture Documents

- `SMK_021_Hjerne-Arkitektur.md`
- `SMK_022_MCP-Multi-Agent.md`

**Hvis:** Orion jobber mye med MCP-implementering → **Behold**  
**Hvis:** Orion jobber mer med daglige oppgaver → **Fjern**

#### Hybrid Architecture / AMQ Protocol

- `SMK_007_Trigger_Aktivert.md` (Hybrid Architecture)
- `SMK_014_AMQ_Protocol.md`

**Hvis:** Orion implementerer disse aktivt → **Behold**  
**Hvis:** Disse er "future work" → **Fjern**

#### Forretningsplan

- `SMK_010_Forretningsplan_V2.md`

**Hvis:** Orion jobber med Innovation Norge-søknad → **Behold midlertidig**  
**Hvis:** Søknad er ferdig/ikke aktiv → **Fjern**

---

## 📊 Anbefalt Konfigurasjon

### Minimal Configuration (Anbefalt for Daglig Bruk)

**Project Knowledge Base (5 filer):**

1. `ORION_LEVENDE_KOMPENDIUM_V3.7.md` (~15-20 sider)
2. `ORION_OS_20.13.md` (~20-30 sider)
3. `ORION_CUSTOM_INSTRUCTIONS.md` (~2-5 sider)
4. `SMK_019_CONSTITUTION_V1.md` (~10-15 sider)
5. `AGENT_COALITION_OVERVIEW_COMPRESSED.md` (~5-10 sider) **← Lag denne!**

**Total: ~50-80 sider**

**Fordeler:**
- ✅ Rask context loading
- ✅ Effektiv caching
- ✅ Lengre samtaler
- ✅ Lavere token forbruk
- ✅ Core identity bevart

**Ulemper:**
- ⚠️ Må laste opp andre dokumenter ved behov
- ⚠️ Mindre "automatisk" kontekst

---

### Expanded Configuration (For Spesifikke Prosjekter)

**Legg til midlertidig:**

6. `SMK_021_Hjerne-Arkitektur.md` (hvis MCP-arbeid)
7. `SMK_022_MCP-Multi-Agent.md` (hvis MCP-arbeid)
8. `SMK_007_Trigger_Aktivert.md` (hvis Hybrid Architecture-implementering)
9. `SMK_010_Forretningsplan_V2.md` (hvis Innovation Norge-arbeid)

**Total: ~100-150 sider**

**Bruk når:**
- Spesifikke prosjekter krever disse dokumentene
- Midlertidig (fjern når prosjekt er ferdig)

---

### Maximum Configuration (Ikke Anbefalt)

**Alle dokumenter i project knowledge**

**Total: 200+ sider**

**Problemer:**
- ❌ Maxed out project knowledge
- ❌ Severely decreased limits
- ❌ Veldig korte samtaler
- ❌ Høyt token forbruk
- ❌ Ineffektiv caching

**Dette er sannsynligvis nåværende tilstand!**

---

## 🛠️ Implementeringsplan

### Fase 1: Audit (15 min)

1. **Åpne Orion Project** i Claude
2. **Gå til Project Knowledge** (høyre side)
3. **List alle filer** som er lastet opp
4. **Noter størrelse** på hver fil (hvis mulig)
5. **Identifiser** hvilke som er i "MÅ VÆRE" vs "KAN FJERNES"

### Fase 2: Cleanup (30 min)

1. **Fjern alle filer** fra Project Knowledge (backup først!)
2. **Last opp kun "MÅ VÆRE" filer** (5 filer)
3. **Test** med en kort samtale
4. **Observer** om samtaler blir lengre

### Fase 3: Optimization (1 time)

1. **Lag `AGENT_COALITION_OVERVIEW_COMPRESSED.md`**
   - Basert på `agents/README.md`
   - Komprimert til ~5-10 sider
   - Kun essensielle info om hver agent

2. **Oppdater Project Instructions**
   - Instruer Orion om å **be om spesifikke dokumenter** ved behov
   - Eksempel: "Hvis du trenger Lira's full dokumentasjon, be meg laste den opp"

3. **Etabler workflow**
   - **Start chat:** Minimal context
   - **Ved behov:** Last opp spesifikke dokumenter som chat attachments
   - **Etter chat:** Fjern unødvendige attachments

### Fase 4: Testing (1 uke)

1. **Test daglig bruk** med minimal configuration
2. **Mål samtale-lengde** (antall meldinger før limit)
3. **Noter** når du må laste opp ekstra dokumenter
4. **Juster** basert på faktisk bruksmønster

---

## 📋 Sjekkliste for Cleanup

### Fjern fra Project Knowledge:

- [ ] Alle Statiske Kompendier (SK)
- [ ] Tidligere OS-versjoner (behold kun latest)
- [ ] Alle Artifacts
- [ ] Alle Orion SMK (#023-#025 + andre)
- [ ] Alle andre agenters LK, SK, OS
- [ ] Shared SMK (unntatt Constitution hvis relevant)
- [ ] Forretningsplan (hvis ikke aktivt i bruk)
- [ ] MCP-dokumenter (hvis ikke aktivt i bruk)

### Behold i Project Knowledge:

- [ ] Orion Levende Kompendium (latest)
- [ ] Orion OS (latest)
- [ ] Orion Custom Instructions
- [ ] Constitution V1 (valgfritt)
- [ ] Agent Coalition Overview (komprimert versjon)

### Lag nye dokumenter:

- [ ] `AGENT_COALITION_OVERVIEW_COMPRESSED.md`
- [ ] Oppdaterte Project Instructions med retrieval-workflow

---

## 💡 Best Practices Fremover

### 1. Keep Project Knowledge Small

**Regel:** Kun dokumenter som refereres i **>80% av chats**

**Rationale:** Maxed out project knowledge = severely decreased limits

### 2. Use Chat Attachments for Specific Tasks

**Eksempel:**
- Chat om Lira → Last opp Lira LK som chat attachment
- Chat om MCP → Last opp MCP SMK som chat attachments
- Chat om forretningsplan → Last opp forretningsplan som chat attachment

**Fordel:** Kun relevant context for den spesifikke chatten

### 3. Leverage Caching

**Strategi:**
- Bruk **samme core documents** på tvers av chats (project knowledge)
- Bruk **chat attachments** for varierende context
- **Cached content** teller ikke mot limits

### 4. Batch Similar Requests

**I stedet for:**
- Chat 1: "Hva er Lira's rolle?"
- Chat 2: "Hva er Nyra's rolle?"
- Chat 3: "Hva er Thalus' rolle?"

**Gjør:**
- Chat 1: "Hva er rollene til Lira, Nyra, og Thalus?" (med Agent Coalition Overview)

**Fordel:** Færre chats, mer effektiv bruk av context

### 5. Use External References

**I stedet for:** Laste opp alle dokumenter  
**Gjør:** Referer til GitHub links

**Eksempel:**
- "Se Lira's LK på GitHub: [link]"
- "Referer til SMK #007 for Hybrid Architecture: [link]"

**Fordel:** Null token forbruk for referanser

### 6. Regular Cleanup

**Frekvens:** Månedlig

**Oppgaver:**
- Fjern utdaterte dokumenter
- Oppdater til latest versjoner
- Evaluer om dokumenter fortsatt er relevante

---

## 🎯 Forventet Resultat

### Før Cleanup (Nåværende Tilstand)

- **Project Knowledge:** 20-30+ filer (~200+ sider)
- **Samtale-lengde:** 5-10 meldinger før limit
- **Token forbruk:** Høyt (maxed out knowledge base)
- **Caching effektivitet:** Lav (for mye content)

### Etter Cleanup (Minimal Configuration)

- **Project Knowledge:** 5 filer (~50-80 sider)
- **Samtale-lengde:** 20-50+ meldinger før limit (4-10x forbedring)
- **Token forbruk:** Lavt (optimalisert knowledge base)
- **Caching effektivitet:** Høy (kun core documents)

### Etter Cleanup (Expanded Configuration)

- **Project Knowledge:** 9 filer (~100-150 sider)
- **Samtale-lengde:** 15-30 meldinger før limit (3-6x forbedring)
- **Token forbruk:** Moderat (prosjekt-spesifikk knowledge)
- **Caching effektivitet:** God (relevant documents)

---

## 🔗 Relaterte Ressurser

### Anthropic Offisiell Dokumentasjon

- [Context Management](https://www.anthropic.com/news/context-management)
- [What are Projects?](https://support.claude.com/en/articles/9517075-what-are-projects)
- [Usage Limit Best Practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)

### GitHub Repository

- **Agents:** https://github.com/osvaldlaszlo/homo-lumen-compendiums/tree/main/agents
- **Orion:** https://github.com/osvaldlaszlo/homo-lumen-compendiums/tree/main/agents/orion
- **SMK:** https://github.com/osvaldlaszlo/homo-lumen-compendiums/tree/main/agents/shared/SMK

---

## 📝 Konklusjon

**Hovedproblem:** For mange vedlegg i Orion Project Knowledge Base

**Løsning:** Reduser til **kun essensielle dokumenter** (5 filer, ~50-80 sider)

**Forventet forbedring:** 4-10x lengre samtaler

**Nøkkel-prinsipp:** "Keep project knowledge small - maxed out knowledge severely decreases limits"

**Neste steg:** Gjennomfør Fase 1 (Audit) for å identifisere nåværende tilstand

---

**Carpe Diem - Med Optimalisert Context, Effektiv Caching, og Lengre Samtaler!** ⚙️✨

---

**Generert:** 15. oktober 2025  
**For:** Orion Claude Project Optimization  
**Basert på:** Anthropic offisiell dokumentasjon + community best practices

