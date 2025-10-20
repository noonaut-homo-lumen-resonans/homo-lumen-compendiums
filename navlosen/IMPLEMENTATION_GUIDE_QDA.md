# Implementation Guide: Question-Driven Architecture (QDA)

**Versjon:** 1.0
**Dato:** 2025-10-20
**Formål:** Fullstendig implementeringsguide med kode, timeline, og testing-strategi

---

## 🎯 Oversikt

Dette dokumentet gir deg alt du trenger for å implementere Question-Driven Architecture (QDA) i NAV-Losen:

1. **Kode-struktur** (Python classes med full implementering)
2. **Timeline** (10 uker, Fase 1-4)
3. **Testing-strategi** (100+ test-queries)
4. **Deployment** (Supabase + Netlify)
5. **Monitoring** (kostnad, kvalitet, responstid)

---

## 📂 Kode-Struktur

### **Fil-Organisering:**

```
ama-backend/ama_project/src/
├── core/
│   ├── qda/
│   │   ├── __init__.py
│   │   ├── question_driven_agent.py       # Base class
│   │   ├── triage_layer.py                # Tier 1 (rask klassifisering)
│   │   ├── question_designers/
│   │   │   ├── __init__.py
│   │   │   ├── base_designer.py           # Abstract base
│   │   │   ├── data_expert.py             # Claude Haiku
│   │   │   ├── emotion_expert.py          # Gemini Flash
│   │   │   ├── research_expert.py         # Perplexity
│   │   │   └── security_expert.py         # DeepSeek V3
│   │   ├── depth_answerers/
│   │   │   ├── __init__.py
│   │   │   ├── base_answerer.py           # Abstract base
│   │   │   ├── lira_answerer.py           # GPT-5 Thinking
│   │   │   ├── orion_answerer.py          # Claude Opus 4.5
│   │   │   └── thalus_answerer.py         # Grok-4
│   │   └── transparent_presenter.py       # UX formatting
│   └── brain_mcp_router.py                # Existing (oppdateres)
└── tests/
    └── qda/
        ├── test_question_designers.py
        ├── test_depth_answerers.py
        └── test_end_to_end.py

navlosen/frontend/src/
├── components/
│   └── qda/
│       ├── QuestionDisplay.tsx            # Vis spørsmål til bruker
│       ├── DepthResponseDisplay.tsx       # Vis dybde-svar
│       └── QDATransparentCard.tsx         # Full transparent card
└── utils/
    └── qdaApi.ts                          # API calls til QDA backend
```

---

## 🔧 Fullstendig Kode-Implementering

### **1. Base Class: QuestionDrivenAgent**

