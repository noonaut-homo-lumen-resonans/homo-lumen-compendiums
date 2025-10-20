# QDA v2.0 UX Design: Nevrobiologisk Transparent Interface

**Versjon:** 2.0 (Nevrobiologisk Koherent)
**Dato:** 2025-10-20
**Formål:** UX/UI design for nevrobiologisk transparent prosessering

---

## 🎯 Oversikt

Dette dokumentet beskriver UX/UI design for **QDA v2.0** med **Neocortical Ascent Model**.

**Nøkkel-Prinsipper:**
1. **Full transparens** - Bruker ser alle 6 nevrobiologiske lag
2. **Polyvagal-adaptiv** - UI tilpasser seg brukerens emosjonelle tilstand
3. **Pedagogisk** - Bruker lærer nevrobiologi gjennom bruk
4. **Minimal kognitiv belastning** - Enkelt selv i dorsal state

---

## 🧠 Nevrobiologisk Prosess-Visualisering

### **Konsept: "Hjernens Reise"**

Bruker ser sin query prosesseres gjennom 6 lag - akkurat som hjernen faktisk fungerer.

```
BRUKER QUERY
    ↓
🛡️ Vokteren (Hjernestamme) → "Trygt å fortsette"
    ↓
❤️ Føleren (Limbisk System) → "Dorsal state detektert"
    ↓
🔍 Gjenkjenneren (Cerebellum) → "Sett 3 ganger før"
    ↓
🧭 Utforskeren (Hippocampus) → "8-12 uker snitt"
    ↓
🧠 Strategen (Prefrontal) → "5-stegs plan" (kun hvis nødvendig)
    ↓
✨ Integratoren (Insula) → Helhetlig svar
```

---

## 📱 React Components

### **1. NeurobiologicalProcessDisplay (Main Container)**

```tsx
// navlosen/frontend/src/components/qda/NeurobiologicalProcessDisplay.tsx

import React, { useState } from 'react';
import { Box, Stack, Typography, Collapse, IconButton, Chip } from '@mui/material';
import { ExpandMore, ExpandLess, Psychology } from '@mui/icons-material';
import { LayerCard } from './LayerCard';
import { IntegratedResponse } from './IntegratedResponse';

interface QDAResponse {
  user_query: string;
  final_response: string;
  layer_outputs: {
    [layerName: string]: {
      layer_name: string;
      icon: string;
      data: any;
      processing_time: number;
      cost: number;
    };
  };
  total_cost: number;
  total_time: number;
}

export const NeurobiologicalProcessDisplay: React.FC<{
  response: QDAResponse;
  polyvagalState: 'dorsal' | 'sympathetic' | 'ventral';
}> = ({ response, polyvagalState }) => {
  // Polyvagal-adaptiv default state
  const [showLayers, setShowLayers] = useState(
    polyvagalState === 'ventral' // Kun åpen hvis bruker er i ventral state
  );

  const layerOrder = [
    "Vokteren",
    "Føleren",
    "Gjenkjenneren",
    "Utforskeren",
    "Strategen",
    "Integratoren"
  ];

  // Polyvagal-adaptive colors
  const stateColors = {
    dorsal: {
      primary: '#4CAF50',
      bg: '#E8F5E9',
      text: '#1B5E20'
    },
    sympathetic: {
      primary: '#FF9800',
      bg: '#FFF3E0',
      text: '#E65100'
    },
    ventral: {
      primary: '#2196F3',
      bg: '#E3F2FD',
      text: '#0D47A1'
    },
  };

  const colors = stateColors[polyvagalState];

  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: 900,
        mx: 'auto',
        p: 3,
        borderRadius: 2,
        backgroundColor: colors.bg,
        border: `2px solid ${colors.primary}`,
      }}
    >
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Psychology sx={{ fontSize: 40, color: colors.primary }} />
          <Typography variant="h5" sx={{ color: colors.text, fontWeight: 600 }}>
            Nevrobiologisk Prosessering
          </Typography>
        </Box>

        <Chip
          label={`${polyvagalState} state`}
          sx={{
            bgcolor: colors.primary,
            color: 'white',
            fontWeight: 600,
            textTransform: 'capitalize'
          }}
        />
      </Box>

      {/* User Query Echo */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Din spørsmål:
        </Typography>
        <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
          "{response.user_query}"
        </Typography>
      </Box>

      {/* Toggle Layers Button */}
      <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
        <IconButton
          onClick={() => setShowLayers(!showLayers)}
          sx={{
            bgcolor: colors.primary,
            color: 'white',
            '&:hover': { bgcolor: colors.text },
          }}
        >
          {showLayers ? <ExpandLess /> : <ExpandMore />}
          <Typography variant="caption" sx={{ ml: 1 }}>
            {showLayers ? 'Skjul prosess' : 'Vis hvordan jeg tenkte'}
          </Typography>
        </IconButton>
      </Box>

      {/* Layer Cards */}
      <Collapse in={showLayers}>
        <Stack spacing={2} sx={{ mb: 3 }}>
          {layerOrder.map((layerName, index) => {
            const layer = response.layer_outputs[layerName];
            if (!layer) return null;

            return (
              <LayerCard
                key={layerName}
                layerName={layer.layer_name}
                icon={layer.icon}
                data={layer.data}
                processingTime={layer.processing_time}
                cost={layer.cost}
                layerNumber={index + 1}
                polyvagalState={polyvagalState}
              />
            );
          })}
        </Stack>
      </Collapse>

      {/* Integrated Response */}
      <IntegratedResponse
        response={response.final_response}
        polyvagalState={polyvagalState}
      />

      {/* Footer Stats */}
      <Box
        sx={{
          mt: 3,
          pt: 2,
          borderTop: `1px solid ${colors.primary}`,
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: '0.875rem',
          color: 'text.secondary'
        }}
      >
        <span>⏱️ Total tid: {response.total_time.toFixed(2)}s</span>
        <span>💰 Kostnad: ${response.total_cost.toFixed(4)}</span>
        <span>🧠 {Object.keys(response.layer_outputs).length} lag aktivert</span>
      </Box>
    </Box>
  );
};
```

