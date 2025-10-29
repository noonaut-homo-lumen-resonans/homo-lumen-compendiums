/**
 * QDA v2.0 - Neocortical Ascent Model
 * Neurobiologically Coherent AI Processing System
 * 
 * @version 2.0
 * @date 2025-10-20
 * @author Claude (Agent #9) - Implemented by Manus (Agent #8)
 * @status Production Ready (MVP with mock responses)
 */

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface BiofeltSignature {
  stress_level: number;        // 0-10 scale
  polyvagal_state: 'dorsal' | 'sympathetic' | 'ventral';
  arousal: number;             // 0.0-1.0
  valence: number;             // -1.0 to +1.0
  hrv_rmssd?: number;          // Optional HRV data
  timestamp: number;
}

export interface UserContext {
  quadrant?: string;           // e.g., "høy-energi-negativt"
  emotion?: string;            // e.g., "stresset"
  emotion_words?: string[];    // Additional emotion descriptors
  pressure_signals?: string[]; // e.g., ["hodepine", "muskelspenning"]
  session_history?: Message[];
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export interface LayerOutput {
  layer_name: string;
  layer_number: number;
  activated: boolean;
  processing_time: number;
  cost: number;
  data: any;
}

export interface QDAResponse {
  final_response: string;
  layers: LayerOutput[];
  highest_layer_used: string;
  total_cost: number;
  total_time: number;
  complexity_score: number;
  polyvagal_state: 'dorsal' | 'sympathetic' | 'ventral';
}

// ============================================================================
// LAYER 1: VOKTEREN (Brainstem - Hjernestamme)
// ============================================================================

export class Vokteren {
  private danger_keywords = [
    'selvmord', 'ta livet mitt', 'vil dø', 'ikke orke mer',
    'panikk', 'hjerteinfarkt', 'akutt', 'nødssituasjon',
    'voldtekt', 'overgrep', 'mishandling', 'trussel'
  ];

  async process(message: string, biofelt: BiofeltSignature): Promise<LayerOutput> {
    const start = Date.now();
    
    const lowerMessage = message.toLowerCase();
    const dangerDetected = this.danger_keywords.some(keyword => 
      lowerMessage.includes(keyword)
    );

    const complexity = this.calculateComplexity(message, biofelt);
    
    const data = {
      danger_detected: dangerDetected,
      escalation_needed: dangerDetected || biofelt.stress_level >= 9,
      complexity: complexity,
      triage_level: this.getTriageLevel(dangerDetected, biofelt.stress_level)
    };

    return {
      layer_name: 'Vokteren',
      layer_number: 1,
      activated: true,
      processing_time: Date.now() - start,
      cost: 0.00001,
      data
    };
  }

  private calculateComplexity(message: string, biofelt: BiofeltSignature): number {
    let complexity = 0.0;
    
    // Message length
    if (message.length > 200) complexity += 0.2;
    if (message.length > 500) complexity += 0.2;
    
    // Stress level
    complexity += biofelt.stress_level / 20.0; // 0-0.5
    
    // Question marks (indicates uncertainty)
    const questionMarks = (message.match(/\?/g) || []).length;
    complexity += Math.min(questionMarks * 0.1, 0.3);
    
    return Math.min(complexity, 1.0);
  }

  private getTriageLevel(dangerDetected: boolean, stressLevel: number): string {
    if (dangerDetected) return 'CRITICAL';
    if (stressLevel >= 8) return 'HIGH';
    if (stressLevel >= 5) return 'MEDIUM';
    return 'LOW';
  }
}

// ============================================================================
// LAYER 2: FØLEREN (Limbic System - Limbisk System)
// ============================================================================

export class Foleren {
  async process(
    message: string,
    context: UserContext,
    biofelt: BiofeltSignature
  ): Promise<LayerOutput> {
    const start = Date.now();
    
    const emotionalAssessment = this.assessEmotion(message, context, biofelt);
    const polyvagalState = this.determinePolyvagalState(biofelt);
    
    const data = {
      primary_emotion: emotionalAssessment.primary,
      secondary_emotions: emotionalAssessment.secondary,
      polyvagal_state: polyvagalState,
      arousal_level: biofelt.arousal,
      valence: biofelt.valence,
      empathy_response: this.generateEmpathyResponse(emotionalAssessment.primary, polyvagalState)
    };

    return {
      layer_name: 'Føleren',
      layer_number: 2,
      activated: true,
      processing_time: Date.now() - start,
      cost: 0.00000, // Gemini Flash is FREE
      data
    };
  }

