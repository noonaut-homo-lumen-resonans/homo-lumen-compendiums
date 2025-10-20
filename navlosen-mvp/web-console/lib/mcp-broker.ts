/**
 * MCP Broker - Lightweight Agent Routing for MVP
 * 
 * This is a simplified routing system for the Homo Lumen OS MVP.
 * It routes requests to the appropriate agent based on intent and context.
 * 
 * In production, this will be replaced with a full MCP (Model Context Protocol) implementation.
 */

export type AgentType = 'orion' | 'lira' | 'thalus' | 'zara' | 'nyra' | 'manus' | 'falcon' | 'aurora';

export interface AgentConfig {
  id: AgentType;
  name: string;
  domain: string[];
  apiEndpoint: string;
  model: string;
  description: string;
}

export interface MCPRequest {
  intent: string;
  context: Record<string, any>;
  userId?: string;
  sessionId?: string;
  timestamp: string;
}

export interface MCPResponse {
  agent: AgentType;
  response: string;
  confidence: number;
  metadata: Record<string, any>;
  timestamp: string;
}

// Agent Configuration
export const AGENTS: Record<AgentType, AgentConfig> = {
  orion: {
    id: 'orion',
    name: 'Orion',
    domain: ['strategy', 'coordination', 'system', 'overview', 'dashboard'],
    apiEndpoint: process.env.NEXT_PUBLIC_ORION_API || '/api/agents/orion',
    model: 'claude-sonnet-4.5',
    description: 'Meta-Koordinator for strategisk oversikt og systemkoordinering'
  },
  lira: {
    id: 'lira',
    name: 'Lira',
    domain: ['emotion', 'healing', 'empathy', 'support', 'mestring', 'chat'],
    apiEndpoint: process.env.NEXT_PUBLIC_LIRA_API || '/api/agents/lira',
    model: 'gpt-5',
    description: 'Empatisk Healer for følelsesmessig støtte og mestring'
  },
  thalus: {
    id: 'thalus',
    name: 'Thalus',
    domain: ['ethics', 'validation', 'guidance', 'rights', 'nav'],
    apiEndpoint: process.env.NEXT_PUBLIC_THALUS_API || '/api/agents/thalus',
    model: 'grok-4',
    description: 'Etisk Vokter for validering og veiledning'
  },
  zara: {
    id: 'zara',
    name: 'Zara',
    domain: ['security', 'privacy', 'data', 'gdpr'],
    apiEndpoint: process.env.NEXT_PUBLIC_ZARA_API || '/api/agents/zara',
    model: 'claude-opus',
    description: 'Sikkerhetsvokter for dataintegritet og personvern'
  },
  nyra: {
    id: 'nyra',
    name: 'Nyra',
    domain: ['design', 'ux', 'visual', 'creative'],
    apiEndpoint: process.env.NEXT_PUBLIC_NYRA_API || '/api/agents/nyra',
    model: 'gemini-2.5-flash',
    description: 'Kreativ Designer for visuell utforming'
  },
  manus: {
    id: 'manus',
    name: 'Manus',
    domain: ['infrastructure', 'technical', 'architecture', 'build'],
    apiEndpoint: process.env.NEXT_PUBLIC_MANUS_API || '/api/agents/manus',
    model: 'claude-sonnet-4.5',
    description: 'Infrastruktur Hub for teknisk arkitektur'
  },
  falcon: {
    id: 'falcon',
    name: 'Falcon',
    domain: ['research', 'analysis', 'competitive', 'market'],
    apiEndpoint: process.env.NEXT_PUBLIC_FALCON_API || '/api/agents/falcon',
    model: 'grok-4',
    description: 'Intelligence Analyst for forskning og analyse'
  },
  aurora: {
    id: 'aurora',
    name: 'Aurora',
    domain: ['documentation', 'knowledge', 'learning', 'memory'],
    apiEndpoint: process.env.NEXT_PUBLIC_AURORA_API || '/api/agents/aurora',
    model: 'gemini-2.5-flash',
    description: 'Kunnskapsvokter for dokumentasjon og læring'
  }
};

