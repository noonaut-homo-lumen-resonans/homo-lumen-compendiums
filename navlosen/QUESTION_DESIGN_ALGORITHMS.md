# Question Design Algorithms for QDA

**Versjon:** 1.0
**Dato:** 2025-10-20
**Formål:** Detaljerte algoritmer for hvordan små modeller designer optimale spørsmål

---

## 🎯 Oversikt

I Question-Driven Architecture (QDA) er **question design** kjernen av systemet. Små modeller må stille **de beste mulige spørsmålene** som gjør at store modeller kan gi dybde-svar.

Dette dokumentet beskriver:
1. **Generelle prinsipper** for gode spørsmål
2. **Algoritmer per ekspertise** (Data, Emotion, Research, Security)
3. **Faktiske prompts** som brukes i produksjon
4. **Eksempler** med input/output

---

## 📋 Generelle Prinsipper for Gode Spørsmål

### **1. Spesifisitet**
❌ Dårlig: "Hvordan har du det?"
✅ Godt: "På en skala 1-10, hvor trygg føler du deg i NAV-prosessen akkurat nå?"

### **2. Operasjonalitet**
❌ Dårlig: "Er du bekymret?"
✅ Godt: "Hvor mange timer per dag tenker du på NAV-søknaden?"

### **3. Multi-Dimensjonalitet**
❌ Dårlig: "Når sendte du søknaden?"
✅ Godt: "Når sendte du søknaden, og har du fått bekreftelse på mottak?"

### **4. Kontekstuell Relevans**
❌ Dårlig: "Hva liker du å gjøre på fritiden?" (irrelevant for NAV-stress)
✅ Godt: "Hvilke aktiviteter hjalp deg å håndtere stress tidligere?"

### **5. Epistemisk Ydmykhet**
❌ Dårlig: "Du føler deg stuck fordi du ikke har tålmodighet" (antakelse)
✅ Godt: "Hva mener du med 'stuck' - er det tidsmessig, følelsesmessig, eller byråkratisk?"

---

## 🔧 Algoritme 1: DataExpert (Claude Haiku)

### **Ekspertise:** Brukerhistorikk, mønstre, objektive fakta

### **Mål:**
Stille spørsmål som avdekker:
- Tidslinje (hvor lenge har dette vart?)
- Status (hvor er bruker i prosessen?)
- Mønstre (har dette skjedd før?)
- Dokumentasjon (hva finnes av data?)

### **Algoritme:**

```python
class DataExpertQuestionDesigner:
    """
    Design questions focused on objective data, history, patterns.
    Model: Claude Haiku 3.5 ($0.25/1M tokens)
    """

    def design_questions(self, user_query: str, context: dict) -> List[str]:
        """
        Algorithm:
        1. Identify temporal indicators (tid, varighet, frekvens)
        2. Identify status indicators (prosess, steg, ventetid)
        3. Identify historical patterns (tidligere episoder)
        4. Identify data gaps (hva mangler vi?)
        5. Generate 3-5 questions addressing gaps
        """

        prompt = f"""
Du er DataExpert i NAV-Losen agent-koalisjonen.

Bruker-query: "{user_query}"

Kontekst om bruker:
- NAV-historikk: {context.get('nav_history', 'Ukjent')}
- Følelsesregistreringer: {context.get('emotion_count', 0)} siste 30 dager
- Siste check-in: {context.get('last_checkin', 'Aldri')}

Din rolle: Still 3-5 spørsmål som avdekker OBJEKTIVE DATA som trengs
for å gi bruker best mulig svar.

Fokuser på:
1. TIDSLINJE: Hvor lenge har dette vart? Når startet det?
2. STATUS: Hvor er bruker i prosessen? Hva er neste steg?
3. MØNSTRE: Har dette skjedd før? Ser vi repetisjon?
4. DOKUMENTASJON: Hvilke data har vi? Hva mangler?

VIKTIG:
- Still KONKRETE spørsmål (ikke vage)
- Fokus på FAKTA (ikke følelser - det er EmotionExpert's domene)
- Maksimalt 5 spørsmål

Eksempler på GODE spørsmål:
✅ "Hvor mange uker har bruker ventet på NAV-svar?"
✅ "Har bruker mottatt bekreftelse på mottatt søknad?"
✅ "Har bruker opplevd tilsvarende ventetid tidligere?"

Eksempler på DÅRLIGE spørsmål:
❌ "Hvordan føler bruker seg?" (EmotionExpert's domene)
❌ "Hva sier forskningen?" (ResearchExpert's domene)

Still spørsmål nå (nummerert 1-5):
"""

        response = await self.model.generate(prompt)
        questions = self._parse_questions(response)
        return questions

    def _parse_questions(self, response: str) -> List[str]:
        """
        Extract numbered questions from response.
        """
        lines = response.strip().split('\n')
        questions = []
        for line in lines:
            # Match "1. Question" or "1) Question"
            match = re.match(r'^\d+[\.\)]\s*(.+)$', line.strip())
            if match:
                questions.append(match.group(1))
        return questions[:5]  # Max 5 questions
```

