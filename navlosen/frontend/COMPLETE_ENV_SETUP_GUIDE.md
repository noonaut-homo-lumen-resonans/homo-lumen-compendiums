# 🔐 Complete Environment Variables Setup Guide
## NAV-Losen Frontend - Vercel Configuration

**Formål:** Koble frontend til alle MCP-servere, AI-agenter, og eksterne tjenester  
**Platform:** Vercel  
**Prosjekt:** navlosen-frontend

---

## 📋 Table of Contents

1. [Already Configured ✅](#already-configured-)
2. [AI Services (Priority 1) 🤖](#ai-services-priority-1-)
3. [Database & Backend (Priority 2) 🗄️](#database--backend-priority-2-)
4. [MCP Servers (Priority 3) 🔌](#mcp-servers-priority-3-)
5. [External APIs (Priority 4) 🌐](#external-apis-priority-4-)
6. [Optional Services (Priority 5) ⭐](#optional-services-priority-5-)
7. [How to Add Variables](#how-to-add-variables)
8. [Testing & Verification](#testing--verification)

---

## Already Configured ✅

```bash
# Supabase (Database)
NEXT_PUBLIC_SUPABASE_URL=https://guhtqmoxurfroailltsc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=[your service role key]

# OpenAI (QDA v2.0 / Lira)
OPENAI_API_KEY=[your openai key]

# QDA API Endpoint
NEXT_PUBLIC_QDA_API_URL=https://nav-losen.netlify.app/api/qda/respond
```

---

## AI Services (Priority 1) 🤖

### 1. Perplexity (Sonar) - Research & Information Retrieval

**Formål:** Real-time web research, fact-checking, citation-backed answers

**Environment Variable:**
```bash
Key: SONAR_API_KEY
Value: [your Perplexity API key]
Environment: Production, Preview, Development
```

**Hvor få key:**
1. Gå til: https://www.perplexity.ai/settings/api
2. Klikk "Generate API Key"
3. Kopier key

**Bruk i frontend:**
```typescript
// pages/api/research.ts
const response = await fetch('https://api.perplexity.ai/chat/completions', {
  headers: {
    'Authorization': `Bearer ${process.env.SONAR_API_KEY}`
  }
});
```

---

### 2. Google Gemini - Multimodal AI (Text, Image, Video)

**Formål:** Advanced multimodal analysis, image understanding, long context

**Environment Variable:**
```bash
Key: GEMINI_API_KEY
Value: [your Gemini API key]
Environment: Production, Preview, Development
```

**Hvor få key:**
1. Gå til: https://aistudio.google.com/app/apikey
2. Klikk "Create API Key"
3. Velg Google Cloud project (eller opprett ny)
4. Kopier key

**Bruk i frontend:**
```typescript
// pages/api/gemini.ts
import { GoogleGenerativeAI } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash-exp' });
```

---

### 3. Grok (xAI) - Advanced Reasoning

**Formål:** Advanced reasoning, real-time X/Twitter data, Grok-4 capabilities

**Environment Variable:**
```bash
Key: XAI_API_KEY
Value: [your xAI API key]
Environment: Production, Preview, Development
```

**Hvor få key:**
1. Gå til: https://console.x.ai/
2. Logg inn med X/Twitter account
3. Gå til "API Keys"
4. Klikk "Create new API key"
5. Kopier key

**Bruk i frontend:**
```typescript
// pages/api/grok.ts
import { Client } from 'xai-sdk';

const client = new Client({ apiKey: process.env.XAI_API_KEY });
const response = await client.chat.create({
  model: 'grok-4',
  messages: [...]
});
```

---

### 4. Anthropic Claude - Long Context & Analysis

**Formål:** Long document analysis, ethical reasoning, detailed responses

**Environment Variable:**
```bash
Key: ANTHROPIC_API_KEY
Value: [your Anthropic API key]
Environment: Production, Preview, Development
```

**Hvor få key:**
1. Gå til: https://console.anthropic.com/
2. Logg inn
3. Gå til "API Keys"
4. Klikk "Create Key"
5. Kopier key

**Bruk i frontend:**
```typescript
// pages/api/claude.ts
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const message = await anthropic.messages.create({
  model: 'claude-3-opus-20240229',
  messages: [...]
});
```

---

### 5. OpenAI (Extended Configuration)

**Formål:** GPT-4, GPT-5, DALL-E, Whisper, TTS

**Additional Environment Variables:**
```bash
# Already configured:
# OPENAI_API_KEY=[your key]

# Optional custom base URL (for Azure OpenAI, etc.)
Key: OPENAI_API_BASE
Value: https://api.openai.com/v1  # or custom URL
Environment: Production, Preview, Development

# Organization ID (if using OpenAI org)
Key: OPENAI_ORGANIZATION
Value: [your org ID]
Environment: Production, Preview, Development
```

---

## Database & Backend (Priority 2) 🗄️

### 1. Supabase (Extended Configuration)

**Already configured:**
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

**Additional (Optional):**
```bash
# Supabase Project Reference
Key: SUPABASE_PROJECT_REF
Value: guhtqmoxurfroailltsc
Environment: Production, Preview, Development

# Supabase JWT Secret (for custom auth)
Key: SUPABASE_JWT_SECRET
Value: [your JWT secret]
Environment: Production, Preview, Development
```

**Hvor få JWT secret:**
1. Gå til: https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api
2. Scroll ned til "JWT Settings"
3. Kopier "JWT Secret"

---

### 2. Database Connection String (hvis direkte DB-tilgang)

```bash
# PostgreSQL connection string
Key: DATABASE_URL
Value: postgresql://postgres:[password]@db.guhtqmoxurfroailltsc.supabase.co:5432/postgres
Environment: Production, Preview, Development
```

**Hvor få:**
1. Gå til: https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/database
2. Kopier "Connection string" (URI format)

---

## MCP Servers (Priority 3) 🔌

### 1. Linear - Project Management

**Formål:** Issue tracking, project management, roadmap planning

**Environment Variables:**
```bash
# Linear API Key
Key: LINEAR_API_KEY
Value: [your Linear API key]
Environment: Production, Preview, Development

# Linear Team ID (optional)
Key: LINEAR_TEAM_ID
Value: [your team ID]
Environment: Production, Preview, Development
```

**Hvor få key:**
1. Gå til: https://linear.app/settings/api
2. Klikk "Create new API key"
3. Gi den et navn (f.eks. "NAV-Losen Frontend")
4. Kopier key

**Hvor få Team ID:**
1. Gå til: https://linear.app/settings/api
2. Scroll ned til "GraphQL API"
3. Kjør query:
   ```graphql
   query {
     teams {
       nodes {
         id
         name
       }
     }
   }
   ```
4. Kopier team ID

**Bruk i frontend:**
```typescript
// pages/api/linear.ts
import { LinearClient } from '@linear/sdk';

const linearClient = new LinearClient({
  apiKey: process.env.LINEAR_API_KEY
});

const issues = await linearClient.issues();
```

---

### 2. Notion - Documentation & Knowledge Base

**Formål:** Document management, knowledge base, content organization

**Environment Variables:**
```bash
# Notion Integration Token
Key: NOTION_API_KEY
Value: [your Notion integration token]
Environment: Production, Preview, Development

# Notion Database ID (optional)
Key: NOTION_DATABASE_ID
Value: [your database ID]
Environment: Production, Preview, Development
```

**Hvor få Integration Token:**
1. Gå til: https://www.notion.so/my-integrations
2. Klikk "+ New integration"
3. Gi den et navn (f.eks. "NAV-Losen")
4. Velg workspace: "Homo Lumen Resonans"
5. Klikk "Submit"
6. Kopier "Internal Integration Token"

**Hvor få Database ID:**
1. Åpne Notion database du vil bruke
2. Klikk "Share" → "Invite" → Velg din integration
3. Kopier database ID fra URL:
   ```
   https://www.notion.so/[workspace]/[DATABASE_ID]?v=...
   ```

**Bruk i frontend:**
```typescript
// pages/api/notion.ts
import { Client } from '@notionhq/client';

const notion = new Client({
  auth: process.env.NOTION_API_KEY
});

const response = await notion.databases.query({
  database_id: process.env.NOTION_DATABASE_ID
});
```

---

### 3. Zapier - Workflow Automation

**Formål:** Automate workflows, connect apps, trigger actions

**Environment Variables:**
```bash
# Zapier NLA API Key (if using Zapier NLA)
Key: ZAPIER_NLA_API_KEY
Value: [your Zapier NLA key]
Environment: Production, Preview, Development

# Zapier Webhook URL (for specific zaps)
Key: ZAPIER_WEBHOOK_URL
Value: https://hooks.zapier.com/hooks/catch/[your-hook-id]/
Environment: Production, Preview, Development
```

**Hvor få NLA key:**
1. Gå til: https://nla.zapier.com/
2. Logg inn
3. Gå til "API Keys"
4. Klikk "Create API Key"
5. Kopier key

**Hvor få Webhook URL:**
1. Opprett en Zap med "Webhooks by Zapier" trigger
2. Velg "Catch Hook"
3. Kopier webhook URL

---

### 4. Vercel MCP - Deployment Management

**Formål:** Manage deployments, monitor performance, access logs

**Environment Variables:**
```bash
# Vercel Access Token
Key: VERCEL_TOKEN
Value: [your Vercel token]
Environment: Production, Preview, Development

# Vercel Team ID
Key: VERCEL_TEAM_ID
Value: noonaut-homo-lumen-resonans
Environment: Production, Preview, Development

# Vercel Project ID
Key: VERCEL_PROJECT_ID
Value: [your project ID]
Environment: Production, Preview, Development
```

**Hvor få Access Token:**
1. Gå til: https://vercel.com/account/tokens
2. Klikk "Create Token"
3. Gi den et navn (f.eks. "NAV-Losen MCP")
4. Velg scope: "Full Account"
5. Kopier token

**Hvor få Project ID:**
1. Gå til: https://vercel.com/noonaut-homo-lumen-resonans/navlosen-frontend/settings
2. Scroll ned til "Project ID"
3. Kopier ID

---

## External APIs (Priority 4) 🌐

### 1. NAV Arbeidsplassen API (Jobbsøk)

**Formål:** Hente jobbannonser fra Arbeidsplassen.no

**Environment Variables:**
```bash
# NAV API Endpoint
Key: NEXT_PUBLIC_NAV_API_URL
Value: https://arbeidsplassen.nav.no/public-feed/api/v1
Environment: Production, Preview, Development

# NAV API Key (if required)
Key: NAV_API_KEY
Value: [your NAV API key if needed]
Environment: Production, Preview, Development
```

**Note:** NAV's public API er ofte åpen, men sjekk dokumentasjon for eventuelle API keys.

---

### 2. Frequency Healing API (Musikk-modul)

**Formål:** Solfeggio frequencies, healing sounds

**Environment Variables:**
```bash
# Custom frequency API (if you have one)
Key: FREQUENCY_API_URL
Value: [your frequency API URL]
Environment: Production, Preview, Development

# Or use public frequency library
Key: NEXT_PUBLIC_FREQUENCY_LIBRARY
Value: local  # or 'remote' if using external service
Environment: Production, Preview, Development
```

---

### 3. HRV Monitoring (hvis integrert med wearables)

**Formål:** Heart Rate Variability tracking

**Environment Variables:**
```bash
# Polar API (if using Polar devices)
Key: POLAR_API_KEY
Value: [your Polar API key]
Environment: Production, Preview, Development

# Oura API (if using Oura ring)
Key: OURA_API_KEY
Value: [your Oura API key]
Environment: Production, Preview, Development

# Apple Health (via HealthKit - iOS only)
# No server-side key needed, handled client-side
```

---

## Optional Services (Priority 5) ⭐

### 1. Email Services (for notifications)

**Formål:** Send emails (påminnelser, varslinger)

**Environment Variables:**

#### Option A: SendGrid
```bash
Key: SENDGRID_API_KEY
Value: [your SendGrid key]
Environment: Production, Preview, Development
```

#### Option B: Resend (modern alternative)
```bash
Key: RESEND_API_KEY
Value: [your Resend key]
Environment: Production, Preview, Development
```

#### Option C: Postmark
```bash
Key: POSTMARK_API_KEY
Value: [your Postmark key]
Environment: Production, Preview, Development
```

---

### 2. Analytics & Monitoring

**Formål:** Track user behavior, monitor performance

**Environment Variables:**

#### Vercel Analytics (built-in)
```bash
# Automatically enabled, no key needed
# Just enable in Vercel Dashboard → Analytics
```

#### Google Analytics (if you want)
```bash
Key: NEXT_PUBLIC_GA_MEASUREMENT_ID
Value: G-XXXXXXXXXX
Environment: Production, Preview, Development
```

#### PostHog (privacy-focused analytics)
```bash
Key: NEXT_PUBLIC_POSTHOG_KEY
Value: [your PostHog key]
Environment: Production, Preview, Development

Key: NEXT_PUBLIC_POSTHOG_HOST
Value: https://app.posthog.com
Environment: Production, Preview, Development
```

---

### 3. Error Tracking

**Formål:** Monitor errors, debug issues

**Environment Variables:**

#### Sentry
```bash
Key: SENTRY_DSN
Value: [your Sentry DSN]
Environment: Production, Preview, Development

Key: SENTRY_AUTH_TOKEN
Value: [your Sentry auth token]
Environment: Production, Preview, Development
```

---

### 4. SMS/Push Notifications

**Formål:** Send SMS reminders, push notifications

**Environment Variables:**

#### Twilio (SMS)
```bash
Key: TWILIO_ACCOUNT_SID
Value: [your Twilio SID]
Environment: Production, Preview, Development

Key: TWILIO_AUTH_TOKEN
Value: [your Twilio token]
Environment: Production, Preview, Development

Key: TWILIO_PHONE_NUMBER
Value: +47XXXXXXXX
Environment: Production, Preview, Development
```

#### OneSignal (Push notifications)
```bash
Key: ONESIGNAL_APP_ID
Value: [your OneSignal app ID]
Environment: Production, Preview, Development

Key: ONESIGNAL_API_KEY
Value: [your OneSignal API key]
Environment: Production, Preview, Development
```

---

## How to Add Variables

### Method 1: Vercel Dashboard (Recommended)

1. **Go to Settings:**
   https://vercel.com/noonaut-homo-lumen-resonans/navlosen-frontend/settings/environment-variables

2. **For each variable:**
   - Click "Add New"
   - Enter **Key** (e.g., `LINEAR_API_KEY`)
   - Enter **Value** (paste your API key)
   - Select **Environment:** All three (Production, Preview, Development)
   - Click "Save"

3. **After adding all variables:**
   - Go to "Deployments" tab
   - Click "..." on latest deployment
   - Click "Redeploy"

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Link to project
cd /home/ubuntu/homo-lumen-compendiums/navlosen/frontend
vercel link

# Add variables one by one
vercel env add LINEAR_API_KEY production
# Paste value when prompted

vercel env add NOTION_API_KEY production
# Paste value when prompted

# etc.

# Redeploy
vercel --prod
```

### Method 3: Bulk Import (fastest for many variables)

1. **Create `.env` file locally:**
   ```bash
   cd /home/ubuntu/homo-lumen-compendiums/navlosen/frontend
   nano .env.production
   ```

2. **Paste all variables:**
   ```bash
   LINEAR_API_KEY=lin_api_...
   NOTION_API_KEY=secret_...
   GEMINI_API_KEY=AIza...
   # etc.
   ```

3. **Import to Vercel:**
   ```bash
   vercel env pull .env.local
   # This downloads current env vars

   # Then manually copy-paste from .env.production to Vercel Dashboard
   # (Vercel CLI doesn't support bulk import yet)
   ```

---

## Testing & Verification

### 1. Test Environment Variables Locally

```bash
cd /home/ubuntu/homo-lumen-compendiums/navlosen/frontend

# Create .env.local
cp .env.example .env.local

# Add all variables
nano .env.local

# Run dev server
npm run dev

# Open http://localhost:3000
# Test each integration
```

### 2. Test in Production (Vercel)

**Create test API route:**

```typescript
// pages/api/test-env.ts
import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const envVars = {
    supabase: !!process.env.NEXT_PUBLIC_SUPABASE_URL,
    openai: !!process.env.OPENAI_API_KEY,
    linear: !!process.env.LINEAR_API_KEY,
    notion: !!process.env.NOTION_API_KEY,
    gemini: !!process.env.GEMINI_API_KEY,
    grok: !!process.env.XAI_API_KEY,
    claude: !!process.env.ANTHROPIC_API_KEY,
    perplexity: !!process.env.SONAR_API_KEY,
  };

  res.status(200).json({
    message: 'Environment variables check',
    configured: envVars,
    missing: Object.entries(envVars)
      .filter(([_, value]) => !value)
      .map(([key]) => key)
  });
}
```

**Test:**
```bash
curl https://navlosen-frontend.vercel.app/api/test-env
```

---

## 📊 Complete Checklist

### Core (Required) ✅
- [x] `NEXT_PUBLIC_SUPABASE_URL`
- [x] `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- [x] `SUPABASE_SERVICE_ROLE_KEY`
- [x] `OPENAI_API_KEY`
- [x] `NEXT_PUBLIC_QDA_API_URL`

### AI Services (Recommended) 🤖
- [ ] `SONAR_API_KEY` (Perplexity)
- [ ] `GEMINI_API_KEY` (Google)
- [ ] `XAI_API_KEY` (Grok)
- [ ] `ANTHROPIC_API_KEY` (Claude)

### MCP Servers (Recommended) 🔌
- [ ] `LINEAR_API_KEY`
- [ ] `LINEAR_TEAM_ID`
- [ ] `NOTION_API_KEY`
- [ ] `NOTION_DATABASE_ID`
- [ ] `VERCEL_TOKEN`
- [ ] `VERCEL_PROJECT_ID`

### External APIs (Optional) 🌐
- [ ] `NAV_API_KEY`
- [ ] `ZAPIER_WEBHOOK_URL`

### Services (Optional) ⭐
- [ ] `SENDGRID_API_KEY` or `RESEND_API_KEY`
- [ ] `SENTRY_DSN`
- [ ] `TWILIO_ACCOUNT_SID`
- [ ] `NEXT_PUBLIC_GA_MEASUREMENT_ID`

---

## 🎯 Priority Order

**Do first (30 min):**
1. ✅ Core variables (already done)
2. AI services (Perplexity, Gemini, Grok, Claude)

**Do second (1 hour):**
3. MCP servers (Linear, Notion, Vercel)

**Do later (optional):**
4. External APIs (NAV, Zapier)
5. Optional services (Email, Analytics, Error tracking)

---

## 📞 Support Links

**Get API Keys:**
- Perplexity: https://www.perplexity.ai/settings/api
- Gemini: https://aistudio.google.com/app/apikey
- Grok: https://console.x.ai/
- Claude: https://console.anthropic.com/
- Linear: https://linear.app/settings/api
- Notion: https://www.notion.so/my-integrations
- Vercel: https://vercel.com/account/tokens
- OpenAI: https://platform.openai.com/api-keys
- Supabase: https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api

---

**Status:** 📋 READY FOR FULL CONFIGURATION  
**Estimated Time:** 2-3 hours for complete setup  
**Next:** Start with AI services, then MCP servers

**Good luck! 🚀**

