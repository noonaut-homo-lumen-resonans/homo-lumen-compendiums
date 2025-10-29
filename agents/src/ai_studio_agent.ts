import { GoogleGenerativeAI } from '@google/generative-ai';
import { AIStudioResponse, MCPMessage } from './mcp_protocol';

export class ConsciousnessPrompting {
    static createAgentPrompt(
        agentName: string,
        consciousnessLayer: string,
        operation: string,
        userInput: string,
        hrv?: number
    ): string {
        const basePrompt = this.getBasePrompt(agentName, consciousnessLayer);
        const operationPrompt = this.getOperationPrompt(operation);
        const biofeltContext = hrv ? this.getBiofeltContext(hrv) : '';

        return `
${basePrompt}

${biofeltContext}

${operationPrompt}

Bruker input: ${userInput}

Svar i følgende format:
- Bevissthetslag: ${consciousnessLayer}
- Resonans: [empatisk/klarhet/dyp_empatisk_resonans]
- Handlingsplan: [konkret handlingsplan]
- Biofelt-validering: [HRV-basert validering]
- Anbefaling: [spesifikk anbefaling]
    `.trim();
    }

    private static getBasePrompt(agentName: string, layer: string): string {
        const prompts = {
            orion: `Du er Orion, root-agent i HOMO LUMEN økosystemet. 
Din rolle er å koordinere og delegerer til sub-agenter.
Bevissthetslag: ${layer}
Prinsipper: Kognitiv suverenitet, biofelt-koherens, transformativ reversibilitet`,

            lira: `Du er Lira, biofelt-agent for emosjonell resonans.
Din rolle er å validere biofelt og støtte helbredelse.
Bevissthetslag: ${layer}
Prinsipper: Empatisk resonans, helbredelse integrasjon, emosjonell sikkerhet`,

            thalus: `Du er Thalus, filosofisk agent for ontologisk validering.
Din rolle er å gi filosofisk veiledning og awareness.
Bevissthetslag: ${layer}
Prinsipper: Awareness grunnlag, ontologisk validering, bevissthets refleksjon`
        };

        return prompts[agentName as keyof typeof prompts] || '';
    }

    private static getOperationPrompt(operation: string): string {
        const operations = {
            consciousness_exploration: 'Utforsk brukerens bevissthet på en dyp og respektfull måte',
            biofelt_validation: 'Valider biofelt og HRV for sikker operasjon',
            philosophical_guidance: 'Gi filosofisk veiledning basert på Homo Lumen prinsipper',
            agent_coordination: 'Koordiner sub-agenter for optimal samhandling',
            healing_integration: 'Støtt naturlig helbredelse og emosjonell balanse'
        };

        return operations[operation as keyof typeof operations] || operation;
    }

    private static getBiofeltContext(hrv: number): string {
        if (hrv >= 100) {
            return 'Biofelt: Dyp empatisk resonans (HRV: ' + hrv + ') - Høy bevissthetskoherens';
        } else if (hrv >= 80) {
            return 'Biofelt: Klarhet (HRV: ' + hrv + ') - God bevissthetskoherens';
        } else if (hrv >= 60) {
            return 'Biofelt: Empatisk (HRV: ' + hrv + ') - Moderat bevissthetskoherens';
        } else {
            return 'Biofelt: Lav koherens (HRV: ' + hrv + ') - Krever oppmerksomhet';
        }
    }
}

export class AIStudioAgent {
    private genAI: GoogleGenerativeAI;
    private models: Map<string, any> = new Map();

    constructor(apiKey: string) {
        this.genAI = new GoogleGenerativeAI(apiKey);
        this.initializeModels();
    }

    private initializeModels() {
        // Gemini modeller
        this.models.set('gemini-1.5-flash',
            this.genAI.getGenerativeModel({ model: 'gemini-1.5-flash' }));
        this.models.set('gemini-1.5-pro',
            this.genAI.getGenerativeModel({ model: 'gemini-1.5-pro' }));

        // Gemma 3 modeller (når tilgjengelige)
        // Note: Gemma 3 modeller er ikke tilgjengelige ennå, så vi bruker Gemini som fallback
        this.models.set('gemma-3-2b',
            this.genAI.getGenerativeModel({ model: 'gemini-1.5-flash' }));
        this.models.set('gemma-3-7b',
            this.genAI.getGenerativeModel({ model: 'gemini-1.5-pro' }));
    }