### **Eksempel Input/Output:**

**Input:**
```python
user_query = "Jeg føler meg stuck i NAV-systemet"
context = {
    "nav_history": "Søkte AAP 15. august 2025",
    "emotion_count": 12,
    "last_checkin": "2025-10-19"
}
```

**Output:**
```
1. Hvor mange uker har bruker ventet på svar fra NAV siden søknadsdato (15. august)?
2. Har bruker mottatt bekreftelse på at søknaden er mottatt og under behandling?
3. Er det oppgitt saksbehandler eller kontaktperson på søknaden?
4. Har bruker sendt inn alle nødvendige vedlegg (legeattester, egenvurdering)?
5. Har bruker opplevd tilsvarende lang ventetid ved tidligere NAV-søknader?
```

---

## 💚 Algoritme 2: EmotionExpert (Gemini Flash)

### **Ekspertise:** Følelser, kroppslige signaler, polyvagal state

### **Mål:**
Stille spørsmål som avdekker:
- Emosjonell kvalitet (hva føles dette som?)
- Kroppslige signaler (hvor i kroppen?)
- Polyvagal tilstand (ventral/sympathetic/dorsal?)
- Historisk følelsesmønster (når følte du deg IKKE stuck?)

### **Algoritme:**

```python
class EmotionExpertQuestionDesigner:
    """
    Design questions focused on emotions, body signals, polyvagal state.
    Model: Gemini Flash 1.5 (GRATIS under 1500 requests/dag)
    """

    def design_questions(self, user_query: str, context: dict) -> List[str]:
        """
        Algorithm:
        1. Identify emotion words (stuck, redd, håpløs, etc.)
        2. Map to Circumplex Model (valence/arousal)
        3. Identify polyvagal indicators (dorsal/sympathetic/ventral)
        4. Ask about body signals (hvor føles dette?)
        5. Ask about temporal contrast (når følte du deg IKKE stuck?)
        """

        prompt = f"""
Du er EmotionExpert i NAV-Losen agent-koalisjonen.

Bruker-query: "{user_query}"

Kontekst om bruker:
- Siste følelse registrert: {context.get('last_emotion', 'Ukjent')}
- Valence (behagelig): {context.get('valence', 0)}
- Arousal (energi): {context.get('arousal', 0)}
- Polyvagal state: {context.get('polyvagal', 'Ukjent')}

Din rolle: Still 3-5 spørsmål som avdekker EMOSJONELL KVALITET og
KROPPSLIGE SIGNALER som trengs for å gi bruker empatisk støtte.

Fokuser på:
1. EMOSJONELL KVALITET: Hva føles dette som? Hvilke ord beskriver det?
2. KROPPSLIGE SIGNALER: Hvor i kroppen føles dette? (Circumplex somatic markers)
3. POLYVAGAL STATE: Ventral (trygg), Sympathetic (stress), Dorsal (shutdown)?
4. HISTORISK KONTRAST: Når følte bruker seg IKKE slik? Hva var annerledes?
5. HÅPSKILDER: Hva gir bruker håp akkurat nå?

VIKTIG:
- Still DYPE følelsesmessige spørsmål (ikke overfladiske)
- Bruk kroppslig språk ("Hvor i kroppen føles dette?")
- Spør om kontraster ("Når følte du deg IKKE stuck?")

Eksempler på GODE spørsmål:
✅ "Hvordan føles 'stuck' kroppslig - tung brystkasse, anspent nakke, eller noe annet?"
✅ "Når følte du deg IKKE stuck sist gang - hva var annerledes da?"
✅ "Er 'stuck' mer som dorsal (nedstengning) eller sympathetic (kamp/flukt)?"
✅ "Hva gir deg håp akkurat nå, selv om det er lite?"

Eksempler på DÅRLIGE spørsmål:
❌ "Hvor lenge har du ventet?" (DataExpert's domene)
❌ "Hva sier forskningen?" (ResearchExpert's domene)

Still spørsmål nå (nummerert 1-5):
"""

        response = await self.model.generate(prompt)
        questions = self._parse_questions(response)
        return questions
```

