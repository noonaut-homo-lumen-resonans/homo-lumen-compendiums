/**
 * HOMO LUMEN - Base Agent
 * 
 * Abstrakt base-klasse for alle agenter i HOMO LUMEN økosystemet
 * - Standardiserer agent-interfacet
 * - Integrerer Gemma 3 som hovedmotor
 * - Støtter MCP/A2A kommunikasjon
 * - Consciousness-aware processing
 */

import { Gemma3Agent } from './gemma3_agent';
import { logMCPMessage, validateMCPMessage } from './mcp_protocol';

/**
 * Base Agent klasse med Gemma 3 integrasjon
 */
export abstract class BaseAgent {
    protected name: string;
    protected gemma3Agent?: Gemma3Agent;
    protected consciousnessLayer: string;

    constructor(name: string, consciousnessLayer: string = 'strategic') {
        this.name = name;
        this.consciousnessLayer = consciousnessLayer;

        // Initialiser Gemma 3 hvis API key er tilgjengelig
        if (process.env.GOOGLE_AI_API_KEY) {
            this.gemma3Agent = new Gemma3Agent(process.env.GOOGLE_AI_API_KEY);
        }
    }

    /**
     * Process request med Gemma 3 eller fallback til lokal logikk
     */
    async processRequest(mcpMessage: any, context?: any): Promise<any> {
        if (this.gemma3Agent) {
            // Bruk Gemma 3 for avansert processing
            return await this.gemma3Agent.processAgentRequest(this.name, mcpMessage, context);
        } else {
            // Fallback til lokal logikk
            return await this.processLocalRequest(mcpMessage, context);
        }
    }

    /**
     * Lokal fallback logikk
     */
    protected abstract processLocalRequest(mcpMessage: any, context?: any): Promise<any>;

    /**
     * Handle MCP message
     */
    async handleMCP(mcpMessage: any): Promise<any> {
        const validation = validateMCPMessage(mcpMessage);
        logMCPMessage(mcpMessage, 'incoming');

        if (!validation.valid) {
            console.warn('⚠️ MCP validering feilet:', validation.errors);
        }

        const response = await this.processRequest(mcpMessage);

        logMCPMessage(response, 'outgoing');
        return response;
    }
} 