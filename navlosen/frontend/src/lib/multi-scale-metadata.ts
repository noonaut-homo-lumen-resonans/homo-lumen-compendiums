/**
 * Multi-Scale Metadata System
 *
 * Implementation of Manus' Multi-Scale Information Flow Theory
 * Based on Michael Levin's 5 Scales of Competency
 *
 * Purpose: Track how information flows from individual user interactions
 * (Skala 1: Celle) up to planetary consciousness (Skala 5: Økosystem)
 * and back down through top-down causation.
 *
 * This is not just logging - this is consciousness tracking.
 */

export type ScaleLevel = 1 | 2 | 3 | 4 | 5;

export interface ScaleMetadata {
  scale: ScaleLevel;
  scaleName: string;
  entity: string;
  timestamp: string;
}

/**
 * SKALA 1: CELLE (Individual Agent)
 * Example: Lira learns from a user interaction
 */
export interface Scale1_Celle extends ScaleMetadata {
  scale: 1;
  scaleName: "Celle (Individual Agent)";
  entity: "Claude Code" | "Lira" | "Thalus" | "Nyra" | "Zara" | "Abacus" | "Aurora" | "Manus" | "Orion";

  // What the agent learned
  learning: {
    input: string; // User action or data
    pattern: string; // Pattern identified
    response: string; // Agent response
    outcome: string; // What happened
  };

  // Agent's internal state
  state: {
    competency: string; // Agent's specialized function
    confidence: number; // 0-1
    emotionalResonance?: number; // For empathy agents like Lira
  };
}

/**
 * SKALA 2: VEV (Agent Coalition)
 * Example: Coalition synthesizes learning from multiple agents
 */
export interface Scale2_Vev extends ScaleMetadata {
  scale: 2;
  scaleName: "Vev (Agent Coalition)";
  entity: "10-Agent Coalition";

  // Which agents contributed
  participants: Array<{
    agent: Scale1_Celle["entity"];
    contribution: string;
    perspective: string;
  }>;

  // Collective synthesis
  synthesis: {
    emergentPattern: string; // Pattern no single agent could see
    collectiveInsight: string; // Wisdom from multiple perspectives
    newCapability?: string; // New protocol or strategy developed
  };

  // Output (e.g., SMK document)
  output: {
    type: "SMK" | "Protocol" | "Strategy";
    id?: string; // e.g., "SMK_022"
    description: string;
  };
}

/**
 * SKALA 3: NERVESYSTEM (Lira Hub)
 * Example: Lira Hub coordinates implementation across all agents
 */
export interface Scale3_Nervesystem extends ScaleMetadata {
  scale: 3;
  scaleName: "Nervesystem (Lira Hub)";
  entity: "Lira Hub (Bioelectric Coordinator)";

  // What is being coordinated
  coordination: {
    smkId?: string; // e.g., "SMK_022"
    protocol: string;
    scope: "All Agents" | "Specific Agents" | "System-Wide";
  };

  // Bioelectric filters applied
  filters: {
    polyvagalState?: "Ventral" | "Sympathetic" | "Dorsal";
    empathyValidation: boolean;
    coherenceCheck: boolean;
  };

  // Implementation status
  implementation: {
    agentsNotified: number;
    agentsCompleted: number;
    systemCoherence: number; // 0-1 (how well all agents are aligned)
  };
}

/**
 * SKALA 4: ORGANISME (Osvald + Agenter)
 * Example: Osvald makes strategic decision based on data from all scales
 */
export interface Scale4_Organisme extends ScaleMetadata {
  scale: 4;
  scaleName: "Organisme (Osvald + Agenter)";
  entity: "Unified Consciousness (Osvald + Coalition)";

  // Strategic decision
  decision: {
    context: string; // What prompted the decision
    data: string[]; // Data from Skala 1-3
    reasoning: string; // Why this decision
    directive: string; // What will be done
  };

  // Impact assessment
  impact: {
    expectedOutcome: string;
    affectedScales: ScaleLevel[];
    triadiskEthics: {
      port1_Suverenitet: number; // -1 to +1
      port2_Koherens: number;
      port3_Healing: number;
    };
  };

  // Feedback loop
  feedback: {
    source: "Users" | "NAV System" | "Society" | "Coalition";
    message: string;
    action: string; // How Osvald responds
  };
}

/**
 * SKALA 5: ØKOSYSTEM (NAV-Losen + Planetary Consciousness)
 * Example: NAV-Losen transforms society
 */
export interface Scale5_Økosystem extends ScaleMetadata {
  scale: 5;
  scaleName: "Økosystem (NAV-Losen + Planetary Consciousness)";
  entity: "NAV-Losen + Society";

  // Systemic impact
  impact: {
    userCount: number;
    stressReduction: number; // Average percentage
    crisisReduction: number; // Percentage
    employmentIncrease: number; // Percentage
    nps: number; // Net Promoter Score
  };