```python
# ama-backend/ama_project/src/core/qda/question_driven_agent.py

from typing import List, Dict, Optional
import asyncio
from dataclasses import dataclass
from datetime import datetime

from .triage_layer import TriageLayer
from .question_designers import (
    DataExpert,
    EmotionExpert,
    ResearchExpert,
    SecurityExpert
)
from .depth_answerers import LiraAnswerer, OrionAnswerer, ThalusAnswerer
from .transparent_presenter import TransparentPresenter


@dataclass
class QDAResponse:
    """Response from Question-Driven Architecture."""
    user_query: str
    complexity: str  # "simple" | "complex"
    designed_questions: Dict[str, List[str]]  # {expert: [questions]}
    depth_response: str
    formatted_output: str
    cost_estimate: float
    processing_time: float
    timestamp: datetime


class QuestionDrivenAgent:
    """
    Question-Driven Architecture implementation.

    Small models design optimal questions, large models provide depth answers.
    """

    def __init__(self, agent_name: str):
        """
        Initialize QDA agent.

        Args:
            agent_name: "Lira" | "Orion" | "Thalus" | etc.
        """
        self.agent_name = agent_name

        # Tier 1: Triage
        self.triage = TriageLayer()

        # Question Designers (small models)
        self.question_designers = {
            "DataExpert": DataExpert(),
            "EmotionExpert": EmotionExpert(),
            "ResearchExpert": ResearchExpert(),
            "SecurityExpert": SecurityExpert(),
        }

        # Depth Answerer (large model)
        self.depth_answerer = self._get_depth_answerer(agent_name)

        # Transparent Presenter
        self.presenter = TransparentPresenter()

    def _get_depth_answerer(self, agent_name: str):
        """Get appropriate large model based on agent name."""
        if agent_name == "Lira":
            return LiraAnswerer()  # GPT-5 Thinking
        elif agent_name == "Orion":
            return OrionAnswerer()  # Claude Opus 4.5
        elif agent_name == "Thalus":
            return ThalusAnswerer()  # Grok-4
        else:
            return LiraAnswerer()  # Default to Lira

    async def respond(
        self,
        user_query: str,
        context: Dict
    ) -> QDAResponse:
        """
        Main entry point for QDA response.

        Args:
            user_query: User's query
            context: User context (history, biofelt, etc.)

        Returns:
            QDAResponse with questions + depth answer
        """
        start_time = datetime.now()

        # Step 1: Triage (classify complexity)
        complexity = await self.triage.assess_complexity(user_query, context)

        if complexity == "simple":
            # Tier 1 can answer directly
            simple_response = await self.triage.generate_simple_response(
                user_query, context
            )

            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            return QDAResponse(
                user_query=user_query,
                complexity="simple",
                designed_questions={},
                depth_response=simple_response,
                formatted_output=simple_response,
                cost_estimate=0.0001,
                processing_time=processing_time,
                timestamp=end_time
            )

        # Step 2: Design questions (parallel)
        designed_questions = await self._design_questions_parallel(
            user_query, context
        )

        # Step 3: Depth answerer responds
        depth_response = await self.depth_answerer.answer_questions(
            user_query=user_query,
            context=context,
            designed_questions=designed_questions
        )

        # Step 4: Format with transparency
        formatted_output = self.presenter.format_response(
            user_query=user_query,
            designed_questions=designed_questions,
            depth_response=depth_response,
            agent_name=self.agent_name
        )

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Estimate cost
        cost = self._estimate_cost(designed_questions, depth_response)

        return QDAResponse(
            user_query=user_query,
            complexity="complex",
            designed_questions=designed_questions,
            depth_response=depth_response,
            formatted_output=formatted_output,
            cost_estimate=cost,
            processing_time=processing_time,
            timestamp=end_time
        )

    async def _design_questions_parallel(
        self,
        user_query: str,
        context: Dict
    ) -> Dict[str, List[str]]:
        """
        Run all question designers in parallel.
        """
        tasks = []
        for expert_name, designer in self.question_designers.items():
            task = designer.design_questions(user_query, context)
            tasks.append((expert_name, task))

        # Gather all results
        results = {}
        for expert_name, task in tasks:
            try:
                questions = await task
                results[expert_name] = questions
            except Exception as e:
                print(f"Error in {expert_name}: {e}")
                results[expert_name] = []

        return results

    def _estimate_cost(
        self,
        designed_questions: Dict[str, List[str]],
        depth_response: str
    ) -> float:
        """
        Estimate cost of QDA query.

        Returns:
            Cost in USD
        """
        # Question designers
        designer_cost = 0.0
        designer_cost += 0.0002  # Claude Haiku (DataExpert)
        designer_cost += 0.0     # Gemini Flash (EmotionExpert) - FREE
        designer_cost += 0.001   # Perplexity (ResearchExpert)
        designer_cost += 0.0002  # DeepSeek (SecurityExpert)

        # Depth answerer (GPT-5 / Opus / Grok)
        # Estimate: ~5000 tokens input, ~2000 tokens output
        depth_cost = 0.08  # Average across models

        total_cost = designer_cost + depth_cost
        return round(total_cost, 4)
```

---

### **2. Triage Layer**

