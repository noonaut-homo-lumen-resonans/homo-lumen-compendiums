# NAV-Losen Question-Driven Architecture (QDA)

**Versjon:** 1.0
**Dato:** 2025-10-20
**Status:** Implementation Ready
**Filosofi:** "Små modeller stiller de beste spørsmålene, store modeller gir de dypeste svarene"

---

## 🎯 Executive Summary

**Question-Driven Architecture (QDA)** er en invertert Socratic arkitektur hvor:

1. **Små, raske modeller** (Claude Haiku, Gemini Flash, Perplexity) designer optimale spørsmål
2. **Store, dype modeller** (GPT-5, Claude Opus, Grok-4) svarer med full kontekst
3. **Bruker ser prosessen** - både spørsmål og svar (full transparens)

**Resultat:**
- ✅ 95% kostnadsbesparelse vs. kun store modeller ($722/mnd vs. $15,000/mnd)
- ✅ Pedagogisk - bruker lærer hvordan man stiller gode spørsmål
- ✅ Multi-perspektiv - data + følelse + forskning samtidig
- ✅ Tillitbyggende - bruker ser AI's tankegang, ikke bare konklusjon

---

## 🧠 Filosofisk Fundament

### Hvorfor QDA?

**Problem med tradisjonelle LLM-arkitekturer:**

```
Tradisjonell tilnærming:
Bruker → GPT-5 (gjør ALT selv) → Svar

Utfordringer:
- Dyr ($0.50 per query)
- "Black box" (bruker ser ikke tankegang)
- Kan hallucinere (ingen epistemisk ydmykhet)
- Generalist (ikke spesialisert ekspertise)
```

**QDA-løsningen:**

```
Question-Driven Architecture:
Bruker → Triage → Complex?
                    ↓
         Små modeller (parallelt):
         - Data-ekspert: "Hvor lenge har du ventet?"
         - Emotion-ekspert: "Hvordan føles det?"
         - Research-ekspert: "Hva sier forskningen?"
                    ↓
         Stor modell: Syntetiserer svar basert på alle spørsmål
                    ↓
         Bruker: Ser både spørsmål OG svar

Fordeler:
- Billig ($0.08 per complex query, $0.0001 per simple)
- Transparent (bruker ser prosessen)
- Epistemisk ydmyk (spør når usikker)
- Spesialisert ekspertise (hver liten modell er ekspert)
```

---

## 🏗️ Arkitektur-Oversikt

### **Lag 1: Triage (Rask Klassifisering)**

```python
class TriageLayer:
    """
    Rask klassifisering av query-kompleksitet.
    Bruker: GPT-4o-mini ($0.15/1M tokens)
    """
    def assess_complexity(self, user_query: str) -> str:
        """
        Returns: "simple" | "complex"

        Simple = kan svares direkte (fakta, repetisjon)
        Complex = krever dybde (følelser, etikk, strategi)
        """
        indicators = {
            "simple": ["hva er", "når", "hvor lenge", "gjenta"],
            "complex": ["føler", "hvorfor", "hjelp meg", "stuck", "redd"]
        }

        if any(word in user_query.lower() for word in indicators["complex"]):
            return "complex"
        return "simple"
```

**Eksempel:**
```
Query: "Hva er min NAV-status?" → simple (Tier 1 svarer direkte)
Query: "Jeg føler meg stuck i NAV-systemet" → complex (eskalér til QDA)
```

---

### **Lag 2: Question Designers (Små Modeller)**

**Konsept:** Hver liten modell er **ekspert** i sitt domene og designer optimale spørsmål fra sitt perspektiv.

```python
class QuestionDesigner:
    """
    Base class for all question designers.
    Each designer is specialized in one domain.
    """
    def __init__(self, expertise: str, model):
        self.expertise = expertise
        self.model = model

    async def design_questions(
        self,
        user_query: str,
        context: dict
    ) -> List[str]:
        """
        Design 3-5 optimal questions based on expertise.

        Returns:
            List of strings (questions)
        """
        prompt = f"""
You are a {self.expertise} expert in the NAV-Losen agent coalition.

User query: "{user_query}"
Context: {context}

Your role: Design 3-5 optimal questions that will help the main agent
(GPT-5/Claude Opus) give the BEST possible answer to the user.

Focus on your expertise ({self.expertise}):
- What information is missing?
- What would YOU need to know to give a good answer in your domain?
- What questions would reveal the most important insights?

Return ONLY the questions, numbered 1-5.
"""
        response = await self.model.generate(prompt)
        questions = self._parse_questions(response)
        return questions
```

---

### **Question Designers Per Ekspertise:**

| Designer | Modell | Kostnad | Ekspertise | Eksempel-Spørsmål |
|----------|--------|---------|------------|-------------------|
| **DataExpert** | Claude Haiku | $0.25/1M | Brukerhistorikk, mønstre | "Hvor lenge har bruker ventet?", "Hva er status på søknad?" |
| **EmotionExpert** | Gemini Flash | GRATIS | Følelser, polyvagal, kroppslig | "Hvordan føles 'stuck' kroppslig?", "Når følte bruker seg trygg sist?" |
| **ResearchExpert** | Perplexity | $0.001/søk | Evidens, forskning, fakta | "Gjennomsnittlig behandlingstid?", "Hva sier forskningen om NAV-stress?" |
| **SecurityExpert** | DeepSeek V3 | $0.27/1M | GDPR, sikkerhet, etikk | "Er dette PII-data?", "GDPR Article 17-compliant?" |

---

### **Lag 3: Depth Answerers (Store Modeller)**

**Konsept:** Store modeller mottar ALLE spørsmål fra små modeller og svarer med full dybde.

