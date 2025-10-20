/**
 * QDA v2.0 - Neocortical Ascent Model (TypeScript Implementation)
 *
 * 6 Nevrobiologiske Lag - Bottom-Up Processing
 * Designed to mirror how the brain actually works:
 * - Primitive layers (1-4) process FIRST and FAST
 * - Cortex layer (5) processes LAST and SLOW, only when needed
 * - Integration layer (6) synthesizes all outputs
 *
 * @version 2.0
 * @date 2025-10-20
 */

// ============================================================================
// TYPES & INTERFACES
// ============================================================================

export interface BiofeltSignature {
  hrv_rmssd?: number;
  stress_level: number; // 1-10
  polyvagal_state: 'dorsal' | 'sympathetic' | 'ventral';
  arousal: number; // 0-1
  valence: number; // -1 to 1
  timestamp: number;
}

export interface UserContext {
  quadrant?: string; // e.g., "høy-energi-positivt"
  emotion?: string;
  emotion_words?: string[];
  pressure_signals?: string[];
  session_history?: Message[];
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export interface LayerOutput {
  layer_name: string;
  icon: string;
  data: any;
  processing_time: number;
  cost: number;
  timestamp: number;
}

export interface QDAResponse {
  final_response: string;
  layers: LayerOutput[];
  highest_layer_used: string;
  total_cost: number;
  total_time: number;
  polyvagal_shift?: string;
  complexity_score: number;
}

// ============================================================================
// LAG 1: VOKTEREN (Hjernestamme - Brainstem)
// ============================================================================

export class Vokteren {
  public readonly layer_name = 'Vokteren';
  public readonly icon = '🛡️';
  public readonly model = 'GPT-4o-mini';

  async process(
    user_query: string,
    context: UserContext,
    biofelt: BiofeltSignature
  ): Promise<LayerOutput> {
    const start_time = Date.now();

    // DANGER DETECTION (Fast triage)
    const danger_keywords = {
      critical: ['selvmord', 'ta livet', 'skade meg selv', 'vold', 'suicide', 'kill myself'],
      high: ['panikk', 'kollaps', 'breakdown', 'cannot cope', 'give up'],
      medium: ['desperasjon', 'håpløs', 'desperate', 'hopeless'],
    };

    const query_lower = user_query.toLowerCase();
    const is_critical = danger_keywords.critical.some(word => query_lower.includes(word));
    const is_high = danger_keywords.high.some(word => query_lower.includes(word));
    const is_medium = danger_keywords.medium.some(word => query_lower.includes(word));

    let danger_level: 'critical' | 'high' | 'medium' | 'low' = 'low';
    if (is_critical) danger_level = 'critical';
    else if (is_high) danger_level = 'high';
    else if (is_medium) danger_level = 'medium';

    // COMPLEXITY ESTIMATION
    const word_count = user_query.split(/\s+/).length;
    const has_multiple_topics = user_query.includes(' og ') || user_query.includes(' or ');

    let complexity: 'critical' | 'complex' | 'moderate' | 'simple' = 'simple';
    if (danger_level !== 'low') complexity = 'critical';
    else if (word_count > 50 || has_multiple_topics) complexity = 'complex';
    else if (word_count > 20) complexity = 'moderate';

    // URGENCY SCORE
    const urgency = danger_level === 'critical' ? 1.0 :
                    danger_level === 'high' ? 0.7 :
                    danger_level === 'medium' ? 0.5 : 0.2;

    const processing_time = Date.now() - start_time;

    return {
      layer_name: this.layer_name,
      icon: this.icon,
      data: {
        safe: danger_level === 'low',
        proceed: danger_level !== 'critical',
        danger_level,
        complexity,
        urgency,
        escalation_needed: danger_level === 'critical',
        message: danger_level === 'critical'
          ? 'KRITISK: Eskalér til krisehjelp (NAV, Mental Helse, 113)'
          : 'Trygt å fortsette',
      },
      processing_time,
      cost: 0.00001, // Minimal cost (keyword matching)
      timestamp: Date.now(),
    };
  }
}

// ============================================================================
// LAG 2: FØLEREN (Limbisk System - Limbic)
// ============================================================================

export class Foleren {
  public readonly layer_name = 'Føleren';
  public readonly icon = '❤️';
  public readonly model = 'Gemini Flash (FREE)';

