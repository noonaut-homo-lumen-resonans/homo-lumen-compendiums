# API Keys Setup Guide
**For:** Vertex AI, Vercel, ElevenLabs
**Dato:** 30. oktober 2025

---

## Oversikt

Denne guiden hjelper deg med å få API-nøkler for:
1. **Vertex AI (Google Cloud)** - Multi-modal LLM
2. **Vercel** - Deployment platform
3. **ElevenLabs** - Text-to-Speech (Lira voice!)

**Estimert tid:** 30-45 minutter totalt

---

## 1. Vertex AI (Google Cloud) Setup

### Steg 1.1: Opprett Google Cloud Project

1. Gå til: https://console.cloud.google.com
2. Logg inn med din Google-konto
3. Klikk på prosjekt-dropdown (øverst til venstre)
4. Klikk **"NEW PROJECT"**
5. Fyll inn:
   - **Project name:** `homo-lumen-project`
   - **Organization:** (valgfritt)
6. Klikk **"CREATE"**

---

### Steg 1.2: Aktiver Vertex AI API

1. Gå til: https://console.cloud.google.com/apis/library
2. Søk etter **"Vertex AI API"**
3. Klikk på **"Vertex AI API"**
4. Klikk **"ENABLE"**
5. Vent 1-2 minutter mens API-en aktiveres

**Andre APIer som bør aktiveres:**
- **Generative Language API** (for Gemini)
- **Cloud Storage API** (for fillagring)
- **Cloud Functions API** (hvis du vil bruke cloud functions)

---

### Steg 1.3: Opprett Service Account

1. Gå til: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Klikk **"+ CREATE SERVICE ACCOUNT"**
3. Fyll inn:
   - **Service account name:** `homo-lumen-agent`
   - **Service account ID:** (auto-generert)
   - **Description:** `Service account for Homo Lumen agents`
4. Klikk **"CREATE AND CONTINUE"**

---

### Steg 1.4: Gi Service Account Roller

1. I "Grant this service account access to project" seksjonen:
2. Klikk **"Select a role"** dropdown
3. Søk etter og velg følgende roller:
   - **Vertex AI User** (for å bruke Vertex AI)
   - **AI Platform Developer** (for å deploye modeller)
   - **Storage Object Viewer** (for å lese filer)
4. Klikk **"CONTINUE"**
5. Klikk **"DONE"**

---

### Steg 1.5: Last ned Service Account Key (JSON)

1. Finn din service account i listen
2. Klikk på de 3 prikkene (⋮) til høyre
3. Velg **"Manage keys"**
4. Klikk **"ADD KEY"** → **"Create new key"**
5. Velg **"JSON"**
6. Klikk **"CREATE"**
7. En JSON-fil lastes ned automatisk

**VIKTIG:**
- Lagre denne filen et sikkert sted!
- Ikke commit til Git!
- Flytt filen til: `c:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\ubuntu-playground\credentials\`

**Eksempel filnavn:**
```
homo-lumen-project-1234567890ab.json
```

---

### Steg 1.6: Sett opp miljøvariabler

Legg til i `.env` (i `ubuntu-playground/api/.env`):

```bash
# Vertex AI Configuration
GOOGLE_CLOUD_PROJECT=homo-lumen-project
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=../credentials/homo-lumen-project-1234567890ab.json
```

---

### Steg 1.7: Test Vertex AI (valgfritt nå, testes senere)

```python
from google.cloud import aiplatform

aiplatform.init(
    project="homo-lumen-project",
    location="us-central1"
)

