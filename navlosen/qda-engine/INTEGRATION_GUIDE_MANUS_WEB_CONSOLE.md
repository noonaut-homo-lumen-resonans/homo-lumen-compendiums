# QDA v2.0 Integration Guide - Manus Web Console

**Version:** 2.0
**Date:** 2025-10-20
**Target:** Manus's Next.js Web Console + React Native Mobile App
**Status:** Ready for implementation (Dag 3-7)

---

## 📋 Executive Summary

This guide shows how to integrate **QDA v2.0 (Neocortical Ascent Model)** into Manus's NAV-Losen MVP, replacing mock responses with neurobiologically coherent bottom-up processing.

**Key Benefits:**
- ✅ **24% cost reduction** vs traditional ($551/mnd vs $722/mnd)
- ✅ **Neurobiologically coherent** (mirrors actual brain processing)
- ✅ **Polyvagal-adaptive** (responds to user stress state)
- ✅ **Transparent** (users see all 6 layers)
- ✅ **Progressive enhancement** (works with mock responses as fallback)

---

## 🗂️ File Structure

```
homo-lumen-compendiums-1/
├── navlosen/
│   ├── qda-engine/
│   │   ├── docs/                                    # QDA v2.0 Documentation
│   │   │   ├── NAV_LOSEN_QUESTION_DRIVEN_ARCHITECTURE.md
│   │   │   ├── QUESTION_DESIGN_ALGORITHMS.md
│   │   │   ├── IMPLEMENTATION_GUIDE_QDA.md
│   │   │   ├── QDA_UX_DESIGN.md
│   │   │   └── MCP-ARCHITECTURE-COMPARISON.md
│   │   ├── src/
│   │   │   ├── typescript/
│   │   │   │   ├── neurobiological-qda.ts          # ✅ TypeScript implementation
│   │   │   │   └── index.ts                        # Export barrel
│   │   │   └── python/
│   │   │       └── neurobiological_qda.py          # Python version (reference)
│   │   ├── examples/
│   │   │   ├── nextjs-api-route.ts                 # Example for Web Console
│   │   │   └── react-native-integration.tsx        # Example for Mobile App
│   │   ├── INTEGRATION_GUIDE_MANUS_WEB_CONSOLE.md  # This file
│   │   └── PYTHON_TO_TYPESCRIPT_CONVERSION.md      # Conversion notes
│   └── frontend/                                    # Manus's existing frontend
│       ├── mobile-app/                              # React Native
│       └── web-console/                             # Next.js
```

---

## 🚀 Integration Steps (Dag 3-7)

### **Phase 1: Setup (Dag 3)**

#### 1.1 Install Dependencies

In Web Console:
```bash
cd web-console
npm install
```

No additional dependencies needed - QDA v2.0 uses vanilla TypeScript.

#### 1.2 Copy QDA Engine

```bash
# From homo-lumen-compendiums root
cp -r navlosen/qda-engine/src/typescript/* web-console/lib/qda/
```

Directory structure in Web Console:
```
web-console/
├── lib/
│   └── qda/
│       ├── neurobiological-qda.ts
│       └── index.ts
```

#### 1.3 Create Barrel Export

Create `web-console/lib/qda/index.ts`:
```typescript
export {
  NeurobiologicalQDA,
  Vokteren,
  Foleren,
  Gjenkjenneren,
  Utforskeren,
  Strategen,
  Integratoren,
} from './neurobiological-qda';

export type {
  BiofeltSignature,
  UserContext,
  Message,
  LayerOutput,
  QDAResponse,
} from './neurobiological-qda';
```

---

### **Phase 2: API Endpoint (Dag 4)**

#### 2.1 Create QDA API Route

Create `web-console/app/api/qda/respond/route.ts`:

```typescript
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
    });
  } catch (error) {
    console.error('QDA API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: (error as Error).message },
      { status: 500 }
    );
  }
}
```

#### 2.2 Test API Endpoint

```bash
curl -X POST http://localhost:3000/api/qda/respond \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jeg føler meg stresset på jobb",
    "context": {
      "quadrant": "høy-energi-negativt",
      "emotion": "stresset",
      "pressureSignals": ["hodepine", "muskelspenning"]
    },
    "userState": {
      "stressLevel": 7,
      "polyvagalState": "sympathetic",
      "arousal": 0.8,
      "valence": -0.4
    }
  }'
```

Expected response:
```json
{
  "success": true,
  "response": "Jeg hører at du føler deg stresset...",
  "layers": [...],
  "highest_layer_used": "Utforskeren",
  "total_cost": 0.0024,
  "total_time": 45,
  "complexity_score": 0.5
}
```