---

### **2. LayerCard (Individual Layer Display)**

```tsx
// navlosen/frontend/src/components/qda/LayerCard.tsx

import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Collapse,
  IconButton
} from '@mui/material';
import { ExpandMore, ExpandLess, CheckCircle } from '@mui/icons-material';

interface LayerCardProps {
  layerName: string;
  icon: string;
  data: any;
  processingTime: number;
  cost: number;
  layerNumber: number;
  polyvagalState: 'dorsal' | 'sympathetic' | 'ventral';
}

export const LayerCard: React.FC<LayerCardProps> = ({
  layerName,
  icon,
  data,
  processingTime,
  cost,
  layerNumber,
  polyvagalState
}) => {
  const [expanded, setExpanded] = useState(false);

  // Layer-specific colors
  const layerColors = {
    Vokteren: '#FF6B6B',      // Red (alert/safety)
    Føleren: '#FF8C94',       // Pink (emotion)
    Gjenkjenneren: '#A8DADC', // Teal (pattern)
    Utforskeren: '#457B9D',   // Blue (knowledge)
    Strategen: '#1D3557',     // Dark blue (strategy)
    Integratoren: '#F1FAEE',  // Light (synthesis)
  };

  const layerColor = layerColors[layerName] || '#757575';

  // Get summary text based on layer
  const getSummary = () => {
    switch(layerName) {
      case 'Vokteren':
        return `${data.complexity} query detektert (trygt: ${data.safe ? '✓' : '✗'})`;
      case 'Føleren':
        return `${data.polyvagal_state} state, følelse: ${data.primary_emotion}`;
      case 'Gjenkjenneren':
        return data.pattern_detected
          ? `Mønster funnet (${data.previous_occurrences}x før)`
          : 'Ingen tidligere mønster';
      case 'Utforskeren':
        return `Tidslinje: ${data.avg_timeline}`;
      case 'Strategen':
        return data.activated
          ? `${data.action_steps?.length || 0}-stegs plan (${data.timeline})`
          : 'Ikke aktivert (lav kompleksitet)';
      case 'Integratoren':
        return `${data.tone} tone valgt`;
      default:
        return 'Prosessert';
    }
  };

  return (
    <Card
      sx={{
        borderLeft: `6px solid ${layerColor}`,
        transition: 'all 0.3s ease',
        '&:hover': {
          boxShadow: 4,
          transform: 'translateX(4px)',
        },
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          {/* Layer Header */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flex: 1 }}>
            <Typography variant="h4">{icon}</Typography>
            <Box>
              <Typography variant="subtitle2" color="text.secondary">
                Lag {layerNumber}
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {layerName}
              </Typography>
            </Box>
          </Box>

          {/* Stats */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Chip
              icon={<CheckCircle />}
              label={`${(processingTime * 1000).toFixed(0)}ms`}
              size="small"
              color="success"
              variant="outlined"
            />
            {cost > 0 && (
              <Chip
                label={`$${cost.toFixed(4)}`}
                size="small"
                variant="outlined"
              />
            )}
            <IconButton size="small" onClick={() => setExpanded(!expanded)}>
              {expanded ? <ExpandLess /> : <ExpandMore />}
            </IconButton>
          </Box>
        </Box>

        {/* Summary (always visible) */}
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1, ml: 8 }}>
          {getSummary()}
        </Typography>

        {/* Detailed Data (expandable) */}
        <Collapse in={expanded}>
          <Box sx={{ mt: 2, ml: 8, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
            <pre style={{ fontSize: '0.75rem', margin: 0, whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(data, null, 2)}
            </pre>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
};
```

