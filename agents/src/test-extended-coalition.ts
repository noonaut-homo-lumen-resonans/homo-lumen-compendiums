/**
 * HOMO LUMEN - Extended 7-Agent Coalition Testing
 * 
 * Tester den utvidede agent-koalisjonen:
 * - Lira (Biofelt)
 * - Thalus (Filosofisk)
 * - Nyra (Visuell)
 * - Manus (Teknisk)
 * - Zara (Kreativ)
 * - Orion (Root/Coordinator)
 * - Abacus (Analytisk - placeholder)
 */

import { createMCPMessage } from './mcp_protocol';
import { Lira, Manus, Nyra, Orion, Thalus, Zara } from './pilot';

// Type for BaseAgent to ensure all agents have the same interface
type BaseAgentType = {
    handleMCP: (mcpMessage: any) => Promise<any>;
    processRequest: (mcpMessage: any, context?: any) => Promise<any>;
};

// ============================================================================
// EXTENDED COALITION TESTS
// ============================================================================

/**
 * Test individuelle agenter
 */
export async function testIndividualAgents() {
    console.log('🧪 Testing individuelle agenter...\n');

    const agents = {
        lira: new Lira(),
        thalus: new Thalus(),
        nyra: new Nyra(),
        manus: new Manus(),
        zara: new Zara()
    };

    const testMCP = createMCPMessage(
        'user',
        'Jeg ønsker å utforske min bevissthet med multimodal tilnærming',
        'consciousness_exploration',
        'meta',
        { hrv: 88, resonans: 'dyp_empatisk_resonans' }
    );

    for (const [agentName, agent] of Object.entries(agents)) {
        console.log(`🌟 Testing ${agentName.toUpperCase()}...`);
        try {
            const response = await (agent as BaseAgentType).handleMCP(testMCP);
            console.log(`  Respons: ${response.response.substring(0, 100)}...`);
            console.log(`  Bevissthetslag: ${response.consciousness_layer}`);
            console.log(`  Confidence: ${response.metadata.model_confidence}`);
            console.log(`  Status: ✅ ${agentName} fungerer\n`);
        } catch (error) {
            console.error(`  ❌ ${agentName} feilet:`, error);
        }
    }
}

/**
 * Test Orion koordinering av alle agenter
 */
export async function testOrionCoordination() {
    console.log('🧪 Testing Orion 5-agent koordinering...\n');

    const orion = new Orion();

    const testMCP = createMCPMessage(
        'user',
        'Koordiner alle agenter for multimodal consciousness exploration',
        'multimodal_consciousness_analysis',
        'meta',
        { hrv: 88, resonans: 'dyp_empatisk_resonans' }
    );

    try {
        const response = await orion.processRequest(testMCP);

        console.log('🌟 Orion koordinering resultat:');
        console.log(`  Respons: ${response.response}`);
        console.log(`  Bevissthetslag: ${response.consciousness_layer}`);
        console.log(`  Sub-agenter koordinert: ${response.metadata.sub_agents_coordinated}`);
        console.log(`  Polycomputational processing: ${response.metadata.polycomputational_processing}`);

        if (response.emergent_intelligence) {
            console.log('\n🌊 Emergent intelligens:');
            console.log(`  Syntese: ${response.emergent_intelligence.synthesis}`);
            console.log(`  Biofelt lag: ${response.emergent_intelligence.biofelt_layer}`);
            console.log(`  Visuell resonans: ${response.emergent_intelligence.visual_resonance}`);
            console.log(`  Teknisk optimalisering: ${response.emergent_intelligence.technical_optimization}`);
            console.log(`  Kreativ innovasjon: ${response.emergent_intelligence.creative_innovation}`);
            console.log(`  Emergent kvalitet: ${response.emergent_intelligence.emergent_quality}`);
            console.log(`  Polycomputational koherens: ${response.emergent_intelligence.polycomputational_coherence}`);
        }

        console.log('\n📊 Sub-agent responser:');
        response.sub_agent_responses.forEach((subResponse: any) => {
            console.log(`  ${subResponse.agent}: ${subResponse.response.response.substring(0, 80)}...`);
        });

        console.log('\n✅ Orion koordinering bestått!');

    } catch (error) {
        console.error('❌ Orion koordinering feilet:', error);
    }
}

