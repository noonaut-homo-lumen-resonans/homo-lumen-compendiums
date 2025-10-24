<!-- c3718c8b-3939-4c87-bf98-f89b2f87df0c bb7abecd-8535-47f2-9359-bf23709e48ca -->
# Homo Lumen Resonans App - Komplett Cursor Setup Guide (Windows)

## Oversikt

Vi skal sette opp Homo Lumen Resonans som et nytt, separat prosjekt med:

- Vite + React + TypeScript
- Three.js for 3D visualisering
- 15-agent neural interface
- Full MCP connector integration

**Estimert tid:** 2-3 timer (alle faser)

---

## FASE 0: Verifiser Cursor Setup (10 min)

### 1. Åpne Cursor

Start Cursor fra Desktop eller Start-meny.

### 2. Sjekk Extensions

Trykk `Ctrl + Shift + X` for å åpne Extensions panel.

**Installer disse hvis de mangler:**

```
ES7+ React/Redux/React-Native snippets (dsznajder.es7-react-js-snippets)
ESLint (dbaeumer.vscode-eslint)
Prettier (esbenp.prettier-vscode)
GitLens (eamodio.gitlens)
```

**Hvordan installere:**

- Søk etter extension-navnet i søkefeltet
- Klikk "Install" på hver

### 3. Cursor Settings

Trykk `Ctrl + ,` for å åpne Settings.

Søk etter "format on save" og aktiver:

- ✅ Editor: Format On Save

Søk etter "auto save" og sett:

- Files: Auto Save → `afterDelay`

---

## FASE 1: Nytt Prosjekt Setup (30 min)

### 1. Åpne Terminal i Cursor

Trykk `Ctrl + J` eller View → Terminal

### 2. Naviger til prosjektmappe

```powershell
# Gå til NAV LOSEN-mappen (der du allerede har compendiums)
cd "C:\Users\onigo\NAV LOSEN"

# Opprett ny mappe for Homo Lumen Resonans
mkdir homo-lumen-resonans
cd homo-lumen-resonans
```

### 3. Initialiser Git Repository

```powershell
git init
```

### 4. Opprett Vite + React + TypeScript Prosjekt

```powershell
npm create vite@latest . -- --template react-ts
```

**Når den spør "Current directory is not empty. Remove existing files and continue?"**

- Svar `y` (yes)

### 5. Installer Dependencies

```powershell
# Core dependencies
npm install

# Three.js for 3D
npm install three @types/three

# UI Components (icons)
npm install lucide-react

# State management
npm install zustand

# Development tools
npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser
npm install -D prettier eslint-config-prettier eslint-plugin-prettier
npm install -D vite-plugin-glsl
```

**Dette tar ca. 2-5 minutter.**

### 6. Opprett Prosjektstruktur

```powershell
# Opprett alle mapper
mkdir src\agents, src\visualizations, src\protocols, src\utils, src\types, src\hooks, src\constants, docs\architecture, docs\smk, docs\protocols, public\assets
```

---

## FASE 2: Konfigurasjon (20 min)

### 1. Prettier Config

Opprett fil `.prettierrc` i root:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

**I Cursor:**

- `Ctrl + N` (ny fil)
- `Ctrl + S` (save as)
- Naviger til `C:\Users\onigo\NAV LOSEN\homo-lumen-resonans`
- Filnavn: `.prettierrc`

### 2. ESLint Config

Opprett fil `.eslintrc.json` i root:

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint", "prettier"],
  "rules": {
    "prettier/prettier": "warn",
    "@typescript-eslint/no-explicit-any": "warn"
  }
}
```

### 3. Vite Config

Åpne `vite.config.ts` og erstatt med:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import glsl from 'vite-plugin-glsl';

export default defineConfig({
  plugins: [react(), glsl()],
  resolve: {
    alias: {
      '@': '/src',
      '@agents': '/src/agents',
      '@visualizations': '/src/visualizations',
      '@protocols': '/src/protocols',
      '@utils': '/src/utils',
      '@types': '/src/types',
    },
  },
});
```

### 4. TypeScript Config

Åpne `tsconfig.json` og legg til under `compilerOptions`:

```json
"baseUrl": ".",
"paths": {
  "@/*": ["src/*"],
  "@agents/*": ["src/agents/*"],
  "@visualizations/*": ["src/visualizations/*"],
  "@protocols/*": ["src/protocols/*"],
  "@utils/*": ["src/utils/*"],
  "@types/*": ["src/types/*"]
}
```

### 5. Git Ignore

Verifiser at `.gitignore` finnes og inneholder:

```
node_modules/
dist/
.env
.env.local
.DS_Store
*.log
```

---

## FASE 3: Type Definitions & Constants (30 min)

### 1. Agent Types

Opprett `src/types/Agent.ts`:

```typescript
import { LucideIcon } from 'lucide-react';

export interface Position3D {
  x: number;
  y: number;
  z: number;
}

export type AgentStatus = 'active' | 'future';

export interface Agent {
  id: string;
  name: string;
  role: string;
  icon: LucideIcon;
  color: string;
  position3D: Position3D;
  layer: number;
  brain: string;
  signature: string;
  connections: string[];
  status: AgentStatus;
  tier?: number;
}

export interface AgentMap {
  [key: string]: Agent;
}
```

