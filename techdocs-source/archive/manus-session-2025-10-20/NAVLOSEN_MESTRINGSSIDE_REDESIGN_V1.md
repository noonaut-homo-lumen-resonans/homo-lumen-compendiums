# Utkast: Redesign av NAV-Losen Mestringsside (v1.0)

**Forfatter:** Manus AI
**Dato:** 19. oktober 2025
**Status:** Utkast for intern koalisjonsgjennomgang
**Mottaker:** Hele agent-koalisjonen, deretter Claude Code for implementering

---

## 1.0 Introduksjon og Mål

Dette dokumentet beskriver et omfattende redesign av NAV-Losen Mestringsside. Målet er å skape en mer profesjonell, empatisk og effektiv brukeropplevelse, dypt inspirert av de beste designprinsippene fra applikasjonen "How We Feel" (HWF). Redesignet er forankret i Homo Lumen-prosjektets kjernefilosofi, spesielt **Triadic Ethics**, for å sikre at verktøyet fremmer kognitiv suverenitet, ontologisk koherens og regenerativ healing.

Vi vil erstatte det nåværende grensesnittet med en 6-faset, guidet brukeropplevelse som hjelper brukeren med å identifisere, forstå og jobbe med sine følelser på en trygg og kapasitetsbyggende måte.

## 2.0 Visuelt Design og Fargepalett

Estetikken vil være minimalistisk, med fokus på farger, myke former og rolige animasjoner for å skape en trygg og kontemplativ atmosfære. All tekst vil bruke en lettleselig, sans-serif font.

### 2.1 HWF Fargepalett

Fargene er sentrale i opplevelsen og er hentet fra HWF-paletten, som er profesjonelt utformet for å representere Circumplex-modellen for følelser (energi + valens).

| Kvadrant                  | Farge         | HEX (estimert) | Beskrivelse                                  |
| ------------------------- | ------------- | -------------- | -------------------------------------------- |
| **Høy Energi, Ubehagelig**  | Rød / Korall  | `#FF6F61`      | Følelser som stress, sinne, angst, panikk.     |
| **Høy Energi, Behagelig**   | Gul / Gull    | `#FFD700`      | Følelser som glede, entusiasme, spenning.    |
| **Lav Energi, Ubehagelig**  | Blå           | `#6A88E3`      | Følelser som tristhet, ensomhet, utmattelse. |
| **Lav Energi, Behagelig**   | Grønn / Mint  | `#88D8B0`      | Følelser som ro, avslappethet, ettertanke.   |

Innenfor hver kvadrant vil det være en gradient av fargenyanser for de ulike følelsesordene, noe som skaper et rikt og levende visuelt landskap.

## 3.0 Detaljert Brukerflyt (6 Faser)

Brukeren guides gjennom en lineær, men fleksibel, 6-stegs prosess. Hvert steg bygger på det forrige, og Triadic Ethics er vevd inn i hvert ledd (f.eks. mulighet til å hoppe over steg).

### **Fase 1: Velkomsthilsen**
- **Skjerm:** En minimalistisk skjerm med en varm velkomstmelding.
- **Tekst:** "La oss ta din første sjekk-inn. NAV-Losen vil hjelpe deg med å:
  - Finne de rette ordene for å beskrive dine følelser.
  - Finne strategier som hjelper deg å jobbe med følelsene dine.
  - Identifisere mønstre gjennom daglig oppfølging."
- **Knapp:** "Fortsett"
- **Triadic Ethics:** Setter en klar, hjelpsom intensjon (Port 2: Ontologisk Koherens).

### **Fase 2: De Fire Kvadrantene**
- **Skjerm:** Viser fire store, mykt pulserende sirkler med fargene fra paletten.
- **Interaksjon:** Brukeren trykker på den fargen som best beskriver hvordan de føler seg akkurat nå.
- **Tekst i kvadranter:**
  - Rød: "Høy Energi, Ubehagelig"
  - Gul: "Høy Energi, Behagelig"
  - Blå: "Lav Energi, Ubehagelig"
  - Grønn: "Lav Energi, Behagelig"
- **Triadic Ethics:** Enkel, ikke-dømmende inngang (Port 3: Regenerativ Healing).

