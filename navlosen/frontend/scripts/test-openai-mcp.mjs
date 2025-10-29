import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const TOOL_NAME = process.argv[2] || "openai_playground_brainstorm";

const SAMPLE_ARGS = {
  openai_playground_brainstorm: {
    theme: "Trygg aktivering etter langvarig stress",
    emotion: "rolig inspirasjon",
  },
  openai_playground_storyboard: {
    sessionContext: "Første felles Playground-økt med veileder",
    durationMinutes: 50,
  },
  openai_playground_reflection: {
    sessionNotes:
      "Vi startet med pust, deretter sanseforankring. Deltaker beskrev lettelse.",
    biofeltSignal: "HRV steg fra 28 til 41",
  },
};

const argumentsForTool =
  TOOL_NAME in SAMPLE_ARGS
    ? SAMPLE_ARGS[TOOL_NAME]
    : { theme: "Ubuntu Playground test session" };

const transport = new StdioClientTransport({
  command: "node",
  args: ["mcp-servers/openai-playground-server.mjs"],
});

const client = new Client({
  name: "navlosen-mcp-tester",
  version: "0.1.0",
});

try {
  await client.connect(transport);

  const tools = await client.listTools();
  if (!tools.tools.some((tool) => tool.name === TOOL_NAME)) {
    throw new Error(
      `Fant ikke verktøyet ${TOOL_NAME}. Tilgjengelige verktøy: ${tools.tools
        .map((tool) => tool.name)
        .join(", ")}`
    );
  }

  const result = await client.callTool({
    name: TOOL_NAME,
    arguments: argumentsForTool,
  });

  const textContent = result.content
    ?.map((entry) => (entry.type === "text" ? entry.text : ""))
    .join("\n")
    .trim();

  console.log(`\n✅ MCP-verktøy '${TOOL_NAME}' svarte:\n`);
  console.log(textContent || JSON.stringify(result, null, 2));
} catch (error) {
  console.error("❌ Klarte ikke å kalle MCP-verktøyet:", error);
  process.exitCode = 1;
} finally {
  await client.close();
}