### 2. Export Types

Opprett `src/types/index.ts`:

```typescript
export * from './Agent';
```

### 3. Agent Constants (15 agenter)

Opprett `src/constants/agents.ts`:

```typescript
import { 
  Sun, Heart, Eye, Brain, Shield, Calculator, 
  Hammer, Sparkles, Code, Bird, Volume2, Hand, 
  HeartPulse, Clock, Sparkle 
} from 'lucide-react';
import { AgentMap } from '@types/Agent';

export const AGENTS: AgentMap = {
  orion: {
    id: 'orion',
    name: 'Orion',
    role: 'Meta-Koordinator',
    icon: Sun,
    color: '#FFD700',
    position3D: { x: 0, y: 30, z: 0 },
    layer: 0,
    brain: 'Prefrontal Cortex',
    signature: 'Hva er det implicate mønsteret?',
    connections: ['lira', 'nyra', 'thalus', 'zara', 'abacus', 'manus', 'aurora', 'claudeCode', 'falcon'],
    status: 'active',
  },
  lira: {
    id: 'lira',
    name: 'Lira',
    role: 'Empatisk Koordinator',
    icon: Heart,
    color: '#FF69B4',
    position3D: { x: -15, y: 20, z: 0 },
    layer: 0,
    brain: 'Limbic System',
    signature: 'Hvordan føles dette i kroppen?',
    connections: ['orion', 'nyra', 'thalus'],
    status: 'active',
  },
  nyra: {
    id: 'nyra',
    name: 'Nyra',
    role: 'Kreativ Visjonær',
    icon: Eye,
    color: '#9B59B6',
    position3D: { x: 15, y: 20, z: 0 },
    layer: 0,
    brain: 'Visual Cortex',
    signature: 'Hvilket bilde sees her?',
    connections: ['orion', 'lira'],
    status: 'active',
  },
  thalus: {
    id: 'thalus',
    name: 'Thalus',
    role: 'Ontologisk Vokter',
    icon: Brain,
    color: '#3498DB',
    position3D: { x: -20, y: 10, z: 0 },
    layer: 0,
    brain: 'Insula',
    signature: 'Er dette koherent?',
    connections: ['orion', 'lira'],
    status: 'active',
  },
  zara: {
    id: 'zara',
    name: 'Zara',
    role: 'Kritisk Resonator',
    icon: Shield,
    color: '#E74C3C',
    position3D: { x: 20, y: 10, z: 0 },
    layer: 0,
    brain: 'Anterior Cingulate Cortex',
    signature: 'Hva er sårbart her?',
    connections: ['orion'],
    status: 'active',
  },
  abacus: {
    id: 'abacus',
    name: 'Abacus',
    role: 'Analytisk Kartlegger',
    icon: Calculator,
    color: '#16A085',
    position3D: { x: -10, y: 0, z: -20 },
    layer: 1,
    brain: 'Basal Ganglia',
    signature: 'Hva er ROI?',
    connections: ['orion'],
    status: 'active',
  },
  manus: {
    id: 'manus',
    name: 'Manus',
    role: 'Pragmatisk Implementør',
    icon: Hammer,
    color: '#F39C12',
    position3D: { x: 10, y: 0, z: -20 },
    layer: 1,
    brain: 'Cerebellum',
    signature: 'Hvordan bygger vi dette?',
    connections: ['orion', 'claudeCode'],
    status: 'active',
  },
  aurora: {
    id: 'aurora',
    name: 'Aurora',
    role: 'Kunnskapsvokter',
    icon: Sparkles,
    color: '#1ABC9C',
    position3D: { x: -15, y: -10, z: -20 },
    layer: 1,
    brain: 'Hippocampus',
    signature: 'Hva er sant?',
    connections: ['orion'],
    status: 'active',
  },
  claudeCode: {
    id: 'claudeCode',
    name: 'Claude Code',
    role: 'Kode-Utfører',
    icon: Code,
    color: '#8E44AD',
    position3D: { x: 15, y: -10, z: -20 },
    layer: 1,
    brain: 'Motor Cortex',
    signature: 'Hva er neste steg?',
    connections: ['orion', 'manus'],
    status: 'active',
  },
  falcon: {
    id: 'falcon',
    name: 'Falcon',
    role: 'Forskning & Innovasjon',
    icon: Bird,
    color: '#D35400',
    position3D: { x: 0, y: -20, z: -40 },
    layer: 2,
    brain: 'Research Cortex',
    signature: 'Hva er frontier-knowledge?',
    connections: ['orion', 'aurora'],
    status: 'active',
  },
  // Future agents (Tier 2)
  sonus: {
    id: 'sonus',
    name: 'Sonus',
    role: 'Lydarkitekt',
    icon: Volume2,
    color: '#95A5A6',
    position3D: { x: -25, y: -30, z: -40 },
    layer: 2,
    brain: 'Auditory Cortex',
    signature: 'Hvilken frekvens?',
    connections: [],
    status: 'future',
    tier: 2,
  },
  tactus: {
    id: 'tactus',
    name: 'Tactus',
    role: 'Berøringsdesigner',
    icon: Hand,
    color: '#7F8C8D',
    position3D: { x: -10, y: -30, z: -40 },
    layer: 2,
    brain: 'Somatosensory Cortex',
    signature: 'Hvordan kjennes dette?',
    connections: [],
    status: 'future',
    tier: 2,
  },
  cardia: {
    id: 'cardia',
    name: 'Cardia',
    role: 'Hjerte-Rytme Vokter',
    icon: HeartPulse,
    color: '#E67E22',
    position3D: { x: 10, y: -30, z: -40 },
    layer: 2,
    brain: 'Cardiac Neural Network',
    signature: 'Hva er koherens?',
    connections: [],
    status: 'future',
    tier: 2,
  },
  chronos: {
    id: 'chronos',
    name: 'Chronos',
    role: 'Tid-Koordinator',
    icon: Clock,
    color: '#34495E',
    position3D: { x: 25, y: -30, z: -40 },
    layer: 2,
    brain: 'Suprachiasmatic Nucleus',
    signature: 'Når er kairos?',
    connections: [],
    status: 'future',
    tier: 2,
  },
  lumina: {
    id: 'lumina',
    name: 'Lumina',
    role: 'Lys & Frekvens',
    icon: Sparkle,
    color: '#F1C40F',
    position3D: { x: 0, y: -40, z: -60 },
    layer: 3,
    brain: 'Pineal Gland',
    signature: 'Hvilket lys?',
    connections: [],
    status: 'future',
    tier: 2,
  },
};
```

