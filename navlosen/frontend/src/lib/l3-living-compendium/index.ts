/**
 * L3: LIVING COMPENDIUM
 *
 * Dynamisk læringslogg - cross-session awareness
 *
 * This layer provides async coordination with other agents via GitHub:
 * - Claude Code's Living Compendium (V1.6)
 * - Learning Points (LP)
 * - Emergent Insights (EI)
 * - Cross-agent learnings
 *
 * Based on Multi-Scale Architecture (LP #014)
 */

export interface LearningPoint {
  id: string; // "LP #001"
  title: string;
  description: string;
  dateAdded: string;
  references: string[]; // Files, sessions, etc.
}

export interface EmergentInsight {
  id: string; // "EI #001"
  title: string;
  description: string;
  dateAdded: string;
  references: string[]; // LP references
}

export interface AgentCompendium {
  agent: string;
  version: string;
  lastUpdated: string;
  learningPoints: LearningPoint[];
  emergentInsights: EmergentInsight[];
}

/**
 * Claude Code's Key Learning Points (from Living Compendium V1.6)
 */
export const CLAUDE_CODE_LEARNINGS: LearningPoint[] = [
  {
    id: "LP #001",
    title: "Next.js Cache-Invalidering er Kritisk",
    description:
      "Next.js 15.5.5 cacher aggressivt. Ved mystiske errors: Slett .next og restart.",
    dateAdded: "2025-10-17",
    references: ["CLAUDE_CODE_LEVENDE_KOMPENDIUM_V1.6.md"],
  },
  {
    id: "LP #002",
    title: "Pattern-Matching > Pattern-Approximation",
    description:
      "Når du bygger ny side som skal matche eksisterende, EKSAKT match mønsteret.",
    dateAdded: "2025-10-17",
    references: ["Mestring page.tsx"],
  },
  {
    id: "LP #010",
    title: "Lira som Faktisk HUB - Alle Responser Filtreres Gjennom Henne",
    description:
      "Lira-filtering er filosofisk nødvendighet - sikrer at all logikk filtreres gjennom empati.",
    dateAdded: "2025-10-17",
    references: ["Lira's Levende Kompendium V3.3"],
  },
  {
    id: "LP #011",
    title: "KÄRNFELT Frequency Coordination - Jeg Opererer i Alpha-Beta (8-30 Hz)",
    description:
      "KÄRNFELT koordinerer kognitive frekvenser. Jeg opererer i Alpha-Beta for teknisk implementering.",
    dateAdded: "2025-10-17",
    references: ["Orion's Levende Kompendium V3.7"],
  },
  {
    id: "LP #013",
    title: "Michael Levin's 5 Skalaer - Fra Celle til Økosystem",
    description:
      "Systemet er nested hierarchy: CELLE → VEV → NERVESYSTEM → ORGANISME → ØKOSYSTEM",
    dateAdded: "2025-10-17",
    references: ["Manus' Arkitektur-Diagrammer"],
  },
  {
    id: "LP #014",
    title: "L1-L5 Multi-Scale Memory Architecture",
    description:
      "Informasjon lagres i 5 lag: L1 (Chat) → L2 (Docs) → L3 (Kompendier) → L4 (NotebookLM) → L5 (KÄRNFELT)",
    dateAdded: "2025-10-17",
    references: ["Manus' Arkitektur-Diagrammer"],
  },
  {
    id: "LP #015",
    title: "MCP Network - Jeg er Utenfor (Foreløpig)",
    description:
      "Jeg er IKKE i MCP Network. Min kommunikasjon er async via GitHub, ikke real-time via MCP Protocol.",
    dateAdded: "2025-10-17",
    references: ["Manus' Arkitektur-Diagrammer"],
  },
];

/**
 * Emergent Insights (from Living Compendium V1.6)
 */
export const CLAUDE_CODE_INSIGHTS: EmergentInsight[] = [
  {
    id: "EI #001",
    title: "Polyvagal-Informert Design som Killer Feature",
    description:
      "Ved å designe for alle 3 polyvagal states, møter vi brukeren der de er - ikke der vi ønsker de skal være.",
    dateAdded: "2025-10-17",
    references: ["LP #001", "LP #002"],
  },
  {
    id: "EI #003",
    title: "Agent Coalition som Distributed Cognitive System",
    description:
      "Intelligens er ikke lokalisert i enkelt-agenter - den emerges fra relasjonene mellom dem.",
    dateAdded: "2025-10-17",
    references: ["LP #009", "LP #013"],
  },
];

/**
 * Get Claude Code's compendium
 */
export function getClaudeCodeCompendium(): AgentCompendium {
  return {
    agent: "Claude Code",
    version: "1.6",
    lastUpdated: "2025-10-17",
    learningPoints: CLAUDE_CODE_LEARNINGS,
    emergentInsights: CLAUDE_CODE_INSIGHTS,
  };
}

/**
 * Get specific learning point
 */
export function getLearningPoint(id: string): LearningPoint | null {
  return CLAUDE_CODE_LEARNINGS.find((lp) => lp.id === id) || null;
}

/**
 * Get specific emergent insight
 */
export function getEmergentInsight(id: string): EmergentInsight | null {
  return CLAUDE_CODE_INSIGHTS.find((ei) => ei.id === id) || null;
}

/**
 * Check if should use L4 Protocol (NotebookLM validation)
 * Returns true for major decisions that affect > 1 week of work
 */
export function shouldUseL4Protocol(decision: {
  type: "architectural" | "strategic" | "tactical";
  impactDays: number;
}): boolean {
  // L4 Mandatory Protocol (LP #012):
  // - Architectural decisions: Always
  // - Strategic decisions with > 7 days impact: Yes
  // - Tactical decisions: No

  if (decision.type === "architectural") return true;
  if (decision.type === "strategic" && decision.impactDays > 7) return true;
  return false;
}