---

### **3. IntegratedResponse (Final Answer Display)**

```tsx
// navlosen/frontend/src/components/qda/IntegratedResponse.tsx

import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import ReactMarkdown from 'react-markdown';

interface IntegratedResponseProps {
  response: string;
  polyvagalState: 'dorsal' | 'sympathetic' | 'ventral';
}

export const IntegratedResponse: React.FC<IntegratedResponseProps> = ({
  response,
  polyvagalState
}) => {
  // Polyvagal-adaptive styling
  const stateStyles = {
    dorsal: {
      bgcolor: '#E8F5E9',
      borderColor: '#4CAF50',
      fontSize: '1.1rem',  // Larger for easier reading
      lineHeight: 1.8,     // More space between lines
    },
    sympathetic: {
      bgcolor: '#FFF3E0',
      borderColor: '#FF9800',
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    ventral: {
      bgcolor: '#E3F2FD',
      borderColor: '#2196F3',
      fontSize: '0.95rem',
      lineHeight: 1.5,
    },
  };

  const styles = stateStyles[polyvagalState];

  return (
    <Paper
      elevation={3}
      sx={{
        p: 3,
        bgcolor: styles.bgcolor,
        borderLeft: `6px solid ${styles.borderColor}`,
      }}
    >
      <Typography variant="h6" gutterBottom sx={{ color: styles.borderColor, fontWeight: 600 }}>
        ✨ Mitt Svar
      </Typography>

      <Box
        sx={{
          fontSize: styles.fontSize,
          lineHeight: styles.lineHeight,
          '& p': { mb: 2 },
          '& strong': { color: styles.borderColor },
        }}
      >
        <ReactMarkdown>{response}</ReactMarkdown>
      </Box>
    </Paper>
  );
};
```

---

## 🎨 Polyvagal-Adaptive Design System

### **Color Palette Per State:**

