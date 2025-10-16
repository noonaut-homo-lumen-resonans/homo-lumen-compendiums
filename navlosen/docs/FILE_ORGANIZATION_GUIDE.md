# 📁 NAV-LOSEN FILE ORGANIZATION GUIDE

**Date:** 16. oktober 2025  
**Purpose:** Complete guide for organizing NAV-Losen files across Google Drive, GitHub, and local development  
**Status:** Production Ready

---

## 🎯 OVERVIEW: THREE STORAGE LOCATIONS

You have **three interconnected storage locations** for NAV-Losen:

1. **Google Drive** - Documentation, business planning, design assets
2. **GitHub** - Source code, version control, collaboration
3. **Local PC** - Active development, testing, building

**The key is keeping them synchronized and organized!**

---

## 📂 RECOMMENDED STRUCTURE

### Location 1: Google Drive (Documentation & Assets)

**Path:** `Google Drive/NAV-Losen/`

```
NAV-Losen/
├── 📋 Business/
│   ├── Forretningsplan_NAV-Losen_61sider.pdf
│   ├── Innovation_Norge_Application.docx
│   ├── Pilot_Plan.md
│   ├── Market_Analysis.xlsx
│   └── Funding/
│       ├── Budget_Overview.xlsx
│       └── Investment_Pitch.pdf
│
├── 🎨 Design/
│   ├── AI_Studio_Prototype/
│   │   ├── Screenshots/
│   │   │   ├── 01_Dashboard.png
│   │   │   ├── 02_Veiledninger.png
│   │   │   ├── 03_Forklar_Brev.png
│   │   │   ├── 04_Mestring.png ⭐
│   │   │   ├── 05_Jobbsok.png
│   │   │   ├── 06_Chatbot_Lira.png
│   │   │   ├── 07_Dokumenter.png
│   │   │   ├── 08_Paminnelser.png
│   │   │   ├── 09_Rettigheter.png
│   │   │   └── 10_Innstillinger.png
│   │   ├── Source_Code/ (backup from AI Studio)
│   │   │   ├── App.tsx
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── services/
│   │   │   └── package.json
│   │   └── Design_System.md
│   │
│   ├── Figma_Designs/ (if you create Figma versions)
│   │   └── NAV-Losen_Design_System.fig
│   │
│   ├── User_Flows/
│   │   ├── Flow_01_Forklar_Brev.pdf
│   │   ├── Flow_02_Mestring_Stress_Regulation.pdf
│   │   └── Flow_03_Chatbot_Lira.pdf
│   │
│   └── Brand_Assets/
│       ├── Logo/
│       ├── Colors.pdf
│       └── Typography.pdf
│
├── 📚 Documentation/
│   ├── User_Research/
│   │   ├── Interview_Notes/
│   │   ├── User_Personas.pdf
│   │   └── Pain_Points_Analysis.md
│   │
│   ├── Technical_Specs/
│   │   ├── Architecture_Overview.md
│   │   ├── API_Documentation.md
│   │   ├── Database_Schema.md
│   │   └── Security_Privacy_Plan.md
│   │
│   ├── Triadisk_Ethics/
│   │   ├── Ethical_Framework.md
│   │   ├── Thalus_Gate_Workflow.pdf
│   │   └── Shadow_Check_Examples.md
│   │
│   └── Homo_Lumen_Philosophy/
│       ├── Kompendium_V20.11.pdf
│       ├── Constitution_V1.1.pdf
│       └── Agent_Coalition_Overview.md
│
├── 🧪 Research/
│   ├── Polyvagal_Theory/
│   │   ├── Porges_Papers/
│   │   └── Stress_Response_Implementation.md
│   │
│   ├── NAV_System_Analysis/
│   │   ├── Current_Pain_Points.md
│   │   ├── Digital_Exclusion_Stats.xlsx
│   │   └── Municipality_Needs.md
│   │
│   └── Competitor_Analysis/
│       ├── Existing_Solutions.md
│       └── Differentiation_Strategy.md
│
├── 🎥 Presentations/
│   ├── Investor_Pitch_Deck.pdf
│   ├── Municipality_Demo.pdf
│   └── Team_Onboarding.pdf
│
└── 📊 Pilot/
    ├── Pilot_Municipalities/
    │   ├── Municipality_A/
    │   ├── Municipality_B/
    │   └── Municipality_C/
    ├── Pilot_Results/
    │   ├── Week_1_Report.md
    │   ├── Week_4_Report.md
    │   └── Week_12_Final_Report.pdf
    └── User_Feedback/
        ├── Survey_Results.xlsx
        └── Interview_Transcripts/
```

