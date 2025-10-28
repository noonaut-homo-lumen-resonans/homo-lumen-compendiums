import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { config as loadEnv } from "dotenv";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load local environment files if present so the MCP server can use the same secrets as Next.js.
const envCandidates = [
  path.resolve(__dirname, "..", ".env.local"),
  path.resolve(__dirname, "..", ".env"),
  path.resolve(__dirname, "..", "..", ".env.local"),
  path.resolve(__dirname, "..", "..", ".env"),
];

for (const candidate of envCandidates) {
  if (fs.existsSync(candidate)) {
    loadEnv({ path: candidate, override: false });
  }
}

const apiKey = process.env.OPENAI_API_KEY;

if (!apiKey) {
  console.error(
    "NAV-Losen MCP: OPENAI_API_KEY er ikke satt. Legg den til i .env.local eller miljøvariablene dine før du starter serveren."
  );
  process.exit(1);
}

const model = process.env.OPENAI_MCP_MODEL || "gpt-4.1-mini";
const baseUrl = process.env.OPENAI_API_BASE || "https://api.openai.com/v1";

async function callOpenAI({
  systemPrompt,
  userPrompt,
  temperature = 0.7,
  maxTokens = 800,
}) {
  const response = await fetch(`${baseUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      temperature,
      max_tokens: maxTokens,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
    }),
  });

  const payload = await response.json();

  if (!response.ok) {
    const errorMessage =
      payload?.error?.message || `${response.status} ${response.statusText}`;
    throw new Error(`OpenAI MCP request failed: ${errorMessage}`);
  }

  const messageContent = payload?.choices?.[0]?.message?.content;
  if (typeof messageContent === "string") {
    return messageContent.trim();
  }

  if (Array.isArray(messageContent)) {
    return messageContent
      .map((entry) => {
        if (typeof entry === "string") {
          return entry;
        }
        if (entry && typeof entry.text === "string") {
          return entry.text;
        }
        return "";
      })
      .filter(Boolean)
      .join("\n")
      .trim();
  }

  return "Ingen respons mottatt fra OpenAI.";
}

function readStringArg(value, fallback) {
  if (typeof value === "string" && value.trim().length > 0) {
    return value.trim();
  }
  return fallback;
}

const tools = {
  openai_playground_brainstorm: {
    name: "openai_playground_brainstorm",
    description:
      "Genererer tre kreative aktiviteter for Ubuntu Playground basert på et tema og ønsket stemning.",
    inputSchema: {
      type: "object",
      properties: {
        theme: {
          type: "string",
          minLength: 2,
          description: "Tema eller fokus for økten (f.eks. 'Mestring av uro').",
        },
        emotion: {
          type: "string",
          description:
            "Ønsket følelsesmessig tone for aktiviteten (f.eks. 'rolig håp').",
        },
      },
      required: ["theme"],
    },
    handler: async (args) => {
      const theme = readStringArg(args.theme, "Åpent tema");
      const emotion = readStringArg(args.emotion, "nøytral forventning");

      return await callOpenAI({
        systemPrompt:
          "Du er en kreativ fasilitator for Ubuntu Playground i NAV-Losen. " +
          "Utform aktiviteter som kombinerer lek, biofelt-bevissthet og mestring. " +
          "Hver aktivitet skal ha tittel, kort beskrivelse og et sanselig anker.",
        userPrompt: `Tema: ${theme}
Ønsket stemning: ${emotion}
Lag tre distinkte aktiviteter i punktliste-format.`,
        temperature: 0.85,
      });
    },
  },
  openai_playground_storyboard: {
    name: "openai_playground_storyboard",
    description:
      "Skisserer en kort tidslinje for en Playground-økt med milepæler og biofelt-sjekkpunkter.",
    inputSchema: {
      type: "object",
      properties: {
        sessionContext: {
          type: "string",
          minLength: 4,
          description:
            "Kort beskrivelse av økten eller situasjonen (f.eks. 'Første møte med veileder etter sykdom').",
        },
        durationMinutes: {
          type: "number",
          minimum: 5,
          maximum: 180,
          description:
            "Anslått varighet i minutter. Brukes til å dele inn tidslinjen.",
        },
      },
      required: ["sessionContext"],
    },
    handler: async (args) => {
      const context = readStringArg(args.sessionContext, "Utforskende økt");
      const duration =
        typeof args.durationMinutes === "number" && !Number.isNaN(args.durationMinutes)
          ? Math.max(5, Math.min(180, args.durationMinutes))
          : 45;

      return await callOpenAI({
        systemPrompt:
          "Du er en strategisk designer for Ubuntu Playground. " +
          "Lag en tidslinje med 4-6 steg, hver med hensikt, anbefalt sanselig støtte og HRV/biofelt-påminnelse.",
        userPrompt: `Kontekst: ${context}
Varighet (min): ${duration}
Format: nummerert liste med tidspunkter.`,
        temperature: 0.65,
      });
    },
  },
  openai_playground_reflection: {
    name: "openai_playground_reflection",
    description:
      "Destiller innsikter og foreslår neste steg basert på notater fra en Playground-økt.",
    inputSchema: {
      type: "object",
      properties: {
        sessionNotes: {
          type: "string",
          minLength: 10,
          description:
            "Rå notater eller transkripsjon fra økten som skal oppsummeres.",
        },
        biofeltSignal: {
          type: "string",
          description:
            "Valgfritt signal eller HRV-observasjon (f.eks. 'lav HRV, høy nervøsitet').",
        },
      },
      required: ["sessionNotes"],
    },
    handler: async (args) => {
      const notes = readStringArg(args.sessionNotes, "");
      const signal = readStringArg(args.biofeltSignal, "Ingen signal registrert");

      if (!notes) {
        throw new Error("sessionNotes må være en utfylt tekststreng.");
      }

      return await callOpenAI({
        systemPrompt:
          "Du er Orion sin refleksjonsstemme for Ubuntu Playground. " +
          "Oppsummer kort, trekk ut læringspunkter og foreslå et neste mikro-steg. " +
          "Hold tone varm og støttende.",
        userPrompt: `Notater fra økten:
${notes}

Biofelt-signal: ${signal}

Gi svar med overskriftene: Sammendrag, Læringspunkter, Neste steg.`,
        temperature: 0.55,
        maxTokens: 700,
      });
    },
  },
};

const server = new Server(
  {
    name: "navlosen-openai-playground",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
    instructions:
      "Denne MCP-serveren kobler Ubuntu Playground til OpenAI-modeller for ideering, " +
      "storyboarding og refleksjon. Sørg for at OPENAI_API_KEY er satt før oppstart.",
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: Object.values(tools).map((tool) => ({
      name: tool.name,
      description: tool.description,
      inputSchema: tool.inputSchema,
    })),
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;
  const tool = tools[name];

  if (!tool) {
    throw new Error(`Ukjent MCP-verktøy: ${name}`);
  }

  const resultText = await tool.handler(args);

  return {
    content: [
      {
        type: "text",
        text: resultText,
      },
    ],
  };
});

const transport = new StdioServerTransport();

try {
  await server.connect(transport);
} catch (error) {
  console.error("NAV-Losen MCP: Klarte ikke å starte serveren.", error);
  process.exit(1);
}
