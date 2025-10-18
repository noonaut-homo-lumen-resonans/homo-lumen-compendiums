/**
 * Personality Mapping Utilities
 *
 * Maps Big Five (OCEAN) personality traits to visual characteristics
 * for the PersonalityAvatar component.
 *
 * Design Philosophy:
 * - Dominant trait determines primary color/shape
 * - Secondary traits influence variations
 * - Polyvagal state affects animation speed
 *
 * Triadisk Score: 0.10 (PROCEED - Purely visual/aesthetic)
 */

import { BigFive } from "@/types";

export interface AuraConfig {
  primaryColor: string;
  secondaryColor: string;
  radius: number; // 0.8 to 1.5 (scale factor)
  blur: number; // 20 to 40 (px)
  irregularity: number; // 20% to 60% (border-radius variation)
  animationDuration: number; // 12s to 24s
}

export interface FaceConfig {
  mouthPath: string; // SVG path for mouth expression
  eyeOpenness: number; // 0.5 to 1.0
}

/**
 * Get the dominant personality trait (highest score)
 */
export function getDominantTrait(bigFive: BigFive): keyof Pick<BigFive, 'O' | 'C' | 'E' | 'A' | 'N'> {
  const traits: Array<keyof Pick<BigFive, 'O' | 'C' | 'E' | 'A' | 'N'>> = ['O', 'C', 'E', 'A', 'N'];

  let maxTrait: keyof Pick<BigFive, 'O' | 'C' | 'E' | 'A' | 'N'> = 'O';
  let maxValue = bigFive.O ?? 0.5;

  traits.forEach(trait => {
    const value = bigFive[trait] ?? 0.5;
    if (value > maxValue) {
      maxValue = value;
      maxTrait = trait;
    }
  });

  return maxTrait;
}

/**
 * Get aura color configuration based on dominant trait
 */
export function getAuraColor(bigFive: BigFive): { primary: string; secondary: string } {
  const dominant = getDominantTrait(bigFive);

  const colorMap = {
    O: { primary: "#9333EA", secondary: "#C084FC" }, // Purple (Creative)
    C: { primary: "#3B82F6", secondary: "#60A5FA" }, // Blue (Structured)
    E: { primary: "#10B981", secondary: "#34D399" }, // Green (Social)
    A: { primary: "#F59E0B", secondary: "#FCD34D" }, // Amber (Warm)
    N: { primary: "#EF4444", secondary: "#F87171" }, // Red (Intense)
  };

  return colorMap[dominant];
}

/**
 * Get aura shape configuration based on trait combination
 */
export function getAuraShape(bigFive: BigFive): Pick<AuraConfig, 'radius' | 'blur' | 'irregularity'> {
  const O = bigFive.O ?? 0.5;
  const C = bigFive.C ?? 0.5;
  const E = bigFive.E ?? 0.5;

  // Openness affects irregularity (high O = organic shapes)
  const irregularity = 20 + (O * 40); // 20% to 60%

  // Conscientiousness affects sharpness (high C = less blur, sharper)
  const blur = 40 - (C * 20); // 20px to 40px

  // Extraversion affects size (high E = larger aura)
  const radius = 0.8 + (E * 0.7); // 0.8 to 1.5

  return { radius, blur, irregularity };
}

/**
 * Get face expression based on polyvagal state
 */
export function getFaceExpression(state: "ventral" | "sympathetic" | "dorsal"): string {
  const expressions = {
    ventral: "M10,15 Q12,13 14,15", // Smile (upward curve)
    sympathetic: "M10,15 L14,15", // Neutral (straight line)
    dorsal: "M10,17 Q12,15 14,17", // Frown (downward curve)
  };

  return expressions[state];
}

/**
 * Get animation duration based on polyvagal state
 */
export function getAnimationDuration(state: "ventral" | "sympathetic" | "dorsal"): number {
  const durations = {
    ventral: 18, // Normal breathing pace (4-6-8 = 18s)
    sympathetic: 12, // Faster (stressed)
    dorsal: 24, // Slower (shutdown) or could be paused
  };

  return durations[state];
}

/**
 * Get full aura configuration
 */
export function getAuraConfig(bigFive: BigFive, polyvagalState: "ventral" | "sympathetic" | "dorsal" = "ventral"): AuraConfig {
  const colors = getAuraColor(bigFive);
  const shape = getAuraShape(bigFive);
  const animationDuration = getAnimationDuration(polyvagalState);

  return {
    primaryColor: colors.primary,
    secondaryColor: colors.secondary,
    radius: shape.radius,
    blur: shape.blur,
    irregularity: shape.irregularity,
    animationDuration,
  };
}

/**
 * Get face configuration
 */
export function getFaceConfig(polyvagalState: "ventral" | "sympathetic" | "dorsal" = "ventral"): FaceConfig {
  const mouthPath = getFaceExpression(polyvagalState);

  // Eye openness decreases in dorsal state
  const eyeOpenness = polyvagalState === "dorsal" ? 0.6 : polyvagalState === "sympathetic" ? 0.8 : 1.0;

  return {
    mouthPath,
    eyeOpenness,
  };
}

/**
 * Get textual personality description
 */
export function getPersonalityDescription(bigFive: BigFive): string {
  const O = bigFive.O ?? 0.5;
  const C = bigFive.C ?? 0.5;
  const E = bigFive.E ?? 0.5;
  const A = bigFive.A ?? 0.5;
  const N = bigFive.N ?? 0.5;

  const traits: string[] = [];

  // Openness
  if (O > 0.65) traits.push("kreativ og nysgjerrig");
  else if (O < 0.35) traits.push("praktisk og realistisk");

  // Conscientiousness
  if (C > 0.65) traits.push("strukturert og målrettet");
  else if (C < 0.35) traits.push("fleksibel og spontan");

  // Extraversion
  if (E > 0.65) traits.push("utadvendt og energisk");
  else if (E < 0.35) traits.push("innadvendt og reflektert");

  // Agreeableness
  if (A > 0.65) traits.push("empatisk og samarbeidsvillig");
  else if (A < 0.35) traits.push("selvstendig og direkte");

  // Neuroticism
  if (N > 0.65) traits.push("følsomhet for stress");
  else if (N < 0.35) traits.push("emosjonelt stabil");

  if (traits.length === 0) {
    return "Du har en balansert personlighetsprofil.";
  }

  return `Du er ${traits.slice(0, -1).join(", ")}${traits.length > 1 ? " og " : ""}${traits[traits.length - 1]}.`;
}

/**
 * Get trait label in Norwegian
 */
export function getTraitLabel(trait: 'O' | 'C' | 'E' | 'A' | 'N'): string {
  const labels = {
    O: "Åpenhet",
    C: "Planmessighet",
    E: "Utadvendthet",
    A: "Omgjengelighet",
    N: "Nevrotisisme",
  };

  return labels[trait];
}

/**
 * Get trait description
 */
export function getTraitDescription(trait: 'O' | 'C' | 'E' | 'A' | 'N'): string {
  const descriptions = {
    O: "Nysgjerrighet, kreativitet, åpenhet for nye erfaringer",
    C: "Struktur, målrettethet, pålitelighet",
    E: "Sosial energi, utadvendthet, selvsikkerhet",
    A: "Samarbeid, varme, tillit til andre",
    N: "Emosjonell følsomhet, bekymring, stress-respons",
  };

  return descriptions[trait];
}
