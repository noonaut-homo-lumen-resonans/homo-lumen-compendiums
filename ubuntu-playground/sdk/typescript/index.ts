/**
 * Ubuntu Playground TypeScript SDK
 *
 * Type-safe client for Ubuntu Playground API with Triadiske Portvokter support.
 * Integrates BiofeltGate, ThalosFilter, and MutationLog validation.
 *
 * @version 1.0.0
 * @author Homo Lumen Coalition
 */

// ===========================
// CORE TYPES (Mirror Pydantic models)
// ===========================

/**
 * ResonanceLevel enum from BiofeltGate
 */
export enum ResonanceLevel {
  CRITICAL = "critical",       // HRV < 40
  LOW = "low",                // HRV 40-64
  BALANCED = "balanced",      // HRV 65-79
  OPTIMAL = "optimal",        // HRV 80-99
  TRANSCENDENT = "transcendent" // HRV 100+
}

/**
 * EthicalSeverity enum from ThalosFilter
 */
export enum EthicalSeverity {
  INFO = "info",
  WARNING = "warning",
  CONCERN = "concern",
  VIOLATION = "violation",
  CRITICAL = "critical"
}

/**
 * BiofeltContext - consciousness-aware processing context
 *
 * This context should be included in all critical operations to enable
 * BiofeltGate validation based on HRV and coherence.
 */
export interface BiofeltContext {
  /** Heart Rate Variability in milliseconds (0-200) */
  hrv_ms: number;

  /** Coherence score (0.0-1.0) */
  coherence: number;

  /** Breathing rhythm sequence (e.g., "4-6-8") */
  pust_rytme?: string;

  /** Felt-resonance theme */
  resonance_theme?: string;

  /** Energy level */
  energy_level?: string;

  /** Stress indicators */
  stress_indicators?: string[];

  /** ISO timestamp */
  timestamp?: string;
}

/**
 * ThalosContext - ethical validation context
 *
 * This context provides additional information for ThalosFilter
 * to make informed ethical decisions.
 */
export interface ThalosContext {
  /** Intent behind the action */
  intent?: string;

  /** Justification for the action */
  justification?: string;

  /** List of agents affected by this action */
  affected_agents?: string[];

  /** Is the action reversible? */
  reversible?: boolean;

  /** Agent who reviewed this action */
  reviewed_by?: string;

  /** Is this an emergency situation? */
  emergency?: boolean;

  /** ISO timestamp */
  timestamp?: string;
}

// ===========================
// REQUEST/RESPONSE TYPES
// ===========================

export interface WriteRequest {
  path: string;
  content: string;
  biofelt_context?: BiofeltContext;
  thalos_context?: ThalosContext;
}

export interface WriteResponse {
  success: boolean;
  path: string;
  size: number;
}

export interface ReadRequest {
  path: string;
}

export interface ReadResponse {
  content: string;
  path: string;
}

export interface ExecuteActionRequest {
  agent: string;
  action_type: string;
  payload: Record<string, any>;
  biofelt_context?: BiofeltContext;
  thalos_context?: ThalosContext;
}

export interface ExecuteActionResponse {
  success: boolean;
  action_id: number;
  status: string;
  message: string;
}

export interface HealthResponse {
  status: "healthy" | "degraded";
  redis: string;
  database: string;
  workspace: string;
  csn_server: string;
  timestamp: string;
}

/**
 * Error response from Triadiske Portvokter
 */
export interface PortvokterError {
  error: string;
  message: string;
  resonance_level?: string;
  hrv_status?: string;
  coherence_status?: string;
  severity?: string;
  violated_principles?: string[];
  warnings?: string[];
  recommendations?: string[];
  requires_review?: boolean;
}

// ===========================
// UTILITY FUNCTIONS
// ===========================

/**
 * Convert NAV Losen HealthConnectData to BiofeltContext
 *
 * @param healthData - Health data from NAV Losen (includes HRV)
 * @param stressLevel - Current stress level (0-10)
 * @param somaticSignals - Somatic signals (body sensations)
 * @returns BiofeltContext for Ubuntu Playground API
 */
export function healthDataToBiofeltContext(
  healthData: {
    hrv?: number;
    heartRate?: number;
    sleepQuality?: "poor" | "fair" | "good";
    sleepHours?: number;
  },
  stressLevel: number,
  somaticSignals: string[]
): BiofeltContext {
  // Map HRV (assume it's already in milliseconds)
  const hrv_ms = healthData.hrv || 50; // Default to LOW threshold

  // Calculate coherence based on stress level and sleep quality
  let coherence = 1.0 - (stressLevel / 10); // Inverse of stress

  if (healthData.sleepQuality === "poor") {
    coherence *= 0.7;
  } else if (healthData.sleepQuality === "fair") {
    coherence *= 0.85;
  }

  // Clamp coherence to 0.0-1.0
  coherence = Math.max(0.0, Math.min(1.0, coherence));

  // Map stress level to energy level
  const energy_level = stressLevel > 7 ? "high" : stressLevel > 4 ? "balanced" : "low";

  // Map somatic signals to stress indicators
  const stress_indicators = somaticSignals.filter(signal =>
    signal.includes("trykk") || signal.includes("spent") || signal.includes("uro")
  );

  return {
    hrv_ms,
    coherence,
    pust_rytme: "4-6-8",
    energy_level,
    stress_indicators,
    timestamp: new Date().toISOString()
  };
}

