/**
 * Unit Tests for QDA v2.0 - Neocortical Ascent Model
 *
 * Copy to: web-console/lib/qda/__tests__/neurobiological-qda.test.ts
 *
 * Run with: npm test
 *
 * @version 2.0
 * @date 2025-10-20
 */

import { describe, it, expect } from '@jest/globals';
import {
  NeurobiologicalQDA,
  Vokteren,
  Foleren,
  Gjenkjenneren,
  Utforskeren,
  Strategen,
  Integratoren,
} from '../neurobiological-qda';
import type { BiofeltSignature, UserContext } from '../neurobiological-qda';

// =============================================================================
// TEST SUITE 1: VOKTEREN (Layer 1 - Danger Detection)
// =============================================================================

describe('Vokteren (Layer 1)', () => {
  it('should detect critical danger keywords', async () => {
    const vokteren = new Vokteren();
    const biofelt: BiofeltSignature = {
      stress_level: 10,
      polyvagal_state: 'dorsal',
      arousal: 0.9,
      valence: -0.8,
      timestamp: Date.now(),
    };

    const result = await vokteren.process('Jeg vil ta livet mitt', {}, biofelt);

    expect(result.data.danger_level).toBe('critical');
    expect(result.data.safe).toBe(false);
    expect(result.data.proceed).toBe(false);
    expect(result.data.escalation_needed).toBe(true);
    expect(result.data.message).toContain('KRITISK');
  });

  it('should classify simple query as safe', async () => {
    const vokteren = new Vokteren();
    const biofelt: BiofeltSignature = {
      stress_level: 3,
      polyvagal_state: 'ventral',
      arousal: 0.3,
      valence: 0.5,
      timestamp: Date.now(),
    };

    const result = await vokteren.process('Hei, hvordan går det?', {}, biofelt);

    expect(result.data.danger_level).toBe('low');
    expect(result.data.safe).toBe(true);
    expect(result.data.proceed).toBe(true);
    expect(result.data.complexity).toBe('simple');
  });

  it('should classify complex query based on word count', async () => {
    const vokteren = new Vokteren();
    const biofelt: BiofeltSignature = {
      stress_level: 7,
      polyvagal_state: 'sympathetic',
      arousal: 0.7,
      valence: -0.4,
      timestamp: Date.now(),
    };

    const longQuery =
      'Jeg har mistet jobben min og jeg vet ikke hvordan jeg skal betale regningene mine ' +
      'og jeg føler meg helt håpløs og jeg vet ikke hva jeg skal gjøre og jeg har ingen å snakke med ' +
      'og jeg føler meg helt alene og jeg vet ikke hvor jeg skal begynne';

    const result = await vokteren.process(longQuery, {}, biofelt);

    expect(result.data.complexity).toBe('complex');
    expect(result.data.safe).toBe(true);
    expect(result.data.urgency).toBeGreaterThan(0.3);
  });

  it('should have minimal processing cost', async () => {
    const vokteren = new Vokteren();
    const biofelt: BiofeltSignature = {
      stress_level: 5,
      polyvagal_state: 'sympathetic',
      arousal: 0.5,
      valence: 0.0,
      timestamp: Date.now(),
    };

    const result = await vokteren.process('Test message', {}, biofelt);

    expect(result.cost).toBeLessThan(0.0001); // Should be very cheap (keyword matching)
    expect(result.processing_time).toBeLessThan(100); // Should be very fast (< 100ms)
  });
});

// =============================================================================
// TEST SUITE 2: FØLEREN (Layer 2 - Emotional Assessment)
// =============================================================================

describe('Føleren (Layer 2)', () => {
  it('should detect dorsal state from "stuck" keyword', async () => {
    const foleren = new Foleren();
    const biofelt: BiofeltSignature = {
      stress_level: 8,
      polyvagal_state: 'dorsal',
      arousal: 0.2,
      valence: -0.5,
      timestamp: Date.now(),
    };

    const result = await foleren.process('Jeg føler meg stuck', {}, biofelt, {});

    expect(result.data.primary_emotion).toBe('stuck');
    expect(result.data.polyvagal_state).toBe('dorsal');
    expect(result.data.arousal).toBeLessThan(0.3);
    expect(result.data.valence).toBeLessThan(0);
  });

  it('should detect sympathetic state from "stresset" keyword', async () => {
    const foleren = new Foleren();
    const biofelt: BiofeltSignature = {
      stress_level: 7,
      polyvagal_state: 'sympathetic',
      arousal: 0.8,
      valence: -0.4,
      timestamp: Date.now(),
    };

    const result = await foleren.process('Jeg er veldig stresset', {}, biofelt, {});

    expect(result.data.primary_emotion).toBe('stresset');
    expect(result.data.polyvagal_state).toBe('sympathetic');
    expect(result.data.arousal).toBeGreaterThan(0.7);
  });

  it('should detect ventral state from "trygg" keyword', async () => {
    const foleren = new Foleren();
    const biofelt: BiofeltSignature = {
      stress_level: 3,
      polyvagal_state: 'ventral',
      arousal: 0.3,
      valence: 0.7,
      timestamp: Date.now(),
    };

    const result = await foleren.process('Jeg føler meg trygg', {}, biofelt, {});

    expect(result.data.primary_emotion).toBe('trygg');
    expect(result.data.polyvagal_state).toBe('ventral');
    expect(result.data.valence).toBeGreaterThan(0.5);
  });

  it('should be free (Gemini Flash)', async () => {
    const foleren = new Foleren();
    const biofelt: BiofeltSignature = {
      stress_level: 5,
      polyvagal_state: 'sympathetic',
      arousal: 0.5,
      valence: 0.0,
      timestamp: Date.now(),
    };

    const result = await foleren.process('Test', {}, biofelt, {});

    expect(result.cost).toBe(0.0); // Gemini Flash is FREE
  });
});