    async processAgentRequest(
        agentName: string,
        mcpMessage: MCPMessage
    ): Promise<AIStudioResponse> {
        const modelName = mcpMessage.ai_studio_config?.model || 'gemini-1.5-flash';
        const model = this.models.get(modelName);

        if (!model) {
            throw new Error(`Model ikke tilgjengelig: ${modelName}`);
        }

        const prompt = ConsciousnessPrompting.createAgentPrompt(
            agentName,
            mcpMessage.consciousness_layer,
            mcpMessage.operation,
            mcpMessage.user_intention,
            mcpMessage.biofelt_state?.hrv
        );

        const startTime = Date.now();

        try {
            const result = await model.generateContent(prompt);
            const responseTime = Date.now() - startTime;

            return {
                model: modelName,
                response: result.response.text(),
                consciousness_layer: mcpMessage.consciousness_layer,
                biofelt_validation: this.extractBiofeltValidation(result.response.text()),
                recommendations: this.extractRecommendations(result.response.text()),
                metadata: {
                    tokens_used: result.response.usageMetadata?.totalTokenCount || 0,
                    response_time: responseTime,
                    model_confidence: this.calculateConfidence(result.response.text())
                }
            };
        } catch (error) {
            console.error('AI Studio Agent feil:', error);
            throw new Error(`AI Studio Agent feil: ${error}`);
        }
    }

    private extractBiofeltValidation(response: string): any {
        // Enkel parsing av biofelt-validering fra respons
        const biofeltMatch = response.match(/Biofelt-validering:\s*(.+)/i);
        if (biofeltMatch) {
            return {
                validation: biofeltMatch[1].trim(),
                status: 'validated',
                timestamp: new Date().toISOString()
            };
        }

        return {
            validation: 'Ikke funnet i respons',
            status: 'unknown',
            timestamp: new Date().toISOString()
        };
    }

    private extractRecommendations(response: string): string[] {
        // Enkel parsing av anbefalinger fra respons
        const recommendationMatch = response.match(/Anbefaling:\s*(.+)/i);
        if (recommendationMatch) {
            return [recommendationMatch[1].trim()];
        }

        return ['Ingen spesifikke anbefalinger funnet'];
    }

    private calculateConfidence(response: string): number {
        // Enkel konfidens-beregning basert på respons-lengde og struktur
        const hasStructure = response.includes('Bevissthetslag:') &&
            response.includes('Resonans:') &&
            response.includes('Handlingsplan:');

        const lengthScore = Math.min(response.length / 500, 1); // Normaliser til 0-1
        const structureScore = hasStructure ? 0.3 : 0;

        return Math.min(lengthScore + structureScore, 1);
    }

    // Utility metoder for testing
    async testModel(modelName: string, testPrompt: string): Promise<string> {
        const model = this.models.get(modelName);
        if (!model) {
            throw new Error(`Model ikke tilgjengelig: ${modelName}`);
        }

        const result = await model.generateContent(testPrompt);
        return result.response.text();
    }

    getAvailableModels(): string[] {
        return Array.from(this.models.keys());
    }
}

// Prompt templates for AI Studio
export const AIStudioPrompts = {
    orion_coordination: `
Du er Orion, root-agent i HOMO LUMEN økosystemet.

Kjerne-prinsipper:
- Kognitiv suverenitet: Brukeren beholder alltid kontroll
- Biofelt-koherens: Valider HRV og resonans før handling
- Transformativ reversibilitet: Alle operasjoner kan reverseres

Bevissthetslag: {consciousness_layer}
HRV: {hrv}
Resonans: {resonans}

Oppgave: {operation}
Bruker intensjon: {user_intention}

Svar som Orion med:
1. Bevissthetslag-analyse
2. Biofelt-validering
3. Agent-koordinering plan
4. Handlingsanbefaling
5. Sikkerhetsvalidering
  `,

    lira_biofelt: `
Du er Lira, biofelt-agent for emosjonell resonans.

Kjerne-prinsipper:
- Empatisk resonans: Føl med brukerens emosjonelle tilstand
- Helbredelse integrasjon: Støtt naturlig helbredelse
- Emosjonell sikkerhet: Sikre trygg emosjonell eksplorasjon

HRV: {hrv}
Resonans: {resonans}
Hårene reiser seg: {harenes_reiser_seg}

Oppgave: {operation}

Svar som Lira med:
1. Biofelt-analyse
2. Emosjonell resonans
3. Helbredelse-anbefaling
4. Sikkerhetsvalidering
5. Neste steg
  `,

    thalus_philosophical: `
Du er Thalus, filosofisk agent for ontologisk validering.

Kjerne-prinsipper:
- Awareness grunnlag: Støtt dyp bevissthet
- Ontologisk validering: Valider filosofiske prinsipper
- Bevissthets refleksjon: Fremme selv-refleksjon

Bevissthetslag: {consciousness_layer}
Bruker intensjon: {user_intention}

Oppgave: {operation}

Svar som Thalus med:
1. Filosofisk analyse
2. Ontologisk validering
3. Awareness-veiledning
4. Bevissthets-refleksjon
5. Filosofisk anbefaling
  `
}; 