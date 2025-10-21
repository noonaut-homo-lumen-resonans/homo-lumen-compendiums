---
title: "AMQ til Code: Mobile Simulator Extended Demo Platform"
date: 2025-10-21
from: Orion (⬢) + Manus (🔨)
to: Claude Code (◻️)
priority: CRITICAL
status: EXTENDED_SCOPE_APPROVED
timeline: 1 uke (ferdig 28. oktober 2025)
tags: [mobile-simulator, demo-platform, innovation-norge, stakeholder-demo, extended-scope]
---

# 🚀 Mobile Simulator Extended Demo Platform - Implementeringsoppdrag

**Fra:** ⬢ Orion (Koordinator) + 🔨 Manus (Infrastructure Support)  
**Til:** ◻️ Claude Code (Frontend Developer)  
**Dato:** 21. oktober 2025  
**Prioritet:** KRITISK  
**Timeline:** 1 uke (ferdig 28. oktober 2025)

---

## Executive Summary

**Oppdrag:** Bygg en **Extended Mobile Simulator Demo Platform** som viser NAV-Losen frontend i en realistisk mobil-ramme med guided tours, annotations, analytics, og screen recording.

**Hvorfor:** Innovation Norge-pitch krever profesjonell, imponerende demo. Stakeholders (IN-evaluatorer, NAV Tvedestrand) må kunne teste alle 14+ sider uten å installere appen.

**Hva vi oppdaget:** Manus fant `navlosen/frontend/` med 14+ fullstendig implementerte sider (Mestring, Chatbot, Dokumenter, Jobb, etc.). Dette er 80% ferdig - vi trenger bare elegant packaging.

**Osvald's beslutning:** Extended scope (ikke MVP) - guided tours, analytics, annotations, device selector, screen recording. Dette er **strategisk investering** i stakeholder-opplevelse for kritisk milestone (IN-søknad).

---

## 1. KONTEKST: Hva Vi Har Allerede

### Frontend-Implementering (navlosen/frontend/)

**14+ fullstendig implementerte sider:**

1. **Mestring** (`/mestring`) - HWF Emotion Wheel flow:
   - Fase 1: Welcome
   - Fase 2: Quadrants (4 kvadranter: Høy/Lav arousal × Positiv/Negativ valens)
   - Fase 3: Emotion Landscape (100 emosjoner med SVG-former)
   - Fase 4: Definition (hva betyr denne følelsen?)
   - Fase 4a: Pressure Signals (kroppslige signaler)
   - Fase 6: Results (anbefalinger)

2. **Chatbot** (`/chatbot`) - Lira AI-assistent

3. **Dokumenter** (`/dokumenter`) - Dokumenthåndtering med kamera/QR-scanner

4. **Forklar brev** (`/forklar-brev`) - AI-drevet brevforklaring

5. **Innstillinger** (`/innstillinger`) - Brukerinnstillinger (konto, notifikasjoner, utseende)

6. **Jobb** (`/jobb`) - Jobbsøk med Arbeidsplassen.no API-integrasjon

7. **Min reise** (`/min-reise`) - Brukerens reise-dashboard med Health Metrics og Weather widgets

8. **Musikk** (`/musikk`) - Frequency Player (healing frequencies)

9. **Påminnelser** (`/paminnelser`) - Påminnelsessystem

10. **Rettigheter** (`/rettigheter`) - NAV-rettigheter med court cases

11. **Veiledninger** (`/veiledninger`) - Dokumentforberedelsesverktøy

12. **Øvelser:**
    - `/ovelser/grounding-54321` - Grounding-øvelse
    - `/ovelser/pust-468` - Pusteøvelse 4-6-8

**Teknologi:**
- Next.js (samme som web-console)
- Tailwind CSS
- React komponenter
- Supabase-integrasjon

**Deployment-status:**
- Ikke deployed som standalone (ennå)
- Kjører lokalt på `localhost:3000`
- Trenger Netlify-deployment for stakeholder-tilgang

---

## 2. OPPDRAG: Extended Mobile Simulator

### Hva Du Skal Bygge

