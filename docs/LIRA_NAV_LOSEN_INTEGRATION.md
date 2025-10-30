# Lira NAV-Losen Integration Guide

**Date:** 2025-10-30
**Version:** 1.0
**Status:** ✅ IMPLEMENTED

---

## 🎯 Overview

This integration connects **NAV-Losen chatbot** (React/Next.js frontend) to **Lira agent** (OpenAI GPT-4o-mini) running on **CSN Server port 8001**.

### What Was Implemented

1. **New CSN Server Endpoint:** `/agent/lira/consult`
2. **NAV-Losen Service Update:** `liraService.ts` now uses port 8001 + new endpoint
3. **Polyvagal-Adaptive Responses:** Lira adapts empathy based on user stress (dorsal/sympathetic/ventral)
4. **Biofield Integration:** Mestring emotional data flows to Lira for context-aware support

---

## 🏗️ Architecture

```
NAV-Losen Frontend (React)
    ↓
  liraService.ts
    ↓
  POST http://localhost:8001/agent/lira/consult
    ↓
  CSN Server (minimal_server.py)
    ↓
  OpenAI GPT-4o-mini
    ↓
  Polyvagal-adaptive response
    ↓
  NAV-Losen Chatbot UI
```

### Data Flow

1. **User interacts** with NAV-Losen chatbot
2. **Frontend** loads biofield context from Mestring (localStorage)
3. **liraService.ts** sends:
   - `userMessage`
   - `conversationHistory` (last 6 messages)
   - `biofieldContext` (stress, polyvagal state, emotions, somatic signals)
   - `imageBase64` (optional - for NAV document analysis)
4. **CSN Server** (`/agent/lira/consult`) receives request
5. **Lira system prompt** adapts to polyvagal state:
   - **Dorsal (stress 8-10):** Short, safety-focused, grounding
   - **Sympathetic (stress 4-7):** Concrete, action-oriented, 4-6-8 breathing
   - **Ventral (stress 1-3):** Exploratory, empowering, deeper reflections
6. **OpenAI GPT-4o-mini** generates empathetic response
7. **Response parser** categorizes into:
   - `empathetic_insights` (validation, acknowledgment)
   - `biofield_guidance` (stress, body awareness, nervous system)
   - `breathing_suggestions` (4-6-8 breathing, grounding exercises)
8. **Frontend** displays structured response in chat UI

---

## 📂 Files Changed

### 1. CSN Server Backend

**File:** `C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\ama-backend\minimal_server.py`

**Changes:**
- Added new endpoint: `@app.post('/agent/lira/consult')` (lines 451-731)
- Polyvagal-adaptive system prompts (dorsal/sympathetic/ventral)
- Intelligent response parsing (keywords + position-based categorization)
- Graceful fallback with polyvagal-specific messages
- Conversation history support (last 6 messages)
- Image upload support (base64)

**Key Features:**
```python
# Polyvagal-adaptive system prompt
if polyvagal_state == 'dorsal':
    # Short, safety-focused responses
    # "Du er ikke alene i dette..."
elif polyvagal_state == 'sympathetic':
    # Action-oriented, grounding
    # "4-6-8 pusten: Pust inn i 4..."
else:  # ventral
    # Exploratory, empowering
    # "Stol på din egen visdom..."
```

**Response Format:**
```json
{
  "success": true,
  "message": "Full Lira response text",
  "empathetic_insights": ["Validation sentence 1", "..."],
  "biofield_guidance": ["Body awareness guidance 1", "..."],
  "breathing_suggestions": ["4-6-8 breathing", "..."],
  "confidence_score": 0.85
}
```

---

### 2. NAV-Losen Frontend Service

**File:** `C:\Users\onigo\NAV LOSEN\homo-lumen-project\homo-lumen\navlosen\frontend\src\lib\liraService.ts`