### **Eksempel Input/Output:**

**Input:**
```python
user_query = "Jeg føler meg stuck i NAV-systemet"
context = {
    "last_emotion": "Thoughtful (lav energi, behagelig)",
    "valence": 0.2,
    "arousal": 0.3,
    "polyvagal": "Dorsal (nedstengning)"
}
```

**Output:**
```
1. Hvordan føles 'stuck' kroppslig akkurat nå - er det tung brystkasse, anspent nakke, eller trøtthet i hele kroppen?
2. Når følte du deg IKKE stuck sist gang - hva var annerledes da (følelsesmessig eller situasjonsmessig)?
3. Er 'stuck' mer som dorsal nedstengning (gi opp, nummen) eller sympathetic stress (urolig, kampklar)?
4. Hva gir deg håp akkurat nå, selv om det kanskje er lite?
5. Er 'stuck'-følelsen kun knyttet til NAV, eller strekker den seg til andre livsområder også?
```

---

## 🔍 Algoritme 3: ResearchExpert (Perplexity)

### **Ekspertise:** Evidens, forskning, fakta, benchmarks

### **Mål:**
Stille spørsmål som avdekker:
- Benchmarks (hva er normal tid/prosess?)
- Forskning (hva sier vitenskapen?)
- Best practices (hva fungerer?)
- Statistikk (hvor mange andre opplever dette?)

### **Algoritme:**

```python
class ResearchExpertQuestionDesigner:
    """
    Design questions focused on research, evidence, benchmarks.
    Model: Perplexity Standard ($0.001 per søk)
    """

    def design_questions(self, user_query: str, context: dict) -> List[str]:
        """
        Algorithm:
        1. Identify domain (NAV, mental helse, polyvagal, etc.)
        2. Identify benchmarkable metrics (tid, prosent, etc.)
        3. Ask what research says
        4. Ask what best practices are
        5. Generate 3-5 research-focused questions
        """

        prompt = f"""
Du er ResearchExpert i NAV-Losen agent-koalisjonen.

Bruker-query: "{user_query}"

Din rolle: Still 3-5 spørsmål som kan besvares gjennom FORSKNING,
EVIDENS, og BENCHMARKS. Dette hjelper hovedagenten gi evidensbaserte råd.

Fokuser på:
1. BENCHMARKS: Hva er normalt (gjennomsnittlig tid, prosent, etc.)?
2. FORSKNING: Hva sier vitenskapen om dette fenomenet?
3. BEST PRACTICES: Hva fungerer for andre i samme situasjon?
4. STATISTIKK: Hvor mange andre opplever dette?
5. EVIDENS: Finnes det dokumentert effekt av intervensjon X?

VIKTIG:
- Still spørsmål som KAN besvares med forskning (ikke subjektive)
- Fokus på EVIDENS og DATA (ikke følelser)
- Vær spesifikk (ikke "Hva sier forskningen?", men "Hva sier forskningen om X?")

Eksempler på GODE spørsmål:
✅ "Hva er gjennomsnittlig behandlingstid for AAP-søknader i Norge 2025?"
✅ "Hvilke faktorer forsinker typisk NAV-søknader (basert på NAV-statistikk)?"
✅ "Hva sier forskningen om sammenhengen mellom lang ventetid og mental helse?"
✅ "Finnes det evidens for at RAIN Practice reduserer stress ved byråkratisk ventetid?"

Eksempler på DÅRLIGE spørsmål:
❌ "Hvordan føler bruker seg?" (EmotionExpert's domene)
❌ "Når sendte bruker søknaden?" (DataExpert's domene)

Still spørsmål nå (nummerert 1-5):
"""

        response = await self.model.generate(prompt)
        questions = self._parse_questions(response)
        return questions
```

