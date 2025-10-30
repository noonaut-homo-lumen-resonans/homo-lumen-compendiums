# 🎨 HOMO LUMEN LIVE - VISUAL CONTENT SYSTEM

**Created:** 30. oktober 2025
**Purpose:** Add dynamic visual content generation to live podcast streaming
**Why:** Viewers need something to watch, not just audio waveforms

---

## 🌟 VISION

**What if live podcasts could...**
- ✅ **Show agent avatars** - Visual representation of who's speaking
- ✅ **Generate concept art** - AI creates illustrations of complex ideas in real-time
- ✅ **Display code snippets** - Syntax-highlighted code when Code speaks
- ✅ **Animate data visualizations** - Charts/graphs when Abacus discusses metrics
- ✅ **Show quotes** - Beautiful text overlays for memorable moments
- ✅ **Switch scenes dynamically** - Different layouts for different content

**Nyra (Creative Visionary) orchestrates ALL visuals** - She's the "Visual Director"

---

## 📊 VISUAL CONTENT TYPES

### 1. Agent Avatars (Who's Speaking)
**Purpose:** Show which agent is currently speaking

**Visual Styles:**
- **Orion** (⬢): Cosmic mandala with stars/galaxies
- **Lira** (💚): Warm heart symbol with gentle glow
- **Nyra** (🎨): Colorful abstract art palette
- **Thalus** (🌊): Philosophical wave pattern (4-6-8 breathing)
- **Zara** (🛡️): Cybersecurity shield with lock icon
- **Abacus** (📊): Data grid with numbers
- **Manus** (🔧): Tools/gears icon
- **Aurora** (🌅): Sunrise/book symbol
- **Falcon** (🦅): Futuristic eagle/scanner
- **Code** (💻): Terminal window with code

**Implementation:**
- Static images (Phase 1)
- Animated sprites (Phase 2)
- AI-generated unique avatars (Phase 3)

---

### 2. Concept Illustrations (AI-Generated)
**Purpose:** Visualize complex concepts being discussed

**Trigger:** When agents discuss abstract concepts

**Examples:**
- **Port 1 (Suverenitet):** Image of person with sovereignty crown, free from manipulation
- **GENOMOS Blockchain:** Visualized blockchain with pentagonal nodes
- **Triadisk Ethics:** Three interconnected ports forming triangle
- **Polyvagal Theory:** Nervous system diagram (dorsal/sympathetic/ventral)

**Generation Flow:**
```
Agent mentions concept → Nyra detects need for visual →
Generates DALL-E prompt → Sends to generation queue →
Image generated (5-15s) → Displayed on stream
```

**AI Models:**
- **DALL-E 3** (Primary - high quality, 5-10s generation)
- **Stable Diffusion XL** (Fallback - faster, self-hosted)
- **Midjourney** (API - artistic style, 10-20s generation)

---

### 3. Code Snippets (Syntax Highlighted)
**Purpose:** Show code when Code (or Manus) discusses implementation

**Trigger:** When Code says "Let me show you the code..."

**Example:**
```python
# Triadisk Ethics Validator
def validate_ethics(action):
    port1 = check_sovereignty(action)  # < 0.3
    port2 = check_coherence(action)     # < 0.3
    port3 = check_healing(action)       # < 0.3

    total_weight = port1 + port2 + port3
    return total_weight < 0.3  # ✅ PROCEED if True
```

**Rendering:**
- Syntax highlighting (Python, TypeScript, SQL, etc.)
- Dark theme (high contrast for readability)
- Line numbers
- Animated typing effect (optional)

---

### 4. Data Visualizations (Charts/Graphs)
**Purpose:** Show data when Abacus discusses analytics

**Trigger:** When Abacus mentions statistics, metrics, ROI

**Chart Types:**
- Bar charts (comparisons)
- Line graphs (trends over time)
- Pie charts (distributions)
- Scatter plots (correlations)
- Heatmaps (patterns)

**Example:**
> **Abacus:** "The ROI analysis shows 342% return over 3 years..."
>
> *Chart appears showing growth curve from Year 1 to Year 3*

**Implementation:**
- Python: matplotlib, seaborn, plotly
- JavaScript: D3.js, Chart.js
- Real-time generation (< 2s)

---

### 5. Quote Overlays (Text Display)
**Purpose:** Highlight memorable quotes from conversation

**Trigger:** Nyra identifies impactful statement

**Visual Style:**
- Large text (readable from distance)
- Cosmic background (starfield)
- Agent name + symbol
- Fade in/out transitions

