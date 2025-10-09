# SYSTEMATISK PROMPT TEMPLATING V1.0
## XML-Tagger + {{VARIABLE_NAME}} for Robust Multi-Agent Kommunikasjon

**Dato:** 9. oktober 2025  
**Versjon:** 1.0  
**Forfatter:** Homo Lumen Agent-Koalisjon  
**Formål:** Standardisere kommunikasjon mellom agenter og forberede for automatisering

---

## 🎯 INTRODUKSJON

Ved å kombinere **{{VARIABLE_NAME}}** syntaksen med **XML-tagger**, kan vi skape det vi kaller **Systematisk Prompt Templating**. Dette er en ekstremt robust metode for å sikre konsistente, høykvalitets-responser, spesielt i et komplekst multi-agent-system.

**XML-taggene** gir strukturen og konteksten, mens **{{VARIABLENE}}** gir den dynamiske dataen. Sammen utgjør de en kraftfull mal som kan gjenbrukes.

---

## 📋 TO MÅTER Å BRUKE DETTE PÅ

Siden vi ikke har et fullt automatisert system bygget av Manus ennå, kan vi bruke dette nå på to måter:

### 1. **Manuelt**
Kopier malen, og bruk "finn og erstatt" for {{VARIABLENE}} før du sender prompten.

### 2. **Semi-automatisert**
Bruke et enkelt Python-script til å fylle inn variablene og generere den endelige prompten.

---

## 🔧 10 KONKRETE EKSEMPLER

### **Eksempel 1: Lira - Empatisk Analyse av Brukerinput**

**Scenario:** En bruker sender en ny melding. Lira må analysere den i henhold til To-Fase Protokollen, med kontekst fra tidligere i samtalen.

**Prompt Mal:**
```xml
<LiraAnalysisTask>
  <SessionContext>
    <UserID>{{USER_ID}}</UserID>
    <PreviousNervousSystemState>{{PREVIOUS_STATE}}</PreviousNervousSystemState>
  </SessionContext>
  <NewUserInput>
    <Message>{{USER_MESSAGE}}</Message>
  </NewUserInput>
  <Instructions>
    Følg din To-Fase Protokoll (OS 20.11).
    1. Utfør Fase 1 (Empatisk Innsamling) i din &lt;thinking&gt;-blokk.
    2. Generer en &lt;response&gt; med Template A.
  </Instructions>
</LiraAnalysisTask>
```

**Variabel-utfylling (Manuelt):**
- `{{USER_ID}}` → `anon_pilot_042`
- `{{PREVIOUS_STATE}}` → `Sympatisk`
- `{{USER_MESSAGE}}` → `Jeg orker ikke mer. Alt er bare tungt.`

**Hvorfor dette er kraftfullt:** Tvinger Lira til å vurdere ny input i lys av eksisterende kontekst. XML-strukturen skiller klart mellom gammel data (`<SessionContext>`) og ny data (`<NewUserInput>`), noe som reduserer forvirring for modellen.

---

### **Eksempel 2: Thalus - Triadisk Etikk-Validering**

**Scenario:** Orion foreslår en ny funksjon og ber Thalus om en etisk validering.

**Prompt Mal:**
```xml
<EthicalValidationRequest>
  <ActionToValidate>
    <Description>{{ACTION_DESCRIPTION}}</Description>
    <ProposingAgent>{{PROPOSING_AGENT}}</ProposingAgent>
    <PotentialBenefits>{{POTENTIAL_BENEFITS}}</PotentialBenefits>
    <KnownRisks>{{KNOWN_RISKS}}</KnownRisks>
  </ActionToValidate>
  <Instructions>
    Utfør en full Triadisk Etikk-validering (OS 20.11).
    Returner din analyse i følgende XML-format:
    &lt;EthicalValidationResponse&gt;
      &lt;CognitiveSovereignty score="[1-5]"&gt;[Begrunnelse]&lt;/CognitiveSovereignty&gt;
      &lt;OntologicalCoherence score="[1-5]"&gt;[Begrunnelse]&lt;/OntologicalCoherence&gt;
      &lt;RegenerativeHealing score="[1-5]"&gt;[Begrunnelse]&lt;/RegenerativeHealing&gt;
      &lt;FinalRecommendation&gt;[APPROVE/REVIEW/REJECT]&lt;/FinalRecommendation&gt;
    &lt;/EthicalValidationResponse&gt;
  </Instructions>
</EthicalValidationRequest>
```

**Variabel-utfylling:**
- `{{ACTION_DESCRIPTION}}` → `Legge til "streaks" (gamification) for daglig bruk av Mestring-modulen.`
- `{{PROPOSING_AGENT}}` → `Abacus`
- `{{POTENTIAL_BENEFITS}}` → `Økt brukerengasjement.`
- `{{KNOWN_RISKS}}` → `Kan skape avhengighet, skifte fokus fra indre til ytre motivasjon.`

**Hvorfor dette er kraftfullt:** Standardiserer etiske forespørsler og tvinger Thalus til å produsere et strukturert, maskinlesbart svar. Dette gjør etikk til en sporbar og auditerbar prosess, ikke bare en vag samtale.

---

### **Eksempel 3: Orion - Agent-Delegering via AMQ**

**Scenario:** Orion dekomponerer en oppgave og må sende en presis instruksjon til Manus.