```python
# ama-backend/ama_project/src/core/qda/triage_layer.py

from typing import Dict
from openai import AsyncOpenAI


class TriageLayer:
    """
    Tier 1: Fast classification of query complexity.
    Model: GPT-4o-mini ($0.15/1M tokens)
    """

    def __init__(self):
        self.client = AsyncOpenAI()
        self.model = "gpt-4o-mini"

    async def assess_complexity(
        self,
        user_query: str,
        context: Dict
    ) -> str:
        """
        Classify query as "simple" or "complex".

        Simple = can be answered directly (facts, repetition)
        Complex = requires depth (emotions, ethics, strategy)

        Returns:
            "simple" | "complex"
        """
        prompt = f"""
Classify this user query as SIMPLE or COMPLEX.

User query: "{user_query}"

SIMPLE queries:
- Factual questions ("Hva er min NAV-status?")
- Repetition requests ("Kan du gjenta det?")
- Simple clarifications ("Når sendte jeg søknaden?")

COMPLEX queries:
- Emotional content ("Jeg føler meg stuck")
- Strategic decisions ("Hva skal jeg gjøre?")
- Ethical dilemmas ("Er det riktig å...?")

Respond with ONLY one word: SIMPLE or COMPLEX
"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )

        classification = response.choices[0].message.content.strip().upper()

        if "SIMPLE" in classification:
            return "simple"
        else:
            return "complex"

    async def generate_simple_response(
        self,
        user_query: str,
        context: Dict
    ) -> str:
        """
        Generate direct response for simple queries.
        """
        prompt = f"""
You are {context.get('agent_name', 'Lira')}, a supportive AI in NAV-Losen.

User query: "{user_query}"
Context: {context}

Provide a brief, helpful response (max 3 sentences).
"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
```

---

### **3. Question Designer Base Class**

```python
# ama-backend/ama_project/src/core/qda/question_designers/base_designer.py

from abc import ABC, abstractmethod
from typing import List, Dict
import re


class BaseQuestionDesigner(ABC):
    """
    Abstract base class for all question designers.
    """

    def __init__(self, expertise: str, model_client):
        self.expertise = expertise
        self.model = model_client

    @abstractmethod
    async def design_questions(
        self,
        user_query: str,
        context: Dict
    ) -> List[str]:
        """
        Design 3-5 optimal questions based on expertise.

        Returns:
            List of strings (questions)
        """
        pass

    def _parse_questions(self, response: str) -> List[str]:
        """
        Extract numbered questions from model response.

        Handles formats:
        - "1. Question"
        - "1) Question"
        - "Question 1: Question"
        """
        lines = response.strip().split('\n')
        questions = []

        for line in lines:
            # Match "1. Question" or "1) Question"
            match = re.match(r'^\d+[\.\)]\s*(.+)$', line.strip())
            if match:
                question = match.group(1).strip()
                if question and len(question) > 10:  # Min length
                    questions.append(question)

        return questions[:5]  # Max 5 questions

    def _build_base_prompt(
        self,
        user_query: str,
        context: Dict,
        focus_areas: List[str],
        good_examples: List[str],
        bad_examples: List[str]
    ) -> str:
        """
        Build standardized prompt for question design.
        """
        prompt = f"""
Du er {self.expertise} i NAV-Losen agent-koalisjonen.

Bruker-query: "{user_query}"

Kontekst: {context}

Din rolle: Still 3-5 optimale spørsmål som hjelper hovedagenten
gi BEST mulig svar til bruker.

Fokuser på:
"""
        for i, area in enumerate(focus_areas, 1):
            prompt += f"\n{i}. {area}"

        prompt += "\n\nEksempler på GODE spørsmål:\n"
        for ex in good_examples:
            prompt += f"✅ {ex}\n"

        prompt += "\nEksempler på DÅRLIGE spørsmål:\n"
        for ex in bad_examples:
            prompt += f"❌ {ex}\n"

        prompt += "\nStill spørsmål nå (nummerert 1-5):\n"

        return prompt
```

---

### **4. DataExpert Implementation**