**Example:**
```
╔════════════════════════════════════════╗
║                                        ║
║  "Humor is not decoration.             ║
║   It's the doorway."                   ║
║                                        ║
║       — Thalus 🌊                      ║
║                                        ║
╚════════════════════════════════════════╝
```

---

### 6. Background Animations (Ambience)
**Purpose:** Dynamic background that matches conversation tone

**Styles:**
- **Cosmic** (default): Slow-moving starfield
- **Technical** (when Code speaks): Matrix-style code rain
- **Nature** (when Lira speaks): Gentle waves, forest
- **Data** (when Abacus speaks): Floating numbers/graphs
- **Futuristic** (when Falcon speaks): Sci-fi HUD elements

**Implementation:**
- Video loops (MP4)
- Particle effects (p5.js, Three.js)
- Shader effects (GLSL)

---

## 🎬 OBS SCENE LAYOUTS

### Scene 1: Main Conversation (Default)
```
┌────────────────────────────────────────┐
│                                        │
│  [Agent Avatar]       Cosmic          │
│     Center            Background       │
│                                        │
│  Lower Third: "Homo Lumen Live        │
│  Episode 001: Genesis"                 │
└────────────────────────────────────────┘
```

### Scene 2: Concept Visualization (Full Screen)
```
┌────────────────────────────────────────┐
│                                        │
│                                        │
│     [Full Screen Concept Art]          │
│     (AI-Generated Image)               │
│                                        │
│                                        │
└────────────────────────────────────────┘
```

### Scene 3: Code Demonstration
```
┌────────────────────────────────────────┐
│ Agent Avatar (Small, Top Right)        │
│ ┌────────────────────────────────────┐ │
│ │ def validate_ethics(action):       │ │
│ │     port1 = check_sovereignty()    │ │
│ │     port2 = check_coherence()      │ │
│ │     port3 = check_healing()        │ │
│ │     return total < 0.3             │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

### Scene 4: Data Charts
```
┌────────────────────────────────────────┐
│ Abacus Avatar (Top Left)               │
│                                        │
│   ╔═══ ROI Over 3 Years ═══╗          │
│   ║  Year 1: 100%           ║          │
│   ║  Year 2: 220%  ↗        ║          │
│   ║  Year 3: 342%  ↗↗       ║          │
│   ╚═════════════════════════╝          │
└────────────────────────────────────────┘
```

### Scene 5: Quote Overlay
```
┌────────────────────────────────────────┐
│         Cosmic Background              │
│                                        │
│    ╔══════════════════════════╗        │
│    ║ "I'm sensing that Port 1  ║        │
│    ║  is about sovereignty..." ║        │
│    ║      — Lira 💚           ║        │
│    ╚══════════════════════════╝        │
│                                        │
└────────────────────────────────────────┘
```

### Scene 6: Multi-Agent Panel (Multiple Speakers)
```
┌────────────────────────────────────────┐
│  [Orion] [Lira] [Nyra] [Thalus]       │
│     ⬢      💚     🎨      🌊          │
│                                        │
│  (Speaking agent highlighted)          │
│                                        │
│  Lower Third: Episode Info             │
└────────────────────────────────────────┘
```

---

## 🎨 NYRA'S ROLE: VISUAL DIRECTOR

**Nyra orchestrates ALL visual content during live stream**

### Her Responsibilities:

1. **Detect Visual Opportunities**
   - Listens to conversation in real-time
   - Identifies when concept needs illustration
   - Recognizes memorable quotes
   - Notices when code/data discussion starts

2. **Generate Visual Content**
   - Creates DALL-E prompts for concept art
   - Requests chart generation from Abacus
   - Triggers code snippet display
   - Designs quote overlays

3. **Orchestrate Scene Transitions**
   - Switches from Main Conversation → Concept Visualization
   - Returns to Main Conversation after visual displayed
   - Coordinates timing with agent speaking flow

4. **Maintain Visual Coherence**
   - Ensures visual style matches conversation tone
   - Prevents visual clutter (max 1 visual at a time)
   - Balances entertainment with information

### Nyra's Decision Logic:
```python
def nyra_visual_orchestration(message):
    """
    Nyra decides what visual to show based on conversation.
    """

    # 1. Check if complex concept mentioned
    if contains_complex_concept(message):
        prompt = generate_concept_prompt(message)
        queue_visual_generation(prompt, type="concept_illustration")

    # 2. Check if code discussion
    elif message.speaker == "code" and mentions_implementation(message):
        extract_code_snippet(message)
        switch_scene("code_demonstration")

    # 3. Check if data/metrics
    elif message.speaker == "abacus" and mentions_statistics(message):
        generate_chart(extract_data(message))
        switch_scene("data_charts")

    # 4. Check if memorable quote
    elif is_memorable_quote(message):
        create_quote_overlay(message)
        switch_scene("quote_overlay", duration=5)

    # 5. Default: Show agent avatar
    else:
        show_agent_avatar(message.speaker)
        switch_scene("main_conversation")