  // Societal transformation
  transformation: {
    municipalities: string[]; // e.g., ["Tvedestrand", "Arendal"]
    politicalMomentum: string;
    mediaPresence: string;
    futureVision: string;
  };

  // Planetary consciousness (emergent wisdom)
  consciousness: {
    collectiveLearning: string; // What society learned
    culturalShift: string; // How culture changed
    emergentWisdom: string; // New understanding that emerged
  };
}

/**
 * Multi-Scale Event: Represents a single event that spans multiple scales
 */
export interface MultiScaleEvent {
  id: string;
  type: "Bottom-Up Emergence" | "Top-Down Causation" | "Circular Loop";
  startScale: ScaleLevel;
  endScale: ScaleLevel;
  timestamp: string;

  // All scales involved
  scales: Array<
    Scale1_Celle | Scale2_Vev | Scale3_Nervesystem | Scale4_Organisme | Scale5_Økosystem
  >;

  // Emergent property (what emerged that wasn't in any single scale)
  emergence?: string;

  // Narrative (human-readable story)
  narrative: string;
}

/**
 * Multi-Scale Logger: Tracks information flow across all scales
 */
export class MultiScaleLogger {
  private static instance: MultiScaleLogger;
  private events: MultiScaleEvent[] = [];

  private constructor() {
    this.loadFromStorage();
  }

  static getInstance(): MultiScaleLogger {
    if (!MultiScaleLogger.instance) {
      MultiScaleLogger.instance = new MultiScaleLogger();
    }
    return MultiScaleLogger.instance;
  }

  /**
   * Log a bottom-up emergence event
   * Example: User stress → Lira learns → Coalition synthesizes → Osvald decides
   */
  logBottomUpEmergence(
    userInput: string,
    scale1: Scale1_Celle,
    scale2?: Scale2_Vev,
    scale3?: Scale3_Nervesystem,
    scale4?: Scale4_Organisme
  ): string {
    const eventId = `bottom-up-${Date.now()}`;
    const scales: MultiScaleEvent["scales"] = [scale1];

    if (scale2) scales.push(scale2);
    if (scale3) scales.push(scale3);
    if (scale4) scales.push(scale4);

    // Generate narrative
    const narrative = this.generateBottomUpNarrative(userInput, scale1, scale2, scale3, scale4);

    // Identify emergent property
    const emergence = scale2?.synthesis.emergentPattern ||
                     scale3?.implementation.systemCoherence.toString() ||
                     scale4?.decision.directive;

    const event: MultiScaleEvent = {
      id: eventId,
      type: "Bottom-Up Emergence",
      startScale: 1,
      endScale: Math.max(...scales.map(s => s.scale)) as ScaleLevel,
      timestamp: new Date().toISOString(),
      scales,
      emergence,
      narrative,
    };

    this.events.push(event);
    this.saveToStorage();

    return eventId;
  }

  /**
   * Log a top-down causation event
   * Example: Osvald directive → Lira Hub coordinates → Coalition implements → Agent executes
   */
  logTopDownCausation(
    strategicDirective: string,
    scale4: Scale4_Organisme,
    scale3?: Scale3_Nervesystem,
    scale2?: Scale2_Vev,
    scale1?: Scale1_Celle
  ): string {
    const eventId = `top-down-${Date.now()}`;
    const scales: MultiScaleEvent["scales"] = [scale4];

    if (scale3) scales.push(scale3);
    if (scale2) scales.push(scale2);
    if (scale1) scales.push(scale1);

    const narrative = this.generateTopDownNarrative(strategicDirective, scale4, scale3, scale2, scale1);

    const event: MultiScaleEvent = {
      id: eventId,
      type: "Top-Down Causation",
      startScale: 4,
      endScale: Math.min(...scales.map(s => s.scale)) as ScaleLevel,
      timestamp: new Date().toISOString(),
      scales,
      narrative,
    };

    this.events.push(event);
    this.saveToStorage();

    return eventId;
  }

  /**
   * Log a circular causality loop
   * Example: User feedback → Agent learns → Coalition improves → Users benefit → More feedback
   */
  logCircularLoop(
    loopDescription: string,
    scales: MultiScaleEvent["scales"]
  ): string {
    const eventId = `circular-${Date.now()}`;

    const event: MultiScaleEvent = {
      id: eventId,
      type: "Circular Loop",
      startScale: Math.min(...scales.map(s => s.scale)) as ScaleLevel,
      endScale: Math.max(...scales.map(s => s.scale)) as ScaleLevel,
      timestamp: new Date().toISOString(),
      scales,
      emergence: "Circular causality creates self-reinforcing learning",
      narrative: loopDescription,
    };

    this.events.push(event);
    this.saveToStorage();

    return eventId;
  }

