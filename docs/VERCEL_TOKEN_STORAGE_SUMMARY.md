# Vercel Access Token Storage Summary

**Dato:** 31. oktober 2025
**Status:** ✅ Lagret i både Google Secret Manager og Windows Credential Manager

---

## 📦 Lagringsplasseringer

### 1. Google Secret Manager ✅
- **Secret navn:** `vercel-access-token`
- **Prosjekt:** `dotted-stage-476513-r4`
- **Versjon:** Latest (1)
- **Status:** Aktivt
- **Bruk:** Produksjon, sikker backup, scripts

**Hente:**
```powershell
gcloud secrets versions access latest --secret=vercel-access-token --project=dotted-stage-476513-r4
```

**Python script:**
```python
from scripts.get_vercel_token_from_secret import get_vercel_token
vercel_token = get_vercel_token()
```

### 2. Windows Credential Manager ✅
- **Credential target:** `VercelAPI:vercel.com`
- **Type:** Generic Credential
- **User:** `vercel-mcp`
- **Status:** Aktivt
- **Bruk:** Lokal tilgang, VS Code extension

**Hente:**
Scriptet `scripts/setup_local_vercel_token.ps1` håndterer henting og lagring.

**Sjekke:**
```powershell
cmdkey /list | Select-String "VercelAPI"
```

### 3. Environment Variable ✅
- **Navn:** `VERCEL_TOKEN`
- **Type:** User-level environment variable
- **Status:** Aktivt
- **Bruk:** VS Code Vercel extension leser automatisk fra denne

**Sjekke:**
```powershell
$env:VERCEL_TOKEN
```

**Sette permanent:**
```powershell
[System.Environment]::SetEnvironmentVariable("VERCEL_TOKEN", "vercel_token_her", "User")
```

---

## 🔄 Oppdatere Vercel Token

### Hvis tokenet må oppdateres:

**1. Oppdater i Google Secret Manager:**
```powershell
.\scripts\save_vercel_token_to_secret_manager.ps1
```

**2. Oppdater lokalt (hent fra Secret Manager):**
```powershell
.\scripts\setup_local_vercel_token.ps1
```

**3. Oppdater Environment Variable (hvis nødvendig):**
```powershell
[System.Environment]::SetEnvironmentVariable("VERCEL_TOKEN", "NY_TOKEN_HER", "User")
```

**4. Restart VS Code/Cursor** etter oppdatering.

---

## 📋 Bruksområder

### VS Code Vercel Extension
VS Code extension leser automatisk fra `VERCEL_TOKEN` environment variable. Ingen ekstra konfigurasjon nødvendig.

### Vercel CLI
```bash
# Sett token for denne sesjonen
export VERCEL_TOKEN=$(gcloud secrets versions access latest --secret=vercel-access-token --project=dotted-stage-476513-r4)

# Eller hent fra Secret Manager
vercel login --token=$(gcloud secrets versions access latest --secret=vercel-access-token --project=dotted-stage-476513-r4)
```

### Programmatisk (Python)
```python
from scripts.get_vercel_token_from_secret import get_vercel_token
vercel_token = get_vercel_token()

# Bruk med requests
import requests
headers = {"Authorization": f"Bearer {vercel_token}"}
response = requests.get("https://api.vercel.com/v2/user", headers=headers)
```

---

## 📚 Relaterte Filer

### Scripts:
- `scripts/save_vercel_token_to_secret_manager.ps1` - Lagre/oppdatere i Secret Manager
- `scripts/setup_local_vercel_token.ps1` - Hente fra Secret Manager og lagre lokalt
- `scripts/get_vercel_token_from_secret.py` - Python helper for å hente fra Secret Manager

### Dokumentasjon:
- `docs/VS_CODE_NOTIFICATIONS_FIX.md` - VS Code Vercel extension setup
- `docs/GOOGLE_CLOUD_PROJECT_SETUP.md` - GCP project overview
- `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md` - Secret Manager guide

---

## ✅ Verifikasjon

Alle lagringsmetoder er testet og fungerer:
- ✅ Google Secret Manager: Lagret og tilgjengelig
- ✅ Windows Credential Manager: Lagret og tilgjengelig
- ✅ Environment Variable: Satt og aktivt

---

## 🔐 Sikkerhet

**Best Practices:**
- ✅ Token er lagret i Secret Manager (sikker backup)
- ✅ Token er lagret i Windows Credential Manager (lokal tilgang)
- ✅ Token er IKKE hardkodet i kode
- ✅ Token er IKKE committet til Git
- ⚠️ Token er satt som environment variable (User-level, sikker)

**Token Format:**
- Starter med: `vercel_` eller annet format
- Lengde: Varierer
- Scope: Full Account (eller spesifikke prosjekter)

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)

