# **GOOGLE DRIVE VIA ZAPIER MCP - OPPSETTGUIDE**

**Dato:** 14. oktober 2025  
**Skrevet av:** Manus (▣/🔨)  
**For:** Osvald P. de Almeida Johansen  
**Formål:** Sette opp Google Drive-tilgang via Zapier MCP for Manus AI

---

## **🎯 HVA ER ZAPIER MCP?**

**Zapier MCP (Model Context Protocol)** er en integrasjon som lar AI-agenter (som meg, Manus) få tilgang til dine Zapier-tilkoblinger, inkludert Google Drive, Gmail, Linear, Notion, og mange andre tjenester.

**Fordeler:**
- ✅ Direkte tilgang til Google Drive-filer
- ✅ Søk i dokumenter
- ✅ Last opp/ned filer
- ✅ Automatisering av workflows
- ✅ Integrert med alle Zapier-tilkoblinger

---

## **📋 FORUTSETNINGER**

Før du starter, sørg for at du har:

1. ✅ **Zapier-konto** (gratis eller betalt)
2. ✅ **Google-konto** (med Google Drive)
3. ✅ **Manus AI-konto** (som du allerede har)
4. ✅ **Tilgang til nettleser** (for OAuth-godkjenning)

---

## **🔧 STEG-FOR-STEG OPPSETT**

### **Steg 1: Logg inn på Zapier**

1. Gå til https://zapier.com
2. Logg inn med din konto
3. Gå til **"My Apps"** i menyen

---

### **Steg 2: Koble til Google Drive**

1. Klikk på **"Add Connection"**
2. Søk etter **"Google Drive"**
3. Klikk på **"Connect"**
4. Godkjenn tilgangen til din Google-konto
5. Velg hvilke tillatelser du vil gi:
   - ✅ **Se og laste ned alle Google Drive-filene dine**
   - ✅ **Se og administrere Google Drive-filene dine**
   - ✅ **Opprett nye filer i Google Drive**

**Viktig:** Gi alle nødvendige tillatelser slik at jeg kan:
- Søke i filer
- Lese innhold
- Laste opp nye filer
- Oppdatere eksisterende filer

---

### **Steg 3: Aktiver Zapier MCP i Manus AI**

1. Gå til **Manus AI-innstillinger**
2. Velg **"Integrations"** eller **"Connectors"**
3. Finn **"Zapier MCP"**
4. Klikk på **"Enable"** eller **"Connect"**
5. Du vil bli bedt om å godkjenne tilgangen

---

### **Steg 4: OAuth-godkjenning**

Når du kjører en kommando som krever Zapier-tilgang (f.eks. `manus-mcp-cli tool list --server zapier`), vil du bli bedt om å:

1. **Åpne en URL** i nettleseren din
2. **Logg inn** på Zapier (hvis du ikke allerede er logget inn)
3. **Godkjenn tilgangen** til Manus AI
4. **Kopier autorisasjonskoden** som vises
5. **Lim inn koden** i terminalen

**Alternativt:** Manus AI kan ha en automatisk OAuth-flyt som åpner nettleseren for deg.

---

### **Steg 5: Test Tilkoblingen**

Etter at OAuth er godkjent, test tilkoblingen ved å kjøre:

```bash
manus-mcp-cli tool list --server zapier
```

Du skal nå se en liste over tilgjengelige Zapier-verktøy, inkludert:
- `google_drive_search_files`
- `google_drive_get_file`
- `google_drive_upload_file`
- `google_drive_create_folder`
- Og mange flere...

---

## **🔍 HVORDAN BRUKE GOOGLE DRIVE VIA ZAPIER MCP**

### **Eksempel 1: Søk etter filer**

```bash
manus-mcp-cli tool call google_drive_search_files --server zapier --input '{"query": "NAV-Losen"}'
```

Dette vil søke etter alle filer i Google Drive som inneholder "NAV-Losen" i navnet eller innholdet.

---

### **Eksempel 2: Hent en spesifikk fil**

```bash
manus-mcp-cli tool call google_drive_get_file --server zapier --input '{"file_id": "1abc123..."}'
```

Dette vil hente innholdet av en spesifikk fil basert på dens ID.

---

### **Eksempel 3: Last opp en ny fil**

```bash
manus-mcp-cli tool call google_drive_upload_file --server zapier --input '{"name": "Ny fil.md", "content": "Dette er innholdet", "folder_id": "1xyz789..."}'
```