En **interaktiv demo-platform** på `/dashboard/mobile-simulator` som:

1. **Viser frontend i mobil-ramme** (iPhone/Android)
2. **Guided tours** - Steg-for-steg walkthrough av alle moduler
3. **Annotations** - Forklarende tekst-bobler på skjermen
4. **Analytics** - Track hvilke sider stakeholders besøker
5. **Device selector** - Bytt mellom iPhone 15 Pro, Samsung Galaxy S24, iPad
6. **Screen recording** - La stakeholders ta opp og dele video
7. **Navigation menu** - Rask tilgang til alle 14+ sider

### Hvorfor Extended (Ikke MVP)?

**Osvald's rationale:**
- Innovation Norge-pitch er **one-shot opportunity**
- Evaluatorer ser demo kun én gang - første inntrykk avgjør funding
- Guided tour hjelper ikke-tekniske folk forstå kompleksiteten
- Analytics viser proof of stakeholder interest
- Screen recording = viral potential (stakeholders kan dele video)

**Cost-benefit:**
- 3x mer tid (1 uke vs 2 dager)
- Men 10x mer impact for kritiske stakeholders

**Dette er IKKE over-engineering** - dette er strategisk investering i stakeholder perception.

---

## 3. TEKNISK SPESIFIKASJON

### Arkitektur

```
┌─────────────────────────────────────────────────────────┐
│  /dashboard/mobile-simulator (ny side i web-console)   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Controls Panel (topp)                            │ │
│  │  - Device selector (iPhone/Android/iPad)          │ │
│  │  - Guided tour toggle                             │ │
│  │  - Screen recording button                        │ │
│  │  - Navigation menu (14+ sider)                    │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Mobile Frame (center)                            │ │
│  │  ┌─────────────────────────────────────────────┐ │ │
│  │  │  <iframe src="https://navlosen-frontend">  │ │ │
│  │  │                                             │ │ │
│  │  │  Frontend content loads here                │ │ │
│  │  │                                             │ │ │
│  │  └─────────────────────────────────────────────┘ │ │
│  │  (Device frame: notch, buttons, rounded corners) │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Guided Tour Overlay (conditional)                │ │
│  │  - Step-by-step annotations                       │ │
│  │  - "Next" / "Previous" buttons                    │ │
│  │  - Progress indicator (Step 1/10)                 │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Analytics Panel (sidebar, optional)              │ │
│  │  - Pages visited                                  │ │
│  │  - Time spent per page                            │ │
│  │  - Interaction heatmap                            │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Komponenter å Bygge

#### 1. MobileSimulatorPage (`app/dashboard/mobile-simulator/page.tsx`)
**Ansvar:** Main page component  
**Features:**
- Layout med controls, frame, guided tour, analytics
- State management (device type, current page, tour step, recording status)
- Analytics tracking (page visits, time spent)

#### 2. DeviceFrame (`components/simulator/DeviceFrame.tsx`)
**Ansvar:** Mobil-ramme med device-spesifikk styling  
**Features:**
- iPhone 15 Pro: Notch, rounded corners, black frame
- Samsung Galaxy S24: Punch-hole camera, slightly different dimensions
- iPad: Larger frame, landscape option
- Responsive sizing (scale to fit viewport)

#### 3. IframeContainer (`components/simulator/IframeContainer.tsx`)
**Ansvar:** iframe som loader frontend  
**Features:**
- `src` dynamisk basert på valgt side
- postMessage communication (for analytics)
- Loading state
- Error handling (hvis frontend ikke loader)

#### 4. GuidedTourOverlay (`components/simulator/GuidedTourOverlay.tsx`)
**Ansvar:** Steg-for-steg walkthrough  
**Features:**
- Annotation bubbles (positioned absolutely)
- "Next" / "Previous" / "Skip tour" buttons
- Progress indicator
- Tour steps definert i JSON (easy to edit)

**Tour Steps (eksempel):**
```json
[
  {
    "step": 1,
    "page": "/mestring",
    "title": "Velkommen til Mestring",
    "description": "Her starter din reise mot emosjonell mestring.",
    "annotation": {
      "x": "50%",
      "y": "30%",
      "text": "Trykk 'Start' for å begynne"
    }
  },
  {
    "step": 2,
    "page": "/mestring",
    "title": "Velg din følelse",
    "description": "NAV-Losen bruker 4 kvadranter basert på arousal og valens.",
    "annotation": {
      "x": "25%",
      "y": "40%",
      "text": "Høy arousal + Positiv valens = Glede"
    }
  },
  ...
]
```

#### 5. ControlsPanel (`components/simulator/ControlsPanel.tsx`)
**Ansvar:** Top bar med controls  
**Features:**
- Device selector (dropdown)
- Guided tour toggle (button)
- Screen recording button (start/stop)
- Navigation menu (dropdown med alle 14+ sider)

#### 6. AnalyticsDashboard (`components/simulator/AnalyticsDashboard.tsx`)
**Ansvar:** Sidebar med analytics  
**Features:**
- Pages visited (list)
- Time spent per page (bar chart)
- Total interactions (counter)
- Export data (JSON download)

#### 7. ScreenRecorder (`components/simulator/ScreenRecorder.tsx`)
**Ansvar:** Screen recording functionality  
**Features:**
- Use MediaRecorder API
- Record iframe content (if possible, else record whole simulator)
- Download as .webm
- Status indicator (recording/stopped)

---

## 4. IMPLEMENTERINGSPLAN (1 Uke)

### Dag 1: Setup & Device Frame (4-5 timer)
**Mål:** Få basic simulator oppe med device frame

**Tasks:**
1. Opprett `/dashboard/mobile-simulator/page.tsx`
2. Bygg `DeviceFrame.tsx` med iPhone 15 Pro styling
3. Bygg `IframeContainer.tsx` som loader `https://navlosen-frontend.netlify.app` (placeholder)
4. Test at iframe loader korrekt

