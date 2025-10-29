# Google Secret Manager - Quick Start Guide
**For:** Homo Lumen Resonans Project
**Project ID:** dotted-stage-476513-r4
**Date:** October 29, 2025

---

## Hva er Google Secret Manager?

Google Secret Manager er en sikker lagringstjeneste for API-nøkler, passord og andre sensitive data. I stedet for å lagre credentials i `.env` filer eller dokumentasjon, lagrer du dem kryptert i Google Cloud.

**Fordeler:**
- ✅ Kryptert lagring (Google-managed encryption)
- ✅ Versjonskontroll (kan gå tilbake til gamle secrets)
- ✅ Audit logging (hvem aksesserte hva og når)
- ✅ Fine-grained access control (kun riktige personer/tjenester har tilgang)
- ✅ Automatisk rotation (kan settes opp)

---

## Oppsett (Engangsprosess)

### 1. Aktiver Google Secret Manager API

```bash
# Logg inn på Google Cloud (hvis ikke allerede gjort)
gcloud auth login

# Sett prosjekt
gcloud config set project dotted-stage-476513-r4

# Aktiver Secret Manager API
gcloud services enable secretmanager.googleapis.com
```

**Alternativt via Web Console:**
1. Gå til: https://console.cloud.google.com/apis/library/secretmanager.googleapis.com?project=dotted-stage-476513-r4
2. Klikk "ENABLE"

---

### 2. Installer Google Cloud SDK (hvis ikke installert)

**Windows:**
1. Last ned: https://cloud.google.com/sdk/docs/install-sdk#windows
2. Kjør installer: `GoogleCloudSDKInstaller.exe`
3. Følg wizard (default settings er OK)
4. Restart terminal/CMD

**Verifiser installasjon:**
```bash
gcloud --version
# Should show: Google Cloud SDK 450.0.0 (or similar)
```

---

### 3. Installer Python Client Library

```bash
pip install google-cloud-secret-manager
```

---

## Lagre Secrets (Opprett nye)

### Via Command Line (Enkleste)

**Lagre GitHub Token:**
```bash
# Erstatt <your_new_github_token> med faktisk token
echo -n "<your_new_github_token>" | gcloud secrets create github-token \
  --data-file=- \
  --replication-policy="automatic"
```

**Lagre Google OAuth Client Secret:**
```bash
echo -n "<your_new_oauth_secret>" | gcloud secrets create google-oauth-client-secret \
  --data-file=-
```

**Lagre Upstash Redis Token:**
```bash
echo -n "<your_new_redis_token>" | gcloud secrets create upstash-redis-token \
  --data-file=-
```

**Lagre ClickUp API Key:**
```bash
echo -n "<your_new_clickup_key>" | gcloud secrets create clickup-api-key \
  --data-file=-
```

**Lagre Notion API Key:**
```bash
echo -n "<your_notion_api_key>" | gcloud secrets create notion-api-key \
  --data-file=-
```

---

### Via Web Console (Visuelt)

1. Gå til: https://console.cloud.google.com/security/secret-manager?project=dotted-stage-476513-r4
2. Klikk "+ CREATE SECRET"
3. Fyll inn:
   - **Name:** `github-token` (lowercase, hyphens only)
   - **Secret value:** Lim inn API key
   - **Replication policy:** "Automatic" (anbefalt)
4. Klikk "CREATE SECRET"

**Repeat for:**
- `google-oauth-client-secret`
- `upstash-redis-token`
- `clickup-api-key`
- `notion-api-key`
- `openai-api-key` (hvis du vil)

---

## Hente Secrets i Kode (Python)

### Metode 1: Direkte fra Python Script

**Oppsett (én gang):**
```bash
# Sett miljøvariabel for authentication
# Windows CMD:
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account-key.json

# Windows PowerShell:
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account-key.json"

# Alternativ: Bruk gcloud auth application-default login
gcloud auth application-default login
```