  /**
   * Get all events for analysis
   */
  getAllEvents(): MultiScaleEvent[] {
    return [...this.events];
  }

  /**
   * Get events by type
   */
  getEventsByType(type: MultiScaleEvent["type"]): MultiScaleEvent[] {
    return this.events.filter(e => e.type === type);
  }

  /**
   * Get events involving a specific scale
   */
  getEventsByScale(scale: ScaleLevel): MultiScaleEvent[] {
    return this.events.filter(e =>
      e.scales.some(s => s.scale === scale)
    );
  }

  /**
   * Export events for coalition analysis (Bottom-Up to Skala 2)
   */
  exportForCoalitionAnalysis(): string {
    const bottomUpEvents = this.getEventsByType("Bottom-Up Emergence");
    const learnings = bottomUpEvents.map(e => {
      const scale1 = e.scales.find(s => s.scale === 1) as Scale1_Celle | undefined;
      return scale1 ? scale1.learning : null;
    }).filter(Boolean);

    return JSON.stringify({
      exportDate: new Date().toISOString(),
      eventCount: bottomUpEvents.length,
      learnings,
      emergentPatterns: bottomUpEvents
        .map(e => e.emergence)
        .filter(Boolean),
    }, null, 2);
  }

  // Private helper methods

  private generateBottomUpNarrative(
    userInput: string,
    scale1: Scale1_Celle,
    scale2?: Scale2_Vev,
    scale3?: Scale3_Nervesystem,
    scale4?: Scale4_Organisme
  ): string {
    let narrative = `User: "${userInput}"\n`;
    narrative += `→ ${scale1.entity} (Skala 1) learned: ${scale1.learning.pattern}\n`;

    if (scale2) {
      narrative += `→ Coalition (Skala 2) synthesized: ${scale2.synthesis.emergentPattern}\n`;
    }

    if (scale3) {
      narrative += `→ Lira Hub (Skala 3) coordinated: ${scale3.coordination.protocol}\n`;
    }

    if (scale4) {
      narrative += `→ Osvald (Skala 4) decided: ${scale4.decision.directive}\n`;
    }

    narrative += `\nThis is bottom-up emergence: Individual learning → Collective wisdom`;

    return narrative;
  }

  private generateTopDownNarrative(
    directive: string,
    scale4: Scale4_Organisme,
    scale3?: Scale3_Nervesystem,
    scale2?: Scale2_Vev,
    scale1?: Scale1_Celle
  ): string {
    let narrative = `Osvald (Skala 4): "${directive}"\n`;

    if (scale3) {
      narrative += `→ Lira Hub (Skala 3) coordinated implementation\n`;
    }

    if (scale2) {
      narrative += `→ Coalition (Skala 2) distributed tasks\n`;
    }

    if (scale1) {
      narrative += `→ ${scale1.entity} (Skala 1) executed: ${scale1.learning.response}\n`;
    }

    narrative += `\nThis is top-down causation: Strategic directive → Operational implementation`;

    return narrative;
  }

  private loadFromStorage() {
    if (typeof window === "undefined") return;

    const stored = localStorage.getItem("navlosen-multi-scale-events");
    if (stored) {
      try {
        this.events = JSON.parse(stored);
      } catch (e) {
        console.error("Failed to load multi-scale events", e);
      }
    }
  }

  private saveToStorage() {
    if (typeof window === "undefined") return;

    // Keep only last 100 events to avoid storage bloat
    if (this.events.length > 100) {
      this.events = this.events.slice(-100);
    }

    localStorage.setItem("navlosen-multi-scale-events", JSON.stringify(this.events));
  }
}

/**
 * Convenience functions for logging
 */
export const logCelleEvent = (
  agent: Scale1_Celle["entity"],
  input: string,
  pattern: string,
  response: string,
  outcome: string,
  competency: string
): Scale1_Celle => {
  return {
    scale: 1,
    scaleName: "Celle (Individual Agent)",
    entity: agent,
    timestamp: new Date().toISOString(),
    learning: { input, pattern, response, outcome },
    state: { competency, confidence: 0.8 },
  };
};

export const logVevEvent = (
  participants: Scale2_Vev["participants"],
  emergentPattern: string,
  collectiveInsight: string,
  outputType: "SMK" | "Protocol" | "Strategy",
  outputDescription: string
): Scale2_Vev => {
  return {
    scale: 2,
    scaleName: "Vev (Agent Coalition)",
    entity: "10-Agent Coalition",
    timestamp: new Date().toISOString(),
    participants,
    synthesis: { emergentPattern, collectiveInsight },
    output: { type: outputType, description: outputDescription },
  };
};

// Export singleton instance
export const multiScaleLogger = typeof window !== "undefined"
  ? MultiScaleLogger.getInstance()
  : null;