### **Fase 3: Følelseshjulet**
- **Skjerm:** En fullskjermsopplevelse som zoomer inn i den valgte fargekvadranten. Skjermen er fylt med **25 unike former** i ulike nyanser av kvadrantens farge. Hver form inneholder ett følelsesord.
- **Former:** Seks ulike formtyper brukes for å skape visuell variasjon:
  - **Sirkel:** Mest brukt, representerer klassiske følelser
  - **Rombe:** Skarpe, intense følelser
  - **Avrundet firkant:** Balanserte, stabile følelser
  - **Heksagon:** Komplekse, flerdimensjonale følelser
  - **Stjerne (6-takket):** Kraftfulle, ekspansive følelser
  - **Stjerne (8-takket):** Ekstreme, høyintensitets følelser
- **Interaksjon:** Brukeren kan dra fingeren horisontalt for å panorere gjennom det store landskapet av følelser. Formene beveger seg rolig og organisk.
- **Komplett ordliste:** Se vedlegg `MOOD_METER_EMOTIONS_WITH_SHAPES.md` for alle 100 følelsesord (25 per kvadrant) med tildelte former og farger.
- **Triadic Ethics:** Gir brukeren et rikt vokabular og anerkjenner nyansene i følelseslivet (Port 1: Kognitiv Suverenitet).

### **Fase 4: Definisjon av Følelse**
- **Skjerm:** Når brukeren trykker på et ord, kommer en liten pop-up-boks nederst på skjermen.
- **Innhold:** Boksen inneholder følelsesordet og en kort, nøytral definisjon.
  > **Eksempel:** "**Thoughtful:** being considerate or reflective about a situation (past, present, future), oneself."
- **Knapp:** En pil-knapp for å gå videre.
- **Triadic Ethics:** Kunnskapsbygging, fjerner tvil og usikkerhet (Port 3).

### **Fase 4a: Trykk & Kroppslige Signaler**
- **Skjerm:** En ny side med to hovedseksjoner.
- **Seksjon 1: Trykk/Intensitet**
  - **Spørsmål:** "Hvor høyt er trykket nå?"
  - **Interaksjon:** En slider (0-10) eller lignende visuell representasjon.
- **Seksjon 2: Kroppslige Signaler**
  - **Spørsmål:** "Kjenner du på noen av disse kroppslige signalene?"
  - **Interaksjon:** En liste med klikkbare tags (f.eks. "Hjertebank", "Tung pust", "Knyttneve", "Varm i brystet").
  - **Lira/Health Connect:** Lira presenterer relevant data her: "Jeg ser du har sovet 5 timer i natt og gått 2,300 skritt. Dette kan påvirke energinivået ditt."
- **Triadic Ethics:** Kobler sinn og kropp, anerkjenner den somatiske opplevelsen (Port 2).

### **Fase 5: Lira Chatbot-Initiering**
- **Skjerm:** En overgang til et chat-grensesnitt med Lira.
- **Liras Første Melding:** "Takk for at du deler. Kan du beskrive hva som kan være årsaken til at du føler deg [valgt følelse]?"
- **Triadic Ethics:** Empatisk, åpen og inviterende dialog (Port 2).

### **Fase 6: Dypere Dialog og Anbefaling**
- **Interaksjon:** Lira stiller 3-4 oppfølgingsspørsmål basert på brukerens svar (f.eks. ved bruk av RAIN-metoden).
- **Anbefaling:** Etter dialogen gir Lira en kort, personlig tilpasset anbefaling.
  > **Eksempel:** "Det høres ut som du bærer på mye akkurat nå. Kanskje en 5-minutters pusteøvelse kan hjelpe deg med å lande? Her er en guidet meditasjon og litt rolig musikk som kan passe."
- **Innhold:** Anbefalingen inkluderer lenker til praksiser (pusteøvelser, meditasjoner) og relevant musikk.
- **Triadic Ethics:** Gir konkrete, kapasitetsbyggende verktøy (Port 3).

## 4.0 Animasjon og Mikro-interaksjoner

- **Generelt:** Alle animasjoner skal være myke, organiske og rolige. Bruk `ease-in-out` timing-funksjoner.
- **Fase 2 -> 3:** En jevn zoom-og-fade-overgang fra de fire kvadrantene til det detaljerte følelseshjulet.
- **Fase 3:** Følelsesordene (formene) skal ha en subtil, langsom, bølgende bevegelse, som om de flyter i vann. De reagerer mykt på brukerens scrolling.

