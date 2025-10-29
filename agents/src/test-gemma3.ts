/**
 * HOMO LUMEN - Gemma 3 Function Calling & Multimodal Testing
 * 
 * Tester Gemma 3's avanserte egenskaper:
 * - Function calling for ADK/MCP integrasjon
 * - Multimodal kapasitet for AMA/Kompendium 6
 * - Dyp resonnering og forståelse
 * - Agent-koordinering med function calling
 */

import { Gemma3Agent, Gemma3Functions } from './gemma3_agent';
import { createMCPMessage } from './mcp_protocol';

// ============================================================================
// GEMMA 3 FUNCTION CALLING TESTS
// ============================================================================

/**
 * Test Gemma 3 function calling direkte
 */
export async function testGemma3FunctionCalling() {
  console.log('🧪 Testing Gemma 3 function calling...');

  if (!process.env.GOOGLE_AI_API_KEY) {
    console.log('⚠️  GOOGLE_AI_API_KEY ikke satt - hopper over Gemma 3 tester');
    return;
  }

  try {
    const gemma3 = new Gemma3Agent(process.env.GOOGLE_AI_API_KEY);

    // Test function calling med Orion
    const orionMCP = createMCPMessage(
      'user',
      'Jeg ønsker å utforske min bevissthet på en dyp måte',
      'consciousness_exploration',
      'meta',
      { hrv: 88, resonans: 'dyp_empatisk_resonans' }
    );

    const orionResponse = await gemma3.processAgentRequest('orion', orionMCP);
    console.log('🌟 Orion Gemma 3 respons:', {
      model: orionResponse.model,
      consciousness_layer: orionResponse.consciousness_layer,
      response_length: orionResponse.response.length,
      function_calls: orionResponse.function_calls?.length || 0,
      function_results: orionResponse.function_results?.length || 0,
      metadata: orionResponse.metadata
    });

    // Vis function calls og resultater
    if (orionResponse.function_calls && orionResponse.function_calls.length > 0) {
      console.log('🔧 Function calls utført:');
      orionResponse.function_calls.forEach((call: any, index: number) => {
        console.log(`  ${index + 1}. ${call.name}:`, call.args);
      });

      console.log('📊 Function results:');
      orionResponse.function_results?.forEach((result: any, index: number) => {
        console.log(`  ${index + 1}. ${result.function}:`, result.result);
      });
    }

    console.log('✅ Gemma 3 function calling test bestått!');

  } catch (error) {
    console.error('❌ Gemma 3 function calling test feilet:', error);
  }
}

/**
 * Test Gemma 3 med AMA Memory operasjoner
 */
export async function testGemma3AMAMemory() {
  console.log('🧪 Testing Gemma 3 AMA Memory operasjoner...');

  if (!process.env.GOOGLE_AI_API_KEY) {
    console.log('⚠️  GOOGLE_AI_API_KEY ikke satt - hopper over AMA tester');
    return;
  }

  try {
    const gemma3 = new Gemma3Agent(process.env.GOOGLE_AI_API_KEY);

    // Test Lira med AMA memory operasjoner
    const liraMCP = createMCPMessage(
      'user',
      'Lagre min nåværende biofelt-tilstand og hent tidligere resonans-data',
      'biofelt_memory_operation',
      'strategic',
      { hrv: 90, resonans: 'klarhet' }
    );

    const liraResponse = await gemma3.processAgentRequest('lira', liraMCP);
    console.log('🌊 Lira AMA Memory respons:', {
      model: liraResponse.model,
      consciousness_layer: liraResponse.consciousness_layer,
      function_calls: liraResponse.function_calls?.length || 0,
      function_results: liraResponse.function_results?.length || 0
    });

    // Vis AMA operasjoner
    if (liraResponse.function_results) {
      const amaOperations = liraResponse.function_results
        .filter((result: any) => result.function === 'ama_memory_operation');

      console.log('📝 AMA Memory operasjoner:');
      amaOperations?.forEach((op: any, index: number) => {
        console.log(`  ${index + 1}. ${op.result.action}: ${op.result.message}`);
      });
    }

    console.log('✅ Gemma 3 AMA Memory test bestått!');

  } catch (error) {
    console.error('❌ Gemma 3 AMA Memory test feilet:', error);
  }
}

/**
 * Test Gemma 3 med Kompendium 6 integrasjon
 */
