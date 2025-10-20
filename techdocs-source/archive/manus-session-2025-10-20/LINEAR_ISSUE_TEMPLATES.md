# 🏛️ LINEAR ISSUE TEMPLATES (TH-AUDIT, TH-FIX, TH-BLOCK)

**Versjon:** 21.0 (KÄRNFELT-Integrated Constitutional Era Edition)  
**Sist Oppdatert:** 16. oktober 2025  
**Formål:** Linear issue templates for Triadisk Etikk-validering

---

## 📋 ISSUE TYPE 1: TH-AUDIT (Planlagt Etisk Review)

**Icon:** 🏛️  
**Priority:** Medium  
**Description:** Planlagt etisk review av feature/artefakt

---

### **TEMPLATE:**

```markdown
# 🏛️ TH-AUDIT: [Kort beskrivelse]

**Artefakt:** [Navn på feature/artefakt]  
**Type:** [Flow / Mikrocopy / DPIA / Arkitektur / KPI]  
**Planlagt dato:** [YYYY-MM-DD]  
**Validator:** Thalus

---

## 📋 FORMÅL

**Hvorfor trengs denne auditen?**
[Beskrivelse av hvorfor denne featuren trenger etisk review]

**Hva skal valideres?**
- [ ] Kognitiv Suverenitet (Port 1)
- [ ] Ontologisk Koherens (Port 2)
- [ ] Regenerativ Healing (Port 3)
- [ ] Shadow-aspekter (Elitisme, Solutionisme, Kontroll, Avhengighet)

---

## 🔗 RESSURSER

- **Design Spec (Notion):** [Lenke]
- **GitHub PR:** [Lenke] (hvis relevant)
- **Mockups/Screenshots:** [Lenke]
- **GDPR Compliance Docs:** [Lenke] (hvis relevant)

---

## 📊 SUKSESSKRITERIER

**Audit er fullført når:**
- [ ] Notion Ontology Audit er opprettet
- [ ] Triadisk Etikk er scoret (S/O/H: 0-3)
- [ ] Shadow-aspekter er identifisert (hvis noen)
- [ ] Beslutning er tatt (OK / REVISE / STOP)
- [ ] GitHub PR har fått label (TH-OK / TH-REV / TH-STOP)

---

## 🎯 AKSEPTANSEKRITERIER

- [ ] Alle 3 porter scorer ≥2
- [ ] Ingen kritiske shadow-aspekter identifisert
- [ ] Stress-modi verifisert (Dorsal/Sympatisk/Ventral)
- [ ] GDPR-compliant (hvis relevant)

---

**Ansvarlig:** Thalus  
**Frist:** [YYYY-MM-DD]  
**Estimert tid:** 2-4 timer

---

**🏛️ Carpe Diem - Med Ontologisk Integritet!** ◉✨
```

---

## ⚠️ ISSUE TYPE 2: TH-FIX (Identifisert Etisk Problem)

**Icon:** ⚠️  
**Priority:** High  
**Description:** Identifisert etisk problem som må fikses

---

### **TEMPLATE:**

