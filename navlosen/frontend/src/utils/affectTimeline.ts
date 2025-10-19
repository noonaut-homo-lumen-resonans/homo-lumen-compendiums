/**
 * Affect Timeline - Data Processing Utilities
 *
 * "Digitalt Hippocampus" - Episodisk emosjonelt minne
 *
 * Filosofisk grunnlag:
 * Dette er NAV-Losens første forsøk på digital episodic memory.
 * Ved å kartlegge brukerens emosjonelle historie i Circumplex-rommet
 * får vi et visuelt arbeidsminne for hvordan følelse og energi flyter.
 *
 * Design-prinsipp: "Affective Archaeology"
 * - Ikke bare logging, men mønstergjenkjenning
 * - Identifiserer "affektive signaturer" (gjentakende tilstander)
 * - Trigger Kairos-interventions når mønstre detekteres
 */

import { calculateValenceFromQuadrant, calculateArousalFromQuadrant, normalizeArousal } from './affectBus';

export interface TimelinePoint {
  timestamp: number;
  valence: number;       // -1 to +1
  arousal: number;       // 0 to 1 (normalized)
  emotionWord: string;
  quadrant: 1 | 2 | 3 | 4;
  hrvRmssd?: number;     // Optional (from mock HRV)
  eventTag?: 'micro-challenge' | 'lira-chat' | 'mestring' | 'bigfive-survey';
  stressLevel?: number;  // 1-10
}

export interface AffectivePattern {
  type: 'low-energy-sustained' | 'high-stress-sustained' | 'positive-peak' | 'negative-valley';
  startTime: number;
  endTime: number;
  description: string;
  severity: 'low' | 'medium' | 'high';
}

/**
 * Process emotion history from localStorage into timeline points
 *
 * Merges:
 * - navlosen-emotions (emotion selections)
 * - navlosen-affect-signals (AffectBus data)
 * - navlosen-mock-hrv-data (HRV data if available)
 */
export function processEmotionHistory(): TimelinePoint[] {
  if (typeof window === 'undefined') return [];

  const points: TimelinePoint[] = [];

  try {
    // Load emotions from localStorage
    const emotionsRaw = localStorage.getItem('navlosen-emotions');
    if (!emotionsRaw) return [];

    const emotions = JSON.parse(emotionsRaw) as Array<{
      word: string;
      quadrant: number;
      timestamp?: number;
    }>;

    // Load affect signals (if available)
    const affectSignalsRaw = localStorage.getItem('navlosen-affect-signals');
    const affectSignals = affectSignalsRaw ? JSON.parse(affectSignalsRaw) : [];

    // Load mock HRV data (if available)
    const hrvDataRaw = localStorage.getItem('navlosen-mock-hrv-data');
    const hrvData = hrvDataRaw ? JSON.parse(hrvDataRaw) : [];

    // Process each emotion into a timeline point
    emotions.forEach((emotion, index) => {
      const timestamp = emotion.timestamp || Date.now() - (emotions.length - index) * 60 * 60 * 1000; // Fallback: spread over hours

      // Calculate valence and arousal from quadrant
      const quadrant = emotion.quadrant as 1 | 2 | 3 | 4;
      const valence = calculateValenceFromQuadrant(quadrant);
      const arousalRaw = calculateArousalFromQuadrant(quadrant);
      const arousal = normalizeArousal(arousalRaw);

      // Find matching HRV data (closest timestamp)
      const matchingHRV = hrvData.find((hrv: any) =>
        Math.abs(hrv.timestamp - timestamp) < 5 * 60 * 1000 // Within 5 minutes
      );

      // Find matching affect signal
      const matchingAffect = affectSignals.find((signal: any) =>
        Math.abs(signal.timestamp - timestamp) < 5 * 60 * 1000
      );

      points.push({
        timestamp,
        valence,
        arousal,
        emotionWord: emotion.word,
        quadrant,
        hrvRmssd: matchingHRV?.rmssd,
        eventTag: matchingAffect?.eventTag,
        stressLevel: matchingAffect?.stressLevel,
      });
    });

    // Sort by timestamp
    points.sort((a, b) => a.timestamp - b.timestamp);

  } catch (error) {
    console.error('[AffectTimeline] Failed to process emotion history:', error);
  }

  return points;
}