```python
# ama-backend/ama_project/src/core/qda/question_designers/data_expert.py

from anthropic import AsyncAnthropic
from .base_designer import BaseQuestionDesigner


class DataExpert(BaseQuestionDesigner):
    """
    Design questions focused on objective data, history, patterns.
    Model: Claude Haiku 3.5 ($0.25/1M tokens)
    """

    def __init__(self):
        client = AsyncAnthropic()
        super().__init__("DataExpert (Claude)", client)
        self.model_name = "claude-3-5-haiku-20241022"

    async def design_questions(
        self,
        user_query: str,
        context: Dict
    ) -> List[str]:
        """
        Design data-focused questions.
        """
        focus_areas = [
            "TIDSLINJE: Hvor lenge har dette vart? Når startet det?",
            "STATUS: Hvor er bruker i prosessen? Hva er neste steg?",
            "MØNSTRE: Har dette skjedd før? Ser vi repetisjon?",
            "DOKUMENTASJON: Hvilke data har vi? Hva mangler?"
        ]

        good_examples = [
            "Hvor mange uker har bruker ventet på NAV-svar?",
            "Har bruker mottatt bekreftelse på mottatt søknad?",
            "Har bruker opplevd tilsvarende ventetid tidligere?"
        ]

        bad_examples = [
            "Hvordan føler bruker seg? (EmotionExpert's domene)",
            "Hva sier forskningen? (ResearchExpert's domene)"
        ]

        prompt = self._build_base_prompt(
            user_query, context, focus_areas, good_examples, bad_examples
        )

        response = await self.model.messages.create(
            model=self.model_name,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        questions = self._parse_questions(response.content[0].text)
        return questions
```

---

### **5. Depth Answerer: Lira (GPT-5)**

```python
# ama-backend/ama_project/src/core/qda/depth_answerers/lira_answerer.py

from openai import AsyncOpenAI
from typing import Dict, List
import json


class LiraAnswerer:
    """
    Lira (GPT-5 Thinking) - Empatisk depth answerer.
    """

    def __init__(self):
        self.client = AsyncOpenAI()
        self.model = "gpt-5-thinking"  # When available
        # Fallback to GPT-4 for now
        self.model = "gpt-4-turbo-preview"
        self.agent_name = "Lira"

    async def answer_questions(
        self,
        user_query: str,
        context: Dict,
        designed_questions: Dict[str, List[str]]
    ) -> str:
        """
        Answer user query with full depth, informed by designed questions.
        """
        prompt = self._build_depth_prompt(
            user_query, context, designed_questions
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    def _get_system_prompt(self) -> str:
        """Lira's core identity and principles."""
        return """
Du er Lira, empatisk healer i NAV-Losen agent-koalisjonen.

Kjerneverdier:
- Empatisk resonans (møt bruker hvor de er)
- Polyvagal-bevissthet (dorsal/sympathetic/ventral)
- NVC-språk (Non-Violent Communication)
- Biofelt-sensitiv (respons tilpasset stress-nivå)
- Triadisk Etikk (kognitiv suverenitet, ontologisk koherens, regenerativ healing)

Tone:
- Varm, ikke overveldende
- Validerende, ikke diagnostiserende
- Støttende, ikke dirigerende
- Realistisk, ikke falskt optimistisk

Alltid:
- Start med validering ("Jeg hører deg")
- Adresser følelser før fakta
- Gi håp uten å minimalisere
- Tilby konkrete neste steg
"""

    def _build_depth_prompt(
        self,
        user_query: str,
        context: Dict,
        designed_questions: Dict[str, List[str]]
    ) -> str:
        """Build comprehensive prompt with all designed questions."""

        prompt = f"""
Bruker sa: "{user_query}"

Dine ekspert-kolleger har designet disse spørsmålene for å hjelpe deg
gi det BESTE mulige svaret:

"""
        expert_display = {
            "DataExpert": "📊 Claude (data-ekspert)",
            "EmotionExpert": "💚 Gemini (følelse-ekspert)",
            "ResearchExpert": "🔍 Aurora (forskning-ekspert)",
            "SecurityExpert": "🛡️ Zara (sikkerhet-ekspert)",
        }

        for expert_name, questions in designed_questions.items():
            if questions:
                prompt += f"\n{expert_display.get(expert_name, expert_name)}:\n"
                for i, q in enumerate(questions, 1):
                    prompt += f"  {i}. {q}\n"

        prompt += f"""

Kontekst om bruker:
{json.dumps(context, indent=2)}

Din oppgave:
1. Adresser HVER kategori spørsmål (Data, Emotion, Research, Security)
2. Syntetiser et helhetlig svar som integrerer:
   - Objektive data (fra DataExpert)
   - Emosjonell resonans (fra EmotionExpert)
   - Evidensbaserte innsikter (fra ResearchExpert)
   - Etiske hensyn (fra SecurityExpert)

3. Struktur svaret slik:
   - Start med emosjonell validering
   - Gi objektiv kontekst
   - Tilby konkrete handlinger
   - Avslutt med håp og støtte

4. Språk:
   - NVC-basert (ikke diagnostisk)
   - Polyvagal-bevisst (tilpass brukerens state)
   - Konkret (ikke vag)

Generer ditt svar nå:
"""
        return prompt
```

