# Fix: Lagre API Key i Secret Manager

**Problem:** Scriptet kan ikke lagre i Secret Manager.

---

## 🔍 Feilsøking

### Steg 1: Sjekk at gcloud fungerer i bash

I din bash terminal, kjør:

```bash
# Sjekk at gcloud er tilgjengelig
gcloud --version

# Sjekk autentisering
gcloud auth list

# Sjekk prosjekt
gcloud config get-value project
```

**Hvis gcloud ikke fungerer:**
- Google Cloud SDK er kanskje ikke i PATH i bash
- Du må kanskje restarte bash-terminalen etter installasjon

### Steg 2: Aktiver Secret Manager API

```bash
gcloud services enable secretmanager.googleapis.com --project=dotted-stage-476513-r4
```

### Steg 3: Autentiser (hvis nødvendig)

```bash
gcloud auth login
gcloud config set project dotted-stage-476513-r4
```

---

## ✅ Løsning: Manuell lagring

Hvis scriptet ikke fungerer, kan du lagre manuelt:

```bash
# Sjekk at API key er satt
echo $ANTHROPIC_API_KEY

# Lagre i Secret Manager (hvis secret ikke eksisterer)
echo -n "$ANTHROPIC_API_KEY" | gcloud secrets create anthropic-api-key \
  --data-file=- \
  --project=dotted-stage-476513-r4 \
  --replication-policy="automatic"

# ELLER oppdatere (hvis secret allerede eksisterer)
echo -n "$ANTHROPIC_API_KEY" | gcloud secrets versions add anthropic-api-key \
  --data-file=- \
  --project=dotted-stage-476513-r4
```

---

## 🔄 Alternativ: Bruk ~/.bashrc i stedet

Hvis Secret Manager ikke fungerer, kan du bruke ~/.bashrc:

```bash
bash scripts/add_to_bashrc.sh
```

Eller manuelt:

```bash
# Legg til i ~/.bashrc
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-DIN_KEY"' >> ~/.bashrc

# Last inn endringene
source ~/.bashrc
```

---

## 🧪 Verifiser lagring

**Secret Manager:**
```bash
gcloud secrets versions access latest --secret=anthropic-api-key --project=dotted-stage-476513-r4
```

**~/.bashrc:**
```bash
grep ANTHROPIC_API_KEY ~/.bashrc
```

---

**Opprettet:** 31. oktober 2025