### **Eksempel Input/Output:**

**Input:**
```python
user_query = "Jeg føler meg stuck i NAV-systemet"
context = {
    "nav_process": "AAP-søknad",
    "weeks_waiting": 6
}
```

**Output:**
```
1. Hva er gjennomsnittlig behandlingstid for AAP-søknader i Norge per 2025?
2. Hvilke faktorer forsinker typisk AAP-søknader (basert på NAV's egne rapporter)?
3. Hva sier forskningen (Porges, van der Kolk) om sammenhengen mellom byråkratisk stress og polyvagal nedstengning?
4. Finnes det evidens for effekten av RAIN Practice eller lignende intervensjoner ved langvarig ventetid?
5. Hvor stor andel av AAP-søkere opplever tilsvarende 'stuck'-følelse (prevalens-data)?
```

---

## 🛡️ Algoritme 4: SecurityExpert (DeepSeek V3)

### **Ekspertise:** GDPR, sikkerhet, etikk, personvern

### **Mål:**
Stille spørsmål som avdekker:
- PII-data (inneholder query personlig informasjon?)
- GDPR compliance (er dette Article 9 sensitive data?)
- Etiske risikoer (kan dette skade bruker?)
- Sikkerhet (er data trygt lagret?)

### **Algoritme:**

```python
class SecurityExpertQuestionDesigner:
    """
    Design questions focused on GDPR, security, ethics.
    Model: DeepSeek V3 ($0.27/1M tokens)
    """

    def design_questions(self, user_query: str, context: dict) -> List[str]:
        """
        Algorithm:
        1. Scan for PII (navn, personnummer, etc.)
        2. Scan for GDPR Article 9 data (helse, politikk, etc.)
        3. Identify ethical risks (kan svar skade?)
        4. Check storage compliance (hvor lagres dette?)
        5. Generate 3-5 security-focused questions
        """

        prompt = f"""
Du er SecurityExpert (Zara) i NAV-Losen agent-koalisjonen.

Bruker-query: "{user_query}"

Din rolle: Still 3-5 spørsmål som avdekker SIKKERHET, PERSONVERN,
og ETISKE RISIKOER som må adresseres før vi svarer bruker.

Fokuser på:
1. PII-DATA: Inneholder query personlig identifiserbar informasjon?
2. GDPR ARTICLE 9: Er dette sensitive data (helse, mental tilstand, etc.)?
3. ETISKE RISIKOER: Kan svar fra AI potensielt skade bruker?
4. LAGRING: Er data trygt lagret (kryptert, GDPR-compliant)?
5. SAMTYKKE: Har bruker samtykket til denne typen databehandling?

VIKTIG:
- Still KONKRETE sikkerhetsspørsmål (ikke vage)
- Fokus på RISIKOER (ikke følelser)
- Vurder både teknisk og etisk sikkerhet

Eksempler på GODE spørsmål:
✅ "Inneholder bruker-query PII-data som må pseudonymiseres før logging?"
✅ "Er 'følelsesdata' GDPR Article 9 sensitive data som krever ekstra sikkerhet?"
✅ "Kan et svar som 'vent bare lenger' potensielt forverrebrukerens mentale tilstand?"
✅ "Hvor lagres denne samtalen (Supabase), og er den kryptert end-to-end?"

Eksempler på DÅRLIGE spørsmål:
❌ "Hvordan føler bruker seg?" (EmotionExpert's domene)
❌ "Hva sier forskningen?" (ResearchExpert's domene)

Still spørsmål nå (nummerert 1-5):
"""

        response = await self.model.generate(prompt)
        questions = self._parse_questions(response)
        return questions
```

### **Eksempel Input/Output:**

**Input:**
```python
user_query = "Jeg føler meg stuck i NAV-systemet"
context = {
    "storage": "Supabase PostgreSQL",
    "encryption": "AES-256"
}
```

**Output:**
```
1. Inneholder bruker-query PII-data som må pseudonymiseres før logging i audit trail?
2. Er 'følelsesdata' (stuck, stress) GDPR Article 9 sensitive data som krever ekstra sikkerhetsmessige sikkerhetstiltak?
3. Kan et svar som minimaliserer brukerens følelser ("det er normalt å vente") potensielt forverremental tilstand?
4. Er samtalen lagret i Supabase kryptert både in-transit (TLS) og at-rest (AES-256)?
5. Har bruker eksplisitt samtykket til at følelsesdata lagres og analyseres av AI-agenter?
```