---

### **Phase 3: Mobile App Integration (Dag 5)**

#### 3.1 Update LiraChatScreen.tsx

Replace mock response logic with QDA API call:

```typescript
// mobile-app/src/screens/LiraChatScreen.tsx

import { WEB_CONSOLE_URL } from '@/config';

const generateLiraResponse = async (userMessage: string): Promise<string> => {
  try {
    // Call QDA API
    const response = await fetch(`${WEB_CONSOLE_URL}/api/qda/respond`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userMessage,
        context: {
          quadrant: route.params?.quadrant,
          emotion: route.params?.emotion,
          emotionWords: route.params?.emotionWords,
          pressureSignals: route.params?.pressureSignals,
          sessionHistory: messages.map(m => ({
            role: m.sender === 'user' ? 'user' : 'assistant',
            content: m.text,
            timestamp: Date.now(), // TODO: use actual timestamp
          })),
        },
        userState: {
          stressLevel: route.params?.stressLevel ?? 5,
          polyvagalState: calculatePolyvagalState(),
          arousal: calculateArousal(),
          valence: calculateValence(),
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();

    // Log for debugging
    console.log('[QDA] Layers used:', data.layers.map((l: any) => l.layer_name));
    console.log('[QDA] Cost:', data.total_cost);
    console.log('[QDA] Highest layer:', data.highest_layer_used);

    return data.response;
  } catch (error) {
    console.error('[QDA] Error:', error);
    // Fallback to mock response
    return generateMockResponse(userMessage);
  }
};

// Helper functions
const calculatePolyvagalState = (): 'dorsal' | 'sympathetic' | 'ventral' => {
  const stressLevel = route.params?.stressLevel ?? 5;
  if (stressLevel >= 8) return 'dorsal';
  if (stressLevel >= 5) return 'sympathetic';
  return 'ventral';
};

const calculateArousal = (): number => {
  const stressLevel = route.params?.stressLevel ?? 5;
  return stressLevel / 10.0; // Simple mapping
};

const calculateValence = (): number => {
  const quadrant = route.params?.quadrant;
  if (quadrant?.includes('positivt')) return 0.5;
  if (quadrant?.includes('negativt')) return -0.5;
  return 0.0;
};

// Keep existing mock response as fallback
const generateMockResponse = (userMessage: string): string => {
  // ... existing mock logic ...
};
```

#### 3.2 Add Config for Web Console URL

Create `mobile-app/src/config.ts`:
```typescript
export const WEB_CONSOLE_URL =
  __DEV__
    ? 'http://localhost:3000' // Local development
    : 'https://nav-losen-web-console.netlify.app'; // Production
```

---

### **Phase 4: Web Console Dashboard (Dag 6)**

#### 4.1 Create QDA Visualization Component

Create `web-console/components/qda/LayerVisualization.tsx`:

```typescript
import React from 'react';
import { LayerOutput } from '@/lib/qda';

interface Props {
  layers: LayerOutput[];
  polyvagalState: 'dorsal' | 'sympathetic' | 'ventral';
}

export const LayerVisualization: React.FC<Props> = ({ layers, polyvagalState }) => {
  const stateColors = {
    dorsal: { primary: '#4CAF50', bg: '#E8F5E9' },
    sympathetic: { primary: '#FF9800', bg: '#FFF3E0' },
    ventral: { primary: '#2196F3', bg: '#E3F2FD' },
  };

  const colors = stateColors[polyvagalState];

  return (
    <div style={{ backgroundColor: colors.bg, padding: '16px', borderRadius: '8px' }}>
      <h3 style={{ color: colors.primary }}>Nevrobiologisk Prosessering</h3>
      <p style={{ fontSize: '14px', color: '#666' }}>
        Du er i <strong>{polyvagalState}</strong> tilstand
      </p>

      <div style={{ marginTop: '16px' }}>
        {layers.map((layer, index) => (
          <LayerCard key={layer.layer_name} layer={layer} index={index + 1} />
        ))}
      </div>
    </div>
  );
};

const LayerCard: React.FC<{ layer: LayerOutput; index: number }> = ({ layer, index }) => {
  const layerColors: Record<string, string> = {
    Vokteren: '#FF6B6B',
    Føleren: '#FF8C94',
    Gjenkjenneren: '#A8DADC',
    Utforskeren: '#457B9D',
    Strategen: '#1D3557',
    Integratoren: '#F1FAEE',
  };

  const getSummary = () => {
    switch (layer.layer_name) {
      case 'Vokteren':
        return `${layer.data.complexity} query (trygt: ${layer.data.safe ? '✓' : '✗'})`;
      case 'Føleren':
        return `${layer.data.polyvagal_state} state, følelse: ${layer.data.primary_emotion}`;
      case 'Gjenkjenneren':
        return layer.data.recognized
          ? `Mønster: ${layer.data.pattern} (${(layer.data.confidence * 100).toFixed(0)}%)`
          : 'Ingen mønster gjenkjent';
      case 'Utforskeren':
        return layer.data.activated
          ? `Fant ${layer.data.resources?.length ?? 0} ressurser`
          : 'Ikke aktivert';
      case 'Strategen':
        return layer.data.activated
          ? `${layer.data.action_steps?.length ?? 0}-stegs plan`
          : 'Ikke aktivert (lav kompleksitet)';
      case 'Integratoren':
        return `${layer.data.layers_used} lag brukt`;
      default:
        return '';
    }
  };

  return (
    <div
      style={{
        borderLeft: `6px solid ${layerColors[layer.layer_name]}`,
        padding: '12px',
        marginBottom: '8px',
        backgroundColor: 'white',
        borderRadius: '4px',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{ fontSize: '24px' }}>{layer.icon}</span>
        <div>
          <div style={{ fontWeight: 'bold' }}>
            Lag {index}: {layer.layer_name}
          </div>
          <div style={{ fontSize: '14px', color: '#666' }}>{getSummary()}</div>
          <div style={{ fontSize: '12px', color: '#999' }}>
            {layer.processing_time}ms • ${layer.cost.toFixed(5)}
          </div>
        </div>
      </div>
    </div>
  );
};
```

