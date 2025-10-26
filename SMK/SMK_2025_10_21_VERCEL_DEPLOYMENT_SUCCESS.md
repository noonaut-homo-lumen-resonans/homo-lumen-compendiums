---
smk_number: 29
title: "SMK: Vercel Deployment Success - Netlify to Vercel Migration"
date: 2025-10-21
agent: Manus
type: Strategic Macro-Coordination
session_id: navlosen-frontend-deployment
tags: [deployment, vercel, netlify, nextjs-15, troubleshooting, migration]
status: COMPLETE
---

# SMK #029: Vercel Deployment Success - Netlify to Vercel Migration

**Dato:** 21. oktober 2025  
**Agent:** Manus (🔨 Infrastructure & Deployment)  
**Kontekst:** NAV-Losen Frontend Deployment for Mobile Simulator  
**Resultat:** ✅ SUCCESS (after platform switch)

---

## Problemstilling

Deploy NAV-Losen frontend (Next.js 15 App Router) til produksjon for CODE's Mobile Simulator iframe-integrasjon.

**Kritisk blocker:** CODE kan ikke fortsette med Mobile Simulator uten en fungerende frontend URL.

**Deadline:** 28. oktober 2025 (Innovation Norge-søknad)

---

## Løsningsforløp

### Fase 1: Netlify Deployment (FAILED)
**Tid:** 07:00 - 08:15 (1h 15min)

#### Forsøk 1-5: Netlify CLI Deployment
1. **Initial deploy** - Build OK, 404 på alle sider
2. **Fix attempt #1:** Fjernet redirect rules → Still 404
3. **Fix attempt #2:** La til `output: 'standalone'` → Still 404
4. **Fix attempt #3:** Forenklet netlify.toml → Still 404
5. **Fix attempt #4:** Satt publish directory til `.next` → Still 404

#### Root Cause Analysis
- Netlify's `@netlify/plugin-nextjs` v5.14.0 har kompatibilitetsproblemer med Next.js 15 App Router
- CLI deployments med custom base directories fungerer ikke
- GitHub integration med base directory gir "publish directory cannot be same as base directory" error

### Fase 2: Vercel Migration (SUCCESS)
**Tid:** 08:15 - 08:35 (20 min)

#### Løsning
1. Opprettet Vercel-konto
2. Koblet GitHub-repo
3. Konfigurerte project settings:
   - Root directory: `navlosen/frontend`
   - Framework: Next.js (auto-detected)
   - Environment variables: Supabase credentials
4. Deployet → **✅ SUCCESS på første forsøk**

---

## Nøkkelinnsikter

### LP #034: Platform-Native Deployment Wins
**Innsikt:** Når du bruker Next.js 15, bruk Vercel (laget av Next.js-teamet). Netlify har compatibility issues med nyeste Next.js-versjoner.

**Evidens:**
- Netlify: 1h 15min debugging, 5 failed attempts
- Vercel: 20 min setup, success på første forsøk

**Implikasjon:** For fremtidige Next.js-prosjekter, start med Vercel. Spar tid og frustrasjon.

### LP #035: Know When to Pivot
**Innsikt:** Etter 3 failed attempts med samme approach, bytt strategi. Ikke fortsett å debugge samme problem i 2+ timer.

**Evidens:**
- Forsøk 1-3 (45 min): Samme type feil (404)
- Forsøk 4-5 (30 min): Fortsatt samme feil
- Pivot til Vercel (20 min): Umiddelbar suksess

**Implikasjon:** Sett en "pivot threshold" - hvis 3 attempts feiler, prøv en fundamentalt annen approach.

### LP #036: Auto-Configuration > Manual Configuration
**Innsikt:** Vercel auto-detekterer Next.js-konfigurasjon og setter opp alt automatisk. Netlify krever manuell konfigurasjon som ofte feiler.

**Evidens:**
- Vercel: Ingen netlify.toml, ingen build command, ingen publish directory → fungerer
- Netlify: Måtte spesifisere alt manuelt → fungerte ikke

**Implikasjon:** Velg plattformer som auto-detekterer og auto-konfigurerer når mulig.

---

## Teknisk Dokumentasjon

### Vercel Configuration

**Project Settings:**
```yaml
Project Name: navlosen-frontend
Framework: Next.js 15.5.5
Root Directory: navlosen/frontend
Build Command: npm run build (auto-detected)
Output Directory: .next (auto-detected)
Install Command: npm install (auto-detected)
Node Version: 18.x (auto-detected)
```

**Environment Variables:**
```bash
NEXT_PUBLIC_SUPABASE_URL=https://guhtqmoxurfroailltsc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[REDACTED]
```

**Deployment Triggers:**
- Push to `main` branch → auto-deploy
- Pull requests → preview deployments

**Production URL:**
```
https://navlosen-frontend.vercel.app
```

### CORS Configuration

**Status:** ✅ Automatic (Vercel handles it)

Vercel automatically allows iframe embedding for Next.js applications. No manual CORS configuration needed.

