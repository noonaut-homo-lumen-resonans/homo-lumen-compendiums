# MCP Integration Plan for Homo Lumen Playground
**Opprettet:** 30. oktober 2025

---

## Oversikt

MCP (Model Context Protocol) lar agentene få tilgang til eksterne verktøy og tjenester.
Ved å koble flere integrasjoner får agentene mer kraft og kan utføre flere oppgaver autonomt.

---

## Nåværende Status

### ✅ Allerede Integrert (fra tidligere sesjon)
1. **Google Workspace** - Docs, Sheets, Drive
2. **Notion** - Knowledge base og dokumentasjon
3. **Linear** - Task tracking
4. **GitHub** - Repository management
5. **Cursor** - Code editor integration
6. **Perplexity** - Web search
7. **Slack** - Team communication (avhengig av config)
8. **ClickUp** - Project management (avhengig av config)
9. **Supabase** - Database (nå lagt til)
10. **Upstash** - Redis/KV storage (nevnt tidligere)
11. **Netlify** - Deployment (nevnt tidligere)

---

## Nye Verktøy å Integrere

### Prioritet 1 (Høy verdi - implementer nå)

#### 1. **Vertex AI (Google Cloud)** ⭐⭐⭐⭐⭐
**Hvorfor:**
- Du har allerede Gemini API-nøkkel
- Gir tilgang til flere LLM-modeller (Gemini Pro, Gemini Flash, etc.)
- Bedre for produksjon enn bare OpenAI
- Multimodal AI (tekst, bilder, video)

**Bruksområder:**
- Lira kan bruke Vertex AI for variasjon
- Bildeanalyse for CV-scanning
- Audiotranskribering for intervjuer

**MCP Server:** `@modelcontextprotocol/server-google-vertex-ai`

**Setup:**
```bash
# Install MCP server
npm install -g @modelcontextprotocol/server-google-vertex-ai

# Add to playground config
{
  "mcpServers": {
    "vertex-ai": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-vertex-ai"],
      "env": {
        "GOOGLE_CLOUD_PROJECT": "homo-lumen-project",
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json"
      }
    }
  }
}
```

---

#### 2. **Vercel** ⭐⭐⭐⭐⭐
**Hvorfor:**
- Du bruker Next.js (NAV-Losen frontend)
- Auto-deploy og hosting
- Edge functions for global performance
- Analytics og monitoring

**Bruksområder:**
- Agenter kan deploye nye features automatisk
- Overvåke deployment-status
- Hente analytics-data
- Administrere environment variables

**API:** Vercel REST API
**Docs:** https://vercel.com/docs/rest-api

**Setup:**
```typescript
// playground/connectors/vercel_connector.py
import os
import requests

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")

async def deploy_project(project_id: str):
    """Deploy a project to Vercel"""
    response = requests.post(
        f"https://api.vercel.com/v13/deployments",
        headers={"Authorization": f"Bearer {VERCEL_TOKEN}"},
        json={"project": project_id}
    )
    return response.json()

async def get_deployments(project_id: str):
    """Get all deployments for a project"""
    response = requests.get(
        f"https://api.vercel.com/v6/deployments?projectId={project_id}",
        headers={"Authorization": f"Bearer {VERCEL_TOKEN}"}
    )
    return response.json()
```

---

#### 3. **ElevenLabs** ⭐⭐⭐⭐
**Hvorfor:**
- Beste TTS (Text-to-Speech) API
- Lira kan snakke til brukere (voice mode)
- Audioguides for NAV-brukere
- Tilgjengelighetsfunksjoner

**Bruksområder:**
- Lira voice chatbot
- Audio-versjoner av CV-tips
- Lydguide for jobbsøking
- Tilgjengelighetsfunksjoner for synshemmede

**API:** ElevenLabs API
**Docs:** https://elevenlabs.io/docs/api-reference

**Setup:**
```python
# playground/connectors/elevenlabs_connector.py
import os
import requests

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

async def text_to_speech(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
    """Convert text to speech using ElevenLabs"""
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "model_id": "eleven_monolingual_v1"
        }
    )
    return response.content  # Audio bytes
```

**Lira Voice Profile:**
- Voice ID: "Rachel" (calm, empathetic, Norwegian-compatible)
- Settings: Stability=0.75, Similarity=0.75, Style=0.5

---

### Prioritet 2 (Medium verdi - implementer senere)

#### 4. **GitLab** ⭐⭐⭐
**Hvorfor:**
- Alternativ til GitHub
- CI/CD pipelines
- Issue tracking

**Bruksområder:**
- Backup repository
- CI/CD for testing
- Mirror av GitHub-repos

**API:** GitLab REST API
**MCP Server:** Kan bruke samme approach som GitHub