/**
 * Route request to appropriate agent based on intent and context
 */
export function routeRequest(request: MCPRequest): AgentType {
  const { intent, context } = request;
  const intentLower = intent.toLowerCase();
  
  // Check each agent's domain keywords
  for (const [agentId, config] of Object.entries(AGENTS)) {
    for (const keyword of config.domain) {
      if (intentLower.includes(keyword)) {
        return agentId as AgentType;
      }
    }
  }
  
  // Default routing based on context
  if (context.emotionalState) return 'lira';
  if (context.needsValidation) return 'thalus';
  if (context.systemLevel) return 'orion';
  
  // Default to Lira (primary user interface)
  return 'lira';
}

/**
 * Send request to agent via MCP Broker
 */
export async function sendToAgent(
  agent: AgentType,
  request: MCPRequest
): Promise<MCPResponse> {
  const config = AGENTS[agent];
  
  try {
    const response = await fetch(config.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: config.model,
        messages: [
          {
            role: 'system',
            content: `You are ${config.name}, ${config.description}. Respond in Norwegian.`
          },
          {
            role: 'user',
            content: request.intent
          }
        ],
        context: request.context
      })
    });
    
    if (!response.ok) {
      throw new Error(`Agent ${agent} returned ${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      agent,
      response: data.response || data.message || data.content,
      confidence: data.confidence || 0.95,
      metadata: {
        model: config.model,
        tokens: data.usage?.total_tokens || 0,
        ...data.metadata
      },
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error(`Error communicating with agent ${agent}:`, error);
    throw error;
  }
}

/**
 * Process request through MCP Broker with Lira Hub filter
 */
export async function processRequest(request: MCPRequest): Promise<MCPResponse> {
  // Step 1: Route through Lira Hub (limbic filter)
  const liraFilter = await sendToAgent('lira', {
    ...request,
    intent: `[FILTER MODE] Assess emotional safety and route: ${request.intent}`
  });
  
  // Step 2: Determine target agent
  const targetAgent = routeRequest(request);
  
  // Step 3: Send to target agent (if not Lira)
  let agentResponse: MCPResponse;
  if (targetAgent === 'lira') {
    agentResponse = await sendToAgent('lira', request);
  } else {
    agentResponse = await sendToAgent(targetAgent, request);
  }
  
  // Step 4: Validate through Lira Hub before returning
  const validatedResponse = await sendToAgent('lira', {
    ...request,
    intent: `[VALIDATION MODE] Ensure empathetic delivery: ${agentResponse.response}`
  });
  
  return {
    ...agentResponse,
    response: validatedResponse.response,
    metadata: {
      ...agentResponse.metadata,
      routedThrough: ['lira', targetAgent, 'lira'],
      filterConfidence: liraFilter.confidence
    }
  };
}

/**
 * Get agent status and health
 */
export async function getAgentStatus(agent: AgentType): Promise<{
  online: boolean;
  latency: number;
  lastSeen: string;
}> {
  const config = AGENTS[agent];
  const startTime = Date.now();
  
  try {
    const response = await fetch(`${config.apiEndpoint}/health`, {
      method: 'GET'
    });
    
    const latency = Date.now() - startTime;
    
    return {
      online: response.ok,
      latency,
      lastSeen: new Date().toISOString()
    };
  } catch (error) {
    return {
      online: false,
      latency: -1,
      lastSeen: new Date().toISOString()
    };
  }
}

/**
 * Log SMK (Symbiotisk Minne Kompendium) entry
 */
export async function logSMK(entry: {
  agent: AgentType;
  type: 'learning' | 'decision' | 'interaction' | 'error';
  content: string;
  metadata: Record<string, any>;
}): Promise<void> {
  // In MVP: Log to Supabase
  // In production: Log to Git + Supabase
  
  try {
    await fetch('/api/smk/log', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...entry,
        timestamp: new Date().toISOString()
      })
    });
  } catch (error) {
    console.error('Failed to log SMK entry:', error);
  }
}