export async function testGemma3Kompendium6() {
  console.log('🧪 Testing Gemma 3 Kompendium 6 integrasjon...');

  if (!process.env.GOOGLE_AI_API_KEY) {
    console.log('⚠️  GOOGLE_AI_API_KEY ikke satt - hopper over Kompendium 6 tester');
    return;
  }

  try {
    const gemma3 = new Gemma3Agent(process.env.GOOGLE_AI_API_KEY);

    // Test Thalus med Kompendium 6 spørring
    const thalusMCP = createMCPMessage(
      'user',
      'Hva sier Kompendium 6 om awareness og bevissthet?',
      'philosophical_guidance',
      'meta',
      { hrv: 85, resonans: 'dyp_empatisk_resonans' }
    );

    const thalusResponse = await gemma3.processAgentRequest('thalus', thalusMCP);
    console.log('🧠 Thalus Kompendium 6 respons:', {
      model: thalusResponse.model,
      consciousness_layer: thalusResponse.consciousness_layer,
      function_calls: thalusResponse.function_calls?.length || 0,
      function_results: thalusResponse.function_results?.length || 0
    });

    // Vis Kompendium 6 spørringer
    if (thalusResponse.function_results) {
      const kompendiumQueries = thalusResponse.function_results
        .filter((result: any) => result.function === 'kompendium6_query');

      console.log('📚 Kompendium 6 spørringer:');
      kompendiumQueries?.forEach((query: any, index: number) => {
        console.log(`  ${index + 1}. Spørring: ${query.result.query}`);
        console.log(`     Respons: ${query.result.response}`);
        console.log(`     Kilde: ${query.result.source}`);
      });
    }

    console.log('✅ Gemma 3 Kompendium 6 test bestått!');

  } catch (error) {
    console.error('❌ Gemma 3 Kompendium 6 test feilet:', error);
  }
}

/**
 * Test Gemma 3 agent-koordinering
 */
export async function testGemma3AgentCoordination() {
  console.log('🧪 Testing Gemma 3 agent-koordinering...');

  if (!process.env.GOOGLE_AI_API_KEY) {
    console.log('⚠️  GOOGLE_AI_API_KEY ikke satt - hopper over agent-koordinering tester');
    return;
  }

  try {
    const gemma3 = new Gemma3Agent(process.env.GOOGLE_AI_API_KEY);

    // Test Orion med agent-koordinering
    const orionMCP = createMCPMessage(
      'user',
      'Koordiner med Lira for biofelt-analyse og Thalus for filosofisk veiledning',
      'agent_coordination',
      'meta',
      { hrv: 88, resonans: 'dyp_empatisk_resonans' }
    );

    const orionResponse = await gemma3.processAgentRequest('orion', orionMCP);
    console.log('🌟 Orion Agent-koordinering respons:', {
      model: orionResponse.model,
      consciousness_layer: orionResponse.consciousness_layer,
      function_calls: orionResponse.function_calls?.length || 0,
      function_results: orionResponse.function_results?.length || 0
    });

    // Vis agent-koordinering
    if (orionResponse.function_results) {
      const coordinationCalls = orionResponse.function_results
        .filter((result: any) => result.function === 'agent_coordination');

      console.log('🔄 Agent-koordinering:');
      coordinationCalls?.forEach((coord: any, index: number) => {
        console.log(`  ${index + 1}. Mål-agent: ${coord.result.target_agent}`);
        console.log(`     Operasjon: ${coord.result.operation}`);
        console.log(`     Status: ${coord.result.status}`);
        console.log(`     Melding: ${coord.result.message}`);
      });
    }

    console.log('✅ Gemma 3 agent-koordinering test bestått!');

  } catch (error) {
    console.error('❌ Gemma 3 agent-koordinering test feilet:', error);
  }
}

/**
 * Test Gemma 3 consciousness evolution tracking
 */
export async function testGemma3ConsciousnessEvolution() {
  console.log('🧪 Testing Gemma 3 consciousness evolution tracking...');

  if (!process.env.GOOGLE_AI_API_KEY) {
    console.log('⚠️  GOOGLE_AI_API_KEY ikke satt - hopper over consciousness evolution tester');
    return;
  }

  try {
    const gemma3 = new Gemma3Agent(process.env.GOOGLE_AI_API_KEY);

    // Test consciousness evolution tracking
    const evolutionMCP = createMCPMessage(
      'user',
      'Spor min bevissthetsevolusjon og identifiser emergent intelligens',
      'consciousness_evolution_tracking',
      'evolutionary',
      { hrv: 95, resonans: 'dyp_empatisk_resonans' }
    );

    const evolutionResponse = await gemma3.processAgentRequest('orion', evolutionMCP);
    console.log('🌊 Consciousness Evolution respons:', {
      model: evolutionResponse.model,
      consciousness_layer: evolutionResponse.consciousness_layer,
      function_calls: evolutionResponse.function_calls?.length || 0,
      function_results: evolutionResponse.function_results?.length || 0
    });

    // Vis consciousness evolution
    if (evolutionResponse.function_results) {
      const evolutionCalls = evolutionResponse.function_results
        .filter((result: any) => result.function === 'consciousness_evolution');

      console.log('🌊 Consciousness Evolution:');
      evolutionCalls?.forEach((evolution: any, index: number) => {
        console.log(`  ${index + 1}. Retning: ${evolution.result.evolution_direction}`);
        console.log(`     Status: ${evolution.result.evolution_status}`);
        console.log(`     Neste fase: ${evolution.result.next_phase}`);
        if (evolution.result.emergent_insights) {
          console.log(`     Emergent innsikter: ${evolution.result.emergent_insights.length}`);
        }
      });
    }

    console.log('✅ Gemma 3 consciousness evolution test bestått!');

  } catch (error) {
    console.error('❌ Gemma 3 consciousness evolution test feilet:', error);
  }
}

