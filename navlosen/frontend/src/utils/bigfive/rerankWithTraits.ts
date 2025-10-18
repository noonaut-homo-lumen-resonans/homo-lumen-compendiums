import { BigFive, Recommendation } from "@/types";

/**
 * Re-rank recommendations using Big Five traits as weak tie-breaker
 *
 * Design principles:
 * - State-first: Polyvagal state + quadrant determine primary ranking
 * - Trait whisper: OCEAN used only when recommendations are similarly good (≤10% boost)
 * - Transparency: Returns explanation for why ranking changed
 *
 * Trait → Recommendation type mapping (from Lira's guidance):
 * - High C → Structured, measurable exercises
 * - High O → Reflection, learning, new content
 * - High E → Social, active intervention
 * - High A → Relational warmth, self-care
 * - High N → Low-threshold safety/grounding
 *
 * @param recommendations - Initial recommendations (sorted by state-based priority)
 * @param bigFive - User's Big Five profile (optional)
 * @returns Re-ranked recommendations with explanations
 *
 * Triadisk Score: 0.13 (PROCEED)
 */

interface RankedRecommendation extends Recommendation {
  adjustedPriority: number;
  traitBoost: number;
  explanation?: string;
}

const MAX_TRAIT_BOOST = 0.1; // 10% maximum boost from traits

export function rerankWithTraits(
  recommendations: Recommendation[],
  bigFive?: BigFive
): RankedRecommendation[] {
  // No Big Five data → return original ranking
  if (!bigFive) {
    return recommendations.map((rec) => ({
      ...rec,
      adjustedPriority: rec.priority,
      traitBoost: 0,
    }));
  }

  // Calculate trait boost for each recommendation
  const rankedRecs: RankedRecommendation[] = recommendations.map((rec) => {
    const boost = calculateTraitBoost(rec, bigFive);
    return {
      ...rec,
      traitBoost: boost,
      adjustedPriority: rec.priority * (1 + boost),
      explanation: boost > 0.02 ? generateExplanation(rec, bigFive) : undefined,
    };
  });

  // Sort by adjusted priority (descending)
  rankedRecs.sort((a, b) => b.adjustedPriority - a.adjustedPriority);

  return rankedRecs;
}

/**
 * Calculate trait boost for a recommendation
 *
 * Returns value in [0, MAX_TRAIT_BOOST]
 */
function calculateTraitBoost(
  recommendation: Recommendation,
  bigFive: BigFive
): number {
  let boost = 0;

  const O = bigFive.O ?? 0.5;
  const C = bigFive.C ?? 0.5;
  const E = bigFive.E ?? 0.5;
  const A = bigFive.A ?? 0.5;
  const N = bigFive.N ?? 0.5;

  switch (recommendation.type) {
    case "exercise":
      // Physical exercises benefit from C (structure) and E (energy)
      boost += (C - 0.5) * 0.15;
      boost += (E - 0.5) * 0.10;
      // High N prefers gentler exercises
      boost -= (N - 0.5) * 0.05;
      break;

    case "practice":
      // Practices (meditation, breathing) benefit from C and low N
      boost += (C - 0.5) * 0.12;
      boost += (0.5 - N) * 0.08; // Lower N → higher boost
      break;

    case "knowledge":
      // Learning content benefits from O (curiosity)
      boost += (O - 0.5) * 0.20;
      break;

    case "music":
      // Music/frequency benefits from O and low N
      boost += (O - 0.5) * 0.10;
      boost += (0.5 - N) * 0.10;
      break;

    case "context":
      // Contextual recommendations (relational, social) benefit from E and A
      boost += (E - 0.5) * 0.15;
      boost += (A - 0.5) * 0.12;
      break;

    default:
      boost = 0;
  }

  // Clamp to [0, MAX_TRAIT_BOOST]
  return Math.max(0, Math.min(MAX_TRAIT_BOOST, boost));
}

/**
 * Generate human-readable explanation for trait-based boost
 */
function generateExplanation(
  recommendation: Recommendation,
  bigFive: BigFive
): string {
  const explanations: string[] = [];

  const O = bigFive.O ?? 0.5;
  const C = bigFive.C ?? 0.5;
  const E = bigFive.E ?? 0.5;
  const A = bigFive.A ?? 0.5;
  const N = bigFive.N ?? 0.5;

  if (O > 0.7 && recommendation.type === "knowledge") {
    explanations.push("Passer din nysgjerrighet og åpenhet");
  }

  if (C > 0.7 && ["exercise", "practice"].includes(recommendation.type)) {
    explanations.push("Passer din strukturerte tilnærming");
  }

  if (E > 0.7 && recommendation.type === "context") {
    explanations.push("Passer din utadvendte energi");
  }

  if (A > 0.7 && recommendation.type === "context") {
    explanations.push("Passer din omsorgsfullhet");
  }

  if (N > 0.7 && ["practice", "music"].includes(recommendation.type)) {
    explanations.push("Rolig tilnærming som passer din følsomhet");
  }

  return explanations.length > 0
    ? explanations.join(", ")
    : "Personalisert basert på din profil";
}

/**
 * Get textual summary of how traits influenced ranking
 */
export function getRerankSummary(bigFive?: BigFive): string {
  if (!bigFive) {
    return "Anbefalinger basert kun på din følelsestilstand (ingen personlighetsprofil).";
  }

  const traits: string[] = [];

  if ((bigFive.O ?? 0.5) > 0.65) traits.push("høy åpenhet");
  if ((bigFive.C ?? 0.5) > 0.65) traits.push("strukturert");
  if ((bigFive.E ?? 0.5) > 0.65) traits.push("utadvendt");
  if ((bigFive.A ?? 0.5) > 0.65) traits.push("omsorgsfull");
  if ((bigFive.N ?? 0.5) > 0.65) traits.push("følsom");

  if (traits.length === 0) {
    return "Anbefalinger primært basert på din følelsestilstand, med små justeringer fra personlighet.";
  }

  return `Anbefalinger tilpasset din tilstand + personlighet (${traits.join(", ")}). Personlighet gir ≤10% justering.`;
}
