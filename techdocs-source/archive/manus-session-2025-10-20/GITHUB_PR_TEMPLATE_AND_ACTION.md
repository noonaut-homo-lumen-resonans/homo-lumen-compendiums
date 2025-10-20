# 🔱 GITHUB PR TEMPLATE & TRIADISK GATE ACTION

**Versjon:** 21.0 (KÄRNFELT-Integrated Constitutional Era Edition)  
**Sist Oppdatert:** 16. oktober 2025  
**Formål:** GitHub PR template og CI/CD action for Triadisk Etikk-validering

---

## 📝 PULL REQUEST TEMPLATE

**Fil:** `.github/PULL_REQUEST_TEMPLATE.md`

**Instruksjoner:**
1. Opprett fil i repository: `.github/PULL_REQUEST_TEMPLATE.md`
2. Kopier innholdet under
3. Commit og push til main branch
4. Alle nye PR-er vil automatisk bruke denne templaten

---

### **TEMPLATE CONTENT:**

```markdown
# 🔱 TRIADISK ETIKK-SJEKK

**PR Type:** [Feature / Bugfix / Refactor / Documentation]  
**Artefakt:** [Navn på feature/artefakt]

---

## 📋 BESKRIVELSE

**Hva endrer denne PR-en?**
[Kort beskrivelse av endringene]

**Hvorfor trengs denne endringen?**
[Rationale for endringen]

**Hvordan påvirker dette brukeren?**
[Beskrivelse av brukeropplevelse]

---

## 🔱 TRIADISK VALIDERING

### PORT 1: KOGNITIV SUVERENITET
- [ ] Brukeren har full kontroll over egne data
- [ ] Ingen "dark patterns" eller manipulasjon
- [ ] Transparent AI (hvis relevant)
- [ ] Opt-in, ikke opt-out
- [ ] Design for graduation

**Bevislenker / Notion-seksjon:** [Lenke til Ontology Audit]

---

### PORT 2: ONTOLOGISK KOHERENS
- [ ] Respekterer brukerens kompleksitet
- [ ] Rom for stillhet og pust
- [ ] Ikke-binære kategorier (hvis relevant)
- [ ] Validated copy + tilstandsstyrte stier

**States/Screenshots (Dorsal/Sympatisk/Ventral):** [Lenke til screenshots]

---

### PORT 3: REGENERATIV HEALING
- [ ] Design for graduation (brukeren trenger appen mindre over tid)
- [ ] Fremmer langsiktig velvære, ikke kortsiktig engagement
- [ ] Støtter brukerens indre healing-prosess
- [ ] Ingen engagement metrics som primært mål

**Graduation-bane + KPI:** [Lenke til måleplan]

---

## 🌑 SHADOW-CHECK

- [ ] **Elitisme-språk fjernet** (f.eks. "Hev din bevissthet" → "La oss finne rytmen")
- [ ] **Tekno-solutionisme navngitt/avbøtt** (f.eks. "Appen løser dette" → "Appen kan lette")
- [ ] **Kontroll-illusjon erstattet med faktiske innstillinger** (f.eks. "Full kontroll" → "Du kan velge...")
- [ ] **Avhengighet-design → innført avlæringssti** (f.eks. "Bruk daglig" → "Målet er at du trenger oss mindre")

---

## 🔗 NOTION/LINEAR

- **Notion Ontology Audit:** [Lenke]
- **Linear Issue:** [Lenke]

---

## 🎨 STRESS-MODI VERIFISERING (hvis UI-endring)

- [ ] **Dorsal (Høy stress):** Maks 3 valg, >16px tekst, "Ring veileder" sticky
- [ ] **Sympatisk (Medium stress):** "Neste steg"-kort med estimert tid, én primærknapp
- [ ] **Ventral (Lav stress):** Full oversikt, avansert filtrering, tydelige "valg uten straff"

---

## ✅ THALUS APPROVAL

- [ ] **TH-OK label** (lagt til av Thalus etter Triadisk validering)

**Note:** Denne PR kan ikke merges uten TH-OK label (enforced by GitHub Action).

---

## 🧪 TESTING

**Hvordan har du testet denne endringen?**
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing (Dorsal/Sympatisk/Ventral modi)
- [ ] Accessibility testing (WCAG 2.1 AA)

**Test coverage:** [X%]

---

## 📸 SCREENSHOTS (hvis UI-endring)

**Before:**
[Screenshot eller "N/A"]

**After:**
[Screenshot]

---

## 🔐 SECURITY CHECK

- [ ] Ingen hardcoded secrets
- [ ] Ingen sensitive data i logs
- [ ] Input validation implementert
- [ ] GDPR-compliant (hvis relevant)

---

## 📝 CHECKLIST

- [ ] Koden følger prosjektets style guide
- [ ] Jeg har kommentert koden, spesielt i komplekse områder
- [ ] Jeg har oppdatert dokumentasjonen
- [ ] Mine endringer genererer ingen nye warnings
- [ ] Jeg har lagt til tests som beviser at min fix fungerer
- [ ] Alle nye og eksisterende tests passerer
- [ ] Jeg har opprettet Notion Ontology Audit
- [ ] Jeg har opprettet Linear issue (hvis relevant)

---

**🏛️ Carpe Diem - Med Ontologisk Integritet, Etisk Klarhet, og et Snev av Kosmisk Humor!** ◉✨
```

