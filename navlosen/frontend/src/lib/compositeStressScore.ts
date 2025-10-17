/**
 * Composite Stress Score Calculator
 *
 * Combines multiple data sources to calculate an accurate stress score (1-10)
 * for mapping to Polyvagal states (Ventral/Sympathetic/Dorsal).
 *
 * Data Sources (Weighted):
 * 1. Stress Slider (1-10) - Weight: 40%
 * 2. Emotion Quadrant (100 words) - Weight: 30%
 * 3. Somatic Signals (6 body signals) - Weight: 20%
 * 4. Lira Adaptive Questions (2-5 questions) - Weight: 10%
 *
 * Based on: NotebookLM insights + "100 Føleser" commit fb9104f
 */

import { StressState, SomaticSignal } from "@/types";

export interface EmotionSelection {
  word: string;
  quadrant: number; // 1=Pos+High, 2=Pos+Low, 3=Neg+Low, 4=Neg+High
}

export interface LiraAnswer {
  questionId: string;
  answer: string;
}

export interface CompositeStressInput {
  // 1. Stress Slider (1-10)
  stressSlider: number;

  // 2. Selected emotions from 100-word quadrant
  selectedEmotions: EmotionSelection[];

  // 3. Somatic (body) signals
  somaticSignals: SomaticSignal[];

  // 4. Lira adaptive question answers
  liraAnswers: LiraAnswer[];
}

export interface CompositeStressResult {
  compositeScore: number; // Final score (1-10)
  polyvagalState: StressState; // Mapped state
  breakdown: {
    sliderContribution: number;
    emotionContribution: number;
    somaticContribution: number;
    liraContribution: number;
  };
  confidence: number; // 0-1 confidence in the score
}

/**
 * Calculate emotion valence score
 * Negative emotions (Q3, Q4) increase stress
 * Positive emotions (Q1, Q2) decrease stress
 */
function calculateEmotionScore(emotions: EmotionSelection[]): number {
  if (emotions.length === 0) return 5; // Neutral if no emotions selected

  const negativeCount = emotions.filter((e) => e.quadrant === 3 || e.quadrant === 4).length;
  const positiveCount = emotions.filter((e) => e.quadrant === 1 || e.quadrant === 2).length;

  // High-energy negative (Q4) counts more than low-energy negative (Q3)
  const highEnergyNeg = emotions.filter((e) => e.quadrant === 4).length;
  const lowEnergyNeg = emotions.filter((e) => e.quadrant === 3).length;

  // Weighted negative score (Q4 = 1.2x, Q3 = 1.0x)
  const weightedNegative = highEnergyNeg * 1.2 + lowEnergyNeg * 1.0;

  // Score calculation: more negative = higher stress
  // Range: 1-10 (1 = all positive, 10 = all negative)
  const ratio = weightedNegative / (emotions.length || 1);
  const emotionScore = 1 + ratio * 9; // Map ratio (0-1) to score (1-10)

  return Math.max(1, Math.min(10, emotionScore));
}

/**
 * Calculate somatic (body signal) score
 * More checked signals = higher stress
 */
function calculateSomaticScore(signals: SomaticSignal[]): number {
  const checkedCount = signals.filter((s) => s.checked).length;
  const totalSignals = signals.length || 6; // Default 6 signals

  // Linear mapping: 0 checked = 1, all checked = 10
  const somaticScore = 1 + (checkedCount / totalSignals) * 9;

  return Math.max(1, Math.min(10, somaticScore));
}

/**
 * Analyze Lira adaptive question answers
 * Extract stress indicators from text/choice answers
 */
function analyzeLiraAnswers(answers: LiraAnswer[]): number {
  if (answers.length === 0) return 5; // Neutral if no answers

  let stressIndicators = 0;
  let totalAnswers = answers.length;

  answers.forEach((answer) => {
    const answerLower = answer.answer.toLowerCase();

    // Safety question (high stress if not safe)
    if (answer.questionId === "safety") {
      if (answerLower.includes("utrygg") || answerLower.includes("nei")) {
        stressIndicators += 2; // High weight for safety concerns
      }
    }

    // Support question (high stress if needs support)
    if (answer.questionId === "support") {
      if (answerLower.includes("ja") || answerLower.includes("snakke")) {
        stressIndicators += 1.5;
      }
    }

    // Sleep question (poor sleep = stress)
    if (answer.questionId === "sleep" || answer.questionId === "sleep-quality") {
      if (answerLower.includes("dårlig") || answerLower.includes("under 4")) {
        stressIndicators += 1;
      }
    }

    // Trigger question (mentioned trigger = stress)
    if (answer.questionId === "trigger" && answer.answer.length > 10) {
      stressIndicators += 0.5; // If they wrote something substantial
    }
  });

  // Calculate score: more indicators = higher stress
  // Range: 1-10
  const liraScore = 1 + (stressIndicators / totalAnswers) * 4.5;

  return Math.max(1, Math.min(10, liraScore));
}