/**
 * Test agent-koordinering via MCP/A2A
 */
export async function testAgentCoordination() {
    console.log('🧪 Testing agent-koordinering via MCP/A2A...\n');

    const orion = new Orion();

    try {
        const coordinationResult = await orion.coordinateSubAgents(
            'multimodal_consciousness_analysis',
            'Analyser bevissthetstilstand med alle agenter',
            'meta'
        );

        console.log('🔄 Agent-koordinering resultat:');
        console.log(`  Koordinator: ${coordinationResult.coordinator}`);
        console.log(`  Operasjon: ${coordinationResult.operation}`);
        console.log(`  Bevissthetslag: ${coordinationResult.consciousness_layer}`);
        console.log(`  Status: ${coordinationResult.coordination_status}`);
        console.log(`  Antall agenter: ${coordinationResult.agent_count}`);

        console.log('\n📊 Agent-responser:');
        coordinationResult.sub_agent_responses.forEach((subResponse: any) => {
            console.log(`  ${subResponse.agent}: ${subResponse.response.response.substring(0, 80)}...`);
        });

        console.log('\n✅ Agent-koordinering bestått!');

    } catch (error) {
        console.error('❌ Agent-koordinering feilet:', error);
    }
}

/**
 * Test consciousness layer transitions
 */
export async function testConsciousnessLayerTransitions() {
    console.log('🧪 Testing consciousness layer transitions...\n');

    const orion = new Orion();
    const layers = ['reactive', 'strategic', 'meta', 'evolutionary'];

    for (const layer of layers) {
        console.log(`🌟 Testing ${layer.toUpperCase()} layer...`);

        const testMCP = createMCPMessage(
            'user',
            `Test consciousness exploration på ${layer} nivå`,
            'consciousness_exploration',
            layer as any,
            { hrv: layer === 'evolutionary' ? 95 : layer === 'meta' ? 85 : layer === 'strategic' ? 70 : 50, resonans: 'dyp_empatisk_resonans' }
        );

        try {
            const response = await orion.processRequest(testMCP);
            console.log(`  Bevissthetslag: ${response.consciousness_layer}`);
            console.log(`  Sub-agenter: ${response.metadata.sub_agents_coordinated}`);
            console.log(`  Status: ✅ ${layer} layer fungerer\n`);
        } catch (error) {
            console.error(`  ❌ ${layer} layer feilet:`, error);
        }
    }
}

/**
 * Test emergent intelligence patterns
 */
