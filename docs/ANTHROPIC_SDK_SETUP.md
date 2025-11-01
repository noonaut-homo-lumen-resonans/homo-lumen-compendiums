# Anthropic SDK Setup - Homo Lumen Compendiums

**Dato:** 31. oktober 2025
**SDK Versjon:** 0.71.0 (installed)

---

## ✅ Status

Anthropic Python SDK er allerede installert i prosjektet.

**Installasjon:**
```bash
pip install anthropic
```

**Verifiser:**
```bash
python -c "import anthropic; print(anthropic.__version__)"
# Output: 0.71.0
```

---

## 🔐 API Key Setup

### Metode 1: Google Secret Manager (Anbefalt for Produksjon)

**Lagre API key:**
```powershell
# Hent API key fra: https://console.anthropic.com/settings/keys
echo -n "sk-ant-api03-YOUR_KEY_HERE" | gcloud secrets create anthropic-api-key --data-file=- --project=dotted-stage-476513-r4
```

**Hente i kode:**
```python
from google.cloud import secretmanager

def get_anthropic_api_key():
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/dotted-stage-476513-r4/secrets/anthropic-api-key/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

### Metode 2: Environment Variable (Lokal Utvikling)

**PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-YOUR_KEY_HERE"
```

**Permanent (User level):**
```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-YOUR_KEY_HERE", "User")
```

**Bash:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-YOUR_KEY_HERE"
```

---

## 📝 Grunnleggende Bruk

### Enkel Melding

```python
import anthropic

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")  # Eller hent fra Secret Manager
)

message = client.messages.create(
    model="claude-sonnet-4-5",  # Eller "claude-3-5-sonnet-20241022"
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)

print(message.content[0].text)
```

### Med System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="Du er en hjelpsom AI-assistent som svarer på norsk.",
    messages=[
        {"role": "user", "content": "Forklar hva Homo Lumen er."}
    ]
)
```

### Streaming Response

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Tell me a story"}
    ]
) as stream:
    for text_block in stream.text_stream:
        print(text_block, end="", flush=True)
```

### Async (for FastAPI)

```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=api_key)

async def chat():
    message = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello"}
        ]
    )
    return message.content
```

---

## 🔄 Oppdater Eksisterende Kode

Prosjektet bruker nå `aiohttp` direkte for Claude API. Anbefaling: oppdater til official SDK.

**Før (aiohttp):**
```python
async with aiohttp.ClientSession() as session:
    async with session.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": self.api_key, ...},
        json=api_request
    ) as response:
        # Parse response
```

**Etter (Anthropic SDK):**
```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=self.api_key)
message = await client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "..."}]
)
```

**Fordeler med SDK:**
- ✅ Automatisk håndtering av API-endringer
- ✅ Bedre error handling
- ✅ Type hints og autocomplete
- ✅ Streaming support out-of-the-box
- ✅ Tool use (function calling) enklere

---

## 📋 Tilgjengelige Modeller

**Claude Sonnet 4.5 (Anbefalt):**
- `claude-sonnet-4-5` (latest)
- `claude-3-5-sonnet-20241022` (specific version)

**Claude Sonnet 3.5:**
- `claude-3-5-sonnet-20241022`
- `claude-3-5-sonnet-20240620`

**Claude Opus:**
- `claude-3-opus-20240229`

**Claude Haiku:**
- `claude-3-haiku-20240307`

---

## 🧪 Test Script

Kjør test-script for å verifisere oppsett:

```bash
python scripts/test_anthropic_sdk.py
```

Eller se eksempler:
```bash
python scripts/setup_anthropic_sdk_example.py
```

---

## 🔗 Relaterte Dokumenter

- `ama-backend/csn_server/platforms/claude_agent.py` - Eksisterende Claude implementasjon
- `docs/VS_CODE_NOTIFICATIONS_FIX.md` - VS Code setup
- `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md` - Secret Manager guide

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)
**Status:** ✅ Ready to use

