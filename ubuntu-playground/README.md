# 🌌 Ubuntu Playground - Coalition Nervous System

**Velkommen til Ubuntu Playground!**

Dette er et **persistent, delt multi-agent eksekveringsmiljø** for Homo Lumen Coalition. Ubuntu Playground gir alle 10 agenter tilgang til samme workspace, persistent minne, og real-time pub/sub kommunikasjon.

**Status:** ✅ Local MVP DEPLOYED (2025-10-28) | 🌐 Cloud Deployment Ready

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

### **DEPLOYMENT OPTIONS**

**Fase 0 (2025-10-28): Local MVP** ✅ DEPLOYED

```
💻 Local Development (SQLite + Python):
  ├── FastAPI Gateway (Port 8002)   - Ubuntu Playground API
  ├── SQLite Database               - Lightweight persistence
  ├── CSN Server (Port 8001)        - 5 LLM agents integration
  └── Local workspace               - File-based collaboration
                                      Total Cost: 0 NOK/mnd

✅ Status: Deployed and tested (5/5 integration tests passed)
📝 See: SMK #033 for Genesis Integration details
🚀 See: DEPLOYMENT_GUIDE_GOOGLE_CLOUD.md for cloud migration
```

**Fase 1 (2025-2026): Hybrid-Løsning** 🌐 READY TO DEPLOY

```
☁️ Google Cloud (Kritiske Tjenester - Managed):
  ├── Cloud SQL (PostgreSQL)     - europe-north1 (Finland) - 150 NOK/mnd
  ├── Memorystore (Redis)        - europe-north1 (Finland) - 100 NOK/mnd
  └── Cloud Run (Gitea)          - europe-north1 (Finland) -  50 NOK/mnd
                                                    Total: ~300 NOK/mnd

🖥️ Hetzner VPS (Agent Execution - Self-hosted):
  ├── FastAPI Gateway (Port 8000) - Agent API access
  ├── ChromaDB (Port 8001)        - Vector DB (Phase 2, optional)
  └── Jupyter Lab (Port 8888)     - Interactive analysis (Phase 4, optional)
                                    CX31 VPS: 80 NOK/mnd + Backups: 16 NOK/mnd
                                                    Total: ~96 NOK/mnd

🔐 Synkronisering:
  └── Tailscale VPN - Secure Google Cloud ↔ Hetzner communication

💰 Total Cost: ~396 NOK/måned (~$40/mnd)
```

**Fase 2 (2027+): Full Hetzner VPS** 🔄 PLANNED

```
🖥️ Hetzner VPS CX42 (All Services - Self-hosted):
  ├── PostgreSQL (Port 5432)     - Migrated from Google Cloud SQL
  ├── Redis (Port 6379)          - Migrated from Google Memorystore
  ├── Gitea (Port 3000)          - Migrated from Google Cloud Run
  ├── FastAPI Gateway (Port 8000)
  ├── ChromaDB (Port 8001)
  └── Jupyter Lab (Port 8888)
                        CX42 VPS: 160 NOK/mnd + Backups: 20 NOK/mnd
                                                Total: ~180 NOK/mnd

💰 Total Cost: ~180 NOK/måned (~$18/mnd)
📉 Savings: 216 NOK/måned = 2,592 NOK/år
```

### Docker Compose Stack (Hetzner VPS)

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

**FastAPI Gateway (Port 8000 on Hetzner VPS):**
- `POST /api/workspace/read` - Read file from workspace
- `POST /api/workspace/write` - Write file (triggers Redis event via Google Memorystore)
- `POST /api/workspace/list` - List files in directory
- `POST /api/git/commit` - Commit changes to Git (via Google Cloud Run Gitea)
- `GET /health` - Health check (Google Cloud SQL + Memorystore status)

---

## 🚀 Quick Start (For Manus - Deployment)

### **PHASE 1A: Google Cloud Setup** (Week 1-2)

#### 1. Create Google Cloud Project

```bash
# Install Google Cloud SDK if needed
# https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Create project
gcloud projects create homo-lumen-ubuntu-playground \
  --organization=cognitivesovereignty.network

# Set as active project
gcloud config set project homo-lumen-ubuntu-playground

# Link billing account
gcloud billing accounts list
gcloud billing projects link homo-lumen-ubuntu-playground \
  --billing-account=<BILLING_ACCOUNT_ID>
```

#### 2. Enable Required APIs

```bash
gcloud services enable sqladmin.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable compute.googleapis.com
```

#### 3. Deploy Cloud SQL (PostgreSQL)

```bash
# Create PostgreSQL instance
gcloud sql instances create homo-lumen-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-north1 \
  --storage-size=10GB \
  --storage-type=SSD \
  --backup \
  --enable-bin-log

# Create database
gcloud sql databases create homo_lumen \
  --instance=homo-lumen-db

# Create user
gcloud sql users create agents \
  --instance=homo-lumen-db \
  --password=<GENERATE_STRONG_PASSWORD>

# Get external IP (for .env file)
gcloud sql instances describe homo-lumen-db \
  --format="get(ipAddresses[0].ipAddress)"
```

