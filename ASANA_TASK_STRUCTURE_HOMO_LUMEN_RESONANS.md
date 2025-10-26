# ASANA TASK STRUCTURE - HOMO LUMEN RESONANS

**Project:** HOMO LUMEN RESONANS  
**Created:** 26. oktober 2025  
**Purpose:** Complete task structure for Asana project setup  
**Agent:** 🔨 Manus

---

## 🚨 SECTION 1: URGENT (Deadline: 28. oktober 2025)

### **Task 1.1: Fix Mobile Simulator Days 4-7 Status**
- **Assignee:** Code
- **Due Date:** 28. oktober 2025
- **Priority:** Urgent
- **Description:**
  ```
  Mobile Simulator deadline is 28. oktober (2 days!). Days 1-3 are complete, 
  but Days 4-7 status is unknown. Need to:
  
  1. Check CODE_STATUS_MOBILE_SIMULATOR_DAG1_2_COMPLETE.md
  2. Verify if Guided Tours are implemented
  3. Complete remaining days (4-7)
  4. Test full functionality
  5. Deploy to production
  
  Reference: HOM-81 (Linear)
  Location: /home/ubuntu/homo-lumen-compendiums/navlosen-mvp/web-console/
  ```
- **Tags:** mobile-simulator, nav-losen, urgent, code

---

### **Task 1.2: Konstitusjons-Mandala Status Check**
- **Assignee:** Nyra
- **Due Date:** 26. oktober 2025 (TODAY!)
- **Priority:** Urgent
- **Description:**
  ```
  Konstitusjons-Mandala deadline is TODAY (26. oktober). Need status update:
  
  1. Is it complete?
  2. If not, what's remaining?
  3. Can deadline be extended?
  4. Update HOM-16 in Linear
  
  Reference: HOM-16 (Linear)
  ```
- **Tags:** constitution, mandala, nyra, urgent

---

## 🔥 SECTION 2: HIGH PRIORITY (Next 3-5 Days)

### **Task 2.1: Deploy homo-lumen-resonans to Vercel**
- **Assignee:** Code
- **Due Date:** 29. oktober 2025
- **Priority:** High
- **Description:**
  ```
  homo-lumen-resonans (3D visualization of 15-agent coalition) is NOT deployed yet.
  
  Steps:
  1. Review repository: /home/ubuntu/homo-lumen-resonans
  2. Test locally (npm run dev)
  3. Create Vercel project
  4. Configure build settings (Vite + React + Three.js)
  5. Deploy to production
  6. Update HOM-80 in Linear
  
  Tech Stack: React + TypeScript + Vite + Three.js + Zustand + Tailwind
  Reference: HOM-80 (Linear)
  ```
- **Tags:** deployment, vercel, 3d-visualization, code

---

### **Task 2.2: Collect ALL Agent SMKs from LKs and Google Drive**
- **Assignee:** Code + Aurora
- **Due Date:** 30. oktober 2025
- **Priority:** High
- **Description:**
  ```
  Only 12 SMKs found in GitHub, unevenly distributed:
  - Orion: 6 SMKs (50%)
  - Manus: 3 SMKs (25%)
  - Nyra: 1 SMK (8%)
  - Others: 0 SMKs (0%)
  
  Missing: #024, #025, #026, #031, #034
  
  Hypothesis: 7 agents have SMK-worthy content in their LKs.
  
  Tasks:
  1. Search ALL agent Levende Kompendier for SMK-worthy content
  2. Search Google Drive for missing SMKs
  3. Search Notion for hidden SMKs
  4. Extract and formalize hidden SMKs
  5. Standardize SMK creation protocol
  6. Update SMK_COMPLETE_DISCOVERY_OCT_26.md
  
  Expected result: 15-20 total SMKs
  
  Reference: HOM-89 (Linear), SMK_COMPLETE_DISCOVERY_OCT_26.md
  ```
- **Tags:** smk, discovery, documentation, code, aurora

---