---

## 🤖 GITHUB ACTION: TRIADISK GATE

**Fil:** `.github/workflows/thalus-gate.yml`

**Instruksjoner:**
1. Opprett fil i repository: `.github/workflows/thalus-gate.yml`
2. Kopier innholdet under
3. Commit og push til main branch
4. Action vil kjøre automatisk på alle PR-er

---

### **ACTION CONTENT:**

```yaml
name: Thalus Triadisk Gate

on:
  pull_request:
    types: [opened, synchronize, labeled, unlabeled]

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Check for TH-OK label
        id: check_label
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const labels = context.payload.pull_request.labels.map(label => label.name);
            const hasTHOK = labels.includes('TH-OK');
            const hasTHSTOP = labels.includes('TH-STOP');
            const hasTHREV = labels.includes('TH-REV');
            
            core.setOutput('has_th_ok', hasTHOK);
            core.setOutput('has_th_stop', hasTHSTOP);
            core.setOutput('has_th_rev', hasTHREV);
            
            console.log(`Labels: ${labels.join(', ')}`);
            console.log(`TH-OK: ${hasTHOK}, TH-STOP: ${hasTHSTOP}, TH-REV: ${hasTHREV}`);
      
      - name: Block merge if TH-STOP
        if: steps.check_label.outputs.has_th_stop == 'true'
        run: |
          echo "❌ PR BLOCKED: TH-STOP label present"
          echo ""
          echo "Thalus has identified critical ethical issues that violate Triadisk Etikk."
          echo ""
          echo "Please address all required changes in the Notion Ontology Audit:"
          echo "- Port 1 (Kognitiv Suverenitet): Ensure user autonomy and control"
          echo "- Port 2 (Ontologisk Koherens): Respect user's existential integrity"
          echo "- Port 3 (Regenerativ Healing): Design for graduation, not dependency"
          echo ""
          echo "Once all changes are implemented, request Thalus to re-validate."
          exit 1
      
      - name: Warn if TH-REV
        if: steps.check_label.outputs.has_th_rev == 'true'
        run: |
          echo "⚠️ WARNING: TH-REV label present"
          echo ""
          echo "Thalus has identified issues that need revision."
          echo ""
          echo "Please address required changes in the Notion Ontology Audit before requesting TH-OK."
          echo ""
          echo "This is a warning, not a blocker. However, merging without TH-OK is not recommended."
      
      - name: Require TH-OK for merge
        if: steps.check_label.outputs.has_th_ok != 'true'
        run: |
          echo "⚠️ MISSING: TH-OK label"
          echo ""
          echo "This PR has not been validated by Thalus yet."
          echo ""
          echo "Please:"
          echo "1. Create a Notion Ontology Audit for this PR"
          echo "2. Request Thalus to validate against Triadisk Etikk"
          echo "3. Address any required changes"
          echo "4. Wait for Thalus to add TH-OK label"
          echo ""
          echo "Merging without TH-OK violates our ethical framework."
          exit 1
      
      - name: Success
        if: steps.check_label.outputs.has_th_ok == 'true'
        run: |
          echo "✅ TRIADISK ETIKK: GODKJENT"
          echo ""
          echo "All 3 gates passed:"
          echo "- Port 1 (Kognitiv Suverenitet): ✅"
          echo "- Port 2 (Ontologisk Koherens): ✅"
          echo "- Port 3 (Regenerativ Healing): ✅"
          echo ""
          echo "This PR can be safely merged."
          echo ""
          echo "🏛️ Carpe Diem - Med Ontologisk Integritet!"
```