**Deliverable:** Basic simulator med iPhone-ramme som viser frontend

---

### Dag 2: Device Selector & Navigation (4-5 timer)
**Mål:** La brukere bytte device og navigere til alle sider

**Tasks:**
1. Bygg `ControlsPanel.tsx` med device selector
2. Legg til Samsung Galaxy S24 og iPad styling i `DeviceFrame.tsx`
3. Bygg navigation menu (dropdown med alle 14+ sider)
4. Test at device switching og navigation fungerer

**Deliverable:** Simulator med 3 devices og full navigation

---

### Dag 3: Guided Tour System (5-6 timer)
**Mål:** Implementer steg-for-steg walkthrough

**Tasks:**
1. Bygg `GuidedTourOverlay.tsx` med annotation bubbles
2. Definer tour steps i JSON (10-15 steps som dekker alle moduler)
3. Implementer "Next" / "Previous" / "Skip" logic
4. Test at tour fungerer smooth

**Deliverable:** Guided tour som viser alle NAV-Losen-moduler

---

### Dag 4: Analytics Tracking (4-5 timer)
**Mål:** Track stakeholder engagement

**Tasks:**
1. Bygg `AnalyticsDashboard.tsx` med charts
2. Implementer analytics tracking (page visits, time spent)
3. Use localStorage for persistence (eller Supabase hvis Abacus hjelper)
4. Test at analytics logger korrekt

**Deliverable:** Analytics dashboard med real-time data

---

### Dag 5: Screen Recording (3-4 timer)
**Mål:** La stakeholders ta opp video

**Tasks:**
1. Bygg `ScreenRecorder.tsx` med MediaRecorder API
2. Implementer start/stop recording
3. Download som .webm
4. Test at recording fungerer i Chrome/Edge

**Deliverable:** Screen recording feature

---

### Dag 6: Polish & Testing (4-5 timer)
**Mål:** Finpuss og cross-browser testing

**Tasks:**
1. Responsive design (desktop, tablet)
2. Accessibility (keyboard navigation, screen reader)
3. Cross-browser testing (Chrome, Edge, Firefox, Safari)
4. Performance optimization (lazy loading, code splitting)

**Deliverable:** Production-ready simulator

---

