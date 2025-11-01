# Permanent API Key Setup - Enkel Guide

**Dato:** 31. oktober 2025

---

## ⚠️ Problem

`gcloud` fungerer ikke i PowerShell, og Secret Manager krever gcloud.

**Løsning:** Bruk `~/.bashrc` for enkel permanent lagring i bash.

---

## ✅ Enkel Løsning: ~/.bashrc

### Metode 1: Bruk Script (Anbefalt)

**I din BASH terminal (ikke PowerShell), kjør:**

```bash
bash scripts/add_to_bashrc.sh
```

Scriptet vil:
1. Hente API key fra `$ANTHROPIC_API_KEY`
2. Legge den til i `~/.bashrc`
3. Gi deg instruksjoner for å aktivere

### Metode 2: Manuell (Hvis script ikke fungerer)

```bash
# 1. Sjekk at API key er satt i denne sesjonen
echo $ANTHROPIC_API_KEY

# 2. Legg til i ~/.bashrc
echo '' >> ~/.bashrc
echo '# Anthropic API Key' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-DIN_KEY_HER"' >> ~/.bashrc

# 3. Last inn endringene
source ~/.bashrc

# 4. Verifiser
echo $ANTHROPIC_API_KEY
```

---

## 🔄 Aktivere i Nye Bash-sesjoner

Etter å ha lagt til i `~/.bashrc`:

1. **Aktivere i denne sesjonen:**
   ```bash
   source ~/.bashrc
   ```

2. **Eller restart bash-terminalen** (vil laste automatisk)

---

## ✅ Verifisering

```bash
# Sjekk at key er satt
echo $ANTHROPIC_API_KEY

# Test med Python
python scripts/test_anthropic_sdk.py
```

---

## 📋 Oppsummering

- ✅ API key satt i `~/.bashrc`
- ✅ Laster automatisk i nye bash-sesjoner
- ✅ Tilgjengelig for alle Python scripts
- ✅ Enkel og fungerer med en gang

---

**Opprettet:** 31. oktober 2025
**Status:** ✅ Enkel løsning

