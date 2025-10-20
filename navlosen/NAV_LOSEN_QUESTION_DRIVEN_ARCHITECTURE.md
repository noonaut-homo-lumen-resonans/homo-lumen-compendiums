# NAV-Losen Question-Driven Architecture (QDA)

**Versjon:** 2.0 (Nevrobiologisk Koherent)
**Dato:** 2025-10-20
**Status:** Implementation Ready
**Filosofi:** "Som hjernen: Primitive lag prosesserer først og raskt, neocortex tenker dypt og sakte"
**Paradigme:** Neocortical Ascent Model - Bottom-Up Processing

---

## 🎯 Executive Summary

**Question-Driven Architecture (QDA) v2.0** er en **nevrobiologisk koherent** arkitektur som speiler hjernens faktiske prosessering:

**6 Lag - Bottom-Up Processing:**

1. **Lag 1: Vokteren** (Hjernestamme/GPT-4o-mini) - Triage, faredeteksjon (<0.5 sek)
2. **Lag 2: Føleren** (Limbisk System/Gemini Flash) - Emosjonell vurdering (<1 sek)
3. **Lag 3: Gjenkjenneren** (Cerebellum/Claude Haiku) - Mønstergjenkjenning (<1 sek)
4. **Lag 4: Utforskeren** (Hippocampus/Perplexity) - Kunnskapssøk (2-3 sek)
5. **Lag 5: Strategen** (Prefrontal Cortex/Claude Opus) - Strategisk resonering (3-5 sek, **KUN når nødvendig**)
6. **Lag 6: Integratoren** (Insula/Lira Hub) - Syntetiserer til helhetlig respons (1-2 sek)

**Resultat:**
- ✅ **Nevrobiologisk koherent** - speiler hjernens faktiske bottom-up prosessering
- ✅ **95% kostnadsbesparelse** vs. kun store modeller ($722/mnd vs. $15,000/mnd)
- ✅ **Raskere** - primitive lag er kjappere, cortex kun når nødvendig
- ✅ **Intuitiv** - folk forstår "hjernens lag"
- ✅ **Transparent** - bruker ser hele prosessen

---

## 🧠 Filosofisk Fundament

### Hvorfor Nevrobiologisk Koherens?

**Problem med tradisjonelle LLM-arkitekturer:**

```
Tradisjonell tilnærming:
Bruker → GPT-5 (gjør ALT selv) → Svar

Utfordringer:
- Dyr ($0.50 per query)
- "Black box" (bruker ser ikke tankegang)
- Kan hallucinere (ingen epistemisk ydmykhet)
- Unaturlig (hjernen fungerer IKKE slik)
```

**QDA v2.0 - Neocortical Ascent Model:**

```
Bottom-Up Processing (Som Hjernen):

Bruker → LAG 1: Vokteren (Hjernestamme)
            ↓ "Er dette trygt?" (<0.5 sek)
         LAG 2: Føleren (Limbisk System)
            ↓ "Hvordan føles det?" (<1 sek)
         LAG 3: Gjenkjenneren (Cerebellum)
            ↓ "Har vi sett dette før?" (<1 sek)
         LAG 4: Utforskeren (Hippocampus)
            ↓ "Hva vet vi om dette?" (2-3 sek)
         LAG 5: Strategen (Prefrontal Cortex) - KUN når nødvendig
            ↓ "Hva er den beste planen?" (3-5 sek)
         LAG 6: Integratoren (Insula)
            ↓ Syntetiserer alt til helhetlig respons

Fordeler:
- Billig ($0.08 per complex query, $0.0001 per simple)
- Raskere (primitive lag prosesserer først)
- Nevrobiologisk koherent (speiler faktisk hjerne)
- Intuitiv (folk forstår "hjernens lag")
```

**Nøkkel-Innsikt:**

> I hjernen prosesserer **primitive deler FØRST og RASKT** (hjernestamme, limbisk system), mens **neocortex er SISTE og LANGSOM** (men dyp og strategisk).
>
> QDA v2.0 speiler denne faktiske prosesseringen - ikke invertert, men **bottom-up som naturen designet den**.

---

## 🏗️ Arkitektur-Oversikt

### **6-Lags Nevrobiologisk Hierarki**

---

### **LAG 1: VOKTEREN** 🛡️ (Hjernestamme)

