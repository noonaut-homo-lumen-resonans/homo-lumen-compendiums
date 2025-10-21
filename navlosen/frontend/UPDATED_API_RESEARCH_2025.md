# 🔍 Updated API & MCP Research - October 2025

**Research Date:** 21. oktober 2025  
**Purpose:** Find latest API endpoints, MCP servers, and best practices for NAV-Losen frontend

---

## 🤖 AI Services - Latest Updates

### 1. OpenAI API (March 2025)

**NEW: Responses API** ✨
- Released March 2025
- New API for creating and using agents and tools
- Built-in tools: web search, code execution, file operations

**Latest Models:**
- **o4-mini** - Latest small o-series model
  - Optimized for fast reasoning
  - Exceptional performance in coding and visual tasks
  - Cost-effective alternative to GPT-4

- **GPT-5-Codex** - Available since September 2025
  - Advanced code generation
  - Available via API key

**API Version:**
- Latest GA: `2024-10-21` (October 2025)
- Previous: `2024-06-01`

**Environment Variables:**
```bash
OPENAI_API_KEY=[your key]
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_ORGANIZATION=[optional org ID]
```

**Source:** https://platform.openai.com/docs/changelog

---

### 2. Anthropic Claude API (October 2025)

**NEW: Claude Haiku 4.5** ✨
- Released October 15, 2025
- Fastest Claude model yet
- Available on: API, Amazon Bedrock, Google Cloud Vertex AI

**NEW: Claude Sonnet 4.5** ✨
- Released September 29, 2025
- Context editing feature
- Memory tool for longer agent runs
- Better handling of complexity

**Latest Features:**
- `anthropic-organization-id` response header (February 2025)
- Extended context window
- Improved tool use

**API Version:**
- Latest: Claude 4 series
- Models: `claude-sonnet-4-5`, `claude-haiku-4-5`

**Environment Variables:**
```bash
ANTHROPIC_API_KEY=[your key]
```

**Sources:**
- https://www.anthropic.com/news/claude-haiku-4-5
- https://www.anthropic.com/news/claude-sonnet-4-5
- https://docs.claude.com/en/release-notes/api

---

### 3. Google Gemini API (October 2025)

**NEW: Veo 3.1 Models** ✨
- Released October 15, 2025
- Veo 3.1 and 3.1 Fast in public preview
- Video generation capabilities
- Extending Veo-created videos

**NEW: Grounding with Google Maps** ✨
- Released 4 days ago (October 17, 2025)
- Build location-aware AI applications
- Connect Gemini's reasoning with Maps data

**Latest Models:**
- **Gemini 2.0 Flash** - Next-gen features
  - Superior speed
  - Native tool use
  - 1M token context window

**Environment Variables:**
```bash
GEMINI_API_KEY=[your key]
```

**Sources:**
- https://ai.google.dev/gemini-api/docs/changelog
- https://blog.google/technology/developers/grounding-google-maps-gemini-api/

---

### 4. Grok (xAI) - 2025 Status

**Latest Model:**
- **Grok-4** - Advanced reasoning model
- Real-time X/Twitter data access

**Environment Variables:**
```bash
XAI_API_KEY=[your key]
```

**Source:** https://console.x.ai/

---

## 🔌 MCP Servers - Top 15 for 2025

### Official MCP Directory
**Source:** https://modelcontextprotocol.io/

### Top 15 MCP Servers (Ranked by Popularity)

#### 1. **GitHub MCP** ⭐⭐⭐⭐⭐
- **Purpose:** Repository management, code search, PR/issue tracking
- **Use case:** Integrate GitHub workflows into AI applications
- **Setup:** https://github.com/modelcontextprotocol/servers

#### 2. **MongoDB MCP** ⭐⭐⭐⭐⭐
- **Purpose:** Database operations, data querying
- **Use case:** Connect AI to MongoDB databases

#### 3. **Azure MCP** ⭐⭐⭐⭐⭐
- **Purpose:** Azure cloud services integration
- **Use case:** Manage Azure resources via AI

