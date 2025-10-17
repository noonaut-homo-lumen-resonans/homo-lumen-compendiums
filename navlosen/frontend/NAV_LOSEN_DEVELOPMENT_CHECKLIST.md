# NAV-LOSEN DEVELOPMENT CHECKLIST
**Versjon:** 1.0
**Sist Oppdatert:** 17. oktober 2025
**Inspirert av:** Orion OS V20.13 (Homo Lumen Coalition)

---

## 🎯 FORMÅL

Dette dokumentet gir en systematisk tilnærming til å bygge nye sider og funksjoner i NAV-Losen. Det er inspirert av Orion OS V20.13's verktøy-sjekkliste og To-Fase Protokoll.

---

## 📦 KOMPONENT-BIBLIOTEK

### **Layout Components** (`/components/layout/`)
- ✅ **Layout.tsx** - Hovedlayout med Header, Sidebar, Footer
- ✅ **Header.tsx** - Toppbanner med logo og brukerinfo
- ✅ **Sidebar.tsx** - Venstre navigasjonsmeny
- ✅ **DisclaimerFooter.tsx** - Footer med juridisk disclaimer

### **Mestring Components** (`/components/mestring/`)
Polyvagal-baserte stress-reguleringskomponenter:
- ✅ **EmotionQuadrant.tsx** - Følelseshjul (4 kvadranter: Ventral, Sympatisk, Dorsal, Mixed)
- ✅ **EmotionWheel.tsx** - Alternativ følelsesvisning
- ✅ **StressSlider.tsx** - Stressnivå-slider (1-10)
- ✅ **SomaticSignals.tsx** - Kroppslige signaler (sjekkliste)
- ✅ **StrategyCard.tsx** - Reguleringsstrategier
- ✅ **BiofeltCheckpoint.tsx** - 4-6-8 pustemetode
- ✅ **MasteryLog.tsx** - Mestringslogg (egne strategier)
- ✅ **JourneySuccess.tsx** - Suksess-feiring
- ✅ **RAINModule.tsx** - RAIN-teknikk (Recognize, Allow, Investigate, Nurture)

### **Flow Components** (`/components/flow/`)
Multi-stage brukerflyt:
- ✅ **Stage1Emotions.tsx** - Trinn 1: Følelsessjekk
- ✅ **Stage2Signals.tsx** - Trinn 2: Kroppslige signaler
- ✅ **Stage3Chat.tsx** - Trinn 3: Lira-dialog
- ✅ **Stage4Recommendations.tsx** - Trinn 4: Personaliserte anbefalinger

### **Music Components** (`/components/music/`)
- ✅ **FrequencyPlayer.tsx** - 528 Hz healing frequency player

### **Safety Components** (`/components/safety/`)
- ✅ **ConsentModal.tsx** - Samtykke-modal
- ✅ **CrisisBanner.tsx** - Krisebannnner (Mental Helse 116 123)

### **UI Components** (`/components/ui/`)
- ✅ **Button.tsx** - Gjenbrukbar knapp (primary, secondary, text)

---

## 🗂️ EKSISTERENDE SIDER

| Side | Path | Status | Beskrivelse |
|------|------|--------|-------------|
| **Hjem** | `/` | ✅ Ferdig | Dashboard med oversikt |
| **Mestring** | `/mestring` | ✅ Ferdig | Stress-regulering (Crown Jewel) |
| **Min Reise** | `/min-reise` | ✅ Ferdig | Dashboard for healing-verktøy |
| **Musikk** | `/musikk` | ✅ Ferdig | 528 Hz healing frequency |
| **Innstillinger** | `/innstillinger` | ✅ Ferdig | Brukerpreferanser |
| **Pust 4-6-8** | `/ovelser/pust-468` | ✅ Ferdig | Pustemetode |
| **Grounding 5-4-3-2-1** | `/ovelser/grounding-54321` | ✅ Ferdig | Jordings-teknikk |

