# NOTION SCHEMA MIGRATION - SMK V2.0

**Dato:** 2025-10-29
**Versjon:** 2.0
**Formål:** Oppdatere SLL database + opprette Visual Essence Library for SMK V2.0

---

## DEL 1: SLL DATABASE - NYE PROPERTIES

### Steg 1: Åpne SLL Database

1. Gå til Notion
2. Finn **SLL (Shared Learning Library)** database
3. Klikk database tittel → **Edit database**

### Steg 2: Legg til 9 nye properties

#### Property 1: `temporal_weight_raw` (Number)

```
Type: Number
Name: temporal_weight_raw
Format: Number (2 decimals)
Default: Empty
Visibility: Hidden (toggle "Hide in views")
Description: "Raw temporal weight computed by script (0.0-1.0)"
```

**Hvordan:**
- Klikk **+ New property** (øverst høyre i database view)
- Velg **Number** type
- Navn: `temporal_weight_raw`
- Under "Format": Velg "Number" med 2 decimals
- Kryss av "Hide in views" (denne skal ikke vises i standard view)

---

#### Property 2: `temporal_weight` (Formula)

```
Type: Formula
Name: temporal_weight
Formula: if(prop("phase") == "published", prop("temporal_weight_raw"), 0)
Description: "Temporal weight (0.0-1.0) - only for published LPs"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Formula** type
- Navn: `temporal_weight`
- I formula editor, skriv:
  ```
  if(prop("phase") == "published", prop("temporal_weight_raw"), 0)
  ```
- Klikk **Done**

**Validering:** Formelen skal returnere tall mellom 0.0-1.0 for published LPs

---

#### Property 3: `half_life_days` (Number)

```
Type: Number
Name: half_life_days
Format: Number (0 decimals)
Default: 120
Description: "Domain-specific half-life in days (code=60, research=180, ethics=365)"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Number** type
- Navn: `half_life_days`
- Under "Options" → Set default value: `120`

---

#### Property 4: `last_cited_timestamp` (Date)

```
Type: Date
Name: last_cited_timestamp
Format: Date only (not date + time)
Default: Empty
Description: "Last time this LP was cited in SMK/ARF/CS"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Date** type
- Navn: `last_cited_timestamp`
- Under "Format": Velg "Date" (ikke "Date + time")

---

#### Property 5: `reactivation_count` (Number)

```
Type: Number
Name: reactivation_count
Format: Number (0 decimals)
Default: 0
Description: "Number of times this LP has been cited/reactivated"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Number** type
- Navn: `reactivation_count`
- Set default: `0`

---

#### Property 6: `freshness_status` (Select)

```
Type: Select
Name: freshness_status
Options:
  - fresh (color: green)
  - aging (color: yellow)
  - stale (color: gray)
Default: Empty
Description: "Computed freshness based on temporal_weight"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Select** type
- Navn: `freshness_status`
- Legg til 3 options:
  - `fresh` (velg grønn farge)
  - `aging` (velg gul farge)
  - `stale` (velg grå farge)

---

#### Property 7: `provenance_block` (Text)

```
Type: Text
Name: provenance_block
Format: Plain text (not rich text)
Default: Empty
Description: "JSON PROVENANCE block from source SMK file"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Text** type
- Navn: `provenance_block`

**Note:** Dette feltet vil inneholde JSON-data fra SMK PROVENANCE header

---

#### Property 8: `shadow_flags` (Checkbox)

```
Type: Checkbox
Name: shadow_flags
Default: Unchecked
Description: "Flagged during shadow audit (overgeneralization, apophenia, bias)"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Checkbox** type
- Navn: `shadow_flags`

---

#### Property 9: `shadow_notes` (Text)

```
Type: Text
Name: shadow_notes
Format: Rich text
Default: Empty
Description: "Link to ARF discussion or details about shadow concern"
```

**Hvordan:**
- Klikk **+ New property**
- Velg **Text** type
- Navn: `shadow_notes`
- Under "Format": Velg "Rich text" (for å kunne legge til Notion links)

---

### Steg 3: Verifiser alle 9 properties er lagt til

**Sjekkliste:**
- [ ] `temporal_weight_raw` (Number, hidden)
- [ ] `temporal_weight` (Formula)
- [ ] `half_life_days` (Number, default 120)
- [ ] `last_cited_timestamp` (Date)
- [ ] `reactivation_count` (Number, default 0)
- [ ] `freshness_status` (Select: fresh/aging/stale)
- [ ] `provenance_block` (Text)
- [ ] `shadow_flags` (Checkbox)
- [ ] `shadow_notes` (Text, rich)

**Validering:**
- Åpne en random LP page i databasen
- Scroll ned til properties
- Sjekk at alle 9 nye properties vises

---

## DEL 2: VISUAL ESSENCE LIBRARY - NY DATABASE

### Steg 1: Opprett ny database

1. Gå til Notion workspace root eller til `homo-lumen-compendiums` page
2. Klikk **+ New page**
3. Velg **Database** → **Table**
4. Navn databasen: **Visual Essence Library**
5. Endre icon: Velg 🎨 eller lignende visuell emoji

### Steg 2: Legg til properties

Notion oppretter automatisk en "Name" property. Rename denne til `ve_id`.

#### Property 1: `ve_id` (Title)

```
Type: Title (default)
Name: ve_id
Format: VE-NNN (e.g., VE-001, VE-047)
Description: "Unique Visual Essence ID"
```

**Hvordan:**
- Dette er default title property
- Rename fra "Name" til `ve_id`

---

#### Property 2: `name` (Text)

```
Type: Text
Name: name
Description: "Descriptive name for the visual essence"
Example: "Mycelial Network Bioluminescence"
```

---

#### Property 3: `description` (Text)

```
Type: Text
Name: description
Format: Rich text
Description: "Detailed description of visual metaphor and meaning"
```

---

#### Property 4: `image_media` (Files & media)

```
Type: Files & media
Name: image_media
Description: "Visual asset file (PNG, JPG, SVG, etc.)"
```

**Hvordan:**
- Velg **Files & media** type
- Agents kan dra-og-slippe bilder direkte her

---

#### Property 5: `palette` (Multi-select)

```
Type: Multi-select
Name: palette
Options:
  - warm
  - cool
  - earth
  - neon
  - monochrome
  - vibrant