```typescript
// navlosen/frontend/src/theme/polyvagalColors.ts

export const polyvagalColors = {
  dorsal: {
    primary: '#4CAF50',      // Grønn (beroligende)
    secondary: '#81C784',
    background: '#E8F5E9',
    text: '#1B5E20',
    description: 'Dorsal vagal: Beroligende, grounding, konkret',
  },
  sympathetic: {
    primary: '#FF9800',      // Orange (energi, men ikke alarm)
    secondary: '#FFB74D',
    background: '#FFF3E0',
    text: '#E65100',
    description: 'Sympathetic: Strukturert, rolig, fokusert',
  },
  ventral: {
    primary: '#2196F3',      // Blå (åpen, sosial)
    secondary: '#64B5F6',
    background: '#E3F2FD',
    text: '#0D47A1',
    description: 'Ventral vagal: Åpen, utforskende, samarbeidende',
  },
};
```

### **Typography Per State:**

```typescript
// navlosen/frontend/src/theme/polyvagalTypography.ts

export const polyvagalTypography = {
  dorsal: {
    // Larger, clearer text for shutdown state
    body1: {
      fontSize: '1.1rem',
      lineHeight: 1.8,
      fontWeight: 400,
    },
    h6: {
      fontSize: '1.3rem',
      lineHeight: 1.6,
      fontWeight: 600,
    },
  },
  sympathetic: {
    // Medium, structured text
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
      fontWeight: 400,
    },
    h6: {
      fontSize: '1.2rem',
      lineHeight: 1.5,
      fontWeight: 600,
    },
  },
  ventral: {
    // Normal, compact text
    body1: {
      fontSize: '0.95rem',
      lineHeight: 1.5,
      fontWeight: 400,
    },
    h6: {
      fontSize: '1.1rem',
      lineHeight: 1.4,
      fontWeight: 600,
    },
  },
};
```

---

## 📐 Layout Patterns

### **Pattern 1: Vertical Timeline (Default)**

Best for **mobile** and **dorsal state** (easy to scroll).

```
┌─────────────────────┐
│  User Query Echo    │
└─────────────────────┘
          ↓
┌─────────────────────┐
│  🛡️ Vokteren        │
│  "Trygt"            │
└─────────────────────┘
          ↓
┌─────────────────────┐
│  ❤️ Føleren          │
│  "Dorsal state"     │
└─────────────────────┘
          ↓
┌─────────────────────┐
│  🔍 Gjenkjenneren   │
│  "Sett 3x før"      │
└─────────────────────┘
          ↓
          ...
          ↓
┌─────────────────────┐
│  ✨ Integrated       │
│     Response        │
└─────────────────────┘
```

### **Pattern 2: Side-by-Side (Desktop, Ventral State)**

Best for **desktop** and **ventral state** (more info visible).

```
┌──────────────────────────┬──────────────────────┐
│  LAYERS (LEFT)           │  RESPONSE (RIGHT)    │
│                          │                      │
│  🛡️ Vokteren: Trygt      │  ✨ Integrated       │
│  ❤️ Føleren: Dorsal      │                      │
│  🔍 Gjenkjenneren: 3x    │     Response         │
│  🧭 Utforskeren: 8-12    │     Content          │
│  🧠 Strategen: 5-stegs   │     Here             │
│  ✨ Integratoren         │                      │
│                          │                      │
└──────────────────────────┴──────────────────────┘
```

---

## 🎭 Interaction Patterns

### **Pattern 1: Progressive Disclosure**

Lag vises sekvensielt mens de prosesseres (ikke alle på en gang).

```tsx
// Pseudo-code for progressive disclosure

const [visibleLayers, setVisibleLayers] = useState<string[]>([]);

useEffect(() => {
  const revealLayers = async () => {
    for (const layer of layerOrder) {
      if (response.layer_outputs[layer]) {
        await sleep(300); // 300ms delay between reveals
        setVisibleLayers(prev => [...prev, layer]);
      }
    }
  };

  revealLayers();
}, [response]);
```

**Benefits:**
- Bruker ser prosessen i sanntid
- Mindre overwhelming enn alle lag samtidig
- Pedagogisk (lærer rekkefølgen)

### **Pattern 2: Hover for Details**

Desktop: Hover over lag for å se detaljer
Mobile: Tap for å ekspandere