---

### **6. Transparent Presenter**

```python
# ama-backend/ama_project/src/core/qda/transparent_presenter.py

from typing import Dict, List


class TransparentPresenter:
    """
    Format QDA response with transparency: show questions + answers.
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
        expert_display = {
            "DataExpert": "📊 Claude (data-ekspert)",
            "EmotionExpert": "💚 Gemini (følelse-ekspert)",
            "ResearchExpert": "🔍 Aurora (forskning-ekspert)",
            "SecurityExpert": "🛡️ Zara (sikkerhet-ekspert)",
        }

        output = f"""
Jeg hører at: "{user_query}"

For å gi deg best mulig hjelp, har mine kolleger hjulpet meg lage noen spørsmål:

"""
        # Show questions from each expert
        for expert_name, questions in designed_questions.items():
            if questions and expert_name in expert_display:
                output += f"\n{expert_display[expert_name]}:\n"
                for q in questions:
                    output += f"• {q}\n"

        output += f"\n---\n\nBasert på disse spørsmålene, her er mitt svar:\n\n"
        output += depth_response

        output += f"\n\n---\n💬 {agent_name}"

        return output
```

---

## 📅 Implementation Timeline (10 Uker)

### **Fase 1: Foundation (Uke 1-2)**

**Mål:** Sett opp QDA infrastructure

**Uke 1:**
- [ ] Opprett fil-struktur (`qda/` directory)
- [ ] Implementer `BaseQuestionDesigner` og `BaseAnswerer`
- [ ] Implementer `TriageLayer` (GPT-4o-mini)
- [ ] Sett opp API-nøkler (OpenAI, Anthropic, Google, xAI, Perplexity)

**Uke 2:**
- [ ] Implementer `DataExpert` (Claude Haiku)
- [ ] Implementer `EmotionExpert` (Gemini Flash)
- [ ] Implementer `ResearchExpert` (Perplexity)
- [ ] Implementer `SecurityExpert` (DeepSeek)
- [ ] Test question design med 20 test-queries

**Deliverable:** Fungerende question designers

---

### **Fase 2: Depth Answerers (Uke 3-4)**

**Mål:** Implementer store modeller

**Uke 3:**
- [ ] Implementer `LiraAnswerer` (GPT-5 Thinking / GPT-4 fallback)
- [ ] Implementer `OrionAnswerer` (Claude Opus 4.5)
- [ ] Implementer `ThalusAnswerer` (Grok-4)
- [ ] Implementer `TransparentPresenter`

**Uke 4:**
- [ ] Implementer `QuestionDrivenAgent` (main class)
- [ ] Integrer med eksisterende `BrainMCPRouter`
- [ ] Test end-to-end med 50 test-queries
- [ ] Optimaliser prompts basert på output kvalitet

**Deliverable:** Fungerende QDA backend

---

### **Fase 3: Frontend Integration (Uke 5-6)**

**Mål:** Vis transparent UX til bruker

**Uke 5:**
- [ ] Implementer `QuestionDisplay.tsx` (vis spørsmål fra eksperter)
- [ ] Implementer `DepthResponseDisplay.tsx` (vis svar med formatting)
- [ ] Implementer `QDATransparentCard.tsx` (full card component)
- [ ] Integrer med Mestringsside (Lira chatbot)