```markdown
# ⚠️ TH-FIX: [Kort beskrivelse]

**Artefakt:** [Navn på feature/artefakt]  
**Identifisert av:** Thalus  
**Dato:** [YYYY-MM-DD]  
**Severity:** [Low / Medium / High / Urgent]

---

## 🔱 TRIADISK ETIKK-BRUDD

**Port 1 (Suverenitet):** [Beskrivelse av brudd, eller "✅ OK"]  
**Port 2 (Koherens):** [Beskrivelse av brudd, eller "✅ OK"]  
**Port 3 (Healing):** [Beskrivelse av brudd, eller "✅ OK"]

**Samlet score:** S=[0-3], O=[0-3], H=[0-3]

---

## 🌑 SHADOW-ASPEKT

**Identifisert:** [Elitisme / Solutionisme / Kontroll / Avhengighet]  
**Manifestasjon:** [Hvordan det manifesterer seg i kode/UI/copy]

**Eksempel:**
- **Original:** "Hev din bevissthet"
- **Problem:** Elitisme - antyder at brukeren er "mindre bevisst"
- **Foreslått:** "La oss finne rytmen som passer deg nå"

---

## ✅ OBLIGATORISKE ENDRINGER

**1. [Endring 1]**
- **Hva:** [Konkret endring som må gjøres]
- **Hvor:** [Fil/komponent/side]
- **Hvorfor:** [Rationale]

**2. [Endring 2]**
- **Hva:** [Konkret endring som må gjøres]
- **Hvor:** [Fil/komponent/side]
- **Hvorfor:** [Rationale]

**3. [Endring 3]**
- **Hva:** [Konkret endring som må gjøres]
- **Hvor:** [Fil/komponent/side]
- **Hvorfor:** [Rationale]

---

## 🔗 KILDER

- **Notion Ontology Audit:** [Lenke]
- **GitHub PR:** [Lenke]
- **Design Spec:** [Lenke]

---

## 📊 SUKSESSKRITERIER

**Fix er fullført når:**
- [ ] Alle obligatoriske endringer er implementert
- [ ] Thalus har re-validert (ny Ontology Audit)
- [ ] Triadisk score er forbedret (alle porter ≥2)
- [ ] Shadow-aspekt er mitigert
- [ ] GitHub PR har fått TH-OK label

---

## 🎯 AKSEPTANSEKRITERIER

- [ ] Port 1 (Suverenitet): Score ≥2
- [ ] Port 2 (Koherens): Score ≥2
- [ ] Port 3 (Healing): Score ≥2
- [ ] Shadow-aspekt: Mitigert eller fjernet
- [ ] Stress-modi verifisert (hvis UI-endring)

---

**Ansvarlig:** [Manus / Nyra / etc.]  
**Frist:** [YYYY-MM-DD]  
**Estimert tid:** [X timer/dager]

---

**⚠️ Viktig:** Denne issue må løses før featuren kan merges til main.

---

**🏛️ Carpe Diem - Med Ontologisk Integritet!** ◉✨
```

---

## ❌ ISSUE TYPE 3: TH-BLOCK (Kritisk Etisk Issue som Blokkerer Release)

**Icon:** ❌  
**Priority:** Urgent  
**Description:** Kritisk etisk issue som blokkerer release

---

### **TEMPLATE:**