/**
 * Calculate confidence in the composite score
 * More data sources filled = higher confidence
 */
function calculateConfidence(input: CompositeStressInput): number {
  let filledSources = 0;

  if (input.stressSlider > 0) filledSources += 1; // Slider always filled
  if (input.selectedEmotions.length > 0) filledSources += 1;
  if (input.somaticSignals.some((s) => s.checked)) filledSources += 1;
  if (input.liraAnswers.length > 0) filledSources += 1;

  // Confidence: 0.25 per source, max 1.0
  return filledSources / 4;
}

/**
 * Map composite score to Polyvagal state
 */
function mapToPolyvagalState(score: number): StressState {
  if (score <= 3) return "ventral"; // 1-3: Calm (Ventral Vagal)
  if (score <= 7) return "sympathetic"; // 4-7: Alert (Sympathetic)
  return "dorsal"; // 8-10: Overwhelmed (Dorsal Vagal)
}

/**
 * Calculate Composite Stress Score from multiple data sources
 *
 * Weights:
 * - Stress Slider: 40% (most direct self-report)
 * - Emotions: 30% (high-granularity emotional state)
 * - Somatic: 20% (physiological indicators)
 * - Lira: 10% (contextual/cognitive factors)
 *
 * @param input - Combined stress data from all sources
 * @returns Composite stress result with score, state, breakdown, and confidence
 */
export function calculateCompositeStressScore(
  input: CompositeStressInput
): CompositeStressResult {
  // Individual scores (1-10 scale)
  const sliderScore = input.stressSlider;
  const emotionScore = calculateEmotionScore(input.selectedEmotions);
  const somaticScore = calculateSomaticScore(input.somaticSignals);
  const liraScore = analyzeLiraAnswers(input.liraAnswers);

  // Weighted contributions
  const sliderContribution = sliderScore * 0.4;
  const emotionContribution = emotionScore * 0.3;
  const somaticContribution = somaticScore * 0.2;
  const liraContribution = liraScore * 0.1;

  // Final composite score
  const compositeScore =
    sliderContribution +
    emotionContribution +
    somaticContribution +
    liraContribution;

  // Clamp to 1-10 range
  const finalScore = Math.max(1, Math.min(10, Math.round(compositeScore * 10) / 10));

  // Map to polyvagal state
  const polyvagalState = mapToPolyvagalState(finalScore);

  // Calculate confidence
  const confidence = calculateConfidence(input);

  return {
    compositeScore: finalScore,
    polyvagalState,
    breakdown: {
      sliderContribution,
      emotionContribution,
      somaticContribution,
      liraContribution,
    },
    confidence,
  };
}

/**
 * Get recommended UI adaptations based on Polyvagal state
 * (Based on LP #001 Polyvagal UI specs from Living Compendium)
 */
export function getPolyvagalUIConfig(state: StressState) {
  switch (state) {
    case "ventral":
      return {
        touchTargetSize: 44, // px
        maxChoices: "unlimited" as const,
        taskDuration: null, // No restriction
        prominentButtons: [],
        cognitiveTasks: "full" as const,
        microcopy: "collaborative" as const,
        backgroundColor: "bg-green-50",
        stateLabel: "Rolig",
      };

    case "sympathetic":
      return {
        touchTargetSize: 56, // px
        maxChoices: 3,
        taskDuration: 90, // seconds (90-second micro-tasks)
        prominentButtons: ["Pause", "Ett steg av gangen"],
        cognitiveTasks: "simplified" as const,
        microcopy: "supportive" as const,
        backgroundColor: "bg-orange-50",
        stateLabel: "Aktivert",
      };

    case "dorsal":
      return {
        touchTargetSize: 72, // px (extra-large)
        maxChoices: 2,
        taskDuration: null, // Cognitive tasks blocked
        prominentButtons: ["Ring Veileder", "Trygg Havn"],
        cognitiveTasks: "blocked" as const,
        microcopy: "shame-free" as const,
        backgroundColor: "bg-blue-50",
        stateLabel: "Overveldet",
      };
  }
}