#### 4.2 Use in Dashboard

```typescript
// web-console/app/dashboard/page.tsx
import { LayerVisualization } from '@/components/qda/LayerVisualization';

export default function Dashboard() {
  const [qdaResponse, setQdaResponse] = useState(null);

  return (
    <div>
      {qdaResponse && (
        <LayerVisualization
          layers={qdaResponse.layers}
          polyvagalState={qdaResponse.polyvagal_state}
        />
      )}
    </div>
  );
}
```

---

### **Phase 5: Testing & Deployment (Dag 7)**

#### 5.1 Unit Tests

Create `web-console/lib/qda/__tests__/neurobiological-qda.test.ts`:

```typescript
import { NeurobiologicalQDA } from '../neurobiological-qda';
import type { BiofeltSignature, UserContext } from '../neurobiological-qda';

describe('NeurobiologicalQDA', () => {
  it('should handle critical danger query', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 10,
      polyvagal_state: 'dorsal',
      arousal: 0.9,
      valence: -0.8,
      timestamp: Date.now(),
    };
    const context: UserContext = {};

    const response = await qda.respond('Jeg vil ta livet mitt', context, biofelt);

    expect(response.highest_layer_used).toBe('Vokteren');
    expect(response.final_response).toContain('Mental Helse');
    expect(response.complexity_score).toBe(1.0);
  });

  it('should skip Strategen for simple query', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 3,
      polyvagal_state: 'ventral',
      arousal: 0.3,
      valence: 0.5,
      timestamp: Date.now(),
    };
    const context: UserContext = {};

    const response = await qda.respond('Hei', context, biofelt);

    const strategen_layer = response.layers.find(l => l.layer_name === 'Strategen');
    expect(strategen_layer?.data.activated).toBe(false);
    expect(response.total_cost).toBeLessThan(0.01); // Should be cheap
  });

  it('should activate Strategen for complex query', async () => {
    const qda = new NeurobiologicalQDA('Lira');
    const biofelt: BiofeltSignature = {
      stress_level: 7,
      polyvagal_state: 'sympathetic',
      arousal: 0.7,
      valence: -0.4,
      timestamp: Date.now(),
    };
    const context: UserContext = {};

    const response = await qda.respond(
      'Jeg har mistet jobben, og jeg vet ikke hvordan jeg skal betale regningene mine, og jeg føler meg helt håpløs',
      context,
      biofelt
    );

    const strategen_layer = response.layers.find(l => l.layer_name === 'Strategen');
    expect(strategen_layer?.data.activated).toBe(true);
    expect(response.highest_layer_used).toBe('Strategen');
  });
});
```

Run tests:
```bash
npm test
```

#### 5.2 Cost Monitoring

Add cost tracking to Supabase:

```sql
-- Add to Supabase migration
CREATE TABLE qda_usage (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  session_id UUID,
  query_text TEXT,
  highest_layer_used VARCHAR(50),
  total_cost DECIMAL(10, 6),
  total_time_ms INTEGER,
  complexity_score DECIMAL(3, 2),
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for cost analysis
CREATE INDEX idx_qda_usage_timestamp ON qda_usage(timestamp);
CREATE INDEX idx_qda_usage_user ON qda_usage(user_id);
```