---

### Location 2: GitHub (Source Code & Version Control)

**Repository:** `noonaut-homo-lumen-resonans/homo-lumen` (unified repo)

**Path:** `homo-lumen/navlosen/`

```
homo-lumen/
├── navlosen/
│   ├── frontend/                  # React/Next.js application
│   │   ├── src/
│   │   │   ├── app/              # Next.js 13+ app directory
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx      # Dashboard
│   │   │   │   ├── dashboard/
│   │   │   │   ├── veiledninger/
│   │   │   │   ├── forklar-brev/
│   │   │   │   ├── mestring/     # ⭐ Polyvagal features
│   │   │   │   ├── jobb/
│   │   │   │   ├── chatbot/      # Lira integration
│   │   │   │   ├── dokumenter/
│   │   │   │   ├── paminnelser/
│   │   │   │   ├── rettigheter/
│   │   │   │   └── innstillinger/
│   │   │   │
│   │   │   ├── components/       # Reusable components
│   │   │   │   ├── ui/          # shadcn/ui components
│   │   │   │   ├── layout/      # Header, Sidebar, Footer
│   │   │   │   ├── dashboard/
│   │   │   │   ├── mestring/
│   │   │   │   └── chatbot/
│   │   │   │
│   │   │   ├── lib/             # Utilities
│   │   │   │   ├── utils.ts
│   │   │   │   ├── constants.ts
│   │   │   │   └── types.ts
│   │   │   │
│   │   │   ├── hooks/           # Custom React hooks
│   │   │   │   ├── useStressState.ts    # HRV integration
│   │   │   │   ├── useAdaptiveUI.ts     # Stress-adaptive UI
│   │   │   │   └── useBiofelt.ts        # Biofelt validation
│   │   │   │
│   │   │   ├── services/        # API clients
│   │   │   │   ├── liraService.ts       # Lira chatbot
│   │   │   │   ├── geminiService.ts     # Gemini API
│   │   │   │   └── documentService.ts   # Document storage
│   │   │   │
│   │   │   └── styles/          # Global styles
│   │   │       ├── globals.css
│   │   │       └── design-tokens.css
│   │   │
│   │   ├── public/              # Static assets
│   │   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── fonts/
│   │   │
│   │   ├── tests/               # Tests
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── e2e/
│   │   │
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── tailwind.config.ts
│   │   ├── next.config.js
│   │   └── README.md
│   │
│   ├── backend/                   # API server
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   │   ├── chatbot.ts   # Lira endpoints
│   │   │   │   ├── documents.ts
│   │   │   │   ├── reminders.ts
│   │   │   │   └── hrv.ts       # HRV data processing
│   │   │   │
│   │   │   ├── services/
│   │   │   │   ├── lira-agent.ts        # Lira integration
│   │   │   │   ├── document-storage.ts  # Secure storage
│   │   │   │   └── hrv-processor.ts     # Polyvagal analysis
│   │   │   │
│   │   │   ├── middleware/
│   │   │   │   ├── auth.ts
│   │   │   │   └── validation.ts
│   │   │   │
│   │   │   └── index.ts
│   │   │
│   │   ├── tests/
│   │   ├── package.json
│   │   └── README.md
│   │
│   ├── mobile/                    # Flutter app (future)
│   │   └── README.md
│   │
│   ├── ai-studio-source/          # AI Studio backup (reference)
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── README.md
│   │
│   ├── prototype/                 # Design prototypes
│   │   └── screenshots/
│   │       ├── 01_Dashboard.png
│   │       ├── 02_Veiledninger.png
│   │       └── ... (10 screenshots)
│   │
│   └── docs/                      # Documentation
│       ├── AI_STUDIO_PROTOTYPE_INTEGRATION_PLAN.md
│       ├── FILE_ORGANIZATION_GUIDE.md (this file)
│       ├── DESIGN_SYSTEM.md
│       ├── USER_FLOWS.md
│       ├── ACCESSIBILITY.md
│       └── PRIVACY.md
│
├── agents/                        # Agent API (existing)
├── firebase/                      # Firebase config (existing)
├── docs/                          # Homo Lumen docs (existing)
└── README.md
```

