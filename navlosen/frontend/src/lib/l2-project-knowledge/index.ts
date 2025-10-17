/**
 * L2: PROJECT KNOWLEDGE
 *
 * Agent-spesifikk kunnskap - statisk kompendium
 *
 * This layer contains NAV-Losen's core knowledge:
 * - Design System principles
 * - Polyvagal Theory guidelines
 * - Development patterns
 * - Component library reference
 *
 * Based on Multi-Scale Architecture (LP #014)
 */

export interface ProjectKnowledge {
  // Design System version
  designSystemVersion: string;

  // Polyvagal Theory principles
  polyvagalPrinciples: {
    dorsal: PolyvagalState;
    sympathetic: PolyvagalState;
    ventral: PolyvagalState;
  };

  // Component library
  components: ComponentReference[];

  // Development patterns
  patterns: DevelopmentPattern[];
}

export interface PolyvagalState {
  name: string;
  description: string;
  stressRange: [number, number]; // [min, max]
  backgroundColor: string;
  uiPrinciples: string[];

  // Exact UI specifications from "Our Ethical Compass"
  touchTargetSize: number; // pixels
  maxChoices: number | "unlimited";
  taskDuration: number | null; // seconds (null = blocked)
  prominentButtons: string[]; // e.g., ["Ring Veileder"]
  cognitiveTasks: "blocked" | "simplified" | "full";
  microcopy: "shame-free" | "supportive" | "collaborative";
}

export interface ComponentReference {
  name: string;
  path: string;
  category: "layout" | "mestring" | "flow" | "music" | "safety" | "ui";
  description: string;
}

export interface DevelopmentPattern {
  name: string;
  description: string;
  example: string;
  references: string[]; // LP #001, SMK #002, etc.
}

/**
 * NAV-Losen Project Knowledge (Static)
 */
