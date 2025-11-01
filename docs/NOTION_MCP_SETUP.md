# Notion MCP Setup Guide

**Dato:** 31. oktober 2025
**For:** Cursor IDE Notion MCP Integration

---

## 🎯 Oversikt

Denne guiden viser hvordan du setter opp Notion MCP (Model Context Protocol) i Cursor IDE, slik at jeg (Claude Code) kan interagere med Notion-databaser direkte.

---

## 📋 Steg 1: Hente Notion API Key

### 1.1. Opprett Notion Integration

1. Gå til: https://www.notion.so/my-integrations
2. Klikk **"+ New integration"**
3. Fyll inn:
   - **Name:** `Homo Lumen MCP`
   - **Type:** Internal
   - **Associated workspace:** Velg ditt workspace
4. Klikk **"Submit"**
5. **Kopier "Internal Integration Token"** (vises kun én gang!)
   - Format: `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 1.2. Gi Integration Tilgang til Databaser

For hver database du vil bruke:
1. Åpne databasen i Notion
2. Klikk **"..."** (øverst høyre)
3. Klikk **"Connections"**
4. Velg **"Homo Lumen MCP"**
5. Bekreft

---

## 🔐 Steg 2: Lagre Notion API Key (Google Secret Manager + Windows Credential Manager)

Notion API-nøkkelen er nå lagret i **både** Google Secret Manager og Windows Credential Manager for maksimal sikkerhet og tilgjengelighet.

### 📦 Lagret i:
1. ✅ **Google Secret Manager** (`notion-api-key`) - For produksjon og sikker lagring
2. ✅ **Windows Credential Manager** (`NotionAPI:notion.so`) - For lokal tilgang

### 🔄 Hente nøkkel lokalt (Windows Credential Manager)

For å hente nøkkel fra Secret Manager og lagre lokalt:
```powershell
.\scripts\setup_local_notion_key.ps1
```

Dette scriptet:
- Henter nøkkel fra Google Secret Manager
- Tester nøkkelen mot Notion API
- Lagrer i Windows Credential Manager for lokal tilgang

---

## 🔐 Steg 2a: Lagre Notion API Key i Secret Manager (Hvis ny eller oppdatering)

### Metode 1: PowerShell Script (Anbefalt for Windows)

```powershell
.\scripts\save_notion_key_to_secret_manager.ps1
```

Følg instruksjonene og lim inn API key når du blir bedt om det.

### Metode 2: Bash Script (For Git Bash)

```bash
bash scripts/save_notion_key_to_secret_manager.sh
```

### Metode 3: Manuelt via gcloud CLI

```powershell
# Legg til gcloud i PATH (hvis ikke allerede)
$env:Path += ";C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"

# Lagre secret
echo -n "secret_din_notion_api_key_her" | gcloud secrets create notion-api-key --data-file=- --project=dotted-stage-476513-r4

# Eller oppdatere eksisterende
echo -n "secret_din_notion_api_key_her" | gcloud secrets versions add notion-api-key --data-file=- --project=dotted-stage-476513-r4
```

---

## ⚙️ Steg 3: Konfigurer Cursor MCP

### 3.1. Cursor MCP Config er Allerede Opprettet

MCP config fil: `C:\Users\onigo\.cursor\mcp.json`

Innhold:
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@orbit-logistics/notion-mcp-server"
      ],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      }
    },
    "supabase": {
      "url": "https://mcp.supabase.com/mcp?project_ref=guhtqmoxurfroailltsc",
      "headers": {}
    }
  }
}
```

### 3.2. Notion API Key er Allerede Lagret! ✅

**Nøkkelen er nå:**
- ✅ Lagret i Google Secret Manager (`notion-api-key`)
- ✅ Lagret i Windows Credential Manager (`NotionAPI:notion.so`)
- ✅ Konfigurert i Cursor MCP (`mcp.json` med CLI argument)

**Du trenger IKKE å sette environment variables lenger!**

Cursor MCP bruker nøkkelen direkte fra `mcp.json` config.

### 3.3. Hente Nøkkel Programmatisk (For Scripts)

**Fra Secret Manager (Python):**
```python
from scripts.get_notion_key_from_secret import get_notion_api_key
notion_key = get_notion_api_key()
```

**Fra Secret Manager (PowerShell):**
```powershell
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
$env:Path += ";$gcloudPath"
$notionKey = gcloud secrets versions access latest --secret=notion-api-key --project=dotted-stage-476513-r4
```