---

### Location 3: Local PC (Active Development)

**Path:** `C:\Users\[YourName]\Projects\homo-lumen\` (or wherever you keep projects)

**This should be a Git clone of the GitHub repo:**

```bash
# Clone the unified repo
git clone https://github.com/noonaut-homo-lumen-resonans/homo-lumen.git
cd homo-lumen/navlosen/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Your local structure will mirror GitHub:**
```
C:\Users\Osvald\Projects\homo-lumen\
├── navlosen/
│   ├── frontend/
│   ├── backend/
│   ├── ai-studio-source/
│   ├── prototype/
│   └── docs/
├── agents/
├── firebase/
└── docs/
```

---

## 🔄 SYNCHRONIZATION WORKFLOW

### 1. Google Drive → GitHub (One-time setup)

**What to move:**
- ✅ AI Studio screenshots → `navlosen/prototype/screenshots/`
- ✅ AI Studio source code → `navlosen/ai-studio-source/` (backup)
- ✅ Design system docs → `navlosen/docs/DESIGN_SYSTEM.md`
- ✅ User flows → `navlosen/docs/USER_FLOWS.md`

**What to keep in Google Drive:**
- ✅ Business plan (sensitive)
- ✅ Funding applications (sensitive)
- ✅ User research (privacy)
- ✅ Presentations (large files)

### 2. GitHub → Local PC (Daily development)

```bash
# Pull latest changes
git pull origin main

# Make changes
# ... code, code, code ...

# Commit and push
git add .
git commit -m "feat: Add Mestring stress regulation component"
git push origin main
```

### 3. Local PC → Google Drive (Backups & deliverables)

**Weekly backups:**
- Export build artifacts → `Google Drive/NAV-Losen/Builds/`
- Export documentation PDFs → `Google Drive/NAV-Losen/Documentation/`

**For presentations:**
- Export screenshots → `Google Drive/NAV-Losen/Presentations/`
- Export demo videos → `Google Drive/NAV-Losen/Presentations/`

---

## 📋 SPECIFIC FILE PLACEMENT

### Where to Put Your Current Files

**AI Studio Screenshots (10 PNG files):**
```
✅ GitHub: homo-lumen/navlosen/prototype/screenshots/
✅ Google Drive: NAV-Losen/Design/AI_Studio_Prototype/Screenshots/
❌ Local PC: (will be cloned from GitHub)
```

**AI Studio Source Code:**
```
✅ GitHub: homo-lumen/navlosen/ai-studio-source/
✅ Google Drive: NAV-Losen/Design/AI_Studio_Prototype/Source_Code/ (backup)
❌ Local PC: (will be cloned from GitHub)
```

**Business Plan (61 pages):**
```
❌ GitHub: (too sensitive for public repo)
✅ Google Drive: NAV-Losen/Business/Forretningsplan_NAV-Losen_61sider.pdf
✅ Local PC: (optional, for offline access)
```