---

#### 5. **Asana** ⭐⭐⭐
**Hvorfor:**
- Project management (alternativ til Linear/ClickUp)
- Gantt charts og timelines
- Bedre for ikke-tech teams

**Bruksområder:**
- Prosjektplanlegging for NAV-Losen
- Task tracking for forretningsside
- Integrering med teamwork

**API:** Asana REST API
**Docs:** https://developers.asana.com/docs

---

#### 6. **Mermaid Chart** ⭐⭐⭐
**Hvorfor:**
- Visualisering av arkitektur
- Diagrammer for dokumentasjon
- Flytskjemaer for prosesser

**Bruksområder:**
- Automatisk generering av arkitektur-diagrammer
- Visualisering av agent-koalisjoner
- Dokumentasjon av dataflyt

**API:** Mermaid.js (frontend library, ikke MCP-server nødvendig)
**Alternative:** Kan bruke Mermaid Live Editor API

---

### Prioritet 3 (Lav prioritet - vurder senere)

#### 7. **Upstash Redis** ⭐⭐
**Allerede nevnt, men ikke satt opp**

**Hvorfor:**
- Serverless Redis
- Caching for API-kall
- Rate limiting
- Session storage

**Bruksområder:**
- Cache jobbsøk-resultater
- Rate limiting for Lira API
- Lagre bruker-sesjoner

---

## Anbefalt Implementeringsrekkefølge

### Uke 1 (Høyeste prioritet):
1. ✅ **Vertex AI** - Gi agentene tilgang til flere LLM-modeller
2. ✅ **Vercel** - Automasjon av deployment for NAV-Losen
3. ✅ **ElevenLabs** - Lira voice chatbot

### Uke 2-3 (Medium prioritet):
4. ⏳ **GitLab** - Backup og CI/CD
5. ⏳ **Asana** - Prosjektstyring for ikke-tech team
6. ⏳ **Upstash Redis** - Caching og performance

### Uke 4+ (Lav prioritet):
7. ⏳ **Mermaid Chart** - Visualisering (kan brukes uten MCP)

---

## Arkitektur-diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Homo Lumen Playground                     │
│                  (Multi-Agent Orchestrator)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌────────┐      ┌────────┐      ┌────────┐
   │  Lira  │      │  Nyra  │      │ Thalus │
   │(Gemini)│      │(Claude)│      │(OpenAI)│
   └────┬───┘      └────┬───┘      └────┬───┘
        │               │                │
        │               │                │
        └───────────────┼────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │       MCP Connectors Layer        │
        ├───────────────────────────────────┤
        │ • Google Workspace (Docs, Sheets) │
        │ • Notion (Knowledge Base)         │
        │ • Linear (Task Tracking)          │
        │ • GitHub (Code Repository)        │
        │ • Supabase (Database)             │
        │ • Slack (Communication)           │
        │ ────────────────────────────────  │
        │ NEW:                              │
        │ • Vertex AI (Multi-modal LLM)     │
        │ • Vercel (Deployment)             │
        │ • ElevenLabs (Voice/TTS)          │
        │ • GitLab (CI/CD)                  │
        │ • Asana (Project Management)      │
        │ • Upstash (Redis Caching)         │
        └───────────────────────────────────┘
```

---

## Implementeringsdetaljer

### 1. Vertex AI Integration

**Fil:** `ubuntu-playground/api/connectors/vertex_ai_connector.py`

```python
from google.cloud import aiplatform
from google.oauth2 import service_account
import os

class VertexAIConnector:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        # Initialize Vertex AI
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        aiplatform.init(
            project=self.project_id,
            location=self.location,
            credentials=credentials
        )

    async def generate_text(self, prompt: str, model: str = "gemini-pro"):
        """Generate text using Vertex AI"""
        from vertexai.preview.generative_models import GenerativeModel

        model = GenerativeModel(model)
        response = await model.generate_content_async(prompt)
        return response.text

    async def generate_image_description(self, image_bytes: bytes):
        """Analyze image using Gemini Pro Vision"""
        from vertexai.preview.generative_models import GenerativeModel, Part

        model = GenerativeModel("gemini-pro-vision")
        image_part = Part.from_data(image_bytes, mime_type="image/jpeg")

        response = await model.generate_content_async([
            image_part,
            "Describe this image in detail"
        ])
        return response.text
```

**Environment variables:**
```bash
GOOGLE_CLOUD_PROJECT=homo-lumen-project
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

---

### 2. Vercel Integration

**Fil:** `ubuntu-playground/api/connectors/vercel_connector.py`

