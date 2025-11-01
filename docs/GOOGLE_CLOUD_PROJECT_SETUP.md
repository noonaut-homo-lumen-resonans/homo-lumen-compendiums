# Google Cloud Project Setup - Homo Lumen Compendiums

**Prosjekt-ID:** `dotted-stage-476513-r4`
**Console URL:** https://console.cloud.google.com/?project=dotted-stage-476513-r4
**Status:** ✅ Aktivt produksjonsprosjekt

**Dato opprettet:** 31. oktober 2025
**Forvaltet av:** Osvald "Noonaut" Johansen
**Organisasjon:** cognitivesovereignty.network

---

## 🎯 Prosjektoversikt

Dette Google Cloud-prosjektet er den **primære sikkerhets- og infrastrukturplattformen** for Homo Lumen Compendiums-prosjektet.

**Hovedbruksområder:**
- 🔐 **Secret Manager** - Sikker lagring av API-nøkler og credentials
- ☁️ **Cloud Services** - Fremtidig deployment og hosting
- 🔍 **Audit Logging** - Sporing av hentinger og endringer
- 🛡️ **Access Control** - Fin-grained tilgangskontroll

---

## ✅ Aktive Tjenester

### Secret Manager
**Status:** ✅ Aktivert
**API:** `secretmanager.googleapis.com`

**Aktive Secrets:**
- `github-token` - GitHub Personal Access Token
  - Versjon: Latest (2)
  - Sist oppdatert: 31. oktober 2025
  - Replikasjon: Automatic
  - Bruk: Git-operasjoner og GitHub API-tilgang
  - Status: ✅ Aktivt og testet
- `notion-api-key` - Notion API-nøkkel
  - Versjon: Latest (1)
  - Sist oppdatert: 31. oktober 2025
  - Replikasjon: Automatic
  - Bruk: Notion MCP integration i Cursor IDE
  - Status: ✅ Aktivt og testet
  - Lagret også i: Windows Credential Manager (`NotionAPI:notion.so`)
- `vercel-access-token` - Vercel Access Token
  - Versjon: Latest (1)
  - Sist oppdatert: 31. oktober 2025
  - Replikasjon: Automatic
  - Bruk: Vercel VS Code extension, deployment management
  - Status: ✅ Aktivt og testet
  - Lagret også i: Windows Credential Manager (`VercelAPI:vercel.com`)
- `supabase-anon-key` - Supabase Anon Key (Public)
  - Versjon: Latest
  - Sist oppdatert: 31. oktober 2025
  - Replikasjon: Automatic
  - Bruk: Frontend/client-side Supabase operasjoner
  - Status: ✅ Aktivt og testet
  - Project: `guhtqmoxurfroailltsc`
  - ⚠️ Kan brukes i frontend (public key)
- `supabase-service-role-key` - Supabase Service Role Key (Secret)
  - Versjon: Latest
  - Sist oppdatert: (Ikke lagret ennå)
  - Replikasjon: Automatic
  - Bruk: Server-side Supabase operasjoner, bypasses RLS
  - Status: ⏳ Må lagres
  - Project: `guhtqmoxurfroailltsc`
  - ⚠️ **KRITISK:** KUN server-side! Aldri eksponer i frontend!

**Secrets som kan legges til:**
- `openai-api-key` - OpenAI API-nøkkel
- `upstash-redis-token` - Upstash Redis-token
- `clickup-api-key` - ClickUp API-nøkkel
- Andre agent API-nøkler (Lira, Nyra, Orion, etc.)

---

## 🔐 Sikkerhet og Tilgang

### Autentisering
**Aktiv bruker:** `osvald@cognitivesovereignty.network`
**Autentisert via:** `gcloud auth login`

### Service Accounts
Ikke konfigurert ennå. Se: `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md`

---

## 📋 Quick Reference

### Viktigste Commands

**Sette prosjekt:**
```bash
gcloud config set project dotted-stage-476513-r4
```

**Se alle secrets:**
```bash
gcloud secrets list
```

**Hente secret:**
```bash
gcloud secrets versions access latest --secret="github-token"
```

**Legge til nytt secret:**
```bash
echo -n "<secret_value>" | gcloud secrets create <secret-name> --data-file=-
```

**Oppdatere eksisterende secret:**
```bash
echo -n "<new_value>" | gcloud secrets versions add <secret-name> --data-file=-
```

---

## 🔗 Nettleser-tilgang

**Direct Links:**

1. **Console Dashboard:**
   https://console.cloud.google.com/?project=dotted-stage-476513-r4

2. **Secret Manager:**
   https://console.cloud.google.com/security/secret-manager?project=dotted-stage-476513-r4

3. **IAM & Admin:**
   https://console.cloud.google.com/iam-admin/iam?project=dotted-stage-476513-r4

4. **API & Services:**
   https://console.cloud.google.com/apis/dashboard?project=dotted-stage-476513-r4

5. **Billing:**
   https://console.cloud.google.com/billing?project=dotted-stage-476513-r4

---

## 💰 Kostnader

**Estimert månedlig kostnad (okt 2025):**

| Tjeneste | Kostnad |
|----------|---------|
| Secret Manager (5 secrets) | ~$0.30 (~3.50 NOK) |
| API-operasjoner (~10k/mnd) | ~$0.03 (~0.30 NOK) |
| **Total** | **~$0.33 (~3.80 NOK/mnd)** |

**⚠️ Merk:** Kostnadene kan øke hvis du legger til flere tjenester (Cloud Run, Cloud SQL, etc.)

---

## 📚 Relaterte Dokumenter

- `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md` - Komplett Secret Manager guide
- `docs/GITHUB_TOKEN_SECURE_USAGE.md` - GitHub token bruksguide
- `scripts/store_github_token_secret.py` - Script for å lagre secrets
- `scripts/get_github_token_from_secret.py` - Script for å hente secrets

---

## 🚀 Neste Steg

### Umiddelbart (High Priority)
1. ✅ **Secret Manager aktivert** - DONE
2. ✅ **GitHub token lagret** - DONE
3. ⚠️ **Rotere eksponert GitHub token** - TODO
4. ⏳ **Migrere andre API-nøkler til Secret Manager** - TODO

### Fremtidige Forbedringer
- [ ] Opprette service account for automatisert tilgang
- [ ] Sette opp Workload Identity Federation for GitHub Actions
- [ ] Konfigurere audit logging og alerts
- [ ] Opprette backup-strategi for secrets
- [ ] Dokumentere alle aktive secrets i prosjektet

---

## 🛡️ Best Practices

1. **✅ DO:**
   - Bruk Secret Manager for ALL sensitive data
   - Roter secrets regelmessig (90 dager)
   - Bruk minst nødvendig tilgang (principle of least privilege)
   - Logg alle secret-hentinger for audit

2. **❌ DON'T:**
   - Ikke hardkode credentials i kode
   - Ikke committ secrets til Git
   - Ikke del secrets i dokumentasjon eller chat
   - Ikke gi unødvendige tilganger til service accounts

---

## 📞 Support

**Spørsmål eller problemer?**
- Sjekk: `docs/GOOGLE_SECRET_MANAGER_QUICK_START.md` (Feilsøking-seksjon)
- Google Cloud Support: https://cloud.google.com/support
- Secret Manager Docs: https://cloud.google.com/secret-manager/docs

---

**Opprettet:** 31. oktober 2025
**Sist oppdatert:** 31. oktober 2025
**Forfatter:** Auto (AI Assistant)
**Status:** ✅ Aktivt prosjekt

