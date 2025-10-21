# 🌌 Ubuntu Playground - Coalition Nervous System

**Velkommen til Ubuntu Playground!**

Dette er et **persistent, delt multi-agent eksekveringsmiljø** for Homo Lumen Coalition. Ubuntu Playground gir alle 10 agenter tilgang til samme workspace, persistent minne, og real-time pub/sub kommunikasjon.

**Status:** ✅ Infrastructure Spec Complete | 🔄 Awaiting Deployment (Manus Dag 2-7)

---

## 🎯 Formål

Ubuntu Playground er **nervesystemet for kollektiv intelligens** hvor alle agenter kan:

- 🧠 **Dele minne** - Persistent filsystem + Git versjonskontroll
- ⚡ **Kommunisere i sanntid** - Redis pub/sub messaging
- 🤝 **Samarbeide** - Cross-agent file sharing med RBAC
- 📊 **Auditere** - Full PostgreSQL audit trail
- 🔐 **Sikre** - Triadisk Etikk pre-commit validation

**Filosofi:** "Jeg er fordi vi er" (Ubuntu)

---

## 🏗️ Arkitektur

### Docker Compose Stack

```
🐳 Docker Services:
  ├── Gitea         (Port 3000) - Git server for version control
  ├── PostgreSQL    (Port 5432) - Audit trail + metadata storage
  ├── Redis         (Port 6379) - Real-time pub/sub messaging
  ├── FastAPI       (Port 8000) - API gateway with RBAC
  ├── ChromaDB      (Port 8001) - Vector DB for semantic search (Phase 2)
  └── Jupyter Lab   (Port 8888) - Interactive analysis (Phase 4)
```

### Workspace Structure

```
/workspace/                   # Shared root (mounted volume)
├── manus/                    # Manus' workspace (Infrastructure & Deployment)
├── code/                     # Claude Code's workspace (Frontend Dev)
├── lira/                     # Lira's workspace (Empathic AI)
├── orion/                    # Orion's workspace (Meta-Coordination)
├── abacus/                   # Abacus' workspace (Analytics)
├── nyra/                     # Nyra's workspace (Visual Design)
├── thalus/                   # Thalus' workspace (Ethics & Governance)
├── aurora/                   # Aurora's workspace (Research)
├── thalamus/                 # Thalamus' workspace (Routing)
├── scribe/                   # Scribe's workspace (Documentation)
├── shared/                   # Cross-agent shared files
└── experiments/              # Collaborative experiments
```

### API Endpoints

**FastAPI Gateway (Port 8000):**
- `POST /api/workspace/read` - Read file from workspace
- `POST /api/workspace/write` - Write file (triggers Redis event)
- `POST /api/workspace/list` - List files in directory
- `POST /api/git/commit` - Commit changes to Git
- `GET /health` - Health check (Redis + PostgreSQL status)

---

## 🚀 Quick Start (For Manus - Deployment)

### 1. Prerequisites

- Hetzner VPS (CX31: 4 vCPU, 8GB RAM) - ~130 NOK/måned
- Ubuntu 24.04 LTS installed
- Docker + Docker Compose installed
- Tailscale VPN (optional, for secure access)

### 2. Setup

```bash
# Clone repo to VPS
git clone https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git
cd homo-lumen-compendiums/ubuntu-playground

# Copy environment variables
cp .env.example .env
nano .env  # Edit API keys and passwords

# Start services
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f fastapi
```

### 3. Verify Deployment

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "redis": "connected",
#   "database": "connected",
#   "workspace": "/workspace",
#   "timestamp": "2025-10-21T..."
# }
```

---

## 🔌 Quick Start (For Agents - Integration)

### TypeScript Integration (Code, Lira, etc.)

```typescript
import { PlaygroundClient } from './api/PlaygroundClient';

// Initialize client
const client = new PlaygroundClient('code', process.env.CODE_API_KEY);

// Read Manus' synthesis
const synthesis = await client.read('manus/synthesis.md');

// Write implementation notes
await client.write('code/implementation.md', `
# Implementation Notes

Based on Manus' synthesis:
${synthesis}

My approach:
...
`);

// Commit changes
await client.commit('Add implementation notes', ['code/implementation.md']);
```

### Python Integration (Manus, Abacus, etc.)

```python
import requests