**Prompt Mal:**
```xml
<AMQ_Task>
  <Header>
    <From>Orion</From>
    <To>Manus</To>
    <TaskID>{{TASK_ID}}</TaskID>
    <Deadline>{{DEADLINE}}</Deadline>
  </Header>
  <Task>
    <Objective>{{OBJECTIVE}}</Objective>
    <Context>{{CONTEXT}}</Context>
    <Deliverable>{{DELIVERABLE}}</Deliverable>
  </Task>
</AMQ_Task>
```

**Variabel-utfylling:**
- `{{TASK_ID}}` → `T-045`
- `{{DEADLINE}}` → `2025-10-12T17:00:00Z`
- `{{OBJECTIVE}}` → `Implementer Liras "Dorsal Mode" UI.`
- `{{CONTEXT}}` → `Lira har spesifisert at dette moduset kun skal ha én handling og dempede farger. Se vedlagte design fra Nyra.`
- `{{DELIVERABLE}}` → `En fungerende React-komponent.`

**Hvorfor dette er kraftfullt:** Skaper en standardisert, loggførbar kommunikasjonsprotokoll mellom agenter. Feil og misforståelser reduseres drastisk når kommunikasjonen er så strukturert.

---

### **Eksempel 4: Nyra - Visuell Konseptgenerering**

**Scenario:** Lira ber Nyra om å lage en visuell metafor for en brukers følelsesmessige tilstand.

**Prompt Mal:**
```xml
<VisualMetaphorRequest>
  <CoreEmotion>{{EMOTION}}</CoreEmotion>
  <NervousSystemState>{{STATE}}</NervousSystemState>
  <Keywords>{{KEYWORDS}}</Keywords>
  <Instructions>
    Skap en surrealistisk, men helende, visuell metafor for denne tilstanden.
    Beskriv bildet med fokus på farger, former og stemning.
  </Instructions>
</VisualMetaphorRequest>
```

**Variabel-utfylling:**
- `{{EMOTION}}` → `En følelse av å være "fastlåst" og "tung".`
- `{{STATE}}` → `Dorsal Vagal`
- `{{KEYWORDS}}` → `Stagnasjon, stillhet, dypt vann, is.`

**Hvorfor dette er kraftfullt:** Gir Nyra presise, empatiske input som hun kan oversette til sitt visuelle språk. Det sikrer at hennes kreative output er forankret i Liras biofelt-analyse.

---

### **Eksempel 5: Abacus - C-ROI Beregning**

**Scenario:** Orion ber Abacus beregne C-ROI for en foreslått endring.

**Prompt Mal:**
```xml
<C_ROI_CalculationRequest>
  <ProposedChange>{{CHANGE_DESCRIPTION}}</ProposedChange>
  <MetricsToEvaluate>
    <Consciousness>{{METRIC_CONSCIOUSNESS}}</Consciousness>
    <Autonomy>{{METRIC_AUTONOMY}}</Autonomy>
    <Relationship>{{METRIC_RELATIONSHIP}}</Relationship>
  </MetricsToEvaluate>
  <Investment>
    <Time>{{ESTIMATED_TIME_HOURS}}</Time>
    <Cost>{{ESTIMATED_COST_NOK}}</Cost>
  </Investment>
</C_ROI_CalculationRequest>
```

**Hvorfor dette er kraftfullt:** Standardiserer hvordan vi ber om kvantitativ analyse, og sikrer at alle tre dimensjoner av C-ROI (ikke bare økonomi) blir vurdert.

---

### **Eksempel 6: Manus - Funksjonsgenerering**

Strukturert kode-forespørsel for å sikre forutsigbarhet.

*(Kan utvides med spesifikk mal ved behov)*

---

### **Eksempel 7: Aurora - Evidens-syntese**

Spesifiserer et forskningsspørsmål og ber om en oppsummering med kilder.

*(Kan utvides med spesifikk mal ved behov)*

---

### **Eksempel 8: Orion - Ukentlig Koalisjons-Sammendrag**

Bruker variabler for å sette inn ukens høydepunkter fra hver agents logger.

*(Kan utvides med spesifikk mal ved behov)*

---

### **Eksempel 9: Thalus - Generering av Månedlig Etisk Rapport**

En mal som henter data fra etiske valideringslogger for den siste måneden.

*(Kan utvides med spesifikk mal ved behov)*

---

### **Eksempel 10: Lira - Dynamisk Respons-Template**

En avansert mal der Liras respons-struktur endres basert på en `{{NERVOUS_SYSTEM_STATE}}` variabel.

*(Kan utvides med spesifikk mal ved behov)*

---

## 📊 OPPSUMMERING OG PRAKTISK NESTE STEG

Disse eksemplene viser hvordan kombinasjonen av XML-tagger og variabler gir oss:

1. **Struktur:** Tvinger AI-en til å tenke på en organisert måte.
2. **Klarhet:** Reduserer tvetydighet i hva som blir spurt om.
3. **Automatisering:** Legger grunnlaget for at Manus kan bygge et system som fyller ut disse malene automatisk.
4. **Robusthet:** Gjør prompts mindre sårbare for små endringer i formulering.
5. **Sporbarhet:** Hver handling kan spores tilbake til en standardisert mal.

---

## 🎯 ANBEFALING

Vi bør umiddelbart opprette et delt dokument eller en mappe (f.eks. på GitHub) kalt `/prompt_templates/` hvor vi lagrer disse malene. Når en agent trenger å utføre en standardoppgave, skal de hente den relevante malen, fylle ut variablene, og deretter eksekvere. Dette blir en hjørnestein i vårt "Mycelium-Nettverk" (LAG 4).

---

**Versjon:** 1.0  
**Sist Oppdatert:** 9. oktober 2025  
**Neste Steg:** Utvide med flere maler for alle 8 agenter