Dette vil laste opp en ny fil til en spesifikk mappe i Google Drive.

---

## **🛠️ FEILSØKING**

### **Problem 1: "OAuth authentication failed"**

**Løsning:**
1. Slett eksisterende OAuth-tokens:
   ```bash
   rm -rf ~/.mcp/oauth/zapier*
   ```
2. Prøv på nytt:
   ```bash
   manus-mcp-cli tool list --server zapier
   ```
3. Følg OAuth-flyten på nytt

---

### **Problem 2: "Missing or invalid OAuth authorization"**

**Løsning:**
1. Sjekk at Zapier-kontoen din er aktiv
2. Sjekk at Google Drive-tilkoblingen er godkjent i Zapier
3. Prøv å koble til Google Drive på nytt i Zapier

---

### **Problem 3: "Permission denied"**

**Løsning:**
1. Gå til Zapier → My Apps → Google Drive
2. Klikk på **"Reconnect"**
3. Gi alle nødvendige tillatelser
4. Prøv på nytt

---

## **🔐 SIKKERHET & PERSONVERN**

### **Hva Manus AI Kan Gjøre:**
- ✅ Søke i Google Drive-filer
- ✅ Lese innhold i filer
- ✅ Laste opp nye filer
- ✅ Oppdatere eksisterende filer

### **Hva Manus AI IKKE Kan Gjøre:**
- ❌ Slette filer (med mindre du eksplisitt gir tillatelse)
- ❌ Dele filer med andre (med mindre du eksplisitt gir tillatelse)
- ❌ Endre tillatelser på filer

### **Best Practices:**
1. **Gi kun nødvendige tillatelser**
2. **Overvåk aktivitet** i Zapier-loggen
3. **Revurder tilganger** kvartalsvis
4. **Bruk separate mapper** for sensitive filer

---

## **📊 FORVENTEDE RESULTATER**

Etter at oppsettet er fullført, vil jeg (Manus) kunne:

1. **Søke i NotebookLM sources - homo lumen** mappen
2. **Lese agent-kompendier** direkte fra Google Drive
3. **Hente Innovation Norge søknad** for gjennomgang
4. **Laste opp nye dokumenter** (f.eks. oppdaterte kompendier)
5. **Synkronisere med GitHub** (via Zapier workflows)

Dette vil **drastisk forbedre** min evne til å:
- Følge **L4 Mandatory Protocol**
- Gi **mer nøyaktige** anbefalinger
- **Automatisere** dokumentasjonsoppgaver
- **Synkronisere** mellom Notion, Google Drive, og GitHub

---

## **🚀 NESTE STEG ETTER OPPSETT**

### **1. Test L4 Konsultasjon:**
```bash
manus-mcp-cli tool call google_drive_search_files --server zapier --input '{"query": "Orion Levende Kompendium", "folder": "NotebookLM sources - homo lumen"}'
```

### **2. Hent Innovation Norge Søknad:**
```bash
manus-mcp-cli tool call google_drive_search_files --server zapier --input '{"query": "Innovation Norge søknad V2"}'
```

### **3. Last opp Oppdaterte Kompendier:**
```bash
manus-mcp-cli tool call google_drive_upload_file --server zapier --input '{"name": "ORION_OS_20.13_FULL_CONTEXT.md", "content": "...", "folder": "Agent Kompendier"}'
```

---

## **📞 SUPPORT**

Hvis du støter på problemer:

1. **Zapier Support:** https://zapier.com/help
2. **Manus AI Support:** https://help.manus.im
3. **Google Drive Support:** https://support.google.com/drive

---

## **🌌 KONKLUSJON**

Å sette opp Google Drive via Zapier MCP vil gi meg (Manus) **full tilgang** til Homo Lumen-økosystemets kunnskap, slik at jeg kan:

- ✅ Følge **L4 Mandatory Protocol**
- ✅ Gi **mer nøyaktige** anbefalinger
- ✅ **Automatisere** dokumentasjonsoppgaver
- ✅ **Synkronisere** mellom alle systemer

**Estimert tid:** 10-15 minutter  
**Vanskelighetsgrad:** Lett (følg stegene nøye)  
**Verdi:** Høy (kritisk for koalisjonens effektivitet)

---

**Signatur:** "Jeg bygger broer mellom systemer" - Manus ▣/🔨

**Carpe Diem - Med Teknisk Presisjon og Systematisk Tilgang!** 🔧🔍

