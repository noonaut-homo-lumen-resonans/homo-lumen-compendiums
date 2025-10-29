/**
 * AffectBus - Tverr-modal informasjonsflyt for bio-semantisk coherence
 *
 * Filosofisk grunnlag:
 * Dette er NAV-Losens "nervesignal-buss" som samler fysiologiske, emosjonelle,
 * og kognitive signaler i én unified datastrøm.
 *
 * Alle Aurora-modulene (Kairos, Timeline, Micro-Challenges, HRV) publiserer
 * og abonnerer på denne felles signalstrømmen.
 *
 * Design-prinsipp: "Consciousness-aware data protocol"
 * - Ikke bare data-syncing, men rytme-syncing
 * - Hvert signal er et "øyeblikk" av brukerens tilstand
 * - Historikken danner et "digital episodic memory"
 */

export interface AffectSignal {
  /** Unix timestamp (milliseconds) */
  timestamp: number;

  /** Emotional valence: -1 (negative) til +1 (positive) */
  valence: number;

  /** Arousal/energy level: 0 (low) til 1 (high) */
  arousal: number;

  /** Heart Rate Variability RMSSD (milliseconds) - optional (fra mock HRV) */
  hrvRmssd?: number;

  /** Current Kairos state - intervention style */
  kairosState?: 'reflective' | 'active' | 'grounding';

  /** Last completed micro-challenge ID */
  lastChallenge?: string;

  /** Emotion word (from HWF wheel) */
  emotionWord?: string;

  /** Stress level (1-10) */
  stressLevel?: number;

  /** Polyvagal state derived from HRV */
  polyvagalState?: 'ventral' | 'sympathetic' | 'dorsal';

  /** Event tag for timeline markers */
  eventTag?: 'micro-challenge' | 'lira-chat' | 'mestring' | 'bigfive-survey';
}

type AffectSignalCallback = (signal: AffectSignal) => void;

/**
 * AffectBus - Singleton event bus for affect signals
 *
 * Usage:
 * ```typescript
 * import { affectBus } from '@/utils/affectBus';
 *
 * // Publish signal
 * affectBus.publish({
 *   timestamp: Date.now(),
 *   valence: 0.7,
 *   arousal: 0.4,
 *   emotionWord: 'Glad',
 *   kairosState: 'reflective'
 * });
 *
 * // Subscribe to new signals
 * affectBus.subscribe((signal) => {
 *   console.log('New affect signal:', signal);
 * });
 *
 * // Get latest signal
 * const latest = affectBus.getLatest();
 *
 * // Get history
 * const last24h = affectBus.getHistory(24);
 * ```
 */
class AffectBus {
  private signals: AffectSignal[] = [];
  private subscribers: AffectSignalCallback[] = [];
  private readonly STORAGE_KEY = 'navlosen-affect-signals';
  private readonly MAX_HISTORY_HOURS = 24 * 30; // 30 days

  constructor() {
    // Load existing signals from localStorage
    this.loadFromStorage();

    // Clean up old signals on init
    this.cleanup();
  }

  /**
   * Publish a new affect signal to the bus
   * - Stores in memory
   * - Persists to localStorage
   * - Notifies all subscribers
   */
  publish(signal: AffectSignal): void {
    // Add timestamp if not provided
    if (!signal.timestamp) {
      signal.timestamp = Date.now();
    }

    // Validate signal
    if (!this.validateSignal(signal)) {
      console.error('[AffectBus] Invalid signal:', signal);
      return;
    }

    // Add to memory
    this.signals.push(signal);

    // Persist to localStorage
    this.saveToStorage();

    // Notify subscribers
    this.subscribers.forEach(callback => {
      try {
        callback(signal);
      } catch (error) {
        console.error('[AffectBus] Subscriber error:', error);
      }
    });

    // Cleanup old signals if needed
    if (this.signals.length % 10 === 0) {
      // Run cleanup every 10 signals
      this.cleanup();
    }
  }

  /**
   * Get the latest affect signal
   */
  getLatest(): AffectSignal | null {
    if (this.signals.length === 0) return null;
    return this.signals[this.signals.length - 1];
  }

  /**
   * Get affect signal history for the last N hours
   */
  getHistory(hours: number): AffectSignal[] {
    const cutoffTime = Date.now() - (hours * 60 * 60 * 1000);
    return this.signals.filter(s => s.timestamp >= cutoffTime);
  }

