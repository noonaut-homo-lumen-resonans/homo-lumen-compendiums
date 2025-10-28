# 🔑 API Keys Configuration Guide

## Oversikt

Denne guiden viser deg nøyaktig hvor du skal legge inn alle API-nøklene for Homo Lumen Agent Coalition.

---

## 📁 Fil-Lokasjon

**Alle API-nøkler legges i:**
```
ama-backend/.env
```

---

## 🤖 LLM Agent API Keys (Obligatorisk)

### 1. Perplexity (Aurora) - Research Intelligence

**Hvor får du nøkkelen:**
1. Gå til: https://www.perplexity.ai/settings/api
2. Log inn med din konto
3. Klikk "Generate New API Key"
4. Kopier nøkkelen (starter med `pplx-`)

**Hvor legger du den inn:**
```bash
# I ama-backend/.env, linje 34:
PERPLEXITY_API_KEY=pplx-<din-nøkkel-her>
```

---

### 2. Google AI (Nyra) - Visual Intelligence

**Hvor får du nøkkelen:**
1. Gå til: https://makersuite.google.com/app/apikey
2. Klikk "Create API Key"
3. Kopier nøkkelen (starter med `AIza`)

**Hvor legger du den inn:**
```bash
# I ama-backend/.env, linje 20:
GOOGLE_AI_API_KEY=AIza<din-nøkkel-her>
```

---

### 3. OpenAI (Lira) - Empathy & Biofelt

**Hvor får du nøkkelen:**
1. Gå til: https://platform.openai.com/api-keys
2. Klikk "Create new secret key"
3. Kopier nøkkelen (starter med `sk-proj-`)

**Hvor legger du den inn:**
```bash
# I ama-backend/.env, linje 17:
OPENAI_API_KEY=sk-proj-<din-nøkkel-her>
```

---

### 4. Anthropic (Orion) - Strategic Coordination

**Hvor får du nøkkelen:**
1. Gå til: https://console.anthropic.com/settings/keys
2. Klikk "Create Key"
3. Kopier nøkkelen (starter med `sk-ant-`)

**Hvor legger du den inn:**
```bash
# I ama-backend/.env, linje 23:
ANTHROPIC_API_KEY=sk-ant-<din-nøkkel-her>
```

---

### 5. X.AI (Thalus) - Philosophical Wisdom

**Hvor får du nøkkelen:**
1. Gå til: https://x.ai/api
2. Klikk "Get API Key"
3. Kopier nøkkelen (starter med `xai-`)

**Hvor legger du den inn:**
```bash
# I ama-backend/.env, linje 27:
XAI_API_KEY=xai-<din-nøkkel-her>
```

---

### 6. DeepSeek (Zara) - Creative Innovation

**Hvor får du nøkkelen:**
1. Gå til: https://platform.deepseek.com/api_keys
2. Klikk "Create API Key"
3. Kopier nøkkelen (starter med `sk-`)

**Hvor legger du den inn:**
```bash
# I ama-backend/.env, linje 30:
DEEPSEEK_API_KEY=sk-<din-nøkkel-her>
```

---

## ☁️ External Services (Valgfritt)

### Redis (Upstash Cloud) - Real-Time Events

**Hvor får du nøklene:**
1. Gå til: https://upstash.com
2. Klikk "Sign Up" (gratis tier: 10,000 commands/dag)
3. Klikk "Create Database"
   - Name: `homo-lumen-csn`
   - Region: **Europe** (velg nærmeste Norge, f.eks. Frankfurt eller Stockholm)
   - Type: **Global** (for low latency)
4. Når databasen er opprettet, kopier:
   - `UPSTASH_REDIS_REST_URL` (f.eks. `https://eu1-...upstash.io`)
   - `UPSTASH_REDIS_REST_TOKEN` (lang string)

**Hvor legger du dem inn:**
```bash
# I ama-backend/.env, linje 42-43:
REDIS_URL=https://eu1-<din-database-id>.upstash.io
REDIS_TOKEN=<din-token-her>
```

---

### Linear - Project Management (Valgfritt)