**Python Kode:**
```python
from google.cloud import secretmanager

def get_secret(secret_name, project_id="dotted-stage-476513-r4"):
    """
    Hent secret fra Google Secret Manager.

    Args:
        secret_name: Navnet på secret (e.g., "github-token")
        project_id: Google Cloud Project ID

    Returns:
        Secret value som string
    """
    client = secretmanager.SecretManagerServiceClient()

    # Build secret version name (use "latest")
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

    # Access secret
    response = client.access_secret_version(request={"name": name})

    # Decode payload
    secret_value = response.payload.data.decode("UTF-8")

    return secret_value

# Bruk:
if __name__ == "__main__":
    github_token = get_secret("github-token")
    print(f"GitHub Token: {github_token[:10]}...") # Print first 10 chars only

    redis_token = get_secret("upstash-redis-token")
    notion_key = get_secret("notion-api-key")
```

**Eksempel for CSN Server:**
```python
# I ama-backend/minimal_server.py eller config.py
import os
from google.cloud import secretmanager

def load_secrets():
    """Load all secrets from Google Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    project_id = "dotted-stage-476513-r4"

    secrets = {
        "GITHUB_TOKEN": "github-token",
        "NOTION_API_KEY": "notion-api-key",
        "UPSTASH_REDIS_TOKEN": "upstash-redis-token",
        "GOOGLE_CLIENT_SECRET": "google-oauth-client-secret",
    }

    config = {}
    for env_var, secret_name in secrets.items():
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        config[env_var] = response.payload.data.decode("UTF-8")

    return config

# Bruk i server startup:
secrets = load_secrets()
NOTION_API_KEY = secrets["NOTION_API_KEY"]
```

---

### Metode 2: Hybrid med .env Fallback

**Best Practice for Development:**
```python
# config.py
import os
from google.cloud import secretmanager

def get_secret_hybrid(secret_name, env_var_name=None):
    """
    Try Google Secret Manager first, fallback to .env file.

    Args:
        secret_name: Name in Secret Manager (e.g., "github-token")
        env_var_name: Environment variable name (e.g., "GITHUB_TOKEN")

    Returns:
        Secret value
    """
    # Try environment variable first (local development)
    if env_var_name and os.getenv(env_var_name):
        print(f"Using {env_var_name} from .env file")
        return os.getenv(env_var_name)

    # Fallback to Google Secret Manager (production)
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/dotted-stage-476513-r4/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        print(f"Using {secret_name} from Google Secret Manager")
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accessing secret {secret_name}: {e}")
        raise

# Bruk:
from dotenv import load_dotenv
load_dotenv()  # Load .env for local development

NOTION_API_KEY = get_secret_hybrid("notion-api-key", "NOTION_API_KEY")
GITHUB_TOKEN = get_secret_hybrid("github-token", "GITHUB_TOKEN")
```

**`.env` file (for local development only - NOT committed to git):**
```
NOTION_API_KEY=your_local_key_for_testing
GITHUB_TOKEN=your_local_token_for_testing
```

**`.env.example` (committed to git - template):**
```
# Local development only - copy to .env and fill in values
# In production, these are loaded from Google Secret Manager
NOTION_API_KEY=
GITHUB_TOKEN=
UPSTASH_REDIS_TOKEN=
```

---

## Service Account Setup (For Automated Access)

**Hvis du vil at servere/workflows skal aksessere secrets automatisk:**

### 1. Opprett Service Account

```bash
gcloud iam service-accounts create homo-lumen-secret-reader \
  --display-name="Homo Lumen Secret Reader" \
  --project=dotted-stage-476513-r4
```

### 2. Gi Tilgang til Secrets

```bash
# Grant "Secret Manager Secret Accessor" role
gcloud projects add-iam-policy-binding dotted-stage-476513-r4 \
  --member="serviceAccount:homo-lumen-secret-reader@dotted-stage-476513-r4.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 3. Last ned Service Account Key

```bash
gcloud iam service-accounts keys create ~/homo-lumen-sa-key.json \
  --iam-account=homo-lumen-secret-reader@dotted-stage-476513-r4.iam.gserviceaccount.com
```

**⚠️ VIKTIG:** Lagre `homo-lumen-sa-key.json` sikkert, IKKE commit til git!

### 4. Bruk Service Account i Kode

```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/homo-lumen-sa-key.json"

# Now Python scripts will automatically use service account
```

---

## Liste alle Secrets (Verifisere)

**Via Command Line:**
```bash
gcloud secrets list --project=dotted-stage-476513-r4
```

**Via Python:**
```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
parent = "projects/dotted-stage-476513-r4"

print("Available secrets:")
for secret in client.list_secrets(request={"parent": parent}):
    print(f"- {secret.name}")