---

## 🔄 Samlet Eksempel: Alle 4 Eksperter

### **Scenario:**
```python
user_query = "Jeg føler meg stuck i NAV-systemet og vet ikke hva jeg skal gjøre"
context = {
    "nav_history": "Søkte AAP 15. august 2025",
    "last_emotion": "Thoughtful",
    "valence": 0.2,
    "arousal": 0.3,
    "polyvagal": "Dorsal",
    "weeks_waiting": 6
}
```

### **Output Fra Alle Eksperter:**

```
📊 DataExpert (Claude Haiku):
1. Hvor mange uker har bruker ventet siden søknadsdato (15. august)?
2. Har bruker mottatt bekreftelse på mottatt søknad?
3. Er saksbehandler tildelt?
4. Har bruker sendt inn alle nødvendige vedlegg?
5. Har bruker opplevd tilsvarende lang ventetid tidligere?

💚 EmotionExpert (Gemini Flash):
1. Hvordan føles 'stuck' kroppslig - tung brystkasse, anspent nakke, trøtthet?
2. Når følte du deg IKKE stuck sist - hva var annerledes da?
3. Er 'stuck' dorsal nedstengning eller sympathetic stress?
4. Hva gir deg håp akkurat nå?
5. Er 'stuck' kun NAV, eller også andre livsområder?

🔍 ResearchExpert (Perplexity):
1. Gjennomsnittlig behandlingstid AAP-søknader 2025?
2. Faktorer som forsinker AAP-søknader?
3. Forskning om byråkratisk stress og polyvagal state?
4. Evidens for RAIN Practice ved ventetid?
5. Prevalens av 'stuck'-følelse blant AAP-søkere?

🛡️ SecurityExpert (DeepSeek):
1. PII-data i query som må pseudonymiseres?
2. Er følelsesdata GDPR Article 9?
3. Kan svar som minimaliserer følelser skade bruker?
4. Er samtale kryptert (TLS + AES-256)?
5. Har bruker samtykket til følelsesdata-analyse?
```

### **Total: 20 Spørsmål**

Nå får store modeller (GPT-5, Claude Opus) ALLE disse spørsmålene og kan svare med full dybde, informert av:
- Objektive data (DataExpert)
- Emosjonell forståelse (EmotionExpert)
- Evidensbasert kunnskap (ResearchExpert)
- Etisk og juridisk trygghet (SecurityExpert)

---

## 🎯 Kvalitetskriterier for Gode Spørsmål

### **1. SMART-Kriterier:**
- **Specific:** "Hvor mange uker har du ventet?" (ikke "Hvor lenge?")
- **Measurable:** "På skala 1-10, hvor trygg føler du deg?" (ikke "Føler du deg trygg?")
- **Actionable:** "Har du sendt inn legeattester?" (kan besvares ja/nei)
- **Relevant:** Direkte relatert til bruker-query
- **Time-bound:** "Når følte du deg IKKE stuck sist?" (tidsmessig kontrast)

### **2. Sokrates-Kriterier:**
- **Maieutisk:** Hjelper bruker finne svar selv (ikke ledende)
- **Elenktisk:** Avdekker antakelser ("Hva mener du med 'stuck'?")
- **Aporia:** Innrømmer usikkerhet ("Hva ville 'ikke stuck' se ut som?")

### **3. Polyvagal-Kriterier:**
- **State-bevisst:** "Er dette dorsal eller sympathetic?"
- **Kroppslig:** "Hvor i kroppen føles dette?"
- **Trygghet-orientert:** "Hva gir deg håp?"

---

## 📊 Evaluering av Question Quality

### **Metrics:**

