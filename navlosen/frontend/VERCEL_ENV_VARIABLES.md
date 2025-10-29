# Vercel Environment Variables - Complete Setup

**Project:** navlosen-frontend  
**Platform:** Vercel  
**Purpose:** Connect frontend to MCP servers and AI agents

---

## 📋 Current Environment Variables

### Already Configured ✅

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://guhtqmoxurfroailltsc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1aHRxbW94dXJmcm9haWxsdHNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwNDQzMjIsImV4cCI6MjA3NjYyMDMyMn0.0W2H_BaS8wRYz5DS8FwrCbvILB7cB5QyZi40oO7VDRk
```

---

## 🔧 MCP Servers - Environment Variables Needed

### 1. Zapier MCP
**Purpose:** Business process automation, workflow integration

```bash
# Zapier credentials (if needed)
ZAPIER_API_KEY=<your_zapier_api_key>
ZAPIER_WEBHOOK_URL=<your_zapier_webhook_url>
```

**Note:** Zapier MCP is typically configured via OAuth during setup. Check if you need API keys.

---

### 2. Supabase MCP
**Purpose:** Database management, real-time data

```bash
# Already configured ✅
NEXT_PUBLIC_SUPABASE_URL=https://guhtqmoxurfroailltsc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1aHRxbW94dXJmcm9haWxsdHNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwNDQzMjIsImV4cCI6MjA3NjYyMDMyMn0.0W2H_BaS8wRYz5DS8FwrCbvILB7cB5QyZi40oO7VDRk

# Service role key (for server-side operations)
SUPABASE_SERVICE_ROLE_KEY=<your_service_role_key>
```

**Where to find:**
1. Go to https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api
2. Copy "service_role" key (secret)

---

### 3. Linear MCP
**Purpose:** Project management, issue tracking

```bash
# Linear API key
LINEAR_API_KEY=<your_linear_api_key>
LINEAR_TEAM_ID=<your_team_id>
```

**Where to find:**
1. Go to https://linear.app/settings/api
2. Create new API key
3. Copy key

---

### 4. Notion MCP
**Purpose:** Document management, knowledge base

```bash
# Notion integration token
NOTION_API_KEY=<your_notion_integration_token>
NOTION_DATABASE_ID=<your_database_id>
```

**Where to find:**
1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy "Internal Integration Token"

---

### 5. Vercel MCP
**Purpose:** Deployment management

```bash
# Vercel token (for API access)
VERCEL_TOKEN=<your_vercel_token>
VERCEL_TEAM_ID=noonaut-homo-lumen-resonans
```

**Where to find:**
1. Go to https://vercel.com/account/tokens
2. Create new token
3. Copy token

---

## 🤖 AI Agents - API Endpoints

### QDA v2.0 (Lira's Brain)
**Purpose:** 6-layer neuroarchitecture for empathetic responses

```bash
# QDA API endpoint
NEXT_PUBLIC_QDA_API_URL=https://nav-losen.netlify.app/api/qda/respond

# OpenAI API (for QDA layers)
OPENAI_API_KEY=<your_openai_api_key>
OPENAI_API_BASE=<optional_custom_base_url>
```

**Where to find OpenAI key:**
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy key

---

### Lira (Empathetic AI Assistant)
**Purpose:** Main chatbot interface

```bash
# Lira API endpoint (if separate from QDA)
NEXT_PUBLIC_LIRA_API_URL=https://nav-losen.netlify.app/api/lira/chat

# Lira configuration
LIRA_MODEL=gpt-4
LIRA_MAX_TOKENS=2000
LIRA_TEMPERATURE=0.7
```

---

### Other AI Services (Optional)

```bash
# Perplexity (for research)
SONAR_API_KEY=<your_perplexity_api_key>

# Google Gemini (for multimodal)
GEMINI_API_KEY=<your_gemini_api_key>

# Grok (xAI)
XAI_API_KEY=<your_xai_api_key>