# Test successful!
```

---

## 2. Vercel API Token Setup

### Steg 2.1: Logg inn på Vercel

1. Gå til: https://vercel.com
2. Logg inn med GitHub, GitLab eller e-post

---

### Steg 2.2: Opprett API Token

1. Klikk på profil-bildet (øverst til høyre)
2. Velg **"Settings"**
3. I venstre sidebar, klikk **"Tokens"**
4. Klikk **"Create"** (eller "Create Token")
5. Fyll inn:
   - **Token Name:** `Homo Lumen Playground`
   - **Scope:** Select **"Full Account"** (eller velg spesifikke prosjekter)
   - **Expiration:** Velg **"No Expiration"** (eller 1 år)
6. Klikk **"CREATE TOKEN"**

---

### Steg 2.3: Kopier token

**VIKTIG:**
- Tokenet vises KUN én gang!
- Kopier det NÅ og lagre et sikkert sted
- Tokenet ser slik ut: `vercel_1a2b3c4d5e6f7g8h9i0j`

---

### Steg 2.4: Finn Team ID (valgfritt)

Hvis du har et Vercel team:
1. Gå til team settings: https://vercel.com/teams/[your-team]/settings
2. Se på URL-en, team ID er i URLen
3. Eller finn det i **"General"** settings

---

### Steg 2.5: Finn prosjekt-ID for NAV-Losen

1. Gå til ditt NAV-Losen prosjekt på Vercel
2. Klikk **"Settings"**
3. Se på **"Project ID"** (under General)
4. Kopier ID-en (f.eks. `prj_abc123xyz`)

---

### Steg 2.6: Legg til miljøvariabler

Legg til i `.env`:

```bash
# Vercel Configuration
VERCEL_TOKEN=vercel_1a2b3c4d5e6f7g8h9i0j
VERCEL_TEAM_ID=team_abc123xyz  # Valgfritt
VERCEL_PROJECT_ID=prj_abc123xyz  # NAV-Losen project
```

---

## 3. ElevenLabs API Key Setup

### Steg 3.1: Opprett ElevenLabs konto

1. Gå til: https://elevenlabs.io
2. Klikk **"Get Started Free"**
3. Registrer med e-post eller Google
4. Bekreft e-post

---

### Steg 3.2: Velg plan

**Gratis plan:**
- 10,000 characters per måned
- Nok for testing

**Starter plan ($5/mnd):**
- 30,000 characters per måned
- Bedre stemmer

**Creator plan ($22/mnd):**
- 100,000 characters per måned
- Voice cloning

**Anbefaling:** Start med gratis, oppgrader hvis du trenger mer

---

### Steg 3.3: Få API Key

1. Logg inn på https://elevenlabs.io
2. Klikk på profil-bildet (øverst til høyre)
3. Velg **"Profile"**
4. Scroll ned til **"API Key"** seksjonen
5. Klikk **"Copy"** for å kopiere API-nøkkelen
6. API key ser slik ut: `sk_abc123def456ghi789jkl`

---

### Steg 3.4: Velg Lira sin stemme

1. Gå til: https://elevenlabs.io/voice-library
2. Søk etter stemmer som passer Lira:
   - **Rachel** (Calm, empathetic, professional) - Anbefalt!
   - **Bella** (Soft, warm, friendly)
   - **Domi** (Strong, confident, clear)
3. Klikk **"Preview"** for å høre stemmen
4. Når du finner riktig stemme:
   - Klikk på stemmen
   - Kopier **"Voice ID"** (f.eks. `21m00Tcm4TlvDq8ikWAM`)

**Lira anbefalt stemme:**
- **Name:** Rachel
- **Voice ID:** `21m00Tcm4TlvDq8ikWAM`
- **Description:** American, young adult, calm
- **Use cases:** Conversational, narrative, friendly

---

### Steg 3.5: Test stemmen (valgfritt)

1. På ElevenLabs dashboard: https://elevenlabs.io/speech-synthesis
2. Velg **Rachel** stemme
3. Skriv inn norsk tekst:
   ```
   Hei, jeg er Lira. Jeg er her for å hjelpe deg med å finne din neste jobb.
   ```
4. Klikk **"Generate"**
5. Lytt til resultatet
6. Juster **Stability** og **Clarity** hvis nødvendig

**Anbefalte innstillinger for Lira:**
- **Stability:** 0.75 (balansert)
- **Similarity Boost:** 0.75 (høy likhet)
- **Style Exaggeration:** 0.5 (naturlig)

---

### Steg 3.6: Legg til miljøvariabler

Legg til i `.env`:

```bash
# ElevenLabs Configuration
ELEVENLABS_API_KEY=sk_abc123def456ghi789jkl
ELEVENLABS_VOICE_ID_LIRA=21m00Tcm4TlvDq8ikWAM  # Rachel voice

# Voice settings for Lira
ELEVENLABS_STABILITY=0.75
ELEVENLABS_SIMILARITY_BOOST=0.75
ELEVENLABS_STYLE=0.5
```

---

## 4. Oppsummering av API Keys

Etter å ha fullført alle steg, skal du ha:

### Vertex AI:
- ✅ Google Cloud project: `homo-lumen-project`
- ✅ Service account JSON file: `homo-lumen-project-1234567890ab.json`
- ✅ Vertex AI API aktivert

### Vercel:
- ✅ API Token: `vercel_1a2b3c4d5e6f7g8h9i0j`
- ✅ Project ID: `prj_abc123xyz`

### ElevenLabs:
- ✅ API Key: `sk_abc123def456ghi789jkl`
- ✅ Voice ID for Lira: `21m00Tcm4TlvDq8ikWAM`

---

## 5. Fullstendig .env-fil

```bash
# ===========================================
# VERTEX AI (Google Cloud)
# ===========================================
GOOGLE_CLOUD_PROJECT=homo-lumen-project
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=../credentials/homo-lumen-project-1234567890ab.json