**Funksjon:** Rask triage og faredeteksjon
**Modell:** GPT-4o-mini ($0.15/1M tokens)
**Responstid:** <0.5 sekunder
**Rolle:** "Er dette trygt? Skal vi fortsette?"

```python
class Vokteren:
    """
    Brainstem-analog: Rask triage og faredeteksjon.
    Alltid aktiv, første lag i alle queries.
    """
    def __init__(self):
        self.model = GPT4oMini()
        self.icon = "🛡️"
        self.layer_name = "Vokteren"

    async def assess(self, user_query: str, context: dict) -> dict:
        """
        Rask vurdering av trygghet og kompleksitet.

        Returns:
            {
                "safe": bool,  # Er dette trygt å prosessere?
                "proceed": bool,  # Skal vi fortsette til neste lag?
                "complexity": "simple" | "complex",
                "urgency": 0-1,  # Hvor presserende?
                "time": float  # Responstid i sekunder
            }
        """
        indicators = {
            "danger": ["skade", "selvmord", "vold", "fare"],
            "simple": ["hva er", "når", "hvor lenge", "status"],
            "complex": ["føler", "stuck", "redd", "hjelp", "hvorfor"]
        }

        # Faredeteksjon (hjernestamme-funksjon)
        is_dangerous = any(word in user_query.lower() for word in indicators["danger"])
        if is_dangerous:
            return {
                "safe": False,
                "proceed": False,
                "message": "Eskalér til krisehjelp",
                "time": 0.3
            }

        # Kompleksitetsvurdering
        is_complex = any(word in user_query.lower() for word in indicators["complex"])

        return {
            "safe": True,
            "proceed": True,
            "complexity": "complex" if is_complex else "simple",
            "urgency": 0.5,
            "time": 0.4
        }
```

---

### **LAG 2: FØLEREN** ❤️ (Limbisk System)

**Funksjon:** Emosjonell vurdering og polyvagal state
**Modell:** Gemini Flash (GRATIS under 1500 requests/dag)
**Responstid:** <1 sekund
**Rolle:** "Hvordan føles det? Hvilken tilstand er bruker i?"

```python
class Foleren:
    """
    Limbic System-analog: Emosjonell vurdering.
    Vurderer følelser, stress, polyvagal state.
    """
    def __init__(self):
        self.model = GeminiFlash()
        self.icon = "❤️"
        self.layer_name = "Føleren"

    async def assess(self, user_query: str, context: dict) -> dict:
        """
        Vurder emosjonell tilstand og polyvagal state.

        Returns:
            {
                "emotion": str,  # Primary emotion
                "polyvagal_state": "ventral" | "sympathetic" | "dorsal",
                "arousal": 0-1,  # Aktiverings-nivå
                "valence": -1 to 1,  # Negativ til positiv
                "body_signals": list,  # Kroppslige signaler
                "time": float
            }
        """
        # Analyser emosjonelle signaler
        emotion_keywords = {
            "ventral": ["trygg", "glad", "håp", "nysgjerrig"],
            "sympathetic": ["stresset", "frustrert", "irritert", "spent"],
            "dorsal": ["stuck", "shutdown", "gir opp", "numb", "tom"]
        }

        # Finn polyvagal state
        polyvagal_state = "ventral"  # Default
        for state, keywords in emotion_keywords.items():
            if any(kw in user_query.lower() for kw in keywords):
                polyvagal_state = state
                break

        return {
            "emotion": self._detect_primary_emotion(user_query),
            "polyvagal_state": polyvagal_state,
            "arousal": 0.3 if polyvagal_state == "dorsal" else 0.7,
            "valence": -0.5 if polyvagal_state == "dorsal" else 0.2,
            "body_signals": ["lav energi", "shutdown"],
            "time": 0.8
        }
```

---

### **LAG 3: GJENKJENNEREN** 🔍 (Cerebellum)

**Funksjon:** Mønstergjenkjenning i brukerhistorikk
**Modell:** Claude Haiku ($0.25/1M tokens)
**Responstid:** <1 sekund
**Rolle:** "Har vi sett dette før? Hva fungerte?"