export const NAV_LOSEN_KNOWLEDGE: ProjectKnowledge = {
  designSystemVersion: "1.0",

  polyvagalPrinciples: {
    dorsal: {
      name: "Dorsal (Shutdown)",
      description: "Overvelmet, shutdown - trenger trygg havn",
      stressRange: [8, 10],
      backgroundColor: "green-50", // Calming forest green (from "Our Ethical Compass")
      uiPrinciples: [
        "Minimalt valg (1-2 max)",
        "Extra-large touch targets",
        "Minimal text",
        "Prominent 'Ring Veileder' button",
      ],

      // Exact specs from "Our Ethical Compass" document
      touchTargetSize: 72, // pixels - extra-large for easy tapping
      maxChoices: 2, // Only 1-2 simple options
      taskDuration: null, // Cognitive tasks are BLOCKED
      prominentButtons: ["Ring Veileder"], // "Call Advisor" is highly visible
      cognitiveTasks: "blocked", // Avoid cognitive demands
      microcopy: "shame-free", // "I see that this is a lot" (not "You're too stressed")
    },
    sympathetic: {
      name: "Sympatisk (Fight/Flight)",
      description: "Stresset, aktiv - trenger mikro-fokus",
      stressRange: [4, 7],
      backgroundColor: "orange-50", // Action-oriented orange/blue (from "Our Ethical Compass")
      uiPrinciples: [
        "Ett mikro-steg av gangen (90 sekunder)",
        "Tydelig feedback",
        "Større buttons (56px)",
        "Max 3 valg",
      ],

      // Exact specs from "Our Ethical Compass" document
      touchTargetSize: 56, // pixels - larger for stressed state
      maxChoices: 3, // Maximum 3 choices
      taskDuration: 90, // Each micro-task ≤ 90 seconds
      prominentButtons: [], // No specific prominent buttons
      cognitiveTasks: "simplified", // Break into micro-steps
      microcopy: "supportive", // "Let's take the first, smallest step"
    },
    ventral: {
      name: "Ventral (Safe & Social)",
      description: "Rolig, oversikt - kan håndtere kompleksitet",
      stressRange: [1, 3],
      backgroundColor: "white", // Light, open near-white (from "Our Ethical Compass")
      uiPrinciples: [
        "Full funksjonalitet",
        "Flere valg og detaljer",
        "Exploratory UI",
        "Advanced features",
      ],

      // Exact specs from "Our Ethical Compass" document
      touchTargetSize: 44, // pixels - normal touch target
      maxChoices: "unlimited", // Show all details and options
      taskDuration: null, // No restriction on task duration
      prominentButtons: [], // No specific prominent buttons
      cognitiveTasks: "full", // Full functionality available
      microcopy: "collaborative", // Like a helpful partner
    },
  },

  components: [
    // Layout
    {
      name: "Layout",
      path: "@/components/layout/Layout",
      category: "layout",
      description: "Main layout wrapper with Header, Sidebar, Footer",
    },
    {
      name: "Header",
      path: "@/components/layout/Header",
      category: "layout",
      description: "Fixed top header (64px)",
    },
    {
      name: "Sidebar",
      path: "@/components/layout/Sidebar",
      category: "layout",
      description: "Navigation sidebar (240px desktop, overlay mobile)",
    },
    {
      name: "DisclaimerFooter",
      path: "@/components/layout/DisclaimerFooter",
      category: "layout",
      description: "Disclaimer footer with crisis resources",
    },

    // Mestring (Crown Jewel!)
    {
      name: "EmotionQuadrant",
      path: "@/components/mestring/EmotionQuadrant",
      category: "mestring",
      description: "Circumplex emotion selection",
    },
    {
      name: "StressSlider",
      path: "@/components/mestring/StressSlider",
      category: "mestring",
      description: "1-10 polyvagal stress level slider",
    },
    {
      name: "SomaticSignals",
      path: "@/components/mestring/SomaticSignals",
      category: "mestring",
      description: "Body awareness checkbox",
    },
    {
      name: "StrategyCard",
      path: "@/components/mestring/StrategyCard",
      category: "mestring",
      description: "Regulation strategy card",
    },
    {
      name: "MasteryLog",
      path: "@/components/mestring/MasteryLog",
      category: "mestring",
      description: "User's personal mastery log",
    },
    {
      name: "BiofeltCheckpoint",
      path: "@/components/mestring/BiofeltCheckpoint",
      category: "mestring",
      description: "4-6-8 breathing exercise",
    },
    {
      name: "JourneySuccess",
      path: "@/components/mestring/JourneySuccess",
      category: "mestring",
      description: "Journey celebration component",
    },

    // Safety
    {
      name: "ConsentModal",
      path: "@/components/safety/ConsentModal",
      category: "safety",
      description: "User consent modal",
    },
    {
      name: "CrisisBanner",
      path: "@/components/safety/CrisisBanner",
      category: "safety",
      description: "Crisis resources banner",
    },
  ],

  patterns: [
    {
      name: "Next.js Cache Invalidation",
      description: "Delete .next folder when encountering ghost errors",
      example: "rm -rf .next && npm run dev",
      references: ["LP #001"],
    },
    {
      name: "Pattern Matching > Approximation",
      description:
        "When building new pages, EXACTLY match reference page structure",
      example: "Copy exact layout from Mestring page, then adapt content",
      references: ["LP #002"],
    },
    {
      name: "Polyvagal-Adaptive Background",
      description: "Change background color based on stress level",
      example:
        "bg-white (ventral), bg-orange-50 (sympathetic), bg-green-50 (dorsal)",
      references: ["EI #001"],
    },
    {
      name: "Lira-Filter Before Response",
      description: "Ask: Would Lira approve this response?",
      example: "Is it empathy-first? Validation before instruction?",
      references: ["LP #010"],
    },
    {
      name: "Triadic Ethics Validation (Mandatory Quality Gate)",
      description:
        "ALL features must pass 3 ethical checks before implementation",
      example:
        "1. Cognitive Sovereignty: Does this give user control? 2. Ontological Coherence: Does this treat user with dignity? 3. Regenerative Healing: Does this build user's capacity?",
      references: ["Our Ethical Compass", "10 Viktigste Beslutninger #5"],
    },
    {
      name: "To-Fase Protokoll (Intelligence → Synthesis)",
      description:
        "Always gather ALL context BEFORE making decisions. 30-50% better efficiency, 60-80% better error detection.",
      example:
        "Fase 1: Glob/Grep/Read to gather context. Fase 2: Edit/Write based on Fase 1.",
      references: ["10 Viktigste Beslutninger #1"],
    },
    {
      name: "Epistemisk Integritet (Document/Estimate/Project)",
      description:
        "Mark all information with evidensgrad to preserve credibility",
      example:
        "✅ Dokumentert (implemented), 🔶 Estimert (informed guess), 🔮 Projisert (future vision)",
      references: ["10 Viktigste Beslutninger #5"],
    },
  ],
};

/**
 * Get project knowledge
 */
export function getProjectKnowledge(): ProjectKnowledge {
  return NAV_LOSEN_KNOWLEDGE;
}

/**
 * Get polyvagal state configuration
 */
export function getPolyvagalState(
  stressLevel: number
): PolyvagalState | null {
  const knowledge = getProjectKnowledge();

  if (stressLevel <= 3) return knowledge.polyvagalPrinciples.ventral;
  if (stressLevel <= 7) return knowledge.polyvagalPrinciples.sympathetic;
  return knowledge.polyvagalPrinciples.dorsal;
}

/**
 * Get component reference by name
 */
export function getComponentReference(
  name: string
): ComponentReference | null {
  const knowledge = getProjectKnowledge();
  return knowledge.components.find((c) => c.name === name) || null;
}