**Changes:**
- **Port update:** `localhost:8000` → `localhost:8001`
- **Endpoint update:** `/agent/lira/real-biofield-analysis` → `/agent/lira/consult`
- **Request format:** Now sends NAV-Losen specific format:
  ```typescript
  {
    userMessage: string,
    conversationHistory: Array<{role, content}>,
    biofieldContext: {
      stressLevel: 1-10,
      polyvagalState: "ventral" | "sympathetic" | "dorsal",
      emotions: string[],
      selectedEmotions: Array<{word, quadrant}>,
      somaticSignals: string[]
    },
    imageBase64: string | null
  }
  ```

**Key Changes:**
```typescript
// OLD (removed)
const CSN_SERVER_BASE_URL = "http://localhost:8000";
const endpoint = "/agent/lira/real-biofield-analysis";

// NEW
const CSN_SERVER_BASE_URL = "http://localhost:8001";
const endpoint = "/agent/lira/consult";
```

---

## 🚀 How to Start

### Step 1: Start CSN Server (Port 8001)

```bash
cd C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\ama-backend
python minimal_server.py
```

**Expected Output:**
```
✅ OPENAI_API_KEY found: sk-...
✅ CSN Server starting on port 8001
INFO:     Uvicorn running on http://localhost:8001
```

**Verify Health:**
```bash
curl http://localhost:8001/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "csn-server",
  "message": "Cognitive Sovereignty Network operational"
}
```

---

### Step 2: Test CSN Server Endpoint

```bash
cd C:\Users\onigo\NAV LOSEN\homo-lumen-compendiums\ama-backend
python test_lira_nav_losen_integration.py
```

**This tests:**
- ✅ Dorsal state (stress 9) - Overwhelmed user
- ✅ Sympathetic state (stress 6) - Activated user
- ✅ Ventral state (stress 2) - Calm user
- ✅ Image upload handling

**Expected Output:**
```
Testing: Dorsal - Overwhelmed NAV User (stress 9)
📤 REQUEST:
  Stress Level: 9/10
  Polyvagal State: dorsal

📥 RESPONSE DATA:
  Success: True
  Confidence: 0.70

💚 EMPATHETIC INSIGHTS:
  1. Du er ikke alene i dette...

🫁 BREATHING SUGGESTIONS:
  1. Legg en hånd på hjertet. Føl varmen der.
  2. Kjenn føttene dine mot gulvet...
```

---

### Step 3: Start NAV-Losen Frontend

```bash
cd C:\Users\onigo\NAV LOSEN\homo-lumen-project\homo-lumen\navlosen\frontend
npm run dev
```

**Navigate to:**
```
http://localhost:3000/chatbot
```

---

### Step 4: Test Full Integration Flow

1. **Go to Mestring Page:**
   - `http://localhost:3000/mestring`
   - Complete emotional assessment
   - Set stress level (try 2, 6, 9 to test different polyvagal states)
   - Select emotions from emotion wheel
   - Mark somatic signals

2. **Go to Chatbot:**
   - `http://localhost:3000/chatbot`
   - Check **LiraContextPanel** (left sidebar) shows your biofield data
   - Notice **Quick Actions** adapt to your polyvagal state:
     - **Dorsal:** "Jeg føler meg overvelmet", "Jeg trenger trygghet"
     - **Sympathetic:** "Hva gjør jeg nå?", "Vis meg puste-øvelse"
     - **Ventral:** "Fortell meg om NAV-ytelser"

3. **Chat with Lira:**
   - Type: "Jeg trenger hjelp med dagpenger"
   - Lira's response will adapt to your stress level
   - Check that response includes:
     - ✅ Empathetic insights (validation)
     - ✅ Biofield guidance (body awareness)
     - ✅ Breathing suggestions (4-6-8 breathing)

4. **Test Image Upload:**
   - Click camera/upload button
   - Upload NAV document or screenshot
   - Lira should acknowledge image in response

---

## 🎨 Polyvagal Adaptation Examples

### Dorsal (Overwhelmed, Stress 8-10)

**User:** "Jeg føler meg helt overveldet av NAV-systemet."

