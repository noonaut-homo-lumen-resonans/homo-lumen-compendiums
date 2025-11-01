# Anthropic API Key - Quick Start Guide

**Dato:** 31. oktober 2025

---

## ⚠️ Viktig: Få Din API Key Først!

**Du må ha en Anthropic API key før du kan sette den.**

1. Gå til: https://console.anthropic.com/settings/keys
2. Logg inn med din Anthropic-konto
3. Klikk "Create Key"
4. **Kopier key** (den vises kun én gang!)
   - Format: `sk-ant-api03-...`

---

## 🔧 Sett API Key (Riktig Syntaks)

### Git Bash / Bash

**⚠️ IKKE SLIK (feil):**
```bash
export ANTHROPIC_API_KEY='bash'  # ❌ FEIL!
```

**✅ RIKTIG:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-DIN_FAKTISKE_KEY_HER"
```

**Eksempel:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-abcdef123456789..."
```

### PowerShell

**⚠️ IKKE SLIK (feil):**
```powershell
$env:ANTHROPIC_API_KEY = 'bash'  # ❌ FEIL!
```

**✅ RIKTIG:**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-DIN_FAKTISKE_KEY_HER"
```

**Eksempel:**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-abcdef123456789..."
```

---

## 🚀 Enkleste Metode: Bruk Setup Script

**I stedet for å skrive kommandoer manuelt, bruk setup-script:**

### Bash:
```bash
bash scripts/setup_anthropic_key.sh
```

### PowerShell:
```powershell
.\scripts\setup_anthropic_key.ps1
```

Scriptet vil:
- ✅ Be deg om API key (skjult input)
- ✅ Validere formatet
- ✅ Gi deg valg: environment variable, .env file, eller Secret Manager
- ✅ Teste at det fungerer

---

## ✅ Verifiser at Det Fungerer

**Test API key:**
```bash
python scripts/test_anthropic_sdk.py
```

**Eller manuelt:**
```python
import os
print(os.getenv("ANTHROPIC_API_KEY"))
# Skal vise: sk-ant-api03-...
```

---

## 💾 Permanent Lagring

### Bash - Legg til i ~/.bashrc eller ~/.bash_profile

```bash
# Åpne fil
nano ~/.bashrc

# Legg til linje
export ANTHROPIC_API_KEY="sk-ant-api03-DIN_KEY"

# Lagre og restart bash
source ~/.bashrc
```

### PowerShell - Permanent (User level)

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-api03-DIN_KEY", "User")

# Restart PowerShell
```

### Google Secret Manager (Anbefalt for Produksjon)

```powershell
# Hent key fra console.anthropic.com først!
echo -n "sk-ant-api03-DIN_KEY" | gcloud secrets create anthropic-api-key --data-file=- --project=dotted-stage-476513-r4
```

---

## ❌ Vanlige Feil

### Feil 1: Glemmer å erstatte placeholder
```bash
# ❌ FEIL
export ANTHROPIC_API_KEY='sk-ant-...'

# ✅ RIKTIG
export ANTHROPIC_API_KEY="sk-ant-api03-abcdef123456..."
```

### Feil 2: Bruker feil anførselstegn
```bash
# ❌ FEIL (singel quotes kan gi problemer med spesialtegn)
export ANTHROPIC_API_KEY='sk-ant-...'

# ✅ RIKTIG (dobbel quotes)
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

### Feil 3: Glemmer `export` i Bash
```bash
# ❌ FEIL (kun for denne kommandoen)
ANTHROPIC_API_KEY="sk-ant-..."

# ✅ RIKTIG (gjør den tilgjengelig for sub-processer)
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

### Feil 4: Mellomrom i key
```bash
# ❌ FEIL
export ANTHROPIC_API_KEY = "sk-ant-..."  # Mellomrom rundt =

# ✅ RIKTIG
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

---

## 🔗 Hvor Få API Key

1. **Gå til Anthropic Console:** https://console.anthropic.com/
2. **Logg inn** (eller opprett konto)
3. **Gå til Settings → API Keys:** https://console.anthropic.com/settings/keys
4. **Klikk "Create Key"**
5. **Gi den et navn** (f.eks. "Homo Lumen Development")
6. **Kopier key** (vises kun én gang!)

**Format:**
- Starter med: `sk-ant-api03-`
- Følges av: lange alfanumeriske karakterer

---

## 📋 Checklist

- [ ] Har du fått API key fra Anthropic Console?
- [ ] Har du kopiert key (vises kun én gang)?
- [ ] Har du satt environment variable korrekt?
- [ ] Har du testet med `python scripts/test_anthropic_sdk.py`?
- [ ] Fungerer det? ✅

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)

