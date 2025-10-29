/**
 * L1: IMMEDIATE CONTEXT
 *
 * Real-time samtale-kontekst - hva skjer AKKURAT NÅ
 *
 * This layer manages the current user interaction state:
 * - Current page/route
 * - Active UI state (modals, forms, etc.)
 * - Real-time user input
 * - Polyvagal state tracking
 *
 * Based on Multi-Scale Architecture (LP #014)
 */

export interface ImmediateContext {
  // Current route
  currentRoute: string;

  // Polyvagal state (Dorsal/Sympatisk/Ventral)
  polyvagalState: "dorsal" | "sympathetic" | "ventral";

  // Current stress level (1-10)
  stressLevel: number;

  // Active UI state
  activeModal: string | null;
  activeForm: string | null;

  // Current user action
  currentAction: string | null;

  // Timestamp
  timestamp: Date;
}

/**
 * Get current immediate context from browser state
 */
export function getCurrentContext(): ImmediateContext {
  if (typeof window === "undefined") {
    return getDefaultContext();
  }

  // Get stress level from localStorage (set by Mestring page)
  const stressLevel = parseInt(
    localStorage.getItem("navlosen-stress-level") || "5"
  );

  // Determine polyvagal state from stress level
  const polyvagalState =
    stressLevel <= 3 ? "ventral" : stressLevel <= 7 ? "sympathetic" : "dorsal";

  return {
    currentRoute: window.location.pathname,
    polyvagalState,
    stressLevel,
    activeModal: null, // TODO: Track via context/state
    activeForm: null, // TODO: Track via context/state
    currentAction: null, // TODO: Track via analytics
    timestamp: new Date(),
  };
}

/**
 * Default context (for SSR)
 */
function getDefaultContext(): ImmediateContext {
  return {
    currentRoute: "/",
    polyvagalState: "ventral",
    stressLevel: 5,
    activeModal: null,
    activeForm: null,
    currentAction: null,
    timestamp: new Date(),
  };
}

/**
 * Log immediate context (for debugging)
 */
export function logContext(context: ImmediateContext): void {
  if (process.env.NODE_ENV === "development") {
    console.log("[L1 Immediate Context]", {
      route: context.currentRoute,
      state: context.polyvagalState,
      stress: context.stressLevel,
      timestamp: context.timestamp.toISOString(),
    });
  }
}
