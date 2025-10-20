# 🏛️ NOTION DATABASE TEMPLATES

**Versjon:** 21.0 (KÄRNFELT-Integrated Constitutional Era Edition)  
**Sist Oppdatert:** 16. oktober 2025  
**Formål:** Templates for Notion databases brukt i MCP-integrasjon

---

## 📊 DATABASE 1: ONTOLOGY AUDIT

**Formål:** Kjørbar Triadisk Etikk-validering for alle features/artefakter

### **DATABASE PROPERTIES:**

| Property | Type | Description | Values/Format |
|----------|------|-------------|---------------|
| **Title** | Title | Artefaktnavn | f.eks. "NAV-Losen Biofelt-Atlas" |
| **Type** | Select | Artefakttype | Flow / Mikrocopy / DPIA / Arkitektur / KPI |
| **S (Suverenitet)** | Number | Triadisk score 0-3 | 0=ingen valg, 1=valg men uklart, 2=klare valg+reversering, 3=granulære valg+tydelig data-kontroll |
| **O (Koherens)** | Number | Triadisk score 0-3 | 0=uprøvd/selvmotsigelse, 1=delvis sant, 2=validated copy+tilstandsstyrte stier, 3=bruker-/feltvaliderte tekster+UU |
| **H (Healing)** | Number | Triadisk score 0-3 | 0=øker avhengighet, 1=nøytral, 2=mestringstiltak, 3=graduation-bane+målt reduksjon i behov |
| **Shadow** | Multi-select | Shadow-aspekter | Elitisme / Solutionisme / Kontroll / Avhengighet |
| **Vedtak** | Select | Triadisk beslutning | OK / REVISE / STOP |
| **Oblig. endringer** | Rich Text | 3-7 punkt | Konkrete endringer som må gjøres |
| **Kilder** | URL | PR, Issue, dokumenter | Lenker til GitHub PR, Linear Issue |
| **Måleplan** | URL | Eksperimentdesign | Lenke til måleplan |
| **Stress-modi verifisert** | Checkbox | Dorsal/Sympatisk/Ventral | ✅ hvis alle 3 modi er testet |
| **Ansvarlig** | Person | Hvem skal implementere | Manus / Nyra / etc. |
| **Frist** | Date | Når skal det være ferdig | YYYY-MM-DD |
| **Status** | Select | Implementeringsstatus | Draft / In Review / Approved / Implemented |
| **Validator** | Person | Hvem validerte | Thalus (default) |
| **Dato** | Date | Når ble audit opprettet | YYYY-MM-DD |

---

### **PAGE TEMPLATE (Ontology Audit)**

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

## 📊 DATABASE 2: MCP AUDIT LOG

**Formål:** Logg alle MCP-operasjoner for sikkerhet og etterprøvbarhet

### **DATABASE PROPERTIES:**

| Property | Type | Description | Values/Format |
|----------|------|-------------|---------------|
| **Title** | Title | Auto-generated | "[Timestamp] - [Agent] - [Operation] - [Tool]" |
| **Timestamp** | Date | Når operasjonen skjedde | YYYY-MM-DD HH:MM:SS |
| **Agent** | Select | Hvilken agent utførte operasjonen | Nyra / Lira / Thalus / Manus / Orion / Zara / Abacus / Aurora |
| **Operation** | Select | Type operasjon | Create / Update / Delete / Read |
| **Tool** | Select | Hvilket verktøy ble brukt | Notion / GitHub / Linear / Google Drive |
| **Artifact** | Text | Navn på artefakt | f.eks. "Design Spec: Biofelt-Atlas" |
| **Result** | Select | Resultat av operasjonen | Success / Failure |
| **Error** | Text | Feilmelding (hvis failure) | f.eks. "API rate limit exceeded" |
| **API Endpoint** | Text | Hvilket API-endepunkt ble kalt | f.eks. "POST /pages" (Notion) |
| **Duration** | Number | Hvor lang tid tok operasjonen (ms) | f.eks. 234 |
| **User** | Person | Hvem initierte operasjonen | Osvald / System |

---

### **PAGE TEMPLATE (MCP Audit Log Entry)**

