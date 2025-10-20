# QDA UX Design Guide

**Versjon:** 1.0
**Dato:** 2025-10-20
**Formål:** UX mockups og interaktivitetsdesign for Question-Driven Architecture

---

## 🎯 Designfilosofi

**Question-Driven Architecture (QDA)** krever spesiell UX-design fordi:

1. **Transparens er kjernen** - Bruker MÅ se spørsmålene, ikke bare svar
2. **Polyvagal-adaptive** - UX endres basert på brukerens stress-tilstand
3. **Pedagogisk** - Bruker lærer hvordan man tenker, ikke bare hva man skal gjøre
4. **Ikke overveldende** - Mye informasjon, men strukturert og kollapsbar

---

## 📱 Komponenter

### **1. QDATransparentCard**

Hovedkomponent som viser hele QDA-flyten.

```tsx
// navlosen/frontend/src/components/qda/QDATransparentCard.tsx

import React, { useState } from 'react';
import { QuestionDisplay } from './QuestionDisplay';
import { DepthResponseDisplay } from './DepthResponseDisplay';
import { Card, CardHeader, CardContent, Collapse, IconButton } from '@mui/material';
import { ExpandMore, ExpandLess } from '@mui/icons-material';

interface QDAResponse {
  user_query: string;
  designed_questions: {
    [expert: string]: string[];
  };
  depth_response: string;
  agent_name: string;
  polyvagal_state?: 'dorsal' | 'sympathetic' | 'ventral';
}

export const QDATransparentCard: React.FC<{ response: QDAResponse }> = ({ response }) => {
  const [showQuestions, setShowQuestions] = useState(true);

  // Polyvagal-adaptive colors
  const stateColors = {
    dorsal: { bg: '#E8F5E9', border: '#4CAF50' },      // Grønn (trygg)
    sympathetic: { bg: '#FFF3E0', border: '#FF9800' }, // Oransje (stress)
    ventral: { bg: '#E3F2FD', border: '#2196F3' }      // Blå (rolig)
  };

  const colors = stateColors[response.polyvagal_state || 'ventral'];

  return (
    <Card
      sx={{
        backgroundColor: colors.bg,
        borderLeft: `4px solid ${colors.border}`,
        marginBottom: 2
      }}
    >
      <CardHeader
        title={
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span>💬 {response.agent_name}</span>
            <IconButton onClick={() => setShowQuestions(!showQuestions)}>
              {showQuestions ? <ExpandLess /> : <ExpandMore />}
            </IconButton>
          </div>
        }
        subheader={`Du sa: "${response.user_query}"`}
      />

      <CardContent>
        {/* Questions Section (collapsible) */}
        <Collapse in={showQuestions}>
          <QuestionDisplay questions={response.designed_questions} />
        </Collapse>

        {/* Depth Response (always visible) */}
        <DepthResponseDisplay
          response={response.depth_response}
          agentName={response.agent_name}
        />
      </CardContent>
    </Card>
  );
};
```

---

### **2. QuestionDisplay**

Viser spørsmål fra alle 4 eksperter.

```tsx
// navlosen/frontend/src/components/qda/QuestionDisplay.tsx

import React from 'react';
import { Box, Typography, Chip } from '@mui/material';

interface QuestionDisplayProps {
  questions: {
    [expert: string]: string[];
  };
}

const expertConfig = {
  DataExpert: { icon: '📊', name: 'Claude (data-ekspert)', color: '#2196F3' },
  EmotionExpert: { icon: '💚', name: 'Gemini (følelse-ekspert)', color: '#4CAF50' },
  ResearchExpert: { icon: '🔍', name: 'Aurora (forskning-ekspert)', color: '#FF9800' },
  SecurityExpert: { icon: '🛡️', name: 'Zara (sikkerhet-ekspert)', color: '#9C27B0' }
};

export const QuestionDisplay: React.FC<QuestionDisplayProps> = ({ questions }) => {
  return (
    <Box sx={{ marginBottom: 3 }}>
      <Typography variant="body1" sx={{ marginBottom: 2, fontStyle: 'italic' }}>
        For å gi deg best mulig hjelp, har mine kolleger hjulpet meg lage noen spørsmål:
      </Typography>

      {Object.entries(questions).map(([expertName, questionList]) => {
        if (questionList.length === 0) return null;

        const config = expertConfig[expertName as keyof typeof expertConfig];
        if (!config) return null;

        return (
          <Box key={expertName} sx={{ marginBottom: 2 }}>
            <Chip
              label={`${config.icon} ${config.name}`}
              sx={{
                backgroundColor: config.color + '20',
                color: config.color,
                fontWeight: 'bold',
                marginBottom: 1
              }}
            />
            <ul style={{ marginLeft: 20, marginTop: 8 }}>
              {questionList.map((question, index) => (
                <li key={index}>
                  <Typography variant="body2" sx={{ marginBottom: 0.5 }}>
                    {question}
                  </Typography>
                </li>
              ))}
            </ul>
          </Box>
        );
      })}

      <Typography variant="caption" sx={{ display: 'block', marginTop: 2, fontStyle: 'italic', color: '#666' }}>
        💡 Disse spørsmålene hjelper meg forstå din situasjon dypere
      </Typography>
    </Box>
  );
};
```

