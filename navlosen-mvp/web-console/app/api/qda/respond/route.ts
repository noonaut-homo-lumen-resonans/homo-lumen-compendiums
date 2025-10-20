/**
 * QDA v2.0 API Endpoint
 * 
 * POST /api/qda/respond
 * Processes user messages through 6 neurobiological layers
 * 
 * @version 2.0
 * @date 2025-10-20
 */

import { NextRequest, NextResponse } from 'next/server';
import { NeurobiologicalQDA } from '@/lib/qda';
import type { BiofeltSignature, UserContext } from '@/lib/qda';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { message, context, userState } = body;

    // Validate input
    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Missing or invalid message' },
        { status: 400 }
      );
    }

    // Build BiofeltSignature
    const biofelt: BiofeltSignature = {
      stress_level: userState?.stressLevel ?? 5,
      polyvagal_state: userState?.polyvagalState ?? 'sympathetic',
      arousal: userState?.arousal ?? 0.5,
      valence: userState?.valence ?? 0.0,
      hrv_rmssd: userState?.hrv_rmssd, // Optional
      timestamp: Date.now(),
    };

    // Build UserContext
    const user_context: UserContext = {
      quadrant: context?.quadrant,
      emotion: context?.emotion,
      emotion_words: context?.emotionWords,
      pressure_signals: context?.pressureSignals,
      session_history: context?.sessionHistory,
    };

    // Initialize QDA v2.0
    const qda = new NeurobiologicalQDA('Lira');

    // Process through 6 layers
    const response = await qda.respond(message, user_context, biofelt);

    // Return response
    return NextResponse.json({
      success: true,
      response: response.final_response,
      layers: response.layers,
      highest_layer_used: response.highest_layer_used,
      total_cost: response.total_cost,
      total_time: response.total_time,
      complexity_score: response.complexity_score,
      polyvagal_state: response.polyvagal_state,
    });
  } catch (error) {
    console.error('QDA API error:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Internal server error', 
        details: (error as Error).message 
      },
      { status: 500 }
    );
  }
}

// Health check endpoint
export async function GET() {
  return NextResponse.json({
    status: 'ok',
    version: '2.0',
    engine: 'QDA Neocortical Ascent Model',
    layers: [
      'Vokteren (Brainstem)',
      'Føleren (Limbic System)',
      'Gjenkjenneren (Cerebellum)',
      'Utforskeren (Hippocampus)',
      'Strategen (Prefrontal Cortex)',
      'Integratoren (Insula)'
    ]
  });
}

