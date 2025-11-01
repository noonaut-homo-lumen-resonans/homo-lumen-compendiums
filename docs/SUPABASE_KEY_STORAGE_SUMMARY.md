# Supabase Key Storage Summary

**Dato:** 31. oktober 2025
**Project Reference:** `guhtqmoxurfroailltsc`

---

## 📋 Oversikt

Supabase nøkler er lagret i **Google Secret Manager** for sikker produksjonslagring.

---

## 🔐 Lagrede Nøkler

### 1. Anon Key (Public) ✅

**Secret Name:** `supabase-anon-key`
**Location:** Google Secret Manager (Project: `dotted-stage-476513-r4`)
**Status:** ✅ Lagret og testet

**Bruk:**
- Frontend/client-side operasjoner
- Kan eksponeres i klientkode (public key)
- Brukes i `NEXT_PUBLIC_SUPABASE_ANON_KEY` environment variable

**Hent nøkkel:**
```powershell
# PowerShell
python scripts/get_supabase_keys_from_secret.py --type anon

# Eller via gcloud
gcloud secrets versions access latest --secret="supabase-anon-key" --project="dotted-stage-476513-r4"
```

---

### 2. Service Role Key (Secret) ⏳

**Secret Name:** `supabase-service-role-key`
**Location:** Google Secret Manager (Project: `dotted-stage-476513-r4`)
**Status:** ⏳ Må lagres (script klar)

**⚠️ SIKKERHET:**
- Har FULL tilgang til databasen
- Bypasser Row Level Security (RLS)
- **ALDRI eksponer i frontend eller klientkode!**
- Bruk KUN server-side!

**Lagre nøkkel:**
```powershell
.\scripts\save_supabase_service_role_key_to_secret_manager.ps1
```

**Hent nøkkel:**
```powershell
# PowerShell
python scripts/get_supabase_keys_from_secret.py --type service-role

# Eller via gcloud
gcloud secrets versions access latest --secret="supabase-service-role-key" --project="dotted-stage-476513-r4"
```

---

## 🌐 Supabase MCP Configuration

**MCP Server:** Supabase MCP
**Location:** `C:\Users\onigo\.cursor\mcp.json`
**Status:** ✅ Konfigurert og fungerer

**Konfigurasjon:**
```json
{
  "supabase": {
    "url": "https://mcp.supabase.com/mcp?project_ref=guhtqmoxurfroailltsc",
    "headers": {}
  }
}
```

**Test:**
- ✅ MCP tilkobling fungerer
- ✅ Kan liste tabeller (`saved_jobs`, `job_alerts`, `application_history`)
- ✅ Kan utføre database-operasjoner via MCP

---

## 📁 Relaterte Filer

### Scripts:
- `scripts/save_supabase_anon_key_to_secret_manager.ps1` - Lagre anon key
- `scripts/save_supabase_service_role_key_to_secret_manager.ps1` - Lagre service role key
- `scripts/get_supabase_keys_from_secret.py` - Hent nøkler fra Secret Manager
- `scripts/setup_local_supabase_anon_key.ps1` - Lagre anon key lokalt (TODO)
- `scripts/setup_local_supabase_service_role_key.ps1` - Lagre service role key lokalt (TODO)

### Dokumentasjon:
- `docs/SUPABASE_KEY_ROTATION_GUIDE.md` - Komplett guide for key rotation
- `docs/GOOGLE_CLOUD_PROJECT_SETUP.md` - GCP project overview
- `navlosen/frontend/VERCEL_ENV_VARIABLES.md` - Vercel environment setup

---

## 🚀 Neste Steg

### Umiddelbart:
1. ✅ Anon Key lagret i Secret Manager
2. ⏳ Lagre Service Role Key i Secret Manager
   - Kjør: `.\scripts\save_supabase_service_role_key_to_secret_manager.ps1`
3. ⏳ Teste Service Role Key (server-side)

### Fremtidig:
- [ ] Lagre nøkler lokalt i Windows Credential Manager for utvikling
- [ ] Oppdatere Vercel environment variables hvis nødvendig
- [ ] Roter nøkler regelmessig (90 dager)

---

## 🛡️ Sikkerhet Best Practices

### ✅ DO:
- ✅ Lagre alle nøkler i Google Secret Manager
- ✅ Bruk Service Role Key KUN server-side
- ✅ Roter nøkler regelmessig (90 dager)
- ✅ Test nye nøkler før rotasjon

### ❌ DON'T:
- ❌ **Aldri** committ nøkler til Git
- ❌ **Aldri** eksponer Service Role Key i frontend
- ❌ **Aldri** del nøkler i dokumentasjon eller chat
- ❌ **Aldri** hardkode nøkler i kode

---

**Opprettet:** 31. oktober 2025
**Status:** ✅ Anon Key lagret, ⏳ Service Role Key må lagres