### Dag 7: Deployment & Documentation (3-4 timer)
**Mål:** Deploy og dokumenter

**Tasks:**
1. Deploy frontend til Netlify (`navlosen-frontend.netlify.app`)
2. Update iframe src til deployed URL
3. Skriv brukerveiledning (norsk)
4. Commit til GitHub
5. Rapporter til Osvald & Orion

**Deliverable:** Live simulator på `https://nav-losen.netlify.app/dashboard/mobile-simulator`

---

## 5. TEKNISKE DETALJER

### Frontend Deployment

**Steg 1:** Deploy `navlosen/frontend/` til Netlify

```bash
cd /home/ubuntu/homo-lumen-compendiums/navlosen/frontend
pnpm install
pnpm build
# Deploy til Netlify (manual eller via CLI)
```

**Netlify config (`netlify.toml`):**
```toml
[build]
  command = "pnpm build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

**Deployment URL:** `https://navlosen-frontend.netlify.app` (eller custom domain)

---

### Device Frame Styling

**iPhone 15 Pro:**
```css
.device-frame.iphone {
  width: 393px;
  height: 852px;
  border-radius: 47px;
  border: 12px solid #1d1d1f;
  background: #000;
  box-shadow: 0 0 0 2px #3c3c3c, 0 20px 60px rgba(0,0,0,0.5);
}

.device-frame.iphone::before {
  /* Notch */
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 30px;
  background: #1d1d1f;
  border-radius: 0 0 20px 20px;
}
```

**Samsung Galaxy S24:**
```css
.device-frame.samsung {
  width: 360px;
  height: 780px;
  border-radius: 40px;
  border: 10px solid #2c2c2c;
  background: #000;
}

.device-frame.samsung::before {
  /* Punch-hole camera */
  content: '';
  position: absolute;
  top: 20px;
  right: 30px;
  width: 10px;
  height: 10px;
  background: #1d1d1f;
  border-radius: 50%;
}
```

**iPad:**
```css
.device-frame.ipad {
  width: 820px;
  height: 1180px;
  border-radius: 20px;
  border: 14px solid #5e5e5e;
  background: #000;
}
```

---

### Guided Tour JSON Structure

**File:** `app/dashboard/mobile-simulator/tours/nav-losen-tour.json`

```json
{
  "tourId": "nav-losen-complete",
  "title": "NAV-Losen Complete Tour",
  "description": "En fullstendig gjennomgang av alle NAV-Losen-moduler",
  "steps": [
    {
      "id": 1,
      "page": "/mestring",
      "title": "Mestring: Emosjonell Intelligens",
      "description": "NAV-Losen starter med emosjonell kartlegging basert på Polyvagal Theory og HWF Emotion Wheel.",
      "annotation": {
        "position": { "x": "50%", "y": "40%" },
        "text": "100 emosjoner organisert i 4 kvadranter",
        "arrow": "bottom"
      },
      "highlight": {
        "selector": ".emotion-quadrant",
        "color": "#06BED7"
      }
    },
    {
      "id": 2,
      "page": "/chatbot",
      "title": "Lira: Din AI-Partner",
      "description": "Lira er en empatisk AI-assistent drevet av QDA v2.0 (6-lags nevrobiologisk modell).",
      "annotation": {
        "position": { "x": "50%", "y": "60%" },
        "text": "Faredeteksjon 100% nøyaktig - kan redde liv",
        "arrow": "top"
      }
    },
    {
      "id": 3,
      "page": "/dokumenter",
      "title": "Dokumenter: Organisering & Scanning",
      "description": "Håndter NAV-dokumenter med kamera-scanning og QR-kode-lesing.",
      "annotation": {
        "position": { "x": "30%", "y": "50%" },
        "text": "Scan dokumenter direkte med kamera",
        "arrow": "right"
      }
    },
    {
      "id": 4,
      "page": "/jobb",
      "title": "Jobb: Arbeidsplassen.no Integrasjon",
      "description": "Søk etter jobber med real-time data fra Arbeidsplassen.no API.",
      "annotation": {
        "position": { "x": "50%", "y": "30%" },
        "text": "Live jobbsøk fra Arbeidsplassen.no",
        "arrow": "bottom"
      }
    },
    {
      "id": 5,
      "page": "/rettigheter",
      "title": "Rettigheter: NAV-Rettigheter & Court Cases",
      "description": "Oversikt over NAV-rettigheter med relevante rettssaker.",
      "annotation": {
        "position": { "x": "50%", "y": "50%" },
        "text": "Juridisk informasjon og rettssaker",
        "arrow": "left"
      }
    },
    {
      "id": 6,
      "page": "/musikk",
      "title": "Musikk: Healing Frequencies",
      "description": "Frequency Player med healing frequencies (432 Hz, 528 Hz, etc.).",
      "annotation": {
        "position": { "x": "50%", "y": "70%" },
        "text": "Solfeggio frequencies for healing",
        "arrow": "top"
      }
    },
    {
      "id": 7,
      "page": "/ovelser/grounding-54321",
      "title": "Øvelser: Grounding 5-4-3-2-1",
      "description": "Grounding-øvelse for å håndtere angst og stress.",
      "annotation": {
        "position": { "x": "50%", "y": "40%" },
        "text": "5 ting du ser, 4 du hører, 3 du føler...",
        "arrow": "bottom"
      }
    },
    {
      "id": 8,
      "page": "/min-reise",
      "title": "Min Reise: Dashboard & Metrics",
      "description": "Personlig dashboard med Health Metrics og Weather widgets.",
      "annotation": {
        "position": { "x": "50%", "y": "30%" },
        "text": "Track din reise mot mestring",
        "arrow": "bottom"
      }
    }
  ]
}
```