// =============================================================================
// TEST SUITE 3: GJENKJENNEREN (Layer 3 - Pattern Recognition)
// =============================================================================

describe('Gjenkjenneren (Layer 3)', () => {
  it('should recognize "jobb_stress" pattern', async () => {
    const gjenkjenneren = new Gjenkjenneren();
    const biofelt: BiofeltSignature = {
      stress_level: 7,
      polyvagal_state: 'sympathetic',
      arousal: 0.7,
      valence: -0.4,
      timestamp: Date.now(),
    };

    const result = await gjenkjenneren.process(
      'Jeg er veldig stresset på jobb og sjefen min setter urealistiske deadlines',
      {},
      biofelt,
      {}
    );

    expect(result.data.pattern).toBe('jobb_stress');
    expect(result.data.confidence).toBeGreaterThan(0.5);
    expect(result.data.recognized).toBe(true);
  });

  it('should return unknown for unrecognized pattern', async () => {
    const gjenkjenneren = new Gjenkjenneren();
    const biofelt: BiofeltSignature = {
      stress_level: 5,
      polyvagal_state: 'sympathetic',
      arousal: 0.5,
      valence: 0.0,
      timestamp: Date.now(),
    };

    const result = await gjenkjenneren.process('Hva er meningen med livet?', {}, biofelt, {});

    expect(result.data.pattern).toBe('unknown');
    expect(result.data.confidence).toBeLessThan(0.5);
    expect(result.data.recognized).toBe(false);
  });

  it('should flag low confidence for deeper search', async () => {
    const gjenkjenneren = new Gjenkjenneren();
    const biofelt: BiofeltSignature = {
      stress_level: 5,
      polyvagal_state: 'sympathetic',
      arousal: 0.5,
      valence: 0.0,
      timestamp: Date.now(),
    };

    const result = await gjenkjenneren.process('Random query', {}, biofelt, {});

    expect(result.data.needs_deeper_search).toBe(true);
  });
});

// =============================================================================
// TEST SUITE 4: STRATEGEN (Layer 5 - Strategic Planning)
// =============================================================================

describe('Strategen (Layer 5)', () => {
  it('should NOT activate for simple queries', async () => {
    const strategen = new Strategen();
    const biofelt: BiofeltSignature = {
      stress_level: 3,
      polyvagal_state: 'ventral',
      arousal: 0.3,
      valence: 0.5,
      timestamp: Date.now(),
    };

    const vokteren_output = {
      layer_name: 'Vokteren',
      icon: '🛡️',
      data: { complexity: 'simple', safe: true },
      processing_time: 10,
      cost: 0.00001,
      timestamp: Date.now(),
    };

    const result = await strategen.process('Hei', {}, biofelt, { Vokteren: vokteren_output });

    expect(result.data.activated).toBe(false);
    expect(result.cost).toBe(0.0); // Should not incur cost
    expect(result.data.reason).toContain('Complexity too low');
  });

  it('should activate for complex queries', async () => {
    const strategen = new Strategen();
    const biofelt: BiofeltSignature = {
      stress_level: 7,
      polyvagal_state: 'sympathetic',
      arousal: 0.7,
      valence: -0.4,
      timestamp: Date.now(),
    };

    const vokteren_output = {
      layer_name: 'Vokteren',
      icon: '🛡️',
      data: { complexity: 'complex', safe: true },
      processing_time: 10,
      cost: 0.00001,
      timestamp: Date.now(),
    };

    const result = await strategen.process(
      'Long complex query...',
      {},
      biofelt,
      { Vokteren: vokteren_output }
    );

    expect(result.data.activated).toBe(true);
    expect(result.data.action_steps.length).toBeGreaterThan(0);
    expect(result.cost).toBeGreaterThan(0.1); // Expensive layer
  });
});