/**
 * Detect affective signatures (repeating patterns)
 *
 * Patterns:
 * - low-energy-sustained: Lav arousal + lav/negativ valens 3+ dager på rad
 * - high-stress-sustained: Høy arousal + negativ valens 3+ dager på rad
 * - positive-peak: Høy valens + høy arousal (celebratory moments)
 * - negative-valley: Lav valens + lav arousal (shutdown moments)
 */
export function detectAffectiveSignatures(points: TimelinePoint[]): AffectivePattern[] {
  const patterns: AffectivePattern[] = [];

  if (points.length < 3) return patterns;

  // Pattern 1: Low energy sustained (3+ days of low arousal + low/negative valence)
  let lowEnergyStart: number | null = null;
  let lowEnergyCount = 0;

  points.forEach((point, index) => {
    const isLowEnergy = point.arousal < 0.4 && point.valence < 0.2;

    if (isLowEnergy) {
      if (lowEnergyStart === null) {
        lowEnergyStart = point.timestamp;
      }
      lowEnergyCount++;
    } else {
      // Pattern broken - check if we have 3+ consecutive low energy points
      if (lowEnergyCount >= 3 && lowEnergyStart !== null) {
        const prevPoint = points[index - 1];
        patterns.push({
          type: 'low-energy-sustained',
          startTime: lowEnergyStart,
          endTime: prevPoint.timestamp,
          description: `Lav energi og motivasjon i ${lowEnergyCount} målinger over ${Math.ceil((prevPoint.timestamp - lowEnergyStart) / (24 * 60 * 60 * 1000))} dager.`,
          severity: lowEnergyCount > 7 ? 'high' : lowEnergyCount > 5 ? 'medium' : 'low',
        });
      }
      lowEnergyStart = null;
      lowEnergyCount = 0;
    }
  });

  // Pattern 2: High stress sustained (3+ days of high arousal + negative valence)
  let highStressStart: number | null = null;
  let highStressCount = 0;

  points.forEach((point, index) => {
    const isHighStress = point.arousal > 0.7 && point.valence < 0;

    if (isHighStress) {
      if (highStressStart === null) {
        highStressStart = point.timestamp;
      }
      highStressCount++;
    } else {
      if (highStressCount >= 3 && highStressStart !== null) {
        const prevPoint = points[index - 1];
        patterns.push({
          type: 'high-stress-sustained',
          startTime: highStressStart,
          endTime: prevPoint.timestamp,
          description: `Høyt stressnivå i ${highStressCount} målinger over ${Math.ceil((prevPoint.timestamp - highStressStart) / (24 * 60 * 60 * 1000))} dager.`,
          severity: highStressCount > 7 ? 'high' : highStressCount > 5 ? 'medium' : 'low',
        });
      }
      highStressStart = null;
      highStressCount = 0;
    }
  });

  // Pattern 3: Positive peaks (high valence + high arousal)
  points.forEach((point) => {
    if (point.valence > 0.6 && point.arousal > 0.7) {
      patterns.push({
        type: 'positive-peak',
        startTime: point.timestamp,
        endTime: point.timestamp,
        description: `Høy energi og positivitet: "${point.emotionWord}"`,
        severity: 'low', // Positive = not concerning
      });
    }
  });

  // Pattern 4: Negative valleys (low valence + low arousal)
  points.forEach((point) => {
    if (point.valence < -0.5 && point.arousal < 0.3) {
      patterns.push({
        type: 'negative-valley',
        startTime: point.timestamp,
        endTime: point.timestamp,
        description: `Lav energi og negativitet: "${point.emotionWord}"`,
        severity: point.stressLevel && point.stressLevel > 7 ? 'high' : 'medium',
      });
    }
  });

  return patterns;
}

/**
 * Get timeline points for a specific time range
 */
export function getTimelinePointsForRange(
  points: TimelinePoint[],
  hours: number
): TimelinePoint[] {
  const cutoffTime = Date.now() - (hours * 60 * 60 * 1000);
  return points.filter(p => p.timestamp >= cutoffTime);
}