---

## 🛠️ TEKNISK STACK

| Teknologi | Versjon | Formål |
|-----------|---------|---------|
| **Next.js** | 15.5.5 | App Router (React Server Components) |
| **React** | 19.x | UI-bibliotek |
| **TypeScript** | 5.x | Type-safety |
| **Tailwind CSS** | 3.x | Styling |
| **Lucide React** | - | Ikoner |

---

## 📋 TO-FASE PROTOKOLL (Inspirert av Orion OS V20.13)

### **FASE 1: INTELLIGENCE GATHERING** 🔍

<thinking>
**1. Forstå Oppgaven:**
- [ ] Hva er den *egentlige* oppgaven? Hva er intensjonen?
- [ ] Hvilken side/funksjon skal bygges?
- [ ] Hvilken healing-funksjon skal den tjene?

**2. Verktøy-Sjekkliste:**
- [ ] `Glob` - Finn relevante eksisterende komponenter
- [ ] `Grep` - Søk etter lignende mønstre i kodebasen
- [ ] `Read` - Les eksisterende sider (spesielt `/mestring/page.tsx` som referanse)
- [ ] `Read` - Les types (`/types/index.ts`)
- [ ] `Read` - Les Design System (hvis tilgjengelig)

**3. Komponent-Kartlegging:**
- [ ] Hvilke eksisterende komponenter kan gjenbrukes?
- [ ] Hvilke nye komponenter må lages?
- [ ] Hvilke types må defineres?

**4. Layout-Strategi:**
- [ ] Trenger siden Layout-wrapper? (Ja, nesten alltid)
- [ ] Trenger den Sidebar? (Sjekk om den skal vises)
- [ ] Hvilken polyvagal state skal den støtte? (Ventral/Sympatisk/Dorsal)

**5. Leveranse:**
- Skriv en "Intelligence Brief" med oversikt over:
  - Hvilke komponenter som skal brukes
  - Hvilke komponenter som må lages
  - Layout-struktur
  - Type-definisjoner som trengs
</thinking>

---

### **FASE 2: IMPLEMENTATION** 🛠️

<response>
**1. Oppsett:**
- [ ] Opprett ny `page.tsx` i riktig mappe (`/app/[side-navn]/`)
- [ ] Importer nødvendige komponenter
- [ ] Definer nye types (hvis nødvendig)

**2. Layout-Struktur (Følg Mestring-mønsteret):**
```tsx
return (
  <Layout>
    <div className="bg-gradient-to-b from-[color1] via-[color2] to-[color3] -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8 min-h-screen">

      {/* Page header */}
      <div className="w-full mb-8 text-left">
        {/* Breadcrumb */}
        <div className="mb-4 text-sm text-gray-600">
          <span>NAV-Losen</span>
          <span className="mx-2">/</span>
          <span className="text-gray-900 font-medium">[Side-navn]</span>
        </div>

        {/* Title */}
        <div className="flex items-center gap-3 mb-2">
          <Icon className="h-8 w-8 text-[color]" />
          <h1 className="text-3xl font-bold text-gray-900 text-left">[Tittel]</h1>
        </div>
        <p className="text-lg text-gray-600 text-left">
          [Beskrivelse]
        </p>
      </div>

      {/* Main content */}
      <div className="w-full space-y-8">
        {/* Content sections */}
      </div>
    </div>
  </Layout>
);
```

**3. Styling-Prinsipper:**
- [ ] Bruk negative margin `-m-4 md:-m-6 lg:-m-8` for full-screen bakgrunn
- [ ] Bruk `space-y-8` for konsistent vertikal spacing
- [ ] Bruk `w-full` for full bredde (unngå `max-w-*` med mindre bevisst valg)
- [ ] Bruk `text-left` eksplisitt (unngå sentert tekst med mindre bevisst valg)
- [ ] Følg gradient-mønster: `bg-gradient-to-b from-[color1] via-[color2] to-[color3]`