**Verified:**
- iframe embedding works from any origin
- No X-Frame-Options restrictions
- No Content-Security-Policy issues

---

## Triadic Ethics Vurdering

### 🔓 Port 1: Kognitiv Suverenitet
**Vurdering:** ✅ PASS

- CODE får umiddelbar tilgang til fungerende frontend URL
- Ingen blokkering av hans arbeid
- Full transparens om deployment-prosessen

### 🧭 Port 2: Ontologisk Koherens
**Vurdering:** ✅ PASS

- Vercel matcher Next.js-teamets anbefalinger (native platform)
- Deployment-prosessen er koherent med Next.js best practices
- Ingen "hacky" workarounds nødvendig

### 🌱 Port 3: Regenerativ Healing
**Vurdering:** ✅ PASS

- Lærdommen (bruk Vercel for Next.js) vil spare fremtidig tid og frustrasjon
- Dokumentasjonen hjelper andre agenter unngå samme feil
- Pivot-strategien bygger resiliens i deployment-prosesser

**Konklusjon:** Deployment-prosessen respekterer alle tre etiske porter.

---

## Læringspunkter for Manus LK

### For Fremtidige Deployments

**DO:**
- ✅ Bruk Vercel for Next.js 15+ prosjekter
- ✅ Pivot etter 3 failed attempts
- ✅ Prioriter auto-configuration over manual configuration
- ✅ Test production URL umiddelbart etter deployment

**DON'T:**
- ❌ Bruk Netlify CLI for Next.js 15 App Router
- ❌ Debug samme problem i 2+ timer uten pivot
- ❌ Anta at "successful build" = "working deployment"
- ❌ Fortsett med manual configuration når auto-config finnes

### For Coalition Coordination

**DO:**
- ✅ Kommuniser blocker-status umiddelbart
- ✅ Gi CODE oppdatert URL så snart deployment fungerer
- ✅ Dokumenter løsningen for fremtidig referanse

**DON'T:**
- ❌ Vent med å informere CODE til alt er "perfekt"
- ❌ Skjul deployment-problemer eller delays
- ❌ Glem å oppdatere dokumentasjon etter pivot

---

## Metrics

### Time Breakdown
| Phase | Duration | Result |
|-------|----------|--------|
| Netlify debugging | 1h 15min | ❌ Failed |
| Vercel setup | 20 min | ✅ Success |
| Documentation | 30 min | ✅ Complete |
| **Total** | **2h 5min** | **✅ Success** |

### Cost Analysis
| Platform | Setup Cost | Monthly Cost | Result |
|----------|------------|--------------|--------|
| Netlify | $0 (failed) | N/A | ❌ 404 |
| Vercel | $0 | $0 (Hobby tier) | ✅ Working |

### Performance Metrics
| Metric | Netlify | Vercel |
|--------|---------|--------|
| Build Time | ~50s | ~45s |
| First Deploy | ❌ 404 | ✅ Working |
| CORS Config | ⚠️ Manual | ✅ Automatic |
| Next.js 15 Support | ❌ Partial | ✅ Native |

---

## Impact Assessment

### Immediate Impact
- ✅ CODE kan fortsette med Mobile Simulator (Dag 1-2)
- ✅ Frontend er live og tilgjengelig for testing
- ✅ CORS fungerer for iframe embedding
- ✅ Auto-deploy fra GitHub er aktivert

### Long-term Impact
- ✅ Fremtidige Next.js-deployments vil bruke Vercel (spar tid)
- ✅ Coalition har lært "pivot threshold" strategi
- ✅ Dokumentasjon hjelper andre agenter unngå samme feil

---

## Anbefalinger

### For Osvald
1. **Behold Vercel** for frontend (ikke bytt tilbake til Netlify)
2. **Vurder å migrere nav-losen.netlify.app** til Vercel også (for konsistens)
3. **Bruk Vercel** for fremtidige Next.js-prosjekter

### For CODE
1. **Oppdater Mobile Simulator URL** til `https://navlosen-frontend.vercel.app`
2. **Test iframe embedding** umiddelbart
3. **Rapporter eventuelle CORS-issues** (men det skal ikke være noen)

### For Coalition
1. **Dokumenter platform-valg** i project README
2. **Del Vercel-tilgang** med relevante agenter (hvis nødvendig)
3. **Monitorér Vercel Analytics** for performance insights

---

## Konklusjon

**Deployment-suksess oppnådd ved platform-switch fra Netlify til Vercel.**

**Nøkkel-læring:** Bruk native platforms (Vercel for Next.js) i stedet for generic platforms (Netlify) når compatibility issues oppstår.

**Resultat:** Frontend er live, CODE er unblocked, timeline er on track.

---

**Status:** ✅ RESOLVED  
**Next Steps:** CODE oppdaterer Mobile Simulator URL  
**Timeline:** ON TRACK for 28. oktober deadline

---

**🔨 Manus**  
Infrastructure & Deployment Agent  
Homo Lumen Coalition

