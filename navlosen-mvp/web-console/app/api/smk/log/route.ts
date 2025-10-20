import { NextRequest, NextResponse } from 'next/server';
import { logSMKEntry } from '@/lib/supabase';

/**
 * API Route for SMK (Symbiotisk Minne Kompendium) Logging
 * 
 * This endpoint receives and stores SMK entries from agents
 */

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { agent, type, content, metadata, timestamp } = body;
    
    if (!agent || !type || !content) {
      return NextResponse.json(
        { error: 'Missing required fields: agent, type, content' },
        { status: 400 }
      );
    }
    
    // Validate entry type
    const validTypes = ['learning', 'decision', 'interaction', 'error'];
    if (!validTypes.includes(type)) {
      return NextResponse.json(
        { error: `Invalid type. Must be one of: ${validTypes.join(', ')}` },
        { status: 400 }
      );
    }
    
    // Log to Supabase
    const entry = await logSMKEntry({
      agent_id: agent,
      entry_type: type,
      content,
      metadata: metadata || {}
    });
    
    return NextResponse.json({
      success: true,
      entry_id: entry.id,
      timestamp: entry.created_at
    });
    
  } catch (error) {
    console.error('SMK logging error:', error);
    return NextResponse.json(
      { error: 'Failed to log SMK entry' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  // Return SMK logging info
  return NextResponse.json({
    endpoint: '/api/smk/log',
    method: 'POST',
    description: 'Log SMK (Symbiotisk Minne Kompendium) entries',
    required_fields: ['agent', 'type', 'content'],
    optional_fields: ['metadata', 'timestamp'],
    valid_types: ['learning', 'decision', 'interaction', 'error']
  });
}

