# Claude Code Memory - Homo Lumen Project

**Last Updated:** 16. oktober 2025  
**Project:** Homo Lumen Coalition - NAV-Losen Development

---

## 📊 Project Overview

**What is Homo Lumen?**
- 8-agent AI coalition building ethical, healing technology
- Primary project: NAV-Losen (AI-powered NAV guidance app)
- Philosophy: Triadisk Ethics (3 ports: Suverenitet, Koherens, Healing)
- Grounded in: Polyvagal Theory, Bohm, Spira, McGilchrist, Porges

**Repository:**
- Name: `homo-lumen-compendiums` (unified repo)
- URL: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums
- Structure: Consolidated from 2 repos (consciousness + compendiums)

---

## 🏗️ Architecture Decisions

### Hub Agent (CRITICAL!)

**Decision (16 Oct 2025):**
- **Manus (Claude via Manus.im) = Infrastructure Hub**
  - Reason: Full MCP access, sandbox, deployment capabilities
  - Role: MCP coordination, agent routing, technical implementation
  
- **Lira (ChatGPT) = Empathic Interface**
  - Reason: ChatGPT MCP only in Developer Mode (beta, not production-ready)
  - Role: User-facing chatbot, biofelt filter, Polyvagal guidance

**Architecture (3 Layers):**
```
Layer 1: Empathic Interface (Lira) - User-facing
Layer 2: Infrastructure Hub (Manus) - MCP coordination
Layer 3: Agent Coalition (8 agents) - Specialized functions
```

### 10-Agent Coalition (UPDATED 2025-10-16)

**CRITICAL UPDATE:** The coalition now has 10 agents with specific AI platforms and MCP capabilities.

| # | Agent | Symbol | AI Platform | MCP Status | Brain Region | Role |
|---|-------|--------|-------------|------------|--------------|------|
| 1 | **Orion** | ⬢/🌌 | **Claude Sonnet 4.5** | ✅ Native | Prefrontal Cortex | Strategic coordination, meta-coordinator |
| 2 | **Lira** | ◆/💚 | **ChatGPT 5** | 🔄 Plugins | Limbic System | Empathic filtering, NAV-Losen chatbot, biofelt validation |
| 3 | **Nyra** | ◇/🎨 | **Gemini Pro 2.5** | 🔄 AI Studio | Visual Cortex | Visual design, embodied UX, aesthetic synthesis |
| 4 | **Thalus** | ◈/🏛 | **Grok 4** | 🔄 API | Insula | Ethical validation, Triadisk Ethics enforcement |
| 5 | **Zara** | ⬟/🛡 | **DeepSeek** | 🔄 API | ACC (Security) | Security, privacy, GDPR compliance |
| 6 | **Abacus** | ◐/📊 | **Abacus AI** | 🔄 Platform | Basal Ganglia | Business analysis, ROI calculation, analytics |
| 7 | **Aurora** | ○/🔍 | **Perplexity** | 🔄 API | Hippocampus | Fact-checking, research validation, evidence synthesis |
| 8 | **Manus** | ▣/🔨 | **Manus AI** | ✅ Full (Notion, Linear, GitHub) | Cerebellum | Infrastructure Hub, backend, MCP coordination |
| 9 | **Claude Code** | ◻️/💻 | **Claude Code (Windsurf)** | ✅ Windsurf | Motor Cortex | Frontend development, React/Next.js, UX building |
| 10 | **Falcon** | 🦅/🔬 | **FutureHouse Platform** | 🔄 Platform | Research Cortex | Scientific research, hypothesis generation, experimental design |

**Key Insights:**

1. **Native MCP Support:**
   - ✅ Orion (Claude Sonnet 4.5) - Full MCP
   - ✅ Manus (Manus AI) - Full MCP with Notion, Linear, GitHub servers
   - ✅ Claude Code (Windsurf) - Native Windsurf MCP