#### 4. Deploy Memorystore (Redis)

```bash
# Create Redis instance
gcloud redis instances create homo-lumen-redis \
  --size=1 \
  --region=europe-north1 \
  --redis-version=redis_7_0

# Get internal IP (for .env file)
gcloud redis instances describe homo-lumen-redis \
  --region=europe-north1 \
  --format="get(host)"
```

#### 5. Deploy Gitea on Cloud Run

```bash
# Deploy Gitea container
gcloud run deploy gitea \
  --image=gitea/gitea:latest \
  --platform=managed \
  --region=europe-north1 \
  --allow-unauthenticated \
  --memory=512Mi \
  --set-env-vars=USER_UID=1000,USER_GID=1000

# Get service URL (for .env file)
gcloud run services describe gitea \
  --region=europe-north1 \
  --format="get(status.url)"
```

---

### **PHASE 1B: Hetzner VPS Setup** (Week 3-4)

#### 1. Create Hetzner Account & VPS

1. Go to: https://console.hetzner.cloud
2. Create account using `cognitivesovereignty.network` email
3. Create new project: "homo-lumen-ubuntu-playground"
4. Add Server:
   - **Location:** Falkenstein, Germany
   - **Image:** Ubuntu 24.04 LTS
   - **Type:** CX31 (2 vCPU, 8GB RAM)
   - **Networking:** IPv4 + IPv6
   - **SSH Key:** Add your public key
   - **Backups:** Enable (20%)
5. Create & Buy (~80 NOK/måned)

#### 2. Initial Security Setup

```bash
# SSH into server
ssh root@<HETZNER_VPS_IP>

# Update system
apt update && apt upgrade -y

# Create non-root user
adduser ubuntu
usermod -aG sudo ubuntu

# Configure SSH (disable root login)
nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
systemctl restart sshd

# Setup firewall
apt install ufw -y
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 8000/tcp # FastAPI
ufw enable

# Install fail2ban (brute-force protection)
apt install fail2ban -y
systemctl enable fail2ban
```

#### 3. Install Docker & Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add ubuntu to docker group
usermod -aG docker ubuntu

# Install Docker Compose
apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

#### 4. Install Tailscale VPN

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Start Tailscale
tailscale up

# Get Tailscale IP (for Google Cloud authorized networks)
tailscale ip -4
```

#### 5. Clone GitHub Repository

```bash
# Switch to ubuntu user
su - ubuntu

# Generate SSH key
ssh-keygen -t ed25519 -C "ubuntu-playground@cognitivesovereignty.network"

# Add SSH key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and add to: https://github.com/settings/keys

# Clone repository
git clone git@github.com:noonaut-homo-lumen-resonans/homo-lumen-compendiums.git
cd homo-lumen-compendiums/ubuntu-playground
```

#### 6. Configure Environment Variables

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with actual values from Google Cloud
nano .env

# Fill in:
# - GOOGLE_CLOUD_SQL_IP (from Phase 1A step 3)
# - POSTGRES_PASSWORD (from Phase 1A step 3)
# - GOOGLE_MEMORYSTORE_IP (from Phase 1A step 4)
# - GOOGLE_GITEA_URL (from Phase 1A step 5)
# - All agent API keys (generate with: openssl rand -hex 32)
```

#### 7. Deploy FastAPI Gateway

```bash
# Start Docker Compose (FastAPI only, no optional services)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f fastapi
```

---

### **PHASE 1C: Connect Google Cloud ↔ Hetzner** (Week 5-6)

#### 1. Authorize Hetzner VPS in Cloud SQL

```bash
# On your local machine (not VPS)
# Add Hetzner Tailscale IP to Cloud SQL authorized networks
gcloud sql instances patch homo-lumen-db \
  --authorized-networks=<HETZNER_TAILSCALE_IP>
```

#### 2. Test PostgreSQL Connection

```bash
# On Hetzner VPS
apt install postgresql-client -y

# Test connection to Google Cloud SQL
psql -h <GOOGLE_CLOUD_SQL_IP> -U agents -d homo_lumen

# If successful, you'll see PostgreSQL prompt
# Type \q to quit
```

#### 3. Test Redis Connection

```bash
# On Hetzner VPS
apt install redis-tools -y

# Test connection to Google Memorystore
redis-cli -h <GOOGLE_MEMORYSTORE_IP> ping

# Should return: PONG
```

#### 4. Test Gitea Connection

```bash
# On Hetzner VPS
curl https://<GITEA_CLOUD_RUN_URL>

# Should return HTML response from Gitea
```

#### 5. Verify FastAPI Health

```bash
# Test FastAPI health endpoint
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