Description: "Color palette(s) used in visual"
```

---

#### Property 6: `archetype_tags` (Multi-select)

```
Type: Multi-select
Name: archetype_tags
Options:
  - emergence
  - connection
  - transformation
  - flow
  - clarity
  - depth
  - cycles
  - resonance
Description: "Jung/Hillman archetypes or visual themes"
```

---

#### Property 7: `license` (Select)

```
Type: Select
Name: license
Options:
  - CC0 (Public Domain)
  - CC-BY (Attribution)
  - Internal Use
Default: Internal Use
Description: "Usage license for visual asset"
```

---

#### Property 8: `related_lps` (Relation)

```
Type: Relation
Name: related_lps
Related database: SLL (Shared Learning Library)
Description: "LPs illustrated by this visual essence"
```

**Hvordan:**
- Velg **Relation** type
- I "Select a database": Velg **SLL**
- Notion vil automatisk opprette reverse relation i SLL kalt "Visual Essence Library"

**VIKTIG:** Gå tilbake til SLL og rename den automatisk opprettede relationen fra "Visual Essence Library" til `illustrated_by`

---

#### Property 9: `created_by` (Person)

```
Type: Person
Name: created_by
Description: "Agent who created/curated this visual"
```

---

#### Property 10: `created_at` (Date)

```
Type: Date
Name: created_at
Format: Date
Description: "When this visual essence was added"
```

---

### Steg 3: Verifiser Visual Essence Library

**Sjekkliste:**
- [ ] Database navn: "Visual Essence Library"
- [ ] Icon: 🎨 eller lignende
- [ ] 10 properties opprettet
- [ ] Relation til SLL fungerer (test ved å legge til dummy entry)

---

## DEL 3: SLL RELATION UPDATE

### Steg 1: Rename auto-created relation i SLL

1. Åpne **SLL** database
2. Finn property som heter "Visual Essence Library" (auto-created fra relationen)
3. Klikk property navn → **Edit property**
4. Rename til: `illustrated_by`
5. Beskrivelse: "Visual essence that illustrates this LP"

---

## DEL 4: VALIDERING

### Test 1: Opprett dummy VE entry

1. Åpne Visual Essence Library
2. Klikk **+ New**
3. Fyll inn:
   - `ve_id`: VE-TEST-001
   - `name`: Test Visual
   - `description`: Test description
   - `palette`: warm
   - `archetype_tags`: emergence
   - `license`: Internal Use
4. Save

### Test 2: Link VE to LP

1. Åpne en LP i SLL database
2. Find `illustrated_by` property
3. Klikk feltet → velg "VE-TEST-001"
4. Verifiser at linken fungerer (klikk på VE entry og sjekk at den åpner)

### Test 3: Reverse relation

1. Åpne VE-TEST-001 i Visual Essence Library
2. Sjekk `related_lps` property
3. Verifiser at LP-en du linket vises her automatisk

**Hvis alle 3 tester passer:** ✅ Schema migration komplett!

---

## DEL 5: MIGRATION SCRIPT (OPTIONAL)

Hvis du vil automatisere dette med Notion API, bruk scriptet:
`scripts/notion_schema_migration_v2.py`

Kjør med:
```bash
export NOTION_TOKEN="secret_..."
export SLL_DATABASE_ID="..."

python scripts/notion_schema_migration_v2.py \
  --notion-token $NOTION_TOKEN \
  --sll-database-id $SLL_DATABASE_ID \
  --create-ve-database
```

---

## TIMELINE ESTIMATION

**Manual GUI oppdatering:**
- SLL properties (9 stk): 15-20 min
- VE database creation: 10-15 min
- Testing & validation: 5-10 min
- **Total: 30-45 minutter**

**API script oppdatering:**
- Initial setup: 10 min
- Script run: 2-5 min
- Validation: 5 min
- **Total: 15-20 minutter**

---

## TROUBLESHOOTING

### Problem: Formula ikke working
**Løsning:** Sjekk at property names matcher eksakt (case-sensitive):
- `phase` må eksistere som property i SLL
- `temporal_weight_raw` må eksistere

### Problem: Relation ikke synlig i SLL
**Løsning:**
- Refresh Notion page
- Sjekk at relationen ble opprettet i begge retninger
- Notion trenger noen ganger 10-30 sekunder til å synkronisere relations

### Problem: Image upload ikke fungerer i VE
**Løsning:**
- Sjekk filstørrelse (< 5 MB for Notion free tier)
- Sjekk filformat (PNG, JPG, SVG støttet)
- Prøv å laste opp via drag-and-drop direkte på page

---

**Status:** Ready for manual execution
**Estimert tid:** 30-45 minutter
**Neste steg:** Week 1 Day 3-4 (SMK Template creation)