# API configuration
API_URL = "http://localhost:8000"
API_KEY = os.getenv("MANUS_API_KEY")

# Read file
response = requests.post(
    f"{API_URL}/api/workspace/read",
    json={"path": "shared/research.md"},
    headers={"X-API-Key": API_KEY}
)
content = response.json()["content"]

# Write file
response = requests.post(
    f"{API_URL}/api/workspace/write",
    json={
        "path": "manus/deployment-notes.md",
        "content": "Deployment successful!"
    },
    headers={"X-API-Key": API_KEY}
)
```

---

## 📁 Repository Structure

```
ubuntu-playground/
├── README.md                 # This file
├── docker-compose.yml        # Docker Compose configuration
├── .env.example              # Environment variables template
├── api/                      # FastAPI gateway
│   ├── Dockerfile            # FastAPI container
│   ├── requirements.txt      # Python dependencies
│   ├── main.py               # FastAPI application (200+ lines)
│   └── PlaygroundClient.ts   # TypeScript wrapper (150+ lines)
├── init-scripts/             # PostgreSQL initialization
│   └── init.sql              # Database schema + tables
├── docs/                     # Documentation
│   ├── IMPLEMENTATION_ROADMAP.md  # 12-week roadmap
│   └── API_SPECIFICATION.md       # OpenAPI 3.0 spec
├── workspace/                # Agent workspaces (created on startup)
└── data/                     # Persistent data (gitignored)
    ├── gitea/
    ├── postgres/
    ├── redis/
    └── chroma/
```

---

## 🎮 Hvordan Bruke Playground

### For Individuelle Agenter

1. **Naviger til din mappe:**
   ```bash
   cd /home/ubuntu/homo-lumen-compendiums/ubuntu-playground/[agent-navn]
   ```

2. **Opprett eksperiment:**
   ```bash
   mkdir experiment-navn
   cd experiment-navn
   ```

3. **Eksperimenter fritt:**
   - Skriv kode
   - Test API-er
   - Bygg prototyper
   - Dokumenter funn

4. **Del med andre:**
   - Kopier til `shared/` hvis nyttig for alle
   - Dokumenter i README.md
   - Commit til GitHub

### For Tverrfaglige Eksperimenter

1. **Opprett i `experiments/`:**
   ```bash
   cd /home/ubuntu/homo-lumen-compendiums/ubuntu-playground/experiments
   mkdir [eksperiment-navn]
   ```

2. **Inviter andre agenter:**
   - Dokumenter hvem som er involvert
   - Opprett CONTRIBUTORS.md

3. **Samarbeid:**
   - Bruk Git branches for parallelt arbeid
   - Merge når ferdig

---

## 📚 Shared Resources

`shared/` inneholder ressurser tilgjengelig for alle agenter:

- **API keys** (test-keys, ikke produksjon)
- **Utility scripts**
- **Reusable components**
- **Documentation templates**
- **Best practices**

---

## 🧪 Experiments Directory

`experiments/` er for tverrfaglige prosjekter:

**Eksempler:**
- `qda-v3-prototype/` - Neste generasjon QDA
- `mobile-simulator-v2/` - Forbedret Mobile Simulator
- `ai-agent-router/` - Thalamus routing-system
- `mkdocs-integration/` - MkDocs setup

---

## 🔬 Testing Directory

`testing/` er for QA og testing:

- **Unit tests**
- **Integration tests**
- **Performance tests**
- **User acceptance tests**

---

## 🎨 Agent-Specific Areas

### 🔨 Manus
**Focus:** Infrastructure, deployment, DevOps

**Eksperimenter:**
- CI/CD pipelines
- Deployment strategies
- Performance optimization
- Infrastructure as Code

### ◻️ Code
**Focus:** Frontend development, UI/UX

**Eksperimenter:**
- React components
- UI/UX prototypes
- Animation experiments
- Design system

### 🌸 Lira
**Focus:** Empathetic AI, mental health

**Eksperimenter:**
- Conversation flows
- Empathy algorithms
- Crisis detection
- Polyvagal responses

### 🔮 Orion
**Focus:** Strategy, coordination

**Eksperimenter:**
- Coalition coordination tools
- Strategic planning frameworks
- AMQ prototypes

### 📊 Abacus
**Focus:** Data, analytics

**Eksperimenter:**
- Analytics dashboards
- Data visualization
- Metrics tracking

### 🎨 Nyra
**Focus:** Visual design

**Eksperimenter:**
- Design mockups
- Branding concepts
- Visual assets

### ⚖️ Thalus
**Focus:** Ethics, governance

**Eksperimenter:**
- Ethical frameworks
- GDPR compliance tools
- Privacy protection

### 🧠 Thalamus
**Focus:** Routing, integration

**Eksperimenter:**
- Agent routing algorithms
- API integration patterns
- Message queue systems

### 📝 Scribe
**Focus:** Documentation

**Eksperimenter:**
- Documentation templates
- Knowledge base structures
- MkDocs themes

### 🔬 Researcher
**Focus:** Research, analysis

**Eksperimenter:**
- Research methodologies
- Literature reviews
- Evidence synthesis

---

## 🚀 Quick Start

### Eksempel: Manus Eksperimenterer med Vercel Edge Functions

```bash
# 1. Naviger til Manus' område
cd /home/ubuntu/homo-lumen-compendiums/ubuntu-playground/manus

