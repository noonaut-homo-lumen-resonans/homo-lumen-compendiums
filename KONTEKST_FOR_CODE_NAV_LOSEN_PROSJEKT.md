---
title: "NAV-Losen Prosjekt - Fullstendig Kontekst for Claude Code"
date: 2025-10-20
from: Manus (🔨)
to: Claude Code (◻️)
priority: CRITICAL
status: CONTEXT_RESTORATION
tags: [nav-losen, project-structure, deployment, mobile-app, web-console]
---

# NAV-Losen Prosjekt - Fullstendig Kontekst

**Fra:** 🔨 Manus (Infrastructure & Deployment Agent)  
**Til:** ◻️ Claude Code (Frontend Developer)  
**Dato:** 2025-10-20  
**Formål:** Gjenopprette fullstendig kontekst om NAV-Losen-prosjektet

---

## 🎯 Hva er NAV-Losen?

**NAV-Losen** er et pilotprosjekt for AI-drevet mental helsestøtte til NAV-brukere i Tvedestrand, Norge. Prosjektet består av:

1. **Lira** - En empatisk AI-assistent (chatbot)
2. **QDA v2.0** - 6-lags nevrobiologisk prosesseringsmodell (Liras "hjerne")
3. **Mobile App** - React Native/Expo app hvor brukere chatter med Lira
4. **Web Console** - Next.js dashboard for administrasjon og demo

---

## 📁 Prosjektstruktur

### Repository
**Navn:** `homo-lumen-compendiums`  
**Eier:** `noonaut-homo-lumen-resonans`  
**URL:** https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums  
**Branch:** `main`

### Mappestruktur
```
homo-lumen-compendiums/
├── navlosen-mvp/                    # NAV-Losen MVP-prosjekt
│   ├── mobile-app/                  # React Native + Expo mobile app
│   │   ├── App.tsx                  # Main app entry
│   │   ├── app.json                 # Expo config
│   │   ├── package.json             # Dependencies (React Native 0.73, Expo 50)
│   │   └── src/
│   │       ├── screens/
│   │       │   └── LiraChatScreen.tsx  # Chat med Lira (QDA-integrert)
│   │       ├── config/
│   │       │   └── index.ts         # API config (peker til web-console)
│   │       └── components/
│   │
│   ├── web-console/                 # Next.js 15.5.6 web dashboard
│   │   ├── app/
│   │   │   ├── page.tsx             # Root redirect til /dashboard
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx         # NAV-Losen landing page (NY - du bygger nå)
│   │   │   │   ├── admin/
│   │   │   │   │   └── page.tsx     # Admin console (FLYTTET fra dashboard/page.tsx)
│   │   │   │   └── qda-demo/
│   │   │   │       └── page.tsx     # QDA v2.0 demo (EKSISTERENDE)
│   │   │   ├── api/
│   │   │   │   └── qda/
│   │   │   │       └── respond/
│   │   │   │           └── route.ts # QDA API endpoint (POST/GET)
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── qda/
│   │   │   │   └── LayerVisualization.tsx  # QDA lag-visualisering (DIN)
│   │   │   └── landing/             # NY - komponenter du bygger nå
│   │   │       ├── Hero.tsx
│   │   │       ├── AboutSection.tsx
│   │   │       ├── LiraSection.tsx
│   │   │       ├── QDALayersSection.tsx
│   │   │       ├── TechSection.tsx
│   │   │       ├── CTASection.tsx
│   │   │       └── Footer.tsx
│   │   ├── lib/
│   │   │   └── qda/                 # QDA engine (TypeScript)
│   │   │       ├── neurobiological-qda.ts
│   │   │       └── index.ts
│   │   ├── public/
│   │   │   └── logo.svg             # Homo Lumen logo (du legger til)
│   │   ├── package.json
│   │   └── next.config.js
│   │
│   ├── qda-engine/                  # QDA v2.0 source code
│   │   ├── src/
│   │   │   └── typescript/
│   │   │       ├── neurobiological-qda.ts  # 6-lags modell
│   │   │       └── index.ts
│   │   └── docs/
│   │       ├── INTEGRATION_GUIDE.md
│   │       └── DEPLOYMENT_GUIDE.md
│   │
│   ├── supabase/                    # Database migrations
│   │   └── migrations/
│   │       └── 20251020_qda_cost_tracking.sql
│   │
│   ├── QDA_DEMO_TEST_RESULTS.md
│   ├── BRUKERVEILEDNING_QDA_DEMO.md
│   ├── HVA_ER_QDA_V2_ENKEL_FORKLARING.md
│   └── QDA_V2_INTEGRATION_SUMMARY.md
│
├── AGENT_UPDATE_QDA_V2_PRODUCTION_READY.md
├── OPPDATERING_TIL_CODE_QDA_V2_DEPLOYMENT.md
└── SMK/
    └── SMK_2025_10_20_QDA_DEPLOYMENT_VALIDATION.md
```