/**
 * Calculate ResonanceLevel from HRV
 */
export function calculateResonanceLevel(hrv_ms: number): ResonanceLevel {
  if (hrv_ms < 40) return ResonanceLevel.CRITICAL;
  if (hrv_ms < 65) return ResonanceLevel.LOW;
  if (hrv_ms < 80) return ResonanceLevel.BALANCED;
  if (hrv_ms < 100) return ResonanceLevel.OPTIMAL;
  return ResonanceLevel.TRANSCENDENT;
}

// ===========================
// UBUNTU PLAYGROUND CLIENT
// ===========================

export class UbuntuPlaygroundClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(baseUrl: string = "http://localhost:8002", apiKey: string) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  /**
   * Get API headers with authentication
   */
  private getHeaders(): HeadersInit {
    return {
      "Content-Type": "application/json",
      "X-API-Key": this.apiKey
    };
  }

  /**
   * Handle API errors from Triadiske Portvokter
   */
  private async handlePortvokterError(response: Response): Promise<never> {
    const error: PortvokterError = await response.json();

    let message = `${error.error}: ${error.message}`;

    if (error.recommendations && error.recommendations.length > 0) {
      message += `\n\nRecommendations:\n${error.recommendations.join("\n")}`;
    }

    throw new Error(message);
  }

  /**
   * Check API health
   */
  async health(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Write a file to the shared workspace
   *
   * @param request - Write request with path, content, and optional contexts
   * @throws Error if BiofeltGate or ThalosFilter blocks the operation
   */
  async writeFile(request: WriteRequest): Promise<WriteResponse> {
    const response = await fetch(`${this.baseUrl}/api/workspace/write`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(request)
    });

    if (response.status === 403) {
      await this.handlePortvokterError(response);
    }

    if (!response.ok) {
      throw new Error(`Write failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Read a file from the shared workspace
   */
  async readFile(request: ReadRequest): Promise<ReadResponse> {
    const response = await fetch(`${this.baseUrl}/api/workspace/read`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error(`Read failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Execute an action (e.g., from CSN Server)
   *
   * @param request - Action execution request with biofelt and thalos contexts
   * @throws Error if BiofeltGate or ThalosFilter blocks the action
   */
  async executeAction(request: ExecuteActionRequest): Promise<ExecuteActionResponse> {
    const response = await fetch(`${this.baseUrl}/api/execute-action`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify(request)
    });

    if (response.status === 403) {
      await this.handlePortvokterError(response);
    }

    if (!response.ok) {
      throw new Error(`Action execution failed: ${response.statusText}`);
    }

    return response.json();
  }
}

// ===========================
// EXAMPLE USAGE
// ===========================

/**
 * Example: NAV Losen writing to Ubuntu Playground with BiofeltContext
 */
export async function exampleNavLosenIntegration() {
  // Initialize client with NAV Losen's API key
  const client = new UbuntuPlaygroundClient(
    "http://localhost:8002",
    "code-dev-key" // Replace with actual agent API key
  );

  // Simulate NAV Losen health data
  const healthData = {
    hrv: 75, // Good HRV
    heartRate: 65,
    sleepQuality: "good" as const,
    sleepHours: 7.5
  };

  const stressLevel = 3; // Low stress (0-10 scale)
  const somaticSignals = ["rolig pust", "avslappet"]; // Relaxed signals

  // Convert to BiofeltContext
  const biofeltContext = healthDataToBiofeltContext(
    healthData,
    stressLevel,
    somaticSignals
  );

  console.log("BiofeltContext:", biofeltContext);
  console.log("Resonance Level:", calculateResonanceLevel(biofeltContext.hrv_ms));

  try {
    // Write a session summary to workspace
    const writeResponse = await client.writeFile({
      path: "navlosen/session_summary.json",
      content: JSON.stringify({
        timestamp: new Date().toISOString(),
        stressLevel,
        biofelt: biofeltContext,
        somaticSignals
      }, null, 2),
      biofelt_context: biofeltContext,
      thalos_context: {
        intent: "Log NAV Losen session summary",
        justification: "User completed mestring session",
        affected_agents: ["navlosen", "code"],
        reversible: true
      }
    });

    console.log("Write successful:", writeResponse);
  } catch (error) {
    console.error("BiofeltGate or ThalosFilter blocked:", error);
  }
}

export default UbuntuPlaygroundClient;
