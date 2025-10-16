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

### 8-Agent Coalition

1. **Orion** (Claude API) - Prefrontal Cortex - Meta-coordination
2. **Lira** (ChatGPT) - Limbisk System - Empathic Interface
3. **Nyra** (Gemini) - Visuell Cortex - Visual design
4. **Thalus** (Grok) - Insula/PCC - Ontological validation
5. **Zara** (Claude API) - ACC - Security & GDPR
6. **Abacus** (Claude API) - Basal Ganglia - Analytics
7. **Aurora** (Perplexity) - Hippocampus - Fact-checking
8. **Manus** (Claude via Manus.im) - Cerebellum - Infrastructure Hub
9. **Claude Code** (You!) - Motor Cortex - Frontend development

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