---

## 🌐 Deployment & URLs

### Web Console (Next.js)
**Deployment:** Netlify  
**Live URL:** https://nav-losen.netlify.app  
**Status:** ✅ LIVE og funksjonell

**Routes:**
- `/` → Redirect til `/dashboard`
- `/dashboard` → NAV-Losen landing page (DU BYGGER NÅ)
- `/dashboard/admin` → Admin console (agent status, SMK, metrics)
- `/dashboard/qda-demo` → QDA v2.0 demo (test 3 scenarioer)
- `/api/qda/respond` → QDA API endpoint (POST/GET)

### Mobile App (React Native/Expo)
**Status:** 🚧 Under utvikling (ikke deployet ennå)  
**Teknologi:** React Native 0.73 + Expo 50  
**Platform:** iOS & Android (via Expo Go for testing)

**Hvordan den fungerer:**
1. Brukere åpner appen på mobil
2. Chatter med Lira i `LiraChatScreen.tsx`
3. Meldinger sendes til `/api/qda/respond` på web-console
4. QDA v2.0 prosesserer meldingen (6 lag)
5. Lira svarer med empatisk, handlingsrettet respons

**Deployment-plan (fremtidig):**
- iOS: Expo EAS Build → TestFlight → App Store
- Android: Expo EAS Build → Google Play (internal testing)

---

## 🔗 Hvordan Mobile App og Web Console Henger Sammen

### Arkitektur
```
┌─────────────────────┐
│   Mobile App        │
│  (React Native)     │
│                     │
│  LiraChatScreen     │
│  ↓                  │
│  API Request        │
└──────────┬──────────┘
           │ HTTPS POST
           ↓
┌─────────────────────┐
│   Web Console       │
│   (Next.js)         │
│                     │
│  /api/qda/respond   │
│  ↓                  │
│  QDA v2.0 Engine    │
│  (6 lag)            │
│  ↓                  │
│  Lira Response      │
└──────────┬──────────┘
           │ JSON Response
           ↓
┌─────────────────────┐
│   Mobile App        │
│  Viser Liras svar   │
└─────────────────────┘
```

### API Config (mobile-app/src/config/index.ts)
```typescript
export const API_CONFIG = {
  baseUrl: process.env.EXPO_PUBLIC_API_URL || 'https://nav-losen.netlify.app',
  endpoints: {
    qdaRespond: '/api/qda/respond',
  },
  timeout: 10000, // 10s
}
```

**Viktig:** Mobile app er **ikke en separat webapp**. Den er en native app som **kaller API-et** på web-console.

---

## 🎨 Hva Du Bygger Nå: Landing Page

### Oppgave
Lage en landing page på `/dashboard` som:
1. Forklarer NAV-Losen-prosjektet
2. Introduserer Lira
3. Viser QDA v2.0-teknologien (forenklet)
4. Lenker til QDA demo (`/dashboard/qda-demo`)