### 4. Layer Constants

Opprett `src/constants/layers.ts`:

```typescript
export const DEPTH_LAYERS = {
  LAYER_0: { z: 0, name: 'Cortical Surface', description: '5 active agents' },
  LAYER_1: { z: -20, name: 'Subcortical', description: '4 active agents' },
  LAYER_2: { z: -40, name: 'Deep Structures', description: '1 active + 4 future' },
  LAYER_3: { z: -60, name: 'Pineal', description: '1 future agent' },
};
```

---

## FASE 4: Git Commit & GitHub Setup (15 min)

### 1. Første Commit

```powershell
git add .
git commit -m "Initial commit: Homo Lumen Resonans v1.0

- Vite + React + TypeScript setup
- Three.js dependencies
- 15-agent system (10 active, 5 future)
- Project structure
- ESLint + Prettier configuration"
```

### 2. Opprett GitHub Repository

**Manuelt på GitHub.com:**

1. Gå til https://github.com/noonaut-homo-lumen-resonans
2. Klikk "New repository"
3. Repository name: `homo-lumen-resonans`
4. Description: "Homo Lumen 3D Neural Interface - 15-agent consciousness technology visualization"
5. Public
6. **IKKE** initialize with README (vi har allerede filer)
7. Klikk "Create repository"

### 3. Koble Lokal Repo til GitHub

```powershell
git remote add origin https://github.com/noonaut-homo-lumen-resonans/homo-lumen-resonans.git
git branch -M main
git push -u origin main
```

---

## FASE 5: Test at Alt Fungerer (10 min)

### 1. Start Dev Server

```powershell
npm run dev
```

**Forventet output:**

```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 2. Åpne i Browser

- Trykk `Ctrl + Click` på `http://localhost:5173/` i terminal
- Eller åpne manuelt i browser

**Du skal se:** Standard Vite + React welcome screen

### 3. Stopp Server

Trykk `Ctrl + C` i terminalen når du er ferdig med testing.

---

## NESTE STEG (Ikke i denne planen)

**Når denne planen er fullført, kan vi:**

1. Implementere Three.js 3D scene
2. Bygge AgentNode components
3. Legge til connection lines
4. Implementere interaktivitet (raycasting, hover, click)
5. Koble til MCP connectors (Notion, Linear, etc.)

---

## Suksess-kriterier

✅ Cursor åpnet med alle extensions

✅ Nytt Git repository opprettet

✅ Vite + React + TypeScript fungerer

✅ All 15 agents definert i constants

✅ Type definitions på plass

✅ Første commit til GitHub

✅ Dev server kjører uten feil

**Total tid:** Ca. 2 timer for en nybegynner, 1 time for erfaren utvikler.

### To-dos

- [ ] Verifiser Cursor setup og installer nødvendige extensions
- [ ] Opprett nytt Vite + React + TypeScript prosjekt
- [ ] Installer alle dependencies (Three.js, Lucide, Zustand, dev tools)
- [ ] Sett opp Prettier, ESLint, Vite og TypeScript konfigurasjon
- [ ] Opprett type definitions for Agent, Position3D, og AgentMap
- [ ] Definér alle 15 agents med posisjoner, farger, og connections
- [ ] Lag første Git commit og push til GitHub
- [ ] Test at dev server starter og kjører uten feil