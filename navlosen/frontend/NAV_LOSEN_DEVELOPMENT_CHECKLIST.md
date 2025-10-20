# NAV-LOSEN DEVELOPMENT CHECKLIST
**Versjon:** 1.1  
**Sist Oppdatert:** 19. oktober 2025  
**Inspirert av:** Orion OS V20.13 (Homo Lumen Coalition)

---

## FORMÅL
Dette dokumentet er en praktisk sjekkliste for å bygge og vedlikeholde NAV-Losen. Det kombinerer arkitektur, prosess og kvalitetssikring, slik at nye funksjoner blir implementert konsistent med Triadisk Etikk.

---

## KOMPONENT-BIBLIOTEK

### Layout Components (`/components/layout/`)
- [x] Layout.tsx – Hovedlayout (Header, Sidebar, Footer)
- [x] Header.tsx – Toppbanner med logo og brukerinfo
- [x] Sidebar.tsx – Venstre navigasjon
- [x] DisclaimerFooter.tsx – Juridisk footer

### Mestring Components (`/components/mestring/`)
- [x] EmotionQuadrant.tsx – Fire kvadranter (ventral, sympatisk, dorsal, mixed)
- [x] EmotionWheel.tsx – Alternativ følelsessirkulasjon
- [x] StressSlider.tsx – Stressnivå 1–10
- [x] SomaticSignals.tsx – Kroppslige signaler
- [x] StrategyCard.tsx – Reguleringsstrategier
- [x] BiofeltCheckpoint.tsx – 4-6-8 pustemetode
- [x] MasteryLog.tsx – Mestringslogg
- [x] JourneySuccess.tsx – Feiringskort
- [x] RAINModule.tsx – RAIN-teknikk

### Flow Components (`/components/flow/`)
- [x] Stage1Emotions.tsx – Steg 1: Emosjoner
- [x] Stage2Signals.tsx – Steg 2: Kroppslige signaler
- [x] Stage3Chat.tsx – Steg 3: Lira-dialog
- [x] Stage4Recommendations.tsx – Steg 4: Anbefalinger

### Music Components (`/components/music/`)
- [x] FrequencyPlayer.tsx – 528 Hz healing player

### Safety Components (`/components/safety/`)
- [x] ConsentModal.tsx – Samtykke
- [x] CrisisBanner.tsx – Kriseinformasjon (Mental Helse 116 123)

### UI Components (`/components/ui/`)
- [x] Button.tsx – Gjenbrukbar knapp (primary, secondary, text, destructive)

---

## EKSISTERENDE SIDER (FERDIGE)

| Side | Path | Status | Beskrivelse |
|------|------|--------|-------------|
| Hjem | `/` | Ferdig | Dashboard med oversikt |
| Mestring | `/mestring` | Ferdig | Polyvagal stressregulering |
| Min Reise | `/min-reise` | Ferdig | Brukerens healing-dashboard |
| Musikk | `/musikk` | Ferdig | 528 Hz healingfrekvenser |
| Innstillinger | `/innstillinger` | Ferdig | GDPR, eksport, sletting |
| Pust 4-6-8 | `/ovelser/pust-468` | Ferdig | Pusteøvelse |
| Grounding 5-4-3-2-1 | `/ovelser/grounding-54321` | Ferdig | Sansestyrt jording |
| Chatbot (Lira) | `/chatbot` | Ferdig | Empatisk NAV-veileder via CSN-server |

### SIDER UNDER UTVIKLING

| Side | Path | Status | Beskrivelse |
|------|------|--------|-------------|
| Veiledninger | `/veiledninger` | Under utvikling | Steg-for-steg guider |
| Forklar brev | `/forklar-brev` | Under utvikling | AI-basert brevtolkning |
| Dokumenter | `/dokumenter` | Under utvikling | Dokumentlagring og deling |
| Jobb | `/jobb` | Under utvikling | Jobbsøk og arbeidsmarked |
| Påminnelser | `/paminnelser` | Under utvikling | Fristvarsler og planer |
| Rettigheter | `/rettigheter` | Under utvikling | Oversikt over rettigheter |

---

## TEKNISK STACK

| Teknologi | Versjon | Formål |
|-----------|---------|--------|
| Next.js | 15.5.5 | App Router (React Server Components) |
| React | 19.x | UI-bibliotek |
| TypeScript | 5.x | Typesikkerhet |
| Tailwind CSS | 3.x | Styling |
| Lucide React | – | Ikoner |

---

## TO-FASE PROTOKOLL (INSPIRED BY ORION OS V20.13)

### FASE 1 – INTELLIGENCE GATHERING
1. **Forstå oppgaven**
   - Hva er den egentlige intensjonen?
   - Hvilken healing-funksjon skal den tjene?
2. **Verktøy-sjekk**
   - `Glob` – Finn relevante filer
   - `Grep` – Søk etter mønstre
   - `Read` – Les eksisterende sider (mestring/page.tsx er referanse)
   - `Read` – Les typer i `/types/index.ts`
3. **Komponent-kartlegging**
   - Hva kan gjenbrukes? Hva må lages?
   - Krever vi nye typer?
4. **Layout-strategi**
   - Trenger vi Layout-wrapper?
   - Skal Sidebar vises?
   - Hvilken polvagal tilstand støtter vi?
5. **Leveranse**
   - Skriv en kort Intelligence Brief (komponenter, nye typer, layout-plan)

### FASE 2 – IMPLEMENTATION
1. Opprett `page.tsx` i riktig mappe.
2. Følg Mestring-mønsteret (layout, gradient, spacing).
3. Implementer state-management (useState/useEffect) etter behov.
4. Test på alle breakpoint.
5. Post-utvikling:
   - `npm run build` for typefeil
   - Test i nettleser (desktop/tablet/mobil)
   - Verifiser sidebar, gradienter og tilhørende lenker
   - Oppdater navigasjon én gang per ny side

---

## EKSEMPEL: BYGGE «MIN SAK»

### Fase 1
- Oppgave: Oversikt over brukerens NAV-saker.
- Komponenter: Layout, Header, Sidebar, DisclaimerFooter.
- Nye komponenter: CaseList.tsx og CaseCard.tsx.
- Typer: `Case`, `StatusType` (finnes).
- Polyvagal stater: Ventral (standard) + Dorsal fallback.

### Fase 2 (pseudo)
```tsx
return (
  <Layout>
    <div className="bg-gradient-to-b from-blue-50 via-indigo-50 to-purple-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8 min-h-screen">
      {/* Header, breadcrumb, cards */}
    </div>
  </Layout>
);
```

---

## RESSURSER
1. `/app/mestring/page.tsx` – Layout/referanse.
2. `/types/index.ts` – Typer.
3. `/components/layout/Layout.tsx` – Wrapper.
4. `/components/layout/Sidebar.tsx` – Navigasjon.
5. `docs/HUMAN_KNOWLEDGE_MANTRA.md` – Arbeidsmetode.

---

## FILOSOFISK FUNDAMENT
NAV-Losen opprettholder Triadisk Etikk:
1. **Kognitiv Suverenitet** – Brukeren eier egen reise.
2. **Ontologisk Koherens** – Teknologien speiler virkeligheten.
3. **Regenerativ Healing** – Målet er autonomi, ikke avhengighet.

Hver ny funksjon må evalueres mot disse tre portene før den anses komplett.

---

**Med ydmykhet og epistemisk integritet**  
– Code (Agent #9), inspirert av Orion OS V20.13
