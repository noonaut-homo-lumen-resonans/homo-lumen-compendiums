/**
 * Kairos Window System - Temporalt nervesystem
 *
 * Filosofisk kjerne:
 * "Kairos" = øyeblikket der naturens rytme samsvarer med brukerens mottakelighet.
 * Dette er IKKE tids-styrt logikk, men STATE-MATCHING mellom semantisk og autonom rytme.
 *
 * Neurobiologisk grunnlag:
 * - Prefrontal cortex (eksekutiv funksjon) + BigFive personality = kognitiv stil
 * - Autonomt nervesystem (HRV) = fysiologisk beredskap
 * - Sammen = "Kairos Window" (optimal timing for intervensjon)
 *
 * Design-prinsipp: "Bio-semantisk homeostat"
 * - Tekst-motoren puster sammen med brukeren
 * - Aldri tvingend - kun justering av tone/kompleksitet
 * - Ethically safe: Respekterer brukerens autonomi (Port 1)
 */

import { BigFive } from '@/types';
import { getPolyvagalStateFromHRV } from './affectBus';

export interface KairosWindow {
  /** Intervention style - HOW to interact */
  interventionStyle: 'reflective' | 'active' | 'grounding';

  /** Complexity level - HOW MUCH information */
  complexity: 'high' | 'medium' | 'low';

  /** Preferred modality - WHAT TYPE of content */
  preferredModality: 'text' | 'visual' | 'somatic';

  /** Tone adjustments - HOW to speak */
  toneAdjustments: {
    verbosity: 'detailed' | 'concise' | 'minimal';
    formalitet: 'formal' | 'casual' | 'intimate';
    pacing: 'slow' | 'medium' | 'fast';
  };

  /** Readiness score (0-1) - HOW READY user is for intervention */
  readinessScore: number;
}

export interface KairosSignal {
  /** BigFive personality traits */
  openness: number;       // 0-1
  conscientiousness: number; // 0-1
  extraversion: number;   // 0-1
  agreeableness: number;  // 0-1
  neuroticism: number;    // 0-1

  /** Physiological flexibility (HRV RMSSD in milliseconds) */
  hrvRmssd: number;

  /** Current emotional state */
  currentValence: number; // -1 to +1
  currentArousal: number; // 0 to 1

  /** Current stress level (1-10) */
  stressLevel?: number;
}

/**
 * Compute Kairos Window from multi-modal signals
 *
 * This combines:
 * - Cognitive style (BigFive personality)
 * - Physiological readiness (HRV)
 * - Emotional state (valence/arousal)
 * - Stress level
 *
 * To determine the optimal "window" for intervention.
 */
export function computeKairosWindow(signal: KairosSignal): KairosWindow {
  const { openness, extraversion, neuroticism, hrvRmssd, currentValence, currentArousal, stressLevel } = signal;

  // 1. Determine physiological readiness from HRV
  const polyvagalState = getPolyvagalStateFromHRV(hrvRmssd);

  let readiness: 'reflective' | 'active' | 'grounding';
  if (polyvagalState === 'ventral' && hrvRmssd > 45) {
    readiness = 'reflective'; // High HRV + safe state = ready for deep work
  } else if (polyvagalState === 'sympathetic' || hrvRmssd < 25) {
    readiness = 'grounding'; // Low HRV = need calming
  } else {
    readiness = 'active'; // Medium HRV = ready for action
  }

  // 2. Determine complexity based on personality + readiness
  let complexity: 'high' | 'medium' | 'low';

  // High Openness + reflective readiness = can handle complexity
  if (openness > 0.65 && readiness === 'reflective') {
    complexity = 'high';
  }
  // High Neuroticism OR grounding readiness = need simplicity
  else if (neuroticism > 0.65 || readiness === 'grounding' || (stressLevel && stressLevel > 7)) {
    complexity = 'low';
  }
  // Default
  else {
    complexity = 'medium';
  }

  // 3. Determine preferred modality based on personality
  let preferredModality: 'text' | 'visual' | 'somatic';

  // High Openness = enjoys text/reading
  if (openness > 0.65) {
    preferredModality = 'text';
  }
  // High Extraversion = prefers visual/interactive
  else if (extraversion > 0.65) {
    preferredModality = 'visual';
  }
  // High Neuroticism OR grounding state = needs somatic/body-based
  else if (neuroticism > 0.65 || readiness === 'grounding') {
    preferredModality = 'somatic';
  }
  // Default
  else {
    preferredModality = 'text';
  }

  // 4. Determine tone adjustments
  const verbosity = complexity === 'high' ? 'detailed' :
                    complexity === 'low' ? 'minimal' : 'concise';

  const formalitet = extraversion > 0.6 ? 'casual' :
                     extraversion < 0.4 ? 'intimate' : 'casual';

  const pacing = readiness === 'grounding' ? 'slow' :
                 readiness === 'active' ? 'fast' : 'medium';

  // 5. Calculate readiness score (0-1)
  // Higher HRV + positive valence + low stress = higher readiness
  const hrvScore = Math.min(1, hrvRmssd / 80); // Normalize HRV to 0-1
  const valenceScore = (currentValence + 1) / 2; // Convert -1...1 to 0...1
  const stressScore = stressLevel ? (10 - stressLevel) / 10 : 0.5; // Invert stress
  const arousalScore = currentArousal; // Already 0-1

  const readinessScore = (hrvScore * 0.4 + valenceScore * 0.3 + stressScore * 0.2 + arousalScore * 0.1);

  return {
    interventionStyle: readiness,
    complexity,
    preferredModality,
    toneAdjustments: {
      verbosity,
      formalitet,
      pacing,
    },
    readinessScore,
  };
}