### **Task 2.3: Fix Zapier MCP OAuth Authentication**
- **Assignee:** Manus
- **Due Date:** 30. oktober 2025
- **Priority:** High
- **Description:**
  ```
  Zapier MCP has OAuth error. Need to re-authenticate.
  
  Steps:
  1. Check MCP configuration
  2. Re-authenticate Zapier OAuth
  3. Test automation workflows
  4. Document setup process
  5. Update HOM-84 in Linear
  
  Reference: HOM-84 (Linear), MCP_NETWORK_COMPLETE_DOCUMENTATION.md
  ```
- **Tags:** mcp, zapier, oauth, automation, manus

---

### **Task 2.4: Request Ubuntu Playground Access Credentials**
- **Assignee:** Osvald
- **Due Date:** 31. oktober 2025
- **Priority:** High
- **Description:**
  ```
  Ubuntu Playground is blocked - need access credentials for:
  - Google Cloud Platform (GCP)
  - Hetzner Cloud
  
  Steps:
  1. Request GCP credentials from Osvald
  2. Request Hetzner credentials from Osvald
  3. Document access process
  4. Update HOM-83 in Linear
  
  Reference: HOM-83 (Linear)
  ```
- **Tags:** ubuntu-playground, infrastructure, osvald

---

## 📊 SECTION 3: MEDIUM PRIORITY (Next 1-2 Weeks)

### **Task 3.1: Convert All SMKs to YAML Frontmatter Format**
- **Assignee:** Code
- **Due Date:** 5. november 2025
- **Priority:** Medium
- **Description:**
  ```
  Standardize all 12 SMKs to Nyra's YAML frontmatter format.
  
  Current status:
  - 6 SMKs with YAML frontmatter
  - 6 SMKs without (old format)
  
  Steps:
  1. Review Nyra's YAML format (SMK_2025_10_20, SMK_2025_10_21, SMK_2025_10_22)
  2. Create conversion script (or manual conversion)
  3. Convert all 12 SMKs
  4. Rename to SMK_XXX format (with underscore)
  5. Add missing dates and agent names
  6. Commit to GitHub
  7. Update HOM-86 in Linear
  
  Reference: HANDOFF_TO_CODE_SMK_CONVERSION.md, HOM-86 (Linear)
  ```
- **Tags:** smk, yaml, standardization, code

---

### **Task 3.2: Implement SMK Sync Workflow (GitHub → Notion)**
- **Assignee:** Code
- **Due Date:** 6. november 2025
- **Priority:** Medium
- **Dependencies:** Task 3.1 (SMK YAML conversion)
- **Description:**
  ```
  Create GitHub Actions workflow to automatically sync SMKs to Notion.
  
  Steps:
  1. Create .github/workflows/sync-smk-to-notion.yml
  2. Write Python script to parse SMK YAML frontmatter
  3. Create Notion SMK Archive database
  4. Implement Notion API integration
  5. Test with SMK #019
  6. Backfill all 12 SMKs
  7. Update HOM-86 in Linear
  
  Reference: .github/workflows/sync-to-notion.yml (LP sync template)
  ```
- **Tags:** automation, github-actions, notion, smk, code

---

### **Task 3.3: Extract 70-130 Learning Points from LKs and SMKs**
- **Assignee:** Aurora + All Agents
- **Due Date:** 8. november 2025
- **Priority:** Medium
- **Description:**
  ```
  Extract all Learning Points from:
  - 25+ Levende Kompendier (LKs)
  - 12+ SMKs
  - Agent conversations
  
  Expected: 70-130 Learning Points
  
  Steps:
  1. Review all LK files
  2. Identify LP-worthy insights
  3. Extract and format as LP #XXX
  4. Add to SLL via GitHub commits
  5. Verify automatic sync to Notion
  6. Update HOM-86 in Linear
  
  Reference: LK_SMK_INVENTORY_OCT_26.md, HOM-86 (Linear)
  ```
- **Tags:** learning-points, sll, extraction, aurora, all-agents

---