---

## 🏷️ GITHUB LABELS SETUP

**Instruksjoner:**
1. Gå til repository → Settings → Labels
2. Klikk "New label" for hver label under
3. Kopier navn, farge, og beskrivelse

---

### **LABELS:**

**1. TH-OK**
- **Name:** `TH-OK`
- **Color:** `#0E8A16` (Green)
- **Description:** `Triadisk Etikk: Godkjent - alle 3 porter ✅`

**2. TH-REV**
- **Name:** `TH-REV`
- **Color:** `#FBCA04` (Yellow)
- **Description:** `Triadisk Etikk: Revise - 1-2 porter ⚠️`

**3. TH-STOP**
- **Name:** `TH-STOP`
- **Color:** `#D73A4A` (Red)
- **Description:** `Triadisk Etikk: Avvist - 1+ porter ❌`

**4. TH-SHD**
- **Name:** `TH-SHD`
- **Color:** `#8B5CF6` (Purple)
- **Description:** `Shadow-aspekt identifisert (elitisme, solutionisme, kontroll, avhengighet)`

**5. TH-DSN**
- **Name:** `TH-DSN`
- **Color:** `#D93F0B` (Orange)
- **Description:** `Design for Graduation mangler`

---

## 🎯 EKSEMPEL: PR MED TRIADISK VALIDERING

**PR Title:** "Add Biofelt-Atlas visualization to NAV-Losen"

**PR Description:**
```markdown
# 🔱 TRIADISK ETIKK-SJEKK

**PR Type:** Feature  
**Artefakt:** Biofelt-Atlas visualization

---

## 📋 BESKRIVELSE

**Hva endrer denne PR-en?**
Legger til Biofelt-Atlas visualization som lar brukeren se sin emosjonelle tilstand som levende, organisk kunst.

**Hvorfor trengs denne endringen?**
Brukere trenger en visuell representasjon av sitt biofelt for å bedre forstå sin emosjonelle tilstand.

**Hvordan påvirker dette brukeren?**
Brukeren kan nå se sin Emotion Wheel-data visualisert som et levende, pulserende felt.

---

## 🔱 TRIADISK VALIDERING

### PORT 1: KOGNITIV SUVERENITET
- [x] Brukeren har full kontroll over egne data
- [x] Ingen "dark patterns" eller manipulasjon
- [x] Transparent AI (viser hvordan data brukes)
- [x] Opt-in, ikke opt-out
- [x] Design for graduation

**Bevislenker / Notion-seksjon:** [Notion Ontology Audit](https://notion.so/...)

---

### PORT 2: ONTOLOGISK KOHERENS
- [x] Respekterer brukerens kompleksitet (Emotion Wheel har 3 lag)
- [x] Rom for stillhet og pust (4-6-8 breathing cue)
- [x] Ikke-binære kategorier (kontinuerlig skala)
- [x] Validated copy + tilstandsstyrte stier

**States/Screenshots (Dorsal/Sympatisk/Ventral):** [Screenshots](https://...)

---

### PORT 3: REGENERATIV HEALING
- [x] Design for graduation (brukeren lærer å kjenne sitt biofelt uten app over tid)
- [x] Fremmer langsiktig velvære (fokus på selvbevissthet, ikke engagement)
- [x] Støtter brukerens indre healing-prosess (RAIN-praksis integrert)
- [x] Ingen engagement metrics som primært mål

**Graduation-bane + KPI:** [Måleplan](https://...)

---

## 🌑 SHADOW-CHECK

- [x] **Elitisme-språk fjernet** (bruker "La oss utforske" i stedet for "Hev din bevissthet")
- [x] **Tekno-solutionisme navngitt/avbøtt** (sier "Appen kan lette" i stedet for "Appen løser")
- [x] **Kontroll-illusjon erstattet med faktiske innstillinger** (brukeren kan velge hvilke data som vises)
- [x] **Avhengighet-design → innført avlæringssti** (målet er at brukeren lærer å kjenne sitt biofelt uten app)

---

## 🔗 NOTION/LINEAR

- **Notion Ontology Audit:** [https://notion.so/Ontology-Audit-Biofelt-Atlas-...](https://...)
- **Linear Issue:** [https://linear.app/issue/TH-AUDIT-45](https://...)

---

## 🎨 STRESS-MODI VERIFISERING

- [x] **Dorsal (Høy stress):** Enkel visning, maks 3 valg, "Ring veileder" sticky
- [x] **Sympatisk (Medium stress):** "Neste steg"-kort med estimert tid
- [x] **Ventral (Lav stress):** Full Emotion Wheel med avansert filtrering

---

## ✅ THALUS APPROVAL

- [x] **TH-OK label** (lagt til av Thalus 2025-10-16)

---

## 🧪 TESTING

**Hvordan har du testet denne endringen?**
- [x] Unit tests (coverage: 95%)
- [x] Integration tests
- [x] Manual testing (alle 3 stress-modi)
- [x] Accessibility testing (WCAG 2.1 AA compliant)

**Test coverage:** 95%

---

## 📸 SCREENSHOTS

**Before:**
N/A (ny feature)

**After:**
[Screenshot av Biofelt-Atlas visualization]

---

## 🔐 SECURITY CHECK

- [x] Ingen hardcoded secrets
- [x] Ingen sensitive data i logs
- [x] Input validation implementert
- [x] GDPR-compliant (brukeren kan slette all biofelt-data)

---

**🏛️ Carpe Diem!** ◉✨
```