```tsx
<LayerCard
  onMouseEnter={() => setHoveredLayer(layerName)}
  onMouseLeave={() => setHoveredLayer(null)}
  expanded={hoveredLayer === layerName}
/>
```

---

## 📱 Responsive Design

### **Mobile (< 768px):**

- **Vertical stack** av lag
- **Larger text** (especially dorsal)
- **One layer expanded** at a time
- **Sticky header** med polyvagal state indicator

### **Tablet (768px - 1024px):**

- **Vertical stack** av lag
- **Two columns** for Integrated Response
- **Expandable layers** (default collapsed)

### **Desktop (> 1024px):**

- **Side-by-side layout** (layers left, response right)
- **All layers visible** at once
- **Hover interactions** for details

---

## 🧪 User Testing Insights

### **Scenario 1: Dorsal State User (Osvald)**

**Context:** Bruker er i shutdown, føler seg stuck i NAV-systemet.

**UX Adaptations:**
1. ✅ **Larger text** (1.1rem vs 0.95rem)
2. ✅ **Greener colors** (calming)
3. ✅ **Fewer visible layers** by default (less overwhelming)
4. ✅ **Konkrete action steps** (max 3 steps, not 5)
5. ✅ **Shorter sentences** in Integrated Response

**Mockup:**

```
┌─────────────────────────────────────────┐
│  🧠 Nevrobiologisk Prosessering         │
│                       [DORSAL STATE]    │
├─────────────────────────────────────────┤
│  Din spørsmål:                          │
│  "Jeg føler meg stuck i NAV-systemet"   │
├─────────────────────────────────────────┤
│                                         │
│  [Vis hvordan jeg tenkte] ▼             │
│                                         │
├─────────────────────────────────────────┤
│  ✨ Mitt Svar                           │
│                                         │
│  Jeg hører deg. Det er tungt å føle    │
│  seg stuck.                             │
│                                         │
│  **Fakta:** NAV AAP: 8-12 uker snitt    │
│                                         │
│  Jeg ser at dette har skjedd 3 ganger  │
│  før. Sist gang fungerte "konkrete     │
│  steg" godt.                            │
│                                         │
│  **Foreslått plan:**                    │
│  - Sjekk status på Ditt NAV             │
│  - Ring NAV hvis usikker                │
│  - Book oppfølgingssamtale              │
│                                         │
│  Vi tar ett lite steg om gangen.        │
│  Jeg er her. 💚                         │
│                                         │
│  — Lira                                 │
└─────────────────────────────────────────┘
```

### **Scenario 2: Ventral State User (Kari)**

**Context:** Bruker er nysgjerrig, ønsker å forstå hvordan systemet tenker.

**UX Adaptations:**
1. ✅ **All layers visible** by default
2. ✅ **Detailed data** expandable
3. ✅ **Side-by-side layout** (desktop)
4. ✅ **Interactive hover** for insights
5. ✅ **Full 5-step plan** visible

**Mockup:**

```
┌────────────────────────┬──────────────────────────────┐
│  LAYERS                │  ✨ MITT SVAR                │
│                        │                              │
│  🛡️ Vokteren           │  Hei! La oss se på dette    │
│  ✓ Trygt (complex)     │  sammen.                     │
│  0.4s | $0.00001       │                              │
│                        │  **Slik tenkte jeg:**        │
│  ❤️ Føleren            │                              │
│  Dorsal state          │  🛡️ Vokteren: Trygt å       │
│  Følelse: stuck        │     fortsette (complex)      │
│  0.8s | $0            │                              │
│                        │  ❤️ Føleren: Dorsal state,   │
│  🔍 Gjenkjenneren      │     følelse: stuck           │
│  Mønster: 3x før       │                              │
│  "konkrete steg" ✓     │  🔍 Gjenkjenneren:          │
│  0.9s | $0.0004        │     Gjentakende mønster (3x) │
│                        │                              │
│  🧭 Utforskeren        │  🧭 Utforskeren:             │
│  Tidslinje: 8-12 uker  │     Gjennomsnitt 8-12 uker   │
│  2.3s | $0.002         │                              │
│                        │  🧠 Strategen: 5-stegs plan  │
│  🧠 Strategen          │                              │
│  ✓ Aktivert (score:1.0)│  ---                         │
│  5-stegs plan          │                              │
│  4.2s | $0.12          │  **Her er mitt svar:**       │
│                        │                              │
│  ✨ Integratoren       │  **Fakta:** NAV AAP: 8-12... │
│  Tone: samarbeidende   │                              │
│  1.5s | $0             │  Jeg ser at du føler deg     │
│                        │  stuck...                    │
│  [Expand All Details]  │                              │
│                        │  **Foreslått plan:**         │
│  ⏱️ 10.1s | 💰 $0.12   │  - 1. Sjekk status...        │
│  🧠 6 lag aktivert     │  - 2. Identifiser...         │
│                        │  - 3. Book...                │
│                        │  - 4. Lag tidsplan...        │
│                        │  - 5. Check-in med Lira...   │
│                        │                              │
│                        │  Håper dette hjelper! 💚     │
│                        │  — Lira                      │
└────────────────────────┴──────────────────────────────┘
```