```python
import os
import aiohttp

class VercelConnector:
    def __init__(self):
        self.token = os.getenv("VERCEL_TOKEN")
        self.team_id = os.getenv("VERCEL_TEAM_ID")
        self.base_url = "https://api.vercel.com"

    async def deploy_project(self, project_name: str, git_ref: str = "main"):
        """Trigger deployment for a project"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/v13/deployments",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json={
                    "name": project_name,
                    "gitSource": {
                        "type": "github",
                        "ref": git_ref
                    }
                }
            ) as response:
                return await response.json()

    async def get_deployment_status(self, deployment_id: str):
        """Check deployment status"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/v13/deployments/{deployment_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            ) as response:
                return await response.json()

    async def list_projects(self):
        """List all Vercel projects"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/v9/projects",
                headers={"Authorization": f"Bearer {self.token}"}
            ) as response:
                return await response.json()
```

**Environment variables:**
```bash
VERCEL_TOKEN=your_vercel_token
VERCEL_TEAM_ID=your_team_id  # Optional
```

---

### 3. ElevenLabs Integration

**Fil:** `ubuntu-playground/api/connectors/elevenlabs_connector.py`

```python
import os
import aiohttp

class ElevenLabsConnector:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"

        # Lira's voice profile
        self.lira_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel

    async def text_to_speech(
        self,
        text: str,
        voice_id: str = None,
        stability: float = 0.75,
        similarity_boost: float = 0.75
    ):
        """Convert text to speech"""
        voice_id = voice_id or self.lira_voice_id

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": stability,
                        "similarity_boost": similarity_boost
                    }
                }
            ) as response:
                return await response.read()  # Audio bytes

    async def list_voices(self):
        """Get available voices"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/voices",
                headers={"xi-api-key": self.api_key}
            ) as response:
                return await response.json()
```

**Environment variables:**
```bash
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

**Lira Voice Endpoint:**
```python
# In main.py
@app.post("/api/lira/voice")
async def lira_speak(text: str):
    """Lira speaks using ElevenLabs"""
    connector = ElevenLabsConnector()
    audio_bytes = await connector.text_to_speech(text)

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "attachment; filename=lira_voice.mp3"
        }
    )
```

---

## Testing

### Test Vertex AI:
```python
from connectors.vertex_ai_connector import VertexAIConnector

connector = VertexAIConnector()
response = await connector.generate_text("Hva er kvantemekanikk?")
print(response)
```

### Test Vercel:
```python
from connectors.vercel_connector import VercelConnector

connector = VercelConnector()
deployments = await connector.list_projects()
print(deployments)
```

### Test ElevenLabs:
```python
from connectors.elevenlabs_connector import ElevenLabsConnector

connector = ElevenLabsConnector()
audio = await connector.text_to_speech("Hei, jeg er Lira!")

with open("lira_voice.mp3", "wb") as f:
    f.write(audio)
```

---

## Kostnader (anslag per måned)

| Tjeneste | Gratis Tier | Betalt Plan | Estimert kostnad |
|----------|-------------|-------------|------------------|
| Vertex AI | $300 credits (første 90 dager) | Pay-as-you-go | $20-50/mnd |
| Vercel | Hobby (gratis) | Pro ($20/mnd) | $0-20/mnd |
| ElevenLabs | 10k characters/mnd | Starter ($5/mnd) | $5-15/mnd |
| GitLab | Free tier | Premium ($19/user/mnd) | $0/mnd |
| Asana | Basic (gratis) | Premium ($10.99/user/mnd) | $0-11/mnd |
| Upstash | 10k commands/dag | Pay-as-you-go | $0-5/mnd |
| **Total** | - | - | **$25-101/mnd** |

**Anbefaling:** Start med gratis tiers, oppgrader etter behov.

---

## Neste Steg

1. **Prioriter 3 integrasjoner:**
   - [ ] Vertex AI (høyest prioritet)
   - [ ] Vercel (deployment automation)
   - [ ] ElevenLabs (Lira voice)

2. **Få API-nøkler:**
   - [ ] Google Cloud Console → Vertex AI API
   - [ ] Vercel Dashboard → Settings → Tokens
   - [ ] ElevenLabs Dashboard → Profile → API Key

3. **Implementer connectors:**
   - [ ] Opprett `connectors/vertex_ai_connector.py`
   - [ ] Opprett `connectors/vercel_connector.py`
   - [ ] Opprett `connectors/elevenlabs_connector.py`

4. **Legg til environment variables i `.env`**

5. **Test hver connector enkeltvis**

6. **Integrer med orchestrator** (`main.py`)

---

**Vil du at jeg skal starte implementeringen av Vertex AI, Vercel eller ElevenLabs først?** 🚀

Eller skal jeg hjelpe deg med å få API-nøklene først?