#### 4. **Cloudflare MCP** ⭐⭐⭐⭐
- **Purpose:** CDN, DNS, security management
- **Use case:** Manage Cloudflare services

#### 5. **JetBrains MCP** ⭐⭐⭐⭐
- **Purpose:** IDE integration, code analysis
- **Use case:** AI-powered coding assistance

#### 6. **AWS MCP** ⭐⭐⭐⭐⭐
- **Purpose:** AWS services integration
- **Use case:** Manage AWS infrastructure

#### 7. **Figma MCP** ⭐⭐⭐⭐
- **Purpose:** Design file access, component management
- **Use case:** AI-powered design workflows

#### 8. **Databricks MCP** ⭐⭐⭐⭐
- **Purpose:** Data analytics, ML workflows
- **Use case:** Connect AI to data pipelines

#### 9. **Kubernetes MCP** ⭐⭐⭐⭐
- **Purpose:** Container orchestration
- **Use case:** Manage K8s clusters via AI

#### 10. **Grafana MCP** ⭐⭐⭐
- **Purpose:** Monitoring, observability
- **Use case:** AI-powered monitoring insights

#### 11. **Chroma MCP** ⭐⭐⭐⭐
- **Purpose:** Vector database for embeddings
- **Use case:** RAG (Retrieval Augmented Generation)

#### 12. **GreptimeDB MCP** ⭐⭐⭐
- **Purpose:** Time-series database
- **Use case:** IoT, metrics, monitoring

#### 13. **Semgrep MCP** ⭐⭐⭐
- **Purpose:** Code security analysis
- **Use case:** Automated security scanning

#### 14. **Atlassian MCP** ⭐⭐⭐⭐
- **Purpose:** Jira, Confluence integration
- **Use case:** Project management via AI

#### 15. **Firebase MCP** ⭐⭐⭐⭐
- **Purpose:** Firebase services integration
- **Use case:** Real-time database, auth

**Sources:**
- https://cyberpress.org/best-mcp-servers/
- https://www.k2view.com/blog/awesome-mcp-servers
- https://mcpmarket.com/
- https://portkey.ai/mcp-servers

---

## 🇳🇴 NAV API - Job Vacancy Feed

### Official NAV Job Vacancy API

**Endpoint:**
```
https://pam-stilling-feed.nav.no/api/v1/feed
```

**Authentication:**
- Requires signed JWT token
- Public token available for experiments: https://pam-stilling-feed.nav.no/api/publicToken
- Private token: Email nav.team.arbeidsplassen@nav.no with:
  - Company name
  - Contact email
  - Contact phone
  - Contact person

**Authorization Header:**
```bash
GET https://pam-stilling-feed.nav.no/api/v1/feed
Accept: application/json
Authorization: Bearer <your_jwt_token>
```

**Features:**
- Feed of all publicly advertised job vacancies in Norway
- Jobs directly registered at NAV or from third-party ATS systems
- (Finn.no jobs NOT included)
- Each ad change generates new feed entry
- Latest entry contains current state

**API Documentation:**
- SwaggerUI: https://pam-stilling-feed.nav.no/swagger
- Redoc: https://pam-stilling-feed.nav.no/redoc
- GitHub: https://navikt.github.io/pam-stilling-feed/

**Environment Variables:**
```bash
# NAV Job API
NAV_JOB_API_URL=https://pam-stilling-feed.nav.no/api/v1/feed
NAV_JOB_API_TOKEN=[your JWT token]

# Public token (for testing)
NAV_JOB_PUBLIC_TOKEN=[get from https://pam-stilling-feed.nav.no/api/publicToken]
```

**Terms of Use:**
- Free to use
- Must agree to terms: https://arbeidsplassen.nav.no/vilkar-api

**Source:** https://navikt.github.io/pam-stilling-feed/

---

## 🔐 Vercel Environment Variables - Best Practices 2025