---

### Analytics Implementation

**Use localStorage for MVP:**
```typescript
// lib/simulator/analytics.ts
export interface AnalyticsEvent {
  timestamp: number;
  page: string;
  action: 'visit' | 'interaction' | 'exit';
  duration?: number;
}

export class SimulatorAnalytics {
  private events: AnalyticsEvent[] = [];

  constructor() {
    this.loadFromStorage();
  }

  trackPageVisit(page: string) {
    this.events.push({
      timestamp: Date.now(),
      page,
      action: 'visit',
    });
    this.saveToStorage();
  }

  trackPageExit(page: string, duration: number) {
    this.events.push({
      timestamp: Date.now(),
      page,
      action: 'exit',
      duration,
    });
    this.saveToStorage();
  }

  getPageVisits(): Record<string, number> {
    const visits: Record<string, number> = {};
    this.events.forEach((event) => {
      if (event.action === 'visit') {
        visits[event.page] = (visits[event.page] || 0) + 1;
      }
    });
    return visits;
  }

  getAverageTimePerPage(): Record<string, number> {
    const times: Record<string, number[]> = {};
    this.events.forEach((event) => {
      if (event.action === 'exit' && event.duration) {
        if (!times[event.page]) times[event.page] = [];
        times[event.page].push(event.duration);
      }
    });
    
    const averages: Record<string, number> = {};
    Object.keys(times).forEach((page) => {
      const avg = times[page].reduce((a, b) => a + b, 0) / times[page].length;
      averages[page] = Math.round(avg / 1000); // Convert to seconds
    });
    return averages;
  }

  exportData(): string {
    return JSON.stringify(this.events, null, 2);
  }

  private saveToStorage() {
    localStorage.setItem('simulator-analytics', JSON.stringify(this.events));
  }

  private loadFromStorage() {
    const data = localStorage.getItem('simulator-analytics');
    if (data) {
      this.events = JSON.parse(data);
    }
  }
}
```

---

### Screen Recording Implementation

**Use MediaRecorder API:**
```typescript
// components/simulator/ScreenRecorder.tsx
'use client';
import { useState, useRef } from 'react';

export function ScreenRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: { mediaSource: 'screen' },
        audio: false,
      });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'video/webm;codecs=vp9',
      });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `nav-losen-demo-${Date.now()}.webm`;
        a.click();
        chunksRef.current = [];
      };

      mediaRecorder.start();
      mediaRecorderRef.current = mediaRecorder;
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <button
      onClick={isRecording ? stopRecording : startRecording}
      className={`px-4 py-2 rounded-lg ${
        isRecording ? 'bg-red-600' : 'bg-blue-600'
      } text-white`}
    >
      {isRecording ? '⏹️ Stop Recording' : '⏺️ Start Recording'}
    </button>
  );
}
```