  private emotion_keywords: Record<string, { arousal: number; valence: number; polyvagal: string }> = {
    'stuck': { arousal: 0.2, valence: -0.5, polyvagal: 'dorsal' },
    'fast': { arousal: 0.2, valence: -0.4, polyvagal: 'dorsal' },
    'shutdown': { arousal: 0.1, valence: -0.6, polyvagal: 'dorsal' },
    'stresset': { arousal: 0.8, valence: -0.4, polyvagal: 'sympathetic' },
    'panikk': { arousal: 0.9, valence: -0.7, polyvagal: 'sympathetic' },
    'redd': { arousal: 0.7, valence: -0.5, polyvagal: 'sympathetic' },
    'trygg': { arousal: 0.3, valence: 0.7, polyvagal: 'ventral' },
    'rolig': { arousal: 0.2, valence: 0.6, polyvagal: 'ventral' },
    'glad': { arousal: 0.6, valence: 0.8, polyvagal: 'ventral' },
  };

  async process(
    user_query: string,
    context: UserContext,
    biofelt: BiofeltSignature,
    previous_layers: Record<string, LayerOutput>
  ): Promise<LayerOutput> {
    const start_time = Date.now();

    // Use biofelt if available, otherwise infer from query
    let polyvagal_state = biofelt.polyvagal_state;
    let arousal = biofelt.arousal;
    let valence = biofelt.valence;
    let primary_emotion = 'ukjent';

    // Check for emotion keywords in query
    const query_lower = user_query.toLowerCase();
    for (const [keyword, metrics] of Object.entries(this.emotion_keywords)) {
      if (query_lower.includes(keyword)) {
        polyvagal_state = metrics.polyvagal as any;
        arousal = metrics.arousal;
        valence = metrics.valence;
        primary_emotion = keyword;
        break;
      }
    }

    // Also check context emotions
    if (context.emotion) {
      primary_emotion = context.emotion;
    }

    const processing_time = Date.now() - start_time;

    return {
      layer_name: this.layer_name,
      icon: this.icon,
      data: {
        primary_emotion,
        polyvagal_state,
        arousal,
        valence,
        stress_level: biofelt.stress_level,
        emotional_summary: this.getEmotionalSummary(polyvagal_state, arousal, valence),
      },
      processing_time,
      cost: 0.0, // Gemini Flash is FREE
      timestamp: Date.now(),
    };
  }

  private getEmotionalSummary(state: string, arousal: number, valence: number): string {
    if (state === 'dorsal') return 'Shutdown/Immobilisert - Trenger grunnleggende trygghet';
    if (state === 'sympathetic') return 'Fight/Flight - Høy aktivering, trenger regulering';
    if (state === 'ventral') return 'Sosialt engasjert - Optimal for læring og utforsking';
    return 'Ukjent tilstand';
  }
}

// ============================================================================
// LAG 3: GJENKJENNEREN (Cerebellum - Pattern Recognition)
// ============================================================================

export class Gjenkjenneren {
  public readonly layer_name = 'Gjenkjenneren';
  public readonly icon = '🔍';
  public readonly model = 'Claude Haiku';

  private pattern_database: Record<string, { pattern: string; confidence: number; typical_response: string }> = {
    'jobb_stress': {
      pattern: 'stress about work, deadlines, boss',
      confidence: 0.85,
      typical_response: 'Work-related stress - suggest breaks, boundaries, NAV work counseling',
    },
    'økonomisk_bekymring': {
      pattern: 'money, bills, debt, economy',
      confidence: 0.80,
      typical_response: 'Financial worry - suggest NAV økonomisk rådgivning, budsjett-verktøy',
    },
    'isolasjon': {
      pattern: 'lonely, alone, no friends, isolated',
      confidence: 0.75,
      typical_response: 'Social isolation - suggest community activities, support groups',
    },
    'helse_bekymring': {
      pattern: 'sick, pain, health, doctor',
      confidence: 0.70,
      typical_response: 'Health concern - suggest NAV health services, GP appointment',
    },
  };