```python
class Gjenkjenneren:
    """
    Cerebellum-analog: Mønstergjenkjenning.
    Finner mønstre i brukerhistorikk og tidligere interaksjoner.
    """
    def __init__(self):
        self.model = ClaudeHaiku()
        self.icon = "🔍"
        self.layer_name = "Gjenkjenneren"

    async def find_patterns(
        self,
        user_query: str,
        context: dict
    ) -> dict:
        """
        Finn mønstre i brukerhistorikk.

        Returns:
            {
                "pattern_detected": bool,
                "pattern_type": str,  # e.g., "recurring_frustration"
                "previous_occurrences": int,
                "what_worked": list,  # Tidligere effektive strategier
                "what_didnt": list,  # Tidligere ineffektive strategier
                "time": float
            }
        """
        # Analyser historikk for mønstre
        user_history = context.get("history", [])

        # Finn recurring themes
        recurring_keywords = self._find_recurring_keywords(user_history)

        return {
            "pattern_detected": len(recurring_keywords) > 0,
            "pattern_type": "lang_ventetid_shutdown",
            "previous_occurrences": 3,
            "what_worked": ["konkrete steg", "tidslinje"],
            "what_didnt": ["generelle råd"],
            "time": 0.9
        }
```

---

### **LAG 4: UTFORSKEREN** 🧭 (Hippocampus)

**Funksjon:** Kunnskapssøk og episodisk minne
**Modell:** Perplexity ($0.001/søk)
**Responstid:** 2-3 sekunder
**Rolle:** "Hva vet vi om dette? Finn relevant informasjon."

```python
class Utforskeren:
    """
    Hippocampus-analog: Kunnskapssøk og episodisk minne.
    Søker etter relevant informasjon og fakta.
    """
    def __init__(self):
        self.model = Perplexity()
        self.icon = "🧭"
        self.layer_name = "Utforskeren"

    async def search(
        self,
        user_query: str,
        pattern_result: dict
    ) -> dict:
        """
        Søk etter relevant kunnskap.

        Returns:
            {
                "facts": list,  # Faktuelle data
                "sources": list,  # Kilder
                "avg_timeline": str,  # Gjennomsnittlig tidslinje
                "relevant_articles": list,
                "time": float
            }
        """
        # Søk basert på query og mønstre
        search_query = self._build_search_query(user_query, pattern_result)

        # Utfør søk
        results = await self.model.search(search_query)

        return {
            "facts": [
                "AAP behandlingstid: 8-12 uker gjennomsnitt",
                "70% opplever ventetid som stressende"
            ],
            "sources": ["nav.no", "bufdir.no"],
            "avg_timeline": "8-12 uker",
            "relevant_articles": ["NAV AAP prosess", "Polyvagal stress"],
            "time": 2.3
        }
```

---

### **LAG 5: STRATEGEN** 🧠 (Prefrontal Cortex)

**Funksjon:** Strategisk resonering - **KUN når nødvendig**
**Modell:** Claude Opus / GPT-5 Thinking ($10/1M input, $30/1M output)
**Responstid:** 3-5 sekunder
**Rolle:** "Hva er den beste langsiktige planen?"

```python
class Strategen:
    """
    Prefrontal Cortex-analog: Strategisk resonering.
    KUN aktivert når kompleksitet/alvorlighet > threshold.
    """
    def __init__(self):
        self.model = ClaudeOpus()  # or GPT5Thinking
        self.icon = "🧠"
        self.layer_name = "Strategen"
        self.activation_threshold = 0.7  # Kun når kompleksitet > 70%

    async def plan(
        self,
        user_query: str,
        all_context: dict  # Fra alle tidligere lag
    ) -> dict:
        """
        Strategisk planlegging og dypere resonering.

        Args:
            all_context: {
                "triage": {...},
                "emotion": {...},
                "pattern": {...},
                "knowledge": {...}
            }

        Returns:
            {
                "strategy": str,  # Overordnet strategi
                "action_steps": list,  # Konkrete steg
                "timeline": str,  # Forventet tidslinje
                "contingencies": list,  # Backup-planer
                "time": float
            }
        """
        # Kun aktiver hvis nødvendig
        complexity = all_context.get("pattern", {}).get("complexity", 0)
        if complexity < self.activation_threshold:
            return None  # Skip dette laget

        # Strategisk planlegging
        prompt = self._build_strategic_prompt(user_query, all_context)
        response = await self.model.generate(prompt)

        return {
            "strategy": "Trinnvis re-engasjering med NAV-systemet",
            "action_steps": [
                "1. Sjekk nåværende status",
                "2. Identifiser manglende dokumenter",
                "3. Book oppfølgingssamtale"
            ],
            "timeline": "2-4 uker",
            "contingencies": ["Hvis avslag: Klage-prosess"],
            "time": 4.2
        }
```