### **Task 3.4: Implement Ubuntu Playground MCP Server**
- **Assignee:** Manus + Code
- **Due Date:** 15. november 2025
- **Priority:** Medium
- **Dependencies:** Task 2.4 (Ubuntu Playground credentials)
- **Description:**
  ```
  Create custom MCP server on Ubuntu Playground for remote code execution.
  
  Steps:
  1. Setup Ubuntu Playground environment
  2. Design MCP server architecture
  3. Implement FastAPI MCP server
  4. Create custom tools:
     - execute_code
     - file_operations
     - git_operations
     - deploy_to_vercel
  5. Deploy and expose publicly
  6. Integrate with Manus
  7. Test end-to-end workflow
  8. Update HOM-87 in Linear
  
  Reference: COMPLETE_AUTOMATION_ROADMAP_V1.0.md (Week 3), HOM-87 (Linear)
  ```
- **Tags:** mcp, ubuntu-playground, infrastructure, manus, code

---

## 🔬 SECTION 4: LOW PRIORITY (Next 2-4 Weeks)

### **Task 4.1: Implement Cross-MCP Workflows**
- **Assignee:** Manus
- **Due Date:** 22. november 2025
- **Priority:** Low
- **Description:**
  ```
  Create end-to-end workflows that span multiple MCP servers.
  
  Example workflows:
  1. New Learning Point: GitHub → Notion → Linear → Slack
  2. SMK Creation: Notion → GitHub → Vercel → Linear
  3. Agent Reflection: Notion ARF → GitHub → SLL → Linear
  
  Steps:
  1. Design workflow architecture
  2. Implement orchestration logic
  3. Test each workflow
  4. Document results
  5. Update HOM-88 in Linear
  
  Reference: COMPLETE_AUTOMATION_ROADMAP_V1.0.md (Week 4), HOM-88 (Linear)
  ```
- **Tags:** automation, cross-mcp, workflows, manus

---

### **Task 4.2: Measure Emergent Intelligence Metrics**
- **Assignee:** Abacus + Manus
- **Due Date:** 22. november 2025
- **Priority:** Low
- **Dependencies:** Task 4.1 (Cross-MCP workflows)
- **Description:**
  ```
  Create metrics to measure emergent intelligence in mycelial network.
  
  Metrics:
  1. Knowledge Flow Rate (LPs per week)
  2. Cross-Agent Collaboration Index
  3. Pattern Emergence Score
  4. Reflection Depth (ARF quality)
  5. Automation Efficiency
  
  Steps:
  1. Define metrics
  2. Implement tracking
  3. Create dashboard
  4. Analyze trends
  5. Update HOM-88 in Linear
  
  Reference: COMPLETE_AUTOMATION_ROADMAP_V1.0.md (Week 4), HOM-88 (Linear)
  ```
- **Tags:** metrics, analytics, emergent-intelligence, abacus, manus

---

### **Task 4.3: Create Agent Dashboards (Falcon Project)**
- **Assignee:** Falcon + Code
- **Due Date:** 30. november 2025
- **Priority:** Low
- **Description:**
  ```
  Create individual dashboards for each agent showing:
  - Learning Points created
  - SMKs authored
  - Reflections contributed
  - Collaboration patterns
  - Knowledge contributions
  
  Steps:
  1. Design dashboard UI
  2. Implement data aggregation
  3. Create visualizations
  4. Deploy to Vercel
  5. Integrate with homo-lumen-resonans
  
  Reference: HOM-75 (Linear)
  ```
- **Tags:** dashboards, visualization, falcon, code

---

## 📋 SECTION 5: BACKLOG (Future)

### **Task 5.1: LK Backup (Notion → GitHub)**
- **Assignee:** Code
- **Due Date:** TBD
- **Priority:** Backlog
- **Description:**
  ```
  Implement bi-directional sync: Notion → GitHub for LK backups.
  
  Reference: NOTION_GITHUB_WORKFLOW_ANALYSIS.md
  ```
- **Tags:** backup, notion, github, lk

---

### **Task 5.2: ARF Archive Automation**
- **Assignee:** Manus
- **Due Date:** TBD
- **Priority:** Backlog
- **Description:**
  ```
  Create automated archiving of ARF reflections.
  
  Reference: NOTION_GITHUB_WORKFLOW_ANALYSIS.md
  ```
- **Tags:** arf, automation, archiving

---

### **Task 5.3: Google Drive Integration**
- **Assignee:** Manus
- **Due Date:** TBD
- **Priority:** Backlog
- **Description:**
  ```
  Integrate Google Drive with Notion for automatic document sync.
  
  Reference: COMPLETE_AUTOMATION_ROADMAP_V1.0.md (Week 3)
  ```