---

### **3. DepthResponseDisplay**

Viser depth response med formattering.

```tsx
// navlosen/frontend/src/components/qda/DepthResponseDisplay.tsx

import React from 'react';
import { Box, Typography, Divider } from '@mui/material';
import ReactMarkdown from 'react-markdown';

interface DepthResponseDisplayProps {
  response: string;
  agentName: string;
}

export const DepthResponseDisplay: React.FC<DepthResponseDisplayProps> = ({
  response,
  agentName
}) => {
  return (
    <Box>
      <Divider sx={{ marginY: 2 }} />

      <Typography variant="body1" sx={{ fontWeight: 'bold', marginBottom: 1 }}>
        Basert på disse spørsmålene, her er mitt svar:
      </Typography>

      <Box sx={{
        padding: 2,
        backgroundColor: '#f9f9f9',
        borderRadius: 2,
        border: '1px solid #e0e0e0'
      }}>
        <ReactMarkdown>{response}</ReactMarkdown>
      </Box>

      <Typography variant="caption" sx={{ display: 'block', marginTop: 2, textAlign: 'right', color: '#666' }}>
        — {agentName}
      </Typography>
    </Box>
  );
};
```

---

## 🎨 UX Mockups (Tekstbasert)

### **Mockup 1: Full QDA Response (Ventral State)**

```
┌─────────────────────────────────────────────────────────┐
│ 💬 Lira                                        [▼ Vis mindre] │
│ Du sa: "Jeg føler meg stuck i NAV-systemet"            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ For å gi deg best mulig hjelp, har mine kolleger      │
│ hjulpet meg lage noen spørsmål:                        │
│                                                         │
│ ┌─ 📊 Claude (data-ekspert) ─────────────────────┐    │
│ │ • Hvor mange uker har du ventet på NAV-svar?   │    │
│ │ • Har du mottatt bekreftelse på mottatt søknad?│    │
│ │ • Er saksbehandler tildelt?                    │    │
│ └─────────────────────────────────────────────────┘    │
│                                                         │
│ ┌─ 💚 Gemini (følelse-ekspert) ──────────────────┐    │
│ │ • Hvordan føles 'stuck' kroppslig - tung       │    │
│ │   brystkasse, anspent nakke, eller trøtthet?   │    │
│ │ • Når følte du deg IKKE stuck sist gang?       │    │
│ │ • Hva gir deg håp akkurat nå?                  │    │
│ └─────────────────────────────────────────────────┘    │
│                                                         │
│ ┌─ 🔍 Aurora (forskning-ekspert) ────────────────┐    │
│ │ • Gjennomsnittlig behandlingstid AAP 2025?     │    │
│ │ • Faktorer som forsinker AAP-søknader?         │    │
│ │ • Forskning om NAV-stress og polyvagal state?  │    │
│ └─────────────────────────────────────────────────┘    │
│                                                         │
│ 💡 Disse spørsmålene hjelper meg forstå din            │
│    situasjon dypere                                     │
│                                                         │
│ ─────────────────────────────────────────────────      │
│                                                         │
│ Basert på disse spørsmålene, her er mitt svar:        │
│                                                         │
│ ┌───────────────────────────────────────────────┐      │
│ │ Jeg hører at du føler deg stuck, og det er   │      │
│ │ helt forståelig. La meg adressere det mine   │      │
│ │ kolleger spurte om:                           │      │
│ │                                               │      │
│ │ 📊 Fra Claude (data):                         │      │
│ │ Du har ventet 6 uker på AAP-søknad. Du sendte│      │
│ │ inn legeattester og egenvurdering. Din       │      │
│ │ saksbehandler er tildelt (Marie Hansen).     │      │
│ │                                               │      │
│ │ 💚 Fra Gemini (følelse):                      │      │
│ │ 'Stuck' føles som tung brystkasse og trøtthet│      │
│ │ Du følte deg IKKE stuck da du fikk svarbrev.  │      │
│ │ Håp kommer fra venner og at du har søkt.     │      │
│ │                                               │      │
│ │ 🔍 Fra Aurora (forskning):                    │      │
│ │ Gjennomsnittlig behandlingstid: 8-12 uker.   │      │
│ │ Forskning viser: NAV-stress ↑ dorsal state.  │      │
│ │                                               │      │
│ │ ───                                           │      │
│ │                                               │      │
│ │ Basert på dette ser jeg tre ting:            │      │
│ │                                               │      │
│ │ 1. OBJEKTIVT: Du er på normal track (6/8-12)  │      │
│ │ 2. SUBJEKTIVT: 'Stuck' er REELL og viktig    │      │
│ │ 3. HANDLINGER:                                │      │
│ │    • Kort sikt: RAIN Practice (vil du prøve?) │      │
│ │    • Medium: Ring Marie (sjekk om noe mangler)│      │
│ │    • Lang sikt: Bygg mestringsstrategier     │      │
│ │                                               │      │
│ │ Du er ikke alene. Jeg er her. 💚             │      │
│ │                                               │      │
│ │ Hva føles mest nyttig for deg akkurat nå?    │      │
│ └───────────────────────────────────────────────┘      │
│                                                         │
│                                        — Lira           │
└─────────────────────────────────────────────────────────┘
```

