
import { GoogleGenAI, GenerateContentResponse, Content, Type } from "@google/genai";
import { GEMINI_API_MODEL_TEXT } from '../constants';
import { ExplanationResult } from "../types";

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  console.warn(
    "API_KEY for Gemini er ikke satt i process.env.API_KEY. API-kall vil feile. " +
    "Sørg for at API_KEY er tilgjengelig som en miljøvariabel."
  );
}

const ai = new GoogleGenAI({ apiKey: API_KEY || "MISSING_API_KEY" });


const explanationSchema = {
  type: Type.OBJECT,
  properties: {
    summary: {
      type: Type.STRING,
      description: 'En kort, enkel oppsummering av hva brevet betyr på B1-nivå norsk.',
    },
    deadlines: {
      type: Type.ARRAY,
      description: 'En liste over viktige datoer eller frister nevnt i brevet.',
      items: {
        type: Type.OBJECT,
        properties: {
          label: { type: Type.STRING, description: 'Hva fristen gjelder.' },
          date: { type: Type.STRING, description: 'Datoen for fristen, formatert som YYYY-MM-DD.' },
        },
        required: ['label', 'date'],
      },
    },
    nextSteps: {
      type: Type.ARRAY,
      description: 'En liste med 1-3 konkrete neste steg brukeren bør ta.',
      items: {
        type: Type.OBJECT,
        properties: {
          label: { type: Type.STRING, description: 'Beskrivelse av det neste steget.' },
        },
         required: ['label'],
      },
    },
  },
  required: ['summary', 'deadlines', 'nextSteps'],
};

/**
 * Gets a structured explanation of a text using Gemini API.
 * @param textToExplain The bureaucratic text to explain.
 * @returns A structured explanation object or null if parsing fails.
 */
export const getExplanationFromGemini = async (textToExplain: string): Promise<ExplanationResult | null> => {
  if (!API_KEY) {
    throw new Error("API-nøkkel for Gemini mangler. Kan ikke forklare tekst.");
  }
  const prompt = `
    Du er en AI-assistent kalt NAV-Tolken. Din oppgave er å oversette kompleks, byråkratisk tekst fra NAV til et strukturert og lettforståelig format for en vanlig borger.
    Du må returnere et JSON-objekt som følger det gitte skjemaet.
    - 'summary': Forklar hovedpoenget i teksten på enkelt norsk (B1-nivå).
    - 'deadlines': Trekk ut alle konkrete frister. Hvis ingen finnes, returner en tom liste.
    - 'nextSteps': List opp 1-3 tydelige, handlingsorienterte neste steg for brukeren. Hvis ingen åpenbare steg finnes, gi et generelt råd.

    Teksten som skal forklares er:
    ---
    ${textToExplain}
    ---
  `;
  try {
    const response: GenerateContentResponse = await ai.models.generateContent({
      model: GEMINI_API_MODEL_TEXT,
      contents: [{ role: "user", parts: [{ text: prompt }] }],
      config: {
        responseMimeType: "application/json",
        responseSchema: explanationSchema,
      },
    });
    
    const responseText = response.text.trim();
    return parseGeminiJsonResponse<ExplanationResult>(responseText);

  } catch (error: any) {
    console.error("Feil ved kall til Gemini API (getExplanation):", error);
    if (error.message && error.message.includes('API key not valid')) {
         throw new Error("Ugyldig API-nøkkel for Gemini. Vennligst sjekk nøkkelen din.");
    }
    throw new Error(`Kunne ikke forklare tekst: ${error.message}`);
  }
};


/**
 * Sends a message to Gemini chat and gets a response.
 * @param message The user's message.
 * @param history The chat history.
 * @param systemInstruction Optional system instruction for the chat model.
 * @returns The bot's response text and any grounding sources.
 */
export const sendMessageToGeminiChat = async (
  message: string,
  history: Content[],
  systemInstruction?: string
): Promise<{text: string, sources?: {title: string, uri: string}[]}> => {
  if (!API_KEY) {
    throw new Error("API-nøkkel for Gemini mangler. Kan ikke sende melding.");
  }
  try {
    const contents: Content[] = [...history, { role: "user", parts: [{ text: message }] }];
    
    const response: GenerateContentResponse = await ai.models.generateContent({
        model: GEMINI_API_MODEL_TEXT,
        contents: contents,
        config: {
            ...(systemInstruction && { systemInstruction: systemInstruction }),
            // Example of including Google Search, adjust as needed.
            // For general chat, it might be better to omit tools unless specific web info is required.
            // tools: [{ googleSearch: {} }], 
        }
    });

    const text = response.text.trim();
    const groundingMetadata = response.candidates?.[0]?.groundingMetadata;
    let sources: {title: string, uri: string}[] = [];

    if (groundingMetadata?.groundingChunks && groundingMetadata.groundingChunks.length > 0) {
      sources = groundingMetadata.groundingChunks
        .map(chunk => chunk.web)
        .filter(web => web && web.uri)
        .map(web => ({ title: web.title || web.uri, uri: web.uri }));
    }
    
    return {text, sources};

  } catch (error: any) {
    console.error("Feil ved kall til Gemini API (sendMessage):", error);
     if (error.message && error.message.includes('API key not valid')) {
         throw new Error("Ugyldig API-nøkkel for Gemini. Vennligst sjekk nøkkelen din.");
    }
    throw new Error(`Kunne ikke sende melding: ${error.message}`);
  }
};

// Helper to parse JSON from Gemini if needed, as per guidelines
export const parseGeminiJsonResponse = <T,>(responseText: string): T | null => {
  let jsonStr = responseText.trim();
  const fenceRegex = /^```(\w*)?\s*\n?(.*?)\n?\s*```$/s;
  const match = jsonStr.match(fenceRegex);
  if (match && match[2]) {
    jsonStr = match[2].trim();
  }
  try {
    return JSON.parse(jsonStr) as T;
  } catch (e) {
    console.error("Kunne ikke parse JSON-respons fra Gemini:", e, "Originaltekst:", responseText);
    return null;
  }
};