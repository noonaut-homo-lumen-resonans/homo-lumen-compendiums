/**
 * Mock HRV (Heart Rate Variability) System
 *
 * Simulates realistic HRV data for testing and demonstration purposes.
 * HRV is a key biomarker for autonomic nervous system function and stress resilience.
 *
 * Key Metrics:
 * - RMSSD (Root Mean Square of Successive Differences): Primary HRV metric, ms
 * - Heart Rate: Beats per minute
 * - Polyvagal State: Derived from RMSSD (ventral/sympathetic/dorsal)
 * - Stress Index: Composite 0-100 score
 *
 * Simulation Logic:
 * - Responds to user's emotional state (from affect signals)
 * - Circadian rhythm (higher HRV in evening, lower in morning)
 * - Realistic noise and variability
 * - Trends over time (practice effects, stress accumulation)
 *
 * Educational Purpose:
 * - Demonstrates how HRV reflects nervous system state
 * - Shows relationship between HRV and emotional well-being
 * - Teaches users about polyvagal theory in action
 *
 * Triadisk Score: 0.12 (PROCEED) - Educational tool, clearly labeled as simulation
 */

import { affectBus } from './affectBus';

// ============================================================================
// TYPES
// ============================================================================

export interface HRVReading {
  timestamp: number;
  rmssd: number;           // ms (healthy range: 20-100+)
  heartRate: number;       // bpm (resting: 50-90)
  polyvagalState: 'ventral' | 'sympathetic' | 'dorsal';
  stressIndex: number;     // 0-100 (lower is better)
  quality: 'excellent' | 'good' | 'fair' | 'poor';
  isSimulated: true;       // Always true - this is mock data
}

export interface HRVStats {
  avgRmssd: number;
  avgHeartRate: number;
  stressAverage: number;
  dominantState: 'ventral' | 'sympathetic' | 'dorsal';
  trend: 'improving' | 'stable' | 'declining';
  readingsCount: number;
}

// ============================================================================
// STORAGE
// ============================================================================

const STORAGE_KEY = 'navlosen-mock-hrv-data';
const MAX_READINGS = 500; // Keep last 500 readings (~2 months if measured hourly)

function loadReadings(): HRVReading[] {
  if (typeof window === 'undefined') return [];

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];

    return JSON.parse(stored);
  } catch (e) {
    console.error('Failed to load HRV readings', e);
    return [];
  }
}

function saveReading(reading: HRVReading): void {
  if (typeof window === 'undefined') return;

  try {
    const readings = loadReadings();
    readings.push(reading);

    // Trim to max
    const trimmed = readings.slice(-MAX_READINGS);

    localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed));
  } catch (e) {
    console.error('Failed to save HRV reading', e);
  }
}

// ============================================================================
// HRV SIMULATION
// ============================================================================

/**
 * Baseline HRV values by age (RMSSD in ms)
 * Source: Nunan et al., 2010 (approximate values)
 */
const BASELINE_RMSSD_BY_AGE: Record<string, number> = {
  '18-25': 50,
  '26-35': 45,
  '36-45': 40,
  '46-55': 35,
  '56-65': 30,
  '66+': 25,
};

/**
 * Get baseline RMSSD for user
 * For now, assume mid-range age (35) - could be personalized later
 */
function getBaselineRmssd(): number {
  return BASELINE_RMSSD_BY_AGE['26-35'];
}

/**
 * Circadian modulation: HRV is typically higher in evening, lower in morning
 */
function getCircadianModifier(): number {
  const hour = new Date().getHours();

  // Morning (6-12): 0.85x baseline
  if (hour >= 6 && hour < 12) {
    return 0.85;
  }

  // Afternoon (12-18): 1.0x baseline
  if (hour >= 12 && hour < 18) {
    return 1.0;
  }

  // Evening (18-23): 1.15x baseline
  if (hour >= 18 && hour < 23) {
    return 1.15;
  }

  // Night (23-6): 1.2x baseline (sleep)
  return 1.2;
}