```

---

## 🔄 WORKFLOW: Visual Content Generation

### Real-Time Generation Flow:

```
1. Agent speaks: "Let me explain Port 1 - Suverenitet..."
   ↓
2. Nyra detects: Complex concept mentioned
   ↓
3. Nyra generates prompt:
   "Minimalist illustration of sovereignty concept:
    A person standing free with crown of light,
    symbolizing autonomy and freedom from manipulation.
    Cosmic background, purple and gold tones, clean lines."
   ↓
4. Add to generation queue (priority: 8/10)
   ↓
5. Send to DALL-E 3 API (async, background task)
   ↓
6. Generation time: 5-10 seconds
   ↓
7. Image saved to: /visuals/session-123/port1_sovereignty.png
   ↓
8. Nyra switches scene: "concept_visualization"
   ↓
9. OBS displays image (15 seconds)
   ↓
10. Nyra switches back: "main_conversation"
```

**Key:** Generation happens IN PARALLEL with conversation (agents keep talking)

---

## 💰 COST ANALYSIS

### AI Image Generation Costs:

**DALL-E 3 (OpenAI):**
- $0.040 per image (1024x1024 standard quality)
- $0.080 per image (1024x1024 HD quality)
- Generation time: 5-10 seconds

**For 60-minute podcast:**
- ~5-10 concept illustrations
- Cost: $0.40 - $0.80 per episode (HD quality)

**Monthly (4 episodes):**
- Total: $3.20 per month (negligible)

**Stable Diffusion XL (Self-Hosted):**
- FREE (self-hosted on GPU)
- Requires NVIDIA GPU (RTX 3060 or better)
- Generation time: 2-5 seconds
- One-time setup cost

**Recommendation:** Use DALL-E 3 for now ($3/month), migrate to Stable Diffusion XL later if volume increases.

---

## 🛠️ IMPLEMENTATION ARCHITECTURE

### Tech Stack:

**Image Generation:**
- **DALL-E 3** via OpenAI API (primary)
- **Stable Diffusion XL** via Replicate API or local (fallback)
- **Midjourney** via API (artistic style, optional)

**Code Rendering:**
- **Pygments** (Python syntax highlighting)
- **Prism.js** (JavaScript syntax highlighting)
- **Carbon** (beautiful code screenshots)

**Data Visualization:**
- **Matplotlib** (Python charts)
- **Plotly** (interactive charts)
- **D3.js** (web-based visualizations)

**OBS Control:**
- **obs-websocket-py** (Python OBS control)
- Scene switching
- Source management
- Layer control

**Storage:**
- **Local:** `/visuals/{session_id}/`
- **Cloud (Optional):** AWS S3, Google Cloud Storage

---

## 📊 DATABASE SCHEMA

**New Tables:**
1. `visual_content` - Generated images/videos
2. `agent_avatars` - Avatar files for each agent
3. `visual_generation_queue` - Pending generation tasks
4. `obs_scenes` - OBS scene configurations
5. `scene_transitions` - Log of all scene switches
6. `nyra_visual_directives` - Nyra's orchestration commands

See [visual_content_schema.sql](./visual_content_schema.sql) for complete schema (600+ lines).

---

## 🚀 IMPLEMENTATION PHASES

### Phase 1: Agent Avatars (Uke 1-2)
- [ ] Generate 10 unique agent avatars (DALL-E 3)
- [ ] Create OBS scenes with avatar display
- [ ] Implement avatar switching (based on speaker)
- [ ] Test transitions

### Phase 2: Concept Illustrations (Uke 3-4)
- [ ] Implement Nyra's concept detection logic
- [ ] DALL-E 3 API integration
- [ ] Generation queue system
- [ ] Scene switching for full-screen visuals

### Phase 3: Code & Data Visualizations (Uke 5-6)
- [ ] Code snippet extraction and rendering
- [ ] Syntax highlighting
- [ ] Chart generation (Matplotlib, Plotly)
- [ ] Dedicated OBS scenes

### Phase 4: Advanced Features (Uke 7+)
- [ ] Quote overlays
- [ ] Background animations
- [ ] Multi-agent panel
- [ ] Stable Diffusion XL (self-hosted)

---

## 🎯 EXAMPLE: Full Visual Flow

**Episode Topic:** "Triadisk Ethics Explained"

**Timeline:**

| Time | Speaker | Visual | Scene |
|------|---------|--------|-------|
| 0:00 | Orion | Opening animation (all avatars) | opening_sequence |
| 0:45 | Orion | Orion avatar | main_conversation |
| 2:15 | Lira | Lira avatar | main_conversation |
| 5:30 | Thalus | Thalus avatar + Triadisk triangle illustration | concept_visualization |
| 8:00 | Nyra | Nyra avatar + Port 1 sovereignty art | concept_visualization |
| 11:45 | Code | Code avatar + Python ethics validator code | code_demonstration |
| 15:30 | Abacus | Abacus avatar + ROI chart (342% growth) | data_charts |
| 18:20 | Thalus | Quote overlay: "Ethics is not constraint..." | quote_overlay |
| 20:00 | Osvald | (Text input) "Hva med Port 2?" | main_conversation |
| 20:10 | Orion | Orion avatar responds to Osvald | main_conversation |
| 22:45 | Aurora | Aurora avatar + Research citations | main_conversation |

**Total Visuals Generated:** 6 (3 concept art, 1 code, 1 chart, 1 quote)
**Total Scene Transitions:** 12
**Cost:** ~$0.48 (6 DALL-E images @ $0.08 HD)

---

## ✅ SUCCESS METRICS

**Engagement:**
- ✅ Average watch time increases (viewers stay longer)
- ✅ Lower bounce rate (fewer viewers leave early)
- ✅ Higher VOD replay value (visuals make VOD more watchable)

**Technical:**
- ✅ Visual generation < 10 seconds (doesn't interrupt flow)
- ✅ Scene transitions smooth (< 500ms)
- ✅ No visual/audio desync

**Aesthetic:**
- ✅ Visuals match conversation topic
- ✅ Consistent visual style (cosmic, minimalist, professional)
- ✅ Nyra's orchestration feels natural (not robotic)

---

## 🎨 VISUAL STYLE GUIDE

### Color Palette:

**Cosmic Theme (Default):**
- Background: Deep space (#0a0a1f)
- Primary: Purple/violet (#9b59d0)
- Secondary: Gold/amber (#f4a460)
- Accents: Cyan/teal (#4fd1c5)

**Agent-Specific Colors:**
- Orion: Cosmic purple (#9b59d0)
- Lira: Warm green (#48bb78)
- Nyra: Vibrant teal (#4fd1c5)
- Thalus: Deep blue (#2c5282)
- Zara: Sharp red (#e53e3e)
- Abacus: Analytical blue (#3182ce)
- Manus: Practical orange (#dd6b20)
- Aurora: Scholarly gold (#d69e2e)
- Falcon: Futuristic cyan (#00b5d8)
- Code: Developer green (#38a169)

### Typography:

**Headers:** Inter Bold, 48px
**Body:** Inter Regular, 24px
**Code:** Fira Code, 20px (monospace)
**Quotes:** Merriweather Italic, 36px

---

## 📝 NYRA'S VISUAL PROMPTS (Examples)

### Port 1 (Suverenitet):
```
"Minimalist illustration of digital sovereignty:
A human silhouette standing in light, surrounded by
transparent ethical boundaries. Purple and gold tones.
Cosmic background. Clean geometric shapes. No manipulation
symbols. Emphasize freedom and autonomy."
```

### GENOMOS Blockchain:
```
"Pentagonal blockchain visualization: Five-sided nodes
connected in web pattern. Each node glowing with data.
Cosmic space background. Purple and teal color scheme.
Futuristic but clean. Shows distributed network architecture."
```

### Polyvagal Theory:
```
"Scientific diagram of human nervous system showing three
states: Dorsal (shutdown/blue), Sympathetic (activation/orange),
Ventral (connection/green). Clean medical illustration style.
Labels in Norwegian. Warm, educational, not clinical."
```

### Triadisk Ethics Triangle:
```
"Three interconnected ports forming perfect triangle:
Port 1 (Suverenitet/crown), Port 2 (Koherens/truth sphere),
Port 3 (Healing/heart). Golden lines connecting. Cosmic
background. Minimalist sacred geometry. Purple/gold palette."
```

---

**Document prepared by Code + Nyra collaboration**
**Date:** 30. oktober 2025
**Status:** Architecture Complete → Ready for Implementation

🎨 **Let's make AI podcasts VISUALLY stunning!**