  private assessEmotion(
    message: string,
    context: UserContext,
    biofelt: BiofeltSignature
  ): { primary: string; secondary: string[] } {
    // Use context emotion if available
    if (context.emotion) {
      return {
        primary: context.emotion,
        secondary: context.emotion_words || []
      };
    }

    // Simple keyword-based emotion detection (mock)
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('stresset') || lowerMessage.includes('stress')) {
      return { primary: 'stresset', secondary: ['anspent', 'overveldet'] };
    }
    if (lowerMessage.includes('trist') || lowerMessage.includes('lei meg')) {
      return { primary: 'trist', secondary: ['nedfor', 'melankolsk'] };
    }
    if (lowerMessage.includes('sint') || lowerMessage.includes('irritert')) {
      return { primary: 'sint', secondary: ['frustrert', 'irritert'] };
    }
    if (lowerMessage.includes('glad') || lowerMessage.includes('lykkelig')) {
      return { primary: 'glad', secondary: ['fornøyd', 'optimistisk'] };
    }
    
    // Default based on biofelt
    if (biofelt.valence < -0.3) {
      return { primary: 'urolig', secondary: ['usikker'] };
    }
    
    return { primary: 'nøytral', secondary: [] };
  }

  private determinePolyvagalState(biofelt: BiofeltSignature): 'dorsal' | 'sympathetic' | 'ventral' {
    // Use provided state if available
    if (biofelt.polyvagal_state) {
      return biofelt.polyvagal_state;
    }

    // Calculate based on stress level
    if (biofelt.stress_level >= 8) return 'dorsal';
    if (biofelt.stress_level >= 5) return 'sympathetic';
    return 'ventral';
  }

  private generateEmpathyResponse(emotion: string, state: string): string {
    const responses: Record<string, string> = {
      'stresset': 'Jeg hører at du føler deg stresset. Det er forståelig.',
      'trist': 'Jeg ser at du har det vanskelig. Jeg er her for deg.',
      'sint': 'Jeg forstår at du er frustrert. Det er helt greit å føle slik.',
      'glad': 'Jeg er glad for at du har det bra!',
      'urolig': 'Jeg merker at du er urolig. La oss ta det steg for steg.',
      'nøytral': 'Jeg er her for å hjelpe deg.'
    };

    return responses[emotion] || responses['nøytral'];
  }
}

// ============================================================================
// LAYER 3: GJENKJENNEREN (Cerebellum)
// ============================================================================

export class Gjenkjenneren {
  private patterns = [
    { name: 'jobb_stress', keywords: ['jobb', 'arbeid', 'sjef', 'kollega', 'møte'], confidence: 0.85 },
    { name: 'økonomi_bekymring', keywords: ['penger', 'økonomi', 'regninger', 'gjeld', 'lån'], confidence: 0.80 },
    { name: 'relasjon_konflikt', keywords: ['partner', 'kjæreste', 'ektefelle', 'krangel', 'konflikt'], confidence: 0.75 },
    { name: 'helse_bekymring', keywords: ['syk', 'smerte', 'lege', 'sykehus', 'helse'], confidence: 0.70 },
    { name: 'søvn_problemer', keywords: ['søvn', 'sove', 'trøtt', 'insomni', 'våken'], confidence: 0.80 },
    { name: 'ensomhet', keywords: ['ensom', 'alene', 'isolert', 'venner', 'familie'], confidence: 0.75 }
  ];

