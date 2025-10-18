/**
 * NAV-Losen Type Definitions
 * Based on Design System v1.0
 */

// Button variants
export type ButtonVariant = "primary" | "secondary" | "text";
export type ButtonSize = "small" | "medium" | "large";

// Status badges
export type StatusType =
  | "under-behandling"
  | "mottatt"
  | "under-vurdering"
  | "soknad-sendt"
  | "avslag";

// Navigation items
export interface NavItem {
  id: string;
  label: string;
  icon: string;
  path: string;
  isActive?: boolean;
}

// Polyvagal stress states
export type StressState = "ventral" | "sympathetic" | "dorsal";

// Emotion types (for Mestring page)
export interface Emotion {
  id: string;
  label: string;
  valence: "positive" | "negative";
  energy: "high" | "low";
}

// Somatic signals (for Mestring page)
export interface SomaticSignal {
  id: string;
  label: string;
  checked: boolean;
}

// Strategy card (for Mestring page)
export interface Strategy {
  id: string;
  title: string;
  description: string;
  duration: string;
  stressState: StressState;
}

// User profile
export interface User {
  id: string;
  name: string;
  email: string;
}

// Document
export interface Document {
  id: string;
  name: string;
  type: string;
  uploadDate: string;
  size: string;
}

// Reminder
export interface Reminder {
  id: string;
  title: string;
  dueDate: string;
  description: string;
  completed: boolean;
}

// Case (sak)
export interface Case {
  id: string;
  title: string;
  status: StatusType;
  date: string;
}

// Multi-stage flow types
export type FlowStage = "emotions" | "signals" | "chat" | "recommendations";

export interface LiraQuestion {
  id: string;
  text: string;
  type: "text" | "choice" | "scale";
  options?: string[];
  required: boolean;
}

export interface LiraAnswer {
  questionId: string;
  answer: string | number;
}

export interface HealthConnectData {
  steps?: number;
  sleepHours?: number;
  sleepQuality?: "poor" | "fair" | "good";
  heartRate?: number;
  hrv?: number;
}

export interface WeatherData {
  temperature: number;
  condition: "sunny" | "cloudy" | "rainy" | "snowy";
  recommendation?: string;
}

export interface Recommendation {
  id: string;
  type: "exercise" | "practice" | "knowledge" | "music" | "context";
  title: string;
  description: string;
  duration?: string;
  link?: string;
  priority: number; // 1-10, higher = more recommended
}

export interface MusicFrequency {
  id: string;
  frequency: number; // Hz
  name: string;
  benefit: string;
  audioUrl?: string;
}

// Big Five (OCEAN) personality traits
// Used as weak priors for recommendation re-ranking
// Source: self-report (voluntary) or inferred (passive, from quadrant patterns)
export interface BigFiveUncertainty {
  O?: number; // 0..1, how uncertain we are about Openness
  C?: number; // Conscientiousness
  E?: number; // Extraversion
  A?: number; // Agreeableness
  N?: number; // Neuroticism
}

export interface BigFive {
  O?: number; // Openness to Experience, 0..1
  C?: number; // Conscientiousness, 0..1
  E?: number; // Extraversion, 0..1
  A?: number; // Agreeableness, 0..1
  N?: number; // Neuroticism, 0..1
  updatedAt?: string; // ISO timestamp
  source?: "self_report" | "inferred" | "mixed";
  uncertainty?: BigFiveUncertainty;
}

// Privacy preferences for Big Five data
export interface BigFivePolicy {
  persist: boolean; // Store locally?
  sync: boolean; // Sync to backend?
  useForReranking: boolean; // Use in recommendation re-ranking?
}

export interface SessionData {
  emotions: { word: string; quadrant: number | null }[];
  stressLevel: number;
  somaticSignals: SomaticSignal[];
  liraAnswers: LiraAnswer[];
  healthConnect?: HealthConnectData;
  weather?: WeatherData;
  bigFive?: BigFive; // Snapshot at recommendation time
  timestamp: string;
}