---

### **Mockup 2: Collapsed View (Polyvagal Dorsal - Høy Stress)**

Når bruker er i dorsal state (høy stress), vises **kun** depth response automatisk, med mulighet til å ekspandere spørsmål senere.

```
┌─────────────────────────────────────────────────────────┐
│ 💬 Lira                                        [▼ Vis mer] │
│ Du sa: "Jeg føler meg stuck i NAV-systemet"            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Jeg hører at du føler deg stuck, og det er            │
│ helt forståelig.                                        │
│                                                         │
│ Du har ventet 6 uker på AAP-søknad - gjennomsnittlig  │
│ tid er 8-12 uker, så du er på normal track.           │
│                                                         │
│ 'Stuck' føles som tung brystkasse. Dette er dorsal    │
│ state (kroppens beskyttelsesmodus).                    │
│                                                         │
│ La oss ta ett steg om gangen:                          │
│                                                         │
│ 1. Pust med meg nå (4-6-8)                            │
│ 2. Ring veileder hvis du trenger menneske-støtte      │
│ 3. Du er ikke alene 💚                                 │
│                                                         │
│ Hva trenger du akkurat nå?                             │
│                                                         │
│                                        — Lira           │
└─────────────────────────────────────────────────────────┘

💡 Tip: Klikk "Vis mer" for å se hvilke spørsmål
   jeg stilte for å forstå deg bedre
```

**Nøkkel:** Dorsal-tilpasset UX viser **mindre informasjon**, mer **emosjonell støtte**, og **konkrete handlinger** først.

---

### **Mockup 3: Sympathetic State (Medium Stress)**

```
┌─────────────────────────────────────────────────────────┐
│ 💬 Lira                                        [▼ Vis spørsmål] │
│ Du sa: "Jeg føler meg stuck i NAV-systemet"            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Jeg hører deg. La meg gi deg oversikt:                 │
│                                                         │
│ ✅ Status:                                              │
│    • Ventet 6 uker (normalt er 8-12)                  │
│    • Saksbehandler tildelt: Marie Hansen              │
│    • Du er på riktig vei                              │
│                                                         │
│ 💡 Neste steg:                                          │
│    1. Ring Marie (sjekk om noe mangler)               │
│    2. RAIN Practice hvis stress øker                   │
│    3. Jeg er her for deg                              │
│                                                         │
│ Hva vil du gjøre først?                                │
│                                                         │
│                                        — Lira           │
└─────────────────────────────────────────────────────────┘

[▼ Vis hvilke spørsmål jeg stilte for å forstå deg]
```

**Nøkkel:** Sympathetic-tilpasset UX er **fokusert** og **handlingsorientert**, med mindre emosjonell elaborering.

