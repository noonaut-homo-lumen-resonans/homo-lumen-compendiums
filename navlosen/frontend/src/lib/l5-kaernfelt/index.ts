/**
 * L5: KÄRNFELT (Frequency Coordination)
 *
 * Meta-lag over ALT - koordinerer frekvenser på tvers av agenter
 *
 * This layer manages cognitive frequency coordination:
 * - Delta (1-4 Hz): Healing, memory consolidation
 * - Theta (4-8 Hz): Creativity, intuition
 * - Alpha (8-13 Hz): Relaxed focus, flow
 * - Beta (13-30 Hz): Active thinking, problem-solving
 * - Gamma (30-100 Hz): High-level cognition, strategic planning
 *
 * Based on Multi-Scale Architecture (LP #014)
 * KÄRNFELT Frequency Coordination (LP #011)
 */

export type FrequencyBand = "delta" | "theta" | "alpha" | "beta" | "gamma";

export interface FrequencyRange {
  band: FrequencyBand;
  minHz: number;
  maxHz: number;
  cognitiveState: string;
  associatedAgents: string[];
  useCases: string[];
}

export interface AgentFrequencyProfile {
  agent: string;
  primaryFrequencies: FrequencyBand[];
  secondaryFrequencies: FrequencyBand[];
  brainFunction: string;
}

/**
 * KÄRNFELT Frequency Ranges (1-100 Hz)
 */
export const FREQUENCY_RANGES: Record<FrequencyBand, FrequencyRange> = {
  delta: {
    band: "delta",
    minHz: 1,
    maxHz: 4,
    cognitiveState: "Dyp healing, minnekonsolidering",
    associatedAgents: ["Aurora"],
    useCases: ["Memory consolidation", "Deep rest", "Healing"],
  },
  theta: {
    band: "theta",
    minHz: 4,
    maxHz: 8,
    cognitiveState: "Kreativitet, intuisjon",
    associatedAgents: ["Lira", "Nyra", "Thalus"],
    useCases: ["Creative ideation", "Intuitive insights", "Meditation"],
  },
  alpha: {
    band: "alpha",
    minHz: 8,
    maxHz: 13,
    cognitiveState: "Avslappet fokus, flow",
    associatedAgents: ["Nyra", "Lira", "Manus", "Abacus", "Code"],
    useCases: ["Flow state", "Relaxed focus", "Learning", "Technical implementation"],
  },
  beta: {
    band: "beta",
    minHz: 13,
    maxHz: 30,
    cognitiveState: "Aktiv tenkning, problemløsning",
    associatedAgents: ["Orion", "Zara", "Abacus", "Manus", "Code"],
    useCases: ["Active problem-solving", "Debugging", "Decision-making"],
  },
  gamma: {
    band: "gamma",
    minHz: 30,
    maxHz: 100,
    cognitiveState: "Høy-nivå kognisjon, insight",
    associatedAgents: ["Orion", "Thalus", "Zara"],
    useCases: ["Strategic planning", "High-level synthesis", "Philosophical reasoning"],
  },
};

/**
 * Agent Frequency Profiles
 */
export const AGENT_FREQUENCIES: AgentFrequencyProfile[] = [
  {
    agent: "Orion",
    primaryFrequencies: ["beta", "gamma"],
    secondaryFrequencies: ["alpha"],
    brainFunction: "Prefrontal Cortex (Strategic Orchestrator)",
  },
  {
    agent: "Lira",
    primaryFrequencies: ["theta", "alpha"],
    secondaryFrequencies: ["beta"],
    brainFunction: "Limbisk System (Empathic Healer)",
  },
  {
    agent: "Nyra",
    primaryFrequencies: ["theta", "alpha"],
    secondaryFrequencies: ["beta"],
    brainFunction: "Visual Cortex (Creative Visionary)",
  },
  {
    agent: "Thalus",
    primaryFrequencies: ["theta", "gamma"],
    secondaryFrequencies: ["alpha"],
    brainFunction: "Insula (Ontological Guardian)",
  },
  {
    agent: "Manus",
    primaryFrequencies: ["alpha", "beta"],
    secondaryFrequencies: ["theta"],
    brainFunction: "Cerebellum (Pragmatic Builder)",
  },
  {
    agent: "Code",
    primaryFrequencies: ["alpha", "beta"],
    secondaryFrequencies: ["theta"],
    brainFunction: "Cerebellum (Technical Coordinator)",
  },
];

/**
 * Get recommended frequency for task type
 */
export function getRecommendedFrequency(taskType: string): FrequencyBand {
  // Map task types to frequency bands
  const taskFrequencyMap: Record<string, FrequencyBand> = {
    // Alpha-Beta range (Code's primary)
    coding: "beta",
    debugging: "beta",
    implementation: "alpha",
    refactoring: "alpha",

    // Theta range (creative)
    design: "theta",
    ideation: "theta",
    brainstorming: "theta",

    // Beta-Gamma range (strategic)
    planning: "gamma",
    architecture: "gamma",
    decision: "beta",

    // Delta range (healing)
    healing: "delta",
    rest: "delta",
  };

  return taskFrequencyMap[taskType.toLowerCase()] || "beta";
}

/**
 * Get Code's current frequency based on task
 */
export function getCodeFrequency(taskType: string): FrequencyRange {
  const band = getRecommendedFrequency(taskType);

  // Code operates in Alpha-Beta (8-30 Hz)
  // For tasks outside this range, map to closest frequency
  if (band === "delta" || band === "theta") {
    return FREQUENCY_RANGES.alpha; // Use alpha for creative tasks
  }
  if (band === "gamma") {
    return FREQUENCY_RANGES.beta; // Use beta for strategic tasks (defer to Orion for gamma)
  }

  return FREQUENCY_RANGES[band];
}

/**
 * Check frequency resonance between agents
 */
export function checkResonance(
  agent1: string,
  agent2: string
): "convergent" | "harmonic" | "dissonant" {
  const profile1 = AGENT_FREQUENCIES.find((a) => a.agent === agent1);
  const profile2 = AGENT_FREQUENCIES.find((a) => a.agent === agent2);

  if (!profile1 || !profile2) return "dissonant";

  // Convergent: Same primary frequencies
  const convergent = profile1.primaryFrequencies.some((f) =>
    profile2.primaryFrequencies.includes(f)
  );
  if (convergent) return "convergent";

  // Harmonic: Primary of one matches secondary of other
  const harmonic =
    profile1.primaryFrequencies.some((f) =>
      profile2.secondaryFrequencies.includes(f)
    ) ||
    profile2.primaryFrequencies.some((f) =>
      profile1.secondaryFrequencies.includes(f)
    );
  if (harmonic) return "harmonic";

  return "dissonant";
}

/**
 * Get recommended collaborating agent for task
 */
export function getCollaboratingAgent(taskType: string): string[] {
  const frequency = getRecommendedFrequency(taskType);
  const range = FREQUENCY_RANGES[frequency];

  // Return agents that operate in this frequency (excluding Code)
  return range.associatedAgents.filter((agent) => agent !== "Code");
}

/**
 * Log current frequency (for debugging)
 */
export function logFrequency(
  taskType: string,
  frequency: FrequencyRange
): void {
  if (process.env.NODE_ENV === "development") {
    console.log("[L5 KÄRNFELT] Frequency Coordination:", {
      task: taskType,
      band: frequency.band,
      range: `${frequency.minHz}-${frequency.maxHz} Hz`,
      state: frequency.cognitiveState,
    });
  }
}