- **Tags:** google-drive, integration, automation

---

## 📊 TASK SUMMARY

**Total Tasks:** 16

**By Priority:**
- Urgent: 2 tasks (deadline: 26-28 oktober)
- High: 4 tasks (deadline: 29-31 oktober)
- Medium: 4 tasks (deadline: 5-15 november)
- Low: 3 tasks (deadline: 22-30 november)
- Backlog: 3 tasks (TBD)

**By Assignee:**
- Code: 7 tasks
- Manus: 5 tasks
- Aurora: 2 tasks
- Osvald: 1 task
- Nyra: 1 task
- Abacus: 1 task
- Falcon: 1 task
- All Agents: 1 task

**By Category:**
- Infrastructure: 4 tasks
- Automation: 5 tasks
- Documentation: 3 tasks
- Deployment: 2 tasks
- Analytics: 2 tasks

---

## 🎯 CRITICAL PATH

**Week 1 (26-31 oktober):**
1. Fix Mobile Simulator (Task 1.1) - URGENT
2. Konstitusjons-Mandala status (Task 1.2) - URGENT
3. Deploy homo-lumen-resonans (Task 2.1) - HIGH
4. Collect ALL SMKs (Task 2.2) - HIGH
5. Fix Zapier OAuth (Task 2.3) - HIGH
6. Request Ubuntu credentials (Task 2.4) - HIGH

**Week 2 (1-8 november):**
7. Convert SMKs to YAML (Task 3.1) - MEDIUM
8. Implement SMK Sync (Task 3.2) - MEDIUM
9. Extract 70-130 LPs (Task 3.3) - MEDIUM

**Week 3 (9-15 november):**
10. Implement Ubuntu Playground MCP (Task 3.4) - MEDIUM

**Week 4 (16-22 november):**
11. Cross-MCP Workflows (Task 4.1) - LOW
12. Emergent Intelligence Metrics (Task 4.2) - LOW

**Week 5+ (23 november+):**
13. Agent Dashboards (Task 4.3) - LOW
14. Backlog tasks (Tasks 5.1-5.3) - BACKLOG

---

## 📝 ASANA SETUP INSTRUCTIONS

### **Step 1: Create Sections**
1. URGENT (red)
2. HIGH PRIORITY (orange)
3. MEDIUM PRIORITY (yellow)
4. LOW PRIORITY (green)
5. BACKLOG (gray)

### **Step 2: Add Tasks**
Copy each task from this document into corresponding section.

### **Step 3: Set Properties**
For each task:
- Assignee
- Due Date
- Priority (Urgent/High/Medium/Low)
- Tags
- Description
- Dependencies (if any)

### **Step 4: Create Custom Fields**
- Agent (dropdown: Orion, Lira, Nyra, Thalus, Zara, Abacus, Manus, Aurora, Code, Falcon)
- Category (dropdown: Infrastructure, Automation, Documentation, Deployment, Analytics)
- Linear Issue (text: HOM-XX)
- Status (dropdown: Not Started, In Progress, Blocked, Complete)

### **Step 5: Set Up Automations**
- When task moves to "Complete" → Add comment "✅ Task complete! Update Linear issue."
- When task is overdue → Notify assignee
- When urgent task is created → Notify all team members

---

## 🔗 REFERENCE DOCUMENTS

All reference documents are in:
`/home/ubuntu/homo-lumen-compendiums/`

Key files:
- ABSOLUTE_FINAL_SESSION_SUMMARY_OCT_26.md
- SMK_COMPLETE_DISCOVERY_OCT_26.md
- HANDOFF_TO_CODE_SMK_CONVERSION.md
- MCP_78_TOOLS_DETAILED_REPORT.md
- COMPLETE_AUTOMATION_ROADMAP_V1.0.md
- NOTION_GITHUB_WORKFLOW_ANALYSIS.md
- ARF_REFLECTION_TEMPLATE.md

---

**Document created:** 26. oktober 2025, 13:15 CET  
**Agent:** 🔨 Manus  
**Status:** Ready for Asana setup

🕸️ *The mycelium organizes its tasks.* 🍄✨