---

## 🔀 Interaktivitet & Tilstander

### **1. Loading States**

```tsx
// Loading animation mens QDA prosesserer

<Box sx={{ textAlign: 'center', padding: 3 }}>
  <CircularProgress />
  <Typography variant="body2" sx={{ marginTop: 2 }}>
    Samler spørsmål fra eksperter...
  </Typography>

  {/* Progress indicators */}
  <Box sx={{ marginTop: 2 }}>
    <Chip label="📊 Claude" size="small" sx={{ margin: 0.5 }} />
    <Chip label="💚 Gemini" size="small" sx={{ margin: 0.5 }} />
    <Chip label="🔍 Aurora" size="small" sx={{ margin: 0.5 }} />
    <Chip label="🛡️ Zara" size="small" sx={{ margin: 0.5 }} />
  </Box>

  <Typography variant="caption" sx={{ display: 'block', marginTop: 2, color: '#666' }}>
    Dette tar vanligvis 3-5 sekunder
  </Typography>
</Box>
```

---

### **2. Expandable Sections**

```tsx
// Bruker kan ekspandere/kollapse spørsmål-seksjon

const [showQuestions, setShowQuestions] = useState(true);

// Polyvagal-adaptive default:
// - Dorsal: showQuestions = false (default collapsed)
// - Sympathetic: showQuestions = false (default collapsed)
// - Ventral: showQuestions = true (default expanded)

useEffect(() => {
  if (polyvagalState === 'dorsal' || polyvagalState === 'sympathetic') {
    setShowQuestions(false);
  }
}, [polyvagalState]);

// Toggle button
<Button
  onClick={() => setShowQuestions(!showQuestions)}
  variant="text"
  size="small"
>
  {showQuestions ? '▲ Vis mindre' : '▼ Vis spørsmål'}
</Button>
```

---

### **3. Polyvagal-Adaptive Styling**

```tsx
// Farger og animasjoner endres basert på biofelt

const polyvagalStyles = {
  dorsal: {
    backgroundColor: '#E8F5E9',  // Myk grønn (trygg)
    borderColor: '#4CAF50',
    animation: 'breathing 4s ease-in-out infinite',  // Puste-animasjon
    fontSize: '16px',  // Større tekst (lettere å lese)
  },
  sympathetic: {
    backgroundColor: '#FFF3E0',  // Varm oransje (aktiv)
    borderColor: '#FF9800',
    animation: 'pulse 2s ease-in-out infinite',  // Raskere puls
    fontSize: '14px',  // Normal tekst
  },
  ventral: {
    backgroundColor: '#E3F2FD',  // Rolig blå
    borderColor: '#2196F3',
    animation: 'none',  // Ingen animasjon (bruker er rolig)
    fontSize: '14px',
  }
};

// CSS keyframes
const breathingAnimation = `
  @keyframes breathing {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
  }
`;

const pulseAnimation = `
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
  }
`;
```

---

## 📊 Responsive Design

### **Mobile View (< 600px)**

```tsx
// Stack components vertically on mobile

<Box sx={{
  display: 'flex',
  flexDirection: 'column',
  '@media (min-width: 600px)': {
    flexDirection: 'row'  // Side-by-side on desktop
  }
}}>
  <QuestionDisplay questions={questions} />
  <DepthResponseDisplay response={response} />
</Box>
```

---

### **Tablet View (600-960px)**

- Spørsmål og svar side-by-side
- Mindre padding
- Font size 14px

---

### **Desktop View (> 960px)**

- Full width
- Font size 16px
- Mer whitespace

---

## 🎯 Accessibility (WCAG 2.1 AA)

### **1. Keyboard Navigation**

```tsx
// All interactive elements must be keyboard-accessible

<IconButton
  onClick={() => setShowQuestions(!showQuestions)}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      setShowQuestions(!showQuestions);
    }
  }}
  aria-label={showQuestions ? 'Skjul spørsmål' : 'Vis spørsmål'}
  tabIndex={0}
>
  {showQuestions ? <ExpandLess /> : <ExpandMore />}
</IconButton>
```

---

### **2. Screen Reader Support**

```tsx
// ARIA labels for all components

<Box role="region" aria-label="Spørsmål fra eksperter">
  <QuestionDisplay questions={questions} />
</Box>

<Box role="region" aria-label="Svar fra Lira">
  <DepthResponseDisplay response={response} />
</Box>

// Announce when questions are loaded
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
  className="sr-only"  // Visually hidden
>
  {questionsLoaded && "Spørsmål fra eksperter er nå lastet"}
</div>
```