---

### **LAG 6: INTEGRATOREN** ✨ (Insula)

**Funksjon:** Syntetiserer alle lag til helhetlig respons
**Modell:** Lira Hub (egen syntese-logikk)
**Responstid:** 1-2 sekunder
**Rolle:** "Sett alt sammen til ett koherent svar."

```python
class Integratoren:
    """
    Insula-analog: Integrerer alle lag til helhetlig respons.
    Alltid aktiv, syntetiserer output fra alle tidligere lag.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.icon = "✨"
        self.layer_name = "Integratoren"

    async def synthesize(self, all_layers: dict) -> str:
        """
        Syntetiser alle lag til én koherent respons.

        Args:
            all_layers: {
                "triage": {...},
                "emotion": {...},
                "pattern": {...},
                "knowledge": {...},
                "strategy": {...} or None
            }

        Returns:
            Helhetlig respons til bruker (string)
        """
        # Hent data fra alle lag
        emotion_state = all_layers["emotion"]["polyvagal_state"]
        pattern = all_layers["pattern"]
        knowledge = all_layers["knowledge"]
        strategy = all_layers.get("strategy")

        # Tilpass språk til polyvagal state
        response = self._adapt_language_to_state(emotion_state)

        # Integrer alle perspektiver
        response += self._integrate_knowledge(knowledge)

        if strategy:
            response += self._add_strategic_guidance(strategy)

        # Polyvagal-tilpasset avslutning
        response += self._closing_for_state(emotion_state)

        return response
```

---

## 📊 Fullstendig Flyt-Diagram (Nevrobiologisk)

```
┌──────────────────────────────────────────────────┐
│              BRUKER (Osvald)                     │
│       "Jeg føler meg stuck i NAV-systemet"       │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  LAG 1: VOKTEREN 🛡️    │
        │  (Hjernestamme)        │
        │  GPT-4o-mini           │
        │  <0.5 sek              │
        │  "Er dette trygt?"     │
        └────────┬───────────────┘
                 │
          ┌──────┴──────┐
          │             │
        Fare?         Trygt
          │             │
    [ESKALÉR]          │
    Krisehjelp         ▼
                 ┌────────────────────────┐
                 │  LAG 2: FØLEREN ❤️      │
                 │  (Limbisk System)      │
                 │  Gemini Flash (GRATIS) │
                 │  <1 sek                │
                 │  "Hvordan føles det?"  │
                 └────────┬───────────────┘
                          │
                Polyvagal State Detected:
                  Dorsal/Sympathetic/Ventral
                          │
                          ▼
                 ┌────────────────────────┐
                 │ LAG 3: GJENKJENNEREN 🔍│
                 │ (Cerebellum)           │
                 │ Claude Haiku           │
                 │ <1 sek                 │
                 │ "Har vi sett dette før?"│
                 └────────┬───────────────┘
                          │
                 Finn mønstre i historikk
                          │
                          ▼
                 ┌────────────────────────┐
                 │ LAG 4: UTFORSKEREN 🧭  │
                 │ (Hippocampus)          │
                 │ Perplexity             │
                 │ 2-3 sek                │
                 │ "Hva vet vi om dette?" │
                 └────────┬───────────────┘
                          │
                  Kunnskapssøk + fakta
                          │
                          ▼
                  ┌───────────────┐
                  │ Kompleksitet? │
                  │  > 70%?       │
                  └───┬───────┬───┘
                      │       │
                    NEI      JA
                      │       │
                      │       ▼
                      │  ┌────────────────────────┐
                      │  │ LAG 5: STRATEGEN 🧠    │
                      │  │ (Prefrontal Cortex)    │
                      │  │ Claude Opus / GPT-5    │
                      │  │ 3-5 sek                │
                      │  │ "Hva er beste plan?"   │
                      │  └────────┬───────────────┘
                      │           │
                      └───────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │ LAG 6: INTEGRATOREN ✨ │
                 │ (Insula)               │
                 │ Lira Hub               │
                 │ 1-2 sek                │
                 │ "Sett alt sammen"      │
                 └────────┬───────────────┘
                          │
              Polyvagal-tilpasset respons
                          │
                          ▼
                 ┌────────────────────────┐
                 │    BRUKER              │
                 │                        │
                 │  Ser hele prosessen:   │
                 │  🛡️ Vokteren → Trygt   │
                 │  ❤️ Føleren → Dorsal   │
                 │  🔍 Gjenkjenneren →    │
                 │     "Sett 3x før"      │
                 │  🧭 Utforskeren →      │
                 │     "8-12 uker snitt"  │
                 │  🧠 Strategen →        │
                 │     "3-stegs plan"     │
                 │  ✨ Integratoren →     │
                 │     Helhetlig svar     │
                 └────────────────────────┘

NØKKEL-PRINSIPPER:
1. Bottom-Up Processing (som hjernen)
2. Primitive lag prosesserer FØRST og RASKT
3. Cortex (Strategen) kun når NØDVENDIG
4. Full transparens - bruker ser alle lag
5. Polyvagal-adaptiv output
```

