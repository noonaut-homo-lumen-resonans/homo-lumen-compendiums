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