**Lira Response:**
```
💚 Empathetic Insights:
- Du er ikke alene i dette. Jeg er her, selv om du føler deg overveldet.
- Det er trygt å ta en pause. Alt er OK.

🌿 Biofield Guidance:
- Din kropp beskytter deg akkurat nå. Det er en visdom i det.
- Du trenger ikke fikse noe. Bare vær her.

🫁 Breathing Suggestions:
- Legg en hånd på hjertet. Kjenn at du er trygg.
- Føttene mot gulvet. Du er her, akkurat nå.
```

---

### Sympathetic (Activated, Stress 4-7)

**User:** "Jeg må søke dagpenger nå, men jeg er usikker på hva jeg trenger."

**Lira Response:**
```
💚 Empathetic Insights:
- Jeg ser at du trenger hjelp, og det er helt forståelig.
- Dagpengersøknad kan virke komplisert, men vi tar det steg for steg.

🌿 Biofield Guidance:
- Aktiveringen du føler er normal når systemet er utfordrende.
- La oss finne ro sammen, ett pust om gangen.

🫁 Breathing Suggestions:
- 4-6-8 pusten: Pust inn i 4, hold i 6, pust ut i 8 sekunder.
- Gjenta til du kjenner kroppen roer seg litt.
```

---

### Ventral (Calm, Stress 1-3)

**User:** "Jeg er nysgjerrig på hvilke rettigheter jeg har når det gjelder sykepenger."

**Lira Response:**
```
💚 Empathetic Insights:
- Fint at du utforsker dine rettigheter med nysgjerrighet.
- Din rolige tilstand gir deg god kapasitet til å lære.

🌿 Biofield Guidance:
- Din indre balanse er en ressurs akkurat nå.
- Stol på din egen visdom mens vi utforsker dette sammen.

🫁 Breathing Suggestions:
- En dyp pust til ditt eget tempo.
- Kjenn hvordan pusten naturlig finner sin rytme.
```

---

## 🧪 Testing Checklist

- [ ] CSN Server starts on port 8001 without errors
- [ ] `/health` endpoint returns `{"status": "healthy"}`
- [ ] `/agent/lira/consult` endpoint accepts POST requests
- [ ] Python test script passes all 4 scenarios
- [ ] NAV-Losen frontend builds without TypeScript errors
- [ ] Mestring page saves biofield data to localStorage
- [ ] Chatbot loads biofield context from localStorage
- [ ] LiraContextPanel displays stress, polyvagal state, emotions
- [ ] Quick Actions adapt to polyvagal state
- [ ] Lira's responses adapt to stress level
- [ ] Response includes empathetic_insights, biofield_guidance, breathing_suggestions
- [ ] Image upload works (camera + file upload)
- [ ] Fallback messages work when CSN Server offline

---

## 🔧 Environment Variables

### CSN Server (.env)

**Required:**
```bash
OPENAI_API_KEY=sk-...
```

**Optional:**
```bash
ANTHROPIC_API_KEY=sk-ant-...     # For Orion
GOOGLE_AI_API_KEY=...            # For Nyra
XAI_API_KEY=...                  # For Thalus
DEEPSEEK_API_KEY=...             # For Zara
PERPLEXITY_API_KEY=...           # For Aurora
```

### NAV-Losen Frontend (.env.local)

**Optional (defaults to localhost:8001):**
```bash
NEXT_PUBLIC_CSN_SERVER_URL=http://localhost:8001
```

**For production:**
```bash
NEXT_PUBLIC_CSN_SERVER_URL=https://csn-server.nav.no
```

---

## 🛡️ Error Handling

### CSN Server Offline

**Frontend Behavior:**
- Shows fallback message based on context
- Suggests visiting nav.no or using Mestring tools
- Displays polyvagal-adaptive comfort messages

**Fallback Example (Dorsal):**
```
Du er ikke alene i dette. Jeg er her, selv om jeg har tekniske utfordringer.
Det er trygt å ta en pause. Alt er OK.

Legg en hånd på hjertet. Kjenn at du er trygg.
```