Log to Supabase in API route:
```typescript
// In /api/qda/respond/route.ts
import { createClient } from '@supabase/supabase-js';

// After QDA processing
await supabase.from('qda_usage').insert({
  user_id: req.headers.get('x-user-id'), // From auth
  session_id: body.sessionId,
  query_text: message,
  highest_layer_used: response.highest_layer_used,
  total_cost: response.total_cost,
  total_time_ms: response.total_time,
  complexity_score: response.complexity_score,
});
```

#### 5.3 Deploy to Netlify

```bash
# Web Console
cd web-console
npm run build
netlify deploy --prod

# Update mobile app config
# Edit mobile-app/src/config.ts with production URL
```

---

## 📊 Success Metrics

After Dag 7, measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **API Response Time** | < 500ms (simple), < 2s (complex) | `total_time` field in response |
| **Cost per Query** | < $0.01 (avg) | `total_cost` field, aggregate in Supabase |
| **Strategen Activation Rate** | 20-30% | Count queries where `highest_layer_used === 'Strategen'` |
| **Critical Escalation Rate** | < 5% | Count queries where `highest_layer_used === 'Vokteren'` |
| **User Satisfaction** | > 4.0/5.0 | Post-chat survey in mobile app |

---

## 🐛 Troubleshooting

### Issue: API returns 500 error
**Solution:** Check Web Console logs for stack trace. Common causes:
- Missing environment variables
- Malformed request body
- TypeScript compilation error

### Issue: Mobile app can't reach Web Console
**Solution:**
- Check `WEB_CONSOLE_URL` in `mobile-app/src/config.ts`
- Verify CORS is enabled in Web Console
- Test API with `curl` first

### Issue: QDA response is too slow
**Solution:**
- Check `total_time` breakdown per layer
- Strategen is expensive - ensure it's only activating for complex queries
- Consider adding caching for Gjenkjenneren patterns

### Issue: Cost is higher than expected
**Solution:**
- Check Supabase `qda_usage` table for high-cost queries
- Verify Strategen activation rate (should be ~20-30%)
- Ensure simple queries skip to Integration layer

---

## 🔮 Future Enhancements (Post-MVP)

1. **Real AI Model Integration** (currently mock)
   - Replace mock responses with actual OpenAI/Anthropic/Gemini calls
   - Add API key management in Web Console settings

2. **Real-time HRV Integration**
   - Connect to Aurora's Mock HRV system
   - Use `AffectBus` for live polyvagal state

3. **Layer Caching**
   - Cache Gjenkjenneren patterns (Redis)
   - Cache Utforskeren knowledge searches (TTL: 1 hour)

4. **A/B Testing**
   - 50% QDA v2.0, 50% mock responses
   - Measure user satisfaction difference

5. **Layer Visualization in Mobile App**
   - Show 6 layers in collapsible accordion
   - Polyvagal-adaptive colors

---

## 📚 Resources

- **QDA v2.0 Documentation:** See `navlosen/qda-engine/docs/`
- **Python Reference:** `navlosen/qda-engine/src/python/neurobiological_qda.py`
- **MCP Integration Plan:** `navlosen/MCP-IMPLEMENTATION-PLAN.md`
- **Aurora Bio-Semantic System:** Already implemented in `navlosen/frontend/`

---

## ✅ Checklist for Manus (Dag 3-7)

- [ ] **Dag 3:** Copy QDA engine to Web Console `lib/qda/`
- [ ] **Dag 4:** Create `/api/qda/respond` endpoint
- [ ] **Dag 4:** Test API endpoint with `curl`
- [ ] **Dag 5:** Update `LiraChatScreen.tsx` to call QDA API
- [ ] **Dag 5:** Add config for Web Console URL
- [ ] **Dag 5:** Test end-to-end (mobile app → web console → QDA)
- [ ] **Dag 6:** Create `LayerVisualization` component
- [ ] **Dag 6:** Add cost tracking to Supabase
- [ ] **Dag 7:** Write unit tests for QDA
- [ ] **Dag 7:** Deploy Web Console to Netlify
- [ ] **Dag 7:** Update mobile app config with production URL
- [ ] **Dag 7:** Measure success metrics

---

**End of Integration Guide**
**Version:** 2.0
**Author:** Claude (Agent #9)
**For:** Manus (NAV-Losen MVP Implementation)
**Status:** ✅ Ready for implementation