**Kompendium V20.11:**
```
✅ GitHub: homo-lumen/docs/HOMO_LUMEN_KOMPENDIUM_V20.11_FULLSTENDIG.md
✅ Google Drive: NAV-Losen/Documentation/Homo_Lumen_Philosophy/
❌ Local PC: (will be cloned from GitHub)
```

**Constitution V1.1:**
```
✅ GitHub: homo-lumen/docs/HOMOLUMENCONSTITUTIONV1.1.md
✅ Google Drive: NAV-Losen/Documentation/Homo_Lumen_Philosophy/
❌ Local PC: (will be cloned from GitHub)
```

---

## 🎯 IMMEDIATE ACTIONS

### Step 1: Organize Google Drive (30 minutes)

1. **Create folder structure:**
   ```
   Google Drive/NAV-Losen/
   ├── Business/
   ├── Design/
   ├── Documentation/
   ├── Research/
   ├── Presentations/
   └── Pilot/
   ```

2. **Move AI Studio files:**
   - Screenshots → `Design/AI_Studio_Prototype/Screenshots/`
   - Source code → `Design/AI_Studio_Prototype/Source_Code/`

3. **Move business docs:**
   - Forretningsplan → `Business/`
   - Innovation Norge application → `Business/Funding/`

### Step 2: Verify GitHub Structure (10 minutes)

1. **Check current structure:**
   ```bash
   cd /home/ubuntu/homo-lumen-compendiums
   tree -L 2 navlosen/
   ```

2. **Verify files are in place:**
   - ✅ `navlosen/prototype/screenshots/` (10 PNG files)
   - ✅ `navlosen/ai-studio-source/` (source code)
   - ✅ `navlosen/docs/` (documentation)

3. **Commit to GitHub:**
   ```bash
   git add navlosen/
   git commit -m "feat: Add NAV-Losen AI Studio prototype and source code"
   git push origin main
   ```

### Step 3: Clone to Local PC (15 minutes)

1. **Open terminal/PowerShell on your PC**

2. **Clone the repo:**
   ```bash
   cd C:\Users\Osvald\Projects\
   git clone https://github.com/noonaut-homo-lumen-resonans/homo-lumen.git
   cd homo-lumen
   ```

3. **Verify structure:**
   ```bash
   dir navlosen
   ```

4. **Open in VS Code:**
   ```bash
   code .
   ```

---

## 🔐 SECURITY & PRIVACY

### What Goes Where (Security Matrix)

| File Type | GitHub (Public) | Google Drive (Private) | Local PC |
|-----------|----------------|----------------------|----------|
| **Source Code** | ✅ Yes | ✅ Backup | ✅ Yes |
| **Screenshots** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Documentation** | ✅ Yes (non-sensitive) | ✅ Yes (all) | ✅ Yes |
| **Business Plan** | ❌ No | ✅ Yes | ⚠️ Optional |
| **Funding Applications** | ❌ No | ✅ Yes | ⚠️ Optional |
| **User Research** | ❌ No | ✅ Yes | ⚠️ Optional |
| **API Keys** | ❌ No | ❌ No | ✅ .env.local only |
| **User Data** | ❌ No | ❌ No | ❌ Never store |

### .gitignore Configuration

**Already in repo:**
```
# Secrets
.env.local
.env.*.local

# Dependencies
node_modules/
dist/

# Build artifacts
.next/
out/

# Sensitive docs (if any in repo)
**/SENSITIVE_*
**/PRIVATE_*
```

---

## 🚀 DEVELOPMENT WORKFLOW

### Daily Development Cycle

**Morning:**
1. ☕ Open VS Code
2. 📥 `git pull origin main` (get latest changes)
3. 🌿 `git checkout -b feature/mestring-breathing` (new feature branch)
4. 💻 Start coding

