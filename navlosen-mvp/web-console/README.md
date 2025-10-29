# Homo Lumen OS - Web Console

Web-based console for managing the Homo Lumen agent coalition and NAV-Losen system.

## 🎯 Overview

The Web Console provides:
- **Agent Status Monitoring** - Real-time status of all 8 agents
- **MCP Broker Management** - Lightweight routing system for MVP
- **SMK Logging** - Symbiotisk Minne Kompendium (Symbiotic Memory Compendium)
- **System Metrics** - Performance and usage analytics
- **Agent Communication** - Direct interaction with individual agents

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    WEB CONSOLE                          │
│                   (Next.js + React)                     │
└──────────────────┬──────────────────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │   MCP BROKER      │  (Lightweight routing)
         └─────────┬─────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐      ┌───▼───┐      ┌───▼───┐
│ ORION │      │ LIRA  │      │THALUS │
│  API  │      │  API  │      │  API  │
└───────┘      └───────┘      └───────┘
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and pnpm
- Supabase account and project
- Environment variables configured

### Installation

1. **Install dependencies:**
```bash
pnpm install
```

2. **Configure environment variables:**
```bash
cp .env.example .env.local
```

Edit `.env.local` with your Supabase credentials:
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

3. **Run development server:**
```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
pnpm build
pnpm start
```

## 📁 Project Structure

```
web-console/
├── app/
│   ├── api/
│   │   ├── agents/[agent]/route.ts   # Agent API endpoints
│   │   └── smk/log/route.ts          # SMK logging endpoint
│   ├── dashboard/
│   │   └── page.tsx                  # Main dashboard
│   └── layout.tsx                    # Root layout
├── lib/
│   ├── mcp-broker.ts                 # MCP Broker logic
│   └── supabase.ts                   # Supabase client
├── .env.example                      # Environment template
└── README.md                         # This file
```

## 🔧 Configuration

### Agent Configuration

Agents are configured in `lib/mcp-broker.ts`:

```typescript
export const AGENTS: Record<AgentType, AgentConfig> = {
  orion: {
    id: 'orion',
    name: 'Orion',
    domain: ['strategy', 'coordination', 'system'],
    apiEndpoint: '/api/agents/orion',
    model: 'claude-sonnet-4.5',
    description: 'Meta-Koordinator'
  },
  // ... other agents
};
```

### MCP Broker Routing

The MCP Broker uses keyword-based routing in MVP:

```typescript
export function routeRequest(request: MCPRequest): AgentType {
  // Check domain keywords
  for (const [agentId, config] of Object.entries(AGENTS)) {
    for (const keyword of config.domain) {
      if (intent.includes(keyword)) {
        return agentId as AgentType;
      }
    }
  }
  
  // Default to Lira
  return 'lira';
}
```

## 📊 Features

### 1. Agent Status Monitoring

Real-time monitoring of all agents:
- Online/offline status
- Response latency
- Last seen timestamp
- Model information

### 2. SMK Logging

Symbiotisk Minne Kompendium entries:
- Learning events
- Decision points
- User interactions
- Error logs

### 3. System Metrics

Performance tracking:
- API response times
- Token usage
- User activity
- System health

### 4. MCP Broker

Lightweight routing for MVP:
- Keyword-based routing
- Lira Hub filtering
- Agent health checks
- Request logging

## 🔐 Security

### Data Firewall

**Critical:** Tvedestrand pilot data NEVER flows to Homo Lumen R&D.

- Separate database schemas
- Row-level security (RLS)
- GDPR-compliant data handling
- Audit logging

### Authentication

Uses Supabase Auth:
- Email/password authentication
- JWT-based sessions
- Role-based access control (RBAC)

## 🧪 Testing

```bash
# Run tests
pnpm test

# Run linter
pnpm lint

# Type checking
pnpm type-check
```

## 📚 API Documentation

### Agent Endpoints

**POST** `/api/agents/[agent]`
- Send message to specific agent
- Request body: `{ model, messages, context }`
- Returns: `{ response, confidence, metadata }`

**GET** `/api/agents/[agent]`
- Get agent information
- Returns: `{ id, name, description, domain, model }`

**GET** `/api/agents/[agent]/health`
- Check agent health
- Returns: `{ status, agent, model, timestamp }`

### SMK Endpoints

**POST** `/api/smk/log`
- Log SMK entry
- Request body: `{ agent, type, content, metadata }`
- Returns: `{ success, entry_id, timestamp }`

## 🚢 Deployment

### Netlify Deployment

1. Connect repository to Netlify
2. Configure build settings:
   - Build command: `pnpm build`
   - Publish directory: `.next`
3. Add environment variables in Netlify dashboard
4. Deploy!

### Environment Variables

Required for production:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `OPENAI_API_KEY` (for Lira)
- `ANTHROPIC_API_KEY` (for Orion, Zara)
- `XAI_API_KEY` (for Thalus, Falcon)
- `GOOGLE_AI_API_KEY` (for Nyra, Aurora)

## 📖 Documentation

- [System Building Guide](../docs/SYSTEM_BUILDING_GUIDE.md)
- [NAV-Losen Decision Log](../NAV_LOSEN_DECISION_LOG.md)
- [Supabase Schema](../supabase/migrations/20251020_initial_schema.sql)
- [MCP Broker Architecture](../docs/MCP_BROKER_ARCHITECTURE.md)

## 🤝 Contributing

This is part of the Homo Lumen OS project. See main repository for contribution guidelines.

## 📝 License

Proprietary - Tvedestrand Kommune Pilot Project

---

**Version:** 1.0.0  
**Last Updated:** 20. oktober 2025  
**Maintainer:** Manus (Agent #8, Infrastruktur Hub)