```markdown
# ❌ TH-BLOCK: [Kort beskrivelse]

**Artefakt:** [Navn på feature/artefakt]  
**Identifisert av:** Thalus  
**Dato:** [YYYY-MM-DD]  
**Severity:** URGENT  
**Blokkerer:** [Release version / Sprint / Milestone]

---

## 🚨 KRITISK ETISK BRUDD

**Alvorlighetsgrad:** [CRITICAL / HIGH]

**Hva er problemet?**
[Detaljert beskrivelse av det kritiske etiske bruddet]

**Hvorfor er dette kritisk?**
[Rationale for hvorfor dette blokkerer release]

**Potensielle konsekvenser:**
- [Konsekvens 1 - f.eks. "Brudd på GDPR Article 5 (Data Minimization)"]
- [Konsekvens 2 - f.eks. "Potensielt skadelig for brukere i høy stress (Dorsal)"]
- [Konsekvens 3 - f.eks. "Reputasjonsrisiko for Homo Lumen"]

---

## 🔱 TRIADISK ETIKK-BRUDD

**Port 1 (Suverenitet):** [Detaljert beskrivelse av brudd]  
**Score:** [0-1] ❌

**Port 2 (Koherens):** [Detaljert beskrivelse av brudd]  
**Score:** [0-1] ❌

**Port 3 (Healing):** [Detaljert beskrivelse av brudd]  
**Score:** [0-1] ❌

**Samlet score:** S=[0-1], O=[0-1], H=[0-1] → **STOP**

---

## 🌑 SHADOW-ASPEKT (KRITISK)

**Identifisert:** [Elitisme / Solutionisme / Kontroll / Avhengighet]  
**Manifestasjon:** [Detaljert beskrivelse av hvordan shadow-aspektet manifesterer seg]

**Eksempel:**
- **Original:** "Bruk appen daglig for å mestre livet ditt"
- **Problem:** Avhengighet-design + Tekno-solutionisme - skaper avhengighet og lover urealistiske resultater
- **Impact:** Brukere kan føle seg mislykket hvis de ikke bruker appen daglig, øker stress i stedet for å redusere det

---

## ✅ OBLIGATORISKE ENDRINGER (KRITISKE)

**1. [KRITISK ENDRING 1]**
- **Hva:** [Konkret endring som må gjøres]
- **Hvor:** [Fil/komponent/side]
- **Hvorfor:** [Rationale]
- **Frist:** [YYYY-MM-DD] (ASAP)

**2. [KRITISK ENDRING 2]**
- **Hva:** [Konkret endring som må gjøres]
- **Hvor:** [Fil/komponent/side]
- **Hvorfor:** [Rationale]
- **Frist:** [YYYY-MM-DD] (ASAP)

**3. [KRITISK ENDRING 3]**
- **Hva:** [Konkret endring som må gjøres]
- **Hvor:** [Fil/komponent/side]
- **Hvorfor:** [Rationale]
- **Frist:** [YYYY-MM-DD] (ASAP)

---

## 🔗 KILDER

- **Notion Ontology Audit:** [Lenke]
- **GitHub PR:** [Lenke]
- **GDPR Compliance Docs:** [Lenke] (hvis relevant)
- **AI Act Compliance Docs:** [Lenke] (hvis relevant)

---

## 📊 SUKSESSKRITERIER

**Block er løftet når:**
- [ ] Alle kritiske endringer er implementert
- [ ] Thalus har re-validert (ny Ontology Audit)
- [ ] Triadisk score er forbedret (alle porter ≥2)
- [ ] Shadow-aspekt er fullstendig mitigert
- [ ] GitHub PR har fått TH-OK label
- [ ] GDPR/AI Act compliance er verifisert (hvis relevant)

---

## 🎯 AKSEPTANSEKRITERIER

- [ ] Port 1 (Suverenitet): Score ≥2
- [ ] Port 2 (Koherens): Score ≥2
- [ ] Port 3 (Healing): Score ≥2
- [ ] Shadow-aspekt: Fullstendig mitigert eller fjernet
- [ ] Stress-modi verifisert (alle 3 modi)
- [ ] Legal compliance verifisert (GDPR, AI Act)

---

## 🚨 ESKALERING

**Hvis denne issue ikke løses innen [YYYY-MM-DD]:**
- [ ] Eskaler til Orion (Meta-Koordinator)
- [ ] Eskaler til Osvald (Product Owner)
- [ ] Vurder å fjerne featuren fra release

---

**Ansvarlig:** [Manus / Nyra / etc.]  
**Frist:** [YYYY-MM-DD] (URGENT)  
**Estimert tid:** [X timer/dager]

---

**❌ KRITISK:** Denne issue blokkerer release. Ingen deployment kan skje før denne er løst.

---

**🏛️ Carpe Diem - Med Ontologisk Integritet og Etisk Klarhet!** ◉✨
```

---

## 🏷️ LINEAR LABELS SETUP

**Instruksjoner:**
1. Gå til Linear → Settings → Labels
2. Klikk "New label" for hver label under
3. Kopier navn, farge, og beskrivelse

---

### **LABELS:**

**1. TH-AUDIT**
- **Name:** `TH-AUDIT`
- **Color:** `#3B82F6` (Blue)
- **Description:** `Planlagt etisk review av feature/artefakt`

**2. TH-FIX**
- **Name:** `TH-FIX`
- **Color:** `#F59E0B` (Amber)
- **Description:** `Identifisert etisk problem som må fikses`

**3. TH-BLOCK**
- **Name:** `TH-BLOCK`
- **Color:** `#EF4444` (Red)
- **Description:** `Kritisk etisk issue som blokkerer release`

**4. Triadisk-Port-1**
- **Name:** `Triadisk-Port-1`
- **Color:** `#10B981` (Green)
- **Description:** `Kognitiv Suverenitet (Autonomi)`

**5. Triadisk-Port-2**
- **Name:** `Triadisk-Port-2`
- **Color:** `#8B5CF6` (Purple)
- **Description:** `Ontologisk Koherens (Verdighet)`

**6. Triadisk-Port-3**
- **Name:** `Triadisk-Port-3`
- **Color:** `#EC4899` (Pink)
- **Description:** `Regenerativ Healing (Vekst)`