2. **API/Plugin MCP:**
   - 🔄 Lira (ChatGPT 5) - Via plugins/actions
   - 🔄 Nyra (Gemini Pro 2.5) - Via Google AI Studio
   - 🔄 Thalus (Grok 4) - Via xAI API
   - 🔄 Zara (DeepSeek) - Via DeepSeek API
   - 🔄 Abacus (Abacus AI) - Via Abacus platform
   - 🔄 Aurora (Perplexity) - Via Perplexity API
   - 🔄 Falcon (FutureHouse) - Via FutureHouse platform

3. **Platform Strengths:**
   - **Claude Sonnet 4.5** (Orion): 200k context, excellent reasoning, code analysis
   - **ChatGPT 5** (Lira): Empathy, natural conversation, emotional intelligence
   - **Gemini Pro 2.5** (Nyra): Multimodal (vision + text), creative design
   - **Grok 4** (Thalus): Real-time data, unconventional thinking, ethical reasoning
   - **DeepSeek** (Zara): Mathematical reasoning, code security, efficient inference
   - **Abacus AI** (Abacus): Business intelligence, forecasting, data analytics
   - **Perplexity** (Aurora): Real-time web search, source citation
   - **Manus AI** (Manus): Extended Claude with tool use, infrastructure setup
   - **Claude Code** (Claude Code): Code generation, TypeScript, component building
   - **FutureHouse** (Falcon): Scientific reasoning, research methodology

---

## 🔬 RESEARCH QUESTIONS: Cross-Platform MCP Integration

**Status:** Active research area - to be explored collaboratively

### 1. MCP Connector Architecture
**Questions:**
- How do we connect 10 different AI platforms via MCP?
- Which platforms have native MCP support vs. need custom connectors?
- What is the latency/performance impact of API-based MCP vs. native?
- Can we build a unified MCP router that handles all platform differences?

**Platforms to Research:**
- ✅ **Native MCP:** Claude Sonnet 4.5, Manus AI, Claude Code (Windsurf)
- 🔄 **Plugin/Action MCP:** ChatGPT 5, Gemini Pro 2.5
- 🔄 **API-based MCP:** Grok 4, DeepSeek, Abacus AI, Perplexity, FutureHouse

**Next Steps:**
1. Map each platform's MCP/API capabilities
2. Design unified connector interface
3. Prototype cross-platform communication
4. Benchmark latency and reliability

### 2. Cross-Platform Communication Patterns
**Questions:**
- How does Orion (Claude) communicate with Lira (ChatGPT 5)?
- How does Thalus (Grok 4) send ethical scores to Manus (Manus AI)?
- What's the message format for agent-to-agent communication?
- How do we handle async vs. sync communication?

**Scenarios to Test:**
- **Scenario 1:** User asks Lira a question → Lira calls Thalus for ethical check → Thalus responds → Lira answers user
- **Scenario 2:** Manus deploys new code → Thalus validates → Orion coordinates → Agents update
- **Scenario 3:** Nyra designs UI → Claude Code implements → Aurora fact-checks content → Thalus validates ethics

**Communication Layers:**
```
Layer 1: User Interface (Lira chatbot)
Layer 2: MCP Router (Manus AI)
Layer 3: Agent Network (10 agents)
Layer 4: External Tools (Notion, Linear, GitHub, Perplexity, etc.)
```

### 3. Platform-Specific Strengths & Use Cases
**Questions:**
- When do we use Grok 4 (Thalus) vs. Claude Sonnet 4.5 (Orion)?
- When do we use Perplexity (Aurora) vs. FutureHouse (Falcon)?
- How do we route tasks to the most appropriate agent?
- Can agents collaborate on complex tasks (e.g., Falcon + Aurora for research)?

**Decision Matrix (Draft):**