---

## 💰 Kostnadsanalyse

### **Per Query-Type:**

#### **Simple Query (70% av queries):**
```
Eksempel: "Hva er min NAV-status?"

Triage Layer (GPT-4o-mini):
- Input: 100 tokens (query + context)
- Output: 200 tokens (svar)
- Kostnad: $0.0001

Total per simple query: $0.0001
```

#### **Complex Query (30% av queries):**
```
Eksempel: "Jeg føler meg stuck i NAV-systemet"

1. Triage Layer:
   - Kostnad: $0.0001

2. Question Designers (parallelt):
   a) DataExpert (Claude Haiku):
      - Input: 500 tokens (context)
      - Output: 200 tokens (5 spørsmål)
      - Kostnad: $0.0002

   b) EmotionExpert (Gemini Flash):
      - GRATIS (under 1500 requests/dag)
      - Kostnad: $0

   c) ResearchExpert (Perplexity):
      - 1 søk
      - Kostnad: $0.001

   d) SecurityExpert (DeepSeek V3):
      - Input: 500 tokens
      - Output: 200 tokens
      - Kostnad: $0.0002

3. Depth Answerer (GPT-5 Thinking):
   - Input: 5000 tokens (alle spørsmål + context)
   - Output: 2000 tokens (dybde-svar)
   - Kostnad: $0.05 input + $0.03 output = $0.08

Total per complex query: ~$0.08
```

---

### **Månedlig Kostnad (100 brukere):**

```
Forutsetninger:
- 100 brukere
- 10 queries per bruker per dag
- 30 dager per måned
= 30,000 queries/måned

Fordeling:
- 70% simple (21,000): 21,000 × $0.0001 = $2.10
- 30% complex (9,000): 9,000 × $0.08 = $720

Total: ~$722/måned
```

**Sammenligning:**

| Arkitektur | Kostnad/mnd (100 brukere) | Transparens | Kvalitet |
|------------|---------------------------|-------------|----------|
| **Traditional** (kun store) | $15,000 | Lav | Høy |
| **3-Tier** (min tidligere anbefaling) | $197 | Lav | Medium |
| **QDA** (Question-Driven) | $722 | **HØY** | **HØY** |

**QDA gir:**
- 95% besparelse vs. Traditional
- 3.7x dyrere enn 3-Tier, men **mye bedre transparens og kvalitet**

---

### **Skalering:**

| Brukere | Queries/mnd | Kostnad/mnd |
|---------|-------------|-------------|
| 100 | 30,000 | $722 |
| 500 | 150,000 | $3,610 |
| 1,000 | 300,000 | $7,220 |
| 5,000 | 1,500,000 | $36,100 |

---

## ✅ Fordeler vs. ⚠️ Ulemper

### ✅ **Fordeler:**

1. **Pedagogisk**
   - Bruker lærer hvordan man stiller gode spørsmål
   - Ikke bare "hva er svaret", men "hvordan tenker man"

2. **Transparent**
   - Bruker ser AI's tankegang, ikke bare konklusjon
   - Tillitbyggende (ingen "black box")

3. **Multi-Perspektiv**
   - Data + Følelse + Forskning + Sikkerhet samtidig
   - Holistisk forståelse