```

---

## Oppdatere Secrets (Nye Versjoner)

**Når du roterer API keys:**

```bash
# Add new version (old versions remain accessible)
echo -n "<new_github_token>" | gcloud secrets versions add github-token \
  --data-file=-
```

**Se historikk:**
```bash
gcloud secrets versions list github-token
# Shows all versions with creation date
```

**Hent eldre versjon (hvis nødvendig):**
```python
# Specify version number instead of "latest"
name = "projects/dotted-stage-476513-r4/secrets/github-token/versions/1"
```

---

## Slette Secrets (Vær Forsiktig!)

```bash
# Destroy secret version (can't be undone)
gcloud secrets versions destroy 1 --secret="github-token"

# Delete entire secret
gcloud secrets delete github-token
```

---

## Kostnader

**Pricing (October 2025):**
- Active secret versions: $0.06/month (per secret version)
- Access operations: $0.03 per 10,000 operations
- Replication: Included

**Estimert kostnad for Homo Lumen:**
- 5 secrets × 1 version each = $0.30/month
- ~10,000 accesses/month = $0.03/month
- **Total: ~$0.33/month (~3.50 NOK/month)**

Neglisjerbart sammenlignet med sikkerhetsrisikoen ved eksponerte credentials!

---

## Praktisk Eksempel: Migrere Notion API Key

### Trinn-for-trinn:

**1. Lagre eksisterende key i Secret Manager:**
```bash
# Erstatt <your_notion_api_key> med din faktiske key
echo -n "<your_notion_api_key>" | \
  gcloud secrets create notion-api-key --data-file=-
```

**2. Verifiser:**
```bash
gcloud secrets versions access latest --secret="notion-api-key"
# Should print your key
```

**3. Oppdater Python script:**
```python
# Før (UNSAFE):
NOTION_API_KEY = "<your_hardcoded_key>"

# Etter (SAFE):
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = "projects/dotted-stage-476513-r4/secrets/notion-api-key/versions/latest"
response = client.access_secret_version(request={"name": name})
NOTION_API_KEY = response.payload.data.decode("UTF-8")
```

**4. Slett key fra dokumentasjon:**
- Søk etter `ntn_3863` i alle filer
- Erstatt med: `[STORED IN GOOGLE SECRET MANAGER: notion-api-key]`

**5. Test:**
```bash
python scripts/parse_lp.py  # Should still work
```

---

## GitHub Actions Integration

**For å bruke secrets i GitHub workflows:**

### 1. Opprett Workload Identity Federation (Anbefalt)

Se: https://github.com/google-github-actions/auth

**Eller bruk Service Account Key (Enklere for start):**

1. Last ned service account key (se over)
2. Legg til GitHub Secret:
   - Repo → Settings → Secrets → Actions
   - Name: `GCP_SA_KEY`
   - Value: Innholdet av `homo-lumen-sa-key.json`

3. Bruk i workflow:
```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v1
  with:
    credentials_json: ${{ secrets.GCP_SA_KEY }}

- name: Get Notion API Key
  run: |
    NOTION_KEY=$(gcloud secrets versions access latest --secret="notion-api-key")
    echo "NOTION_API_KEY=$NOTION_KEY" >> $GITHUB_ENV
```

---

## Feilsøking

**Problem: "Permission denied" når du kjører Python script**

```bash
# Solution: Authenticate gcloud
gcloud auth application-default login
```

**Problem: "Secret not found"**

```bash
# Check if secret exists
gcloud secrets list | grep notion-api-key

# Check permissions
gcloud secrets get-iam-policy notion-api-key
```

**Problem: "Could not load the default credentials"**

```bash
# Set credentials explicitly
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

---

## Neste Steg

1. **Aktiver Secret Manager API** (se trinn 1)
2. **Opprett secrets** for alle 5 exposed credentials
3. **Oppdater Python scripts** til å bruke `get_secret_hybrid()`
4. **Test lokalt** med .env fallback
5. **Verifiser produksjon** henter fra Secret Manager
6. **Slett credentials fra dokumentasjon**

---

**Spørsmål?**
Kontakt Zara (Security) eller Code (Implementation) via async communication channels.

**Generated:** October 29, 2025
**Author:** Code (Agent #9)
**Next Review:** When rotating keys (next 90 days)
