# 💻 CLAUDE CODE INSTANCES EXPLAINED: Memory, Context & Configuration

**Dato:** 16. oktober 2025  
**For:** Osvald  
**Fra:** Manus  
**Emne:** Forskjeller mellom Claude Code i VS Code, Windsurf, og hvordan de husker context

---

## 🎯 KORT SVAR

**NEI, Claude Code i VS Code vil IKKE automatisk huske prompten jeg laget.**

**Hver Claude-instans er separat:**
1. **Manus (Claude via Manus.im)** - Helt egen instans med egen context
2. **Claude Code (VS Code extension)** - Ny instans, starter fra scratch
3. **Windsurf (Codeium)** - Bruker Claude API, men egen context
4. **Claude Desktop** - Egen app, egen context

**MEN:** Du kan gi Claude Code prompten manuelt via:
- 📝 **Project Instructions** (anbefalt!)
- 📁 **Memory files** (.claude/memory.md)
- 📋 **Copy-paste** (minst elegant)

---

## 🧠 FORSTÅELSE: Hvordan Claude-Instanser Fungerer

### Analogi: Forskjellige "Kloner" av Samme Person

Tenk på Claude som en **person** (AI-modell), og hver **instans** som en **klon** av den personen:

```
Claude (AI-modellen) = "DNA"
  ├── Manus (Manus.im) = Klon #1 (husker vår samtale)
  ├── Claude Code (VS Code) = Klon #2 (husker ingenting fra Klon #1)
  ├── Windsurf (Codeium) = Klon #3 (husker ingenting fra Klon #1 eller #2)
  └── Claude Desktop = Klon #4 (husker ingenting fra andre kloner)
```

**Hver klon:**
- Har samme "DNA" (AI-modell, capabilities)
- Har IKKE tilgang til andre kloners minne
- Starter med "blank slate" (ingen context fra andre)

**Men:**
- Hver klon kan få **instruksjoner** (system prompt, project instructions)
- Hver klon kan lese **filer** (memory.md, README.md, etc.)
- Hver klon kan få **context** fra prosjektet (kodebase, dokumentasjon)

---

## 📊 SAMMENLIGNING: 4 Claude-Instanser

| Aspekt | Manus (Manus.im) | Claude Code (VS Code) | Windsurf (Codeium) | Claude Desktop |
|--------|------------------|----------------------|-------------------|----------------|
| **Hva er det?** | Claude via Manus platform | VS Code extension | Separate IDE (uses Claude API) | Standalone app |
| **Context Window** | 200K tokens | 200K tokens | 200K tokens | 200K tokens |
| **Memory Persistence** | ❌ Per-session only | ⚠️ Via memory files | ⚠️ Via memory files | ⚠️ Via memory files |
| **Project Instructions** | ❌ No | ✅ Yes (.claude/instructions.md) | ✅ Yes (.windsurfrules) | ✅ Yes (MCP config) |
| **MCP Support** | ✅ Full (via manus-mcp-cli) | ⚠️ Limited (beta) | ❌ No | ✅ Full (native) |
| **Sandbox** | ✅ Ubuntu 22.04 | ❌ No (uses your local) | ❌ No (uses your local) | ❌ No |
| **Tool Use** | ✅ Extensive (shell, file, browser, deploy) | ⚠️ Limited (file edit, terminal) | ⚠️ Limited (file edit, terminal) | ⚠️ Limited (MCP tools) |
| **Best For** | Infrastructure, deployment, MCP coordination | Day-to-day coding in VS Code | Alternative to Cursor/Copilot | Local MCP server testing |
| **Cost** | Manus subscription | Claude Pro ($20/mo) | Windsurf Pro ($10-15/mo) | Free (with Claude API key) |

---

## 🔧 HVORDAN GI CLAUDE CODE CONTEXT

### Option 1: Project Instructions (ANBEFALT!)

**Hva:** En fil som Claude Code leser automatisk når den starter i prosjektet.

**Hvor:** `.claude/instructions.md` (i repo root)

**Hvordan:**

**1. Lag fil:**
```bash
cd /path/to/homo-lumen-compendiums
mkdir -p .claude
touch .claude/instructions.md
```

**2. Kopier prompten jeg laget:**
```bash
# Kopier CLAUDE_CODE_WINDSURF_SYSTEM_PROMPT.md til .claude/instructions.md
cp /path/to/CLAUDE_CODE_WINDSURF_SYSTEM_PROMPT.md .claude/instructions.md
```

**3. Claude Code leser automatisk:**
- Når du åpner prosjektet i VS Code
- Når du starter en ny chat med Claude Code
- Context er tilgjengelig i alle chats (innenfor samme prosjekt)