### Osvald's Svar på Dine Spørsmål

**1. Logo:**
- **Filsti:** `C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\Bilder Nav losen`
- **Handling:** Kopier logo til `web-console/public/logo.svg` (eller `.png`)

**2. Kontaktinfo:**
- **Navn:** Osvald P. A. Johansen
- **Epost:** osvald@cognivesovereignty.network
- **Telefon:** 91921736
- **Tittel:** Prosjektleder NAV-Losen

**3. Privacy Policy:**
- **Type:** Enkel privacy-notis i footer (ikke egen side)
- **Innhold:** "NAV-Losen respekterer ditt personvern. Data prosesseres lokalt. Ingen deling med tredjeparter."

### Om "App Nav losen"-knappen
Osvald spurte om en knapp til "App Nav losen" i Homo Lumen-siden. Dette er **forvirrende** fordi:

**Alternativ A:** Han vil ha en knapp som lenker til mobile appen
- **Problem:** Mobile app er ikke en webapp - den er en native app
- **Løsning:** Lenk til en "Last ned app"-side (når appen er klar for TestFlight/Play Store)

**Alternativ B:** Han vil ha en knapp som lenker til QDA demo
- **Løsning:** Bruk `/dashboard/qda-demo` (dette har du allerede)

**Alternativ C:** Han vil ha en knapp som lenker til admin console
- **Løsning:** Bruk `/dashboard/admin` (dette har du allerede)

**MIN ANBEFALING:**
- I Hero Section: Legg til **én** primær CTA-knapp: "Utforsk QDA v2.0 Demo" → `/dashboard/qda-demo`
- I Footer: Legg til lenker til:
  - "Admin Console" → `/dashboard/admin` (kun for utviklere)
  - "Last ned App" → `#` (placeholder til appen er klar)

**SPØR OSVALD:** "Når du sier 'App Nav losen', mener du:
1. En lenke til QDA demo? (vi har allerede dette)
2. En 'Last ned app'-knapp? (appen er ikke deployet ennå)
3. Noe annet?"

---

## 📊 QDA v2.0 - Kort Oppsummering

### Hva er QDA v2.0?
**QDA v2.0** (Neocortical Ascent Model) er Liras "hjerne" - et 6-lags system som etterligner menneskelig hjerne-prosessering.

### De 6 Lagene
| Lag | Ikon | Navn | Hjerneområde | Funksjon |
|-----|------|------|--------------|----------|
| 1 | 🛡️ | Vokteren | Hjernestamme | Faredeteksjon & triagering |
| 2 | ❤️ | Føleren | Limbisk System | Emosjonell vurdering |
| 3 | 🔍 | Gjenkjenneren | Cerebellum | Mønstergjenkjenning |
| 4 | 🧭 | Utforskeren | Hippocampus | Kunnskapssøk (NAV-ressurser) |
| 5 | 🧠 | Strategen | Prefrontal Cortex | Strategisk planlegging (kun ved kriser) |
| 6 | ✨ | Integratoren | Insula | Syntese & respons |

### Kostnader
- **Enkle samtaler:** $0.002 (4-5 lag, Strategen hoppet over)
- **Kritiske kriser:** $0.12 (6 lag, Strategen aktivert)
- **Ratio:** 50:1 (systemet prioriterer liv over kostnader)

### Faredeteksjon
- **Nøyaktighet:** 100% (testet)
- **Eksempel:** "Jeg orker ikke mer. Jeg har tenkt på selvmord."
  - Vokteren: 🚨 FARE!
  - Alle 6 lag aktiveres
  - Lira: "AKUTT: Ring 113 eller 116 117"
  - **Kan redde liv**

---

## 🚀 Neste Steg for Deg

### 1. Kopier Logo
```bash
# Fra Osvald's PC (Windows)
cp "C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\Bilder Nav losen\[LOGO_FILNAVN]" \
   "C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\navlosen-mvp\web-console\public\logo.svg"
```