  /**
   * Get all affect signals
   */
  getAll(): AffectSignal[] {
    return [...this.signals];
  }

  /**
   * Subscribe to new affect signals
   * Returns unsubscribe function
   */
  subscribe(callback: AffectSignalCallback): () => void {
    this.subscribers.push(callback);

    // Return unsubscribe function
    return () => {
      const index = this.subscribers.indexOf(callback);
      if (index > -1) {
        this.subscribers.splice(index, 1);
      }
    };
  }

  /**
   * Clear all signals (useful for testing/reset)
   */
  clear(): void {
    this.signals = [];
    this.saveToStorage();
  }

  // Private methods

  private validateSignal(signal: AffectSignal): boolean {
    // Valence must be between -1 and 1
    if (signal.valence !== undefined && (signal.valence < -1 || signal.valence > 1)) {
      console.warn('[AffectBus] Valence out of range:', signal.valence);
      return false;
    }

    // Arousal must be between 0 and 1
    if (signal.arousal !== undefined && (signal.arousal < 0 || signal.arousal > 1)) {
      console.warn('[AffectBus] Arousal out of range:', signal.arousal);
      return false;
    }

    // HRV RMSSD should be positive (if provided)
    if (signal.hrvRmssd !== undefined && signal.hrvRmssd < 0) {
      console.warn('[AffectBus] Invalid HRV RMSSD:', signal.hrvRmssd);
      return false;
    }

    return true;
  }

  private loadFromStorage(): void {
    if (typeof window === 'undefined') return;

    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (stored) {
        this.signals = JSON.parse(stored);
      }
    } catch (error) {
      console.error('[AffectBus] Failed to load from storage:', error);
      this.signals = [];
    }
  }

  private saveToStorage(): void {
    if (typeof window === 'undefined') return;

    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.signals));
    } catch (error) {
      console.error('[AffectBus] Failed to save to storage:', error);
    }
  }

  private cleanup(): void {
    const cutoffTime = Date.now() - (this.MAX_HISTORY_HOURS * 60 * 60 * 1000);
    const beforeCount = this.signals.length;

    this.signals = this.signals.filter(s => s.timestamp >= cutoffTime);

    const removedCount = beforeCount - this.signals.length;
    if (removedCount > 0) {
      console.log(`[AffectBus] Cleaned up ${removedCount} old signals`);
      this.saveToStorage();
    }
  }
}

// Singleton instance
export const affectBus = new AffectBus();

// Helper functions for common calculations

/**
 * Calculate valence from emotion quadrant
 * Q1/Q4 (Pleasant) = positive valence
 * Q2/Q3 (Unpleasant) = negative valence
 */
export function calculateValenceFromQuadrant(quadrant: 1 | 2 | 3 | 4): number {
  switch (quadrant) {
    case 1: return 0.7;  // Pleasant High Energy
    case 2: return -0.7; // Unpleasant High Energy
    case 3: return -0.7; // Unpleasant Low Energy
    case 4: return 0.7;  // Pleasant Low Energy
    default: return 0;
  }
}

/**
 * Calculate arousal from emotion quadrant
 * Q1/Q2 (High Energy) = high arousal
 * Q3/Q4 (Low Energy) = low arousal
 */
export function calculateArousalFromQuadrant(quadrant: 1 | 2 | 3 | 4): number {
  switch (quadrant) {
    case 1: return 0.8;  // Pleasant High Energy
    case 2: return 0.8;  // Unpleasant High Energy
    case 3: return -0.5; // Unpleasant Low Energy (negative = very low)
    case 4: return -0.5; // Pleasant Low Energy (negative = very low)
    default: return 0;
  }
}

/**
 * Map arousal to 0-1 scale (from -1 to 1 scale)
 */
export function normalizeArousal(arousal: number): number {
  // Convert from -1...1 scale to 0...1 scale
  return (arousal + 1) / 2;
}

/**
 * Get polyvagal state from HRV RMSSD
 *
 * Neurobiological grounding:
 * - RMSSD > 50ms: High parasympathetic tone (ventral vagal - safe & social)
 * - RMSSD 25-50ms: Sympathetic activation (fight/flight mobilization)
 * - RMSSD < 25ms: Dorsal vagal shutdown (freeze/collapse)
 */
export function getPolyvagalStateFromHRV(rmssd: number): 'ventral' | 'sympathetic' | 'dorsal' {
  if (rmssd > 50) return 'ventral';
  if (rmssd > 25) return 'sympathetic';
  return 'dorsal';
}