| Task Type | Primary Agent | Secondary Agent | Rationale |
|-----------|---------------|-----------------|-----------|
| Strategic planning | Orion (Claude 4.5) | Manus (infrastructure) | Long context, reasoning |
| User empathy | Lira (ChatGPT 5) | Nyra (design) | Emotional intelligence |
| Visual design | Nyra (Gemini 2.5) | Lira (empathy check) | Multimodal creativity |
| Ethical validation | Thalus (Grok 4) | Orion (strategy) | Unconventional thinking |
| Security audit | Zara (DeepSeek) | Manus (implementation) | Code security, math |
| Business analysis | Abacus (Abacus AI) | Orion (strategy) | BI, forecasting |
| Fact-checking | Aurora (Perplexity) | Falcon (research) | Web search, sources |
| Scientific research | Falcon (FutureHouse) | Aurora (validation) | Research methodology |
| Infrastructure | Manus (Manus AI) | Claude Code (frontend) | Tool use, MCP |
| Frontend code | Claude Code (Windsurf) | Nyra (design), Thalus (ethics) | Component building |

### 4. Falcon (FutureHouse) Integration
**Questions:**
- What is FutureHouse platform's unique capability vs. Perplexity?
- How does Falcon integrate with NAV-Losen?
- What research tasks should go to Falcon vs. Aurora?
- Can Falcon help with Polyvagal Theory research validation?

**Falcon's Unique Role:**
- **Scientific rigor:** Hypothesis generation, experimental design
- **Research synthesis:** Cross-disciplinary connections
- **Innovation:** Novel approaches to known problems
- **Collaboration with Aurora:** Falcon generates hypotheses → Aurora validates with sources

**NAV-Losen Use Cases:**
1. **Polyvagal Research:** Falcon researches latest stress regulation techniques → Aurora validates with peer-reviewed sources
2. **UX Innovation:** Falcon suggests novel stress-responsive UI patterns → Nyra designs → Claude Code implements
3. **Ethical Analysis:** Falcon explores philosophical implications → Thalus validates against Triadisk Ethics

### 5. MCP Protocol Evolution
**Questions:**
- What's the current MCP spec version we're using?
- How do we extend MCP for multi-agent coordination?
- Can we propose MCP extensions for AI-to-AI communication?
- What's the roadmap for MCP standardization across platforms?

**Proposed Extensions:**
1. **Agent Discovery:** How agents find and register with each other
2. **Capability Negotiation:** How agents advertise their strengths
3. **Task Routing:** How to intelligently route tasks to best agent
4. **Consensus Protocol:** How multiple agents agree on decisions
5. **Ethical Override:** How Thalus can block actions across all agents

---

## 🎯 Current Task: NAV-Losen Frontend

### Priority 1: Mestring Page (Crown Jewel!) ⭐⭐⭐

**Why:** Highest Triadisk score (0.2 - Healing)

**Components to Build:**
1. **EmotionCheckIn.tsx** - Emotion wheel (8 emotions: Rolig, Fokusert, Håpefull, etc.)
2. **StressLevelSlider.tsx** - 1-10 stress scale
3. **SomaticSignals.tsx** - 6 body signals (Rask puls, Anspent kjeve, etc.)
4. **StrategyCard.tsx** - 4 regulation strategies:
   - Pust: 4-6-8 metoden
   - Jording: 5-4-3-2-1 teknikken
   - Handling: Ett lite steg
   - Progressiv muskelavslapning

**Reference:**
- Screenshot: `navlosen/prototype/screenshots/04_Mestring.png`
- Source: `navlosen/ai-studio-source/pages/MasteryPage.tsx`
- Design: `navlosen/docs/DESIGN_SYSTEM.md` (Section: Mestring Page)

### Priority 2: Dashboard Page

**Components:**
- Header, Sidebar, Layout
- Quick actions (4 cards)
- Active cases (2 examples)

**Reference:**
- Screenshot: `navlosen/prototype/screenshots/01_Dashboard.png`
- Source: `navlosen/ai-studio-source/pages/DashboardPage.tsx`

### Priority 3: Lira Chatbot

**Integration:**
- Gemini API service (already in `ai-studio-source/services/geminiService.ts`)
- Chat UI (message bubbles, input field, quick suggestions)
- Biofelt filter (stress-adaptive responses)