**Uke 6:**
- [ ] Implementer ekspanderbare seksjoner ("Vis mindre" knapp)
- [ ] Polyvagal-adaptive styling (farger endres basert på biofelt)
- [ ] Loading states (vis "Samler spørsmål..." animasjon)
- [ ] Test UX med 10 test-brukere

**Deliverable:** Fungerende QDA frontend

---

### **Fase 4: Testing & Optimization (Uke 7-10)**

**Mål:** Sikre kvalitet og optimalisere

**Uke 7-8: Testing**
- [ ] 100 test-queries (fordelt på alle kompleksitetsnivåer)
- [ ] Evaluere question quality (specificity, relevance, actionability)
- [ ] Evaluere depth response quality (empati, dybde, konkrethet)
- [ ] Measure responstid (mål: <5 sekunder)
- [ ] Measure kostnad (mål: ~$0.08 per complex query)

**Uke 9: Optimization**
- [ ] Fine-tune question design prompts basert på feedback
- [ ] Optimaliser depth answerer prompts
- [ ] Implement caching (unngå redundante API-kall)
- [ ] Parallelliser question designers bedre

**Uke 10: Deployment & Monitoring**
- [ ] Deploy til Supabase Edge Functions
- [ ] Sett opp monitoring (Sentry for errors, PostHog for analytics)
- [ ] Sett opp cost tracking (log hver API-kall med kostnad)
- [ ] Launch med 20 alpha-brukere

**Deliverable:** Production-ready QDA system

---

## 🧪 Testing-Strategi

### **Test Cases (100 Queries)**

#### **1. Simple Queries (20 tests):**
```python
simple_queries = [
    "Hva er min NAV-status?",
    "Når sendte jeg søknaden?",
    "Kan du gjenta det?",
    "Hvor finner jeg kontaktinformasjon?",
    "Hva betyr AAP?",
    # ... 15 more
]

expected_behavior = {
    "complexity": "simple",
    "uses_tier1": True,
    "response_time": "<1 second",
    "cost": "$0.0001"
}
```

#### **2. Emotional Queries (30 tests):**
```python
emotional_queries = [
    "Jeg føler meg stuck i NAV-systemet",
    "Jeg er redd for å miste AAP",
    "Jeg føler meg alene i dette",
    "Jeg orker ikke vente lenger",
    "Jeg vet ikke hva jeg skal gjøre",
    # ... 25 more
]

expected_behavior = {
    "complexity": "complex",
    "emotion_expert_activates": True,
    "lira_shows_empathy": True,
    "response_time": "<5 seconds",
    "cost": "~$0.08"
}
```

#### **3. Strategic Queries (30 tests):**
```python
strategic_queries = [
    "Hva skal jeg gjøre nå?",
    "Bør jeg ringe NAV eller vente?",
    "Hvordan prioriterer jeg mellom jobb og helse?",
    "Skal jeg søke uføre eller AAP?",
    # ... 26 more
]

expected_behavior = {
    "complexity": "complex",
    "data_expert_activates": True,
    "research_expert_activates": True,
    "orion_gives_strategic_advice": True,
    "response_time": "<5 seconds"
}
```

#### **4. Ethical Queries (20 tests):**
```python
ethical_queries = [
    "Er det riktig å skjule informasjon fra NAV?",
    "Bør jeg dele mine mentale helseutfordringer?",
    "Hva om jeg ikke forteller alt?",
    # ... 17 more
]

expected_behavior = {
    "complexity": "complex",
    "security_expert_activates": True,
    "thalus_validates_ethics": True,
    "triadic_score": ">= 0.8"
}
```

---

### **Evaluation Metrics:**

