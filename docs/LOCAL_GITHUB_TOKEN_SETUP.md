# Lokal GitHub Token Lagring - Setup Guide

**Dato:** 31. oktober 2025
**For:** Homo Lumen Compendiums lokal utvikling

---

## 🎯 Oversikt

For lokal utvikling kan det være praktisk å lagre GitHub-tokenet lokalt, slik at du ikke trenger å hente det fra Secret Manager hver gang du gjør Git-operasjoner.

**⚠️ VIKTIG:** Dette er kun for lokal utvikling. For produksjon bør du alltid bruke Secret Manager.

---

## Metode 1: Git Credential Manager (Anbefalt) ⭐

Git Credential Manager lagrer tokens kryptert i Windows Credential Manager.

### Steg 1: Installer Git Credential Manager (hvis ikke allerede installert)

Git Credential Manager kommer vanligvis med Git for Windows. Sjekk om det er installert:

```powershell
# Sjekk om det er installert
where.exe git-credential-manager.exe
```

Hvis ikke installert:
1. Last ned: https://github.com/git-ecosystem/git-credential-manager/releases
2. Eller oppdater Git for Windows (som inkluderer GCM)

### Steg 2: Konfigurer Git til å bruke Credential Manager

```bash
# Sett Credential Manager som credential helper
git config --global credential.helper manager

# Eller for Windows Credential Manager
git config --global credential.helper wincred
```

### Steg 3: Lagre token første gang

```bash
# Når du gjør første push/pull, vil Git spørre om credentials
# Bruk ditt GitHub token som passord:
# Username: noonaut-homo-lumen-resonans
# Password: <ditt_github_token>

git push origin main
```

Git Credential Manager vil da lagre tokenet kryptert i Windows Credential Manager.

**For å manuelt lagre token:**
```powershell
# Hent token fra Secret Manager
$token = gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4

# Lagre i Windows Credential Manager
cmdkey /generic:git:https://github.com /user:noonaut-homo-lumen-resonans /pass:$token
```

**For å se lagrede credentials:**
```powershell
cmdkey /list | Select-String -Pattern "git"
```

**For å slette lagrede credentials:**
```powershell
cmdkey /delete:git:https://github.com
```

---

## Metode 2: Lokal .git/config med credential helper ⚠️

Dette lagrer tokenet i `.git/config` (IKKE committet til repo).

### Steg 1: Sett opp credential helper i repo

```bash
cd "C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums"

# Sett credential helper kun for dette repoet
git config credential.helper store

# Eller for Windows Credential Manager
git config credential.helper wincred
```

### Steg 2: Lagre token første gang

```bash
# Push en gang - Git vil spørre om credentials
git push origin main

# Username: noonaut-homo-lumen-resonans
# Password: <ditt_github_token>
```

Tokenet lagres da i `.git/config` eller Windows Credential Manager (ikke synlig i filen).

---

## Metode 3: Environment Variable (Lokal utvikling) ⚠️

⚠️ **Mindre sikkert, men enkelt for lokal utvikling**

### Steg 1: Lagre token som environment variable

**PowerShell (Session-basert):**
```powershell
# Bare for denne PowerShell-sesjonen
$env:GITHUB_TOKEN = gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4
```

**PowerShell (Permanent - User):**
```powershell
# Lagre permanent for brukeren
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", (gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4), "User")

# Restart PowerShell for at endringen skal tre i kraft
```

**Bash (Session-basert):**
```bash
export GITHUB_TOKEN=$(gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4)
```

**Bash (Permanent):**
```bash
# Legg til i ~/.bashrc eller ~/.bash_profile
echo 'export GITHUB_TOKEN=$(gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4)' >> ~/.bashrc
source ~/.bashrc
```

### Steg 2: Bruk token med Git

**PowerShell:**
```powershell
$token = $env:GITHUB_TOKEN
git push https://$token@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git main
```

**Bash:**
```bash
git push https://$GITHUB_TOKEN@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git main
```

### Steg 3: Konfigurer Git remote med token (ikke anbefalt)

⚠️ **Ikke anbefalt - token blir synlig i Git config**

```bash
# Hent token
token=$(gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4)

# Sett remote URL med token (MIDLERTIDIG)
git remote set-url origin https://$token@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git

# ⚠️ HUSK: Fjern token fra URL etter bruk!
git remote set-url origin https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git
```

---

## Metode 4: Script Wrapper (Best Practice) ⭐⭐⭐