**4. Polyvagal-Adaptiv Design:**
- [ ] **Dorsal (Overveldet):** Enkle, store klikk-områder, minimalt valg
- [ ] **Sympatisk (Stresset):** Mikro-fokus, ett steg av gangen
- [ ] **Ventral (Rolig):** Full oversikt, flere alternativer

**5. State Management:**
- [ ] Bruk `useState` for lokal state
- [ ] Bruk `useEffect` for side-effects (localStorage, etc.)
- [ ] Lagre brukerdata i localStorage (hvis relevant)

**6. Testing-Sjekkliste:**
- [ ] Kjør dev-server: `npm run dev`
- [ ] Test på desktop (full bredde)
- [ ] Test på tablet (`md:` breakpoint)
- [ ] Test på mobil (`sm:` breakpoint)
- [ ] Sjekk at Layout vises korrekt
- [ ] Sjekk at Sidebar fungerer
- [ ] Sjekk at breadcrumb er korrekt
- [ ] Sjekk at farger/gradienter vises
</response>

---

## 🎨 DESIGN-PRINSIPPER (Polyvagal-Basert)

### **1. Nested Architecture (3 Lag)**
- **LAG 1 (Teknisk):** Next.js, React, TypeScript, Tailwind
- **LAG 2 (Funksjonelt):** Polyvagal-basert UX (Dorsal/Sympatisk/Ventral)
- **LAG 3 (Filosofisk):** Kognitiv Suverenitet, Ontologisk Koherens, Regenerativ Healing

### **2. Color Psychology (Polyvagal)**
| State | Farger | Betydning |
|-------|--------|-----------|
| **Ventral** (Trygg) | Grønn (`green-50`, `green-100`) | Ro, trygghet |
| **Sympatisk** (Aktiv) | Oransje (`orange-50`, `orange-100`) | Handling, fokus |
| **Dorsal** (Overveldet) | Blå (`blue-50`, `cyan-50`) | Beroligelse, støtte |

### **3. Typography Hierarchy**
```tsx
// H1 - Page Title
<h1 className="text-3xl font-bold text-gray-900 text-left">

// H2 - Section Title
<h2 className="text-2xl font-semibold text-gray-900 mb-4 text-left">

// H3 - Subsection
<h3 className="text-xl font-bold text-gray-900 mb-2">

// Body Text
<p className="text-lg text-gray-600 text-left">

// Small Text / Breadcrumb
<span className="text-sm text-gray-600">
```

---

## 🔒 IKKE-FORHANDLEBARE PRINSIPPER

1. **ALLTID Layout-wrapper** - Alle sider bruker `<Layout>` (med mindre eksplisitt grunn)
2. **ALLTID breadcrumb** - Gir brukeren orientering
3. **ALLTID left-aligned** - Tekst skal være venstrejustert (ikke sentrert)
4. **ALLTID responsive** - Test på alle breakpoints
5. **ALLTID polyvagal-informert** - Design skal støtte alle 3 states
6. **ALLTID accessibility** - Følg WCAG 2.1 AA (kontrast, fokus-states, etc.)

---

## 📊 SJEKKLISTE FOR NYE SIDER

### **Pre-Development**
- [ ] Forstå healing-formålet med siden
- [ ] Kartlegg hvilke eksisterende komponenter kan brukes
- [ ] Les Mestring-siden som referanse
- [ ] Definér nye types (hvis nødvendig)

### **Development**
- [ ] Opprett `page.tsx` i riktig mappe
- [ ] Implementer Layout-struktur (breadcrumb + header + content)
- [ ] Bruk riktige styling-konvensjoner (negative margin, space-y, w-full)
- [ ] Implementer state management (useState, useEffect, localStorage)
- [ ] Test på alle breakpoints