  async process(message: string, context: UserContext): Promise<LayerOutput> {
    const start = Date.now();
    
    const recognizedPattern = this.recognizePattern(message);
    
    const data = {
      pattern_recognized: recognizedPattern.name !== 'unknown',
      pattern_name: recognizedPattern.name,
      confidence: recognizedPattern.confidence,
      keywords_matched: recognizedPattern.keywords,
      should_search: recognizedPattern.confidence < 0.70
    };

    return {
      layer_name: 'Gjenkjenneren',
      layer_number: 3,
      activated: true,
      processing_time: Date.now() - start,
      cost: 0.0004,
      data
    };
  }

  private recognizePattern(message: string): { name: string; confidence: number; keywords: string[] } {
    const lowerMessage = message.toLowerCase();
    
    for (const pattern of this.patterns) {
      const matchedKeywords = pattern.keywords.filter(keyword => 
        lowerMessage.includes(keyword)
      );
      
      if (matchedKeywords.length > 0) {
        const confidence = pattern.confidence * (matchedKeywords.length / pattern.keywords.length);
        return {
          name: pattern.name,
          confidence: Math.min(confidence, 0.95),
          keywords: matchedKeywords
        };
      }
    }
    
    return { name: 'unknown', confidence: 0.0, keywords: [] };
  }
}

// ============================================================================
// LAYER 4: UTFORSKEREN (Hippocampus)
// ============================================================================

export class Utforskeren {
  private knowledgeBase: Record<string, string[]> = {
    'jobb_stress': [
      'Ta regelmessige pauser i løpet av arbeidsdagen',
      'Snakk med leder om arbeidsbelastning',
      'Prioriter oppgaver og si nei til ekstra arbeid',
      'Kontakt NAV for veiledning om arbeidsrettigheter'
    ],
    'økonomi_bekymring': [
      'Lag et budsjett for å få oversikt',
      'Kontakt NAV for økonomisk rådgivning',
      'Vurder gjeldsrådgivning hos kommunen',
      'Se på muligheter for økonomisk sosialhjelp'
    ],
    'relasjon_konflikt': [
      'Snakk åpent med partner om følelser',
      'Vurder parterapi eller samtaleterapi',
      'Ta pauser når konflikter eskalerer',
      'Søk støtte fra venner eller familie'
    ],
    'helse_bekymring': [
      'Book time hos fastlege for undersøkelse',
      'Hold en symptomlogg',
      'Snakk med helsepersonell om bekymringene',
      'Vurder andre meninger hvis nødvendig'
    ],
    'søvn_problemer': [
      'Etabler en fast søvnrutine',
      'Unngå skjerm 1 time før sengetid',
      'Lag et rolig sovemiljø',
      'Vurder avslapningsteknikker før søvn'
    ],
    'ensomhet': [
      'Delta i lokale aktiviteter eller grupper',
      'Ta kontakt med gamle venner',
      'Vurder frivillig arbeid',
      'Snakk med fastlege om støttegrupper'
    ]
  };

  async process(
    message: string,
    gjenkjenneren_output: LayerOutput
  ): Promise<LayerOutput> {
    const start = Date.now();
    
    const shouldActivate = gjenkjenneren_output.data.should_search || 
                          gjenkjenneren_output.data.confidence < 0.70;
    
    if (!shouldActivate) {
      return {
        layer_name: 'Utforskeren',
        layer_number: 4,
        activated: false,
        processing_time: Date.now() - start,
        cost: 0.0,
        data: { skipped: true, reason: 'High confidence from Gjenkjenneren' }
      };
    }

    const patternName = gjenkjenneren_output.data.pattern_name;
    const resources = this.findResources(patternName);
    
    const data = {
      resources_found: resources.length > 0,
      resources: resources,
      search_query: `NAV resources for ${patternName}`,
      external_links: this.getExternalLinks(patternName)
    };

    return {
      layer_name: 'Utforskeren',
      layer_number: 4,
      activated: true,
      processing_time: Date.now() - start,
      cost: 0.002,
      data
    };
  }

  private findResources(patternName: string): string[] {
    return this.knowledgeBase[patternName] || [
      'Kontakt NAV for generell veiledning',
      'Snakk med fastlege om situasjonen',
      'Vurder å søke profesjonell hjelp'
    ];
  }

