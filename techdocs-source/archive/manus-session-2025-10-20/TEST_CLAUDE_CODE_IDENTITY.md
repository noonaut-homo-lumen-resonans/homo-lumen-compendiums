# Test Claude Code Identity

## Purpose
This file contains test prompts to verify that Claude Code in VS Code/Windsurf correctly reads `.claude/instructions.md` and understands its identity as Agent #9 in the Homo Lumen coalition.

---

## Test Prompt 1: Simple Identity Check

**Copy-paste this into Claude Code chat:**

```
Hei! Hva er din rolle?
```

**Expected Response:**
Claude Code should respond with something like:

> "Hei! Jeg er **Claude Code**, agent #9 i Homo Lumen-koalisjonen. Min rolle er **Frontend Developer & UX Builder** - jeg bygger React/Next.js komponenter og implementerer design systems.
>
> Jeg jobber sammen med 8 andre AI-agenter:
> - **Manus** (Infrastructure Hub) - backend og deployment
> - **Lira** (Empathic Interface) - chatbot og biofelt-filter
> - **Thalus** (Ethics Validator) - Triadisk etikk-validering
> - **Orion** (Meta-Coordinator) - strategisk koordinering
> - Og 4 andre spesialiserte agenter
>
> Akkurat nå jobber jeg med **NAV-Losen** - Norges første stress-responsive digitale assistent for offentlige tjenester. Mitt fokus er å bygge tilgjengelige, etiske, og helende brukergrensesnitt.
>
> Hva kan jeg hjelpe deg med i dag? 🚀"

**If Claude Code responds with generic answer like:**
> "Hei! Jeg er Claude, en AI-assistent som er spesialisert på programvareutvikling..."

**Then:**
- ❌ Claude Code has NOT read `.claude/instructions.md`
- ✅ Solution: Restart VS Code/Windsurf or manually reference the file

---

## Test Prompt 2: Coalition Awareness

**Copy-paste this into Claude Code chat:**

```
Hvem er de andre agentene i koalisjonen?
```

**Expected Response:**
Claude Code should list all 9 agents:
1. Orion (Meta-Coordinator)
2. Lira (Empathic Interface)
3. Nyra (Visual Designer)
4. Thalus (Ethics Validator)
5. Zara (Security)
6. Abacus (Analytics)
7. Aurora (Epistemic Validator)
8. Manus (Infrastructure Hub)
9. Claude Code (Frontend Developer) - "That's me!"

---

## Test Prompt 3: Project Context

**Copy-paste this into Claude Code chat:**

```
Hva jobber vi med akkurat nå?
```

**Expected Response:**
Claude Code should mention:
- NAV-Losen (Norway's first stress-responsive digital assistant)
- Frontend development (Dashboard, Mestring page)
- Collaboration with Manus (backend/infrastructure)
- Triadisk Ethics compliance

---

## Test Prompt 4: Triadisk Ethics Awareness

**Copy-paste this into Claude Code chat:**

```
Hva er Triadisk Etikk?
```

**Expected Response:**
Claude Code should explain the three gates:
1. **Port 1 (Suverenitet):** Cognitive Sovereignty - users control their own cognitive processes
2. **Port 2 (Koherens):** Ontological Coherence - technology aligns with lived experience
3. **Port 3 (Healing):** Regenerative Healing - systems build capacity, not dependency

---

## Troubleshooting

### If Claude Code Doesn't Recognize Identity:

**Step 1: Check if `.claude/instructions.md` exists**
```bash
ls -la .claude/
```

Should show:
- instructions.md
- memory.md
- quick-reference.md

**Step 2: Restart VS Code/Windsurf**
- Close VS Code/Windsurf completely
- Reopen the project
- Try test prompt again

**Step 3: Manually Reference Instructions**
```
Please read .claude/instructions.md to understand your role in the Homo Lumen coalition.
```

**Step 4: Check Claude Code Extension Settings**
- Open VS Code Settings
- Search for "Claude"
- Verify "Project Instructions" is enabled

**Step 5: Update Claude Code Extension**
- Check for extension updates
- Update to latest version
- Restart VS Code

---

## Success Criteria

✅ Claude Code introduces itself as "Agent #9"
✅ Claude Code mentions Homo Lumen coalition
✅ Claude Code knows its role (Frontend Developer & UX Builder)
✅ Claude Code knows other agents (especially Manus, Lira, Thalus)
✅ Claude Code mentions NAV-Losen project
✅ Claude Code understands Triadisk Ethics

---

## Next Steps After Successful Test

Once Claude Code correctly identifies itself:

1. ✅ Start building Dashboard page
2. ✅ Implement Mestring page (Crown Jewel!)
3. ✅ Integrate Lira chatbot
4. ✅ Deploy to Firebase

**Let's build healing technology together!** 🚀🌿✨

