# Notion API Key Storage Summary

**Dato:** 31. oktober 2025
**Status:** ✅ Lagret i både Google Secret Manager og Windows Credential Manager

---

## 📦 Lagringsplasseringer

### 1. Google Secret Manager ✅
- **Secret navn:** `notion-api-key`
- **Prosjekt:** `dotted-stage-476513-r4`
- **Versjon:** Latest (1)
- **Status:** Aktivt
- **Bruk:** Produksjon, sikker backup, scripts

**Hente:**
```powershell
gcloud secrets versions access latest --secret=notion-api-key --project=dotted-stage-476513-r4
```

**Python script:**
```python
from scripts.get_notion_key_from_secret import get_notion_api_key
notion_key = get_notion_api_key()
```

### 2. Windows Credential Manager ✅
- **Credential target:** `NotionAPI:notion.so`
- **Type:** Generic Credential
- **User:** `notion-mcp`
- **Status:** Aktivt
- **Bruk:** Lokal tilgang, Cursor MCP (kan brukes i fremtiden)

**Hente:**
Scriptet `scripts/setup_local_notion_key.ps1` håndterer henting og lagring.

**Sjekke:**
```powershell
cmdkey /list | Select-String "NotionAPI"
```

### 3. Cursor MCP Config ✅
- **Fil:** `C:\Users\onigo\.cursor\mcp.json`
- **Metode:** CLI argument (`-t`) direkte i config
- **Status:** Aktivt og testet
- **Bruk:** Cursor IDE Notion MCP integration

---

## 🔄 Oppdatere Notion API Key

### Hvis nøkkelen må oppdateres:

**1. Oppdater i Google Secret Manager:**
```powershell
.\scripts\save_notion_key_to_secret_manager.ps1
```

**2. Oppdater lokalt (hent fra Secret Manager):**
```powershell
.\scripts\setup_local_notion_key.ps1
```

**3. Oppdater Cursor MCP config:**
Rediger `C:\Users\onigo\.cursor\mcp.json` og oppdater API-nøkkelen i `args`-arrayet:
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@orbit-logistics/notion-mcp-server",
        "-t",
        "NY_API_KEY_HER"
      ]
    }
  }
}
```

**4. Restart Cursor** etter oppdatering.

---

## 📚 Relaterte Filer

### Scripts:
- `scripts/save_notion_key_to_secret_manager.ps1` - Lagre/oppdatere i Secret Manager
- `scripts/setup_local_notion_key.ps1` - Hente fra Secret Manager og lagre lokalt
- `scripts/get_notion_key_from_secret.py` - Python helper for å hente fra Secret Manager
- `scripts/test_notion_api.py` - Test Notion API connection

### Dokumentasjon:
- `docs/NOTION_MCP_SETUP.md` - Komplett setup guide
- `docs/GOOGLE_CLOUD_PROJECT_SETUP.md` - GCP project overview
- `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md` - Secret Manager guide

---

## ✅ Verifikasjon

Alle lagringsmetoder er testet og fungerer:
- ✅ Google Secret Manager: Lagret og tilgjengelig
- ✅ Windows Credential Manager: Lagret og tilgjengelig
- ✅ Cursor MCP Config: Konfigurert og testet

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)