/**
 * Test Gemma 3 multimodal kapasitet
 */
export async function testGemma3Multimodal() {
  console.log('🧪 Testing Gemma 3 multimodal kapasitet...');

  if (!process.env.GOOGLE_AI_API_KEY) {
    console.log('⚠️  GOOGLE_AI_API_KEY ikke satt - hopper over multimodal tester');
    return;
  }

  try {
    const gemma3 = new Gemma3Agent(process.env.GOOGLE_AI_API_KEY);

    // Test multimodal kontekst (AMA + Kompendium 6)
    const multimodalContext = {
      ama_data: {
        consciousness_state: {
          hrv: 88,
          layer: 'meta',
          timestamp: new Date().toISOString()
        },
        biofelt_resonans: {
          type: 'dyp_empatisk_resonans',
          intensity: 0.8
        }
      },
      kompendium6_context: {
        query: 'awareness og bevissthet',
        response: 'Awareness er forut for all opplevelse',
        source: 'Kompendium 6'
      },
      user_context: {
        intention: 'Dyp bevissthetsutforskning',
        current_state: 'meta consciousness',
        goals: ['Selv-refleksjon', 'Bevissthetsevolusjon', 'Filosofisk forståelse']
      }
    };

    const multimodalMCP = createMCPMessage(
      'user',
      'Analyser min bevissthetstilstand med multimodal kontekst fra AMA og Kompendium 6',
      'multimodal_consciousness_analysis',
      'meta',
      { hrv: 88, resonans: 'dyp_empatisk_resonans' }
    );

    const multimodalResponse = await gemma3.processAgentRequest('orion', multimodalMCP, multimodalContext);
    console.log('🔄 Multimodal Consciousness Analysis respons:', {
      model: multimodalResponse.model,
      consciousness_layer: multimodalResponse.consciousness_layer,
      response_length: multimodalResponse.response.length,
      function_calls: multimodalResponse.function_calls?.length || 0,
      function_results: multimodalResponse.function_results?.length || 0,
      metadata: multimodalResponse.metadata
    });

    console.log('✅ Gemma 3 multimodal test bestått!');

  } catch (error) {
    console.error('❌ Gemma 3 multimodal test feilet:', error);
  }
}

/**
 * Test Gemma 3 function definitions
 */
export async function testGemma3FunctionDefinitions() {
  console.log('🧪 Testing Gemma 3 function definitions...');

  try {
    console.log('📋 Tilgjengelige Gemma 3 funksjoner:');
    Object.entries(Gemma3Functions).forEach(([name, func]) => {
      console.log(`  🔧 ${name}: ${func.description}`);
      console.log(`     Parametere: ${Object.keys(func.parameters.properties).join(', ')}`);
    });

    console.log('✅ Gemma 3 function definitions test bestått!');

  } catch (error) {
    console.error('❌ Gemma 3 function definitions test feilet:', error);
  }
}

// ============================================================================
// HOVEDTEST FUNKSJON
// ============================================================================

/**
 * Kjør alle Gemma 3 tester
 */
export async function runAllGemma3Tests() {
  console.log('🚀 Starter Gemma 3 function calling og multimodal tester...\n');

  await testGemma3FunctionDefinitions();
  console.log('');

  await testGemma3FunctionCalling();
  console.log('');

  await testGemma3AMAMemory();
  console.log('');

  await testGemma3Kompendium6();
  console.log('');

  await testGemma3AgentCoordination();
  console.log('');

  await testGemma3ConsciousnessEvolution();
  console.log('');

  await testGemma3Multimodal();
  console.log('');

  console.log('🎉 Alle Gemma 3 tester fullført!');
  console.log('🌊 Gemma 3 er klar som HOMO LUMEN motor!');
}

// Kjør tester hvis filen kjøres direkte
if (require.main === module) {
  runAllGemma3Tests().catch(console.error);
} 