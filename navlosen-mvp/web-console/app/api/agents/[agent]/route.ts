import { NextRequest, NextResponse } from 'next/server';
import { AGENTS, AgentType } from '@/lib/mcp-broker';
import { logSMKEntry } from '@/lib/supabase';

/**
 * API Route for Agent Communication
 *
 * This handles requests to individual agents through the MCP Broker
 */

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ agent: string }> }
) {
  const { agent: agentParam } = await params;
  const agentId = agentParam as AgentType;
  const agent = AGENTS[agentId];

  if (!agent) {
    return NextResponse.json(
      { error: 'Agent not found' },
      { status: 404 }
    );
  }

  // Health check endpoint
  if (request.nextUrl.pathname.endsWith('/health')) {
    return NextResponse.json({
      status: 'online',
      agent: agent.name,
      model: agent.model,
      timestamp: new Date().toISOString()
    });
  }

  // Return agent info
  return NextResponse.json({
    id: agent.id,
    name: agent.name,
    description: agent.description,
    domain: agent.domain,
    model: agent.model
  });
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ agent: string }> }
) {
  const { agent: agentParam } = await params;
  
  try {
    const agentId = agentParam as AgentType;
    const agent = AGENTS[agentId];

    if (!agent) {
      return NextResponse.json(
        { error: 'Agent not found' },
        { status: 404 }
      );
    }

    const body = await request.json();
    const { model, messages, context } = body;

    // Log the interaction
    await logSMKEntry({
      agent_id: agentId,
      entry_type: 'interaction',
      content: messages[messages.length - 1]?.content || '',
      metadata: {
        model: model || agent.model,
        context
      }
    });

    // In MVP: Return mock response
    // In production: Forward to actual AI API

    const mockResponses: Record<AgentType, string> = {
      orion: 'Jeg er Orion, meta-koordinator for Homo Lumen OS. Jeg hjelper med strategisk oversikt og systemkoordinering. Hvordan kan jeg assistere deg i dag?',
      lira: 'Jeg er Lira, din empatiske følgesvenn. Jeg er her for å støtte deg gjennom følelsesmessige utfordringer og hjelpe deg med mestring. Hva tenker du på akkurat nå?',
      thalus: 'Jeg er Thalus, etisk vokter. Jeg sikrer at alle beslutninger og handlinger er i tråd med våre etiske prinsipper og dine rettigheter. Hva trenger du veiledning om?',
      zara: 'Jeg er Zara, sikkerhetsvokter. Jeg beskytter dine data og personvern. Alle dine opplysninger er trygt lagret og behandlet i henhold til GDPR.',
      nyra: 'Jeg er Nyra, kreativ designer. Jeg skaper visuelle opplevelser som resonerer med deg. Hva slags design trenger du hjelp med?',
      manus: 'Jeg er Manus, infrastruktur hub. Jeg bygger og vedlikeholder de tekniske systemene som holder Homo Lumen OS i gang.',
      falcon: 'Jeg er Falcon, intelligence analyst. Jeg forsker og analyserer informasjon for å gi deg de beste innsiktene.',
      aurora: 'Jeg er Aurora, kunnskapsvokter. Jeg dokumenterer og organiserer all læring og kunnskap i systemet.'
    };

    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));

    return NextResponse.json({
      response: mockResponses[agentId] || 'Hei! Jeg er her for å hjelpe deg.',
      confidence: 0.95,
      metadata: {
        model: agent.model,
        tokens: 150,
        timestamp: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Agent API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