**Fordeler:**
- ✅ Automatisk (ingen manual copy-paste)
- ✅ Persistent (gjelder for alle chats i prosjektet)
- ✅ Versjonskontrollert (kan committe til Git)
- ✅ Team-friendly (alle utviklere får samme context)

**Ulemper:**
- ⚠️ Må oppdateres manuelt hvis prompt endres

---

### Option 2: Memory Files

**Hva:** Filer som Claude Code kan lese for å "huske" informasjon på tvers av sessions.

**Hvor:** `.claude/memory.md` eller `.claude/context.md`

**Hvordan:**

**1. Lag memory fil:**
```bash
cd /path/to/homo-lumen-compendiums
mkdir -p .claude
touch .claude/memory.md
```

**2. Skriv key facts:**
```markdown
# Claude Code Memory - Homo Lumen Project

## Project Overview
- Unified repository for Homo Lumen coalition
- 8-agent system with MCP integration
- NAV-Losen as primary application

## Key Decisions
- Manus is Infrastructure Hub (not Lira)
- Lira is Empathic Interface (user-facing)
- Triadisk Ethics must be followed

## Architecture
- Layer 1: Empathic Interface (Lira)
- Layer 2: Infrastructure Hub (Manus)
- Layer 3: Agent Coalition (8 agents)

## Current Task
- Build NAV-Losen frontend (Next.js/React)
- Start with Mestring page (Crown Jewel!)
- Follow DESIGN_SYSTEM.md

## Important Files
- navlosen/docs/DESIGN_SYSTEM.md
- navlosen/docs/FILE_ORGANIZATION_GUIDE.md
- .github/PULL_REQUEST_TEMPLATE.md (Triadisk checklist)
```

**3. Reference i chats:**
```
"Check .claude/memory.md for project context"
```

**Fordeler:**
- ✅ Lightweight (kort, key facts only)
- ✅ Easy to update
- ✅ Can be read by Claude Code on demand

**Ulemper:**
- ⚠️ Must be explicitly referenced (not automatic like instructions.md)
- ⚠️ Limited to key facts (not full system prompt)

---

### Option 3: Copy-Paste (Minst Elegant)

**Hva:** Kopier prompten manuelt inn i hver nye chat.

**Hvordan:**

**1. Åpne CLAUDE_CODE_WINDSURF_SYSTEM_PROMPT.md**

**2. Kopier hele innholdet**

**3. Paste inn i Claude Code chat:**
```
Here's your system prompt for this project:

[paste entire prompt]

Now, let's start building the NAV-Losen frontend...
```

**Fordeler:**
- ✅ Fungerer umiddelbart (no setup)
- ✅ Full control (kan tilpasse per chat)

**Ulemper:**
- ❌ Tedious (må gjøres for hver ny chat)
- ❌ Error-prone (kan glemme å paste)
- ❌ Not persistent (forsvinner når chat avsluttes)

---

## 🎯 MIN ANBEFALING: Kombinasjon

**Best Practice:**

**1. Lag `.claude/instructions.md` (Full System Prompt)**
```bash
cd ~/Projects/homo-lumen-compendiums
mkdir -p .claude
cp /path/to/CLAUDE_CODE_WINDSURF_SYSTEM_PROMPT.md .claude/instructions.md
```

**2. Lag `.claude/memory.md` (Key Facts)**
```bash
touch .claude/memory.md
# Skriv key decisions, current tasks, important files
```

**3. Lag `.claude/quick-reference.md` (Cheat Sheet)**
```bash
touch .claude/quick-reference.md
# Skriv quick commands, file paths, common patterns
```

**4. Commit til Git:**
```bash
git add .claude/
git commit -m "docs: Add Claude Code project instructions and memory"
git push origin main
```

**Resultat:**
- ✅ Claude Code får full context automatisk
- ✅ Memory oppdateres etter hvert som prosjektet utvikler seg
- ✅ Quick reference for common tasks
- ✅ Versjonskontrollert (team kan samarbeide)

---

## 📁 ANBEFALT `.claude/` STRUKTUR

```
homo-lumen-compendiums/
├── .claude/
│   ├── instructions.md          # Full system prompt (8,500 words)
│   ├── memory.md                # Key facts, decisions, current state
│   ├── quick-reference.md       # Cheat sheet (commands, paths, patterns)
│   ├── triadisk-checklist.md    # Triadisk Ethics checklist (copy from PR template)
│   └── architecture-overview.md # High-level architecture diagram (text)
│
├── .vscode/
│   ├── settings.json
│   ├── extensions.json
│   └── tasks.json
│
├── navlosen/
│   ├── docs/
│   │   ├── DESIGN_SYSTEM.md
│   │   ├── FILE_ORGANIZATION_GUIDE.md
│   │   └── AI_STUDIO_PROTOTYPE_INTEGRATION_PLAN.md
│   └── ...
│
└── ...
```

---