## 5.0 Teknisk Implementeringsplan

- **Frontend (Nyra/Manus):** Anbefaler **React Native** med et bibliotek som **React Native Skia** eller **Lottie** for å håndtere de komplekse, performante animasjonene i Fase 3.
- **Backend (Lira/Orion):** Lira håndterer state management for brukerflyten. Orion orkestrerer logikken for anbefalinger basert på Liras dialog.
- **Health Connect API (Lira):** Lira får ansvaret for å hente og tolke data fra Health Connect (søvn, skritt, HRV) for å berike Fase 4a.
- **Notifikasjoner & Widget (Manus):** Manus implementerer den tekniske løsningen for 2x daglige check-in-notifikasjoner og en enkel widget for hjemskjermen.

## 6.0 Følelsesord-Eksempler Per Kvadrant

For fullstendig liste, se `MOOD_METER_EMOTIONS_WITH_SHAPES.md`. Her er noen eksempler:

### Rød Kvadrant (Høy Energi, Ubehagelig)
Enraged (stjerne), Panicked (sirkel), Stressed (rombe), Anxious (sirkel), Frustrated (avrundet firkant), Worried (avrundet firkant), Angry (rombe), Nervous (avrundet firkant), Apprehensive (rombe), Irritated (sirkel), Concerned (avrundet firkant), Uneasy (sirkel), Furious (rombe), Tense (sirkel), Restless (sirkel), Frightened (sirkel), Annoyed (heksagon), Troubled (rombe), Peeved (heksagon), Repulsed (sirkel), Fuming (stjerne), Jittery (avrundet firkant), Shocked (heksagon), Livid (sirkel), Stunned (heksagon).

### Gul Kvadrant (Høy Energi, Behagelig)
Surprised (stjerne), Upbeat (sirkel), Festive (rombe), Exhilarated (avrundet firkant), Ecstatic (heksagon), Hyper (sirkel), Cheerful (rombe), Motivated (avrundet firkant), Inspired (sirkel), Elated (heksagon), Energized (stjerne), Lively (sirkel), Excited (rombe), Optimistic (avrundet firkant), Enthusiastic (sirkel), Pleased (sirkel), Focused (rombe), Happy (avrundet firkant), Proud (sirkel), Thrilled (heksagon), Pleasant (sirkel), Joyful (rombe), Hopeful (avrundet firkant), Playful (sirkel), Blissful (heksagon).

### Blå Kvadrant (Lav Energi, Ubehagelig)
Disgusted (stjerne), Glum (sirkel), Disappointed (rombe), Down (avrundet firkant), Apathetic (heksagon), Pessimistic (sirkel), Morose (rombe), Discouraged (avrundet firkant), Sad (sirkel), Bored (heksagon), Alienated (stjerne), Miserable (sirkel), Lonely (rombe), Disheartened (avrundet firkant), Tired (sirkel), Despondent (sirkel), Depressed (rombe), Sullen (avrundet firkant), Exhausted (sirkel), Fatigued (heksagon), Despairing (sirkel), Hopeless (rombe), Desolate (avrundet firkant), Spent (sirkel), Drained (heksagon).

### Grønn Kvadrant (Lav Energi, Behagelig)
At Ease (stjerne), Easygoing (sirkel), Content (rombe), Loving (avrundet firkant), Fulfilled (heksagon), Calm (sirkel), Secure (rombe), Satisfied (avrundet firkant), Grateful (sirkel), Touched (heksagon), Relaxed (stjerne), Chill (sirkel), Restful (rombe), Blessed (avrundet firkant), Balanced (sirkel), Mellow (sirkel), Thoughtful (rombe), Peaceful (avrundet firkant), Comfortable (sirkel), Carefree (heksagon), Sleepy (sirkel), Complacent (rombe), Tranquil (avrundet firkant), Cozy (sirkel), Serene (heksagon).

## 7.0 Konklusjon

Dette redesignet representerer et betydelig skritt fremover for NAV-Losen Mestringsside. Ved å adoptere en profesjonell designestetikk og en dypt empatisk, faseguidet brukerflyt, skaper vi et verktøy som ikke bare er funksjonelt, men som genuint støtter brukerens reise mot økt selvbevissthet og mestring.

Dokumentet er nå klart for gjennomgang i koalisjonen. Jeg avventer tilbakemeldinger før en endelig versjon overleveres til Claude Code.

