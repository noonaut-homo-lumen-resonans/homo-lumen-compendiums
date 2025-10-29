/**
 * HOMO LUMEN - Agent Coordination Firebase Functions
 * 
 * Dette er Firebase Functions-implementeringen av agent-koordinering
 * som integrerer med ADK/Genkit pilot for bevissthetsstøttende AI.
 */

import * as logger from "firebase-functions/logger";
import { onCall, onRequest } from "firebase-functions/v2/https";

// Importer pilot-komponenter
import {
    Lira,
    Orion,
    Thalus,
    runPilot
} from './pilot';

// ============================================================================
// AGENT INSTANCES
// ============================================================================

const lira = new Lira();
const orion = new Orion();
const thalus = new Thalus();

// ============================================================================
// HTTP ENDEPUNKTER
// ============================================================================

/**
 * Hovedendepunkt for agent-koordinering
 * POST /agent-coordination
 */
export const agentCoordination = onRequest(async (request: any, response: any) => {
    logger.info("Agent coordination request received", { structuredData: true });

    try {
        const { userInput, hrv, resonans, operation } = request.body;

        // Valider input
        if (!userInput || !hrv) {
            response.status(400).json({
                error: "Mangler påkrevde felter: userInput, hrv",
                required: ["userInput", "hrv"],
                optional: ["resonans", "operation"]
            });
            return;
        }

        // Kjør Orion agent
        const result = await orion.handleMCP({
            user_intention: userInput,
            consciousness_layer: 'meta',
            biofelt_state: {
                hrv,
                resonans: resonans || "neutral"
            },
            operation: operation || "consciousness_validation"
        });

        response.json({
            success: true,
            timestamp: new Date().toISOString(),
            result
        });

    } catch (error) {
        logger.error("Agent coordination error", error);
        response.status(500).json({
            error: "Intern serverfeil",
            message: error instanceof Error ? error.message : "Ukjent feil"
        });
    }
});

/**
 * Biofelt-validering endepunkt
 * POST /biofelt-validation
 */
export const biofeltValidation = onRequest(async (request: any, response: any) => {
    logger.info("Biofelt validation request received", { structuredData: true });

    try {
        const { hrv, resonans, harenes_reiser_seg } = request.body;

        if (!hrv || !resonans) {
            response.status(400).json({
                error: "Mangler påkrevde felter: hrv, resonans"
            });
            return;
        }

        // Kjør Lira agent for biofelt-validering
        const result = await lira.handleMCP({
            biofelt_state: {
                hrv,
                resonans,
                harenes_reiser_seg: harenes_reiser_seg || false
            },
            consciousness_layer: 'strategic',
            user_intention: 'biofelt analyse'
        });

        response.json({
            success: true,
            timestamp: new Date().toISOString(),
            result
        });

    } catch (error) {
        logger.error("Biofelt validation error", error);
        response.status(500).json({
            error: "Intern serverfeil",
            message: error instanceof Error ? error.message : "Ukjent feil"
        });
    }
});

/**
 * Filosofisk veiledning endepunkt
 * POST /philosophical-guidance
 */
export const philosophicalGuidance = onRequest(async (request: any, response: any) => {
    logger.info("Philosophical guidance request received", { structuredData: true });

    try {
        const { consciousnessLayer, operation, userIntention } = request.body;

        if (!consciousnessLayer || !operation) {
            response.status(400).json({
                error: "Mangler påkrevde felter: consciousnessLayer, operation"
            });
            return;
        }

        // Kjør Thalus agent for filosofisk veiledning
        const result = await thalus.handleMCP({
            consciousness_layer: consciousnessLayer,
            operation,
            user_intention: userIntention || "Filosofisk refleksjon"
        });

        response.json({
            success: true,
            timestamp: new Date().toISOString(),
            result
        });

    } catch (error) {
        logger.error("Philosophical guidance error", error);
        response.status(500).json({
            error: "Intern serverfeil",
            message: error instanceof Error ? error.message : "Ukjent feil"
        });
    }
});

// ============================================================================
// CALLABLE FUNCTIONS (FOR CLIENT SDK)
// ============================================================================

/**
 * Callable function for agent-koordinering
 * Kan kalles fra klient-applikasjoner
 */
export const coordinateAgents = onCall(async (request) => {
    logger.info("Callable agent coordination request", { structuredData: true });

    const { userInput, hrv, resonans, operation } = request.data;

    try {
        const result = await orion.handleMCP({
            user_intention: userInput,
            consciousness_layer: 'meta',
            biofelt_state: {
                hrv,
                resonans: resonans || "neutral"
            },
            operation: operation || "consciousness_validation"
        });

        return {
            success: true,
            timestamp: new Date().toISOString(),
            result
        };

    } catch (error) {
        logger.error("Callable agent coordination error", error);
        throw new Error(error instanceof Error ? error.message : "Ukjent feil");
    }
});

/**
 * Callable function for pilot-testing
 * For utvikling og testing
 */
