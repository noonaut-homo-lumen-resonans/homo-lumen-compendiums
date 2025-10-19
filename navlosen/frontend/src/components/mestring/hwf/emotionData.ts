/**
 * Emotion Word Data for HWF-inspired Mestring Flow
 *
 * 36 følelsesord per kvadrant (totalt 144 ord)
 * Hver kvadrant har sin egen farge-gradient
 *
 * Basert på: How We Feel (HWF) app + Circumplex Model
 */

export type EmotionWord = {
  id: string;
  word: string; // Norwegian word
  definition: string; // Short definition in Norwegian
  quadrant: 1 | 2 | 3 | 4;
  colorIntensity: number; // 0-1, determines shade within quadrant
  shape: "circle" | "oval-h" | "oval-v" | "blob"; // Organic shapes
};

/**
 * QUADRANT 1: Høy Energi, Ubehagelig (Rød)
 * Følelser: stress, sinne, angst, panikk, irritasjon, frustrasjon
 */
export const Q1_EMOTIONS: EmotionWord[] = [
  {
    id: "q1-stressed",
    word: "Stresset",
    definition: "En følelse av å være overveldet av krav og press",
    quadrant: 1,
    colorIntensity: 0.9,
    shape: "blob",
  },
  {
    id: "q1-angry",
    word: "Sint",
    definition: "Intens misfornøydhet eller vrede mot noe eller noen",
    quadrant: 1,
    colorIntensity: 0.95,
    shape: "circle",
  },
  {
    id: "q1-anxious",
    word: "Engstelig",
    definition: "Bekymret og nervøs om fremtidige hendelser eller utfall",
    quadrant: 1,
    colorIntensity: 0.8,
    shape: "oval-v",
  },
  // TODO: Add remaining 33 Q1 emotions
  // Placeholder for nå - vil bli utvidet med dine bilder/data
];

/**
 * QUADRANT 2: Høy Energi, Behagelig (Gul)
 * Følelser: glede, entusiasme, spenning, energi, inspirasjon
 */
export const Q2_EMOTIONS: EmotionWord[] = [
  {
    id: "q2-joyful",
    word: "Glad",
    definition: "En sterk følelse av lykke og tilfredshet",
    quadrant: 2,
    colorIntensity: 0.9,
    shape: "circle",
  },
  {
    id: "q2-excited",
    word: "Spent",
    definition: "Full av forventning og positiv energi",
    quadrant: 2,
    colorIntensity: 0.95,
    shape: "blob",
  },
  {
    id: "q2-enthusiastic",
    word: "Entusiastisk",
    definition: "Ivrig og lidenskapelig engasjert i noe",
    quadrant: 2,
    colorIntensity: 0.85,
    shape: "oval-h",
  },
  // TODO: Add remaining 33 Q2 emotions
];

/**
 * QUADRANT 3: Lav Energi, Ubehagelig (Blå)
 * Følelser: tristhet, ensomhet, utmattelse, sorg, håpløshet
 */
export const Q3_EMOTIONS: EmotionWord[] = [
  {
    id: "q3-sad",
    word: "Trist",
    definition: "En følelse av sorg, tap eller ulykkelig",
    quadrant: 3,
    colorIntensity: 0.8,
    shape: "oval-v",
  },
  {
    id: "q3-lonely",
    word: "Ensom",
    definition: "En følelse av isolasjon og mangel på tilknytning",
    quadrant: 3,
    colorIntensity: 0.75,
    shape: "circle",
  },
  {
    id: "q3-exhausted",
    word: "Utslitt",
    definition: "Fullstendig utmattet fysisk eller mentalt",
    quadrant: 3,
    colorIntensity: 0.9,
    shape: "blob",
  },
  // TODO: Add remaining 33 Q3 emotions
];

/**
 * QUADRANT 4: Lav Energi, Behagelig (Grønn)
 * Følelser: ro, avslappethet, ettertanke, fred, tilfredsstillelse
 */
export const Q4_EMOTIONS: EmotionWord[] = [
  {
    id: "q4-calm",
    word: "Rolig",
    definition: "En tilstand av indre fred og avslappethet",
    quadrant: 4,
    colorIntensity: 0.7,
    shape: "circle",
  },
  {
    id: "q4-thoughtful",
    word: "Ettertenksom",
    definition: "Being considerate or reflective about a situation (past, present, future), oneself",
    quadrant: 4,
    colorIntensity: 0.6,
    shape: "oval-h",
  },
  {
    id: "q4-peaceful",
    word: "Fredelig",
    definition: "En dyp følelse av harmoni og ro",
    quadrant: 4,
    colorIntensity: 0.65,
    shape: "blob",
  },
  // TODO: Add remaining 33 Q4 emotions
];

// Combine all emotions
export const ALL_EMOTIONS = [
  ...Q1_EMOTIONS,
  ...Q2_EMOTIONS,
  ...Q3_EMOTIONS,
  ...Q4_EMOTIONS,
];

// Get emotions by quadrant
export function getEmotionsByQuadrant(quadrant: 1 | 2 | 3 | 4): EmotionWord[] {
  return ALL_EMOTIONS.filter((e) => e.quadrant === quadrant);
}

// Get emotion by ID
export function getEmotionById(id: string): EmotionWord | undefined {
  return ALL_EMOTIONS.find((e) => e.id === id);
}