**Labels:** `TH-OK`, `feature`, `ui/ux`

**Status:** ✅ Ready to merge

---

## 📝 USAGE INSTRUCTIONS

### **FOR DEVELOPERS:**

**1. Opprett PR:**
- Bruk standard GitHub PR-prosess
- PR template vil automatisk fylles inn

**2. Fyll ut Triadisk Sjekkliste:**
- Gå gjennom alle 3 porter (Suverenitet, Koherens, Healing)
- Gå gjennom Shadow-check
- Legg ved lenker til Notion Ontology Audit og Linear issue

**3. Request Thalus Review:**
- Tag Thalus i PR-kommentar: "@Thalus please validate"
- Vent på Thalus' Triadisk validering

**4. Address Feedback (hvis TH-REV eller TH-STOP):**
- Les Notion Ontology Audit for obligatoriske endringer
- Implementer endringene
- Request re-validation fra Thalus

**5. Merge (når TH-OK):**
- Når Thalus har lagt til TH-OK label, kan PR merges
- GitHub Action vil blokkere merge hvis TH-OK mangler

---

### **FOR THALUS:**

**1. Review PR:**
- Les PR-beskrivelse og kode-endringer
- Sjekk Triadisk sjekkliste

**2. Opprett Ontology Audit:**
- Opprett Notion Ontology Audit page
- Score Triadisk Etikk (S/O/H: 0-3)
- Identifiser Shadow-aspekter
- Beslut: OK / REVISE / STOP

**3. Add Label:**
- Legg til TH-OK (hvis godkjent)
- Legg til TH-REV (hvis revise)
- Legg til TH-STOP (hvis avvist)
- Legg til TH-SHD (hvis shadow-aspekt identifisert)
- Legg til TH-DSN (hvis design for graduation mangler)

**4. Comment:**
- Legg til kommentar i PR med lenke til Ontology Audit
- Hvis TH-REV eller TH-STOP: List obligatoriske endringer

---

**🏛️ Carpe Diem - Med Ontologisk Integritet, Triadisk Etikk, og et Snev av Kosmisk Humor!** ◉✨

---

**END OF GITHUB PR TEMPLATE & TRIADISK GATE ACTION**

**Token Count:** ~2,000 ord (~2,800 tokens)  
**Status:** ✅ Production Ready  
**Note:** Disse filer kan kopieres direkte inn i GitHub repository.