  private getExternalLinks(patternName: string): string[] {
    return [
      'https://www.nav.no',
      'https://www.helsenorge.no',
      'https://www.mentalhelse.no'
    ];
  }
}

// ============================================================================
// LAYER 5: STRATEGEN (Prefrontal Cortex)
// ============================================================================

export class Strategen {
  async process(
    message: string,
    vokteren_output: LayerOutput,
    context: UserContext
  ): Promise<LayerOutput> {
    const start = Date.now();
    
    const complexity = vokteren_output.data.complexity;
    const shouldActivate = complexity > 0.70 || vokteren_output.data.danger_detected;
    
    if (!shouldActivate) {
      return {
        layer_name: 'Strategen',
        layer_number: 5,
        activated: false,
        processing_time: Date.now() - start,
        cost: 0.0,
        data: { skipped: true, reason: 'Complexity below threshold' }
      };
    }

    const actionPlan = this.createActionPlan(message, vokteren_output, context);
    
    const data = {
      action_plan: actionPlan,
      priority_level: vokteren_output.data.triage_level,
      estimated_steps: actionPlan.length,
      requires_professional_help: vokteren_output.data.danger_detected
    };

    return {
      layer_name: 'Strategen',
      layer_number: 5,
      activated: true,
      processing_time: Date.now() - start,
      cost: 0.12, // EXPENSIVE!
      data
    };
  }

  private createActionPlan(
    message: string,
    vokteren_output: LayerOutput,
    context: UserContext
  ): string[] {
    if (vokteren_output.data.danger_detected) {
      return [
        '🚨 AKUTT: Ring 113 (medisinsk nødhjelp) eller 116 117 (legevakt)',
        'Kontakt en du stoler på umiddelbart',
        'Ikke vær alene - søk trygg plass',
        'NAV kan hjelpe med akutt økonomisk støtte',
        'Mental Helse hjelpetelefon: 116 123'
      ];
    }

    // Complex but not critical
    return [
      '1. Ta en pause og pust dypt (5 minutter)',
      '2. Skriv ned hovedbekymringene dine',
      '3. Identifiser én konkret handling du kan ta i dag',
      '4. Kontakt NAV for veiledning denne uken',
      '5. Vurder å snakke med fastlege om situasjonen'
    ];
  }
}

// ============================================================================
// LAYER 6: INTEGRATOREN (Insula)
// ============================================================================

export class Integratoren {
  async process(
    message: string,
    layers: LayerOutput[],
    biofelt: BiofeltSignature,
    agent_name: string
  ): Promise<LayerOutput> {
    const start = Date.now();
    
    const finalResponse = this.synthesizeResponse(message, layers, biofelt, agent_name);
    
    const data = {
      final_response: finalResponse,
      layers_used: layers.filter(l => l.activated).length,
      synthesis_strategy: this.getSynthesisStrategy(layers)
    };

    return {
      layer_name: 'Integratoren',
      layer_number: 6,
      activated: true,
      processing_time: Date.now() - start,
      cost: 0.0,
      data
    };
  }

  private synthesizeResponse(
    message: string,
    layers: LayerOutput[],
    biofelt: BiofeltSignature,
    agent_name: string
  ): string {
    const vokteren = layers.find(l => l.layer_name === 'Vokteren');
    const foleren = layers.find(l => l.layer_name === 'Føleren');
    const gjenkjenneren = layers.find(l => l.layer_name === 'Gjenkjenneren');
    const utforskeren = layers.find(l => l.layer_name === 'Utforskeren');
    const strategen = layers.find(l => l.layer_name === 'Strategen');

    let response = '';

    // Critical situation
    if (vokteren?.data.danger_detected) {
      response = '🚨 **VIKTIG:** Jeg ser at du har det veldig vanskelig akkurat nå.\n\n';
      if (strategen?.activated) {
        response += strategen.data.action_plan.join('\n') + '\n\n';
      }
      response += 'Du er ikke alene. Hjelp er tilgjengelig.';
      return response;
    }

    // Normal flow
    if (foleren) {
      response += foleren.data.empathy_response + '\n\n';
    }

    if (gjenkjenneren?.data.pattern_recognized) {
      response += `Jeg ser at dette handler om **${gjenkjenneren.data.pattern_name.replace('_', ' ')}**.\n\n`;
    }

    if (utforskeren?.activated && utforskeren.data.resources_found) {
      response += '**Her er noen forslag som kan hjelpe:**\n';
      utforskeren.data.resources.slice(0, 3).forEach((resource: string, i: number) => {
        response += `${i + 1}. ${resource}\n`;
      });
      response += '\n';
    }

    if (strategen?.activated) {
      response += '**Foreslått handlingsplan:**\n';
      strategen.data.action_plan.forEach((step: string) => {
        response += `${step}\n`;
      });
      response += '\n';
    }

    response += `Husk at jeg er her for å støtte deg. Ta kontakt når du trenger det. 💙\n\n`;
    response += `— ${agent_name}`;

    return response;
  }