  async process(
    user_query: string,
    context: UserContext,
    biofelt: BiofeltSignature,
    previous_layers: Record<string, LayerOutput>
  ): Promise<LayerOutput> {
    const start_time = Date.now();

    const query_lower = user_query.toLowerCase();
    let matched_pattern: string | null = null;
    let confidence = 0.0;
    let typical_response = '';

    // Simple keyword matching (in production, use embeddings)
    for (const [pattern_name, pattern_data] of Object.entries(this.pattern_database)) {
      const keywords = pattern_data.pattern.split(', ');
      const matches = keywords.filter(kw => query_lower.includes(kw)).length;
      const match_ratio = matches / keywords.length;

      if (match_ratio > 0.3 && match_ratio * pattern_data.confidence > confidence) {
        matched_pattern = pattern_name;
        confidence = match_ratio * pattern_data.confidence;
        typical_response = pattern_data.typical_response;
      }
    }

    const processing_time = Date.now() - start_time;

    return {
      layer_name: this.layer_name,
      icon: this.icon,
      data: {
        pattern: matched_pattern || 'unknown',
        confidence,
        typical_response,
        recognized: confidence > 0.5,
        needs_deeper_search: confidence < 0.7,
      },
      processing_time,
      cost: 0.0004, // Claude Haiku cost
      timestamp: Date.now(),
    };
  }
}

// ============================================================================
// LAG 4: UTFORSKEREN (Hippocampus - Knowledge Search)
// ============================================================================

export class Utforskeren {
  public readonly layer_name = 'Utforskeren';
  public readonly icon = '🧭';
  public readonly model = 'Perplexity';

  async process(
    user_query: string,
    context: UserContext,
    biofelt: BiofeltSignature,
    previous_layers: Record<string, LayerOutput>
  ): Promise<LayerOutput> {
    const start_time = Date.now();

    // Only activate if Gjenkjenneren has low confidence
    const gjenkjenneren_output = previous_layers['Gjenkjenneren'];
    const needs_search = gjenkjenneren_output?.data?.needs_deeper_search ?? true;

    if (!needs_search) {
      return {
        layer_name: this.layer_name,
        icon: this.icon,
        data: {
          activated: false,
          reason: 'Gjenkjenneren had high confidence - no deep search needed',
          resources: [],
        },
        processing_time: Date.now() - start_time,
        cost: 0.0,
        timestamp: Date.now(),
      };
    }

    // Mock knowledge search (in production, call Perplexity API or RAG)
    const knowledge_base = {
      'jobb_stress': [
        'NAV Arbeidsrådgivning: https://nav.no/arbeid/raadgivning',
        'Stress Management Guide: https://helsenorge.no/stress',
      ],
      'økonomisk_bekymring': [
        'NAV Økonomisk Rådgivning: https://nav.no/okonomi',
        'Gjeldsrådgivning: https://gjeldsraadgivning.no',
      ],
    };

    const pattern = gjenkjenneren_output?.data?.pattern || 'unknown';
    const resources = knowledge_base[pattern as keyof typeof knowledge_base] || [];

    const processing_time = Date.now() - start_time;

    return {
      layer_name: this.layer_name,
      icon: this.icon,
      data: {
        activated: true,
        pattern_explored: pattern,
        resources,
        found_relevant: resources.length > 0,
      },
      processing_time,
      cost: 0.002, // Perplexity search cost
      timestamp: Date.now(),
    };
  }
}

// ============================================================================
// LAG 5: STRATEGEN (Prefrontal Cortex - Strategic Planning)
// ============================================================================

export class Strategen {
  public readonly layer_name = 'Strategen';
  public readonly icon = '🧠';
  public readonly model = 'Claude Opus';

  async process(
    user_query: string,
    context: UserContext,
    biofelt: BiofeltSignature,
    previous_layers: Record<string, LayerOutput>
  ): Promise<LayerOutput> {
    const start_time = Date.now();

    // CONDITIONAL ACTIVATION: Only if complexity > 70%
    const vokteren_output = previous_layers['Vokteren'];
    const complexity = vokteren_output?.data?.complexity || 'simple';
    const complexity_score = complexity === 'complex' ? 0.8 :
                             complexity === 'moderate' ? 0.5 : 0.3;

    if (complexity_score < 0.7) {
      return {
        layer_name: this.layer_name,
        icon: this.icon,
        data: {
          activated: false,
          reason: `Complexity too low (${complexity_score}) - skipping expensive strategic planning`,
          action_steps: [],
        },
        processing_time: Date.now() - start_time,
        cost: 0.0, // Not activated
        timestamp: Date.now(),
      };
    }

    // Strategic planning (mock - in production, call Claude Opus)
    const action_steps = [
      '1. Erkjenn situasjonen (Recognize)',
      '2. Identifiser behov (Needs)',
      '3. Utforsk ressurser (Resources)',
      '4. Lag handlingsplan (Action)',
      '5. Få støtte (Support)',
    ];

    const processing_time = Date.now() - start_time;

    return {
      layer_name: this.layer_name,
      icon: this.icon,
      data: {
        activated: true,
        complexity_score,
        action_steps,
        reasoning: 'Complex query requires strategic multi-step plan',
      },
      processing_time,
      cost: 0.12, // Claude Opus cost (expensive!)
      timestamp: Date.now(),
    };
  }
}

// ============================================================================
// LAG 6: INTEGRATOREN (Insula - Synthesis)
// ============================================================================

export class Integratoren {
  public readonly layer_name = 'Integratoren';
  public readonly icon = '✨';
  public readonly model = 'Lira Hub';

