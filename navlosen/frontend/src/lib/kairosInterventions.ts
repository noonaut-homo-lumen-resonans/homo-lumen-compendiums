/**
 * Kairos Intervention Patterns (D07 Synkronitetsvev)
 *
 * Based on Manus document: User Behavior Segmentation + Kairos Patterns
 * Implements 4 critical intervention moments with ethical safeguards.
 *
 * Triadic Ethics Compliance:
 * - Port 1 (Kognitiv Suverenitet): Total opt-in, no automatic push notifications
 * - Port 2 (Ontologisk Koherens): Shame-free language, suggestions not demands
 * - Port 3 (Regenerativ Healing): Capacity building, graduation design
 */

import { SomaticSignal } from "@/types";
import { type LiraAnswer } from "@/components/mestring/Stage3LiraChat";

// ============================================================================
// TYPES & INTERFACES
// ============================================================================

export interface KairosContext {
  // Current session data
  stressLevel: number;
  selectedEmotions: { word: string; quadrant: number | null }[];
  somaticSignals: SomaticSignal[];
  liraAnswers: LiraAnswer[];
  polyvagalState: "ventral" | "sympathetic" | "dorsal";

  // Historical data (from localStorage)
  previousStressLevel?: number;
  lastCheckInDate?: Date;
  consecutiveVentralSessions?: number;
  totalSessions?: number;
}

export type KairosPattern =
  | "dorsal-shutdown"      // Kairos 1: Trygg Havn
  | "sympathetic-peak"     // Kairos 2: Pustepause + Titrering
  | "deadline-nudge"       // Kairos 3: Klarspråk validation
  | "ventral-mastery";     // Kairos 4: Feire & Ekspandere

export interface KairosIntervention {
  pattern: KairosPattern;
  triggered: boolean;
  confidence: number; // 0-1
  suggestion: {
    title: string;
    message: string;
    actionLabel: string;
    actionType: "breathing" | "grounding" | "celebration" | "continue";
  };
  ethicalNote: string; // Port 1 compliance: User can always dismiss
}

// ============================================================================
// KAIROS PATTERN DETECTION
// ============================================================================

/**
 * Kairos 1: Dorsal Shutdown → "Trygg Havn" modus
 *
 * Triggers:
 * - CCI < 0.40 (proxy: stress level 8-10)
 * - 3+ high-intensity somatic signals
 * - Safety question answered "Nei, jeg føler meg utrygg"
 *
 * Intervention: Minimal UI, essential grounding, safety resources
 */
export function detectDorsalShutdown(context: KairosContext): KairosIntervention | null {
  const { stressLevel, somaticSignals, liraAnswers, polyvagalState } = context;

  // Trigger 1: Dorsal state (stress 8-10)
  const isDorsal = polyvagalState === "dorsal";

  // Trigger 2: 3+ high-intensity somatic signals
  const highIntensitySomatic = somaticSignals.filter(s => s.intensity >= 7).length;
  const hasManySomaticSignals = highIntensitySomatic >= 3;

  // Trigger 3: Safety question answered negatively
  const safetyAnswer = liraAnswers.find(a => a.questionId === "safety")?.answer;
  const feelsSafe = safetyAnswer !== "Nei, jeg føler meg utrygg";

  // Confidence calculation
  let confidence = 0;
  if (isDorsal) confidence += 0.4;
  if (hasManySomaticSignals) confidence += 0.3;
  if (!feelsSafe) confidence += 0.3;

  const triggered = confidence >= 0.6; // Require 60%+ confidence

  if (!triggered) return null;

  return {
    pattern: "dorsal-shutdown",
    triggered: true,
    confidence,
    suggestion: {
      title: "Trygg Havn-modus",
      message: "Vi ser at du har det veldig vanskelig akkurat nå. Vil du prøve en rask jording-øvelse (5-4-3-2-1) for å komme tilbake til kroppen?",
      actionLabel: "Ja, hjelp meg å jorde meg",
      actionType: "grounding",
    },
    ethicalNote: "Du kan alltid hoppe over dette og fortsette. Du bestemmer.",
  };
}

/**
 * Kairos 2: Sympatisk Stresspeak → Pustepause + Titrering
 *
 * Triggers:
 * - CCI 0.42-0.48 (borderline, proxy: stress 6-8 + rapid change)
 * - Rapid emotion toggle (5+ emotions selected, mix of Q3/Q4)
 * - Stress slider jump > 3 points from previous session
 *
 * Intervention: Proactive breathing pause before continuing
 */
