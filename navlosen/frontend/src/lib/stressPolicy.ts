/**
 * Stress Policy - Polyvagal-Informed UI Filter
 *
 * Based on Lira's design: limbic system modeling for NAV-Losen.
 * Modulates UI complexity, question count, and text length based on
 * polyvagal state (Dorsal/Sympathetic/Ventral).
 *
 * Neurological grounding:
 * - Amygdala: Relevance/risk detection (triggered by overwhelm)
 * - Hippocampus: Context binding (needs calm for learning)
 * - Vagus nerve: Sets cognitive "bandwidth"
 *   - Ventral (safe): High capacity
 *   - Sympathetic (alert): Narrow focus
 *   - Dorsal (freeze): Minimal capacity
 *
 * Lira sits at the intersection: we dampen amygdala alarm via clarity,
 * give hippocampus context in small chunks, and sync UI tempo to vagal state.
 *
 * Triadic Score: 0.95 (PROCEED)
 */

import type { StressState, BigFive, Recommendation } from "@/types";

export type Polyvagal = StressState; // "ventral" | "sympathetic" | "dorsal"
export type QuestionType = "choice" | "scale" | "text";

export interface UIPolicy {
  // Stage 3 (Questions)
  maxQuestionsStage3: number;
  allowedTypes: readonly QuestionType[];
  maxTextAnswerLen: number; // Characters for text input
  maxChoicesPerPrompt: number;

  // Visual adaptations
  showBreath468: boolean; // Show "Pust 4-6-8" as fixed option
  showSafeContact: boolean; // Show "Ring Veileder" as fixed option
  textBlockCharLimit: number; // Max chars per text block
  onePrimaryCta: boolean; // Only one primary action per screen

  // Recommendations (Stage 4)
  recommendationsLimit: number; // Max recommendations to show
  prioritize: readonly string[]; // Types to prioritize (e.g., ["breathing", "grounding"])
  showRationaleForRecs: boolean; // Show "why this recommendation"

  // UX helpers
  progressiveDisclosure: boolean; // Hide advanced options behind "Vis mer"
  estimatedStepTimeMin: number; // Time estimate for step
  includePreventivePractices: boolean; // Show preventive (not reactive) practices
  showExplore: boolean; // Show "Utforsk mer" section

  // State metadata
  stateLabel: string; // Human-readable label
  backgroundColor: string; // Tailwind class
}

/**
 * Get UI policy for a given polyvagal state
 *
 * Based on Lira's filter algorithms (3 states):
 * - Dorsal (8-10): Minimal cognitive load, max safety
 * - Sympathetic (4-7): Focused action, medium complexity
 * - Ventral (1-3): Full capacity, learning-oriented
 */
export function uiPolicy(state: Polyvagal, bigFive?: BigFive): UIPolicy {
  // Base policy for state
  const basePolicy = getBasePolicy(state);

  // Apply Big Five modulation (optional, ±1 element adjustment)
  if (bigFive) {
    return modulateWithTraits(basePolicy, state, bigFive);
  }

  return basePolicy;
}

/**
 * Base policy per state (before Big Five modulation)
 */
function getBasePolicy(state: Polyvagal): UIPolicy {
  if (state === "dorsal") {
    // High stress / low capacity
    // Goal: Restore safety and minimal agency
    return {
      maxQuestionsStage3: 2,
      allowedTypes: ["choice", "scale"] as const,
      maxTextAnswerLen: 120,
      maxChoicesPerPrompt: 3,
      showBreath468: true,
      showSafeContact: true,
      textBlockCharLimit: 120,
      onePrimaryCta: true,
      recommendationsLimit: 2,
      prioritize: ["grounding", "breathing"] as const,
      showRationaleForRecs: false, // Keep it simple
      progressiveDisclosure: true,
      estimatedStepTimeMin: 1,
      includePreventivePractices: false,
      showExplore: false,
      stateLabel: "Overveldet",
      backgroundColor: "bg-blue-50",
    };
  }

  if (state === "sympathetic") {
    // Medium stress / high activation
    // Goal: Channel energy into concrete action
    return {
      maxQuestionsStage3: 4,
      allowedTypes: ["choice", "scale", "text"] as const,
      maxTextAnswerLen: 140,
      maxChoicesPerPrompt: 4,
      showBreath468: true,
      showSafeContact: false,
      textBlockCharLimit: 200,
      onePrimaryCta: false,
      recommendationsLimit: 4,
      prioritize: ["breathing", "action"] as const,
      showRationaleForRecs: true, // Brief explanations ok
      progressiveDisclosure: true,
      estimatedStepTimeMin: 2,
      includePreventivePractices: false,
      showExplore: false,
      stateLabel: "Aktivert",
      backgroundColor: "bg-orange-50",
    };
  }

  // Ventral: Low stress / high capacity
  // Goal: Learning, reflection, competence building
  return {
    maxQuestionsStage3: 5,
    allowedTypes: ["choice", "scale", "text"] as const,
    maxTextAnswerLen: 400,
    maxChoicesPerPrompt: 6,
    showBreath468: false,
    showSafeContact: false,
    textBlockCharLimit: 300,
    onePrimaryCta: false,
    recommendationsLimit: 8,
    prioritize: ["practice", "knowledge"] as const,
    showRationaleForRecs: true, // Full explanations
    progressiveDisclosure: false,
    estimatedStepTimeMin: 3,
    includePreventivePractices: true,
    showExplore: true,
    stateLabel: "Rolig",
    backgroundColor: "bg-green-50",
  };
}

