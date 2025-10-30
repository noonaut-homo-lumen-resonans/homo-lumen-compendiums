# Jobbsøk Forbedringer - NAV-Losen

## Oversikt

Dette dokumentet beskriver forbedringene som skal implementeres for "Finn din neste jobb"-funksjonen.

---

## 1. Avanserte Filtre

### Eksisterende filtre
- ✅ Søkeord (tekst)
- ✅ Kategori (Alle, Helse, Service, Teknologi, Håndverk, Kontor)

### Nye filtre som skal legges til

#### A. Geografi
- **Fylke-velger** (dropdown med alle fylker)
- **Kommune-søk** (autocomplete)
- **Geografisk radius** (f.eks. "innen 50 km fra Oslo")
- **Hjemmekontor-mulighet** (toggle)

#### B. Stillingsstørrelse
- **Heltid** (100%)
- **Deltid** (50-99%)
- **Tilkalling** (<50%)
- **Prosjektbasert**

#### C. Erfaring
- **Ingen erfaring** (for nyutdannede)
- **1-3 år erfaring**
- **3-5 år erfaring**
- **5+ år erfaring**

#### D. Ansettelsestype
- **Fast ansettelse**
- **Midlertidig**
- **Vikariat**
- **Sesongarbeid**

#### E. Søknadsfrist
- **I dag** (søknadsfrist i dag)
- **Denne uken** (frist innen 7 dager)
- **Denne måneden** (frist innen 30 dager)
- **Har tid** (frist >30 dager)

---

## 2. Bookmark/Lagringsfunksjon

### Funksjonalitet
- **"Lagre jobb"-knapp** på hver jobbannonse (hjerte-ikon)
- **Lokal lagring** (localStorage) før bruker logger inn
- **Synkronisering** til Supabase når bruker logger inn
- **"Mine lagrede jobber"-side** (egen seksjon)

### Datamodell
```typescript
interface SavedJob {
  id: string;
  jobId: string;
  userId: string;
  savedAt: Date;
  notes?: string;
  applicationStatus: 'not_applied' | 'applied' | 'interview' | 'rejected' | 'accepted';
  tags: string[];
}
```

### Filtrering på lagrede jobber
- **Ikke søkt** (lagret, men ikke sendt søknad)
- **Søkt** (søknad sendt)
- **Intervju** (kalt inn til intervju)
- **Avslag** (fått avslag)
- **Tilbud** (fått jobbtilbud)

---

## 3. Jobbvarsler/Notifications

### Typer varsler
1. **Nye jobber** - Varsle når nye jobber matcher brukerens kriterier
2. **Søknadsfrist** - Varsle 3 dager og 1 dag før søknadsfrist
3. **Jobbanbefaling** - Lira anbefaler relevante jobber

### Varslings-kanaler
- **E-post** (daglig/ukentlig digest)
- **Push-notifications** (mobile/desktop)
- **In-app** (varselsikon i header)

### Datamodell
```typescript
interface JobAlert {
  id: string;
  userId: string;
  name: string;
  searchCriteria: {
    keywords: string[];
    categories: string[];
    locations: string[];
    jobTypes: string[];
  };
  frequency: 'realtime' | 'daily' | 'weekly';
  active: boolean;
  createdAt: Date;
}
```

---

## 4. Forbedret Søkerelevans

### A. Sorteringsalternativer
- **Mest relevant** (standard - basert på søkeord match)
- **Nyeste først** (nylig publisert)
- **Frist nærmest** (søknadsfrist snart)
- **Nærmest meg** (geografisk avstand)
- **Lira-anbefaling** (AI-kurert basert på profil)

### B. Match-score
Hvert søkeresultat får en "match score" (0-100%) basert på:
- **Søkeord-match** (30%)
- **Kategori-match** (20%)
- **Geografi-match** (15%)
- **Erfaring-match** (15%)
- **Bruker-preferanser** (20%)

Visualiseres som:
```
[████████░░] 80% match
```