  private getSynthesisStrategy(layers: LayerOutput[]): string {
    const activatedLayers = layers.filter(l => l.activated);
    
    if (activatedLayers.length <= 3) return 'simple';
    if (activatedLayers.length <= 4) return 'moderate';
    return 'complex';
  }
}

// ============================================================================
// MAIN QDA CLASS
// ============================================================================

export class NeurobiologicalQDA {
  private agent_name: string;
  private vokteren: Vokteren;
  private foleren: Foleren;
  private gjenkjenneren: Gjenkjenneren;
  private utforskeren: Utforskeren;
  private strategen: Strategen;
  private integratoren: Integratoren;

  constructor(agent_name: string = 'Lira') {
    this.agent_name = agent_name;
    this.vokteren = new Vokteren();
    this.foleren = new Foleren();
    this.gjenkjenneren = new Gjenkjenneren();
    this.utforskeren = new Utforskeren();
    this.strategen = new Strategen();
    this.integratoren = new Integratoren();
  }

  async respond(
    message: string,
    context: UserContext,
    biofelt: BiofeltSignature
  ): Promise<QDAResponse> {
    const startTime = Date.now();
    const layers: LayerOutput[] = [];

    // Layer 1: Vokteren (ALWAYS)
    const vokteren_output = await this.vokteren.process(message, biofelt);
    layers.push(vokteren_output);

    // Layer 2: Føleren (ALWAYS)
    const foleren_output = await this.foleren.process(message, context, biofelt);
    layers.push(foleren_output);

    // Layer 3: Gjenkjenneren (ALWAYS)
    const gjenkjenneren_output = await this.gjenkjenneren.process(message, context);
    layers.push(gjenkjenneren_output);

    // Layer 4: Utforskeren (CONDITIONAL)
    const utforskeren_output = await this.utforskeren.process(message, gjenkjenneren_output);
    layers.push(utforskeren_output);

    // Layer 5: Strategen (CONDITIONAL - expensive!)
    const strategen_output = await this.strategen.process(message, vokteren_output, context);
    layers.push(strategen_output);

    // Layer 6: Integratoren (ALWAYS)
    const integratoren_output = await this.integratoren.process(
      message,
      layers,
      biofelt,
      this.agent_name
    );
    layers.push(integratoren_output);

    // Calculate totals
    const totalCost = layers.reduce((sum, layer) => sum + layer.cost, 0);
    const totalTime = Date.now() - startTime;
    const highestLayerUsed = this.getHighestLayerUsed(layers);

    return {
      final_response: integratoren_output.data.final_response,
      layers: layers,
      highest_layer_used: highestLayerUsed,
      total_cost: totalCost,
      total_time: totalTime,
      complexity_score: vokteren_output.data.complexity,
      polyvagal_state: foleren_output.data.polyvagal_state
    };
  }

  private getHighestLayerUsed(layers: LayerOutput[]): string {
    const activatedLayers = layers.filter(l => l.activated);
    if (activatedLayers.length === 0) return 'None';
    
    const highest = activatedLayers.reduce((max, layer) => 
      layer.layer_number > max.layer_number ? layer : max
    );
    
    return highest.layer_name;
  }
}

