# Supabase API Key Rotation Guide

**Dato:** 31. oktober 2025
**Project Reference:** `guhtqmoxurfroailltsc`

---

## 🎯 Oversikt

Supabase krever **3 typer nøkler**:
1. **Project URL** - `https://guhtqmoxurfroailltsc.supabase.co` (allerede kjent)
2. **Anon Key** (Public) - Brukt i frontend, kan roteres
3. **Service Role Key** (Secret) - Brukt for server-side operasjoner, KUN server-side!

---

## 📋 Steg 1: Hente Nye Nøkler fra Supabase Dashboard

### 1.1. Logg inn på Supabase Dashboard

1. Gå til: https://supabase.com/dashboard/project/guhtqmoxurfroailltsc
2. Logg inn med ditt Supabase-konto

### 1.2. Gå til API Settings

1. I venstre meny, klikk **"Settings"** (tannhjul-ikon)
2. Klikk **"API"** under Settings
3. Du vil se følgende seksjoner:
   - **Project URL** (allerede kjent)
   - **Project API keys**
     - `anon` `public` - Dette er ANON_KEY
     - `service_role` `secret` - Dette er SERVICE_ROLE_KEY

### 1.3. Kopier Nøklene

**Anon Key (Public):**
- Finn "anon" `public` key
- Kopier hele JWT tokenet (starter med `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)
- Dette er `NEXT_PUBLIC_SUPABASE_ANON_KEY`

**Service Role Key (Secret):**
- Finn "service_role" `secret` key
- ⚠️ **VIKTIG:** Klikk "Reveal" eller "Show" for å se den
- Kopier hele JWT tokenet
- Dette er `SUPABASE_SERVICE_ROLE_KEY`
- ⚠️ **Aldri eksponer denne i frontend eller klientkode!**

---

## 🔄 Steg 2: Rotere Nøkler (Hvis Nødvendig)

### 2.1. Rotere Anon Key

Hvis du vil rotere anon key (f.eks. etter kompromittering):

1. Gå til: https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api
2. Under "Project API keys", finn `anon` `public`
3. Klikk **"Reset"** eller **"Regenerate"**
4. ⚠️ **Viktig:** Den gamle nøkkelen vil slutte å fungere umiddelbart!
5. Kopier den nye nøkkelen

### 2.2. Rotere Service Role Key

**⚠️ ADVARSEL:** Rotering av service_role key vil bryte alle server-side operasjoner umiddelbart!

1. Gå til: https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api
2. Under "Project API keys", finn `service_role` `secret`
3. Klikk **"Reset"** eller **"Regenerate"**
4. ⚠️ **Planlegg dette nøye:** Oppdater alle server-side applikasjoner først!
5. Kopier den nye nøkkelen

---

## 💾 Steg 3: Lagre Nye Nøkler i Secret Manager

### 3.1. Lagre Anon Key

```powershell
# Metode 1: PowerShell script
.\scripts\save_supabase_anon_key_to_secret_manager.ps1

# Metode 2: Manuelt via gcloud
echo -n "din_nye_anon_key_her" | gcloud secrets create supabase-anon-key --data-file=- --project=dotted-stage-476513-r4

# Eller oppdatere eksisterende
echo -n "din_nye_anon_key_her" | gcloud secrets versions add supabase-anon-key --data-file=- --project=dotted-stage-476513-r4
```

### 3.2. Lagre Service Role Key

```powershell
# Metode 1: PowerShell script
.\scripts\save_supabase_service_role_key_to_secret_manager.ps1

# Metode 2: Manuelt via gcloud
echo -n "din_nye_service_role_key_her" | gcloud secrets create supabase-service-role-key --data-file=- --project=dotted-stage-476513-r4

# Eller oppdatere eksisterende
echo -n "din_nye_service_role_key_her" | gcloud secrets versions add supabase-service-role-key --data-file=- --project=dotted-stage-476513-r4
```

---

## 🔄 Steg 4: Oppdatere Lokale Credentials

### 4.1. Oppdatere i Windows Credential Manager

```powershell
# Anon Key
.\scripts\setup_local_supabase_anon_key.ps1

# Service Role Key
.\scripts\setup_local_supabase_service_role_key.ps1
```

### 4.2. Oppdatere Environment Variables

**PowerShell:**
```powershell
# Anon Key (kan brukes i frontend)
[System.Environment]::SetEnvironmentVariable("NEXT_PUBLIC_SUPABASE_ANON_KEY", "din_nye_anon_key", "User")

# Service Role Key (KUN server-side!)
[System.Environment]::SetEnvironmentVariable("SUPABASE_SERVICE_ROLE_KEY", "din_nye_service_role_key", "User")
```

**Bash:**
```bash
# Anon Key
export NEXT_PUBLIC_SUPABASE_ANON_KEY="din_nye_anon_key"
echo 'export NEXT_PUBLIC_SUPABASE_ANON_KEY="din_nye_anon_key"' >> ~/.bashrc

# Service Role Key (KUN server-side!)
export SUPABASE_SERVICE_ROLE_KEY="din_nye_service_role_key"
echo 'export SUPABASE_SERVICE_ROLE_KEY="din_nye_service_role_key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📱 Steg 5: Oppdatere Vercel Environment Variables

Hvis du bruker Vercel, må du også oppdatere der:

1. Gå til: https://vercel.com/noonaut-homo-lumen-resonans/navlosen-frontend/settings/environment-variables
2. Finn følgende variabler:
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Oppdater med ny anon key
   - `SUPABASE_SERVICE_ROLE_KEY` - Oppdater med ny service role key
3. Klikk "Save"
4. **Redeploy** applikasjonen for at endringene skal tre i kraft

---

## ✅ Steg 6: Verifisere Nye Nøkler

### Test Anon Key (Frontend)

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://guhtqmoxurfroailltsc.supabase.co',
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Test query
const { data, error } = await supabase
  .from('saved_jobs')
  .select('count')
  .limit(1)

if (error) {
  console.error('❌ Anon key test feilet:', error)
} else {
  console.log('✅ Anon key fungerer!')
}
```

### Test Service Role Key (Server-side)

```python
from supabase import create_client, Client

url = "https://guhtqmoxurfroailltsc.supabase.co"
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(url, key)

# Test query
response = supabase.table('saved_jobs').select("count").execute()

if response.data:
    print("✅ Service role key fungerer!")
else:
    print("❌ Service role key test feilet")
```

---

## 🛡️ Sikkerhet Best Practices

### ✅ DO:
- ✅ Lagre alle nøkler i Google Secret Manager
- ✅ Bruk Service Role Key KUN server-side
- ✅ Roter nøkler regelmessig (90 dager)
- ✅ Bruk forskjellige nøkler for development og production
- ✅ Begrens tilgang til Service Role Key (kun backend/services)

### ❌ DON'T:
- ❌ **Aldri** committ nøkler til Git
- ❌ **Aldri** eksponer Service Role Key i frontend
- ❌ **Aldri** del nøkler i dokumentasjon eller chat
- ❌ **Aldri** bruk Service Role Key i klientkode
- ❌ **Aldri** hardkode nøkler i kode

---

## 📚 Relaterte Filer

### Scripts:
- `scripts/save_supabase_anon_key_to_secret_manager.ps1`
- `scripts/save_supabase_service_role_key_to_secret_manager.ps1`
- `scripts/setup_local_supabase_anon_key.ps1`
- `scripts/setup_local_supabase_service_role_key.ps1`
- `scripts/get_supabase_keys_from_secret.py`

### Dokumentasjon:
- `docs/GOOGLE_CLOUD_PROJECT_SETUP.md` - GCP project overview
- `navlosen/frontend/VERCEL_ENV_VARIABLES.md` - Vercel environment setup
- `navlosen/supabase/README.md` - Supabase setup guide

---

**Opprettet:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)