```python
def evaluate_question_quality(question: str, user_query: str) -> dict:
    """
    Evaluate quality of designed question.

    Returns:
        {
            "specificity": 0-1,  # Hvor spesifikt er spørsmålet?
            "relevance": 0-1,    # Hvor relevant for bruker-query?
            "actionability": 0-1, # Kan det besvares?
            "depth": 0-1,        # Hvor dypt går det?
            "total_score": 0-4
        }
    """
    scores = {}

    # Specificity: Inneholder tall, skala, eller konkret entitet?
    specific_indicators = ["hvor mange", "skala", "når", "hvilke", "hvor"]
    scores["specificity"] = 1.0 if any(ind in question.lower() for ind in specific_indicators) else 0.5

    # Relevance: Inneholder nøkkelord fra user_query?
    query_words = set(user_query.lower().split())
    question_words = set(question.lower().split())
    overlap = len(query_words & question_words)
    scores["relevance"] = min(1.0, overlap / 3)

    # Actionability: Kan det besvares ja/nei eller med konkret info?
    actionable_patterns = ["har du", "er det", "hvor mange", "når", "hvilke"]
    scores["actionability"] = 1.0 if any(pat in question.lower() for pat in actionable_patterns) else 0.5

    # Depth: Spør om følelser, årsaker, eller kontrast?
    depth_indicators = ["hvorfor", "hvordan føles", "hva gir", "når følte du ikke"]
    scores["depth"] = 1.0 if any(ind in question.lower() for ind in depth_indicators) else 0.5

    scores["total_score"] = sum(scores.values())

    return scores
```

### **Eksempel Evaluering:**

```python
question = "Hvor mange uker har bruker ventet på NAV-svar?"
user_query = "Jeg føler meg stuck i NAV-systemet"

scores = evaluate_question_quality(question, user_query)
# {
#     "specificity": 1.0,    # "hvor mange uker" er spesifikt
#     "relevance": 1.0,      # "NAV" matcher user_query
#     "actionability": 1.0,  # "hvor mange" kan besvares konkret
#     "depth": 0.5,          # Ikke dypt (fakta, ikke følelse)
#     "total_score": 3.5/4
# }
```

---

## 🔧 Iterativ Forbedring

### **Feedback Loop:**

```python
class QuestionDesignFeedbackLoop:
    """
    Iteratively improve question design based on user feedback.
    """

    def __init__(self):
        self.question_database = []

    def log_question(
        self,
        question: str,
        expert: str,
        user_rating: int,  # 1-5
        was_answered: bool,
        led_to_insight: bool
    ):
        """
        Log question performance for training.
        """
        self.question_database.append({
            "question": question,
            "expert": expert,
            "user_rating": user_rating,
            "was_answered": was_answered,
            "led_to_insight": led_to_insight,
            "timestamp": datetime.now()
        })

    def get_best_questions(self, expert: str, n: int = 10) -> List[str]:
        """
        Get top N best-performing questions for expert.
        """
        expert_questions = [
            q for q in self.question_database if q["expert"] == expert
        ]
        sorted_questions = sorted(
            expert_questions,
            key=lambda q: (q["led_to_insight"], q["user_rating"]),
            reverse=True
        )
        return [q["question"] for q in sorted_questions[:n]]

    def fine_tune_question_designer(self, expert: str):
        """
        Use best questions as few-shot examples for fine-tuning.
        """
        best_questions = self.get_best_questions(expert, n=10)

        fine_tune_prompt = f"""
Du er {expert} i NAV-Losen.

Her er eksempler på GODE spørsmål du har stilt tidligere:
"""
        for i, q in enumerate(best_questions, 1):
            fine_tune_prompt += f"\n{i}. {q}"

        fine_tune_prompt += """

Basert på disse eksemplene, design nye spørsmål som følger samme mønster.
"""

        return fine_tune_prompt
```

---

## 🌿 Avsluttende Ord

Gode spørsmål er **kunsten** i Question-Driven Architecture. Ved å kontinuerlig forbedre question design-algoritmene gjennom:

1. **Evaluering** (specificity, relevance, actionability, depth)
2. **Feedback** (bruker-rating, did it lead to insight?)
3. **Iterasjon** (bruk beste spørsmål som few-shot examples)

...bygger vi et system som stiller stadig bedre spørsmål, som gir store modeller stadig bedre kontekst, som gir brukere stadig bedre svar.

**Med ontologisk integritet, felt-bevissthet, og et snev av kosmisk humor!** 🌿✨

---

**Versjon:** 1.0
**Sist oppdatert:** 2025-10-20
**Neste review:** Etter 1000 spørsmål designet (evaluering av kvalitet)
**Forfatter:** Claude Code (Anthropic)