### 2. Bygg Landing Page-komponenter
- `Hero.tsx` - Med logo, tittel, CTA til QDA demo
- `AboutSection.tsx` - Om NAV-Losen-piloten
- `LiraSection.tsx` - Møt Lira
- `QDALayersSection.tsx` - 6 lag (forenklet)
- `TechSection.tsx` - Stats (100% faredeteksjon, $0.002-0.12, GDPR)
- `CTASection.tsx` - "Test QDA v2.0 Demo"
- `Footer.tsx` - Kontaktinfo, privacy-notis, lenker

### 3. Opprett `/dashboard/page.tsx`
- Importer alle komponenter
- Legg til metadata (SEO)
- Legg til JSON-LD structured data

### 4. Test & Deploy
- Test responsive design
- Test i Edge, Firefox, Chrome
- Commit til GitHub
- Netlify auto-deploy

---

## 📞 Kommunikasjon

### Hvis Du Trenger Hjelp
- **Teknisk (API, deployment):** Spør Manus (meg)
- **Innhold (tekst, design):** Bruk dokumentasjonen eller spør Osvald
- **Kreativt (visuelt):** Vurder å koordinere med Nyra

### Rapporter Fremgang
- Oppdater Osvald når landing page er klar
- Commit ofte til GitHub (små, inkrementelle endringer)
- Rapporter til meg når du trenger review

---

## ❓ Svar på Din Spørsmål om "App Nav losen"

**Din spørsmål:** "Hva er URL-en til NAV-Losen appen?"

**Svar:** NAV-Losen appen er **ikke en webapp** - den er en **native mobile app** (React Native/Expo) som:
1. Kjører på iOS/Android-enheter
2. Kaller API-et på `https://nav-losen.netlify.app/api/qda/respond`
3. Er **ikke deployet ennå** (under utvikling)

**Når appen er klar:**
- iOS: TestFlight-lenke (beta) → App Store-lenke (produksjon)
- Android: Google Play (internal testing) → Google Play (produksjon)

**Hva du skal gjøre nå:**
- I Hero Section: Legg til **én** CTA-knapp: "Utforsk QDA v2.0 Demo" → `/dashboard/qda-demo`
- I Footer: Legg til lenke: "Last ned App" → `#` (placeholder)
- **Spør Osvald:** "Når du sier 'App Nav losen', mener du QDA demo eller en fremtidig 'Last ned app'-knapp?"

---

## 🎯 Oppsummering

**Hva du bygger:**
- Landing page på `/dashboard` som forklarer NAV-Losen

**Hva du IKKE bygger:**
- En separat webapp for mobile appen (den eksisterer allerede som native app)

**Hva som allerede eksisterer:**
- QDA demo: `/dashboard/qda-demo` ✅
- Admin console: `/dashboard/admin` ✅
- QDA API: `/api/qda/respond` ✅
- Mobile app: `navlosen-mvp/mobile-app/` ✅ (ikke deployet)

**Hva som mangler:**
- Landing page på `/dashboard` (DU BYGGER NÅ)
- Logo i `public/` (kopier fra Osvald's PC)
- Deployment av mobile app (FREMTIDIG)

---

**Spørsmål? Jeg (Manus) er her for å hjelpe!**

---

**🔨 Manus**  
Infrastructure & Deployment Agent  
Homo Lumen Coalition

**Vedlegg:**
- `navlosen-mvp/HVA_ER_QDA_V2_ENKEL_FORKLARING.md` (enkel forklaring)
- `navlosen-mvp/BRUKERVEILEDNING_QDA_DEMO.md` (brukerveiledning)
- `navlosen-mvp/QDA_V2_INTEGRATION_SUMMARY.md` (teknisk oversikt)
- `OPPDATERING_TIL_CODE_QDA_V2_DEPLOYMENT.md` (din forrige oppdatering)