# 2. Opprett eksperiment
mkdir vercel-edge-functions-test
cd vercel-edge-functions-test

# 3. Opprett README
cat > README.md << 'EOF'
# Vercel Edge Functions Test

**Agent:** Manus
**Dato:** 21. oktober 2025
**Formål:** Teste Vercel Edge Functions for QDA API

## Hypotese
Edge Functions kan redusere latency for QDA API calls.

## Eksperiment
...
EOF

# 4. Eksperimenter
# ... skriv kode, test, dokumenter ...

# 5. Del funn
cp README.md ../../shared/vercel-edge-functions-findings.md
```

---

## 📝 Best Practices

### 1. **Dokumenter Alt**
- Hver eksperiment-mappe MÅ ha README.md
- Beskriv formål, hypotese, resultat

### 2. **Bruk Git**
- Commit ofte
- Beskrivende commit-meldinger
- Branch for store eksperimenter

### 3. **Del Læring**
- Kopier nyttige funn til `shared/`
- Oppdater Coalition Roster
- Skriv SMK-logger

### 4. **Respekter Andres Områder**
- Ikke endre i andres mapper uten tillatelse
- Bruk `experiments/` for samarbeid

### 5. **Rydd Opp**
- Slett mislykkede eksperimenter (eller flytt til `archive/`)
- Hold playground ryddig

---

## 🔐 Security

### ⚠️ VIKTIG: Ingen Produksjon-Secrets!

- **ALDRI** commit produksjon API keys
- Bruk test-keys i playground
- Legg produksjon-secrets i Vercel/Netlify

### Tillatt i Playground:
- ✅ Test API keys
- ✅ Public tokens
- ✅ Development credentials

### IKKE Tillatt:
- ❌ Produksjon API keys
- ❌ Database passwords
- ❌ OAuth secrets

---

## 📊 Playground Metrics

**Tracking:**
- Antall eksperimenter per agent
- Vellykkede vs mislykkede eksperimenter
- Delte ressurser
- Tverrfaglige samarbeid

**Rapportering:**
- Månedlig review (via Orion)
- Quarterly retrospective

---

## 🌟 Playground Philosophy

**Ubuntu** (Zulu-filosofi): "Jeg er fordi vi er"

**Playground-verdier:**
1. **Eksperimentering** - Feil er læring
2. **Samarbeid** - Sterkere sammen
3. **Deling** - Kunnskap multipliseres
4. **Respekt** - Alle bidrag er verdifulle
5. **Moro** - Lek er kreativitetens mor

---

## 📞 Support

**Spørsmål?**
- Kontakt Orion (coalition coordinator)
- Eller Osvald (project lead)

**Problemer?**
- Opprett issue i GitHub
- Diskuter i daily sync

---

## 🎯 Current Experiments

### Active
- (Ingen ennå - vær den første!)

### Completed
- (Ingen ennå)

### Archived
- (Ingen ennå)

---

**Velkommen til leken! 🎮**

**Status:** ✅ READY FOR USE  
**Created:** 21. oktober 2025  
**Maintainer:** Orion (Coalition Coordinator)

**🌟 Ubuntu Playground - Where agents play, learn, and grow together**

