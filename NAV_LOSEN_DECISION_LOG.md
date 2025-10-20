# NAV-LOSEN DECISION LOG

**Opprettet:** 20. oktober 2025  
**Sist oppdatert:** 20. oktober 2025  
**Eier:** Osvald P. A. Johansen  
**Koordinator:** Orion (Agent #1)

---

## 20. oktober 2025

### **D1: OS-Positioning**
- **Beslutning:** Presentere som Homo Lumen OS (ikke bare app)
- **Rationale:** Bredere visjon, skalerbar arkitektur
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

### **D2: Delt SMK**
- **Beslutning:** Samme Git-repo + Supabase for begge manifestasjoner
- **Rationale:** Læring flyter mellom R&D og Produkt
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

### **D3: MVP Scope**
- **Beslutning:** 3 agenter (Lira, Orion, Thalus) i MVP
- **Rationale:** Pragmatisk, rask iterasjon
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

### **D4: Data Firewall**
- **Beslutning:** Tvedestrand-data ALDRI til Homo Lumen
- **Rationale:** GDPR-compliance, bruker-tillit
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

### **D5: Implementeringsmodell**
- **Beslutning:** Alternativ B (Parallell Light)
- **Rationale:** Balanse mellom visjon og pragmatisme
- **Budget:** 160K NOK
- **Timeline:** 8 uker
- **Pilot:** Tvedestrand uke 4 (5 brukere)
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

### **D6: Backend**
- **Beslutning:** Supabase
- **Rationale:** Open-source, GDPR-compliant, PostgreSQL-basert, real-time subscriptions
- **Alternativer vurdert:** Firebase (avvist pga. Google-eierskap)
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

### **D7: Mobile App**
- **Beslutning:** React Native + Expo
- **Rationale:** Rask prototyping, cross-platform, stor community
- **Alternativer vurdert:** Flutter (avvist pga. mindre MCP-støtte)
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

### **D8: Web Console**
- **Beslutning:** Next.js/React
- **Rationale:** Homo Lumen OS trenger web-basert console for agent-interaksjon
- **Godkjent av:** Osvald
- **Dato:** 20. oktober 2025

---

## Implementeringsplan

### **Fase 1a: MVP Foundation (Uke 1-4)**
- Supabase backend
- React Native app (NAV-Losen)
- Web Console (Homo Lumen OS)
- Mestringsside (Fase 1-6)
- Lira chatbot (ChatGPT-5)
- Pilot: 5 brukere i Tvedestrand

### **Fase 1b: Agent Coalition (Uke 5-8)**
- MCP Broker (lightweight routing)
- Orion Dashboard
- Thalus Veiledning
- SMK-logger (Git + Supabase)
- Demo: Offentlig presentasjon

---

## Teknisk Stack

**Backend:**
- Supabase (PostgreSQL + Auth + Edge Functions)

**Frontend:**
- React Native + Expo (NAV-Losen mobile)
- Next.js/React (Homo Lumen OS web console)

**AI:**
- ChatGPT-5 (Lira)
- Claude Sonnet 4.5 (Orion)
- Grok 3 (Thalus)

**Infrastruktur:**
- Git (SMK-arkitektur)
- Netlify (deployment)
- MCP Broker (agent routing)

---

## Neste Steg

**Dag 1-2 (20-21. oktober):**
1. Opprett Supabase-prosjekt
2. Definer database schema
3. Sett opp React Native-prosjekt (Expo)
4. Sett opp Web Console-prosjekt (Next.js)
5. Implementer data firewall

**Dag 3-5 (22-24. oktober):**
1. Implementer MCP Broker
2. Integrer API-endpoints
3. Lag SMK-logger

**Dag 6-7 (25-26. oktober):**
1. Test setup med dummy data
2. Deploy til Netlify (staging)
3. Forbered uke 2 (Mestringsside implementering)

---

## Referanser

- [System Building Guide](./techdocs-source/archive/manus-session-2025-10-20/SYSTEM_BUILDING_GUIDE_FOR_ORION_AND_LIRA_SUMMARY.md)
- [SMK #027: Superposisjon-Arkitektur](./techdocs-source/archive/manus-session-2025-10-20/SMK_027_SUPERPOSISJON_ARKITEKTUR.md)
- [Orion Decision Synthesis](./techdocs-source/archive/manus-session-2025-10-20/ORION_DECISION_SYNTHESIS_AGENT_MAPPING.md)
- [Linear Issues](https://linear.app/homo-lumen)

---

**Versjon:** 1.0  
**Status:** Aktiv  
**Neste gjennomgang:** 27. oktober 2025 (etter uke 1)