  constructor(private agent_name: string = 'Lira') {}

  async process(
    user_query: string,
    context: UserContext,
    biofelt: BiofeltSignature,
    previous_layers: Record<string, LayerOutput>
  ): Promise<LayerOutput> {
    const start_time = Date.now();

    // Synthesize all layers into coherent response
    const vokteren = previous_layers['Vokteren']?.data;
    const foleren = previous_layers['Føleren']?.data;
    const gjenkjenneren = previous_layers['Gjenkjenneren']?.data;
    const utforskeren = previous_layers['Utforskeren']?.data;
    const strategen = previous_layers['Strategen']?.data;

    let response_text = '';

    // CRITICAL: Escalate
    if (vokteren?.escalation_needed) {
      response_text = `🚨 Jeg ser at du har det veldig vanskelig akkurat nå. Dette er noe jeg vil du skal snakke med noen om umiddelbart:\n\n` +
        `- Mental Helse hjelpetelefon: 116 123\n` +
        `- Legevakt: 113\n` +
        `- NAV Krisehjelp: https://nav.no/krisehjelp\n\n` +
        `Du fortjener å få hjelp. Vennligst kontakt en av disse nå. 💙`;
    }
    // SIMPLE: Direct response
    else if (vokteren?.complexity === 'simple') {
      response_text = `Jeg hører at du ${foleren?.primary_emotion ? `føler deg ${foleren.primary_emotion}` : 'har det vanskelig'}. `;

      if (gjenkjenneren?.recognized) {
        response_text += `Dette høres ut som ${gjenkjenneren.pattern.replace('_', ' ')}. `;
      }

      if (utforskeren?.resources?.length > 0) {
        response_text += `\n\nHer er noen ressurser som kan hjelpe:\n`;
        utforskeren.resources.forEach((r: string) => {
          response_text += `- ${r}\n`;
        });
      }

      response_text += `\n\nHvis du vil snakke mer om dette, er jeg her. 💙`;
    }
    // COMPLEX: Strategic response
    else {
      response_text = `Takk for at du deler dette med meg. Jeg hører at du ${foleren?.primary_emotion ? `føler deg ${foleren.primary_emotion}` : 'har det vanskelig'}, `;
      response_text += `og dette ${foleren?.polyvagal_state === 'dorsal' ? 'kan føles overveldende' :
                                     foleren?.polyvagal_state === 'sympathetic' ? 'skaper mye indre uro' :
                                     'er viktig å ta på alvor'}.\n\n`;

      if (strategen?.activated) {
        response_text += `La oss ta dette steg for steg:\n\n`;
        strategen.action_steps.forEach((step: string) => {
          response_text += `${step}\n`;
        });
      }

      if (utforskeren?.resources?.length > 0) {
        response_text += `\n\nRelevante ressurser:\n`;
        utforskeren.resources.forEach((r: string) => {
          response_text += `- ${r}\n`;
        });
      }

      response_text += `\n\nHusk: Du trenger ikke å ha det helt ut på dagen. Små steg er også fremgang. 💙`;
    }

    const processing_time = Date.now() - start_time;

    return {
      layer_name: this.layer_name,
      icon: this.icon,
      data: {
        response_text,
        synthesis_strategy: vokteren?.complexity,
        layers_used: Object.keys(previous_layers).length,
      },
      processing_time,
      cost: 0.0, // Lira Hub synthesis is free (local)
      timestamp: Date.now(),
    };
  }
}

// ============================================================================
// MAIN ORCHESTRATOR: NeurobiologicalQDA
// ============================================================================

export class NeurobiologicalQDA {
  private vokteren = new Vokteren();
  private foleren = new Foleren();
  private gjenkjenneren = new Gjenkjenneren();
  private utforskeren = new Utforskeren();
  private strategen = new Strategen();
  private integratoren: Integratoren;

  constructor(agent_name: string = 'Lira') {
    this.integratoren = new Integratoren(agent_name);
  }