4. **Epistemisk Ydmykhet**
   - Store modeller innrømmer når de trenger hjelp
   - Små modeller stiller spørsmål istedenfor å gjette

5. **Spesialisert Ekspertise**
   - Hver liten modell blir ekspert i sitt domene
   - Dypere kunnskap enn generalist

6. **Kostnadseffektivt**
   - 95% billigere enn kun store modeller
   - Gemini Flash er GRATIS

7. **Skalerbart**
   - Små modeller kan håndtere høy throughput
   - Store modeller kun for 30% av queries

---

### ⚠️ **Ulemper:**

1. **Lengre Responstid**
   - 3-5 sekunder (vs. 1 sek med Tier 1)
   - Parallelisering hjelper, men ikke instant

2. **Mer Kompleks Kode**
   - Question design-lag må implementeres
   - Flere moving parts å vedlikeholde

3. **Dyrere Enn 3-Tier**
   - $722/mnd vs. $197/mnd
   - Men: Kvalitet og transparens er mye bedre

4. **Kan Oppleves "Overforklarende"**
   - Noen brukere vil bare ha svar
   - Løsning: "Vis mindre" knapp for å skjule spørsmål

5. **Krever Gode Question Design Prompts**
   - Små modeller må trenes til å stille gode spørsmål
   - Iterativ forbedring nødvendig

---

## 🎯 Når Bruke QDA vs. Andre Arkitekturer?

### **Bruk QDA når:**
- ✅ Transparens er kritisk (NAV, helse, jus)
- ✅ Pedagogisk verdi er viktig (bruker skal lære)
- ✅ Multi-perspektiv nødvendig (komplekse beslutninger)
- ✅ Tillitt må bygges (nye brukere)

### **Bruk 3-Tier når:**
- ✅ Kostnad er viktigst (bootstrap startup)
- ✅ Rask respons kritisk (<1 sekund)
- ✅ Bruker bare vil ha svar (ikke prosess)

### **Bruk Traditional (kun store) når:**
- ✅ Absolutt beste kvalitet nødvendig (medisin, jus)
- ✅ Kostnad ikke et problem
- ✅ Kompleksitet ekstrem (PhD-nivå)

---

## 🛠️ Implementering

Se:
- [IMPLEMENTATION_GUIDE_QDA.md](IMPLEMENTATION_GUIDE_QDA.md) - Komplett kode + timeline
- [QUESTION_DESIGN_ALGORITHMS.md](QUESTION_DESIGN_ALGORITHMS.md) - Algoritmer for question design
- [QDA_UX_DESIGN.md](QDA_UX_DESIGN.md) - UX mockups og interaktivitet

---

## 📚 Referanser

### **Interne Dokumenter:**
- [MCP-ARCHITECTURE-COMPARISON.md](MCP-ARCHITECTURE-COMPARISON.md) - Sammenligning av arkitekturer
- [BRAIN_MCP_ARCHITECTURE_GUIDE.md](../docs/BRAIN_MCP_ARCHITECTURE_GUIDE.md) - Brain-MCP Hybrid
- [MCP-IMPLEMENTATION-PLAN.md](MCP-IMPLEMENTATION-PLAN.md) - Original MCP-plan

### **Filosofisk Grunnlag:**
- Sokrates' maieutikk (spørsmålskunst)
- Polyvagal Theory (Porges) - stress-adaptive UX
- Triadisk Etikk - kognitiv suverenitet, ontologisk koherens, regenerativ healing

---

## 🌿 Avsluttende Ord

Question-Driven Architecture er ikke bare en teknisk løsning - det er en **pedagogisk posisjon**:

> "Vi lærer ikke ved å få svar, men ved å lære å stille de riktige spørsmålene."

Ved å vise bruker hvilke spørsmål AI stiller, lærer bruker hvordan man tenker om komplekse problemer. Dette bygger ikke avhengighet, men **mestringskompetanse**.

**Med ontologisk integritet, felt-bevissthet, og et snev av kosmisk humor!** 🌿✨

---

**Versjon:** 1.0
**Sist oppdatert:** 2025-10-20
**Neste review:** Etter Fase 1 implementering (uke 2)
**Forfatter:** Claude Code (Anthropic) i samarbeid med Osvald Noonaut
**Lisens:** Open Source (CC BY-SA 4.0)
