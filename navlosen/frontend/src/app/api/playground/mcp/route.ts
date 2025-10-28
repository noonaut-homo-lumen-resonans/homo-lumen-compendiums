import { NextResponse } from "next/server";
import path from "node:path";

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

interface CallToolBody {
  tool: string;
  arguments?: Record<string, unknown>;
}

async function withMcpClient<T>(
  handler: (client: Client) => Promise<T>
): Promise<T> {
  const serverPath = path.join(
    process.cwd(),
    "mcp-servers",
    "openai-playground-server.mjs"
  );

  const transport = new StdioClientTransport({
    command: "node",
    args: [serverPath],
  });

  const client = new Client({
    name: "navlosen-frontend",
    version: "0.1.0",
  });

  try {
    await client.connect(transport);
    return await handler(client);
  } finally {
    await client.close();
  }
}

function normalizeResult(result: any) {
  const textContent =
    result?.content
      ?.map((entry: any) => (entry?.type === "text" ? entry.text : ""))
      .join("\n")
      .trim() || null;

  return {
    raw: result,
    text: textContent,
  };
}

export async function GET() {
  if (!process.env.OPENAI_API_KEY) {
    return NextResponse.json(
      {
        error:
          "OPENAI_API_KEY mangler. Oppdater .env.local før Playground MCP kan brukes.",
      },
      { status: 500 }
    );
  }

  try {
    const tools = await withMcpClient((client) => client.listTools());
    return NextResponse.json(tools);
  } catch (error) {
    console.error("Failed to list MCP tools:", error);
    return NextResponse.json(
      { error: "Kunne ikke laste MCP-verktøy. Se server-logg for detaljer." },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  if (!process.env.OPENAI_API_KEY) {
    return NextResponse.json(
      {
        error:
          "OPENAI_API_KEY mangler. Oppdater .env.local før Playground MCP kan brukes.",
      },
      { status: 500 }
    );
  }

  let body: CallToolBody;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { error: "Ugyldig JSON-body." },
      { status: 400 }
    );
  }

  if (!body?.tool || typeof body.tool !== "string") {
    return NextResponse.json(
      { error: "Body må inneholde feltet 'tool' (string)." },
      { status: 400 }
    );
  }

  try {
    const result = await withMcpClient((client) =>
      client.callTool({
        name: body.tool,
        arguments: body.arguments ?? {},
      })
    );

    return NextResponse.json(normalizeResult(result));
  } catch (error) {
    console.error("Failed to call MCP tool:", error);
    return NextResponse.json(
      {
        error:
          error instanceof Error
            ? error.message
            : "Kunne ikke kalle MCP-verktøy.",
      },
      { status: 500 }
    );
  }
}
