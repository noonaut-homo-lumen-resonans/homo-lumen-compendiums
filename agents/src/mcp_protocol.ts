/**
 * HOMO LUMEN - Model Context Protocol (MCP)
 * 
 * Standardisert protokoll for agent-til-agent kommunikasjon
 * og kontekstdeling i bevissthetsstøttende AI-økosystemet
 */

// ============================================================================
// MCP INTERFACES OG TYPER
// ============================================================================

/**
 * Hovedinterface for MCP-meldinger
 * Standardiserer hvordan agenter kommuniserer med hverandre
 */
export interface MCPMessage {
    // Agent-identifikasjon
    agent_id: string;
    model_type: string;
    consciousness_layer: 'reactive' | 'strategic' | 'meta' | 'evolutionary';

    // Brukerintensjon og kontekst
    user_intention: string;
    operation: string;

    // Biofelt-tilstand (valgfritt)
    biofelt_state?: {
        hrv?: number;
        resonans?: string;
        harenes_reiser_seg?: boolean;
    };

    // Minne og historikk
    memory_context?: any;
    previous_responses?: any[];

    // AI Studio konfigurasjon (valgfritt)
    ai_studio_config?: {
        model: string;
        temperature: number;
        max_tokens?: number;
        consciousness_aware: boolean;
    };

    // Metadata
    timestamp?: string;
    session_id?: string;
    validation_status?: 'pending' | 'validated' | 'failed';
}

/**
 * MCP-respons fra agenter
 */
export interface MCPResponse {
    agent_id: string;
    status: 'success' | 'error' | 'validation_failed' | 'biofelt_validation_failed';
    result: any;
    message: string;
    consciousness_layer?: string;
    biofelt_validation?: any;
    recommendations?: string[];
    timestamp: string;
}

/**
 * AI Studio respons for Google AI Studio integrasjon
 */
export interface AIStudioResponse {
    model: string;
    response: string;
    consciousness_layer: string;
    biofelt_validation: any;
    recommendations: string[];
    function_calls?: any[];
    function_results?: any[];
    metadata: {
        tokens_used: number;
        response_time: number;
        model_confidence: number;
        function_calls_executed?: number;
    };
}

/**
 * MCP-validering resultat
 */
export interface MCPValidation {
    valid: boolean;
    errors?: string[];
    warnings?: string[];
    consciousness_layer: string;
    biofelt_coherent: boolean;
}

// ============================================================================
// MCP VALIDERING OG HJELEPEFUNKSJONER
// ============================================================================

/**
 * Validerer en MCP-melding
 */
export function validateMCPMessage(message: MCPMessage): MCPValidation {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Påkrevde felter
    if (!message.agent_id) errors.push('agent_id er påkrevd');
    if (!message.model_type) errors.push('model_type er påkrevd');
    if (!message.consciousness_layer) errors.push('consciousness_layer er påkrevd');
    if (!message.user_intention) errors.push('user_intention er påkrevd');
    if (!message.operation) errors.push('operation er påkrevd');

    // Biofelt-validering
    let biofelt_coherent = true;
    if (message.biofelt_state) {
        if (typeof message.biofelt_state.hrv === 'number' && message.biofelt_state.hrv < 60) {
            warnings.push('HRV under 60 - lav bevissthetskohærens');
            biofelt_coherent = false;
        }
        if (
            typeof message.biofelt_state.resonans === 'string' &&
            !['positiv', 'dyp_empatisk_resonans', 'klarhet'].includes(message.biofelt_state.resonans)
        ) {
            warnings.push('Suboptimal resonans for bevissthetsstøttende operasjoner');
        }
    }

    // Bevissthetslag-validering
    const validLayers = ['reactive', 'strategic', 'meta', 'evolutionary'];
    if (!validLayers.includes(message.consciousness_layer)) {
        errors.push(`Ugyldig consciousness_layer: ${message.consciousness_layer}`);
    }

    return {
        valid: errors.length === 0,
        errors,
        warnings,
        consciousness_layer: message.consciousness_layer,
        biofelt_coherent
    };
}

/**
 * Oppretter en standardisert MCP-melding
 */
export function createMCPMessage(
    agent_id: string,
    user_intention: string,
    operation: string,
    consciousness_layer: 'reactive' | 'strategic' | 'meta' | 'evolutionary',
    biofelt_state?: any
): MCPMessage {
    return {
        agent_id,
        model_type: 'gemini-1.5-flash',
        consciousness_layer,
        user_intention,
        operation,
        biofelt_state,
        timestamp: new Date().toISOString(),
        validation_status: 'pending'
    };
}

/**
 * Oppretter en standardisert MCP-respons
 */
export function createMCPResponse(
    agent_id: string,
    status: 'success' | 'error' | 'validation_failed' | 'biofelt_validation_failed',
    result: any,
    message: string
): MCPResponse {
    return {
        agent_id,
        status,
        result,
        message,
        timestamp: new Date().toISOString()
    };
}

// ============================================================================
// MCP LOGGING OG OBSERVABILITY
// ============================================================================

/**
 * Logger MCP-meldinger for observability
 */
export function logMCPMessage(message: MCPMessage, direction: 'incoming' | 'outgoing') {
    console.log(`📨 MCP ${direction.toUpperCase()}:`, {
        from: message.agent_id,
        operation: message.operation,
        consciousness_layer: message.consciousness_layer,
        timestamp: message.timestamp
    });
}

/**
 * Logger MCP-responser for observability
 */
export function logMCPResponse(response: MCPResponse) {
    console.log(`📤 MCP RESPONSE:`, {
        from: response.agent_id,
        status: response.status,
        consciousness_layer: response.consciousness_layer,
        timestamp: response.timestamp
    });
}

// ============================================================================
// MCP AGENT COORDINATION
// ============================================================================

/**
 * Koordinerer MCP-kall mellom agenter
 */
export async function coordinateMCPCall(
    fromAgent: string,
    toAgent: string,
    mcpMessage: MCPMessage,
    agentHandler: (mcp: MCPMessage) => Promise<MCPResponse>
): Promise<MCPResponse> {
    // Logg utgående melding
    logMCPMessage(mcpMessage, 'outgoing');

    try {
        // Valider MCP-melding
        const validation = validateMCPMessage(mcpMessage);
        if (!validation.valid) {
            return createMCPResponse(
                toAgent,
                'validation_failed',
                null,
                `MCP-validering feilet: ${validation.errors?.join(', ')}`
            );
        }

        // Kall agent
        const response = await agentHandler(mcpMessage);

        // Logg respons
        logMCPResponse(response);

        return response;

    } catch (error) {
        const errorResponse = createMCPResponse(
            toAgent,
            'error',
            null,
            `MCP-kall feilet: ${error instanceof Error ? error.message : 'Ukjent feil'}`
        );

        logMCPResponse(errorResponse);
        return errorResponse;
    }
}

// ============================================================================
// EKSPORT
// ============================================================================

// Alle interfaces og funksjoner er allerede eksportert via 'export' nøkkelordet
// over, så vi trenger ikke duplikate eksport-deklarasjoner her