# Anthropic Claude
ANTHROPIC_API_KEY=<your_anthropic_api_key>
```

---

## 📝 How to Add Environment Variables to Vercel

### Method 1: Via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard:**
   https://vercel.com/noonaut-homo-lumen-resonans/navlosen-frontend/settings/environment-variables

2. **Add each variable:**
   - Click "Add New"
   - Enter **Key** (e.g., `LINEAR_API_KEY`)
   - Enter **Value** (e.g., your actual API key)
   - Select **Environment:** Production, Preview, Development (select all)
   - Click "Save"

3. **Redeploy:**
   - Go to "Deployments" tab
   - Click "..." on latest deployment
   - Click "Redeploy"

### Method 2: Via Vercel CLI

```bash
# Install Vercel CLI (if not installed)
npm install -g vercel

# Login
vercel login

# Link to project
cd /home/ubuntu/homo-lumen-compendiums/navlosen/frontend
vercel link

# Add environment variables
vercel env add LINEAR_API_KEY
# Paste your key when prompted

# Repeat for each variable
vercel env add NOTION_API_KEY
vercel env add OPENAI_API_KEY
# etc.

# Redeploy
vercel --prod
```

---

## 🔐 Security Best Practices

### Public vs Private Variables

**Public (NEXT_PUBLIC_*):**
- Exposed to browser
- Safe for client-side code
- Examples: Supabase URL, API endpoints

**Private (no prefix):**
- Server-side only
- Never exposed to browser
- Examples: API keys, service role keys

### Which Variables Should Be Public?

```bash
# ✅ Public (safe for browser)
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_QDA_API_URL
NEXT_PUBLIC_LIRA_API_URL

# ❌ Private (server-side only)
SUPABASE_SERVICE_ROLE_KEY
OPENAI_API_KEY
LINEAR_API_KEY
NOTION_API_KEY
ZAPIER_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
```

---

## 🧪 Testing Environment Variables

### In Local Development

1. **Create `.env.local` file:**
   ```bash
   cd /home/ubuntu/homo-lumen-compendiums/navlosen/frontend
   nano .env.local
   ```

2. **Add all variables:**
   ```bash
   # Copy all variables from above
   NEXT_PUBLIC_SUPABASE_URL=...
   SUPABASE_SERVICE_ROLE_KEY=...
   # etc.
   ```

3. **Test locally:**
   ```bash
   npm run dev
   # Open http://localhost:3000
   ```

### In Production (Vercel)

1. **Check if variables are loaded:**
   - Create test API route: `/api/test-env`
   - Return `process.env.VARIABLE_NAME` (for private vars)
   - Check browser console (for public vars)

2. **Debug:**
   - Go to Vercel Dashboard → Deployments → Latest → Function Logs
   - Check for errors related to missing env vars

---

## 📊 Complete Environment Variables Checklist

### Core (Required)
- [x] `NEXT_PUBLIC_SUPABASE_URL`
- [x] `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- [ ] `SUPABASE_SERVICE_ROLE_KEY`
- [ ] `NEXT_PUBLIC_QDA_API_URL`
- [ ] `OPENAI_API_KEY`

### MCP Servers (Optional but Recommended)
- [ ] `LINEAR_API_KEY`
- [ ] `LINEAR_TEAM_ID`
- [ ] `NOTION_API_KEY`
- [ ] `NOTION_DATABASE_ID`
- [ ] `ZAPIER_API_KEY`
- [ ] `VERCEL_TOKEN`

### AI Services (Optional)
- [ ] `SONAR_API_KEY` (Perplexity)
- [ ] `GEMINI_API_KEY` (Google)
- [ ] `XAI_API_KEY` (Grok)
- [ ] `ANTHROPIC_API_KEY` (Claude)

---

## 🚀 Next Steps

1. **Gather all API keys** from respective platforms
2. **Add to Vercel Dashboard** (Method 1 above)
3. **Redeploy** Vercel project
4. **Test** that all integrations work
5. **Document** which keys are active

---

## 📞 Need Help?

**Where to get API keys:**
- Supabase: https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api
- Linear: https://linear.app/settings/api
- Notion: https://www.notion.so/my-integrations
- OpenAI: https://platform.openai.com/api-keys
- Vercel: https://vercel.com/account/tokens

**Questions?**
- Ask Manus for deployment help
- Ask Lira for MCP configuration
- Ask Osvald for credentials

---

**Status:** 📋 READY FOR CONFIGURATION  
**Next:** Gather API keys and add to Vercel Dashboard