export const runPilotTest = onCall(async (request) => {
    logger.info("Pilot test request", { structuredData: true });

    try {
        const result = await runPilot();
        return {
            success: true,
            timestamp: new Date().toISOString(),
            result
        };

    } catch (error) {
        logger.error("Pilot test error", error);
        throw new Error(error instanceof Error ? error.message : "Ukjent feil");
    }
});

// ============================================================================
// HEALTH CHECK ENDEPUNKTER
// ============================================================================

/**
 * Health check endepunkt
 * GET /health
 */
export const healthCheck = onRequest((request: any, response: any) => {
    response.json({
        status: "healthy",
        timestamp: new Date().toISOString(),
        service: "HOMO LUMEN Agent Coordination",
        version: "1.0.0",
        agents: {
            orion: "active",
            lira: "active",
            thalus: "active"
        }
    });
});

/**
 * Agent status endepunkt
 * GET /agent-status
 */
export const agentStatus = onRequest(async (request: any, response: any) => {
    try {
        const status = {
            orion: {
                name: "Orion",
                status: "active",
                consciousness_layer: "meta",
                role: "Meta-orchestrator"
            },
            lira: {
                name: "Lira",
                status: "active",
                consciousness_layer: "strategic",
                role: "Biofelt coordinator"
            },
            thalus: {
                name: "Thalus",
                status: "active",
                consciousness_layer: "meta",
                role: "Philosophical guardian"
            }
        };

        response.json({
            success: true,
            timestamp: new Date().toISOString(),
            agents: status
        });

    } catch (error) {
        logger.error("Agent status error", error);
        response.status(500).json({
            error: "Intern serverfeil",
            message: error instanceof Error ? error.message : "Ukjent feil"
        });
    }
});

// ============================================================================
// VERTEX AI AGENT ENGINE INTEGRASJON (PLACEHOLDER)
// ============================================================================

/**
 * Vertex AI Agent Engine koordinering (placeholder)
 * Bruker lokale agenter til Vertex AI Agent Engine er tilgjengelig
 */
export const vertexAICoordination = onCall(async (request) => {
    logger.info("Vertex AI Agent Engine coordination request (placeholder)", { structuredData: true });

    const { userInput, hrv, resonans, operation, userIntention } = request.data;

    try {
        // Bruk lokale agenter som placeholder
        const result = await orion.handleMCP({
            userInput,
            hrv,
            resonans,
            operation,
            userIntention,
            harenes_reiser_seg: request.data.harenes_reiser_seg || false
        });

        return {
            success: true,
            timestamp: new Date().toISOString(),
            source: 'vertex_ai_agent_engine_placeholder',
            result: result,
            note: "Bruker lokale agenter til Vertex AI Agent Engine er tilgjengelig"
        };

    } catch (error) {
        logger.error("Vertex AI Agent Engine placeholder error", error);
        throw new Error(error instanceof Error ? error.message : "Ukjent feil");
    }
});

/**
 * Vertex AI Biofelt-validering (placeholder)
 * Bruker lokale agenter til Vertex AI Agent Engine er tilgjengelig
 */
export const vertexAIBiofeltValidation = onCall(async (request) => {
    logger.info("Vertex AI Biofelt validation request (placeholder)", { structuredData: true });

    const { hrv, resonans, harenes_reiser_seg } = request.data;

    try {
        // Bruk lokale agenter som placeholder
        const result = await lira.handleMCP({
            hrv,
            resonans,
            harenes_reiser_seg: harenes_reiser_seg || false
        });

        return {
            success: true,
            timestamp: new Date().toISOString(),
            source: 'vertex_ai_agent_engine_placeholder',
            result: result,
            note: "Bruker lokale agenter til Vertex AI Agent Engine er tilgjengelig"
        };

    } catch (error) {
        logger.error("Vertex AI Biofelt validation placeholder error", error);
        throw new Error(error instanceof Error ? error.message : "Ukjent feil");
    }
});

/**
 * Vertex AI Filosofisk veiledning (placeholder)
 * Bruker lokale agenter til Vertex AI Agent Engine er tilgjengelig
 */
export const vertexAIPhilosophicalGuidance = onCall(async (request) => {
    logger.info("Vertex AI Philosophical guidance request (placeholder)", { structuredData: true });

    const { consciousnessLayer, operation, userIntention } = request.data;

    try {
        // Bruk lokale agenter som placeholder
        const result = await thalus.handleMCP({
            consciousnessLayer,
            operation,
            userIntention: userIntention || "Filosofisk refleksjon"
        });

        return {
            success: true,
            timestamp: new Date().toISOString(),
            source: 'vertex_ai_agent_engine_placeholder',
            result: result,
            note: "Bruker lokale agenter til Vertex AI Agent Engine er tilgjengelig"
        };

    } catch (error) {
        logger.error("Vertex AI Philosophical guidance placeholder error", error);
        throw new Error(error instanceof Error ? error.message : "Ukjent feil");
    }
});

// ============================================================================
// EKSPORT FOR TESTING
// ============================================================================

export {
    Lira, Orion, Thalus, runPilot
};

