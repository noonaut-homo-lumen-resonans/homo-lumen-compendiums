# NAV Arbeidsplassen.no API Søknad

## E-post utkast til nav.team.arbeidsplassen@nav.no

---

**Emne:** Søknad om API-tilgang til Arbeidsplassen.no for NAV-Losen prosjekt

---

Hei NAV Arbeidsplassen-teamet,

Jeg henvender meg for å søke om tilgang til Arbeidsplassen.no Public Feed API for et prosjekt som heter **NAV-Losen**.

### Om prosjektet

NAV-Losen er en bevissthetsbasert teknologiplattform utviklet for å hjelpe NAV-brukere med å finne relevant arbeid tilpasset deres biofeltprofil og stressnivå. Prosjektet er del av et større økosystem kalt "Homo Lumen" som fokuserer på stressresponsiv teknologi og bevissthetsorientert veiledning.

**Hovedfunksjoner:**
- Jobbsøk med sanntids filtrering og kategorisering
- AI-drevet karriereveiledning (chatbot "Lira")
- CV-bygging og søknadsassistanse
- Integrering med brukerens stressnivå og energimålinger (HRV/biofelt)
- Gmail-integrering for enkel jobbsøknad

### Teknisk implementering

**Plattform:** Next.js 14 (React/TypeScript)
**Deployment:** Netlify / Vercel (planlagt)
**Backend:** FastAPI (Python) for AI-agenter
**Brukerbase:** NAV-brukere i jobbsøkerprosess (estimert 100-500 brukere i pilotfase)

**API-bruk:**
- Hente jobbannonser basert på søkeord og filtre
- Sanntids søk med paginering
- Kategorisering etter STYRK08
- Geografisk filtrering
- Utløpsdato og publiseringsdato

**Forventet trafikkvolum:**
- Ca. 500-1000 API-kall per dag i pilotfase
- Caching implementert for å redusere unødvendige kall
- Ingen automatisert scraping eller masseinnhenting

### Sikkerhet og personvern

- API-nøkkel lagres i miljøvariabler (`.env.local`)
- Ingen videreformidling av data til tredjeparter
- GDPR-kompatibel brukerdata-håndtering
- Ingen lagring av personlige søkedata

### Kontaktinformasjon

**Prosjekt:** NAV-Losen (Homo Lumen)
**Utvikler:** Osvald Nigon
**E-post:** [DIN E-POST]
**GitHub:** [GITHUB REPO HVIS AKTUELT]
**Formål:** Ikke-kommersiell pilot for NAV-brukere

### Dokumentasjon

Jeg har lest gjennom API-dokumentasjonen på:
- https://navikt.github.io/pam-stilling-feed/
- https://arbeidsplassen.api.no/swagger-ui/

Jeg forstår at API-nøkkelen må behandles konfidensielt og at misbruk kan føre til at tilgangen trekkes tilbake.

### Ønsket API-tilgang

- **API:** Arbeidsplassen.no Public Feed API
- **Endpoints:** `/public-feed/api/v1/ads` (primært)
- **Rate limit:** Standard tilgang (kan diskuteres)
- **Formål:** Ikke-kommersiell pilot

Jeg setter stor pris på om dere kan vurdere denne søknaden. Hvis dere trenger mer informasjon eller har spørsmål om prosjektet, er jeg mer enn gjerne tilgjengelig for dialog.

Med vennlig hilsen,
Osvald Nigon

---

## Informasjon NAV trenger

Når du sender denne e-posten, vær forberedt på å kunne svare på følgende:

### Teknisk informasjon
- [ ] Prosjektets formål og målgruppe
- [ ] Estimert antall brukere
- [ ] Forventet API-trafikkvolum
- [ ] Teknisk stack (Next.js, React, TypeScript)
- [ ] Deployment-plattform (Netlify/Vercel)
- [ ] Hvordan API-nøkkelen beskyttes

### Juridisk/GDPR
- [ ] Personvernserklæring (hvis aktuelt)
- [ ] Brukervilkår for tjenesten
- [ ] Hvordan brukerdata håndteres
- [ ] Om data lagres eller videregis

### Prosjektinformasjon
- [ ] Prosjektets varighet (pilot vs. permanent)
- [ ] Om prosjektet er kommersiell eller ikke
- [ ] Eventuelle partnere eller samarbeidspartnere
- [ ] Kontaktinformasjon for prosjektleder

### Sikkerhet
- [ ] Hvordan API-nøkkelen lagres (miljøvariabler)
- [ ] Om det er implementert caching
- [ ] Hvordan du unngår misbruk/scraping
- [ ] Om du har implementert rate limiting på klientsiden

---

## Neste steg

1. **Tilpass e-posten** med din egen kontaktinformasjon
2. **Vurder om du vil dele GitHub-repo** (kan styrke søknaden)
3. **Legg ved screenshot** av NAV-Losen jobbsøk hvis ønskelig
4. **Send til:** nav.team.arbeidsplassen@nav.no
5. **Forventet responstid:** 1-2 uker (basert på NAV sine dokumenter)

---

## Alternativer mens du venter

Hvis du vil teste funksjonaliteten mens du venter på API-tilgang:

### 1. Bruk mock data (allerede implementert)
```bash
# Frontend bruker automatisk mock data hvis API-nøkkel mangler
npm run dev
```

### 2. Test med offentlig data
Arbeidsplassen.no har noen åpne endepunkter uten API-nøkkel:
```bash
curl "https://arbeidsplassen.nav.no/public-feed/api/v1/categories"
```

### 3. Scraping som siste utvei
Hvis API-tilgang nektes, kan du vurdere legal web scraping av arbeidsplassen.no (respekter robots.txt).

---

**Lykke til med søknaden!** 🚀