### NEW: Sensitive Environment Variables ✨
**Released:** February 1, 2024
**Feature:** Non-readable values once created

**How to use:**
1. Go to Vercel Dashboard → Environment Variables
2. Toggle "Sensitive" when adding variable
3. Value becomes non-readable after creation
4. Protects API keys, secrets

**Source:** https://vercel.com/changelog/sensitive-environment-variables-are-now-available

---

### System Environment Variables

**Automatically populated by Vercel:**
```bash
VERCEL=1
VERCEL_ENV=production  # or preview, development
VERCEL_URL=your-deployment-url.vercel.app
VERCEL_REGION=iad1  # deployment region
VERCEL_GIT_COMMIT_SHA=abc123...
VERCEL_GIT_COMMIT_REF=main
VERCEL_GIT_REPO_OWNER=noonaut-homo-lumen-resonans
VERCEL_GIT_REPO_SLUG=homo-lumen-compendiums
```

**Source:** https://vercel.com/docs/environment-variables/system-environment-variables

---

### Best Practices

#### 1. Use NEXT_PUBLIC_ prefix for client-side variables
```bash
# ✅ Exposed to browser (safe)
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_API_ENDPOINT=...

# ❌ Server-side only (never exposed)
OPENAI_API_KEY=...
DATABASE_URL=...
```

#### 2. Enable Sensitive Variables for secrets
- API keys
- Database passwords
- OAuth secrets
- JWT secrets

#### 3. Use different values per environment
- Production: Real API keys
- Preview: Staging API keys
- Development: Test API keys

#### 4. Never commit .env files to Git
```bash
# .gitignore
.env
.env.local
.env.*.local
```

**Sources:**
- https://vercel.com/docs/environment-variables
- https://nextjs.org/docs/pages/guides/environment-variables
- https://vercel.com/docs/environment-variables/sensitive-environment-variables

---

## 📊 Summary of Key Findings

### AI Services Updates
1. ✅ **OpenAI Responses API** (March 2025) - New agent framework
2. ✅ **Claude Haiku 4.5** (October 2025) - Fastest Claude model
3. ✅ **Gemini 2.0 Flash** + **Grounding with Maps** (October 2025)
4. ✅ **o4-mini** - Cost-effective reasoning model

### MCP Servers
- **42+ official MCP servers** available
- **Top 15** ranked by popularity and use case
- **GitHub, MongoDB, Azure** are most popular
- **Figma, Databricks, Kubernetes** for specialized workflows

### NAV API
- ✅ **Official Job Vacancy Feed** available
- ✅ **Public token** for testing
- ✅ **Private token** via email request
- ✅ **Free to use** with terms agreement

### Vercel Best Practices
- ✅ **Sensitive variables** feature (Feb 2024)
- ✅ **System variables** auto-populated
- ✅ **NEXT_PUBLIC_** prefix for client-side
- ✅ **Never commit .env** to Git

---

## 🎯 Recommendations for NAV-Losen

### Priority 1: Update AI Services
```bash
# Add to Vercel
OPENAI_API_KEY=[use latest API]
ANTHROPIC_API_KEY=[Claude 4 series]
GEMINI_API_KEY=[Gemini 2.0 Flash]
```

### Priority 2: Enable NAV Job API
```bash
# Request private token from NAV
NAV_JOB_API_URL=https://pam-stilling-feed.nav.no/api/v1/feed
NAV_JOB_API_TOKEN=[request from nav.team.arbeidsplassen@nav.no]
```

### Priority 3: Consider MCP Servers
- **GitHub MCP** - For code management
- **Supabase MCP** - Already using Supabase
- **Notion MCP** - For documentation
- **Linear MCP** - For project management

### Priority 4: Enable Sensitive Variables
- Mark all API keys as "Sensitive" in Vercel
- Prevents accidental exposure in logs

---

**Research completed:** 21. oktober 2025, 15:20 CET  
**Next steps:** Add environment variables to Vercel Dashboard

**🔨 Manus**

