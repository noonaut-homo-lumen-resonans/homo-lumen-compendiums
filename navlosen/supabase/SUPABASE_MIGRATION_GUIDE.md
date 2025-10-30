# Supabase SQL-Migration Guide
**For:** NAV-Losen Job Search Database Setup

---

## Steg 1: Åpne Supabase Dashboard

1. Gå til: https://guhtqmoxurfroailltsc.supabase.co
2. Logg inn med din Supabase-konto

---

## Steg 2: Naviger til SQL Editor

1. Se på venstre sidebar
2. Klikk på **"SQL Editor"** (har et database-ikon)
3. Du vil se en liste over tidligere queries

---

## Steg 3: Åpne SQL-filen som skal kjøres

1. Åpne filen på din datamaskin:
   ```
   c:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\navlosen\supabase\migrations\001_create_job_tables.sql
   ```

2. Merk alt innhold (Ctrl+A) og kopier (Ctrl+C)

---

## Steg 4: Opprett ny SQL Query

1. I Supabase SQL Editor, klikk **"New query"** (øverst til høyre)
2. Gi den et navn: "NAV Jobs Migration"
3. Lim inn hele SQL-innholdet fra filen (Ctrl+V)

---

## Steg 5: Kjør SQL-migrasjonen

1. Klikk **"Run"** knappen (eller trykk Ctrl+Enter)
2. Vent mens SQL-en kjører (tar ca. 5-10 sekunder)
3. Du skal se:
   ```
   Success. No rows returned
   ```

---

## Steg 6: Verifiser at tabellene ble opprettet

Kjør denne SQL-en i en ny query:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('saved_jobs', 'job_alerts', 'application_history');
```

Du skal se 3 rader:
- `saved_jobs`
- `job_alerts`
- `application_history`

---

## Steg 7: Sjekk Row Level Security (RLS)

Kjør denne SQL-en:

```sql
SELECT tablename, policyname
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('saved_jobs', 'job_alerts', 'application_history');
```

Du skal se 12 policies (4 per tabell):
- Users can view own [table]
- Users can insert own [table]
- Users can update own [table]
- Users can delete own [table]

---

## Steg 8: Test database-tilkobling fra frontend

Kjør denne koden i din Next.js app (f.eks. i en test-side):

```typescript
import { supabase } from '@/lib/supabase'

// Test query
const { data, error } = await supabase
  .from('saved_jobs')
  .select('*')
  .limit(1)

if (error) {
  console.error('Supabase error:', error)
} else {
  console.log('Supabase connection successful! Data:', data)
}
```

Hvis det fungerer, vil du se:
```
Supabase connection successful! Data: []
```

(Array er tom fordi vi ikke har data ennå)

---

## Feilsøking

### Problem 1: "permission denied for schema public"

**Løsning:** Kjør disse kommandoene:

```sql
GRANT USAGE ON SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO postgres, anon, authenticated, service_role;
```

### Problem 2: "relation already exists"

**Løsning:** Tabellene er allerede opprettet. Du kan droppe dem og kjøre på nytt:

```sql
DROP TABLE IF EXISTS saved_jobs CASCADE;
DROP TABLE IF EXISTS job_alerts CASCADE;
DROP TABLE IF EXISTS application_history CASCADE;
```

Deretter kjør migrasjonen på nytt.

### Problem 3: "function uuid_generate_v4() does not exist"

**Løsning:** UUID-extension mangler. Kjør:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Problem 4: "Cannot connect to Supabase from frontend"

**Sjekkliste:**
- [ ] Er `NEXT_PUBLIC_SUPABASE_URL` satt i `.env.local`?
- [ ] Er `NEXT_PUBLIC_SUPABASE_ANON_KEY` satt i `.env.local`?
- [ ] Er Next.js server restartet etter å ha lagt til env vars?
- [ ] Er `@supabase/supabase-js` installert? (`npm list @supabase/supabase-js`)

---

## Neste Steg

Etter at migrasjonen er kjørt:

1. ✅ Test tilkobling fra frontend
2. ✅ Implementer BookmarkButton-komponent
3. ✅ Test lagring av jobber
4. ✅ Implementer "Mine lagrede jobber"-side

---

## Nyttige SQL-queries for testing

### Se alle lagrede jobber (for en bruker)

```sql
SELECT * FROM saved_jobs
WHERE user_id = 'YOUR_USER_ID'
ORDER BY saved_at DESC;
```

### Slett alle lagrede jobber (for testing)

```sql
DELETE FROM saved_jobs WHERE user_id = 'YOUR_USER_ID';
```

### Se statistikk

```sql
SELECT * FROM v_user_job_stats WHERE user_id = 'YOUR_USER_ID';
```

### Se nylige lagrede jobber med søknadsstatus

```sql
SELECT * FROM v_recent_saved_jobs WHERE user_id = 'YOUR_USER_ID';
```

---

**Lykke til!** 🚀

Hvis du får problemer, sjekk dokumentasjonen i `supabase/README.md`.