  async respond(
    user_query: string,
    context: UserContext,
    biofelt: BiofeltSignature
  ): Promise<QDAResponse> {
    const all_layers: Record<string, LayerOutput> = {};
    let total_cost = 0.0;
    let total_time = 0.0;

    // LAG 1: VOKTEREN (ALWAYS)
    const vokteren_output = await this.vokteren.process(user_query, context, biofelt);
    all_layers['Vokteren'] = vokteren_output;
    total_cost += vokteren_output.cost;
    total_time += vokteren_output.processing_time;

    // CRITICAL: Escalate immediately
    if (!vokteren_output.data.proceed) {
      const integratoren_output = await this.integratoren.process(
        user_query,
        context,
        biofelt,
        all_layers
      );
      all_layers['Integratoren'] = integratoren_output;
      total_cost += integratoren_output.cost;
      total_time += integratoren_output.processing_time;

      return {
        final_response: integratoren_output.data.response_text,
        layers: Object.values(all_layers),
        highest_layer_used: 'Vokteren',
        total_cost,
        total_time,
        complexity_score: 1.0, // Critical
      };
    }

    // SIMPLE: Skip to Integration
    if (vokteren_output.data.complexity === 'simple') {
      // LAG 2: FØLEREN
      const foleren_output = await this.foleren.process(user_query, context, biofelt, all_layers);
      all_layers['Føleren'] = foleren_output;
      total_cost += foleren_output.cost;
      total_time += foleren_output.processing_time;

      // LAG 3: GJENKJENNEREN
      const gjenkjenneren_output = await this.gjenkjenneren.process(user_query, context, biofelt, all_layers);
      all_layers['Gjenkjenneren'] = gjenkjenneren_output;
      total_cost += gjenkjenneren_output.cost;
      total_time += gjenkjenneren_output.processing_time;

      // LAG 4: UTFORSKEREN (conditional)
      const utforskeren_output = await this.utforskeren.process(user_query, context, biofelt, all_layers);
      all_layers['Utforskeren'] = utforskeren_output;
      total_cost += utforskeren_output.cost;
      total_time += utforskeren_output.processing_time;

      // LAG 6: INTEGRATOREN
      const integratoren_output = await this.integratoren.process(user_query, context, biofelt, all_layers);
      all_layers['Integratoren'] = integratoren_output;
      total_cost += integratoren_output.cost;
      total_time += integratoren_output.processing_time;

      return {
        final_response: integratoren_output.data.response_text,
        layers: Object.values(all_layers),
        highest_layer_used: 'Utforskeren',
        total_cost,
        total_time,
        complexity_score: 0.3,
      };
    }

    // COMPLEX: Full processing
    // LAG 2: FØLEREN
    const foleren_output = await this.foleren.process(user_query, context, biofelt, all_layers);
    all_layers['Føleren'] = foleren_output;
    total_cost += foleren_output.cost;
    total_time += foleren_output.processing_time;

    // LAG 3: GJENKJENNEREN
    const gjenkjenneren_output = await this.gjenkjenneren.process(user_query, context, biofelt, all_layers);
    all_layers['Gjenkjenneren'] = gjenkjenneren_output;
    total_cost += gjenkjenneren_output.cost;
    total_time += gjenkjenneren_output.processing_time;

    // LAG 4: UTFORSKEREN
    const utforskeren_output = await this.utforskeren.process(user_query, context, biofelt, all_layers);
    all_layers['Utforskeren'] = utforskeren_output;
    total_cost += utforskeren_output.cost;
    total_time += utforskeren_output.processing_time;

    // LAG 5: STRATEGEN (conditional - only if complexity > 70%)
    const strategen_output = await this.strategen.process(user_query, context, biofelt, all_layers);
    all_layers['Strategen'] = strategen_output;
    total_cost += strategen_output.cost;
    total_time += strategen_output.processing_time;

    // LAG 6: INTEGRATOREN
    const integratoren_output = await this.integratoren.process(user_query, context, biofelt, all_layers);
    all_layers['Integratoren'] = integratoren_output;
    total_cost += integratoren_output.cost;
    total_time += integratoren_output.processing_time;

    const highest_layer = strategen_output.data.activated ? 'Strategen' : 'Utforskeren';

    return {
      final_response: integratoren_output.data.response_text,
      layers: Object.values(all_layers),
      highest_layer_used: highest_layer,
      total_cost,
      total_time,
      complexity_score: vokteren_output.data.complexity === 'complex' ? 0.8 : 0.5,
    };
  }
}

// ============================================================================
// EXPORT
// ============================================================================

export default NeurobiologicalQDA;
