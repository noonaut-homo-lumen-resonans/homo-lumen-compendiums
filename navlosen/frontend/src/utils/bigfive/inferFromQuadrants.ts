import { BigFive } from "@/types";

/**
 * Infer Big Five traits from quadrant patterns (passive, weak inference)
 *
 * Maps emotion quadrant frequencies to OCEAN traits using simple heuristics.
 * These are WEAK priors - we cap influence at ±0.1 per trait to avoid determinism.
 *
 * Quadrant mapping (from Lira's guidance):
 * - Q1 (Positive + High Energy) → +E, +O
 * - Q2 (Positive + Low Energy) → +A, +E (weaker), +O
 * - Q3 (Negative + Low Energy) → +N
 * - Q4 (Negative + High Energy) → +N, -A (in conflict contexts)
 *
 * High uncertainty (0.6-0.7) reflects the speculative nature of passive inference.
 *
 * @param quadrantHistory - Array of quadrant selections with timestamps
 * @param windowDays - Rolling window for analysis (default: 30 days)
 * @returns BigFive profile with source="inferred" and high uncertainty
 *
 * Triadisk Score: 0.12 (PROCEED)
 */

interface QuadrantEntry {
  quadrant: number;
  timestamp: string;
}

export function inferFromQuadrants(
  quadrantHistory: QuadrantEntry[],
  windowDays: number = 30
): BigFive {
  // Filter to rolling window
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - windowDays);

  const recentHistory = quadrantHistory.filter(
    (entry) => new Date(entry.timestamp) >= cutoff
  );

  if (recentHistory.length === 0) {
    // No data, return neutral with very high uncertainty
    return {
      O: 0.5,
      C: 0.5,
      E: 0.5,
      A: 0.5,
      N: 0.5,
      updatedAt: new Date().toISOString(),
      source: "inferred",
      uncertainty: {
        O: 0.9,
        C: 0.9,
        E: 0.9,
        A: 0.9,
        N: 0.9,
      },
    };
  }

  // Count frequencies by quadrant
  const counts = { 1: 0, 2: 0, 3: 0, 4: 0 };
  recentHistory.forEach((entry) => {
    if (entry.quadrant >= 1 && entry.quadrant <= 4) {
      counts[entry.quadrant as 1 | 2 | 3 | 4]++;
    }
  });

  const total = recentHistory.length;
  const freqs = {
    q1: counts[1] / total,
    q2: counts[2] / total,
    q3: counts[3] / total,
    q4: counts[4] / total,
  };

  // Base scores (neutral = 0.5)
  let O = 0.5;
  let C = 0.5;
  let E = 0.5;
  let A = 0.5;
  let N = 0.5;

  // Apply weak bias from quadrant patterns (max ±0.1)
  const BIAS_CAP = 0.1;

  // Openness: Q1/Q2 + broader emotional granularity
  O += Math.min((freqs.q1 + freqs.q2 * 0.5) * 0.15, BIAS_CAP);

  // Conscientiousness: Weak signal (mostly affects regulation strategy, not affect)
  // No strong inference from quadrants alone
  C += 0; // Neutral

  // Extraversion: Q1 strong, Q2 weak positive
  E += Math.min((freqs.q1 * 0.2 + freqs.q2 * 0.05), BIAS_CAP);

  // Agreeableness: Q2 positive, Q4 weak negative (conflict)
  A += Math.min((freqs.q2 * 0.15 - freqs.q4 * 0.05), BIAS_CAP);
  A = Math.max(A - BIAS_CAP, Math.min(A + BIAS_CAP, A)); // Clamp

  // Neuroticism: Q3/Q4 positive (negative valence)
  N += Math.min((freqs.q3 + freqs.q4) * 0.12, BIAS_CAP);

  // Clamp all values to [0, 1]
  O = Math.max(0, Math.min(1, O));
  C = Math.max(0, Math.min(1, C));
  E = Math.max(0, Math.min(1, E));
  A = Math.max(0, Math.min(1, A));
  N = Math.max(0, Math.min(1, N));

  // Calculate uncertainty based on sample size
  // More data = lower uncertainty, but still higher than self-report
  const baseUncertainty = 0.7;
  const uncertaintyReduction = Math.min(total / 100, 0.2); // Max reduction 0.2
  const uncertainty = Math.max(0.5, baseUncertainty - uncertaintyReduction);

  return {
    O,
    C,
    E,
    A,
    N,
    updatedAt: new Date().toISOString(),
    source: "inferred",
    uncertainty: {
      O: uncertainty,
      C: uncertainty + 0.1, // C has weakest signal, highest uncertainty
      E: uncertainty,
      A: uncertainty,
      N: uncertainty - 0.05, // N has strongest signal from quadrants
    },
  };
}

/**
 * Helper: Load quadrant history from localStorage
 */
export function loadQuadrantHistory(): QuadrantEntry[] {
  if (typeof window === "undefined") return [];

  try {
    const stored = localStorage.getItem("navlosen-quadrant-history");
    if (!stored) return [];
    return JSON.parse(stored);
  } catch (e) {
    console.error("Failed to load quadrant history:", e);
    return [];
  }
}

/**
 * Helper: Save quadrant selection to history
 */
export function saveQuadrantEntry(quadrant: number): void {
  if (typeof window === "undefined") return;

  try {
    const history = loadQuadrantHistory();
    const newEntry: QuadrantEntry = {
      quadrant,
      timestamp: new Date().toISOString(),
    };

    // Add new entry
    history.push(newEntry);

    // Keep only last 365 days (1 year rolling window)
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - 365);
    const filtered = history.filter(
      (entry) => new Date(entry.timestamp) >= cutoff
    );

    localStorage.setItem("navlosen-quadrant-history", JSON.stringify(filtered));
  } catch (e) {
    console.error("Failed to save quadrant entry:", e);
  }
}