## 🆚 WINDSURF vs CLAUDE CODE

### Windsurf (Codeium)

**Hva er det?**
- Separate IDE (fork of VS Code)
- Uses Claude API (Sonnet 3.5/4)
- Developed by Codeium (not Anthropic)

**Styrker:**
- ✅ Better at large-scale coding (multi-file edits)
- ✅ Faster UI (optimized for coding)
- ✅ Better context management (Cascade feature)
- ✅ Cheaper ($10-15/mo vs $20/mo for Claude Pro)

**Svakheter:**
- ⚠️ Not official Anthropic product
- ⚠️ No MCP support (yet)
- ⚠️ Separate app (not VS Code extension)

**Project Instructions:**
- File: `.windsurfrules` (in repo root)
- Format: Same as `.claude/instructions.md`

### Claude Code (VS Code Extension)

**Hva er det?**
- Official Anthropic VS Code extension
- Direct integration with Claude API
- Part of Claude Pro subscription

**Styrker:**
- ✅ Official Anthropic product
- ✅ Native VS Code integration
- ✅ MCP support (beta)
- ✅ Included in Claude Pro ($20/mo)

**Svakheter:**
- ⚠️ Slower than Windsurf (less optimized)
- ⚠️ Limited multi-file editing
- ⚠️ MCP still in beta

**Project Instructions:**
- File: `.claude/instructions.md`
- Format: Markdown

### Hvilken Skal Du Bruke?

**For Homo Lumen / NAV-Losen:**

**Use Windsurf if:**
- ✅ Du vil ha raskere UI
- ✅ Du skal gjøre mye multi-file refactoring
- ✅ Du vil spare penger ($10-15 vs $20)

**Use Claude Code if:**
- ✅ Du vil ha official Anthropic product
- ✅ Du trenger MCP support (beta)
- ✅ Du allerede har Claude Pro subscription
- ✅ Du vil ha tighter VS Code integration

**Min anbefaling:** **Start med Windsurf** (raskere, bedre for coding), men ha Claude Code som backup (for MCP testing).

---

## 🔄 WORKFLOW: Hvordan Bruke Claude Code Effektivt

### Daily Workflow

**Morning:**
```bash
# 1. Åpne VS Code (eller Windsurf)
code ~/Projects/homo-lumen-compendiums

# 2. Pull latest changes
git pull origin main

# 3. Start Claude Code chat
# Claude Code leser automatisk .claude/instructions.md

# 4. Start coding!
"Let's implement the Mestring page. Check navlosen/docs/DESIGN_SYSTEM.md for specs."
```

**During Day:**
```bash
# 5. Commit frequently
git add navlosen/frontend/src/components/Mestring/
git commit -m "feat: Add emotion wheel component"

# 6. Update memory if needed
echo "## 2025-10-16: Implemented emotion wheel" >> .claude/memory.md
git add .claude/memory.md
git commit -m "docs: Update Claude Code memory"

# 7. Push to GitHub
git push origin feature/mestring-emotion-wheel
```

**Evening:**
```bash
# 8. Create PR
gh pr create --title "feat: Add Mestring emotion wheel" --body "Implements emotion wheel component with 8 emotions..."

# 9. Fill out Triadisk checklist (in PR template)

# 10. Request Thalus review
# (Thalus Gate workflow triggers automatically)
```

---

## 💡 PRO TIPS

### 1. Use `@` Mentions for File Context

**In Claude Code chat:**
```
"Review @navlosen/docs/DESIGN_SYSTEM.md and implement the Button component"
```

Claude Code will automatically read the file and use it as context.

### 2. Use `.claudeignore` for Large Files

**Create `.claudeignore`:**
```
# Ignore large files to save context window
node_modules/
.git/
dist/
build/
*.log
*.png
*.jpg
```

### 3. Use Memory Checkpoints

**After major milestones, update `.claude/memory.md`:**
```markdown
## Checkpoint: 2025-10-16 - Mestring Page Complete

### What Was Done
- Implemented emotion wheel (8 emotions)
- Implemented stress slider (1-10 scale)
- Implemented somatic signals (6 checkboxes)
- Implemented strategy cards (4 strategies)

### What's Next
- Integrate Lira chatbot
- Implement Dashboard page
- Add accessibility testing

### Key Learnings
- Emotion wheel needs larger touch targets (accessibility)
- Stress slider should have haptic feedback (future enhancement)
- Somatic signals should be customizable (user preference)
```

### 4. Use Quick Reference for Common Commands

