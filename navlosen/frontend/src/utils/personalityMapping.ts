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
 * Get face configuration based on personality traits (primary) and polyvagal state (secondary)
 *
 * Design decision: Personality determines baseline expression, polyvagal state modulates it
 * - High E+A = friendly smile (regardless of current state)
 * - High N or low polyvagal = slightly dampened expression
 */
export function getFaceConfig(
  polyvagalState: "ventral" | "sympathetic" | "dorsal" = "ventral",
  bigFive?: BigFive
): FaceConfig {
  let mouthPath: string;
  let eyeOpenness: number;

  // If BigFive data available, use personality traits to determine baseline expression
  if (bigFive) {
    const E = bigFive.E ?? 0.5; // Extraversion
    const A = bigFive.A ?? 0.5; // Agreeableness
    const N = bigFive.N ?? 0.5; // Neuroticism

    // High Extraversion + Agreeableness = warm, friendly smile
    // Low Extraversion = more neutral/reserved expression
    const friendliness = (E + A) / 2;

    if (friendliness > 0.6) {
      // Friendly smile (high E+A)
      mouthPath = "M10,15 Q12,13 14,15"; // Smile
      eyeOpenness = 1.0; // Wide, friendly eyes
    } else if (friendliness > 0.4) {
      // Gentle/neutral expression (moderate E+A)
      mouthPath = "M10,15 Q12,14 14,15"; // Slight smile
      eyeOpenness = 0.9;
    } else {
      // Reserved/serious expression (low E+A)
      mouthPath = "M10,15 L14,15"; // Neutral line
      eyeOpenness = 0.8;
    }

    // Neuroticism dampens expression slightly (worried/tense)
    if (N > 0.7) {
      eyeOpenness = Math.max(0.7, eyeOpenness - 0.1);
    }

    // Polyvagal state can modulate but not override personality
    // Only in extreme dorsal state (shutdown), show slight dampening
    if (polyvagalState === "dorsal") {
      eyeOpenness = Math.max(0.6, eyeOpenness - 0.2);
    }
  } else {
    // Fallback: Use only polyvagal state (old behavior)
    mouthPath = getFaceExpression(polyvagalState);
    eyeOpenness = polyvagalState === "dorsal" ? 0.6 : polyvagalState === "sympathetic" ? 0.8 : 1.0;
  }

  return {
    mouthPath,
    eyeOpenness,
  };
}

/**
 * Get textual personality description (expanded for richer context)
 */
export function getPersonalityDescription(bigFive: BigFive): string {
  const O = bigFive.O ?? 0.5;
  const C = bigFive.C ?? 0.5;
  const E = bigFive.E ?? 0.5;
  const A = bigFive.A ?? 0.5;
  const N = bigFive.N ?? 0.5;

  const traits: string[] = [];

  // Openness - kreativitet og åpenhet for nye erfaringer
  if (O > 0.65) traits.push("kreativ og nysgjerrig, du setter pris på nye ideer og erfaringer");
  else if (O > 0.35) traits.push("åpen for nye perspektiver når det føles riktig");
  else traits.push("praktisk og realistisk, du foretrekker kjente løsninger");

  // Conscientiousness - struktur og målrettethet
  if (C > 0.65) traits.push("strukturert og målrettet, du liker å ha kontroll og planlegge fremover");
  else if (C > 0.35) traits.push("balanserer planlegging med fleksibilitet");
  else traits.push("fleksibel og spontan, du tilpasser deg lett til endringer");

  // Extraversion - sosial energi
  if (E > 0.65) traits.push("utadvendt og energisk, du får energi fra å være sammen med andre");
  else if (E > 0.35) traits.push("trives både med sosial tid og tid alene");
  else traits.push("innadvendt og reflektert, du trenger tid alene for å lade batteriene");

  // Agreeableness - samarbeid og empati
  if (A > 0.65) traits.push("empatisk og samarbeidsvillig, du bryr deg dypt om andre mennesker");
  else if (A > 0.35) traits.push("balanserer mellom egne behov og andres");
  else traits.push("selvstendig og direkte, du setter grenser og prioriterer dine egne behov");

  // Neuroticism - emosjonell stabilitet
  if (N > 0.65) traits.push("følsom for stress og bekymring, du reagerer sterkt på utfordringer");
  else if (N > 0.35) traits.push("opplever både rolige og stressende perioder");
  else traits.push("emosjonelt stabil og rolig, du håndterer stress godt");

  // Join traits with proper punctuation
  return traits.join(". ") + ".";
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
