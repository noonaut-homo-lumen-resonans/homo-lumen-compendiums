/**
 * Lira Service - CSN Server Integration
 *
 * Handles communication with ama-backend CSN Server for Lira (GPT-4) chatbot.
 * Endpoint: POST /agent/lira/real-biofield-analysis
 *
 * Features:
 * - Real OpenAI GPT-4 integration via CSN Server
 * - Biofield-aware responses (uses Mestring context if available)
 * - Empathetic personality (Lira's system prompt)
 * - Graceful error handling with fallback messages
 */

export interface BiofieldContext {
  stressLevel: number; // 1-10
  polyvagalState: "ventral" | "sympathetic" | "dorsal";
  emotions?: string[];
  selectedEmotions?: { word: string; quadrant: number | null }[];
  somaticSignals?: string[];
  lastMestringTimestamp?: number;
}

export interface LiraMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  imageUrl?: string; // Base64 or URL for uploaded/captured image
  imageDescription?: string; // OCR/analysis result from Lira
}

export interface LiraResponse {
  success: boolean;
  message: string;
  empathetic_insights?: string[];
  biofield_guidance?: string[];
  breathing_suggestions?: string[];
  confidence_score?: number;
  error?: string;
}

// CSN Server configuration
const CSN_SERVER_BASE_URL =
  process.env.NEXT_PUBLIC_CSN_SERVER_URL || "http://localhost:8000";

/**
 * Send message to Lira with optional biofield context and image
 */