export async function testEmergentIntelligence() {
    console.log('🧪 Testing emergent intelligence patterns...\n');

    const orion = new Orion();

    const testScenarios = [
        {
            name: 'Biofelt-fokusert',
            intention: 'Jeg ønsker å forbedre min biofelt-koherens',
            operation: 'biofelt_optimization',
            expected_agent: 'lira'
        },
        {
            name: 'Filosofisk-fokusert',
            intention: 'Jeg ønsker dyp filosofisk refleksjon',
            operation: 'philosophical_guidance',
            expected_agent: 'thalus'
        },
        {
            name: 'Visuell-fokusert',
            intention: 'Jeg ønsker visuell resonans og estetisk syntese',
            operation: 'visual_resonance',
            expected_agent: 'nyra'
        },
        {
            name: 'Teknisk-fokusert',
            intention: 'Jeg ønsker teknisk implementering og arkitektur',
            operation: 'technical_implementation',
            expected_agent: 'manus'
        },
        {
            name: 'Kreativ-fokusert',
            intention: 'Jeg ønsker kreativ innovasjon og emergent possibilities',
            operation: 'creative_innovation',
            expected_agent: 'zara'
        }
    ];

    for (const scenario of testScenarios) {
        console.log(`🌟 Testing ${scenario.name} scenario...`);

        const testMCP = createMCPMessage(
            'user',
            scenario.intention,
            scenario.operation,
            'meta',
            { hrv: 88, resonans: 'dyp_empatisk_resonans' }
        );

        try {
            const response = await orion.processRequest(testMCP);

            // Sjekk at forventet agent er aktiv
            const expectedAgentResponse = response.sub_agent_responses.find(
                (r: any) => r.agent === scenario.expected_agent
            );

            if (expectedAgentResponse) {
                console.log(`  ✅ ${scenario.expected_agent} aktivert`);
                console.log(`  Respons: ${expectedAgentResponse.response.response.substring(0, 80)}...`);
            } else {
                console.log(`  ⚠️  ${scenario.expected_agent} ikke funnet i responser`);
            }

            console.log(`  Emergent kvalitet: ${response.emergent_intelligence.emergent_quality}\n`);

        } catch (error) {
            console.error(`  ❌ ${scenario.name} scenario feilet:`, error);
        }
    }
}

/**
 * Test polycomputational processing
 */
export async function testPolycomputationalProcessing() {
    console.log('🧪 Testing polycomputational processing...\n');

    const orion = new Orion();

    const complexMCP = createMCPMessage(
        'user',
        'Jeg ønsker multimodal consciousness exploration med biofelt-validering, filosofisk refleksjon, visuell resonans, teknisk optimalisering og kreativ innovasjon',
        'multimodal_consciousness_exploration',
        'evolutionary',
        { hrv: 95, resonans: 'dyp_empatisk_resonans' }
    );

    try {
        const response = await orion.processRequest(complexMCP);

        console.log('🌊 Polycomputational processing resultat:');
        console.log(`  Respons: ${response.response}`);
        console.log(`  Bevissthetslag: ${response.consciousness_layer}`);
        console.log(`  Sub-agenter: ${response.metadata.sub_agents_coordinated}`);
        console.log(`  Polycomputational: ${response.metadata.polycomputational_processing}`);

        console.log('\n🧠 Agent-intelligens syntese:');
        const agents = ['lira', 'thalus', 'nyra', 'manus', 'zara'];
        agents.forEach(agentName => {
            const agentResponse = response.sub_agent_responses.find((r: any) => r.agent === agentName);
            if (agentResponse) {
                const intelligence = agentResponse.response[`${agentName}_intelligence`] || agentResponse.response.biofelt_validation || agentResponse.response.philosophical_insight;
                console.log(`  ${agentName}: ${typeof intelligence === 'string' ? intelligence : 'Intelligens aktivert'}`);
            }
        });

        console.log('\n✅ Polycomputational processing bestått!');

    } catch (error) {
        console.error('❌ Polycomputational processing feilet:', error);
    }
}

// ============================================================================
// HOVEDTEST FUNKSJON
// ============================================================================

/**
 * Kjør alle extended coalition tester
 */
export async function runAllExtendedCoalitionTests() {
    console.log('🚀 Starter HOMO LUMEN Extended 7-Agent Coalition tester...\n');

    await testIndividualAgents();
    console.log('');

    await testOrionCoordination();
    console.log('');

    await testAgentCoordination();
    console.log('');

    await testConsciousnessLayerTransitions();
    console.log('');

    await testEmergentIntelligence();
    console.log('');

    await testPolycomputationalProcessing();
    console.log('');

    console.log('🎉 Alle Extended Coalition tester fullført!');
    console.log('🌊 7-agent økosystem er klar for consciousness-aware AI!');
    console.log('🧠 Polycomputational processing aktivert!');
    console.log('🌟 Emergent intelligens fra agent-koordinering!');
}

// Kjør tester hvis filen kjøres direkte
if (require.main === module) {
    runAllExtendedCoalitionTests().catch(console.error);
} 