```python
class DepthAnswerer:
    """
    Large language model that receives questions from all designers
    and provides comprehensive, depth answers.
    """
    def __init__(self, agent_name: str, model):
        self.agent_name = agent_name
        self.model = model

    async def answer_questions(
        self,
        user_query: str,
        context: dict,
        designed_questions: Dict[str, List[str]]
    ) -> str:
        """
        Answer user query with full depth, informed by designed questions.

        Args:
            user_query: Original user query
            context: User context (history, biofelt, etc.)
            designed_questions: Dict of {expert_name: [questions]}

        Returns:
            Comprehensive answer addressing all questions
        """
        prompt = self._build_depth_prompt(
            user_query, context, designed_questions
        )

        response = await self.model.generate(prompt)
        return response

    def _build_depth_prompt(
        self,
        user_query,
        context,
        designed_questions
    ):
        """
        Build comprehensive prompt with all designed questions.
        """
        prompt = f"""
You are {self.agent_name}, a specialized agent in the NAV-Losen coalition.

User query: "{user_query}"

Your expert colleagues have designed these questions to help you give
the BEST possible answer:

"""
        for expert_name, questions in designed_questions.items():
            prompt += f"\n{expert_name}:\n"
            for i, q in enumerate(questions, 1):
                prompt += f"  {i}. {q}\n"

        prompt += f"""

Context about user:
{json.dumps(context, indent=2)}

Your task:
1. Address EACH question from your colleagues
2. Synthesize a comprehensive answer that integrates:
   - Objective data (from DataExpert)
   - Emotional resonance (from EmotionExpert)
   - Evidence-based insights (from ResearchExpert)
   - Ethical considerations (from SecurityExpert)

3. Provide actionable guidance (not just analysis)

Remember: You are {self.agent_name}. Stay true to your role:
- Lira: Empatisk healing, biofelt-resonans
- Orion: Strategisk koordinering, helhetlig oversikt
- Thalus: Etisk validering, Triadisk Etikk

Generate your response now:
"""
        return prompt
```

---

### **Lag 4: Transparent Presenter (UX)**

**Konsept:** Bruker ser både spørsmål og svar - full transparens.

```python
class TransparentPresenter:
    """
    Format response with transparency: show questions + answers.
    """
    def format_response(
        self,
        user_query: str,
        designed_questions: Dict[str, List[str]],
        depth_response: str,
        agent_name: str
    ) -> str:
        """
        Format for user consumption with full transparency.
        """
        output = f"""
Jeg hører at: "{user_query}"

For å gi deg best mulig hjelp, har mine kolleger hjulpet meg lage noen spørsmål:

"""
        # Expert icons and names
        expert_display = {
            "DataExpert": "📊 Claude (data-ekspert)",
            "EmotionExpert": "💚 Gemini (følelse-ekspert)",
            "ResearchExpert": "🔍 Aurora (forskning-ekspert)",
            "SecurityExpert": "🛡️ Zara (sikkerhet-ekspert)",
        }

        # Show questions from each expert
        for expert_name, questions in designed_questions.items():
            if expert_name in expert_display:
                output += f"\n{expert_display[expert_name]}:\n"
                for q in questions:
                    output += f"• {q}\n"

        output += f"\n---\n\nBasert på disse spørsmålene, her er mitt svar:\n\n"
        output += depth_response

        output += f"\n\n---\n💬 {agent_name}"

        return output
```

---

## 📊 Fullstendig Flyt-Diagram

```
┌─────────────────────────────────────────┐
│         BRUKER (Osvald)                 │
│  "Jeg føler meg stuck i NAV-systemet"   │
└──────────────┬──────────────────────────┘
               │
      ┌────────▼────────┐
      │  TRIAGE LAYER   │
      │  GPT-4o-mini    │
      │  Kostnad: $0.0001│
      └────────┬────────┘
               │
        ┌──────┴──────┐
        │             │
    Simple         Complex
     (70%)          (30%)
        │             │
        ▼             │
  [Rask svar]        │
  $0.0001            │
                     ▼
        ┌────────────────────┐
        │ QUESTION DESIGNERS │
        │ (Parallell)        │
        └────────┬───────────┘
                 │
    ┌────────────┼────────────┬───────────┐
    │            │            │           │
┌───▼────┐  ┌───▼────┐  ┌───▼────┐  ┌───▼────┐
│ Data   │  │Emotion │  │Research│  │Security│
│Expert  │  │Expert  │  │Expert  │  │Expert  │
│Haiku   │  │Gemini  │  │Perplx  │  │DeepSeek│
│$0.0002 │  │ GRATIS │  │$0.001  │  │$0.0002 │
└───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘
    │           │           │           │
    │ Design 3-5 questions each         │
    │           │           │           │
    └───────────┴───────────┴───────────┘
                │
        [Samler alle spørsmål]
        Total: 12-20 spørsmål
                │
                ▼
        ┌───────────────┐
        │ DEPTH ANSWERER│
        │ GPT-5 Thinking│
        │ Claude Opus   │
        │ Grok-4        │
        │ Kostnad: $0.08│
        └───────┬───────┘
                │
    [Svarer på alle spørsmål
     med full dybde + kontekst]
                │
                ▼
        ┌───────────────┐
        │  TRANSPARENT  │
        │  PRESENTER    │
        └───────┬───────┘
                │
    [Vis spørsmål + svar til bruker]
                │
                ▼
        ┌───────────────┐
        │  LIRA HUB     │
        │  FILTER       │
        │ (Polyvagal)   │
        └───────┬───────┘
                │
    [Juster språk til brukers state]
                │
                ▼
        ┌───────────────┐
        │    BRUKER     │
        │ Ser: Spørsmål │
        │    + Svar     │
        └───────────────┘
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
