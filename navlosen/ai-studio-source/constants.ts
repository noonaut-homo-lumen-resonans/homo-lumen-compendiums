
import { Guide, Document, Reminder, NavCase, MasteryFeeling, MasteryStrategy, JobPosting, JobApplication } from './types';

export const APP_NAME = "NAV-Losen";

export const APP_ROUTES = {
  DASHBOARD: "/dashboard",
  GUIDES: "/veiledninger",
  EXPLAIN_LETTER: "/forklar-brev",
  CHATBOT: "/chatbot",
  DOCUMENTS: "/dokumenter",
  REMINDERS: "/påminnelser",
  RIGHTS: "/rettigheter",
  SETTINGS: "/innstillinger",
  MASTERY: "/mestring",
  JOB: "/jobb",
};

export const MOCK_GUIDES: Guide[] = [
  {
    id: 'dagpenger',
    title: 'Slik søker du dagpenger (steg for steg)',
    summary: 'En komplett guide til hvordan du søker om dagpenger ved arbeidsledighet.',
    category: 'Arbeidsledighet',
    timeEstimate: 'Ca. 30 minutter',
    requirements: 'BankID, oppsigelse/permitteringsvarsel, arbeidsavtaler, lønnsslipper.',
    content: `
# Dagpenger ved arbeidsledighet

Denne veiledningen hjelper deg gjennom prosessen med å søke dagpenger fra NAV.

## Hvem kan få dagpenger?
For å ha rett til dagpenger må du som hovedregel:
- Ha mistet minst 50 % av arbeidstiden din.
- Ha hatt en minsteinntekt på minst 1,5 G (grunnbeløpet i folketrygden) de siste 12 månedene, eller minst 3 G de siste 36 månedene.
- Være reell arbeidssøker og registrert hos NAV.
- Oppholde deg i Norge.

## Slik søker du
1.  **Registrer deg som arbeidssøker:** Dette gjør du på nav.no.
2.  **Søk om dagpenger:** Søknaden sender du digitalt via nav.no. Ha nødvendig dokumentasjon klar.
3.  **Send meldekort:** Du må sende meldekort hver 14. dag så lenge du er arbeidssøker.

## Nødvendig dokumentasjon
- Arbeidsavtaler og oppsigelse/permitteringsvarsel.
- Lønnslipper eller annen dokumentasjon på inntekt.
- Eventuelle vitnemål eller kursbevis.

**Merk:** Dette er en forenklet veiledning. For fullstendig og oppdatert informasjon, se alltid [nav.no](https://nav.no). NAV-Losen gir veiledende informasjon og erstatter ikke offisiell rådgivning fra NAV.
    `,
    lastUpdated: '2024-05-15',
  },
  {
    id: 'sykepenger',
    title: 'Slik fungerer sykepenger (steg for steg)',
    summary: 'Informasjon om rettigheter og prosessen for å motta sykepenger ved sykdom.',
    category: 'Sykdom',
    timeEstimate: 'Ca. 15 minutter',
    requirements: 'Sykmelding fra lege, BankID for å sende digital søknad.',
    content: `
# Sykepenger ved sykdom

Denne veiledningen gir deg en oversikt over sykepengeordningen.

## Hvem kan få sykepenger?
For å ha rett til sykepenger må du:
- Være arbeidsufør på grunn av sykdom eller skade.
- Ha vært i arbeid i minst fire uker umiddelbart før du ble syk (opptjeningstid).
- Tape pensjonsgivende inntekt på grunn av arbeidsuførheten.

## Hvordan fungerer det?
- **Egenmelding:** Du kan bruke egenmelding for kortere fravær (vanligvis opptil 3 dager).
- **Sykmelding:** For lengre fravær trenger du sykmelding fra lege.
- **Søknad om sykepenger:** Du sender digital søknad om sykepenger på nav.no etter at sykmeldingsperioden er over.
- **Arbeidsgiverperioden:** Arbeidsgiver betaler vanligvis sykepenger de første 16 kalenderdagene. Deretter overtar NAV.

## Viktig å huske på
- Lever sykmeldingen til arbeidsgiver så snart som mulig.
- Følg opp aktivitetskrav fra NAV hvis du er langvarig sykmeldt.

**Merk:** Dette er en forenklet veiledning. For fullstendig og oppdatert informasjon, se alltid [nav.no](https://nav.no). NAV-Losen gir veiledende informasjon og erstatter ikke offisiell rådgivning fra NAV.
    `,
    lastUpdated: '2024-05-10',
  },
  {
    id: 'barnetrygd',
    title: 'Slik fungerer barnetrygd',
    summary: 'Informasjon om hvem som har rett på barnetrygd og hvordan det fungerer.',
    category: 'Familie og barn',
    timeEstimate: '5 minutter (lesing)',
    requirements: 'Vanligvis ingen, skjer automatisk for barn født i Norge.',
    content: `# Barnetrygd\n\nBarnetrygd er en månedlig utbetaling til foreldre med barn under 18 år.\n\n## Hvem får barnetrygd?\n- Barnetrygd gis automatisk for barn født i Norge.\n- Du trenger vanligvis ikke å søke.\n- Hvis du er EØS-borger og jobber i Norge, må du søke.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
  {
    id: 'foreldrepenger',
    title: 'Slik søker du foreldrepenger',
    summary: 'Alt du trenger å vite om søknadsprosessen for foreldrepenger.',
    category: 'Familie og barn',
    timeEstimate: 'Ca. 45 minutter',
    requirements: 'Dokumentasjon på inntekt, terminbekreftelse.',
    content: `# Foreldrepenger\n\nForeldrepenger erstatter inntekten din når du er hjemme med barnet ved fødsel eller adopsjon.\n\n## Hvem kan få?\n- Du må ha hatt inntekt i minst seks av de ti siste månedene.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
   {
    id: 'kontantstotte',
    title: 'Slik søker du kontantstøtte',
    summary: 'For deg med barn mellom ett og to år som ikke er i barnehage med offentlig tilskudd.',
    category: 'Familie og barn',
    timeEstimate: 'Ca. 20 minutter',
    requirements: 'BankID, informasjon om barnehageplass.',
    content: `# Kontantstøtte\n\nEn støtte for familier med små barn som ikke benytter barnehageplass.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
    {
    id: 'sfo',
    title: 'Slik søker du redusert betaling i SFO',
    summary: 'Informasjon om hvordan familier med lav inntekt kan søke om redusert pris på SFO.',
    category: 'Familie og barn',
    timeEstimate: 'Ca. 25 minutter',
    requirements: 'Dokumentasjon på husholdningens samlede inntekt.',
    content: `# Redusert foreldrebetaling i SFO\n\nFamilier med lav inntekt kan søke kommunen om redusert betaling.\n\n**Merk:** Ordningen administreres av kommunen, ikke NAV. Sjekk din kommunes nettsider.`,
    lastUpdated: '2024-06-10',
  },
  {
    id: 'sosialhjelp',
    title: 'Slik søker du økonomisk sosialhjelp',
    summary: 'En midlertidig inntektssikring for deg som ikke kan dekke levekostnadene dine selv.',
    category: 'Økonomi',
    timeEstimate: 'Ca. 1 time',
    requirements: 'Full oversikt over inntekter, utgifter, boforhold og familiesituasjon.',
    content: `# Økonomisk Sosialhjelp\n\nDette er en midlertidig økonomisk støtte.\n\n## Hvem kan få?\n- Alle som oppholder seg lovlig i Norge og ikke kan sørge for sitt eget livsopphold.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
   {
    id: 'boutgifter',
    title: 'Slik får du hjelp med boutgifter',
    summary: 'Oversikt over støtteordninger som bostøtte og hjelp til bolig.',
    category: 'Økonomi',
    timeEstimate: 'Ca. 20 minutter (lesing)',
    requirements: 'Husleiekontrakt, dokumentasjon på inntekt og formue.',
    content: `# Hjelp til boutgifter\n\nDet finnes flere ordninger, som bostøtte fra Husbanken, eller støtte til bolig fra NAV.\n\n**Merk:** Bostøtte søkes via Husbanken.`,
    lastUpdated: '2024-06-10',
  },
    {
    id: 'kvalifiseringsprogram',
    title: 'Veiledning for Kvalifiseringsprogrammet',
    summary: 'Et program for deg som ønsker å komme i jobb, men trenger ekstra oppfølging.',
    category: 'Økonomi',
    timeEstimate: 'Krever samtale med NAV',
    requirements: 'Du må ta kontakt med din lokale NAV-veileder.',
    content: `# Kvalifiseringsprogrammet (KVP)\n\nEt program med tett og individuell oppfølging.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
  {
    id: 'aap',
    title: 'Slik søker du AAP (Arbeidsavklaringspenger)',
    summary: 'En guide til AAP for deg som trenger hjelp til å komme tilbake i jobb.',
    category: 'Uførhet',
    timeEstimate: 'Ca. 1 time',
    requirements: 'Dokumentasjon fra lege/behandler, BankID.',
    content: `# Arbeidsavklaringspenger (AAP)\n\nAAP sikrer deg inntekt i perioder du trenger hjelp fra NAV for å komme i arbeid.\n\n## Vilkår\n- Arbeidsevnen din må være nedsatt med minst 50 prosent.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
  {
    id: 'uforetrygd',
    title: 'Slik søker du uføretrygd',
    summary: 'Informasjon om uføretrygd for deg med varig nedsatt inntektsevne.',
    category: 'Uførhet',
    timeEstimate: 'Ca. 1-2 timer',
    requirements: 'Omfattende dokumentasjon fra lege/spesialist, full oversikt over arbeidserfaring.',
    content: `# Uføretrygd\n\nUføretrygd skal sikre inntekt for personer som har fått sin inntektsevne varig nedsatt.\n\n## Vilkår\n- Inntektsevnen må være varig nedsatt med minst 50 prosent.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
    {
    id: 'hjelpemidler',
    title: 'Slik søker du om hjelpemidler',
    summary: 'Hvordan søke om hjelpemidler for å mestre hverdagen.',
    category: 'Uførhet',
    timeEstimate: 'Varierer',
    requirements: 'Vurdering fra lege, ergoterapeut eller annen fagperson.',
    content: `# Hjelpemidler\n\nNAV kan gi støtte til hjelpemidler dersom du har en varig (over to år) funksjonsnedsettelse.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
  {
    id: 'alderspensjon',
    title: 'Slik planlegger du alderspensjon',
    summary: 'Planlegg din fremtidige pensjon fra folketrygden.',
    category: 'Pensjon',
    timeEstimate: '30-60 minutter (planlegging)',
    requirements: 'BankID for å logge inn og se din opptjening.',
    content: `# Alderspensjon\n\nAlderspensjon sikrer deg inntekt når du blir pensjonist.\n\n## Fleksibelt uttak\n- Du kan starte uttak fra du fyller 62 år.\n\n**Merk:** Se alltid [nav.no](https://nav.no).`,
    lastUpdated: '2024-06-05',
  },
    {
    id: 'afp',
    title: 'Veiledning for AFP',
    summary: 'Informasjon om Avtalefestet pensjon (AFP) i privat sektor.',
    category: 'Pensjon',
    timeEstimate: '20 minutter (lesing)',
    requirements: 'Være ansatt i en bedrift med tariffavtale som inkluderer AFP.',
    content: `# Avtalefestet pensjon (AFP)\n\nAFP er en pensjonsordning for ansatte i bedrifter med tariffavtale der AFP inngår.\n\n**Merk:** Se alltid [fellesordningen.no](https://fellesordningen.no).`,
    lastUpdated: '2024-06-05',
  },
];


export const MOCK_DOCUMENTS: Document[] = [
  { id: 'doc1', name: 'Vedtak om dagpenger.pdf', type: 'Vedtak', uploadDate: '2024-04-20', size: '1.2 MB' },
  { id: 'doc2', name: 'Legeerklæring_sykmelding.docx', type: 'Legeerklæring', uploadDate: '2024-05-05', size: '350 KB' },
  { id: 'doc3', name: 'Søknad_foreldrepenger.pdf', type: 'Søknad', uploadDate: '2024-03-10', size: '800 KB' },
];

export const MOCK_REMINDERS: Reminder[] = [
  { id: 'rem1', title: 'Send meldekort', dueDate: '2024-06-10', description: 'Husk å sende meldekort for perioden.', completed: false },
  { id: 'rem2', title: 'Ettersend dokumentasjon AAP', dueDate: '2024-06-15', description: 'Siste frist for å ettersende legeerklæring.', completed: false },
  { id: 'rem3', title: 'Legetime Dr. Hansen', dueDate: '2024-06-05', description: 'Viktig legetime for oppfølging.', completed: true },
];

export const MOCK_NAV_CASES: NavCase[] = [
  { id: 'case1', title: 'Søknad om dagpenger', status: 'Under behandling', nextStep: 'NAV vurderer din søknad. Forventet svar innen 3 uker.', lastUpdated: '2024-05-28'},
  { id: 'case2', title: 'Klage på vedtak - Sykepenger', status: 'Mottatt', nextStep: 'NAV Klageinstans vil behandle klagen. Du vil motta brev når saksbehandler er tildelt.', lastUpdated: '2024-05-20'},
  { id: 'case3', title: 'Oppfølging sykmelding', status: 'Trenger oppfølging', nextStep: 'Du må sende inn oppfølgingsplan innen 2 uker.', lastUpdated: '2024-05-29'},
];

export const MOCK_JOB_POSTINGS: JobPosting[] = [
  { id: 'job1', title: 'Butikkmedarbeider', company: 'Rema 1000', location: 'Kristiansand', url: '#' },
  { id: 'job2', title: 'Kundebehandler', company: 'Telenor', location: 'Arendal', url: '#' },
  { id: 'job3', title: 'Lagerarbeider', company: 'Posten', location: 'Grimstad', url: '#' },
];

export const MOCK_JOB_APPLICATIONS: JobApplication[] = [
  { id: 'app1', jobTitle: 'Butikkmedarbeider', company: 'Rema 1000', status: 'Søknad sendt', dateApplied: '2024-05-28' },
  { id: 'app2', jobTitle: 'Assistent', company: 'Agder kommune', status: 'Under vurdering', dateApplied: '2024-05-25' },
];


export const GENERAL_DISCLAIMER = "NAV-Losen gir veiledende informasjon og er ment som et hjelpemiddel. Informasjonen her erstatter ikke offisiell rådgivning, informasjon eller vedtak fra NAV. Sjekk alltid nav.no for den mest oppdaterte og nøyaktige informasjonen.";
export const AI_DISCLAIMER = "AI-generert innhold kan inneholde feil eller unøyaktigheter. Verifiser alltid viktig informasjon med offisielle kilder hos NAV.";
export const AI_DISCLAIMER_SHORT = "AI-forklaringen kan inneholde feil. Sjekk alltid mot nav.no. Dette er veiledning, ikke juridisk råd.";

export const GEMINI_API_MODEL_TEXT = "gemini-2.5-flash";


// --- Mestring / Mastery Constants ---

export const MASTERY_FEELINGS: MasteryFeeling[] = [
  { label: 'Rolig', valence: 'pleasant', energy: 'low' },
  { label: 'Fokusert', valence: 'pleasant', energy: 'high' },
  { label: 'Håpefull', valence: 'pleasant', energy: 'low' },
  { label: 'Stresset', valence: 'unpleasant', energy: 'high' },
  { label: 'Overveldet', valence: 'unpleasant', energy: 'high' },
  { label: 'Sint', valence: 'unpleasant', energy: 'high' },
  { label: 'Bekymret', valence: 'unpleasant', energy: 'low' },
  { label: 'Trist', valence: 'unpleasant', energy: 'low' },
  { label: 'Nummen', valence: 'unpleasant', energy: 'low' },
  { label: 'Forvirret', valence: 'unpleasant', energy: 'high' },
  { label: 'Motivert', valence: 'pleasant', energy: 'high' },
  { label: 'Nysgjerrig', valence: 'pleasant', energy: 'low' },
];

export const MASTERY_SYMPTOMS: string[] = [
  'Rask puls',
  'Anspent kjeve/skuldre',
  'Klump i magen',
  'Tørr munn',
  'Svimmel / lett i hodet',
  'Tåkesyn',
  'Søvnmangel'
];

export const MASTERY_STRATEGIES: MasteryStrategy[] = [
  {
    id: 'breathe',
    title: 'Pust: 4-6-8 metoden',
    duration: '1-3 minutter',
    description: 'En enkel pusteøvelse for å roe nervesystemet. Pust inn i 4 sek, hold i 6 sek, og pust ut i 8 sek. Gjenta 3-5 ganger.',
    tags: ['calm', 'high-stress', 'all'],
  },
  {
    id: 'grounding',
    title: 'Jording: 5-4-3-2-1 teknikken',
    duration: '2-5 minutter',
    description: 'Koble deg til sansene dine for å finne ro. Legg merke til: 5 ting du kan se, 4 ting du kan ta på, 3 ting du kan høre, 2 ting du kan lukte, og 1 ting du kan smake.',
    tags: ['grounding', 'high-stress', 'all'],
  },
  {
    id: 'action',
    title: 'Handling: Ett lite steg',
    duration: '3 minutter',
    description: 'Når alt føles overveldende, bryt det ned. Identifiser den aller minste, konkrete tingen du kan gjøre akkurat nå for å komme videre. Skriv det ned og fokuser kun på det.',
    tags: ['action', 'focus', 'all'],
  },
  {
    id: 'muscle_relaxation',
    title: 'Progressiv muskelavslapping',
    duration: '5-10 minutter',
    description: 'Stram og slapp av musklene i kroppen systematisk. Start med tærne, arbeid deg oppover. Hold spenningen i 5 sekunder, slapp av i 10.',
    tags: ['calm', 'grounding', 'high-stress'],
  },
  {
    id: 'mindful_observation',
    title: 'Mindful observasjon',
    duration: '2-3 minutter',
    description: 'Velg en gjenstand foran deg. Studer den i 2-3 minutter - form, farge, tekstur. Dette hjelper deg å være til stede her og nå.',
    tags: ['grounding', 'focus'],
  },
  {
    id: 'short_walk',
    title: 'Kort gåtur',
    duration: '5 minutter',
    description: 'Gå sakte i 5 minutter, fokuser på føttene som berører bakken. Frisk luft og bevegelse kan redusere stress.',
    tags: ['action', 'calm', 'all'],
  },
  {
    id: 'write_worries',
    title: 'Skriv ned bekymringer',
    duration: '3-5 minutter',
    description: 'Noter tre ting du bekymrer deg for, og én ting du kan gjøre med hver. Dette hjelper med å organisere tankene.',
    tags: ['action', 'focus'],
  },
    // --- NYE STRATEGIER ---
  {
    id: 'box_breathing',
    title: 'Boks-pust (4-4-4-4)',
    duration: '1-2 minutter',
    description: 'En enkel teknikk for å gjenvinne fokus. Pust inn i 4 sek, hold pusten i 4 sek, pust ut i 4 sek, og hold pusten ute i 4 sek. Gjenta.',
    tags: ['calm', 'focus', 'all'],
  },
  {
    id: 'name_emotion',
    title: 'Navngi følelsen',
    duration: '30-60 sekunder',
    description: 'Sett ord på det du føler akkurat nå, f.eks. "Jeg føler meg overveldet". Å navngi følelsen kan redusere dens intensitet.',
    tags: ['grounding', 'focus'],
  },
  {
    id: 'mini_plan',
    title: 'Mini-plan',
    duration: '1 minutt',
    description: 'Bestem deg for én, og bare én, liten ting du skal gjøre de neste 10 minuttene. F.eks. "Hente et glass vann". Dette bryter handlingslammelse.',
    tags: ['action', 'focus'],
  },
];