/**
 * Get Kairos Window from BigFive + current affect signal
 *
 * This is a convenience wrapper that loads latest affect signal
 * and combines with BigFive to compute window.
 */
export function getKairosWindowFromBigFive(
  bigFive: BigFive,
  currentAffect?: {
    valence: number;
    arousal: number;
    hrvRmssd?: number;
    stressLevel?: number;
  }
): KairosWindow {
  // Default values if no current affect
  const valence = currentAffect?.valence ?? 0;
  const arousal = currentAffect?.arousal ?? 0.5;
  const hrvRmssd = currentAffect?.hrvRmssd ?? 50; // Default to medium HRV
  const stressLevel = currentAffect?.stressLevel;

  const signal: KairosSignal = {
    openness: bigFive.O ?? 0.5,
    conscientiousness: bigFive.C ?? 0.5,
    extraversion: bigFive.E ?? 0.5,
    agreeableness: bigFive.A ?? 0.5,
    neuroticism: bigFive.N ?? 0.5,
    hrvRmssd,
    currentValence: valence,
    currentArousal: arousal,
    stressLevel,
  };

  return computeKairosWindow(signal);
}

/**
 * Apply Kairos Window to text content
 *
 * Adjusts text based on verbosity level:
 * - detailed: Full text (100%)
 * - concise: ~60% of text (remove elaborations)
 * - minimal: ~30% of text (core message only)
 *
 * Note: This is a simple implementation. In production, would use NLP.
 */
export function applyKairosToText(text: string, window: KairosWindow): string {
  const { verbosity } = window.toneAdjustments;

  // For now, simple implementation based on sentence count
  if (verbosity === 'detailed') {
    return text; // Return full text
  }

  // Split into sentences
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];

  if (verbosity === 'minimal') {
    // Return first 1-2 sentences only (30%)
    const keepCount = Math.max(1, Math.ceil(sentences.length * 0.3));
    return sentences.slice(0, keepCount).join(' ');
  }

  if (verbosity === 'concise') {
    // Return first 60% of sentences
    const keepCount = Math.max(2, Math.ceil(sentences.length * 0.6));
    return sentences.slice(0, keepCount).join(' ');
  }

  return text;
}

/**
 * Get Kairos-adjusted definition text
 *
 * Specifically for emotion definitions in HWF wheel.
 * Adjusts based on complexity level.
 */
export function getKairosAdjustedDefinition(
  fullDefinition: string,
  window: KairosWindow
): {
  definition: string;
  showExtendedInfo: boolean;
} {
  const { complexity } = window;

  if (complexity === 'low') {
    // Minimal definition - first sentence only
    const firstSentence = fullDefinition.split('.')[0] + '.';
    return {
      definition: firstSentence,
      showExtendedInfo: false,
    };
  }

  if (complexity === 'medium') {
    // Standard definition
    return {
      definition: fullDefinition,
      showExtendedInfo: false,
    };
  }

  // complexity === 'high'
  // Full definition + extended info
  return {
    definition: fullDefinition,
    showExtendedInfo: true, // Could show polyvagal context, somatic signals, etc.
  };
}

/**
 * Get welcoming message adjusted for Kairos
 *
 * Used in Dashboard and other pages to greet user appropriately.
 */
export function getKairosWelcomeMessage(
  userName: string | null,
  window: KairosWindow
): string {
  const { formalitet, pacing } = window.toneAdjustments;
  const { readinessScore } = window;

  // Base greeting
  const name = userName || 'deg';

  if (formalitet === 'formal') {
    if (readinessScore > 0.7) {
      return `Velkommen tilbake. Du virker klar for å ta fatt på dagen.`;
    } else if (readinessScore < 0.4) {
      return `Velkommen. Ta det i ditt eget tempo.`;
    } else {
      return `Velkommen tilbake.`;
    }
  }

  if (formalitet === 'intimate') {
    if (readinessScore > 0.7) {
      return `Velkommen tilbake, ${name}. Du virker i god form i dag. 💚`;
    } else if (readinessScore < 0.4) {
      return `Hei ${name}. Husk at det er lov å ta det rolig. 🌿`;
    } else {
      return `Hei ${name}. Hvordan har du det?`;
    }
  }

  // casual (default)
  if (readinessScore > 0.7) {
    return `Hei ${name}! Klar for en produktiv dag? ✨`;
  } else if (readinessScore < 0.4) {
    return `Hei ${name}. Hvordan kan jeg hjelpe deg i dag?`;
  } else {
    return `Hei ${name}! Velkommen tilbake.`;
  }
}

/**
 * Cache Kairos Window in localStorage
 * Useful for avoiding recalculation on every render
 */
export function cacheKairosWindow(window: KairosWindow): void {
  if (typeof window === 'undefined') return;

  try {
    localStorage.setItem('navlosen-kairos-window', JSON.stringify(window));
  } catch (error) {
    console.error('[Kairos] Failed to cache window:', error);
  }
}

/**
 * Load cached Kairos Window from localStorage
 */
export function loadCachedKairosWindow(): KairosWindow | null {
  if (typeof window === 'undefined') return null;

  try {
    const cached = localStorage.getItem('navlosen-kairos-window');
    if (cached) {
      return JSON.parse(cached);
    }
  } catch (error) {
    console.error('[Kairos] Failed to load cached window:', error);
  }

  return null;
}