### C. "Hvorfor denne jobben?"-forklaring
Under hver jobbannonse:
> ✨ **Passer deg fordi:**
> - Du har tidligere søkt på "helsefagarbeider"
> - Ligger nær din bostedsadresse
> - Matcher ditt erfaringsnivå

---

## 5. Lira Chatbot-integrasjon

### Konversasjonsflyt

#### Steg 1: Bruker spør Lira om karriere
```
Bruker: "Jeg vet ikke hvilken jobb jeg skal søke på"
Lira: "La meg hjelpe deg! Hvilke interesser har du?"
```

#### Steg 2: Lira kartlegger profil
- **Interesser** (helse, teknologi, kreativt, etc.)
- **Erfaring** (år i arbeidslivet, tidligere roller)
- **Utdanning** (høyeste fullførte utdanning)
- **Preferanser** (geografisk, stillingsstørrelse, fleksibilitet)
- **Livssituasjon** (familie, bosted, helse)

#### Steg 3: Lira anbefaler konkrete jobber
```
Lira: "Basert på din bakgrunn anbefaler jeg disse 5 jobbene:"
1. Helsefagarbeider hos Oslo Kommune (90% match)
2. Sykepleier hos Haukeland Sykehus (85% match)
...

[Knapp: Se alle anbefalinger]
```

#### Steg 4: Lira hjelper med søknad
```
Bruker: "Hjelp meg å søke på jobb #1"
Lira: "Flott valg! Skal jeg hjelpe deg med CV og søknadsbrev?"

[Knapp: Ja, hjelp meg med CV]
[Knapp: Nei, bare send søknad]
```

### Teknisk integrasjon
- **Lira API-endepunkt**: `POST /api/lira/job-recommendations`
- **Bruker-profil**: Hentet fra Supabase
- **Jobber**: Hentet fra Arbeidsplassen.no API
- **AI-matching**: OpenAI GPT-4 for matching og forklaring

---

## 6. CV-Matching

### Funksjonalitet
Hvis bruker har lastet opp CV til NAV-Losen:
- **Automatisk CV-analyse** (OpenAI)
- **Skill-extraction** (programmer, språk, sertifiseringer)
- **Match-score** for hver jobb basert på CV
- **Gap-analyse** ("Du mangler erfaring med X")

### Visuell feedback
```
┌─────────────────────────────────────┐
│ Helsefagarbeider hos Oslo Kommune   │
├─────────────────────────────────────┤
│ 🟢 Dine styrker:                    │
│ ✓ Helsefagarbeider-autorisasjon     │
│ ✓ 3 års erfaring i hjemmetjeneste   │
│ ✓ Førerkort klasse B                │
│                                     │
│ 🟡 Ønskelig, men ikke påkrevd:     │
│ • Kurs i legemiddelhåndtering       │
│ • Erfaring med demens               │
│                                     │
│ [Søk likevel] [Forbedre CV først]  │
└─────────────────────────────────────┘
```

---

## 7. Søknadshistorikk

### Funksjonalitet
- **Sporing av sendte søknader** (via Gmail API)
- **Status-oppdatering** manuelt eller automatisk
- **Tidslinjevisning** av søknadsprosessen
- **Påminnelser** om oppfølging

### Eksempel-visning
```
📧 Helsefagarbeider hos Oslo Kommune
   ├─ 20. okt: Søknad sendt
   ├─ 25. okt: Avvist (mangler krav)
   └─ Ferdig

📧 Sykepleier hos Haukeland Sykehus
   ├─ 22. okt: Søknad sendt
   ├─ 28. okt: Kalt inn til intervju (3. nov kl 10:00)
   └─ Venter på svar

📧 Butikkmedarbeider hos Rema 1000
   ├─ 24. okt: Søknad sendt
   └─ Ingen respons (send påminnelse?)
```

---

## 8. Forbedret UI/UX

### A. Jobb-kort redesign
- **Større thumbnail** (bedriftslogo hvis tilgjengelig)
- **Match-score visuelt** (progress bar)
- **Quick actions** (lagre, søk, del)
- **Tags** (hjemmekontor, fleksibel arbeidstid, etc.)