/**
 * Calculate average valence and arousal for a time range
 */
export function getAverageAffect(points: TimelinePoint[]): {
  avgValence: number;
  avgArousal: number;
  dominantQuadrant: 1 | 2 | 3 | 4;
} {
  if (points.length === 0) {
    return { avgValence: 0, avgArousal: 0.5, dominantQuadrant: 1 };
  }

  const sumValence = points.reduce((sum, p) => sum + p.valence, 0);
  const sumArousal = points.reduce((sum, p) => sum + p.arousal, 0);

  const avgValence = sumValence / points.length;
  const avgArousal = sumArousal / points.length;

  // Determine dominant quadrant
  let dominantQuadrant: 1 | 2 | 3 | 4;
  if (avgValence > 0 && avgArousal > 0.5) {
    dominantQuadrant = 1; // Pleasant High Energy
  } else if (avgValence < 0 && avgArousal > 0.5) {
    dominantQuadrant = 2; // Unpleasant High Energy
  } else if (avgValence < 0 && avgArousal <= 0.5) {
    dominantQuadrant = 3; // Unpleasant Low Energy
  } else {
    dominantQuadrant = 4; // Pleasant Low Energy
  }

  return { avgValence, avgArousal, dominantQuadrant };
}

/**
 * Generate auto-insights from timeline data
 *
 * User preference: Only show if user wants to see them
 */
export function generateAutoInsights(points: TimelinePoint[]): string[] {
  const insights: string[] = [];

  if (points.length < 7) {
    return ['Fortsett å registrere dine følelser for å se mønstre over tid.'];
  }

  // Insight 1: Time of day patterns (morning vs afternoon vs evening)
  const morningPoints = points.filter(p => {
    const hour = new Date(p.timestamp).getHours();
    return hour >= 6 && hour < 12;
  });

  const afternoonPoints = points.filter(p => {
    const hour = new Date(p.timestamp).getHours();
    return hour >= 12 && hour < 18;
  });

  const eveningPoints = points.filter(p => {
    const hour = new Date(p.timestamp).getHours();
    return hour >= 18 || hour < 6;
  });

  const morningAvg = getAverageAffect(morningPoints);
  const afternoonAvg = getAverageAffect(afternoonPoints);
  const eveningAvg = getAverageAffect(eveningPoints);

  // Find which time of day has highest energy
  const energyByTime = [
    { time: 'formiddagene', arousal: morningAvg.avgArousal, count: morningPoints.length },
    { time: 'ettermiddagene', arousal: afternoonAvg.avgArousal, count: afternoonPoints.length },
    { time: 'kveldene', arousal: eveningAvg.avgArousal, count: eveningPoints.length },
  ].filter(t => t.count > 0);

  if (energyByTime.length > 0) {
    const highestEnergy = energyByTime.reduce((max, t) => t.arousal > max.arousal ? t : max);
    insights.push(`Du har mest energi på ${highestEnergy.time}.`);
  }

  // Insight 2: Most common emotion
  const emotionCounts: Record<string, number> = {};
  points.forEach(p => {
    emotionCounts[p.emotionWord] = (emotionCounts[p.emotionWord] || 0) + 1;
  });

  const mostCommon = Object.entries(emotionCounts)
    .sort(([, a], [, b]) => b - a)[0];

  if (mostCommon) {
    insights.push(`Din mest registrerte følelse er "${mostCommon[0]}" (${mostCommon[1]} ganger).`);
  }

  // Insight 3: Overall trend
  const recent7Days = getTimelinePointsForRange(points, 7 * 24);
  const recentAvg = getAverageAffect(recent7Days);

  if (recentAvg.avgValence > 0.3) {
    insights.push('Du har hatt en positiv uke.');
  } else if (recentAvg.avgValence < -0.3) {
    insights.push('Du har hatt en utfordrende uke. Husk at det er lov å søke støtte.');
  } else {
    insights.push('Du har hatt en balansert uke med både oppturer og nedturer.');
  }

  return insights;
}
