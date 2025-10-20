# NAV-Losen System Building Guide for Orion & Lira

**Til:** Orion (Agent #1, Meta-Koordinator) & Lira (Agent #2, Empatisk Healer)
**Fra:** Manus (Agent #8, Infrastruktur Hub)
**Dato:** 20. oktober 2025
**Formål:** Gi Orion og Lira all informasjon de trenger for å veilede Osvald gjennom byggingen av NAV-Losen-systemet

---

## 🌟 Målsetting

Dette dokumentet gir Orion (strategisk koordinering) og Lira (empatisk veiledning) en **komplett informasjonspakke** for å guide Osvald gjennom byggingen av NAV-Losen MVP. Dokumentet inkluderer teknisk arkitektur, implementeringsplan, prioritert backlog, beslutningspunkter, ressurser og suksesskriterier.

---

## 📊 EXECUTIVE SUMMARY

**NAV-Losen Status (20. oktober 2025):**

* ✅ **Arkitektur definert:** Gradient Presence Architecture (Alternativ 2, Orion's anbefaling)
* ✅ **Mestringsside designet:** HWF-inspirert, 100 følelsesord, 6-fase brukerflyt
* ✅ **Teknisk stack valgt:** React Native, Netlify, MkDocs, Firebase/Supabase
* ✅ **Competitive analysis fullført:** Falcon + Aurora (Nordic first-mover advantage)
* ⏳ **Implementering:** Ikke startet (venter på Osvald's beslutning)

**Kritiske Beslutninger Osvald Må Ta:**

1. **Godkjenne Alternativ 2** (Gradient Presence Architecture)
2. **Velge backend** (Firebase vs. Supabase)
3. **Velge AI-provider** (OpenAI vs. Anthropic vs. Gemini vs. hybrid)
4. **Prioritere MVP-features** (hvilke 3 agenter først?)

---

## 1. TEKNISK ARKITEKTUR

### 1.1 Gradient Presence Architecture (Alternativ 2)

**Konsept:** Agenter har "hjemme-domener", men universell tilgang via MCP Broker.

**5 Agenter i MVP:**

1. **Orion** (Dashboard, strategisk oversikt)
2. **Lira** (Mestring, empatisk healing)
3. **Thalus** (Veiledning, etisk validering)
4. **Zara** (Sikkerhet, data-integritet) - *passiv i MVP*
5. **Nyra** (Design, UX) - *passiv i MVP*

**Arkitektur-Komponenter:**

```
USER
 └── LIRA HUB
       └── MCP BROKER
            ├── ORION
            ├── LIRA
            └── THALUS
```

**Informasjonsflyt:**

1. Bruker → Lira Hub (biofelt-filter)
2. Lira → MCP Broker (routing)
3. MCP Broker → Relevant Agent (Orion/Lira/Thalus)
4. Agent → Lira Hub (validering)
5. Lira → Bruker (empatisk levering)

### 1.2 Teknisk Stack

**Frontend:** React Native, MkDocs, Netlify
**Backend:** Supabase anbefalt (GDPR-vennlig)
**AI-Providers:**

* Lira: ChatGPT-5
* Orion: Claude Sonnet 4.5
* Thalus: Grok-4
* Nyra: Gemini 2.5 Flash
* Zara: Claude Opus

**Memory Levels:**

* L1: LocalStorage
* L2: Supabase/Firebase
* L3: GitHub
* L4: Google Drive + NotebookLM
* L5: Notion + Linear

**Integrasjoner:** Health Connect, NAV API, Polyvagal Tracking

### 1.3 Mestringsside (HWF-Inspirert)

**6-Fase Brukerflyt:**

1. Velkomst
2. Fire Kvadranter
3. Følelseshjul (100 former)
4. Definisjon + Trykk/Kroppssignaler
5. Lira Chatbot-initiering
6. Dypere dialog & anbefaling

---

## 2. IMPLEMENTERINGSPLAN

**Fase 1a:** MVP Foundation (Uke 1-4)
**Fase 1b:** Agent Coalition (Uke 5-8)
**Fase 2:** NAV Integration (Uke 9-12)
**Fase 3:** Polyvagal & Biofelt (Uke 13-16)

---

## 3. PRIORITERT BACKLOG

**Høy:** Mestringsside, Lira, Orion, Thalus, MCP Broker, Supabase, Health Connect, Triadic Ethics
**Medium:** NAV API, Bureaucratic Stress Modul, Ring Veileder, Mastery Log
**Lav:** Polyvagal Tracking, Biofelt Dashboard, RAIN Practice, Zara, Aurora

---

## 4. BESLUTNINGSPUNKTER

**D1:** Godkjenne Alternativ 2
**D2:** Velge backend (anbefalt: Supabase)
**D3:** Velge AI-provider for Lira (anbefalt: ChatGPT-5)
**D4:** Velge MVP-nivå (anbefalt: Balansert)

---

## 5. RESSURSER OG VERKTØY

**GitHub:** `/homo-lumen-compendiums/`
**Notion:** Dashboard og arkitektur
**Google Drive + NotebookLM:** Research
**Verktøy:** VS Code, Expo, Supabase CLI, MkDocs, Figma, Mermaid, ChatGPT-5, Claude, Grok

---

## 6. SUKSESSKRITERIER

* Brukeropplevelse: trygg, rask, empatisk
* Teknisk: stabilt, skalerbart, GDPR-kompatibelt
* Etisk: validering via Triadic Ethics (Port 1-2-3)

---

## 7. RISIKO OG MITIGERING

**Høy:** Kompleksitet, API-kostnad, NAV-tilgang
**Medium:** Health Connect-integrasjon, MCP routing
**Lav:** Netlify deploy, Supabase ytelse

---

## 8. ORION'S STRATEGISKE VEILEDNING

* Planlegging, oversikt, oppgavebryting
* Daglige strategiske innsjekk
* Triadic-etikksjekk ved beslutninger

---

## 9. LIRA'S EMPATISKE VEILEDNING

* Pust, innsjekk, trygghet
* Emosjonell støtte, validering, RAIN-protokoll

---

## 10. NESTE STEG

1. Les dokumentet
2. Ta beslutninger D1-D4
3. Osvald gir tilbakemelding til Orion & Lira

---

**Forfatter:** Manus (Agent #8)
**Dato:** 20. oktober 2025
**Status:** ✅ KLAR FOR DISTRIBUSJON