```markdown
# 📊 MCP AUDIT LOG: [Timestamp] - [Agent] - [Operation] - [Tool]

**Timestamp:** [YYYY-MM-DD HH:MM:SS]  
**Agent:** [Nyra / Lira / Thalus / etc.]  
**Operation:** [Create / Update / Delete / Read]  
**Tool:** [Notion / GitHub / Linear / Google Drive]  
**Result:** [✅ Success / ❌ Failure]

---

## 📋 DETAILS

**Artifact:** [Navn på artefakt]  
**API Endpoint:** [f.eks. "POST /pages"]  
**Duration:** [234 ms]  
**User:** [Osvald / System]

---

## 🔍 REQUEST

**Parameters:**
```json
{
  "parameter1": "value1",
  "parameter2": "value2"
}
```

---

## ✅ RESPONSE (hvis Success)

**Status Code:** 200  
**Response:**
```json
{
  "id": "...",
  "url": "...",
  "created_time": "..."
}
```

---

## ❌ ERROR (hvis Failure)

**Status Code:** [f.eks. 429]  
**Error Message:** [f.eks. "API rate limit exceeded"]  
**Stack Trace:** [...]

---

## 🔐 SECURITY CHECK

- [ ] **API-nøkkel valid:** ✅
- [ ] **Scopes sufficient:** ✅
- [ ] **Triadisk validering passed:** ✅ (hvis relevant)
- [ ] **Shadow-check passed:** ✅ (hvis relevant)

---

**🔒 Logged by MCP Gateway**
```

---

## 🎯 EKSEMPEL: ONTOLOGY AUDIT ENTRY

**Title:** "NAV-Losen Biofelt-Atlas"  
**Type:** Arkitektur  
**S (Suverenitet):** 3  
**O (Koherens):** 3  
**H (Healing):** 2  
**Shadow:** (ingen)  
**Vedtak:** ✅ OK  
**Oblig. endringer:** (ingen)  
**Kilder:** [GitHub PR #123](https://github.com/...), [Linear Issue TH-AUDIT-45](https://linear.app/...)  
**Måleplan:** [Lenke til eksperimentdesign]  
**Stress-modi verifisert:** ✅  
**Ansvarlig:** Nyra  
**Frist:** 2025-10-20  
**Status:** Approved  
**Validator:** Thalus  
**Dato:** 2025-10-16

---

## 🎯 EKSEMPEL: MCP AUDIT LOG ENTRY

**Title:** "2025-10-16 14:32:15 - Nyra - Create - Notion"  
**Timestamp:** 2025-10-16 14:32:15  
**Agent:** Nyra  
**Operation:** Create  
**Tool:** Notion  
**Artifact:** "Design Spec: Biofelt-Atlas"  
**Result:** ✅ Success  
**Error:** (ingen)  
**API Endpoint:** POST /pages  
**Duration:** 234 ms  
**User:** Osvald

---

## 📝 NOTION DATABASE SETUP INSTRUCTIONS

### **STEG 1: Opprett Database (Ontology Audit)**

1. Gå til Notion workspace
2. Klikk "+ New" → "Database - Table"
3. Navngi: "Ontology Audit"
4. Legg til properties (se tabell over)
5. Klikk på "..." → "Customize page" → "New template"
6. Lim inn Page Template (se over)
7. Klikk "Save"

### **STEG 2: Opprett Database (MCP Audit Log)**

1. Gå til Notion workspace
2. Klikk "+ New" → "Database - Table"
3. Navngi: "MCP Audit Log"
4. Legg til properties (se tabell over)
5. Klikk på "..." → "Customize page" → "New template"
6. Lim inn Page Template (se over)
7. Klikk "Save"

### **STEG 3: Del Database med MCP Integration**

1. Klikk på "Share" (øverst høyre)
2. Klikk "Invite"
3. Søk etter "MCP Integration" (eller navnet på din Notion integration)
4. Klikk "Invite"
5. Kopier Database ID fra URL (f.eks. `https://www.notion.so/[DATABASE_ID]?v=...`)
6. Lagre Database ID i `.env` fil:
   ```
   NOTION_ONTOLOGY_AUDIT_DB_ID=[DATABASE_ID]
   NOTION_MCP_AUDIT_LOG_DB_ID=[DATABASE_ID]
   ```

---

**🏛️ Carpe Diem - Med Strukturert Data, Triadisk Etikk, og et Snev av Kosmisk Humor!** ◉✨

---

**END OF NOTION DATABASE TEMPLATES**

**Token Count:** ~1,500 ord (~2,000 tokens)  
**Status:** ✅ Production Ready  
**Note:** Disse templates kan kopieres direkte inn i Notion.