/**
 * Emotional state modulation: Affect valence and arousal influence HRV
 *
 * High valence (positive emotions) → Higher HRV
 * High arousal (activated state) → Lower HRV (unless positive + high arousal = challenge)
 * Low valence + Low arousal (depression) → Lower HRV
 */
function getEmotionalModifier(): number {
  const latestAffect = affectBus.getLatest();

  if (!latestAffect) {
    return 1.0; // Neutral
  }

  const { valence, arousal } = latestAffect;

  // Ventral vagal (safe & social): High valence, moderate arousal
  if (valence > 0.3 && arousal < 0.7) {
    return 1.1; // Boost HRV
  }

  // Sympathetic (fight/flight): High arousal, any valence
  if (arousal > 0.7) {
    return 0.7; // Suppress HRV
  }

  // Dorsal vagal (shutdown): Low valence, low arousal
  if (valence < -0.3 && arousal < 0.4) {
    return 0.75; // Suppress HRV
  }

  // Neutral-ish
  return 0.95;
}

/**
 * Add realistic noise to readings (biological systems are noisy)
 */
function addNoise(value: number, noisePercent: number = 0.1): number {
  const noise = (Math.random() - 0.5) * 2 * noisePercent;
  return value * (1 + noise);
}

/**
 * Calculate polyvagal state from RMSSD
 *
 * Ventral: RMSSD > 45 (healthy, regulated)
 * Sympathetic: RMSSD 25-45 (activated)
 * Dorsal: RMSSD < 25 (shutdown, dysregulated)
 */
function getPolyvagalStateFromRmssd(rmssd: number): 'ventral' | 'sympathetic' | 'dorsal' {
  if (rmssd > 45) return 'ventral';
  if (rmssd >= 25) return 'sympathetic';
  return 'dorsal';
}

/**
 * Calculate heart rate from RMSSD (inverse relationship)
 * Higher HRV → Lower resting heart rate
 */
function calculateHeartRate(rmssd: number): number {
  // Typical resting HR: 60-80 bpm
  // Good HRV (50+ ms) → 55-65 bpm
  // Poor HRV (20 ms) → 75-85 bpm

  const baseHR = 70;
  const hrModifier = (rmssd - 45) * -0.3;

  return Math.round(addNoise(baseHR + hrModifier, 0.05));
}

/**
 * Calculate stress index (0-100, lower is better)
 */
function calculateStressIndex(rmssd: number, heartRate: number): number {
  // Combine RMSSD and HR into stress metric
  // Low RMSSD + High HR = High stress

  const rmssdScore = Math.max(0, Math.min(100, (100 - rmssd) * 1.5));
  const hrScore = Math.max(0, Math.min(100, (heartRate - 50) * 2));

  const stress = (rmssdScore + hrScore) / 2;

  return Math.round(Math.max(0, Math.min(100, stress)));
}

/**
 * Assess HRV quality category
 */
function assessQuality(rmssd: number): 'excellent' | 'good' | 'fair' | 'poor' {
  if (rmssd >= 60) return 'excellent';
  if (rmssd >= 45) return 'good';
  if (rmssd >= 30) return 'fair';
  return 'poor';
}

/**
 * Generate a realistic HRV reading
 */
export function generateHRVReading(): HRVReading {
  // Start with baseline
  let rmssd = getBaselineRmssd();

  // Apply modifiers
  rmssd *= getCircadianModifier();
  rmssd *= getEmotionalModifier();

  // Add noise
  rmssd = addNoise(rmssd, 0.15);

  // Clamp to realistic range
  rmssd = Math.max(10, Math.min(120, rmssd));
  rmssd = Math.round(rmssd * 10) / 10; // Round to 1 decimal

  // Derive other metrics
  const heartRate = calculateHeartRate(rmssd);
  const polyvagalState = getPolyvagalStateFromRmssd(rmssd);
  const stressIndex = calculateStressIndex(rmssd, heartRate);
  const quality = assessQuality(rmssd);

  const reading: HRVReading = {
    timestamp: Date.now(),
    rmssd,
    heartRate,
    polyvagalState,
    stressIndex,
    quality,
    isSimulated: true,
  };

  // Save to localStorage
  saveReading(reading);

  return reading;
}

/**
 * Get latest HRV reading (or generate if none exists)
 */
