/**
 * Example: Next.js API Route for QDA v2.0
 *
 * Copy this to: web-console/app/api/qda/respond/route.ts
 *
 * @version 2.0
 * @date 2025-10-20
 */

import { NextRequest, NextResponse } from 'next/server';
import { NeurobiologicalQDA } from '@/lib/qda';
import type { BiofeltSignature, UserContext } from '@/lib/qda';

// Optional: Add Supabase for cost tracking
// import { createClient } from '@supabase/supabase-js';
// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.SUPABASE_SERVICE_ROLE_KEY!
// );

/**
 * POST /api/qda/respond
 *
 * Request body:
 * {
 *   message: string;
 *   context?: {
 *     quadrant?: string;
 *     emotion?: string;
 *     emotionWords?: string[];
 *     pressureSignals?: string[];
 *     sessionHistory?: Array<{role: string; content: string; timestamp: number}>;
 *   };
 *   userState?: {
 *     stressLevel?: number;
 *     polyvagalState?: 'dorsal' | 'sympathetic' | 'ventral';
 *     arousal?: number;
 *     valence?: number;
 *     hrv_rmssd?: number;
 *   };
 *   sessionId?: string;
 * }
 *
 * Response:
 * {
 *   success: true;
 *   response: string;
 *   layers: Array<LayerOutput>;
 *   highest_layer_used: string;
 *   total_cost: number;
 *   total_time: number;
 *   complexity_score: number;
 * }
 */
export async function POST(req: NextRequest) {
  const startTime = Date.now();

  try {
    // Parse request body
    const body = await req.json();
    const { message, context, userState, sessionId } = body;

    // Validate required fields
    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        {
          success: false,
          error: 'Missing or invalid "message" field',
          details: 'Request must include a non-empty "message" string',
        },
        { status: 400 }
      );
    }

    // Build BiofeltSignature from userState
    const biofelt: BiofeltSignature = {
      stress_level: userState?.stressLevel ?? 5,
      polyvagal_state: userState?.polyvagalState ?? 'sympathetic',
      arousal: userState?.arousal ?? 0.5,
      valence: userState?.valence ?? 0.0,
      hrv_rmssd: userState?.hrv_rmssd,
      timestamp: Date.now(),
    };

    // Build UserContext
    const user_context: UserContext = {
      quadrant: context?.quadrant,
      emotion: context?.emotion,
      emotion_words: context?.emotionWords,
      pressure_signals: context?.pressureSignals,
      session_history: context?.sessionHistory?.map((msg: any) => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
      })),
    };

    // Initialize QDA v2.0
    const qda = new NeurobiologicalQDA('Lira');

    // Process through 6 neurobiological layers
    console.log('[QDA] Processing query:', message.substring(0, 50) + '...');
    console.log('[QDA] Stress level:', biofelt.stress_level);
    console.log('[QDA] Polyvagal state:', biofelt.polyvagal_state);

    const response = await qda.respond(message, user_context, biofelt);

    console.log('[QDA] Highest layer used:', response.highest_layer_used);
    console.log('[QDA] Total cost:', response.total_cost);
    console.log('[QDA] Processing time:', response.total_time, 'ms');

    // Optional: Log to Supabase for cost tracking
    // try {
    //   await supabase.from('qda_usage').insert({
    //     user_id: req.headers.get('x-user-id'), // From auth middleware
    //     session_id: sessionId,
    //     query_text: message,
    //     highest_layer_used: response.highest_layer_used,
    //     total_cost: response.total_cost,
    //     total_time_ms: response.total_time,
    //     complexity_score: response.complexity_score,
    //   });
    // } catch (dbError) {
    //   console.error('[QDA] Failed to log to Supabase:', dbError);
    //   // Don't fail the request if logging fails
    // }

    // Return response
    const totalTime = Date.now() - startTime;
    return NextResponse.json({
      success: true,
      response: response.final_response,
      layers: response.layers,
      highest_layer_used: response.highest_layer_used,
      total_cost: response.total_cost,
      total_time: response.total_time,
      complexity_score: response.complexity_score,
      api_time: totalTime, // Total API latency including QDA processing
    });
  } catch (error) {
    console.error('[QDA] Error processing request:', error);

    return NextResponse.json(
      {
        success: false,
        error: 'Internal server error',
        details: (error as Error).message,
        stack: process.env.NODE_ENV === 'development' ? (error as Error).stack : undefined,
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/qda/respond
 *
 * Health check endpoint
 */
export async function GET() {
  return NextResponse.json({
    status: 'ok',
    version: '2.0',
    name: 'QDA - Neocortical Ascent Model',
    layers: [
      '🛡️ Vokteren (Brainstem)',
      '❤️ Føleren (Limbic)',
      '🔍 Gjenkjenneren (Cerebellum)',
      '🧭 Utforskeren (Hippocampus)',
      '🧠 Strategen (Prefrontal Cortex)',
      '✨ Integratoren (Insula)',
    ],
  });
}