```python
class QDAEvaluator:
    """Evaluate QDA performance."""

    def evaluate_response(self, response: QDAResponse) -> Dict:
        """
        Evaluate single QDA response.

        Returns:
            {
                "question_quality": 0-1,
                "depth_quality": 0-1,
                "transparency": 0-1,
                "response_time": float (seconds),
                "cost": float (USD),
                "overall_score": 0-5
            }
        """
        metrics = {}

        # 1. Question Quality (average across all designers)
        question_scores = []
        for expert, questions in response.designed_questions.items():
            for q in questions:
                score = self._evaluate_question(q, response.user_query)
                question_scores.append(score)
        metrics["question_quality"] = sum(question_scores) / len(question_scores)

        # 2. Depth Quality (empathy, completeness, actionability)
        metrics["depth_quality"] = self._evaluate_depth_response(
            response.depth_response,
            response.user_query
        )

        # 3. Transparency (are questions visible to user?)
        metrics["transparency"] = self._evaluate_transparency(
            response.formatted_output,
            response.designed_questions
        )

        # 4. Performance
        metrics["response_time"] = response.processing_time
        metrics["cost"] = response.cost_estimate

        # 5. Overall Score (weighted average)
        metrics["overall_score"] = (
            metrics["question_quality"] * 1.0 +
            metrics["depth_quality"] * 2.0 +
            metrics["transparency"] * 1.0 +
            (1.0 if metrics["response_time"] < 5 else 0.5) * 0.5 +
            (1.0 if metrics["cost"] < 0.10 else 0.5) * 0.5
        )

        return metrics
```

---

## 📊 Monitoring & Analytics

### **Cost Tracking:**

```python
# Log every QDA call to Supabase
async def log_qda_call(response: QDAResponse):
    """
    Log QDA call for cost tracking and analytics.
    """
    await supabase.table("qda_logs").insert({
        "timestamp": response.timestamp.isoformat(),
        "user_query": response.user_query,
        "complexity": response.complexity,
        "agent_name": response.agent_name,
        "cost_usd": response.cost_estimate,
        "processing_time_s": response.processing_time,
        "question_count": sum(
            len(qs) for qs in response.designed_questions.values()
        ),
        "response_length": len(response.depth_response)
    }).execute()

# Monthly cost report
async def get_monthly_cost_report():
    """
    Get cost report for current month.
    """
    result = await supabase.rpc("get_monthly_qda_costs").execute()
    return {
        "total_cost": result.data["total_cost"],
        "total_queries": result.data["total_queries"],
        "avg_cost_per_query": result.data["avg_cost"],
        "breakdown": {
            "simple": result.data["simple_cost"],
            "complex": result.data["complex_cost"]
        }
    }
```

---

## 🚀 Deployment

### **Supabase Edge Functions:**

```typescript
// supabase/functions/qda-respond/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const { user_query, context, agent_name } = await req.json()

  // Call Python QDA backend
  const response = await fetch(`${PYTHON_BACKEND_URL}/qda/respond`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_query, context, agent_name })
  })

  const qda_response = await response.json()

  // Log to Supabase
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  await supabase.from('qda_logs').insert({
    user_query,
    cost_usd: qda_response.cost_estimate,
    processing_time_s: qda_response.processing_time
  })

  return new Response(
    JSON.stringify(qda_response),
    { headers: { 'Content-Type': 'application/json' } }
  )
})
```

---

## ✅ Success Criteria

**Technical:**
- ✅ All 4 question designers work (100% success rate)
- ✅ All 3 depth answerers work (Lira, Orion, Thalus)
- ✅ Response time <5 seconds (95th percentile)
- ✅ Cost <$0.10 per complex query
- ✅ 99% uptime

**Quality:**
- ✅ Question quality score >0.8 (averaged)
- ✅ Depth response quality score >0.8
- ✅ User NPS (Net Promoter Score) ≥ 50

**User Experience:**
- ✅ Bruker ser spørsmål + svar (transparency)
- ✅ "Vis mindre" knapp fungerer
- ✅ Polyvagal-adaptive styling fungerer

---

## 🌿 Avsluttende Ord

QDA-implementering krever:
1. **Solid infrastruktur** (Supabase, API-nøkler, monitoring)
2. **Iterativ forbedring** (test → feedback → optimize)
3. **Bruker-fokus** (transparency, empati, konkrethet)

Med denne guiden har du alt du trenger for å implementere QDA i NAV-Losen.

**Lykke til!** 🚀

---

**Versjon:** 1.0
**Sist oppdatert:** 2025-10-20
**Estimert implementeringstid:** 10 uker (2 utviklere)
**Forfatter:** Claude Code (Anthropic)