export function getLatestHRVReading(): HRVReading {
  const readings = loadReadings();

  if (readings.length === 0) {
    return generateHRVReading();
  }

  const latest = readings[readings.length - 1];
  const ageMinutes = (Date.now() - latest.timestamp) / (1000 * 60);

  // If latest reading is older than 60 minutes, generate new
  if (ageMinutes > 60) {
    return generateHRVReading();
  }

  return latest;
}

/**
 * Get readings for a time range
 */
export function getHRVReadings(hours: number = 24): HRVReading[] {
  const readings = loadReadings();
  const cutoff = Date.now() - (hours * 60 * 60 * 1000);

  return readings.filter(r => r.timestamp > cutoff);
}

/**
 * Calculate statistics for recent readings
 */
export function getHRVStats(hours: number = 24): HRVStats {
  const readings = getHRVReadings(hours);

  if (readings.length === 0) {
    // Return defaults
    return {
      avgRmssd: 0,
      avgHeartRate: 0,
      stressAverage: 0,
      dominantState: 'sympathetic',
      trend: 'stable',
      readingsCount: 0,
    };
  }

  const avgRmssd = readings.reduce((sum, r) => sum + r.rmssd, 0) / readings.length;
  const avgHeartRate = readings.reduce((sum, r) => sum + r.heartRate, 0) / readings.length;
  const stressAverage = readings.reduce((sum, r) => sum + r.stressIndex, 0) / readings.length;

  // Find dominant state
  const stateCounts = readings.reduce((acc, r) => {
    acc[r.polyvagalState] = (acc[r.polyvagalState] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const dominantState = Object.keys(stateCounts).reduce((a, b) =>
    stateCounts[a] > stateCounts[b] ? a : b
  ) as 'ventral' | 'sympathetic' | 'dorsal';

  // Calculate trend (compare first half vs second half)
  let trend: 'improving' | 'stable' | 'declining' = 'stable';

  if (readings.length >= 10) {
    const midpoint = Math.floor(readings.length / 2);
    const firstHalf = readings.slice(0, midpoint);
    const secondHalf = readings.slice(midpoint);

    const firstHalfAvg = firstHalf.reduce((sum, r) => sum + r.rmssd, 0) / firstHalf.length;
    const secondHalfAvg = secondHalf.reduce((sum, r) => sum + r.rmssd, 0) / secondHalf.length;

    const change = ((secondHalfAvg - firstHalfAvg) / firstHalfAvg) * 100;

    if (change > 5) trend = 'improving';
    else if (change < -5) trend = 'declining';
  }

  return {
    avgRmssd: Math.round(avgRmssd * 10) / 10,
    avgHeartRate: Math.round(avgHeartRate),
    stressAverage: Math.round(stressAverage),
    dominantState,
    trend,
    readingsCount: readings.length,
  };
}

/**
 * Initialize mock HRV system (generate initial readings if none exist)
 */
export function initializeMockHRV(): void {
  const readings = loadReadings();

  // If no readings, generate a few historical ones
  if (readings.length === 0) {
    const now = Date.now();

    // Generate readings for last 7 days (every 4 hours)
    for (let i = 168; i >= 0; i -= 4) {
      const timestamp = now - (i * 60 * 60 * 1000);

      // Temporarily override Date for circadian rhythm
      const originalNow = Date.now;
      Date.now = () => timestamp;

      const reading = generateHRVReading();
      reading.timestamp = timestamp;

      // Restore Date.now
      Date.now = originalNow;

      if (typeof window !== 'undefined') {
        try {
          const stored = localStorage.getItem(STORAGE_KEY);
          const readings = stored ? JSON.parse(stored) : [];
          readings.push(reading);
          localStorage.setItem(STORAGE_KEY, JSON.stringify(readings));
        } catch (e) {
          console.error('Failed to save initial HRV reading', e);
        }
      }
    }
  }
}

/**
 * Clear all mock HRV data (for testing)
 */
export function clearMockHRVData(): void {
  if (typeof window === 'undefined') return;

  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (e) {
    console.error('Failed to clear HRV data', e);
  }
}