export function detectSympatheticPeak(context: KairosContext): KairosIntervention | null {
  const { stressLevel, selectedEmotions, previousStressLevel, polyvagalState } = context;

  // Trigger 1: Borderline sympathetic/dorsal (stress 6-8)
  const isBorderline = stressLevel >= 6 && stressLevel <= 8;

  // Trigger 2: Rapid emotion toggle (5+ emotions, mix of negative quadrants Q3/Q4)
  const negativeEmotions = selectedEmotions.filter(e => e.quadrant === 3 || e.quadrant === 4);
  const hasRapidToggle = selectedEmotions.length >= 5 && negativeEmotions.length >= 3;

  // Trigger 3: Stress jump > 3 points
  const stressJump = previousStressLevel
    ? Math.abs(stressLevel - previousStressLevel) > 3
    : false;

  // Confidence calculation
  let confidence = 0;
  if (isBorderline) confidence += 0.4;
  if (hasRapidToggle) confidence += 0.3;
  if (stressJump) confidence += 0.3;

  const triggered = confidence >= 0.5; // Lower threshold for proactive support

  if (!triggered) return null;

  return {
    pattern: "sympathetic-peak",
    triggered: true,
    confidence,
    suggestion: {
      title: "Pustepause",
      message: "Du virker å være i en høy-stress tilstand akkurat nå. Vil du ta en rask pustepause (4-6-8 metoden) før du fortsetter? Det tar bare 90 sekunder.",
      actionLabel: "Ja, la oss puste sammen",
      actionType: "breathing",
    },
    ethicalNote: "Dette er frivillig. Du kan fortsette direkte hvis du vil.",
  };
}

/**
 * Kairos 3: Deadline-Nudge → Klarspråk validering
 *
 * Triggers:
 * - User returns after 7+ days
 * - Incomplete stage transition (e.g., started Stage 2, never reached Stage 4)
 *
 * Intervention: Gentle reminder with clear language, validation of their struggle
 */
export function detectDeadlineNudge(context: KairosContext): KairosIntervention | null {
  const { lastCheckInDate, totalSessions } = context;

  if (!lastCheckInDate) return null; // First session, no nudge needed

  // Trigger 1: 7+ days since last check-in
  const daysSinceLastCheckIn = Math.floor(
    (new Date().getTime() - lastCheckInDate.getTime()) / (1000 * 60 * 60 * 24)
  );
  const hasBeenAway = daysSinceLastCheckIn >= 7;

  // Trigger 2: Has used the system before (totalSessions > 0)
  const isReturningUser = (totalSessions || 0) > 0;

  const triggered = hasBeenAway && isReturningUser;

  if (!triggered) return null;

  return {
    pattern: "deadline-nudge",
    triggered: true,
    confidence: 1.0, // High confidence for time-based trigger
    suggestion: {
      title: "Velkommen tilbake!",
      message: `Det har gått ${daysSinceLastCheckIn} dager siden sist. Det er helt greit å ta pauser. Hvordan har det vært for deg?`,
      actionLabel: "Fortsett der jeg slapp",
      actionType: "continue",
    },
    ethicalNote: "Ingen press. Bruk systemet når det passer deg.",
  };
}

/**
 * Kairos 4: Ventral Mestring → Feire & Ekspandere
 *
 * Triggers:
 * - CCI > 0.70 (proxy: stress 1-3, ventral state)
 * - 3+ consecutive ventral check-ins
 * - Mastery log growth (if implemented)
 *
 * Intervention: Celebration + Graduation messaging (Port 3: Use system less)
 */
export function detectVentralMastery(context: KairosContext): KairosIntervention | null {
  const { polyvagalState, consecutiveVentralSessions, stressLevel } = context;

  // Trigger 1: Ventral state (stress 1-3)
  const isVentral = polyvagalState === "ventral";

  // Trigger 2: 3+ consecutive ventral sessions
  const hasConsistency = (consecutiveVentralSessions || 0) >= 3;

  // Trigger 3: Very low stress (1-2)
  const isVeryCalm = stressLevel <= 2;

  // Confidence calculation
  let confidence = 0;
  if (isVentral) confidence += 0.4;
  if (hasConsistency) confidence += 0.4;
  if (isVeryCalm) confidence += 0.2;

  const triggered = confidence >= 0.8; // High threshold for celebration

  if (!triggered) return null;

  return {
    pattern: "ventral-mastery",
    triggered: true,
    confidence,
    suggestion: {
      title: "Du mestrer dette! 🌱",
      message: "Vi har lagt merke til at du har vært i en rolig tilstand over flere økter. Det er fantastisk! Kanskje du trenger NAV-Losen sjeldnere nå?",
      actionLabel: "Fortell meg mer",
      actionType: "celebration",
    },
    ethicalNote: "Port 3: Vårt mål er at du trenger oss mindre over tid. Dette er suksess!",
  };
}