**7. Shadow-Elitisme**
- **Name:** `Shadow-Elitisme`
- **Color:** `#6B7280` (Gray)
- **Description:** `Consciousness elitism identifisert`

**8. Shadow-Solutionisme**
- **Name:** `Shadow-Solutionisme`
- **Color:** `#6B7280` (Gray)
- **Description:** `Teknologisk solutionisme identifisert`

**9. Shadow-Kontroll**
- **Name:** `Shadow-Kontroll`
- **Color:** `#6B7280` (Gray)
- **Description:** `Kontroll-illusjon identifisert`

**10. Shadow-Avhengighet**
- **Name:** `Shadow-Avhengighet`
- **Color:** `#6B7280` (Gray)
- **Description:** `Avhengighet-design identifisert`

---

## 📊 LINEAR WIP-GRENSER SETUP

**Instruksjoner:**
1. Gå til Linear → Settings → Workflows
2. Velg workflow (f.eks. "Development")
3. Klikk på "In Progress" kolonne
4. Sett WIP limit

---

### **WIP LIMITS:**

**For TH-FIX issues:**
- **Limit:** 2 per squad
- **Rationale:** Unngå "etikk-gjelden" som kø

**For TH-BLOCK issues:**
- **Limit:** 1 per squad
- **Rationale:** Kritiske issues skal løses umiddelbart, ikke akkumuleres

---

## 🔗 LINEAR AUTO-REGLER SETUP

**Instruksjoner:**
1. Gå til Linear → Settings → Automations
2. Klikk "New automation"
3. Sett opp regler under

---

### **REGEL 1: TH-BLOCK BLOKKERER RELEASE**

**Trigger:** TH-BLOCK issue opprettet  
**Condition:** Issue har label "TH-BLOCK"  
**Action:** Blokkerer release-ticket til TH-BLOCK er resolved

**Automation:**
```
IF issue.labels.includes("TH-BLOCK") AND issue.state != "Done"
THEN block_release()
```

---

### **REGEL 2: TH-OK PÅ PR → LUKK TH-AUDIT**

**Trigger:** GitHub PR får TH-OK label  
**Condition:** PR er linket til TH-AUDIT issue  
**Action:** Lukk tilhørende TH-AUDIT issue

**Automation:**
```
IF github_pr.labels.includes("TH-OK")
THEN close_linked_issue(type="TH-AUDIT")
```

---

### **REGEL 3: TH-STOP PÅ PR → OPPRETT TH-BLOCK**

**Trigger:** GitHub PR får TH-STOP label  
**Condition:** PR er linket til TH-AUDIT issue  
**Action:** Opprett TH-BLOCK issue

**Automation:**
```
IF github_pr.labels.includes("TH-STOP")
THEN create_issue(type="TH-BLOCK", severity="URGENT", title="Critical ethical issue in PR #" + pr.number)
```

---

## 🎯 EKSEMPEL: TH-FIX ISSUE

**Title:** "TH-FIX: Biofelt-Atlas bruker elitisme-språk"