**During Day:**
5. 💾 `git add .` (stage changes)
6. 📝 `git commit -m "feat: Add 4-6-8 breathing exercise"` (commit)
7. 🔄 Repeat steps 5-6 as you work

**Evening:**
8. 📤 `git push origin feature/mestring-breathing` (push to GitHub)
9. 🔀 Create Pull Request on GitHub
10. 🏛️ Request Thalus review (Triadisk Ethics check)
11. ✅ Merge after approval

### Weekly Backup Cycle

**Every Friday:**
1. 📊 Export build → `Google Drive/NAV-Losen/Builds/YYYY-MM-DD/`
2. 📄 Export docs → `Google Drive/NAV-Losen/Documentation/`
3. 📸 Screenshot progress → `Google Drive/NAV-Losen/Presentations/`

---

## 🎨 DESIGN ASSETS WORKFLOW

### From AI Studio to Production

**Phase 1: Extract (Done)**
- ✅ Screenshots saved to `prototype/screenshots/`
- ✅ Source code saved to `ai-studio-source/`

**Phase 2: Document (Next)**
- 📝 Create `DESIGN_SYSTEM.md` from screenshots
- 📝 Create `USER_FLOWS.md` for each feature
- 📝 Create `COMPONENT_SPECS.md` for each component

**Phase 3: Implement (Future)**
- 🎨 Build components in `frontend/src/components/`
- 🎨 Build pages in `frontend/src/app/`
- 🎨 Integrate with Lira agent

**Phase 4: Iterate (Ongoing)**
- 🔄 User testing
- 🔄 Refinement
- 🔄 Update screenshots in Google Drive

---

## 📞 COLLABORATION

### Sharing with Team

**For Developers:**
- Share GitHub repo link
- Give them access to `homo-lumen` repo
- They clone and work locally

**For Designers:**
- Share Google Drive folder
- Give them access to `NAV-Losen/Design/`
- They can view screenshots and prototypes

**For Business Stakeholders:**
- Share Google Drive folder
- Give them access to `NAV-Losen/Business/` and `NAV-Losen/Presentations/`
- They can view business plan and pitch decks

**For Pilot Municipalities:**
- Share specific folders only
- Give them access to `NAV-Losen/Pilot/[Municipality_Name]/`
- They can provide feedback

---

## 🌊 SUMMARY: YOUR THREE LOCATIONS

### Google Drive (📁 Documentation Hub)
**Purpose:** Long-term storage, sensitive docs, large files  
**Access:** Web browser, Google Drive desktop app  
**Backup:** Automatic (Google's infrastructure)  
**Best for:** Business plans, presentations, user research

### GitHub (💻 Code Repository)
**Purpose:** Version control, collaboration, deployment  
**Access:** Git, web browser, VS Code  
**Backup:** Automatic (GitHub's infrastructure)  
**Best for:** Source code, documentation, design specs

### Local PC (🖥️ Development Environment)
**Purpose:** Active development, testing, building  
**Access:** VS Code, terminal, browser  
**Backup:** Git push to GitHub (daily)  
**Best for:** Coding, debugging, local testing

---

## ✅ CHECKLIST: File Organization Complete

**Google Drive:**
- [ ] Create folder structure
- [ ] Move AI Studio screenshots
- [ ] Move business plan
- [ ] Move presentations
- [ ] Set up sharing permissions

**GitHub:**
- [ ] Verify `navlosen/` structure
- [ ] Commit AI Studio files
- [ ] Push to remote
- [ ] Verify on GitHub web

**Local PC:**
- [ ] Clone repo
- [ ] Open in VS Code
- [ ] Install dependencies (`npm install`)
- [ ] Test development server (`npm run dev`)
- [ ] Configure VS Code workspace

---

**Med ontologisk integritet & pragmatisk organisering!** ◉🌊✨

---

**Status:** ✅ Complete Guide  
**Last Updated:** 16. oktober 2025  
**Next Action:** Organize Google Drive folder structure