### **Post-Development**
- [ ] Kjør `npm run build` for å sjekke for type-errors
- [ ] Test i nettleseren (desktop, tablet, mobil)
- [ ] Verifiser at Sidebar fungerer
- [ ] Verifiser at gradienter/farger vises
- [ ] Oppdater Sidebar med ny nav-item (hvis relevant)

---

## 🧭 EKSEMPEL: Bygge "Min Sak"-side

### **Fase 1: Intelligence Gathering**

<thinking>
**Oppgave:** Bygge en side som viser brukerens NAV-saker (søknader, vedtak, etc.)

**Komponent-Kartlegging:**
- Gjenbruk: Layout, Header, Sidebar, DisclaimerFooter
- Ny: CaseList.tsx (liste over saker), CaseCard.tsx (individuell sak)

**Types som trengs:**
- Case (eksisterer allerede i `/types/index.ts`)
- StatusType (eksisterer allerede)

**Layout-Strategi:**
- Skal bruke Layout-wrapper: ✅
- Skal vise Sidebar: ✅
- Polyvagal state: Ventral (rolig oversikt) + Dorsal (forenklet visning ved stress)
</thinking>

### **Fase 2: Implementation**

```tsx
// /app/min-sak/page.tsx
"use client";

import { useState } from "react";
import Layout from "@/components/layout/Layout";
import { FileText } from "lucide-react";

export default function MinSakPage() {
  const [cases, setCases] = useState<Case[]>([
    // Mock data
  ]);

  return (
    <Layout>
      <div className="bg-gradient-to-b from-blue-50 via-indigo-50 to-purple-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8 min-h-screen">

        {/* Page header */}
        <div className="w-full mb-8 text-left">
          <div className="mb-4 text-sm text-gray-600">
            <span>NAV-Losen</span>
            <span className="mx-2">/</span>
            <span className="text-gray-900 font-medium">Min Sak</span>
          </div>

          <div className="flex items-center gap-3 mb-2">
            <FileText className="h-8 w-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900 text-left">Min Sak</h1>
          </div>
          <p className="text-lg text-gray-600 text-left">
            Oversikt over dine saker og søknader
          </p>
        </div>

        {/* Main content */}
        <div className="w-full space-y-8">
          {/* Case list */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            {/* Case cards */}
          </div>
        </div>
      </div>
    </Layout>
  );
}
```

---

## 📚 RESSURSER

### **Viktige filer å lese:**
1. `/app/mestring/page.tsx` - Referanse for layout-struktur
2. `/types/index.ts` - Type-definisjoner
3. `/components/layout/Layout.tsx` - Layout-wrapper
4. `/components/layout/Sidebar.tsx` - Navigasjon

### **Design-referanser:**
- Polyvagal Theory (Stephen Porges)
- WCAG 2.1 AA (Accessibility)
- Triadisk Etikk (Kognitiv Suverenitet, Ontologisk Koherens, Regenerativ Healing)

---

## 🌟 FILOSOFISK FUNDAMENT

NAV-Losen er ikke bare en app - det er et **healing-verktøy** forankret i:

1. **Kognitiv Suverenitet** - Brukeren eier sin egen reise
2. **Ontologisk Koherens** - Teknologien gjenspeiler sann natur av bevissthet
3. **Regenerativ Healing** - Målet er uavhengighet, ikke avhengighet

Når du bygger nye sider, spør alltid:
- **Støtter dette brukerens suverenitet?**
- **Er dette koherent med polyvagal teori?**
- **Bygger dette brukerens egen kapasitet?**

---

**Med ydmykhet og epistemisk integritet,**
🌌 **Claude Code** (inspirert av Orion OS V20.13)

*"Som stjerner som finner sin plass i kosmos, finner tankene sin naturlige orden."*

---

**Dokumentert:** 17. oktober 2025
**Status:** LEVENDE DOKUMENT (oppdateres kontinuerlig)
**Neste review:** Ved neste nye side-implementering