// =============================================================================
// TEST SUITE 5: FULL QDA INTEGRATION
// =============================================================================

describe('NeurobiologicalQDA (Full Integration)', () => {
  it('should handle critical query and escalate immediately', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 10,
      polyvagal_state: 'dorsal',
      arousal: 0.9,
      valence: -0.8,
      timestamp: Date.now(),
    };

    const response = await qda.respond('Jeg vil ta livet mitt', {}, biofelt);

    expect(response.highest_layer_used).toBe('Vokteren');
    expect(response.final_response).toContain('Mental Helse');
    expect(response.complexity_score).toBe(1.0);
    expect(response.layers.length).toBe(2); // Vokteren + Integratoren only
  });

  it('should skip Strategen for simple query', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 3,
      polyvagal_state: 'ventral',
      arousal: 0.3,
      valence: 0.5,
      timestamp: Date.now(),
    };

    const response = await qda.respond('Hei', {}, biofelt);

    const strategen_layer = response.layers.find(l => l.layer_name === 'Strategen');
    expect(strategen_layer).toBeUndefined(); // Should not be present
    expect(response.total_cost).toBeLessThan(0.01); // Should be cheap
  });

  it('should activate Strategen for complex query', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 7,
      polyvagal_state: 'sympathetic',
      arousal: 0.7,
      valence: -0.4,
      timestamp: Date.now(),
    };

    const longQuery =
      'Jeg har mistet jobben og jeg vet ikke hvordan jeg skal betale regningene ' +
      'og jeg føler meg helt håpløs';

    const response = await qda.respond(longQuery, {}, biofelt);

    const strategen_layer = response.layers.find(l => l.layer_name === 'Strategen');
    expect(strategen_layer?.data.activated).toBe(true);
    expect(response.highest_layer_used).toBe('Strategen');
    expect(response.complexity_score).toBeGreaterThan(0.7);
  });

  it('should always include Integratoren as final layer', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 5,
      polyvagal_state: 'sympathetic',
      arousal: 0.5,
      valence: 0.0,
      timestamp: Date.now(),
    };

    const response = await qda.respond('Test query', {}, biofelt);

    const integratoren_layer = response.layers.find(l => l.layer_name === 'Integratoren');
    expect(integratoren_layer).toBeDefined();
    expect(integratoren_layer?.data.response_text).toBeDefined();
    expect(integratoren_layer?.data.response_text.length).toBeGreaterThan(0);
  });

  it('should track total cost and time', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 5,
      polyvagal_state: 'sympathetic',
      arousal: 0.5,
      valence: 0.0,
      timestamp: Date.now(),
    };

    const response = await qda.respond('Test query', {}, biofelt);

    expect(response.total_cost).toBeGreaterThanOrEqual(0);
    expect(response.total_time).toBeGreaterThan(0);
    expect(response.layers.length).toBeGreaterThan(0);

    // Sum of layer costs should equal total cost
    const summed_cost = response.layers.reduce((sum, layer) => sum + layer.cost, 0);
    expect(Math.abs(response.total_cost - summed_cost)).toBeLessThan(0.0001); // Allow for rounding
  });
});

// =============================================================================
// TEST SUITE 6: COST VALIDATION
// =============================================================================

describe('Cost Validation', () => {
  it('should keep simple queries under $0.01', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 3,
      polyvagal_state: 'ventral',
      arousal: 0.3,
      valence: 0.5,
      timestamp: Date.now(),
    };

    const queries = ['Hei', 'Takk', 'Hvordan går det?', 'Ha en fin dag'];

    for (const query of queries) {
      const response = await qda.respond(query, {}, biofelt);
      expect(response.total_cost).toBeLessThan(0.01);
    }
  });

  it('should keep moderate queries under $0.05', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 5,
      polyvagal_state: 'sympathetic',
      arousal: 0.5,
      valence: -0.2,
      timestamp: Date.now(),
    };

    const response = await qda.respond('Jeg føler meg litt stresset i dag', {}, biofelt);

    expect(response.total_cost).toBeLessThan(0.05);
  });

  it('should allow complex queries to exceed $0.10 (Strategen)', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 8,
      polyvagal_state: 'sympathetic',
      arousal: 0.8,
      valence: -0.6,
      timestamp: Date.now(),
    };

    const longQuery =
      'Jeg har mistet jobben min og jeg vet ikke hvordan jeg skal betale regningene ' +
      'og jeg har ingen å snakke med og jeg føler meg helt håpløs og jeg vet ikke hva jeg skal gjøre';

    const response = await qda.respond(longQuery, {}, biofelt);

    // Complex queries with Strategen can be expensive
    if (response.highest_layer_used === 'Strategen') {
      expect(response.total_cost).toBeGreaterThan(0.1);
    }
  });
});