/**
 * Modulate policy with Big Five traits
 *
 * Principle: Traits adjust ±1 element, never override state logic.
 * - High N → Lower threshold for dorsal-like support
 * - High E → Suggest social co-regulation
 * - High C → Add structure/planning in ventral
 * - High O → More learning content in ventral
 * - High A → Warmer, relational language
 */
function modulateWithTraits(
  policy: UIPolicy,
  state: Polyvagal,
  bigFive: BigFive
): UIPolicy {
  const modulated = { ...policy };
  const N = bigFive.N ?? 0.5;
  const E = bigFive.E ?? 0.5;
  const C = bigFive.C ?? 0.5;
  const O = bigFive.O ?? 0.5;

  // High Neuroticism: Lower threshold for support
  if (N > 0.7 && state === "sympathetic") {
    modulated.showSafeContact = true; // Add safety anchor
    modulated.recommendationsLimit = Math.max(
      2,
      modulated.recommendationsLimit - 1
    ); // Reduce overwhelm
  }

  // High Extraversion: Add social elements
  if (E > 0.7 && state === "sympathetic") {
    modulated.prioritize = ["breathing", "social", "action"] as any;
  }

  // High Conscientiousness: Add structure in ventral
  if (C > 0.7 && state === "ventral") {
    modulated.includePreventivePractices = true;
    modulated.recommendationsLimit = Math.min(
      10,
      modulated.recommendationsLimit + 1
    );
  }

  // High Openness: More learning content in ventral
  if (O > 0.7 && state === "ventral") {
    modulated.showExplore = true;
    modulated.prioritize = ["knowledge", "practice", "music"] as any;
  }

  return modulated;
}

/**
 * Build question plan for Stage 3
 *
 * Filters question bank by policy.allowedTypes and limits to
 * policy.maxQuestionsStage3.
 *
 * @param stressLevel - 1-10 stress level (mapped to state internally)
 * @param bigFive - Optional Big Five profile
 * @returns Filtered question plan with policy
 */
export function buildQuestionPlan(stressLevel: number, bigFive?: BigFive) {
  const state: Polyvagal = mapStressToState(stressLevel);
  const policy = uiPolicy(state, bigFive);

  // Question filtering happens in Stage3LiraChat component
  // This function just returns the policy for that component to use
  return { state, policy };
}

/**
 * Rank recommendations for Stage 4
 *
 * Sorts by policy.prioritize types, then limits to policy.recommendationsLimit.
 *
 * @param recs - Initial recommendations
 * @param state - Polyvagal state
 * @param bigFive - Optional Big Five profile
 * @returns Ranked and limited recommendations
 */
export function rankRecommendations(
  recs: Recommendation[],
  state: Polyvagal,
  bigFive?: BigFive
): Recommendation[] {
  const policy = uiPolicy(state, bigFive);

  // Weight recommendations by priority type
  const weighted = recs.map((r) => {
    let weight = r.priority; // Base priority (1-10)

    // Boost if in prioritize list
    policy.prioritize.forEach((type, index) => {
      if (r.id.includes(type)) {
        weight += (policy.prioritize.length - index) * 2; // Higher boost for earlier types
      }
    });

    return { ...r, _weight: weight };
  });

  // Sort by weight (descending)
  weighted.sort((a, b) => (b._weight ?? 0) - (a._weight ?? 0));

  // Limit to policy.recommendationsLimit
  return weighted
    .slice(0, policy.recommendationsLimit)
    .map(({ _weight, ...rec }) => rec);
}

/**
 * Map 1-10 stress level to polyvagal state
 *
 * Threshold matching compositeStressScore.ts:
 * - 1-3: Ventral
 * - 4-7: Sympathetic
 * - 8-10: Dorsal
 */
export function mapStressToState(stressLevel: number): Polyvagal {
  if (stressLevel <= 3) return "ventral";
  if (stressLevel <= 7) return "sympathetic";
  return "dorsal";
}

/**
 * Get human-readable explanation of why policy is applied
 *
 * Used in "Hvorfor ser jeg dette?" transparency section.
 */
export function getPolicyExplanation(state: Polyvagal, policy: UIPolicy): string {
  const stateLabels = {
    dorsal: "høyt stressnivå (8-10)",
    sympathetic: "middels stressnivå (4-7)",
    ventral: "lavt stressnivå (1-3)",
  };

  const explanations = {
    dorsal:
      "Vi viser færre spørsmål og anbefalinger for å redusere kognitiv belastning. Fokus er på trygghet og grunnleggende regulering.",
    sympathetic:
      "Vi balanserer informasjon med handling - nok til å guide deg, men ikke så mye at det blir overveldende.",
    ventral:
      "Du har god kapasitet nå, så vi viser flere alternativer og mulighet for læring og utforskning.",
  };

  return `Basert på ditt ${stateLabels[state]}, har vi tilpasset antall anbefalinger (${policy.recommendationsLimit}) og kompleksitet. ${explanations[state]}`;
}