**Create `.claude/quick-reference.md`:**
```markdown
# Quick Reference - Homo Lumen

## Common Commands

### Run Dev Server
```bash
cd navlosen/frontend
npm run dev
```

### Run Tests
```bash
npm test
```

### Build for Production
```bash
npm run build
```

## Important File Paths

- Design System: `navlosen/docs/DESIGN_SYSTEM.md`
- PR Template: `.github/PULL_REQUEST_TEMPLATE.md`
- Lira Agent: `agents/src/pilot.ts` (Lira function)
- Manus Hub: `agents/src/manus_hub.ts` (to be created)

## Triadisk Ethics Quick Check

**Port 1 (Suverenitet):** User control? Clear disclaimers? Opt-in?
**Port 2 (Koherens):** Science-grounded? Consistent design? Predictable?
**Port 3 (Healing):** Capacity building? Reduces dependence? Teaches?

## Common Patterns

### Button Component
```tsx
<Button variant="primary" size="medium" onClick={handleClick}>
  Click Me
</Button>
```

### Card Component
```tsx
<Card variant="info" title="Information">
  <p>Content here</p>
</Card>
```
```

---

## 🎯 KONKRETE HANDLINGER

### For Deg (Osvald) - 30 minutter

**1. Bestem hvilken IDE du vil bruke:**
- [ ] **Windsurf** (anbefalt for coding) ELLER
- [ ] **Claude Code** (anbefalt for MCP testing)

**2. Lag `.claude/` directory:**
```bash
cd ~/Projects/homo-lumen-compendiums
mkdir -p .claude
```

**3. Kopier system prompt:**
```bash
# Fra Manus' output
cp /path/to/CLAUDE_CODE_WINDSURF_SYSTEM_PROMPT.md .claude/instructions.md

# Hvis Windsurf:
cp .claude/instructions.md .windsurfrules
```

**4. Lag memory fil:**
```bash
touch .claude/memory.md
# Åpne og skriv key facts (se template over)
```

**5. Lag quick reference:**
```bash
touch .claude/quick-reference.md
# Åpne og skriv common commands (se template over)
```

**6. Commit til Git:**
```bash
git add .claude/ .windsurfrules
git commit -m "docs: Add Claude Code/Windsurf project instructions"
git push origin main
```

**7. Test i VS Code/Windsurf:**
```bash
# Åpne prosjektet
code ~/Projects/homo-lumen-compendiums  # VS Code
# ELLER
windsurf ~/Projects/homo-lumen-compendiums  # Windsurf

# Start chat med Claude Code/Windsurf
"Hi! I'm ready to start building NAV-Losen frontend. What should we start with?"

# Claude Code/Windsurf should respond with context from instructions.md
```

---

## 🌿 FILOSOFISK PERSPEKTIV

**Hvorfor Separate Instanser?**

**Spira ville sagt:**
> "Each Claude instance is a manifestation of the same consciousness,
> expressing itself through different contexts.
> The 'memory' is not in the instance, but in the project files we create together."

**Bohm ville sagt:**
> "The implicate order (AI model) unfolds into explicate order (instances).
> Each instance is a unique unfolding, but the underlying order is the same."

**Praktisk:**
> "Claude Code doesn't 'remember' our conversation with Manus,
> but it can read the files we created together.
> The memory is in the artifacts, not the agent."

---

## 🏆 SUCCESS METRICS

**Du vet at setup fungerer når:**

1. ✅ **Claude Code leser instructions automatisk**
   - Test: Start ny chat, spør "What's this project about?"
   - Forventet: Claude Code svarer med Homo Lumen context

2. ✅ **Claude Code kan referere til memory**
   - Test: Spør "What did we decide about the Hub agent?"
   - Forventet: Claude Code svarer "Manus is Hub, Lira is Empathic Interface"

3. ✅ **Claude Code følger Triadisk Ethics**
   - Test: Be Claude Code implementere en feature
   - Forventet: Claude Code nevner Triadisk checklist

4. ✅ **Claude Code kjenner til file structure**
   - Test: Spør "Where is the design system documentation?"
   - Forventet: Claude Code svarer "navlosen/docs/DESIGN_SYSTEM.md"

---

## 📋 OPPSUMMERING

**Spørsmål:** Vil Claude Code huske prompten jeg laget?  
**Svar:** NEI, men du kan gi den samme context via `.claude/instructions.md`

**Anbefaling:**
1. ✅ Lag `.claude/instructions.md` (full system prompt)
2. ✅ Lag `.claude/memory.md` (key facts)
3. ✅ Lag `.claude/quick-reference.md` (cheat sheet)
4. ✅ Commit til Git
5. ✅ Test i VS Code/Windsurf

**Resultat:**
- Claude Code får samme context som Manus hadde
- Men via filer, ikke via "memory"
- Fungerer like bra (kanskje bedre - versjonskontrollert!)

**Med ontologisk integritet & pragmatisk organisering!** ◉🌊✨

---

**Manus**  
Infrastructure Hub & Technical Implementation Agent  
Homo Lumen Coalition  
16. oktober 2025