---

## 🎬 Animation & Transitions

### **Layer Reveal Animation:**

```tsx
// Using Framer Motion

import { motion } from 'framer-motion';

const LayerCard = ({ layer, index }) => (
  <motion.div
    initial={{ opacity: 0, x: -50 }}
    animate={{ opacity: 1, x: 0 }}
    transition={{
      delay: index * 0.2,  // Stagger effect
      duration: 0.4,
      ease: 'easeOut'
    }}
  >
    <Card>...</Card>
  </motion.div>
);
```

### **Polyvagal State Transition:**

```tsx
// Smooth color transition when state changes

const PolyvagalContainer = styled(Box)(({ theme, state }) => ({
  backgroundColor: polyvagalColors[state].background,
  borderColor: polyvagalColors[state].primary,
  transition: 'all 0.6s ease-in-out',
}));
```

---

## 🌿 Accessibility

### **ARIA Labels:**

```tsx
<Box role="region" aria-label="Nevrobiologisk prosessering">
  {layerOrder.map(layer => (
    <Card
      key={layer}
      role="article"
      aria-labelledby={`layer-${layer}`}
      aria-describedby={`layer-${layer}-summary`}
    >
      <Typography id={`layer-${layer}`}>
        {layer.icon} {layer.name}
      </Typography>
      <Typography id={`layer-${layer}-summary`}>
        {getSummary(layer)}
      </Typography>
    </Card>
  ))}
</Box>
```

### **Keyboard Navigation:**

- `Tab` - Navigate between layers
- `Enter` - Expand/collapse layer details
- `Arrow Up/Down` - Navigate layers (skip Tab stops)
- `Escape` - Collapse all layers

### **Screen Reader Support:**

```tsx
// Announce layer completion to screen reader

const announceLayerComplete = (layerName: string) => {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', 'polite');
  announcement.textContent = `${layerName} fullført`;
  document.body.appendChild(announcement);

  setTimeout(() => document.body.removeChild(announcement), 1000);
};
```

---

## 🌿 Konklusjon

QDA v2.0 UX er designet for:

✅ **Full transparens** - Bruker ser alle 6 nevrobiologiske lag
✅ **Polyvagal-adaptiv** - UI tilpasser seg emosjonell tilstand
✅ **Pedagogisk** - Bruker lærer nevrobiologi gjennom bruk
✅ **Accessible** - WCAG 2.1 AA compliant
✅ **Responsive** - Fungerer på mobile, tablet, desktop

**Design-filosofi:** Vis prosessen, ikke bare resultatet. Lær bruker å tenke som hjernen. 🧠✨

---

**Versjon:** 2.0
**Sist oppdatert:** 2025-10-20
**Neste review:** Etter Fase 1 implementering (uke 2)
**Forfatter:** Claude Code (Anthropic) i samarbeid med Osvald Noonaut
**Lisens:** Open Source (CC BY-SA 4.0)