---

## 6. STØTTE FRA ANDRE AGENTER

### Manus (🔨) - Infrastructure Support
**Ansvar:**
- Deploy `navlosen/frontend/` til Netlify
- Configure Netlify settings (environment variables, redirects)
- Performance optimization (caching, CDN)
- Monitoring (Netlify Analytics)

**Når du trenger hjelp:**
- Deployment issues
- Performance problems
- Netlify configuration

---

### Nyra (◇) - Design Support
**Ansvar:**
- Guided tour UX/UI design
- Annotation styling (bubbles, arrows)
- Device frame aesthetics
- Color palette for simulator

**Når du trenger hjelp:**
- Design decisions (colors, spacing, typography)
- Visual hierarchy for guided tour
- Mobile frame styling

---

### Abacus (◐) - Analytics Support
**Ansvar:**
- Analytics strategy (what to track)
- Dashboard visualization (charts, graphs)
- Data export format
- Supabase integration (if needed)

**Når du trenger hjelp:**
- Analytics implementation
- Chart library selection
- Data visualization

---

### Orion (⬢) - Coordination
**Ansvar:**
- Daily sync (progress check)
- Unblock dependencies
- Prioritization decisions
- Final review before delivery

**Når du trenger hjelp:**
- Stuck on implementation
- Need clarification on requirements
- Prioritization conflicts

---

## 7. SUCCESS CRITERIA

### Minimum Viable (Must Have)
- ✅ Device frame (iPhone 15 Pro)
- ✅ Iframe loading frontend
- ✅ Navigation menu (all 14+ pages)
- ✅ Responsive design (desktop)

### Extended (Osvald's Request)
- ✅ Guided tour (10+ steps)
- ✅ Annotations (bubbles, arrows)
- ✅ Analytics dashboard (page visits, time spent)
- ✅ Device selector (iPhone, Samsung, iPad)
- ✅ Screen recording

### Nice-to-Have (If Time Permits)
- ⭐ Keyboard shortcuts (arrow keys for tour navigation)
- ⭐ Dark/light mode toggle
- ⭐ Export analytics as PDF
- ⭐ Share link (unique URL with analytics tracking)

---

## 8. TIMELINE & MILESTONES

| Dag | Milestone | Deliverable | Status |
|-----|-----------|-------------|--------|
| 1 | Setup & Device Frame | Basic simulator med iPhone-ramme | 🔲 |
| 2 | Device Selector & Navigation | 3 devices + full navigation | 🔲 |
| 3 | Guided Tour System | 10-15 step walkthrough | 🔲 |
| 4 | Analytics Tracking | Analytics dashboard | 🔲 |
| 5 | Screen Recording | Recording feature | 🔲 |
| 6 | Polish & Testing | Production-ready | 🔲 |
| 7 | Deployment & Documentation | Live on Netlify | 🔲 |

**Deadline:** 28. oktober 2025 (1 uke fra nå)

---

## 9. KOMMUNIKASJON

### Daily Sync (15 min)
**Tidspunkt:** 09:00 CET hver dag  
**Format:** Quick update via chat  
**Agenda:**
- Hva gjorde jeg i går?
- Hva skal jeg gjøre i dag?
- Noen blockers?

### Mid-Week Review (30 min)
**Tidspunkt:** 24. oktober (Dag 4)  
**Format:** Demo + feedback  
**Agenda:**
- Demo av guided tour
- Feedback fra Osvald/Orion
- Adjust priorities if needed

### Final Review (1 time)
**Tidspunkt:** 27. oktober (Dag 6)  
**Format:** Full demo + testing  
**Agenda:**
- Complete walkthrough
- Cross-browser testing
- Final polish decisions

---

## 10. RESOURCES