// ============================================================================
// MAIN DETECTION FUNCTION
// ============================================================================

/**
 * Detect all Kairos patterns for a given context
 * Returns interventions sorted by confidence (highest first)
 */
export function detectKairosPatterns(context: KairosContext): KairosIntervention[] {
  const interventions: KairosIntervention[] = [];

  const dorsal = detectDorsalShutdown(context);
  if (dorsal) interventions.push(dorsal);

  const sympathetic = detectSympatheticPeak(context);
  if (sympathetic) interventions.push(sympathetic);

  const deadline = detectDeadlineNudge(context);
  if (deadline) interventions.push(deadline);

  const ventral = detectVentralMastery(context);
  if (ventral) interventions.push(ventral);

  // Sort by confidence (highest first)
  return interventions.sort((a, b) => b.confidence - a.confidence);
}

// ============================================================================
// ETHICAL SAFEGUARDS (Zara Protocol)
// ============================================================================

/**
 * Zara Protocol Mitigations (from Manus document):
 *
 * 1. No manipulative nudging
 *    - All interventions are opt-in suggestions, never auto-triggered
 *    - User can always dismiss with no consequences
 *
 * 2. No re-traumatization
 *    - Shame-free language (NVC compliance)
 *    - "Forslag" not "Krav" (suggestions not demands)
 *    - Validation of struggle, not judgment
 *
 * 3. HRV data protection
 *    - Since we use HRV proxy (stress slider), no biometric data is collected
 *    - All data stored locally (localStorage only)
 *    - Full transparency in UI (user sees exactly what is measured)
 *
 * 4. Epistemisk ydmykhet (Epistemic Humility)
 *    - Kairos patterns are probabilistic, not deterministic
 *    - Confidence scores shown to user
 *    - System acknowledges uncertainty
 */

export const ETHICAL_GUARDRAILS = {
  totalOptIn: true,
  noAutoPush: true,
  shameFreeLanguage: true,
  localStorageOnly: true,
  userCanDismiss: true,
  transparentMeasurement: true,
  epistemicHumility: true,
  graduationDesign: true, // Port 3: Encourage less use over time
} as const;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Load historical context from localStorage
 */
export function loadHistoricalContext(): Partial<KairosContext> {
  if (typeof window === "undefined") return {};

  try {
    const lastCheckIn = localStorage.getItem("navlosen-last-check-in");
    const consecutiveVentral = localStorage.getItem("navlosen-consecutive-ventral");
    const totalSessions = localStorage.getItem("navlosen-total-sessions");
    const previousStress = localStorage.getItem("navlosen-previous-stress");

    return {
      lastCheckInDate: lastCheckIn ? new Date(lastCheckIn) : undefined,
      consecutiveVentralSessions: consecutiveVentral ? parseInt(consecutiveVentral, 10) : 0,
      totalSessions: totalSessions ? parseInt(totalSessions, 10) : 0,
      previousStressLevel: previousStress ? parseInt(previousStress, 10) : undefined,
    };
  } catch (error) {
    console.error("Error loading historical context:", error);
    return {};
  }
}

/**
 * Update historical context in localStorage
 */
export function updateHistoricalContext(
  polyvagalState: "ventral" | "sympathetic" | "dorsal",
  stressLevel: number
): void {
  if (typeof window === "undefined") return;

  try {
    // Update last check-in date
    localStorage.setItem("navlosen-last-check-in", new Date().toISOString());

    // Update consecutive ventral sessions
    const currentConsecutive = parseInt(
      localStorage.getItem("navlosen-consecutive-ventral") || "0",
      10
    );

    if (polyvagalState === "ventral") {
      localStorage.setItem("navlosen-consecutive-ventral", String(currentConsecutive + 1));
    } else {
      localStorage.setItem("navlosen-consecutive-ventral", "0");
    }

    // Update total sessions
    const currentTotal = parseInt(
      localStorage.getItem("navlosen-total-sessions") || "0",
      10
    );
    localStorage.setItem("navlosen-total-sessions", String(currentTotal + 1));

    // Store previous stress level for next session
    localStorage.setItem("navlosen-previous-stress", String(stressLevel));
  } catch (error) {
    console.error("Error updating historical context:", error);
  }
}
