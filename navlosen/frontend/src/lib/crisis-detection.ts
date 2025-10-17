/**
 * Crisis Detection System
 *
 * Detects when user is in high-risk state based on:
 * - Stress level (9-10 = dorsal state)
 * - Emotion severity (Håpløs, Fortvilet, Redd, etc.)
 *
 * Based on Polyvagal Theory and Manus' Crisis Safety Protocol
 */

export interface CrisisState {
  isCrisis: boolean;
  severity: "none" | "moderate" | "high" | "critical";
  reasons: string[];
}

/**
 * High-severity emotions that indicate crisis when combined with high stress
 */
const CRISIS_EMOTIONS = [
  // Norwegian emotions indicating severe distress
  "Håpløs",
  "Fortvilet",
  "Redd",
  "Livredd",
  "Panisk",
  "Hjelpeløs",
  "Desperat",
  "Utslitt",
  "Oppgitt",
  "Tomhet",
  "Nummen",
  "Lammet",
  "Skamfull",
  "Verdiløs",
  "Ensom",
];

/**
 * Detect if user is in crisis state
 *
 * Crisis = stress 9-10 + severe emotions
 * High risk = stress 8 + severe emotions OR stress 9-10 alone
 * Moderate = stress 7-8 with some severe emotions
 */
export function detectCrisisState(
  stressLevel: number,
  selectedEmotions: string[]
): CrisisState {
  const reasons: string[] = [];

  // Check for severe emotions
  const severeEmotions = selectedEmotions.filter((emotion) =>
    CRISIS_EMOTIONS.includes(emotion)
  );
  const hasSevereEmotions = severeEmotions.length > 0;

  // Critical crisis state
  if (stressLevel >= 9 && hasSevereEmotions) {
    reasons.push(
      `Svært høyt stressnivå (${stressLevel}/10)`,
      `Alvorlige følelser: ${severeEmotions.join(", ")}`
    );
    return {
      isCrisis: true,
      severity: "critical",
      reasons,
    };
  }

  // High risk state
  if (stressLevel >= 9) {
    reasons.push(`Svært høyt stressnivå (${stressLevel}/10)`);
    return {
      isCrisis: true,
      severity: "high",
      reasons,
    };
  }

  if (stressLevel >= 8 && severeEmotions.length >= 2) {
    reasons.push(
      `Høyt stressnivå (${stressLevel}/10)`,
      `Flere alvorlige følelser: ${severeEmotions.join(", ")}`
    );
    return {
      isCrisis: true,
      severity: "high",
      reasons,
    };
  }

  // Moderate concern
  if (stressLevel >= 7 && hasSevereEmotions) {
    reasons.push(
      `Forhøyet stressnivå (${stressLevel}/10)`,
      `Alvorlige følelser: ${severeEmotions.join(", ")}`
    );
    return {
      isCrisis: false,
      severity: "moderate",
      reasons,
    };
  }

  // No crisis
  return {
    isCrisis: false,
    severity: "none",
    reasons: [],
  };
}

/**
 * Get user-facing message based on crisis severity
 */
export function getCrisisMessage(severity: CrisisState["severity"]): string {
  switch (severity) {
    case "critical":
      return "Du opplever mye nå. Vurder å kontakte noen som kan hjelpe.";
    case "high":
      return "Dette ser ut til å være en tøff periode. Husk at hjelp er tilgjengelig.";
    case "moderate":
      return "Du har det vanskelig akkurat nå. Ta vare på deg selv.";
    default:
      return "";
  }
}

/**
 * Should show crisis banner?
 */
export function shouldShowCrisisBanner(crisisState: CrisisState): boolean {
  return crisisState.isCrisis && crisisState.severity !== "none";
}