export async function sendToLira(
  userMessage: string,
  conversationHistory: LiraMessage[],
  biofieldContext?: BiofieldContext,
  imageBase64?: string
): Promise<LiraResponse> {
  try {
    // Construct biofield data from context (or use defaults)
    const biofieldData = {
      emotional_context: {
        emotions: biofieldContext?.emotions || [],
        mood: getBiofieldMood(biofieldContext?.polyvagalState),
        energy: getBiofieldEnergy(biofieldContext?.stressLevel),
      },
      hrv_data: {
        hrv_ms: estimateHRV(biofieldContext?.stressLevel),
        coherence_score: estimateCoherence(biofieldContext?.stressLevel),
        stress_level: normalizeStressLevel(biofieldContext?.stressLevel),
        energy_level: normalizeEnergyLevel(biofieldContext?.stressLevel),
      },
      current_state: biofieldContext?.polyvagalState || "neutral",
      stress_level: normalizeStressLevel(biofieldContext?.stressLevel),
      energy_level: normalizeEnergyLevel(biofieldContext?.stressLevel),
      breath_pattern: [4, 6, 8], // Default optimal pattern
      additional_context: buildContextString(userMessage, conversationHistory, imageBase64),
    };

    const response = await fetch(
      `${CSN_SERVER_BASE_URL}/agent/lira/real-biofield-analysis`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(biofieldData),
      }
    );

    if (!response.ok) {
      throw new Error(`CSN Server error: ${response.status}`);
    }

    const data = await response.json();

    // Parse response from CSN Server format
    return {
      success: true,
      message: formatLiraResponse(data),
      empathetic_insights: data.empathetic_insights,
      biofield_guidance: data.biofield_guidance,
      breathing_suggestions: data.breathing_suggestions,
      confidence_score: data.confidence_score,
    };
  } catch (error) {
    console.error("Lira service error:", error);

    // Fallback response if CSN Server unavailable
    return {
      success: false,
      message: getFallbackResponse(userMessage, biofieldContext),
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

/**
 * Format Lira's response from CSN Server data
 */
function formatLiraResponse(data: any): string {
  const parts: string[] = [];

  // Gentle acknowledgment (primary empathetic response)
  if (data.analysis?.gentle_acknowledgment) {
    parts.push(data.analysis.gentle_acknowledgment);
  }

  // Biofield insights
  if (data.analysis?.biofield_insights) {
    parts.push(data.analysis.biofield_insights);
  }

  // Emotional understanding
  if (data.analysis?.emotional_understanding) {
    parts.push(data.analysis.emotional_understanding);
  }

  // Empowering reflection
  if (data.analysis?.empowering_reflection) {
    parts.push(data.analysis.empowering_reflection);
  }

  // If no structured response, use raw empathetic insights
  if (parts.length === 0 && data.empathetic_insights) {
    return data.empathetic_insights.join("\n\n");
  }

  return parts.join("\n\n") || "Jeg er her for deg. Hvordan kan jeg hjelpe?";
}

/**
 * Get fallback response when CSN Server unavailable
 */
function getFallbackResponse(
  userMessage: string,
  context?: BiofieldContext
): string {
  const lowerMessage = userMessage.toLowerCase();

  // Stress-related keywords
  if (
    lowerMessage.includes("stress") ||
    lowerMessage.includes("overveldet") ||
    lowerMessage.includes("angst")
  ) {
    return `Jeg ser at du kanskje opplever stress akkurat nå. ${
      context?.polyvagalState === "dorsal"
        ? "La oss ta det helt rolig."
        : "Det er helt normalt."
    } Jeg vil gjerne hjelpe, men jeg er for øyeblikket ikke tilgjengelig. Prøv gjerne Mestring-verktøyet vårt, eller kontakt NAV direkte hvis du trenger akutt hjelp.`;
  }

  // NAV-specific keywords
  if (
    lowerMessage.includes("nav") ||
    lowerMessage.includes("dagpenger") ||
    lowerMessage.includes("søknad")
  ) {
    return `Jeg kan hjelpe deg med NAV-relaterte spørsmål, men jeg er for øyeblikket ikke tilgjengelig. Vennligst besøk nav.no for offisiell informasjon, eller prøv igjen senere. Du kan også klikke "Snakk med veileder" nedenfor for å komme i kontakt med en menneskelig veileder.`;
  }

  // Generic fallback
  return `Hei, jeg er Lira. Jeg vil gjerne hjelpe deg, men jeg er for øyeblikket ikke tilgjengelig på grunn av tekniske problemer. Vennligst prøv igjen om litt, eller klikk "Snakk med veileder" nedenfor for å få hjelp fra en menneskelig veileder. For offisiell NAV-informasjon, besøk nav.no.`;
}

/**
 * Build context string for Lira (conversation summary)
 */
function buildContextString(
  currentMessage: string,
  history: LiraMessage[],
  imageBase64?: string
): string {
  let context = "";

  if (history.length === 0) {
    context = `First message: ${currentMessage}`;
  } else {
    const recentHistory = history.slice(-3); // Last 3 messages
    const conversationSummary = recentHistory
      .map((msg) => `${msg.role}: ${msg.content.substring(0, 100)}`)
      .join(" | ");
    context = `Conversation context: ${conversationSummary} | Current: ${currentMessage}`;
  }

  if (imageBase64) {
    context += ` | User uploaded an image (please analyze and help interpret NAV-related documents, forms, or letters)`;
  }

  return context;
}

/**
 * Helper: Get mood string from polyvagal state
 */
function getBiofieldMood(state?: string): string {
  switch (state) {
    case "ventral":
      return "calm";
    case "sympathetic":
      return "alert";
    case "dorsal":
      return "overwhelmed";
    default:
      return "neutral";
  }
}

/**
 * Helper: Get energy string from stress level
 */
function getBiofieldEnergy(stressLevel?: number): string {
  if (!stressLevel) return "balanced";
  if (stressLevel <= 3) return "flowing";
  if (stressLevel <= 7) return "activated";
  return "depleted";
}

/**
 * Helper: Estimate HRV from stress level (1-10 → ~45-95 ms)
 */
function estimateHRV(stressLevel?: number): number {
  if (!stressLevel) return 70; // Default neutral
  return Math.max(45, 95 - stressLevel * 5); // Higher stress = lower HRV
}

/**
 * Helper: Estimate coherence from stress level (1-10 → 0.3-0.9)
 */
function estimateCoherence(stressLevel?: number): number {
  if (!stressLevel) return 0.6; // Default neutral
  return Math.max(0.3, 0.9 - stressLevel * 0.06); // Higher stress = lower coherence
}

/**
 * Helper: Normalize stress level to 0.0-1.0
 */
function normalizeStressLevel(stressLevel?: number): number {
  if (!stressLevel) return 0.5;
  return Math.min(1.0, Math.max(0.0, stressLevel / 10));
}

/**
 * Helper: Normalize energy level to 0.0-1.0 (inverse of stress)
 */
function normalizeEnergyLevel(stressLevel?: number): number {
  if (!stressLevel) return 0.5;
  return Math.min(1.0, Math.max(0.0, 1.0 - stressLevel / 10));
}

/**
 * Load biofield context from localStorage (if recent Mestring session exists)
 */
export function loadBiofieldContext(): BiofieldContext | undefined {
  if (typeof window === "undefined") return undefined;

  try {
    const stressLevel = localStorage.getItem("navlosen-stress-level");
    const emotions = localStorage.getItem("navlosen-emotions");
    const signals = localStorage.getItem("navlosen-somatic-signals");
    const lastSession = localStorage.getItem(
      "navlosen-last-mestring-timestamp"
    );

    // Only use context if session is recent (within last 24 hours)
    const lastTimestamp = lastSession ? parseInt(lastSession, 10) : 0;
    const hoursSinceSession = (Date.now() - lastTimestamp) / (1000 * 60 * 60);
    if (hoursSinceSession > 24) return undefined;

    // Parse data
    const parsedEmotions = emotions ? JSON.parse(emotions) : [];
    const parsedSignals = signals ? JSON.parse(signals) : [];
    const stress = stressLevel ? parseInt(stressLevel, 10) : 5;

    // Determine polyvagal state
    let polyvagalState: "ventral" | "sympathetic" | "dorsal" = "sympathetic";
    if (stress <= 3) polyvagalState = "ventral";
    else if (stress >= 8) polyvagalState = "dorsal";

    return {
      stressLevel: stress,
      polyvagalState,
      emotions: parsedEmotions.map((e: any) => e.word),
      somaticSignals: parsedSignals
        .filter((s: any) => s.checked)
        .map((s: any) => s.label),
      lastMestringTimestamp: lastTimestamp,
    };
  } catch (error) {
    console.error("Failed to load biofield context:", error);
    return undefined;
  }
}