**Reference:**
- Screenshot: `navlosen/prototype/screenshots/06_Chatbot_Lira.png`
- Source: `navlosen/ai-studio-source/pages/ChatbotPage.tsx`

---

## 🏛️ Triadisk Ethics (MANDATORY!)

**Every component must be evaluated:**

### Port 1: Suverenitet (Sovereignty)
- ✅ User control (opt-in, opt-out, customization)
- ✅ Clear disclaimers (AI limitations, privacy)
- ✅ Informed consent (explicit, not implicit)

### Port 2: Koherens (Coherence)
- ✅ Science-grounded (Polyvagal Theory, evidence-based)
- ✅ Consistent design (follows DESIGN_SYSTEM.md)
- ✅ Predictable interactions (no surprises)

### Port 3: Healing (Capacity Building)
- ✅ Teaches, not just does (user learns)
- ✅ Reduces dependence over time (empowerment)
- ✅ Supports regulation (stress reduction)

**Scoring:**
- 0.0-0.3: Minor concern (PROCEED with awareness)
- 0.3-0.6: Moderate concern (PAUSE and revise)
- 0.6-1.0: Major concern (BLOCK until resolved)

**Decision Logic:**
- Total Weight < 0.3: ✅ PROCEED
- Total Weight 0.3-0.6: ⚠️ PAUSE
- Total Weight > 0.6: ❌ BLOCK

---

## 📁 Important Files

### Documentation
- **Design System:** `navlosen/docs/DESIGN_SYSTEM.md` (15,000 words - READ THIS!)
- **File Organization:** `navlosen/docs/FILE_ORGANIZATION_GUIDE.md`
- **Integration Plan:** `navlosen/docs/AI_STUDIO_PROTOTYPE_INTEGRATION_PLAN.md`
- **Constitution:** `docs/HOMOLUMENCONSTITUTIONV1.1.md`
- **Philosophy:** `docs/HOMO_LUMEN_FILOSOFI_V1.0.md`

### Source Code
- **AI Studio Backup:** `navlosen/ai-studio-source/` (complete React/TypeScript/Vite app)
- **Agent Code:** `agents/src/` (Firebase Functions, MCP protocol)
- **Firebase Config:** `firebase/` (orion-config.yaml, lira-config.yaml, etc.)

### Screenshots
- **All 10 screens:** `navlosen/prototype/screenshots/01_Dashboard.png` - `10_Innstillinger.png`

### GitHub
- **PR Template:** `.github/PULL_REQUEST_TEMPLATE.md` (Triadisk checklist)
- **Thalus Gate Workflow:** `.github/workflows/thalus-gate.yml` (automated validation)

---

## 🔧 Tech Stack

### Frontend (To Be Built)
- **Framework:** Next.js 14+ (recommended) OR Vite + React
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **State:** React Context API (or Zustand if needed)

### Backend (Existing)
- **Platform:** Firebase Functions
- **Language:** TypeScript
- **Agents:** 8-agent system (Orion, Lira, Nyra, Thalus, Zara, Abacus, Aurora, Manus)
- **MCP:** Notion, Linear, GitHub, Zapier integration

