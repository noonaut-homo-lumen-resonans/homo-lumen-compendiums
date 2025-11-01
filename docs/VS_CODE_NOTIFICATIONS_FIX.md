# VS Code Notifications - Feil Løsning Guide

**Dato:** 31. oktober 2025
**For:** VS Code / Cursor IDE Feil

---

## 🔴 Feil 1: Claude Code MCP Provider

**Melding:** "Failed to register Claude Code MCP provider. Make sure Claude CLI is installed."

### Løsning

**Steg 1: Installer Claude CLI**

**Windows (PowerShell):**
```powershell
# Last ned og installer Claude CLI
winget install Anthropic.Claude

# Eller via npm (hvis du har Node.js)
npm install -g @anthropic-ai/cli
```

**Verifiser installasjon:**
```powershell
claude --version
```

**Steg 2: Autentiser Claude CLI**

```powershell
# Sett API-nøkkel
claude config set api-key YOUR_ANTHROPIC_API_KEY

# Eller via environment variable
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

**Hvor få Anthropic API Key:**
1. Gå til: https://console.anthropic.com/settings/keys
2. Klikk "Create Key"
3. Kopier key (den vises kun én gang!)

**Steg 3: Restart VS Code**

Etter installasjon, restart VS Code for at MCP provider skal registreres.

---

## 🔴 Feil 2: Vercel Access Token

**Melding:** "Please set your Vercel Access Token in the extension settings `vercelVSCode.accessToken`."

### Løsning

**Steg 1: Opprett Vercel Access Token**

1. Gå til: https://vercel.com/account/tokens
2. Logg inn med din Vercel-konto
3. Klikk **"Create Token"**
4. Fyll inn:
   - **Name:** `VS Code Extension`
   - **Scope:** `Full Account` (eller velg spesifikke prosjekter)
   - **Expiration:** Velg `No Expiration` (eller 1 år)
5. Klikk **"Create"**
6. **Kopier tokenet** (vises kun én gang!)
   - Format: `vercel_1a2b3c4d5e6f7g8h9i0j`

**Steg 2: Sett Token i VS Code Settings**

**Metode 1: Via Settings UI (Anbefalt)**

1. Åpne VS Code Settings:
   - `Ctrl + ,` (eller `Cmd + ,` på Mac)
   - Eller: File → Preferences → Settings

2. Søk etter: `vercel access token`

3. Klikk på "Vercel for VS Code" extension settings

4. Lim inn tokenet i feltet `Vercel: Access Token`

**Metode 2: Via settings.json (Direkte)**

1. Åpne Command Palette:
   - `Ctrl + Shift + P` (eller `Cmd + Shift + P` på Mac)

2. Type: `Preferences: Open User Settings (JSON)`

3. Legg til:
```json
{
  "vercelVSCode.accessToken": "vercel_ditt_token_her"
}
```

**Metode 3: Via Workspace Settings (Kun for dette prosjektet)**

Hvis du vil ha token kun for dette prosjektet:

1. Opprett/rediger `.vscode/settings.json` i prosjektet:
```json
{
  "vercelVSCode.accessToken": "vercel_ditt_token_her"
}
```

**⚠️ VIKTIG:**
- Legg `.vscode/settings.json` i `.gitignore` hvis du legger token der!
- Eller bruk environment variable (se under)

**Metode 4: Via Environment Variable (Anbefalt for Teams)**

Sett environment variable:
```powershell
# PowerShell
$env:VERCEL_TOKEN = "vercel_ditt_token_her"

# Permanent (User level)
[System.Environment]::SetEnvironmentVariable("VERCEL_TOKEN", "vercel_ditt_token_her", "User")
```

VS Code extension vil automatisk lese fra `VERCEL_TOKEN` environment variable.

**Steg 3: Restart VS Code**

Restart VS Code for at endringen skal tre i kraft.

---

## ℹ️ Info: Multiple Workspace Files

**Melding:** "This folder contains multiple workspace files. Do you want to open one?"

Dette er **ikke en feil**, men en informasjon. Hvis du vil åpne et spesifikt workspace:

1. Klikk "Select Workspace"
2. Velg ønsket workspace-fil (`.code-workspace`)
3. Eller ignorer denne meldingen

---

## ✅ Verifisering

**Test Claude MCP:**
```powershell
# Sjekk at Claude CLI fungerer
claude --version

# Test MCP connection
claude mcp list
```

**Test Vercel Extension:**
1. Åpne Command Palette: `Ctrl + Shift + P`
2. Type: `Vercel:`
3. Du skal se Vercel-kommandoer i listen
4. Prøv: `Vercel: Open Dashboard`

---

## 🛡️ Sikkerhet

### Lagre Tokens Sikkert

**Anbefalt:**
1. ✅ Bruk environment variables (ikke commit til Git)
2. ✅ Bruk Google Secret Manager (for produksjon)
3. ✅ Bruk VS Code User Settings (ikke workspace settings)

**Ikke gjør:**
1. ❌ Committ tokens til `.vscode/settings.json` i Git
2. ❌ Del tokens i chat eller dokumenter
3. ❌ Hardkode tokens i kode

**For dette prosjektet:**
Token kan lagres i Google Secret Manager:
```powershell
# Lagre Vercel token i Secret Manager
echo -n "vercel_ditt_token" | gcloud secrets create vercel-access-token --data-file=- --project=dotted-stage-476513-r4
```

---

## 📋 Quick Reference

### Claude CLI Setup
```powershell
# Installer
winget install Anthropic.Claude

# Autentiser
claude config set api-key YOUR_API_KEY

# Verifiser
claude --version
```

### Vercel Token Setup
```powershell
# 1. Hent token fra: https://vercel.com/account/tokens

# 2. Sett i VS Code settings.json:
{
  "vercelVSCode.accessToken": "vercel_ditt_token"
}

# 3. Eller via environment variable:
$env:VERCEL_TOKEN = "vercel_ditt_token"
```

---

## 🔗 Relaterte Dokumenter

- `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md` - Sikker lagring av tokens
- `ubuntu-playground/docs/API_KEYS_SETUP_GUIDE.md` - Vercel token setup guide
- `techdocs-source/archive/manus-session-2025-10-20/CLAUDE_CODE_INSTANCES_EXPLAINED.md` - Claude Code dokumentasjon

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)
**Status:** ✅ Løsningsguide

