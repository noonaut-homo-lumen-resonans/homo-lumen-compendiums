import { BigFive } from "@/types";

/**
 * Merge self-report and inferred Big Five profiles
 *
 * Uses Bayesian-ish weighted fusion:
 * - Self-report gets higher weight (α) when fresh and low uncertainty
 * - Inferred gets lower weight (1-α) but contributes when self-report is old/missing
 * - Freshness decay: self-report weight decreases over time (30-day half-life)
 *
 * Result has source="mixed" and combined uncertainty.
 *
 * @param selfReport - Voluntary survey data (high confidence)
 * @param inferred - Passive inference from quadrants (low confidence)
 * @returns Merged BigFive profile
 *
 * Triadisk Score: 0.11 (PROCEED)
 */

export function mergeProfiles(
  selfReport?: BigFive,
  inferred?: BigFive
): BigFive | undefined {
  // Case 1: Only self-report available
  if (selfReport && !inferred) {
    return selfReport;
  }

  // Case 2: Only inferred available
  if (!selfReport && inferred) {
    return inferred;
  }

  // Case 3: Neither available
  if (!selfReport && !inferred) {
    return undefined;
  }

  // Case 4: Both available - merge with weighting
  if (selfReport && inferred) {
    const alpha = calculateAlpha(selfReport);

    const traits = ["O", "C", "E", "A", "N"] as const;
    const merged: Partial<BigFive> = {};
    const mergedUncertainty: Partial<BigFive["uncertainty"]> = {};

    traits.forEach((trait) => {
      const selfValue = selfReport[trait] ?? 0.5;
      const inferredValue = inferred[trait] ?? 0.5;

      // Weighted average
      merged[trait] = alpha * selfValue + (1 - alpha) * inferredValue;

      // Combined uncertainty (weighted average, slightly higher)
      const selfUnc = selfReport.uncertainty?.[trait] ?? 0.5;
      const inferredUnc = inferred.uncertainty?.[trait] ?? 0.7;
      mergedUncertainty[trait] =
        Math.min(1, (alpha * selfUnc + (1 - alpha) * inferredUnc) * 1.1);
    });

    return {
      ...merged,
      updatedAt: new Date().toISOString(),
      source: "mixed",
      uncertainty: mergedUncertainty,
    } as BigFive;
  }

  return undefined;
}

/**
 * Calculate alpha (weight for self-report)
 *
 * Factors:
 * - Freshness: Exponential decay with 30-day half-life
 * - Uncertainty: Lower uncertainty → higher weight
 *
 * Returns value in [0.5, 0.95]
 * - Fresh self-report with low uncertainty: α ≈ 0.9
 * - Old self-report with high uncertainty: α ≈ 0.5 (equal weighting)
 */
function calculateAlpha(selfReport: BigFive): number {
  const HALF_LIFE_DAYS = 30;
  const MIN_ALPHA = 0.5;
  const MAX_ALPHA = 0.95;

  // Freshness factor
  const ageMs = Date.now() - new Date(selfReport.updatedAt || 0).getTime();
  const ageDays = ageMs / (1000 * 60 * 60 * 24);
  const freshnessFactor = Math.exp(-Math.log(2) * (ageDays / HALF_LIFE_DAYS));

  // Uncertainty factor (average across traits)
  const uncertainties = [
    selfReport.uncertainty?.O,
    selfReport.uncertainty?.C,
    selfReport.uncertainty?.E,
    selfReport.uncertainty?.A,
    selfReport.uncertainty?.N,
  ].filter((u) => u !== undefined) as number[];

  const avgUncertainty =
    uncertainties.length > 0
      ? uncertainties.reduce((sum, u) => sum + u, 0) / uncertainties.length
      : 0.5;

  const uncertaintyFactor = 1 - avgUncertainty; // Lower uncertainty → higher factor

  // Combined alpha (geometric mean of factors)
  const rawAlpha = Math.sqrt(freshnessFactor * uncertaintyFactor);

  // Clamp to range
  return Math.max(MIN_ALPHA, Math.min(MAX_ALPHA, rawAlpha));
}

/**
 * Helper: Load merged Big Five from localStorage
 *
 * Priority order:
 * 1. Try loading self-report
 * 2. Try loading inferred
 * 3. Merge if both exist
 */
export function loadBigFive(): BigFive | undefined {
  if (typeof window === "undefined") return undefined;

  try {
    const selfReportStr = localStorage.getItem("navlosen-bigfive-selfreport");
    const inferredStr = localStorage.getItem("navlosen-bigfive-inferred");

    const selfReport = selfReportStr ? JSON.parse(selfReportStr) : undefined;
    const inferred = inferredStr ? JSON.parse(inferredStr) : undefined;

    return mergeProfiles(selfReport, inferred);
  } catch (e) {
    console.error("Failed to load Big Five:", e);
    return undefined;
  }
}

/**
 * Helper: Save self-report Big Five to localStorage
 */
export function saveSelfReport(bigFive: BigFive): void {
  if (typeof window === "undefined") return;

  try {
    const data = { ...bigFive, source: "self_report" };
    localStorage.setItem("navlosen-bigfive-selfreport", JSON.stringify(data));
  } catch (e) {
    console.error("Failed to save self-report Big Five:", e);
  }
}

/**
 * Helper: Save inferred Big Five to localStorage
 */
export function saveInferred(bigFive: BigFive): void {
  if (typeof window === "undefined") return;

  try {
    const data = { ...bigFive, source: "inferred" };
    localStorage.setItem("navlosen-bigfive-inferred", JSON.stringify(data));
  } catch (e) {
    console.error("Failed to save inferred Big Five:", e);
  }
}

/**
 * Helper: Delete all Big Five data
 */
export function deleteBigFiveData(): void {
  if (typeof window === "undefined") return;

  try {
    localStorage.removeItem("navlosen-bigfive-selfreport");
    localStorage.removeItem("navlosen-bigfive-inferred");
    localStorage.removeItem("navlosen-bigfive-policy");
    console.log("✅ All Big Five data deleted");
  } catch (e) {
    console.error("Failed to delete Big Five data:", e);
  }
}