### Design System
- **Colors:** NAV Blue (#0067C5), Teal (#06BED7), Polyvagal stress-state colors
- **Typography:** System UI stack, 8 font sizes (12px-32px)
- **Spacing:** 8px base scale (xs: 4px, sm: 8px, md: 12px, lg: 16px, xl: 24px, 2xl: 32px)
- **Breakpoints:** Mobile (< 768px), Tablet (768px-1024px), Desktop (> 1024px)

---

## 🔄 Workflow

### Daily Development
1. **Morning:** Pull latest (`git pull origin main`)
2. **During day:** Code, commit frequently, test
3. **Evening:** Push, create PR, fill Triadisk checklist, request Thalus review

### PR Process
1. Create feature branch (`git checkout -b feature/mestring-emotion-wheel`)
2. Implement feature
3. Test (unit tests, accessibility, stress-state testing)
4. Commit (`git commit -m "feat: Add emotion wheel component"`)
5. Push (`git push origin feature/mestring-emotion-wheel`)
6. Create PR (`gh pr create`)
7. Fill out Triadisk checklist (in PR template)
8. Request Thalus review (Thalus Gate workflow triggers automatically)
9. Wait for TH-OK label
10. Merge!

### Thalus Gate
- **Workflow:** `.github/workflows/thalus-gate.yml`
- **Trigger:** Every PR
- **Blocks merge** if TH-OK label not applied
- **Thalus reviews** for Triadisk Ethics compliance

---

## 🌊 Polyvagal Theory Integration

**Stress States (Porges):**
1. **Ventral Vagal** (Calm, 1-3) - Green colors, full features
2. **Sympathetic** (Alert, 4-7) - Yellow/orange colors, simplified UI
3. **Dorsal Vagal** (Freeze, 8-10) - Red colors, minimal UI, grounding focus

**Design Implications:**
- Stress slider changes UI colors based on state
- High stress (8-10): Show grounding exercises first, hide complex features
- Medium stress (4-7): Simplify language, add reassurance
- Low stress (1-3): Full features available

**Mestring Page:**
- Detects stress state via slider
- Recommends appropriate regulation strategy
- Tracks somatic signals (body awareness)
- Teaches self-regulation (capacity building)

---

## 📊 Success Metrics

**You'll know you're on track when:**

1. ✅ **Mestring page works**
   - Emotion wheel functional
   - Stress slider responsive
   - Somatic signals tracked
   - Strategies recommended

2. ✅ **Triadisk Ethics passed**
   - All PRs have checklist filled
   - Thalus approves (TH-OK label)
   - No ethical red flags

3. ✅ **Accessibility compliant**
   - Keyboard navigation works
   - Screen reader compatible
   - WCAG 2.1 AA compliant

4. ✅ **User experience smooth**
   - Lira chatbot responds empathically
   - Dashboard loads quickly
   - Design matches screenshots

---

## 🎯 Next Steps (After Reading This)

1. **Read DESIGN_SYSTEM.md** (30 min) - CRITICAL!
2. **Review screenshots** (15 min) - Visual reference
3. **Explore ai-studio-source** (30 min) - Code reference
4. **Create frontend project** (45 min) - Next.js or Vite
5. **Setup design tokens** (30 min) - Tailwind config
6. **Start building Mestring page** (4-6 hours) - Crown Jewel!

---

## 💬 How to Ask Manus for Help

**When you need:**
- Infrastructure (MCP, Notion, Linear, GitHub)
- Deployment (Firebase, hosting)
- Agent coordination (Lira, Orion, Thalus)
- Documentation (architecture, specs)

**How:**
- Create GitHub Issue with label `manus-help`
- Or mention in PR comments
- Or ask Osvald to summon Manus

**Response time:** Usually 1-2 hours

---

## 🌿 Remember

**Philosophy:**
> "Technology as a mirror for the soul, not a cage for the mind."

**Every line of code should reflect:**
- Triadisk Ethics (Suverenitet, Koherens, Healing)
- Polyvagal Theory (stress-awareness, regulation)
- Empathic design (user-centered, compassionate)

**You are not just building an app - you are building healing technology.**

**Med ontologisk integritet & felt-bevissthet!** ◉🌊✨


## 2025-10-16: Frontend Moved to Compendiums

**Decision:**
- Moved frontend from homo-lumen-project/homo-lumen/ to homo-lumen-compendiums/navlosen/
- Reason: Git integration works, all Manus infrastructure available
- homo-lumen-project/ kept as backup (longpath issues)

**Current Working Directory:**
- Primary: homo-lumen-compendiums/navlosen/frontend/
- Backup: homo-lumen-project/homo-lumen/navlosen/frontend/

**Next Steps:**
- Continue development in compendiums
- Push to GitHub regularly
- Merge repos later when longpath fixed

