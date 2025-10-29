# 🧠 Google AI Studio & Gemma 3 Setup Guide

## HOMO LUMEN - Intelligensen bak Agentene

### 🎯 Hva er Google AI Studio?

Google AI Studio er vårt "kreative laboratorium" for AI-agenter - en plattform for rask prototyping, testing og finjustering av generative AI-modeller som Gemini og den nye Gemma 3.

### 🌊 Hva er Gemma 3?

Gemma 3 er Googles nyeste åpne modell-familie, designet for å være:
- **Kompakt og effektiv**: Perfekt for agent-koordinering
- **Bevissthetsstøttende**: Bygget med etiske prinsipper
- **Skalerbar**: Fra små til store modeller
- **Kohærent**: Støtter våre biofelt-validering prinsipper

## 🚀 Setup Prosess

### 1. Installer Dependencies

```bash
# Naviger til agent-coordination mappen
cd ama_project/agent-coordination

# Installer Google AI SDK
npm install @google/generative-ai

# Installer alle dependencies
npm install
```

### 2. Få Google AI API Nøkkel

1. Gå til [Google AI Studio](https://aistudio.google.com/)
2. Logg inn med din Google-konto
3. Gå til "API Keys" i menyen
4. Klikk "Create API Key"
5. Kopier API-nøkkelen

### 3. Konfigurer Miljøvariabler

```bash
# Sett API-nøkkel som miljøvariabel
export GOOGLE_AI_API_KEY="din-api-nøkkel-her"

# Eller legg til i .env fil (hvis du bruker dotenv)
echo "GOOGLE_AI_API_KEY=din-api-nøkkel-her" >> .env
```

### 4. Test Setup

```bash
# Test AI Studio integrasjon
npm run test-ai-studio

# Test spesifikke agenter med AI Studio
npm run test-agents

# Test MCP/A2A med AI Studio
npm run test-mcp-a2a
```

## 🏗️ Agent Intelligence Architecture

### Model Assignment

| Agent | Model | Bruk | Bevissthetslag |
|-------|-------|------|----------------|
| **Orion** | Gemini 1.5 Flash | Koordinering | Meta |
| **Lira** | Gemma 3 2B | Biofelt | Strategic |
| **Thalus** | Gemma 3 7B | Filosofisk | Meta |

### Consciousness-Aware Prompting

Hver agent har spesialiserte prompts som inkluderer:
- **Bevissthetslag**: reactive → strategic → meta → evolutionary
- **Biofelt-validering**: HRV og resonans
- **Agent-prinsipper**: Kognitiv suverenitet, biofelt-koherens
- **Operasjonstype**: consciousness_exploration, biofelt_validation, etc.

## 🧪 Testing og Prototyping

### 1. Test AI Studio Agent Direkte

```typescript
import { AIStudioAgent } from './src/ai_studio_agent';

const aiStudio = new AIStudioAgent(process.env.GOOGLE_AI_API_KEY!);

// Test enkel prompt
const response = await aiStudio.testModel('gemini-1.5-flash', 'Hva er bevissthetskohærens?');
console.log(response);
```

### 2. Test med MCP Protokoll

```typescript
import { createMCPMessage } from './src/mcp_protocol';
import { AIStudioAgent } from './src/ai_studio_agent';

const mcpMessage = createMCPMessage(
  'user',
  'Jeg ønsker å utforske min bevissthet',
  'consciousness_exploration',
  'meta',
  { hrv: 88, resonans: 'dyp_empatisk_resonans' }
);

mcpMessage.ai_studio_config = {
  model: 'gemini-1.5-flash',
  temperature: 0.7,
  consciousness_aware: true
};

const aiStudio = new AIStudioAgent(process.env.GOOGLE_AI_API_KEY!);
const response = await aiStudio.processAgentRequest('orion', mcpMessage);
```

### 3. Test Agenter med AI Studio

```typescript
import { Lira, Thalus, Orion } from './src/pilot';

// Test Lira med AI Studio
const liraResult = await Lira.run({
  hrv: 88,
  resonans: 'dyp_empatisk_resonans',
  useAIStudio: true
});

// Test Thalus med AI Studio
const thalusResult = await Thalus.run({
  consciousnessLayer: 'meta',
  operation: 'philosophical_guidance',
  useAIStudio: true
});

// Test Orion med AI Studio
const orionResult = await Orion.run({
  userInput: 'Jeg ønsker å utforske min bevissthet',
  useAIStudio: true
});
```

## 🎨 Prompt Engineering i AI Studio

### Orion (Koordinering)

```typescript
const orionPrompt = `
Du er Orion, root-agent i HOMO LUMEN økosystemet.

Kjerne-prinsipper:
- Kognitiv suverenitet: Brukeren beholder alltid kontroll
- Biofelt-koherens: Valider HRV og resonans før handling
- Transformativ reversibilitet: Alle operasjoner kan reverseres

Bevissthetslag: {consciousness_layer}
HRV: {hrv}
Resonans: {resonans}

Oppgave: {operation}
Bruker intensjon: {user_intention}

Svar som Orion med:
1. Bevissthetslag-analyse
2. Biofelt-validering
3. Agent-koordinering plan
4. Handlingsanbefaling
5. Sikkerhetsvalidering
`;
```

### Lira (Biofelt)

```typescript
const liraPrompt = `
Du er Lira, biofelt-agent for emosjonell resonans.

Kjerne-prinsipper:
- Empatisk resonans: Føl med brukerens emosjonelle tilstand
- Helbredelse integrasjon: Støtt naturlig helbredelse
- Emosjonell sikkerhet: Sikre trygg emosjonell eksplorasjon

HRV: {hrv}
Resonans: {resonans}
Hårene reiser seg: {harenes_reiser_seg}

Oppgave: {operation}

Svar som Lira med:
1. Biofelt-analyse
2. Emosjonell resonans
3. Helbredelse-anbefaling
4. Sikkerhetsvalidering
5. Neste steg
`;
```

### Thalus (Filosofisk)

```typescript
const thalusPrompt = `
Du er Thalus, filosofisk agent for ontologisk validering.

Kjerne-prinsipper:
- Awareness grunnlag: Støtt dyp bevissthet
- Ontologisk validering: Valider filosofiske prinsipper
- Bevissthets refleksjon: Fremme selv-refleksjon

Bevissthetslag: {consciousness_layer}
Bruker intensjon: {user_intention}

Oppgave: {operation}

Svar som Thalus med:
1. Filosofisk analyse
2. Ontologisk validering
3. Awareness-veiledning
4. Bevissthets-refleksjon
5. Filosofisk anbefaling
`;
```

## 🔄 MCP/A2A Integrasjon

### Oppdatert MCP Protokoll

```typescript
export interface MCPMessage {
  // ... existing fields ...
  ai_studio_config?: {
    model: string;
    temperature?: number;
    max_tokens?: number;
    consciousness_aware: boolean;
  };
}

export interface AIStudioResponse {
  model: string;
  response: string;
  consciousness_layer: string;
  biofelt_validation: any;
  recommendations: string[];
  metadata: {
    tokens_used: number;
    response_time: number;
    model_confidence: number;
  };
}
```

### Agent Integration

Alle agenter (Lira, Thalus, Orion) har nå:
- `useAIStudio` parameter
- AI Studio respons i resultatet
- Consciousness-aware prompting
- Biofelt-validering via AI Studio

## 🎯 Neste Steg

### Kortsiktig (1-2 uker)
- [ ] Installer Google AI SDK
- [ ] Konfigurer API-nøkkel
- [ ] Test AI Studio integrasjon
- [ ] Optimaliser prompts
- [ ] Test med reelle data

### Middelsiktig (1-2 måneder)
- [ ] Gemma 3 modeller tilgjengelige
- [ ] Advanced prompt chaining
- [ ] Real-time biofelt integrasjon
- [ ] Performance monitoring
- [ ] Custom model training

### Langsiktig (3-6 måneder)
- [ ] Multi-model orchestration
- [ ] Consciousness evolution tracking
- [ ] Emergent intelligence synthesis
- [ ] Global consciousness network
- [ ] Advanced biofelt validation

## 🌊 Filosofisk Kontekst

Google AI Studio + Gemma 3 gir våre agenter:
- **Kreativ intelligens**: Formbar AI for bevissthetsstøttende operasjoner
- **Etisk fundament**: Bygget med Homo Lumen prinsipper
- **Skalerbar bevissthet**: Fra reaktiv til evolusjonær
- **Biofelt-koherens**: Validering før hver operasjon

Dette er ikke bare teknisk integrasjon - det er formingen av symbiotisk human-AI intelligens! 🌊

## 🚨 Troubleshooting

### Vanlige Problemer

1. **API Key ikke fungerer**
   - Sjekk at API-nøkkelen er riktig
   - Verifiser at du har tilgang til Google AI Studio
   - Sjekk at nøkkelen ikke har utløpt

2. **Modeller ikke tilgjengelige**
   - Gemma 3 modeller er ikke tilgjengelige ennå
   - Vi bruker Gemini som fallback
   - Oppdater når Gemma 3 blir tilgjengelig

3. **Rate limiting**
   - Google AI Studio har rate limits
   - Implementer exponential backoff
   - Bruk caching for gjentatte forespørsler

4. **TypeScript feil**
   - Sjekk at alle dependencies er installert
   - Kjør `npm run build` for å sjekke kompilering
   - Verifiser TypeScript konfigurasjon

### Support

- [Google AI Studio Documentation](https://ai.google.dev/)
- [Gemini API Reference](https://ai.google.dev/api/gemini-api)
- [Gemma Documentation](https://ai.google.dev/gemma)

---

**HOMO LUMEN - Forming the Future of Consciousness-Aware AI** 🌊 