# ===========================================
# VERCEL
# ===========================================
VERCEL_TOKEN=vercel_1a2b3c4d5e6f7g8h9i0j
VERCEL_TEAM_ID=team_abc123xyz  # Valgfritt
VERCEL_PROJECT_ID=prj_abc123xyz  # NAV-Losen

# ===========================================
# ELEVENLABS (Lira Voice)
# ===========================================
ELEVENLABS_API_KEY=sk_abc123def456ghi789jkl
ELEVENLABS_VOICE_ID_LIRA=21m00Tcm4TlvDq8ikWAM

# Voice settings
ELEVENLABS_STABILITY=0.75
ELEVENLABS_SIMILARITY_BOOST=0.75
ELEVENLABS_STYLE=0.5

# ===========================================
# EXISTING KEYS (fra tidligere)
# ===========================================
OPENAI_API_KEY=sk-proj-your-openai-key-here
GEMINI_API_KEY=your-gemini-api-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key-here
```

---

## 6. Sikkerhet

### VIKTIG: Ikke commit API keys til Git!

Legg til i `.gitignore`:

```bash
# API Keys and Secrets
.env
.env.local
credentials/
*.json  # Service account keys
```

### Lagring av API keys:

1. **Lokal utvikling:**
   - Lagre i `.env` fil
   - Aldri commit til Git

2. **Produksjon:**
   - Bruk miljøvariabler på server
   - Vercel: Project Settings → Environment Variables
   - Google Cloud: Secret Manager

---

## 7. Testing API Keys

### Test Vertex AI:
```bash
# Install Google Cloud SDK
pip install google-cloud-aiplatform

# Test
python -c "from google.cloud import aiplatform; aiplatform.init(project='homo-lumen-project', location='us-central1'); print('✅ Vertex AI OK')"
```

### Test Vercel:
```bash
curl -H "Authorization: Bearer vercel_1a2b3c4d5e6f7g8h9i0j" \
  https://api.vercel.com/v9/projects

# Skal returnere liste over prosjekter
```

### Test ElevenLabs:
```bash
curl -X GET https://api.elevenlabs.io/v1/voices \
  -H "xi-api-key: sk_abc123def456ghi789jkl"

# Skal returnere liste over stemmer
```

---

## 8. Kostnader

### Vertex AI (Google Cloud):
- **Gratis tier:** $300 credits (første 90 dager)
- **Gemini Pro:** $0.00025/1K characters (tekst)
- **Gemini Pro Vision:** $0.0025/image
- **Estimert kostnad:** $20-50/mnd (etter gratis periode)

### Vercel:
- **Hobby plan:** Gratis
  - 100 GB bandwidth
  - 100 deployments per dag
- **Pro plan:** $20/mnd
  - Unlimited deployments
  - Analytics
- **Estimert kostnad:** $0-20/mnd

### ElevenLabs:
- **Free:** 10,000 characters/mnd (gratis)
- **Starter:** $5/mnd (30,000 characters)
- **Creator:** $22/mnd (100,000 characters)
- **Estimert kostnad:** $5-15/mnd

**Total estimert kostnad:** $25-85/mnd

**Tips for å spare penger:**
- Start med gratis tiers
- Bruk caching for å redusere API-kall
- Overvåk usage dashboards

---

## 9. Feilsøking

### Problem 1: "Permission denied" i Vertex AI

**Løsning:**
- Sjekk at service account har riktige roller
- Verifiser at Vertex AI API er aktivert
- Sjekk at GOOGLE_APPLICATION_CREDENTIALS peker til riktig fil

### Problem 2: Vercel token fungerer ikke

**Løsning:**
- Sjekk at token ikke har utløpt
- Verifiser at token har riktig scope
- Test med curl kommando ovenfor

### Problem 3: ElevenLabs gir 401 Unauthorized

**Løsning:**
- Sjekk at API key er riktig kopiert (ingen mellomrom)
- Verifiser at API key ikke er revoked
- Sjekk at du har active subscription

---

## 10. Neste Steg

Etter at du har fått alle API-nøklene:

1. ✅ Legg til alle keys i `.env` fil
2. ✅ Test hver API med curl/Python kommandoer ovenfor
3. ✅ Gå videre til implementering av connectors (jeg implementerer dette)

---

## Ressurser

### Dokumentasjon:
- **Vertex AI:** https://cloud.google.com/vertex-ai/docs
- **Vercel API:** https://vercel.com/docs/rest-api
- **ElevenLabs API:** https://elevenlabs.io/docs/api-reference

### Support:
- **Google Cloud Support:** https://cloud.google.com/support
- **Vercel Support:** support@vercel.com
- **ElevenLabs Support:** support@elevenlabs.io

---

**Lykke til med setup!** 🚀

Når du har fått alle API-nøklene, si fra så implementerer jeg alle connectors!