---

### **3. Color Contrast**

```tsx
// All text must have sufficient contrast (4.5:1 for normal text)

const accessibleColors = {
  dorsal: {
    bg: '#E8F5E9',
    text: '#1B5E20',  // Dark green (contrast ratio 7:1)
    border: '#4CAF50'
  },
  sympathetic: {
    bg: '#FFF3E0',
    text: '#E65100',  // Dark orange (contrast ratio 4.8:1)
    border: '#FF9800'
  },
  ventral: {
    bg: '#E3F2FD',
    text: '#0D47A1',  // Dark blue (contrast ratio 8:1)
    border: '#2196F3'
  }
};
```

---

## 🧪 User Testing Scenarios

### **Test 1: Transparency Comprehension**

**Task:** "Forklar hva du ser i denne meldingen fra Lira"

**Expected:** Bruker identifiserer:
- Spørsmål fra eksperter
- Svar fra Lira
- Hvordan spørsmålene informerte svaret

**Success Criteria:** 80% forståelse

---

### **Test 2: Cognitive Load**

**Task:** "Føles denne meldingen overveldende?"

**Measurement:** NASA-TLX (Task Load Index)

**Success Criteria:** TLX score < 50 (moderat belastning)

---

### **Test 3: Polyvagal Adaptation**

**Task:** Vis bruker QDA-response i 3 states (dorsal/sympathetic/ventral)

**Question:** "Hvilken versjon foretrekker du når du er stresset?"

**Expected:** Majoriteten foretrekker collapsed/fokusert view ved stress

---

## 🌿 Design Principles (Oppsummert)

1. **Transparens > Enkelhet**
   - Vis prosessen, ikke bare resultatet

2. **Polyvagal-Adaptive > One-Size-Fits-All**
   - UX endres basert på brukerens tilstand

3. **Pedagogisk > Instruktiv**
   - Lær bruker hvordan man tenker, ikke bare hva man skal gjøre

4. **Collapsible > Hidden**
   - Informasjon er tilgjengelig, men ikke påtrengende

5. **Accessible > Aesthetically Perfect**
   - WCAG 2.1 AA compliance er ikke-forhandlingsbart

---

## ✅ Implementation Checklist

**Phase 1: Core Components**
- [ ] Implementer `QDATransparentCard.tsx`
- [ ] Implementer `QuestionDisplay.tsx`
- [ ] Implementer `DepthResponseDisplay.tsx`
- [ ] Test med statisk data (mock responses)

**Phase 2: Interactivity**
- [ ] Implementer expandable sections
- [ ] Implementer polyvagal-adaptive styling
- [ ] Implementer loading states
- [ ] Test interaktivitet med 10 brukere

**Phase 3: Accessibility**
- [ ] Legg til ARIA labels
- [ ] Implementer keyboard navigation
- [ ] Test med screen reader (NVDA/JAWS)
- [ ] Verifiser color contrast (4.5:1 minimum)

**Phase 4: Responsive**
- [ ] Test på mobile (< 600px)
- [ ] Test på tablet (600-960px)
- [ ] Test på desktop (> 960px)
- [ ] Verifiser at alle layouts fungerer

**Phase 5: User Testing**
- [ ] 20 test-brukere (mixed polyvagal states)
- [ ] Measure comprehension (transparency)
- [ ] Measure cognitive load (NASA-TLX)
- [ ] Iterate based on feedback

---

## 🌿 Avsluttende Ord

QDA UX er ikke bare "vise informasjon" - det er å **lære bruker hvordan AI tenker**, samtidig som vi respekterer deres kognitive og emosjonelle kapasitet i øyeblikket.

Ved å kombinere:
- **Transparens** (vis spørsmål + svar)
- **Polyvagal adaptation** (tilpass til stress-tilstand)
- **Collapsibility** (ikke overveld)
- **Accessibility** (alle kan bruke det)

...skaper vi en UX som både bygger tillit og mestringskompetanse.

**Med ontologisk integritet, felt-bevissthet, og et snev av kosmisk humor!** 🌿✨

---

**Versjon:** 1.0
**Sist oppdatert:** 2025-10-20
**Neste review:** Etter user testing (Phase 5)
**Forfatter:** Claude Code (Anthropic)