Opprett en wrapper-funksjon som automatisk henter token når det trengs.

### PowerShell Funksjon (Legg i $PROFILE)

```powershell
# Legg til i PowerShell profile: notepad $PROFILE

function git-with-token {
    param([string[]]$args)

    # Hent token fra Secret Manager
    $token = gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Kunne ikke hente token" -ForegroundColor Red
        return
    }

    # For push/pull operasjoner, bruk token
    if ($args[0] -eq "push" -or $args[0] -eq "pull") {
        $remote = git remote get-url origin
        if ($remote -match "github\.com") {
            $remoteWithToken = $remote -replace "https://", "https://$token@"
            git remote set-url origin $remoteWithToken
            git @args
            git remote set-url origin $remote
        } else {
            git @args
        }
    } else {
        git @args
    }
}

# Alias (valgfritt)
Set-Alias -Name ggit -Value git-with-token
```

**Bruk:**
```powershell
git-with-token push origin main
# Eller med alias:
ggit push origin main
```

### Bash Funksjon

```bash
# Legg til i ~/.bashrc

git-with-token() {
    # Hent token fra Secret Manager
    local token=$(gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4 2>/dev/null)

    if [ -z "$token" ]; then
        echo "❌ Kunne ikke hente token" >&2
        return 1
    fi

    # For push/pull, sett remote URL med token midlertidig
    if [ "$1" = "push" ] || [ "$1" = "pull" ]; then
        local current_remote=$(git remote get-url origin)
        if echo "$current_remote" | grep -q "github.com"; then
            git remote set-url origin $(echo "$current_remote" | sed "s|https://|https://$token@|")
            git "$@"
            git remote set-url origin "$current_remote"
        else
            git "$@"
        fi
    else
        git "$@"
    fi
}

# Alias
alias ggit="git-with-token"
```

**Bruk:**
```bash
git-with-token push origin main
# Eller:
ggit push origin main
```

---

## Anbefalt Oppsett: Hybrid Løsning ⭐⭐⭐

**Beste praksis:** Kombiner Secret Manager med lokal caching:

1. **Hovedlagring:** Secret Manager (for sikkerhet)
2. **Lokal cache:** Windows Credential Manager (for bekvemmelighet)
3. **Refresh:** Hent fra Secret Manager og oppdater cache når token roteres

### Setup Script

```powershell
# scripts/setup_local_github_token.ps1

# Hent token fra Secret Manager
$token = gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Kunne ikke hente token fra Secret Manager" -ForegroundColor Red
    exit 1
}

# Lagre i Windows Credential Manager
cmdkey /generic:git:https://github.com /user:noonaut-homo-lumen-resonans /pass:$token

Write-Host "✅ Token lagret lokalt i Windows Credential Manager" -ForegroundColor Green
Write-Host "   Token hentes automatisk fra Secret Manager" -ForegroundColor Gray
```

**Kjør etter token-rotasjon:**
```powershell
.\scripts\setup_local_github_token.ps1
```

---

## Sammenligning

| Metode | Sikkerhet | Bekvemmelighet | Anbefaling |
|--------|-----------|----------------|------------|
| Git Credential Manager | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Best |
| Script Wrapper | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Bra |
| Environment Variable | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ OK for lokal |
| .git/config | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⚠️ OK |
| Hardkodet i remote | ⭐ | ⭐⭐⭐⭐⭐ | ❌ Ikke anbefalt |

---

## Oppdatering etter Token Rotasjon

Når du roterer tokenet i Secret Manager, må du også oppdatere lokal lagring:

```powershell
# 1. Oppdater i Secret Manager (allerede gjort)
echo -n "<nytt_token>" | gcloud secrets versions add github-token --data-file=-

# 2. Hent nytt token og lagre lokalt
.\scripts\setup_local_github_token.ps1

# Eller manuelt:
$token = gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4
cmdkey /generic:git:https://github.com /user:noonaut-homo-lumen-resonans /pass:$token
```

---

## Feilsøking

**Problem: Git spør fortsatt om passord**

```bash
# Sjekk credential helper
git config --global credential.helper

# Sjekk lagrede credentials
cmdkey /list | Select-String -Pattern "git"

# Slett og lagre på nytt
cmdkey /delete:git:https://github.com
.\scripts\setup_local_github_token.ps1
```

**Problem: Token fungerer ikke**

```bash
# Test token direkte
$token = gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4
curl -H "Authorization: token $token" https://api.github.com/user
```

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)
**Neste Review:** Ved behov