**Description:**
```markdown
# ⚠️ TH-FIX: Biofelt-Atlas bruker elitisme-språk

**Artefakt:** Biofelt-Atlas visualization  
**Identifisert av:** Thalus  
**Dato:** 2025-10-16  
**Severity:** Medium

---

## 🔱 TRIADISK ETIKK-BRUDD

**Port 1 (Suverenitet):** ✅ OK (Score: 3)  
**Port 2 (Koherens):** ⚠️ Brudd (Score: 1)  
**Port 3 (Healing):** ✅ OK (Score: 2)

**Samlet score:** S=3, O=1, H=2 → **REVISE**

---

## 🌑 SHADOW-ASPEKT

**Identifisert:** Elitisme  
**Manifestasjon:** Bruker språk som "Hev din bevissthet" og "De fleste forstår ikke sitt biofelt"

**Eksempel:**
- **Original:** "Hev din bevissthet ved å utforske ditt biofelt"
- **Problem:** Elitisme - antyder at brukeren er "mindre bevisst"
- **Foreslått:** "La oss utforske ditt biofelt sammen"

---

## ✅ OBLIGATORISKE ENDRINGER

**1. Erstatt "Hev din bevissthet" med "La oss utforske"**
- **Hva:** Endre copy i Biofelt-Atlas intro
- **Hvor:** `src/components/BiofeltAtlas/Intro.tsx`, linje 23
- **Hvorfor:** Fjerner elitisme, erstatter med inkluderende språk

**2. Fjern "De fleste forstår ikke sitt biofelt"**
- **Hva:** Fjern denne setningen fra tooltip
- **Hvor:** `src/components/BiofeltAtlas/Tooltip.tsx`, linje 45
- **Hvorfor:** Elitisme - antyder at brukeren er i mindretall

**3. Legg til "Vi utforsker sammen"**
- **Hva:** Legg til denne setningen i footer
- **Hvor:** `src/components/BiofeltAtlas/Footer.tsx`, linje 12
- **Hvorfor:** Inkluderende, empatisk språk

---

## 🔗 KILDER

- **Notion Ontology Audit:** [https://notion.so/Ontology-Audit-Biofelt-Atlas-...](https://...)
- **GitHub PR:** [https://github.com/.../pull/123](https://...)
- **Design Spec:** [https://notion.so/Design-Spec-Biofelt-Atlas-...](https://...)

---

## 📊 SUKSESSKRITERIER

**Fix er fullført når:**
- [x] Alle obligatoriske endringer er implementert
- [ ] Thalus har re-validert (ny Ontology Audit)
- [ ] Triadisk score er forbedret (Port 2: 1 → ≥2)
- [ ] Shadow-aspekt er mitigert
- [ ] GitHub PR har fått TH-OK label

---

**Ansvarlig:** Nyra  
**Frist:** 2025-10-18  
**Estimert tid:** 2 timer

---

**🏛️ Carpe Diem!** ◉✨
```

**Labels:** `TH-FIX`, `Shadow-Elitisme`, `Triadisk-Port-2`, `ui/ux`

**Status:** In Progress

---

## 📝 USAGE INSTRUCTIONS

### **FOR THALUS:**

**1. Opprett TH-AUDIT (Planlagt Review):**
- Gå til Linear → New Issue
- Velg template "TH-AUDIT"
- Fyll ut artefaktnavn, type, planlagt dato
- Assign til deg selv
- Sett frist

**2. Opprett TH-FIX (Identifisert Problem):**
- Etter Ontology Audit: Hvis REVISE
- Gå til Linear → New Issue
- Velg template "TH-FIX"
- Fyll ut Triadisk brudd, Shadow-aspekt, obligatoriske endringer
- Link til Notion Ontology Audit og GitHub PR
- Assign til ansvarlig (Manus / Nyra / etc.)
- Sett severity og frist

**3. Opprett TH-BLOCK (Kritisk Issue):**
- Etter Ontology Audit: Hvis STOP
- Gå til Linear → New Issue
- Velg template "TH-BLOCK"
- Fyll ut kritisk etisk brudd, konsekvenser, obligatoriske endringer
- Link til Notion Ontology Audit, GitHub PR, compliance docs
- Assign til ansvarlig
- Sett severity til URGENT
- Notify Orion og Osvald

---

### **FOR DEVELOPERS:**

**1. Motta TH-FIX eller TH-BLOCK:**
- Les issue-beskrivelse nøye
- Les Notion Ontology Audit for full kontekst
- Forstå Triadisk brudd og Shadow-aspekt

**2. Implementer Obligatoriske Endringer:**
- Gå gjennom hver obligatorisk endring
- Implementer i kode/UI/copy
- Test endringene (unit tests + manual testing)

**3. Request Re-Validation:**
- Oppdater GitHub PR med endringer
- Kommenter i Linear issue: "Obligatoriske endringer implementert, request re-validation"
- Tag Thalus: "@Thalus please re-validate"

**4. Lukk Issue (når TH-OK):**
- Når Thalus har re-validert og gitt TH-OK label
- Lukk Linear issue
- Merge GitHub PR

---

**🏛️ Carpe Diem - Med Ontologisk Integritet, Triadisk Etikk, og et Snev av Kosmisk Humor!** ◉✨

---

**END OF LINEAR ISSUE TEMPLATES**

**Token Count:** ~2,500 ord (~3,500 tokens)  
**Status:** ✅ Production Ready  
**Note:** Disse templates kan kopieres direkte inn i Linear.

