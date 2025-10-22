/**
 * Analytics Tracking Utility
 *
 * Tracks Mobile Simulator usage in localStorage.
 * All data stays local (Triadic Ethics Port 1 - Cognitive Sovereignty).
 *
 * @version 1.0
 * @date 2025-10-22
 */

export interface SessionData {
  id: string;
  startTime: number;
  endTime?: number;
  deviceType: 'iphone' | 'samsung' | 'ipad';
  pages: PageVisit[];
  toursCompleted: string[];
}

export interface PageVisit {
  path: string;
  timestamp: number;
  duration?: number;
}

export interface AnalyticsStorage {
  sessions: SessionData[];
  currentSession: SessionData | null;
}

const STORAGE_KEY = 'simulator-analytics';

/**
 * Initialize a new session
 */
export function startSession(deviceType: 'iphone' | 'samsung' | 'ipad'): string {
  const analytics = getAnalytics();

  // End any existing session
  if (analytics.currentSession) {
    endSession();
  }

  const sessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  const newSession: SessionData = {
    id: sessionId,
    startTime: Date.now(),
    deviceType,
    pages: [],
    toursCompleted: [],
  };

  analytics.currentSession = newSession;
  saveAnalytics(analytics);

  return sessionId;
}

/**
 * End the current session
 */
export function endSession(): void {
  const analytics = getAnalytics();

  if (analytics.currentSession) {
    analytics.currentSession.endTime = Date.now();
    analytics.sessions.push(analytics.currentSession);
    analytics.currentSession = null;
    saveAnalytics(analytics);
  }
}

/**
 * Track a page visit
 */
export function trackPageVisit(path: string): void {
  const analytics = getAnalytics();

  if (!analytics.currentSession) {
    return; // No active session
  }

  // End previous page visit (calculate duration)
  const currentPages = analytics.currentSession.pages;
  if (currentPages.length > 0) {
    const lastPage = currentPages[currentPages.length - 1];
    if (!lastPage.duration) {
      lastPage.duration = Date.now() - lastPage.timestamp;
    }
  }

  // Add new page visit
  analytics.currentSession.pages.push({
    path,
    timestamp: Date.now(),
  });

  saveAnalytics(analytics);
}

/**
 * Track tour completion
 */
export function trackTourCompletion(tourId: string): void {
  const analytics = getAnalytics();

  if (!analytics.currentSession) {
    return;
  }

  analytics.currentSession.toursCompleted.push(tourId);
  saveAnalytics(analytics);
}

/**
 * Track device change
 */
export function trackDeviceChange(deviceType: 'iphone' | 'samsung' | 'ipad'): void {
  const analytics = getAnalytics();

  if (!analytics.currentSession) {
    return;
  }

  analytics.currentSession.deviceType = deviceType;
  saveAnalytics(analytics);
}

/**
 * Get analytics data
 */
function getAnalytics(): AnalyticsStorage {
  if (typeof window === 'undefined') {
    return { sessions: [], currentSession: null };
  }

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (error) {
    console.error('Failed to load analytics:', error);
  }

  return { sessions: [], currentSession: null };
}

/**
 * Save analytics data
 */
function saveAnalytics(analytics: AnalyticsStorage): void {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(analytics));
  } catch (error) {
    console.error('Failed to save analytics:', error);
  }
}

/**
 * Get aggregated analytics for dashboard
 */
export function getAggregatedAnalytics(timeRangeDays: number = 7) {
  const analytics = getAnalytics();
  const now = Date.now();
  const timeRange = timeRangeDays * 24 * 60 * 60 * 1000;

  // Filter sessions within time range
  const recentSessions = analytics.sessions.filter(
    (session) => now - session.startTime < timeRange
  );

  // Calculate metrics
  const totalSessions = recentSessions.length;
  const activeToday = recentSessions.filter(
    (session) => now - session.startTime < 24 * 60 * 60 * 1000
  ).length;

  // Page views
  const pageViews: { [path: string]: number } = {};
  recentSessions.forEach((session) => {
    session.pages.forEach((page) => {
      pageViews[page.path] = (pageViews[page.path] || 0) + 1;
    });
  });

  // Device distribution
  const deviceCounts: { [device: string]: number } = {};
  recentSessions.forEach((session) => {
    deviceCounts[session.deviceType] = (deviceCounts[session.deviceType] || 0) + 1;
  });

  // Tour completions
  const tourCompletions: { [tourId: string]: number } = {};
  recentSessions.forEach((session) => {
    session.toursCompleted.forEach((tourId) => {
      tourCompletions[tourId] = (tourCompletions[tourId] || 0) + 1;
    });
  });

  // Average session duration
  const totalDuration = recentSessions.reduce((acc, session) => {
    if (session.endTime) {
      return acc + (session.endTime - session.startTime);
    }
    return acc;
  }, 0);
  const avgDuration = totalDuration / (recentSessions.length || 1);

  return {
    totalSessions,
    activeToday,
    activeLast7Days: recentSessions.length,
    avgDuration: formatDuration(avgDuration),
    pageViews,
    deviceCounts,
    tourCompletions,
  };
}

/**
 * Format duration in human-readable format
 */
function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  if (minutes > 0) {
    return `${minutes}m ${remainingSeconds}s`;
  }
  return `${seconds}s`;
}

/**
 * Clear all analytics data
 */
export function clearAnalytics(): void {
  if (typeof window === 'undefined') {
    return;
  }

  localStorage.removeItem(STORAGE_KEY);
}
