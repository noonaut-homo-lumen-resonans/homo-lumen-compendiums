/**
 * NAV-LOSEN MVP - Configuration
 * 
 * @version 1.0
 * @date 2025-10-20
 */

// Detect if running in development mode
const __DEV__ = process.env.NODE_ENV === 'development';

// Web Console URL configuration
export const WEB_CONSOLE_URL = __DEV__
  ? 'http://localhost:3000' // Local development
  : 'https://nav-losen-web-console.netlify.app'; // Production (to be deployed)

// API endpoints
export const API_ENDPOINTS = {
  QDA_RESPOND: `${WEB_CONSOLE_URL}/api/qda/respond`,
  AGENTS: `${WEB_CONSOLE_URL}/api/agents`,
  SMK_LOG: `${WEB_CONSOLE_URL}/api/smk/log`,
};

// Feature flags
export const FEATURES = {
  USE_QDA_API: true, // Set to false to use mock responses
  ENABLE_DEBUG_LOGS: __DEV__,
  ENABLE_COST_TRACKING: true,
};

// Timeouts (in milliseconds)
export const TIMEOUTS = {
  QDA_REQUEST: 10000, // 10 seconds
  FALLBACK_DELAY: 1500, // 1.5 seconds
};

