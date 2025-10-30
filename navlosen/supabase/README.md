# Supabase Setup for NAV-Losen

## Oversikt

Denne mappen inneholder database-migrations for NAV-Losen jobbsøk-funksjonalitet.

---

## Steg 1: Kjør SQL Migration

1. Gå til din Supabase dashboard: https://guhtqmoxurfroailltsc.supabase.co
2. Klikk på "SQL Editor" i venstre meny
3. Klikk "New query"
4. Kopier hele innholdet fra `migrations/001_create_job_tables.sql`
5. Lim inn i SQL-editoren
6. Klikk "Run" (eller Ctrl+Enter)

Du skal se følgende tabeller opprettet:
- `saved_jobs` - Lagrede jobber
- `job_alerts` - Jobbvarsler
- `application_history` - Søknadshistorikk

**Verifiser at tabellene ble opprettet:**
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('saved_jobs', 'job_alerts', 'application_history');
```

---

## Steg 2: Konfigurer Frontend

### A. Opprett .env.local

Opprett filen `navlosen/frontend/.env.local` med følgende innhold:

```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://guhtqmoxurfroailltsc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1aHRxbW94dXJmcm9haWxsdHNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwNDQzMjIsImV4cCI6MjA3NjYyMDMyMn0.0W2H_BaS8wRYz5DS8FwrCbvILB7cB5QyZi40oO7VDRk

# Arbeidsplassen.no API (når du får API-nøkkel fra NAV)
# ARBEIDSPLASSEN_API_KEY=your_api_key_here

# Google OAuth (hvis du har satt opp Google Cloud)
# GOOGLE_CLIENT_ID=your_google_client_id
# GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### B. Installer Supabase Client

```bash
cd navlosen/frontend
npm install @supabase/supabase-js
```

---

## Steg 3: Test Supabase-tilkobling

Kjør denne koden i din frontend for å teste tilkobling:

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Test query
const { data, error } = await supabase
  .from('saved_jobs')
  .select('*')
  .limit(10)

if (error) {
  console.error('Supabase error:', error)
} else {
  console.log('Supabase connection successful:', data)
}
```

---

## Database Schema

### saved_jobs
Lagrer jobber som brukeren har bookmarket.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Referanse til auth.users |
| job_id | VARCHAR(255) | ID fra Arbeidsplassen.no |
| job_title | VARCHAR(500) | Stillingstittel |
| company_name | VARCHAR(500) | Bedriftsnavn |
| location | VARCHAR(255) | Geografisk plassering |
| saved_at | TIMESTAMP | Når jobben ble lagret |
| notes | TEXT | Brukernotater |
| application_status | VARCHAR(50) | Status: not_applied, applied, interview, rejected, accepted |
| tags | TEXT[] | Bruker-definerte tags |
| job_data | JSONB | Full jobbdata fra API |

### job_alerts
Brukerens jobbvarsler for nye stillinger.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Referanse til auth.users |
| name | VARCHAR(255) | Navn på varselet |
| search_criteria | JSONB | Søkekriterier (keywords, location, etc.) |
| frequency | VARCHAR(20) | realtime, daily, weekly |
| active | BOOLEAN | Om varselet er aktivt |
| last_sent_at | TIMESTAMP | Siste gang varselet ble sendt |
| created_at | TIMESTAMP | Opprettelsestidspunkt |

### application_history
Sporing av jobbsøknader.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Referanse til auth.users |
| job_id | VARCHAR(255) | ID fra Arbeidsplassen.no |
| company | VARCHAR(255) | Bedriftsnavn |
| position | VARCHAR(255) | Stillingstittel |
| applied_at | TIMESTAMP | Søknadsdato |
| status | VARCHAR(50) | Status: applied, viewed, interview_scheduled, etc. |
| notes | TEXT | Brukernotater |
| interview_date | TIMESTAMP | Intervjudato (hvis aktuelt) |
| response_date | TIMESTAMP | Dato for svar fra arbeidsgiver |
| application_method | VARCHAR(50) | gmail, email, website, in_person |
| email_thread_id | VARCHAR(255) | Gmail thread ID |

---

## Row Level Security (RLS)

Alle tabeller har RLS aktivert, som betyr:
- Brukere kan kun se sine egne data
- Brukere kan kun endre sine egne data
- Ingen kan se andres lagrede jobber, varsler eller søknadshistorikk

Dette sikres automatisk av Supabase via PostgreSQL RLS-policies.

---

## API Endpoints (Next.js API Routes)

Etter at tabellene er opprettet, kan du bruke disse API-endepunktene:

### Lagre jobb
```typescript
POST /api/jobs/save
{
  "jobId": "mock-1",
  "jobTitle": "Helsefagarbeider",
  "companyName": "Oslo Kommune",
  "location": "Oslo",
  "notes": "Interessant stilling",
  "tags": ["helse", "prioritet"]
}
```

### Hent lagrede jobber
```typescript
GET /api/jobs/saved
```

### Oppdater søknadsstatus
```typescript
PATCH /api/jobs/saved/:id
{
  "applicationStatus": "applied"
}
```

### Slett lagret jobb
```typescript
DELETE /api/jobs/saved/:id
```

---

## Views

### v_recent_saved_jobs
Nylige lagrede jobber med søknadsstatus.

```sql
SELECT * FROM v_recent_saved_jobs LIMIT 10;
```

### v_user_job_stats
Brukerstatistikk for jobbsøk.

```sql
SELECT * FROM v_user_job_stats WHERE user_id = 'YOUR_USER_ID';
```

---

## Feilsøking

### Problem: "relation does not exist"
**Løsning:** Kjør SQL-migrasjonen på nytt i SQL Editor.

### Problem: "Row Level Security policy violation"
**Løsning:** Sjekk at du er innlogget og at `auth.uid()` returnerer din user ID.

### Problem: "permission denied for table"
**Løsning:** Kjør GRANT-kommandoene på slutten av migrasjonen.

### Problem: Kan ikke koble til Supabase
**Løsning:** Verifiser at NEXT_PUBLIC_SUPABASE_URL og NEXT_PUBLIC_SUPABASE_ANON_KEY er riktig satt i .env.local.

---

## Neste Steg

1. ✅ Kjør SQL-migration
2. ✅ Konfigurer .env.local
3. ✅ Installer @supabase/supabase-js
4. ⏳ Implementer frontend-komponenter (bookmark-knapp, lagrede jobber-side)
5. ⏳ Test full flyt (lagre jobb → se lagrede jobber → oppdater status)

---

**Dokumentet sist oppdatert:** 30. oktober 2025
