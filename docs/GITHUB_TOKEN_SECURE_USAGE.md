# GitHub Token - Sikker Bruk via Google Secret Manager

**Dato:** 31. oktober 2025
**Prosjekt:** homo-lumen-compendiums
**Secret Manager:** `dotted-stage-476513-r4` → `github-token`

---

## ✅ Status

GitHub Personal Access Token er nå lagret **sikkert** i Google Secret Manager i stedet for å være hardkodet i Git remote URL.

**Secret navn:** `github-token`
**Lokasjon:** Google Cloud Project `dotted-stage-476513-r4`

---

## 🔐 Hente Token for Git-operasjoner

### Metode 1: PowerShell Script (Anbefalt)

Opprett en PowerShell-funksjon i din `$PROFILE`:

```powershell
function Get-GitHubToken {
    # Hent token fra Google Secret Manager
    $token = gcloud secrets versions access latest --secret="github-token" --project="dotted-stage-476513-r4"
    return $token
}

# Bruk for Git push/pull:
$token = Get-GitHubToken
git push https://$token@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git main
```

**Eller som one-liner:**
```powershell
git push https://$(gcloud secrets versions access latest --secret="github-token")@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git main
```

### Metode 2: Python Script

Bruke eksisterende script:
```bash
python scripts/get_github_token_from_secret.py
# Output: GitHub token (klar for bruk)
```

**Eksempel i PowerShell:**
```powershell
$token = python scripts/get_github_token_from_secret.py
git push https://$token@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git main
```

### Metode 3: Git Credential Helper (Automatisk)

Konfigurer Git til å automatisk hente token fra Secret Manager:

**PowerShell script (`setup_git_credential_helper.ps1`):**
```powershell
# Lagre som: scripts/setup_git_credential_helper.ps1

# Opprett en wrapper som henter token fra Secret Manager
$wrapperScript = @'
#!/bin/bash
# Git credential helper wrapper
token=$(gcloud secrets versions access latest --secret="github-token" --project="dotted-stage-476513-r4" 2>/dev/null)
echo "https://noonaut-homo-lumen-resonans:$token@github.com"
'@

# Installer som Git credential helper
git config --global credential.helper "!f() { echo 'username=noonaut-homo-lumen-resonans'; echo 'password='$(gcloud secrets versions access latest --secret='github-token' --project='dotted-stage-476513-r4')'; }; f"
```

**⚠️ Merk:** Denne metoden fungerer best med SSH-nøkler i stedet for tokens.

---

## 🧪 Test Token Henting

**Verifiser at token fungerer:**
```powershell
# Hent token
$token = gcloud secrets versions access latest --secret="github-token"

# Test API-tilgang
$headers = @{ "Authorization" = "token $token" }
Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers | ConvertTo-Json
```

**Forventet output:**
```json
{
  "login": "noonaut-homo-lumen-resonans",
  "id": 209359258,
  ...
}
```

---

## 🔄 Oppdatere Token (Når du roterer)

**Legg til ny versjon i Secret Manager:**
```powershell
# Hent nytt token (f.eks. fra GitHub Settings → Developer settings → Personal access tokens)
$newToken = Read-Host "Lim inn nytt GitHub token"

# Lagre som ny versjon (beholder gamle versjoner)
echo -n $newToken | gcloud secrets versions add github-token --data-file=-
```

**Sjekk versjonshistorie:**
```powershell
gcloud secrets versions list github-token
```

---

## 🛡️ Sikkerhet

**✅ DO:**
- ✅ Bruk Secret Manager for all lagring av tokens
- ✅ Roter tokens regelmessig (hver 90 dager)
- ✅ Revoke gamle tokens på GitHub etter rotasjon
- ✅ Bruk tokens med minst nødvendig scope

**❌ DON'T:**
- ❌ Ikke committ tokens til Git
- ❌ Ikke hardkode tokens i scripts eller dokumentasjon
- ❌ Ikke del tokens i chat/dokumenter (som denne!)
- ❌ Ikke bruk samme token i flere miljøer

---

## 📖 Relaterte Dokumenter

- `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md` - Komplett guide for Secret Manager
- `scripts/store_github_token_secret.py` - Script for å lagre token
- `scripts/get_github_token_from_secret.py` - Script for å hente token

---

## ✅ Token Rotasjon Fullført (31. oktober 2025)

Det eksponerte tokenet er nå rotert og erstattet med nytt token.

**Ny token versjon:** [2] (lagret 31. oktober 2025)
**Status:** ✅ Aktivt og testet
**GitHub bruker:** noonaut-homo-lumen-resonans

**For fremtidig rotasjon:**
1. **Gå til GitHub:** https://github.com/settings/tokens
2. **Opprett nytt token** med samme tilgang
3. **Lagre nytt token i Secret Manager:**
   ```bash
   echo -n "<nytt_token>" | gcloud secrets versions add github-token --data-file=- --project=dotted-stage-476513-r4
   ```
4. **Test token:**
   ```bash
   token=$(gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4)
   curl -H "Authorization: token $token" https://api.github.com/user
   ```
5. **Revoke gamle token** på GitHub (når du har verifisert at nytt fungerer)

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)
**Neste Review:** Når token roteres (ca. 90 dager)