### B. Kompakt list-visning
Toggle mellom:
- **Kort-visning** (stor, detaljert)
- **Liste-visning** (kompakt, raskere skanning)
- **Tabell-visning** (sortérbar)

### C. Mobil-optimalisering
- **Swipe-gester** (swipe høyre = lagre, swipe venstre = se neste)
- **Filter-drawer** (slide inn fra høyre)
- **"Søk nå"-knapp** alltid synlig (sticky)

---

## 9. Statistikk og Innsikt

### Dashboard for jobbsøker
```
┌─────────────────────────────────────┐
│ Din jobbsøkerstatistikk             │
├─────────────────────────────────────┤
│ Søknader sendt: 12                  │
│ Intervjuer: 3                       │
│ Tilbud: 1                           │
│ Gj.snitt responstid: 8 dager        │
│                                     │
│ Mest populære kategorier:           │
│ 🏥 Helse (5 søknader)               │
│ 🛒 Service (4 søknader)             │
│ 💻 Teknologi (3 søknader)           │
│                                     │
│ Tips:                               │
│ • Du får flest svar på helsejobber  │
│ • Prøv å søke på flere teknologi-   │
│   stillinger (høy etterspørsel)     │
└─────────────────────────────────────┘
```

---

## 10. Sosiale Funksjoner (fremtidig)

### Jobbdeling
- **Del jobb** til venner/familie via e-post eller sosiale medier
- **"Kjente i bedriften"**-visning (hvis integrasjon med LinkedIn)

### Anmeldelser
- **Bedriftsanmeldelser** (Glassdoor-lignende)
- **"Tidligere NAV-brukere jobber her"**-badge

---

## Implementeringsprioritet

### Fase 1 (Høy prioritet - 1-2 uker)
1. ✅ Avanserte filtre (geografi, stillingsstørrelse, erfaring)
2. ✅ Bookmark/lagring-funksjon
3. ✅ Forbedret UI (match-score, sortering)

### Fase 2 (Medium prioritet - 2-4 uker)
4. ✅ Jobbvarsler (e-post)
5. ✅ Lira-integrasjon (jobbanbefaling)
6. ✅ Søknadshistorikk

### Fase 3 (Lav prioritet - 4+ uker)
7. ⏳ CV-matching med AI
8. ⏳ Statistikk og innsikt
9. ⏳ Sosiale funksjoner

---

## Teknisk Stack

### Frontend
- **React/Next.js** (allerede implementert)
- **Tailwind CSS** (styling)
- **React Hook Form** (filter-håndtering)
- **Zustand/Redux** (state management for lagrede jobber)

### Backend
- **Next.js API Routes** (middleware)
- **Supabase** (database for lagrede jobber, varsler, søknadshistorikk)
- **Arbeidsplassen.no API** (jobbdata)
- **OpenAI API** (CV-matching, Lira-anbefalinger)
- **Gmail API** (søknadssending, sporing)

### Database Schema (Supabase)
```sql
-- Saved Jobs
CREATE TABLE saved_jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  job_id VARCHAR(255) NOT NULL,
  saved_at TIMESTAMP DEFAULT NOW(),
  notes TEXT,
  application_status VARCHAR(50),
  tags TEXT[],
  UNIQUE(user_id, job_id)
);

-- Job Alerts
CREATE TABLE job_alerts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  name VARCHAR(255) NOT NULL,
  search_criteria JSONB NOT NULL,
  frequency VARCHAR(20) NOT NULL,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Application History
CREATE TABLE application_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  job_id VARCHAR(255) NOT NULL,
  company VARCHAR(255),
  position VARCHAR(255),
  applied_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50),
  notes TEXT,
  interview_date TIMESTAMP,
  response_date TIMESTAMP
);
```

---

## Neste Steg

1. **Implementer Fase 1-features** (avanserte filtre + bookmarks)
2. **Test med reell Arbeidsplassen.no API** (når API-nøkkel er klar)
3. **Integrer med Lira** for jobbanbefaling
4. **Sett opp Supabase-database**
5. **Deploy til produksjon** (Netlify/Vercel)

---

**Dokumentet sist oppdatert:** 30. oktober 2025