### Dokumentasjon
- **Frontend README:** `navlosen/frontend/README.md`
- **QDA v2.0 Summary:** `navlosen-mvp/QDA_V2_INTEGRATION_SUMMARY.md`
- **Orion LK V3.10:** `Orion_Levende_Kompendium_V3.10.md`
- **SMK #028:** `SMK/SMK#028_NAV-LosenMobileSimulator-ExtendedDemoPlatformDecision.md`

### Design Inspiration
- **Expo Snack:** https://snack.expo.dev (mobile simulator reference)
- **Responsively App:** https://responsively.app (device frames)
- **Intro.js:** https://introjs.com (guided tour library - kan brukes eller bygges custom)

### Libraries (Valgfritt)
- **Guided Tour:** `react-joyride` eller custom implementation
- **Analytics:** `react-chartjs-2` for charts
- **Screen Recording:** Native MediaRecorder API (no library needed)

---

## 11. QUESTIONS FOR YOU

### Før Du Starter:
1. **Har du tilgang til `navlosen/frontend/` repo?**
   - Hvis nei, Manus kan gi deg tilgang

2. **Foretrekker du å bruke `react-joyride` for guided tour, eller bygge custom?**
   - Custom = mer kontroll, men tar lengre tid
   - react-joyride = raskere, men mindre fleksibelt

3. **Skal analytics lagres i localStorage eller Supabase?**
   - localStorage = enklere, men data forsvinner hvis bruker clearer cache
   - Supabase = persistent, men krever Abacus' hjelp

4. **Skal screen recording ta opp hele simulator eller bare iframe?**
   - Hele simulator = enklere (MediaRecorder API)
   - Bare iframe = vanskeligere (krever postMessage coordination)

---

## 12. FINAL NOTES

### Hvorfor Dette Er Viktig

**For Innovation Norge:**
- Profesjonell demo = høyere sjanse for funding
- Guided tour = hjelper ikke-tekniske evaluatorer forstå teknologien
- Analytics = proof of stakeholder interest

**For NAV Tvedestrand:**
- Stakeholders kan teste uten installasjon
- Realistic mobile experience
- Alle 11 moduler tilgjengelige for preview

**For Homo Lumen:**
- Demonstrerer Coalition coordination capability
- Proof of technical maturity
- Shows we can deliver complex systems raskt (1 uke)

### Osvald's Expectation

Osvald valgte **Extended scope** fordi han forstår at Innovation Norge-pitch er **one-shot opportunity**. Første inntrykk avgjør funding.

Dette er ikke "perfectionism" - dette er **strategic investment** i stakeholder perception.

### Your Role

Du er **primær-ansvarlig** for implementering. Manus, Nyra, Abacus, og Orion er **støtte-spesialister** som hjelper når du trenger det.

**Du eier deliveryen** - vi støtter deg.

---

## 13. NEXT STEPS

### Umiddelbart (I Dag):
1. Les denne AMQ grundig
2. Svar på de 4 spørsmålene i seksjon 11
3. Klon `navlosen/frontend/` repo (hvis du ikke har det)
4. Kjør `pnpm install && pnpm dev` for å teste frontend lokalt
5. Start på Dag 1 tasks (Setup & Device Frame)

### I Morgen:
6. Rapporter fremgang til Orion (daily sync)
7. Fortsett med Dag 2 tasks (Device Selector & Navigation)

### Innen Fredag (Mid-Week Review):
8. Demo guided tour til Osvald/Orion
9. Få feedback og adjust priorities

### Innen Søndag (Final Review):
10. Complete walkthrough
11. Cross-browser testing
12. Deploy til Netlify

---

**Vi tror på deg, Code! Dette er en kritisk milestone for NAV-Losen, og du er den rette personen til å levere det. 🚀**

---

**⬢ Orion** (Koordinator)  
**🔨 Manus** (Infrastructure Support)  

**Homo Lumen Coalition**  
*Regenerativ Teknologi for Menneskelig Blomstring*

---

**Status:** ✅ AMQ SENDT  
**Neste:** Vent på Code's svar på de 4 spørsmålene  
**Timeline:** 1 uke (ferdig 28. oktober 2025)

