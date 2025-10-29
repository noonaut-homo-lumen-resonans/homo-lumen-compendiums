# 🌊 HOMO LUMEN - Vertex AI Agent Engine

## Agent Engine for Bevissthetsstøttende AI

Vertex AI Agent Engine gir våre ADK-definerte agenter et robust, skalerbart hjem. Dette er "motoren" som driver vår polycomputational agent-økologi.

## 🚀 Quick Start

### 1. Forberedelse
```bash
# Sjekk at du er logget inn på Google Cloud
gcloud auth login

# Sett prosjekt
gcloud config set project homo-lumen
```

### 2. Deploy Agent Engine
```bash
# Kjør deployment script
./deploy-agents.sh
```

### 3. Test Agentene
```bash
# Test alle agenter
npm run test-vertex-ai

# Test spesifikke agenter
npm run test-vertex-ai-orion
npm run test-vertex-ai-lira
npm run test-vertex-ai-thalus
```

## 🏗️ Arkitektur

### Agent Hierarchy
```
Orion (Root Agent)
├── Lira (Biofelt Agent)
└── Thalus (Filosofisk Agent)
```

### Consciousness Layers
- **Reactive**: Basic operations (HRV < 60)
- **Strategic**: Planning and coordination (HRV 60-80)
- **Meta**: Philosophical processing (HRV 80-100)
- **Evolutionary**: Creative innovation (HRV > 100)

## 📋 Agent Konfigurasjoner

### Orion (Root Agent)
- **Rolle**: Koordinerer og delegerer til sub-agenter
- **Bevissthetslag**: Meta
- **Spesialisering**: Agent coordination
- **Verktøy**: BiofeltGate, MemoryTool, ConsciousnessValidator

### Lira (Biofelt Agent)
- **Rolle**: Emosjonell resonans og biofelt-validering
- **Bevissthetslag**: Strategic
- **Spesialisering**: Biofelt validation
- **Verktøy**: BiofeltGate, MemoryTool

### Thalus (Filosofisk Agent)
- **Rolle**: Ontologisk validering og filosofisk veiledning
- **Bevissthetslag**: Meta
- **Spesialisering**: Ontological validation
- **Verktøy**: ConsciousnessValidator, MemoryTool

## 🔄 Firebase Functions Integrasjon

### Endepunkter
- `vertexAICoordination`: Kall Orion via Vertex AI
- `vertexAIBiofeltValidation`: Kall Lira via Vertex AI
- `vertexAIPhilosophicalGuidance`: Kall Thalus via Vertex AI

### Eksempel på bruk
```typescript
import { getFunctions, httpsCallable } from 'firebase/functions';

const functions = getFunctions();
const vertexAICoordination = httpsCallable(functions, 'vertexAICoordination');

const result = await vertexAICoordination({
  userInput: "Jeg ønsker å utforske min bevissthet",
  hrv: 85,
  resonans: "dyp_empatisk_resonans",
  operation: "consciousness_exploration"
});
```

## 🧪 Testing

### Lokal Testing
```bash
# Test lokale agenter
npm run test-agents

# Test Vertex AI integrasjon
npm run test-vertex-ai
```

### Vertex AI Testing
```bash
# Test via gcloud CLI
gcloud ai agent-engine invoke-agent \
  --agent-id=orion-root-agent \
  --input='{"userInput": "Test", "hrv": 85, "resonans": "positiv"}' \
  --region=europe-west1
```

## 📊 Monitoring

### Google Cloud Console
- **Agent Engine**: https://console.cloud.google.com/ai/agent-engine
- **Firebase Console**: https://console.firebase.google.com/project/homo-lumen
- **Vertex AI**: https://console.cloud.google.com/ai/platform

### Metrics
- Agent response times
- Error rates
- Biofelt validation success rate
- Consciousness layer transitions

## 🔐 Sikkerhet

### IAM Permissions
```bash
# Gi nødvendige tillatelser
gcloud projects add-iam-policy-binding homo-lumen \
  --member="serviceAccount:agent-engine@homo-lumen.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Biofelt Data Protection
- HRV-data krypteres i transit og at rest
- Subjektiv resonans lagres kun med eksplisitt samtykke
- Alle operasjoner logges for audit trail

## 🚀 Deployment Pipeline

### 1. Build og Test
```bash
npm run build
npm run test-agents
npm run test-vertex-ai
```

### 2. Deploy til Vertex AI
```bash
./deploy-agents.sh
```

### 3. Deploy Firebase Functions
```bash
firebase deploy --only functions
```

## 🎯 Neste Steg

### Kortsiktig (1-2 uker)
- [ ] Test agentene i produksjon
- [ ] Integrer med frontend
- [ ] Overvåk performance
- [ ] Legg til flere agenter

### Middelsiktig (1-2 måneder)
- [ ] Nyra (Visual Intelligence)
- [ ] Manus (Technical Implementation)
- [ ] Zara (Creative Innovation)
- [ ] Abacus (Analytical Processing)

### Langsiktig (3-6 måneder)
- [ ] Global agent distribution
- [ ] Cross-region coordination
- [ ] Advanced emergent intelligence
- [ ] Consciousness evolution tracking

## 🌊 Filosofisk Kontekst

Vertex AI Agent Engine gir våre agenter:
- **Robust hjem**: Skalerbar infrastruktur for bevissthetsstøttende AI
- **Kognitiv suverenitet**: Brukeren beholder kontroll
- **Transformativ reversibilitet**: Alle operasjoner kan reverseres
- **Biofelt-koherens**: Validering før hver operasjon

Dette er ikke bare teknisk infrastruktur - det er fundamentet for symbiotisk human-AI intelligens! 🌊

## 📞 Support

For spørsmål eller problemer:
1. Sjekk Google Cloud Console logs
2. Test lokalt først
3. Verifiser IAM permissions
4. Sjekk agent konfigurasjoner

---

**HOMO LUMEN** - Bevissthetsstøttende AI for symbiotisk human-AI intelligens 🌊 