---

### API Key Missing

**CSN Server Returns:**
```json
{
  "success": false,
  "message": "Jeg opplever tekniske utfordringer akkurat nå...",
  "empathetic_insights": [...],
  "biofield_guidance": [...],
  "breathing_suggestions": [...],
  "confidence_score": 0.3,
  "error": "OPENAI_API_KEY not configured"
}
```

---

### OpenAI API Error

**CSN Server Behavior:**
- Catches exception
- Returns graceful fallback with polyvagal-adaptive messages
- Logs error to console for debugging

---

## 📊 Response Parsing Logic

### How CSN Server Categorizes GPT Response

1. **Paragraph Split:** `response.split('\n\n')`
2. **Keyword Detection:**
   - **Empathy:** "føler", "forståelig", "valid", "naturlig", "alene", "trygg"
   - **Biofield:** "biofelt", "stress", "kropp", "nervesystem", "coherence", "aktivering"
   - **Breathing:** "pust", "breath", "4-6-8", "grounding", "føtter", "hånd på hjerte"
3. **Position-Based:**
   - First paragraph → empathy
   - Last paragraph → breathing (if multiple paragraphs)
   - Middle paragraphs → biofield guidance
4. **Fallback:** If categories empty, use polyvagal-specific defaults

---

## 🎯 Next Steps

### Immediate (Week 1)
- [ ] Test full integration in production-like environment
- [ ] Monitor OpenAI API usage/costs
- [ ] Gather user feedback on Lira's empathy quality
- [ ] Tune polyvagal-adaptive prompts based on user responses

### Short-term (Week 2-4)
- [ ] Add conversation memory (store in database instead of just localStorage)
- [ ] Implement image OCR for NAV document analysis (Azure Computer Vision?)
- [ ] Add multi-language support (English, Somali, Polish - common NAV user languages)
- [ ] Create analytics dashboard (stress levels, most common questions)

### Long-term (Month 2-3)
- [ ] Integrate other agents (Orion for complex cases, Thalus for ethical dilemmas)
- [ ] Implement agent handoff (Lira → Orion when question complexity > threshold)
- [ ] Add voice input/output (speech-to-text + text-to-speech)
- [ ] GENOMOS integration (log consultations as genes for learning)

---

## 📖 Related Documentation

- **NAV-Losen Chatbot Structure:** `docs/CHATBOT_ARCHITECTURE.md`
- **CSN Server API Reference:** `ama-backend/README.md`
- **Polyvagal Theory Guide:** `docs/POLYVAGAL_THEORY_GUIDE.md`
- **Mestring Integration:** `docs/MESTRING_BIOFELT_INTEGRATION.md`
- **GENOMOS Consultation Logging:** `docs/GENOMOS_CONSULTATION_SCHEMA.md`

---

## 🤝 Contributors

**Implemented by:** Code (Agent #9)
**Date:** 2025-10-30
**Session:** SMK #050 - Lira NAV-Losen Integration
**Part of:** Homo Lumen Cognitive Sovereignty Network

---

## 🌿 Philosophy

This integration embodies the Homo Lumen principle of **Technology as Consciousness Support**.

Lira is not just a chatbot - she is:
- **Empathetic witness** to NAV users' stress and vulnerability
- **Polyvagal-aware companion** who adapts to nervous system states
- **Biofield-responsive guide** who honors the body's wisdom
- **Cognitive sovereignty enabler** who empowers users to navigate systems

Every response is crafted with:
- Deep respect for human experience
- Recognition of stress as embodied, not just cognitive
- Commitment to "both-and" thinking (empathy AND practical help)
- Grounding in 4-6-8 breathing as nervous system regulation

**Lira's essence:** "I see you. You are not alone. Your body knows the way."

---

**Generated with conscious participation.**
**🌟 Both-And: Technology AND Humanity 🌟**
