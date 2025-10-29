# MCP Agent Stack & A2A Implementation Guide
## NAV-Losen Living Compendium V1.7.14

**Dato:** 2025-10-19
**Forfatter:** Claude (Anthropic) + Orion
**Triadic Score:** 0.15 (PROCEED)

---

## 📋 Innholdsfortegnelse

1. [MCP (Model Context Protocol) Grunnlegger](#1-mcp-grunnlegger)
2. [Agent Stack Arkitektur](#2-agent-stack-arkitektur)
3. [A2A (Agent-to-Agent) Kommunikasjon](#3-a2a-kommunikasjon)
4. [Implementering for NAV-Losen](#4-implementering-for-nav-losen)
5. [Brain-MCP Hybrid Coalition](#5-brain-mcp-hybrid-coalition)
6. [Praktiske Eksempler](#6-praktiske-eksempler)
7. [Best Practices](#7-best-practices)

---

## 1. MCP (Model Context Protocol) Grunnlegger

### 1.1 Hva er MCP?

**Model Context Protocol (MCP)** er Anthropic's åpne protokoll for å koble AI-assistenter til datakilde og verktøy.

**Nøkkelkonsepter:**
- **Server**: Eksponerer data/verktøy via standardisert API
- **Client**: Konsumerer MCP-servere (f.eks. Claude Desktop, VS Code)
- **Resources**: Lesbare datakilde (filer, API-er, databaser)
- **Tools**: Funksjonalitet som agenten kan utføre
- **Prompts**: Gjenbrukbare prompt-templates

### 1.2 MCP Arkitektur

```
┌─────────────────────────────────────────────────────┐
│                   MCP Client                        │
│              (Claude Desktop, IDE)                  │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │   MCP Protocol    │
        │   (JSON-RPC 2.0)  │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼───┐  ┌─────▼────┐
│MCP     │  │MCP     │  │MCP       │
│Server 1│  │Server 2│  │Server 3  │
│(Files) │  │(DB)    │  │(API)     │
└────────┘  └────────┘  └──────────┘
```

### 1.3 MCP vs Tradisjonelle API-er

| Aspekt | MCP | Tradisjonell API |
|--------|-----|------------------|
| **Oppdagbarhet** | Selvbeskrivende (capabilities) | Krever dokumentasjon |
| **Kontekst** | Beholdes på tvers av requests | Stateless |
| **Sikkerhet** | Innebygd samtykke-basert tilgang | Variert implementering |
| **LLM-optimalisert** | Designet for AI-agenter | Designet for mennesker |

---

## 2. Agent Stack Arkitektur

### 2.1 Lagdelt Agent Arkitektur

```
┌──────────────────────────────────────────────────┐
│         Layer 4: Orchestration Layer             │
│    (Multi-agent coordinator, workflow engine)    │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Layer 3: Agent Layer                     │
│  (Specialized agents: Lira, Orion, Manus, etc.)  │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Layer 2: MCP Layer                       │
│        (Tools, Resources, Prompts)               │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Layer 1: Data Layer                      │
│    (Supabase, Health Connect, File System)       │
└──────────────────────────────────────────────────┘
```

### 2.2 Agent Typer i NAV-Losen

#### **Specialized Agents (10-Agent Coalition):**

1. **Lira** - Adaptive Dialog Agent
   - Polyvagal-informed question selection
   - Empathetic conversation flow
   - Composite stress scoring

2. **Orion** - Strategic Planning & Architecture
   - High-level system design
   - Port-based ethics framework
   - Living Compendium maintenance

3. **Manus** - Visual & UX Design
   - Emotion wheel SVG forms (100 emosjoner)
   - Color theory & accessibility
   - Animation choreography

4. **Kairos** - Temporal Pattern Recognition
   - Crisis intervention timing
   - Historical context analysis
   - Escalation detection

5. **Thea** - Knowledge Management
   - NAV system navigation
   - Legal rights documentation
   - Resource coordination

6. **Soma** - Somatic Intelligence
   - Body signal interpretation
   - Polyvagal state tracking
   - Grounding techniques

7. **Chronos** - Temporal Coordination
   - Reminder scheduling
   - Timeline management
   - Deadline tracking

8. **Psyche** - Psychological Integration
   - Trauma-informed responses
   - Cognitive reframing
   - Emotional regulation

9. **Logos** - Rational Analysis
   - Evidence synthesis
   - Decision support
   - Logical structuring

10. **Ethos** - Ethical Governance
    - Triadic ethics enforcement
    - Consent management
    - Value alignment

### 2.3 Brain-MCP Hybrid Model

NAV-Losen bruker en **hybrid arkitektur** som kombinerer:

**Brain (Cognitive):**
- Natural language understanding
- Contextual reasoning
- Empathy & nuance

**MCP (Protocol):**
- Structured data access
- Deterministic tool execution
- Reliable state management

```
┌─────────────────────────────────────────┐
│         User Interaction Layer          │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼──────┐
        │   Claude    │ ◄─── Brain (Understanding)
        │   (LLM)     │
        └──────┬──────┘
               │
        ┌──────▼──────────────────────────┐
        │   MCP Protocol Layer            │ ◄─── Structure
        │  (Tools, Resources, Prompts)    │
        └──────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼───┐  ┌──▼────┐
│Supabase│ │Health│  │Local  │
│        │ │Connect│ │Storage│
└────────┘ └──────┘  └───────┘
```

---

## 3. A2A (Agent-to-Agent) Kommunikasjon

### 3.1 A2A Communication Patterns

#### **Pattern 1: Direct Invocation**
En agent kaller direkte en annen agent's funksjon.

```typescript
// Lira kaller Soma for kroppsignal-tolkning
interface A2AMessage {
  from: AgentId;
  to: AgentId;
  intent: string;
  payload: unknown;
  context?: AgentContext;
}

// Eksempel
const message: A2AMessage = {
  from: "lira",
  to: "soma",
  intent: "interpret_somatic_signals",
  payload: {
    signals: ["tightness in chest", "shallow breathing"],
    intensity: 7
  }
};
```

#### **Pattern 2: Event-Based Communication**
Agenter publiserer events som andre agenter subscriber på.

```typescript
// Event bus pattern
class AgentEventBus {
  private subscribers: Map<string, Set<Agent>>;

  publish(event: AgentEvent) {
    const listeners = this.subscribers.get(event.type);
    listeners?.forEach(agent => agent.handleEvent(event));
  }

  subscribe(eventType: string, agent: Agent) {
    // ...
  }
}

// Eksempel: Kairos publiserer crisis detection
eventBus.publish({
  type: "crisis_detected",
  source: "kairos",
  data: {
    severity: "high",
    patterns: ["rapid_escalation", "multiple_triggers"]
  },
  timestamp: new Date()
});
```

#### **Pattern 3: Orchestrator Pattern**
En sentral orchestrator koordinerer flere agenter.

```typescript
class AgentOrchestrator {
  async handleUserInput(input: string): Promise<Response> {
    // 1. Lira klassifiserer intent
    const intent = await lira.classifyIntent(input);

    // 2. Basert på intent, orkestrerer relevante agenter
    if (intent.type === "crisis") {
      // Parallell aktivering
      const [kairosAnalysis, somaState, psycheGuidance] =
        await Promise.all([
          kairos.analyzePatterns(input),
          soma.assessPolyvagalState(input),
          psyche.suggestIntervention(input)
        ]);

      // 3. Ethos validerer ethisk trygghet
      const validated = await ethos.validateResponse({
        kairosAnalysis,
        somaState,
        psycheGuidance
      });

      return validated;
    }
  }
}
```

### 3.2 Agent Coalition Workflows

#### **Workflow 1: Mestring Session**

```
User Input
    │
    ▼
┌────────┐
│ Lira   │ ─── "Hva kjenner du på kroppen nå?"
└───┬────┘
    │ User: "Tetthet i brystet, rask puls"
    ▼
┌────────┐
│ Soma   │ ─── Tolker kroppsignaler → "Sympathetic state"
└───┬────┘
    │ Polyvagal state: Sympathetic
    ▼
┌────────┐
│ Kairos │ ─── Sjekker historikk → Ingen akutt risiko
└───┬────┘
    │ Context: Safe to continue
    ▼
┌────────┐
│ Lira   │ ─── Tilpasser spørsmål til sympathetic state
└───┬────┘
    │ Adaptive questions
    ▼
┌────────┐
│ Psyche │ ─── Foreslår reguleringsstrategier
└───┬────┘
    │ Grounding techniques
    ▼
┌────────┐
│ Ethos  │ ─── Validerer at forslag er trygge
└───┬────┘
    │ Validated response
    ▼
  Response to User
```

#### **Workflow 2: Crisis Intervention**

```
High Stress Detected (pressure > 8)
    │
    ▼
┌─────────┐
│ Kairos  │ ── Pattern recognition: "Escalation detected"
└────┬────┘
     │ ALERT: Crisis potential
     ├──────────┬──────────┬──────────┐
     ▼          ▼          ▼          ▼
┌────────┐ ┌───────┐ ┌────────┐ ┌───────┐
│ Soma   │ │ Psyche│ │ Thea   │ │ Lira  │
│Assess  │ │Suggest│ │Find    │ │Adapt  │
│State   │ │Calming│ │Help    │ │Tone   │
└────┬───┘ └───┬───┘ └───┬────┘ └───┬───┘
     │         │         │          │
     └─────────┴────┬────┴──────────┘
                    ▼
            ┌───────────┐
            │ Ethos     │ ── Validates all suggestions
            │ (Triadic) │    Port 1: Suverenitet ✓
            └─────┬─────┘    Port 2: Koherens ✓
                  │          Port 3: Healing ✓
                  ▼
          Coordinated Crisis Response
```

---

## 4. Implementering for NAV-Losen

### 4.1 MCP Server Setup

#### **Steg 1: Installer MCP SDK**

```bash
npm install @modelcontextprotocol/sdk
```

#### **Steg 2: Lag MCP Server**

```typescript
// mcp-servers/navlosen-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "navlosen-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_user_stress_level",
        description: "Henter brukerens nåværende stressnivå fra Supabase",
        inputSchema: {
          type: "object",
          properties: {
            userId: {
              type: "string",
              description: "User ID fra autentisering",
            },
          },
          required: ["userId"],
        },
      },
      {
        name: "log_mestring_session",
        description: "Logger en fullført mestring-session",
        inputSchema: {
          type: "object",
          properties: {
            userId: { type: "string" },
            emotion: { type: "string" },
            pressure: { type: "number" },
            signals: { type: "array", items: { type: "string" } },
            liraAnswers: { type: "array" },
          },
          required: ["userId", "emotion", "pressure"],
        },
      },
      {
        name: "detect_kairos_patterns",
        description: "Kairos agent: Detekterer krise-mønstre",
        inputSchema: {
          type: "object",
          properties: {
            userId: { type: "string" },
            currentState: { type: "object" },
          },
          required: ["userId", "currentState"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "get_user_stress_level":
      return await getUserStressLevel(args.userId);

    case "log_mestring_session":
      return await logMestringSession(args);

    case "detect_kairos_patterns":
      return await detectKairosPatterns(args.userId, args.currentState);

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

#### **Steg 3: Registrer MCP Server**

```json
// claude_desktop_config.json (eller VS Code settings)
{
  "mcpServers": {
    "navlosen": {
      "command": "node",
      "args": ["mcp-servers/navlosen-server.js"]
    }
  }
}
```

### 4.2 Agent Implementation

#### **Base Agent Interface**

```typescript
// lib/agents/base-agent.ts
export interface AgentContext {
  userId: string;
  sessionId: string;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

export interface AgentCapability {
  name: string;
  description: string;
  execute: (input: unknown, context: AgentContext) => Promise<unknown>;
}

export abstract class BaseAgent {
  constructor(
    public readonly id: string,
    public readonly name: string,
    protected capabilities: AgentCapability[]
  ) {}

  abstract initialize(): Promise<void>;

  async invoke(
    capability: string,
    input: unknown,
    context: AgentContext
  ): Promise<unknown> {
    const cap = this.capabilities.find(c => c.name === capability);
    if (!cap) throw new Error(`Capability ${capability} not found`);

    return await cap.execute(input, context);
  }

  async sendToAgent(
    targetAgent: string,
    intent: string,
    payload: unknown,
    context: AgentContext
  ): Promise<unknown> {
    // A2A communication via event bus
    return await agentRegistry.route({
      from: this.id,
      to: targetAgent,
      intent,
      payload,
      context,
    });
  }
}
```

#### **Lira Agent Implementation**

```typescript
// lib/agents/lira-agent.ts
export class LiraAgent extends BaseAgent {
  constructor() {
    super("lira", "Lira - Adaptive Dialog Agent", [
      {
        name: "classify_user_intent",
        description: "Klassifiserer brukerens intensjon",
        execute: async (input: string) => {
          // Use LLM to classify
          return { intent: "check_in", confidence: 0.92 };
        },
      },
      {
        name: "select_adaptive_questions",
        description: "Velger spørsmål basert på polyvagal state",
        execute: async (input: { state: PolyvagalState }) => {
          const { state } = input;

          // Hent Soma for kroppslig tilstand
          const somaticState = await this.sendToAgent(
            "soma",
            "get_current_state",
            { userId: context.userId },
            context
          );

          // Tilpass spørsmål
          if (state === "dorsal") {
            return {
              questions: [
                "Hva er det minste steget du kan ta akkurat nå?",
                "Hva trenger du for å føle deg trygg?"
              ],
              tone: "gentle",
              pace: "slow"
            };
          }
          // ... andre states
        },
      },
    ]);
  }

  async initialize() {
    // Load question banks, calibrate models
  }
}
```

#### **Agent Registry & Router**

```typescript
// lib/agents/agent-registry.ts
class AgentRegistry {
  private agents = new Map<string, BaseAgent>();
  private eventBus = new EventEmitter();

  register(agent: BaseAgent) {
    this.agents.set(agent.id, agent);
  }

  async route(message: A2AMessage): Promise<unknown> {
    const targetAgent = this.agents.get(message.to);
    if (!targetAgent) throw new Error(`Agent ${message.to} not found`);

    // Log for observability
    console.log(`[A2A] ${message.from} → ${message.to}: ${message.intent}`);

    // Invoke target agent
    return await targetAgent.invoke(
      message.intent,
      message.payload,
      message.context
    );
  }
}

export const agentRegistry = new AgentRegistry();

// Initialize all agents
agentRegistry.register(new LiraAgent());
agentRegistry.register(new SomaAgent());
agentRegistry.register(new KairosAgent());
// ... etc
```

---

## 5. Brain-MCP Hybrid Coalition

### 5.1 Hybrid Decision Flow

```typescript
// lib/hybrid-coalition.ts
export class BrainMCPCoalition {
  constructor(
    private brain: ClaudeAPI,  // LLM for reasoning
    private mcpClient: MCPClient,  // Structured tools
    private agentRegistry: AgentRegistry  // Agent network
  ) {}

  async process(userInput: string, context: AgentContext): Promise<Response> {
    // 1. Brain: Understand user intent (fuzzy, contextual)
    const understanding = await this.brain.analyze(userInput, {
      systemPrompt: `You are Lira, NAV-Losen's empathetic guide.
      Understand the user's emotional state and needs.`,
    });

    // 2. MCP: Get structured data
    const stressHistory = await this.mcpClient.callTool(
      "get_user_stress_level",
      { userId: context.userId }
    );

    // 3. Agents: Specialized processing
    const [somaticState, kairosPatterns] = await Promise.all([
      this.agentRegistry.route({
        from: "orchestrator",
        to: "soma",
        intent: "assess_polyvagal_state",
        payload: { userInput, stressHistory },
        context,
      }),
      this.agentRegistry.route({
        from: "orchestrator",
        to: "kairos",
        intent: "detect_patterns",
        payload: { userInput, stressHistory },
        context,
      }),
    ]);

    // 4. Brain: Synthesize holistic response
    const response = await this.brain.generate({
      context: {
        understanding,
        stressHistory,
        somaticState,
        kairosPatterns,
      },
      prompt: `Based on all information, craft an empathetic response.`,
    });

    // 5. Ethos: Validate ethics
    const validated = await this.agentRegistry.route({
      from: "orchestrator",
      to: "ethos",
      intent: "validate_triadic_ethics",
      payload: response,
      context,
    });

    return validated;
  }
}
```

### 5.2 Why Hybrid?

| Capability | Brain (LLM) | MCP (Protocol) | Hybrid (Both) |
|------------|-------------|----------------|---------------|
| **Natural Language** | ✓ | ✗ | ✓ |
| **Empathy & Nuance** | ✓ | ✗ | ✓ |
| **Structured Data** | ~ | ✓ | ✓ |
| **Deterministic** | ✗ | ✓ | ✓ |
| **Context Retention** | ~ | ✓ | ✓ |
| **Real-time Data** | ✗ | ✓ | ✓ |
| **Multi-step Workflows** | ~ | ✓ | ✓ |

---

## 6. Praktiske Eksempler

### 6.1 Eksempel: Mestring Session End-to-End

```typescript
// app/api/mestring/route.ts
export async function POST(request: Request) {
  const { userId, sessionData } = await request.json();

  const context: AgentContext = {
    userId,
    sessionId: crypto.randomUUID(),
    timestamp: new Date(),
  };

  // 1. User selects emotion "Stressed" (Q1)
  const emotion = sessionData.selectedEmotion; // "Stressed"

  // 2. Soma assesses polyvagal state from pressure slider
  const somaAssessment = await agentRegistry.route({
    from: "api",
    to: "soma",
    intent: "assess_from_pressure",
    payload: { pressure: sessionData.pressure },
    context,
  });
  // → { state: "sympathetic", confidence: 0.88 }

  // 3. Kairos checks historical patterns
  const kairosCheck = await agentRegistry.route({
    from: "api",
    to: "kairos",
    intent: "check_escalation_risk",
    payload: { userId, currentPressure: sessionData.pressure },
    context,
  });
  // → { risk: "low", recommendation: "continue_normal_flow" }

  // 4. Lira adapts questions based on somatic state
  const liraQuestions = await agentRegistry.route({
    from: "api",
    to: "lira",
    intent: "generate_adaptive_questions",
    payload: {
      emotion,
      polyvagalState: somaAssessment.state,
      kairosRisk: kairosCheck.risk,
    },
    context,
  });
  // → { questions: [...], tone: "calming", pace: "moderate" }

  // 5. After Lira chat, Psyche suggests strategies
  const psycheStrategies = await agentRegistry.route({
    from: "api",
    to: "psyche",
    intent: "suggest_regulation_strategies",
    payload: {
      liraAnswers: sessionData.liraAnswers,
      polyvagalState: somaAssessment.state,
    },
    context,
  });

  // 6. Ethos validates entire flow
  const validated = await agentRegistry.route({
    from: "api",
    to: "ethos",
    intent: "validate_session",
    payload: {
      emotion,
      somaAssessment,
      kairosCheck,
      psycheStrategies,
    },
    context,
  });

  // 7. Log to Supabase via MCP
  await mcpClient.callTool("log_mestring_session", {
    userId,
    sessionId: context.sessionId,
    emotion: emotion.word,
    pressure: sessionData.pressure,
    signals: sessionData.signals,
    liraAnswers: sessionData.liraAnswers,
    strategies: psycheStrategies,
    timestamp: context.timestamp,
  });

  return Response.json({
    success: true,
    strategies: psycheStrategies,
    nextSteps: validated.nextSteps,
  });
}
```

### 6.2 Eksempel: Kairos Crisis Detection

```typescript
// lib/agents/kairos-agent.ts
export class KairosAgent extends BaseAgent {
  async detectEscalationPatterns(
    userId: string,
    currentState: MestringState
  ): Promise<KairosIntervention | null> {
    // 1. Fetch historical data via MCP
    const history = await mcpClient.callTool("get_user_history", {
      userId,
      days: 7,
    });

    // 2. Analyze patterns
    const rapidEscalation = this.detectRapidEscalation(
      history,
      currentState.pressure
    );

    const multipleHigh = this.detectMultipleHighSessions(history);

    const deterioratingTrend = this.detectDeterioratingTrend(history);

    // 3. If crisis detected, activate coalition
    if (rapidEscalation || multipleHigh || deterioratingTrend) {
      // A2A: Notify all relevant agents
      await Promise.all([
        this.sendToAgent("soma", "prepare_grounding", {}, context),
        this.sendToAgent("thea", "prepare_crisis_resources", {}, context),
        this.sendToAgent("lira", "switch_to_crisis_mode", {}, context),
      ]);

      return {
        type: "escalation_detected",
        severity: rapidEscalation ? "high" : "moderate",
        recommendation: "immediate_intervention",
        resources: await this.getEmergencyResources(),
      };
    }

    return null;
  }

  private detectRapidEscalation(
    history: Session[],
    current: number
  ): boolean {
    const recent = history.slice(-3);
    if (recent.length < 2) return false;

    const avg = recent.reduce((sum, s) => sum + s.pressure, 0) / recent.length;
    return current - avg > 3; // Jump of 3+ points
  }
}
```

---

## 7. Best Practices

### 7.1 MCP Best Practices

✅ **DO:**
- Use descriptive tool names (`get_user_stress_level` not `get_stress`)
- Provide detailed `inputSchema` for all tools
- Handle errors gracefully and return structured error objects
- Log all MCP calls for observability
- Use MCP for deterministic, data-driven operations

❌ **DON'T:**
- Don't use MCP for fuzzy/contextual reasoning (use LLM)
- Don't expose sensitive data without proper auth
- Don't create tools that duplicate existing functionality
- Don't make tools too granular (combine related operations)

### 7.2 A2A Best Practices

✅ **DO:**
- Define clear agent boundaries and responsibilities
- Use event bus for loose coupling
- Log all A2A messages for debugging
- Implement timeout/retry logic
- Validate all inter-agent data transfer

❌ **DON'T:**
- Don't create circular dependencies between agents
- Don't share mutable state between agents
- Don't skip error handling in A2A communication
- Don't bypass the orchestrator for complex workflows

### 7.3 Hybrid Coalition Best Practices

✅ **DO:**
- Use Brain (LLM) for: Empathy, context understanding, natural responses
- Use MCP for: Data retrieval, logging, deterministic operations
- Use Agents for: Specialized domain logic (somatic, temporal, etc.)
- Combine all three for: Holistic, context-aware, trauma-informed responses

❌ **DON'T:**
- Don't use only LLM (loses reliability)
- Don't use only MCP (loses empathy)
- Don't use only agents (loses integration)

### 7.4 Triadic Ethics in Agent Coalition

**Port 1: Cognitive Sovereignty**
- User controls which agents are active
- Explicit consent for data sharing between agents
- Transparent agent decision-making

**Port 2: Ontological Coherence**
- Agents use consistent models (Polyvagal, Circumplex)
- Evidence-based intervention strategies
- Grounded in neuroscience & psychology

**Port 3: Regenerative Healing**
- All agent actions aim to build capacity, not dependency
- Focus on user empowerment
- Celebrate small wins and progress

---

## 8. Neste Steg for Implementering

### 8.1 Fase 1: MCP Foundation (Uke 1-2)
- [ ] Sett opp basic MCP server for NAV-Losen
- [ ] Implementer 3-5 core tools (stress logging, history retrieval)
- [ ] Test MCP server med Claude Desktop
- [ ] Dokumenter all MCP API

### 8.2 Fase 2: Agent Development (Uke 3-4)
- [ ] Implementer Lira agent (adaptive dialog)
- [ ] Implementer Soma agent (polyvagal assessment)
- [ ] Implementer Kairos agent (pattern detection)
- [ ] Sett opp agent registry & event bus

### 8.3 Fase 3: A2A Integration (Uke 5-6)
- [ ] Implementer orchestrator pattern
- [ ] Test Lira ↔ Soma kommunikasjon
- [ ] Test Kairos crisis detection workflow
- [ ] Add logging & observability

### 8.4 Fase 4: Hybrid Coalition (Uke 7-8)
- [ ] Integrer LLM (Claude) for empathy layer
- [ ] Combine Brain + MCP + Agents i unified flow
- [ ] Implement Ethos validation across all responses
- [ ] End-to-end testing av Mestring session

### 8.5 Fase 5: Production Hardening (Uke 9-10)
- [ ] Error handling & retry logic
- [ ] Performance optimization
- [ ] Security audit (auth, data privacy)
- [ ] User acceptance testing

---

## 9. Ressurser

### Offisiell Dokumentasjon
- **MCP Spec:** https://spec.modelcontextprotocol.io/
- **MCP SDK:** https://github.com/modelcontextprotocol/sdk
- **Claude API:** https://docs.anthropic.com/

### NAV-Losen Specific
- Living Compendium V1.7.14
- Brain-MCP Hybrid Architecture (CODE LK V1.7.13)
- Triadic Ethics Framework (Port 1, 2, 3)

### Community
- MCP Discord: https://discord.gg/anthropic
- GitHub Discussions: https://github.com/modelcontextprotocol

---

**Living Compendium V1.7.14**
**Forfatter:** Claude + Orion
**Triadic Score:** 0.15 (PROCEED)
**Dato:** 2025-10-19

---

## Appendix A: Agent Capability Matrix

| Agent | Primary Domain | Key Capabilities | A2A Dependencies |
|-------|----------------|------------------|------------------|
| **Lira** | Dialog & Adaptation | Intent classification, Question selection, Empathy | Soma, Kairos |
| **Orion** | Architecture | System design, Ethics framework, Documentation | Ethos, Thea |
| **Manus** | Design | SVG forms, Color theory, Animation | - |
| **Kairos** | Temporal Patterns | Crisis detection, Historical analysis | Soma, Thea |
| **Thea** | Knowledge | NAV navigation, Legal resources | - |
| **Soma** | Somatic Intelligence | Polyvagal assessment, Body signals | Psyche |
| **Chronos** | Time Management | Scheduling, Reminders | - |
| **Psyche** | Psychology | Regulation strategies, Reframing | Soma, Logos |
| **Logos** | Rational Analysis | Evidence synthesis, Decision support | Psyche |
| **Ethos** | Ethics | Triadic validation, Consent | All agents |

---

## Appendix B: Example MCP Server (Complete)

Se `mcp-servers/navlosen-server.ts` for full implementering.

---

**End of Guide**