**Hvor får du nøkkelen:**
1. Gå til: https://linear.app/settings/api
2. Klikk "Create Personal API Key"
3. Gi den et navn (f.eks. "Homo Lumen Integration")
4. Kopier nøkkelen (starter med `lin_api_`)

**Hvor legger du den inn:**
```bash
# I ama-backend/.env, linje 47:
LINEAR_API_KEY=lin_api_<din-nøkkel-her>
```

---

### Supabase - Database & Auth (Valgfritt)

**Hvor får du nøklene:**
1. Gå til: https://supabase.com
2. Log inn og opprett et nytt prosjekt
3. Gå til **Settings** → **API**
4. Kopier:
   - **Project URL** (f.eks. `https://abcdefgh.supabase.co`)
   - **anon/public** key (lang string som starter med `eyJ...`)

**Hvor legger du dem inn:**
```bash
# I ama-backend/.env, linje 51-52:
SUPABASE_URL=https://<ditt-prosjekt-id>.supabase.co
SUPABASE_KEY=eyJ<din-nøkkel-her>
```

---

## 🧪 Testing API Keys

### Test All LLM Agents

```bash
cd ama-backend
python -m uvicorn minimal_server:app --host 0.0.0.0 --port 8001 --reload
```

Se på console output - den viser hvilke API keys som er konfigurert:
```
✅ PERPLEXITY_API_KEY found: pplx-a...2345
✅ GOOGLE_AI_API_KEY found: AIza...Cgc
✅ OPENAI_API_KEY found: sk-p...hKMA
✅ ANTHROPIC_API_KEY found: sk-a...pQAA
✅ XAI_API_KEY found: xai-...s1l
✅ DEEPSEEK_API_KEY found: sk-6...2ee
```

---

## 📊 Status Oversikt

| Service | Obligatorisk | Fil |
|---------|--------------|-----|
| **Perplexity** | ✅ Ja | `ama-backend/.env` linje 34 |
| **Google AI** | ✅ Ja | `ama-backend/.env` linje 20 |
| **OpenAI** | ✅ Ja | `ama-backend/.env` linje 17 |
| **Anthropic** | ✅ Ja | `ama-backend/.env` linje 23 |
| **X.AI** | ✅ Ja | `ama-backend/.env` linje 27 |
| **DeepSeek** | ✅ Ja | `ama-backend/.env` linje 30 |
| **Redis (Upstash)** | ⚠️ Anbefalt | `ama-backend/.env` linje 42-43 |
| **Linear** | ❌ Valgfritt | `ama-backend/.env` linje 47 |
| **Supabase** | ❌ Valgfritt | `ama-backend/.env` linje 51-52 |

---

## 🚀 Quick Start

**Minimum for å starte:**
1. Legg inn API-nøkler for alle 6 agenter
2. Start CSN Server:
   ```bash
   cd ama-backend
   python -m uvicorn minimal_server:app --host 0.0.0.0 --port 8001 --reload
   ```
3. Test collective intelligence consultation:
   ```bash
   curl -X POST http://localhost:8001/collective-intelligence/consultation \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Test spørsmål",
       "requester": "Osvald"
     }'
   ```

---

## ❓ Troubleshooting

### "API_KEY not found"

**Problem:** En eller flere agenter vil kjøre i fallback mode.

**Løsning:** Legg inn manglende API-nøkkel i `ama-backend/.env`.

### "Redis connection failed"

**Problem:** Upstash Redis ikke konfigurert.

**Løsning:**
1. Opprett gratis Upstash Redis database
2. Kopier URL og Token
3. Legg inn i `ama-backend/.env` linje 42-43

---

## 🔒 Security Best Practices

1. **ALDRI commit .env-filen til git**
2. **ALDRI del API-nøkler i chat eller dokumenter**
3. **Roter nøkler regelmessig** (hver 3-6 måned)
4. **Bruk separate nøkler** for dev/staging/production
5. **Overvåk bruk** i hver service-portal

---

**Dokumentert:** 28. oktober 2025
**Sist oppdatert:** 28. oktober 2025