**Fra Windows Credential Manager (Powershell):**
```powershell
# Vanskelig å hente direkte, men scriptet setup_local_notion_key.ps1 håndterer dette
```

---

## ✅ Steg 4: Test Notion API Connection

### Test Script

```powershell
# Legg til gcloud i PATH
$env:Path += ";C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"

# Kjør test
python scripts/test_notion_api.py
```

**Forventet Output:**
```
============================================================
Notion API Connection Test
============================================================

[*] Henter Notion API key fra Secret Manager...
[OK] Notion API key hentet fra Secret Manager
[OK] API key hentet (lengde: 50 tegn, starter med: secret_xxx...)
[*] Tester Notion API connection...
    URL: https://api.notion.com/v1/users/me

[OK] Notion API Connection Successful!
============================================================
User ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Name: Your Name
Workspace: Your Workspace
============================================================

[OK] Notion API test vellykket!
```

---

## 🛠️ Steg 5: Restart Cursor

Etter å ha satt environment variable:

1. **Steng Cursor helt**
2. **Åpne Cursor på nytt**
3. Cursor vil automatisk laste MCP config og koble til Notion

---

## 📚 Tilgjengelige Notion MCP Tools

Etter vellykket oppsett, vil jeg (Claude Code) ha tilgang til følgende Notion MCP tools:

### Search (1 tool)
- `notion-search` - Semantic search over workspace

### Pages (5 tools)
- `notion-fetch` - Retrieve page/database details
- `notion-create-pages` - Create new pages
- `notion-update-page` - Update existing page
- `notion-move-pages` - Move pages to new parent
- `notion-duplicate-page` - Duplicate a page

### Databases (2 tools)
- `notion-create-database` - Create new database
- `notion-update-database` - Update database properties

### Comments (2 tools)
- `notion-create-comment` - Add comment to page
- `notion-get-comments` - Get all page comments

### Workspace (3 tools)
- `notion-get-teams` - List teamspaces
- `notion-get-users` - List workspace users
- `notion-list-agents` - List custom agents/workflows

### User (2 tools)
- `notion-get-self` - Get bot user info
- `notion-get-user` - Get specific user

---

## 🔍 Verifisere at MCP Fungerer

### Metode 1: Be Claude Code om å bruke Notion

Prøv å be meg om:
- "Kan du søke i Notion etter [nøkkelord]?"
- "Opprett en ny side i Notion med tittel [tittel]"
- "Hent alle kommentarer fra Notion page [url]"

### Metode 2: Sjekk Cursor MCP Logs

1. Åpne Cursor Developer Tools: `Ctrl + Shift + I`
2. Se etter MCP-relaterte meldinger i Console

---

## ⚠️ Troubleshooting

### Problem: "NOTION_API_KEY not found"

**Løsning:**
1. Sjekk at environment variable er satt: `echo $env:NOTION_API_KEY`
2. Restart Cursor etter å ha satt variable
3. Verifiser at `~/.cursor/mcp.json` har riktig config

### Problem: "Authentication failed"

**Løsning:**
1. Verifiser at API key er korrekt (starter med `secret_`)
2. Sjekk at integration har tilgang til databaser
3. Test API key direkte: `python scripts/test_notion_api.py`

### Problem: "MCP server not found"

**Løsning:**
1. Sjekk at Node.js er installert: `node --version`
2. MCP server installeres automatisk via `npx`, men kan ta noen sekunder første gang

---

## 📝 Notater

- **API Key Format:** Notion API keys starter med `secret_` og er ca. 50 tegn lange
- **Secret Manager:** API key lagres sikkert i Google Secret Manager
- **Environment Variable:** Cursor bruker `${NOTION_API_KEY}` environment variable
- **Auto-install:** MCP server (`@orbit-logistics/notion-mcp-server`) installeres automatisk via `npx`

---

## ✅ Checklist

- [ ] Notion API key hentet fra https://www.notion.so/my-integrations
- [ ] API key lagret i Google Secret Manager
- [ ] Environment variable `NOTION_API_KEY` satt (eller hentes fra Secret Manager)
- [ ] Cursor MCP config oppdatert (`~/.cursor/mcp.json`)
- [ ] Notion API test vellykket (`python scripts/test_notion_api.py`)
- [ ] Cursor restartet
- [ ] MCP tools tilgjengelige i Cursor

---

**Status:** ✅ Config opprettet, klar for testing når API key er satt!



