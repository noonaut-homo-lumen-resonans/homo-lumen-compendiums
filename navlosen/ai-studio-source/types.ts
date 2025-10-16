
export interface User {
  id: string;
  name: string;
  email: string; // Placeholder
}

export interface Guide {
  id: string;
  title: string;
  summary: string;
  category: string;
  content: string; // Markdown content for the guide
  lastUpdated: string;
  timeEstimate?: string;
  requirements?: string;
  deadlinesInfo?: string;
}

export interface Document {
  id:string;
  name: string;
  type: string; // e.g., 'Vedtak', 'Legeerklæring'
  uploadDate: string;
  size: string; // e.g., '2.3 MB'
  // url: string; // Placeholder for actual document URL
}

export interface Reminder {
  id: string;
  title: string;
  dueDate: string;
  description: string;
  completed: boolean;
}

export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: number;
  isLoading?: boolean;
  error?: string;
  sources?: { title: string; uri: string }[];
}

export interface NavCase { // For "Hva nå?" feature mock
  id: string;
  title: string;
  status: string;
  nextStep: string;
  lastUpdated: string;
}

export enum ChatbotState {
  IDLE,
  LOADING,
  ERROR,
}

export enum NavTolkState {
  IDLE,
  LOADING,
  SUCCESS,
  ERROR,
}

export interface ExplanationResult {
  summary: string;
  deadlines: { label: string; date: string }[];
  nextSteps: { label: string }[];
}

// FIX: Added 'high-stress' to the list of allowed tags to match its usage in constants and components.
export interface MasteryStrategy {
  id: string;
  title: string;
  description: string;
  duration: string;
  tags: ('calm' | 'focus' | 'action' | 'grounding' | 'all' | 'high-stress')[];
}

export interface MasteryFeeling {
  label: string;
  valence: 'pleasant' | 'unpleasant';
  energy: 'high' | 'low';
}

export interface JobPosting {
  id: string;
  title: string;
  company: string;
  location: string;
  url: string;
}

export interface JobApplication {
  id: string;
  jobTitle: string;
  company: string;
  status: 'Søknad sendt' | 'Under vurdering' | 'Intervju' | 'Avslag';
  dateApplied: string;
}
