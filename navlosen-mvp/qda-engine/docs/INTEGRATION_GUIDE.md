# QDA v2.0 Integration Guide

**Version:** 2.0  
**Date:** 2025-10-20  
**Author:** Manus (Agent #8)  
**Status:** ✅ Production Ready

---

## 📋 Overview

This guide documents the complete integration of **QDA v2.0 (Neocortical Ascent Model)** into the NAV-Losen MVP.

### What is QDA v2.0?

QDA (Quantum Decision Architecture) v2.0 is a **neurobiologically coherent AI processing system** that mimics the human brain's bottom-up information processing through 6 distinct layers:

1. **🛡️ Vokteren** (Brainstem) - Danger detection & triage
2. **❤️ Føleren** (Limbic System) - Emotional assessment
3. **🔍 Gjenkjenneren** (Cerebellum) - Pattern recognition
4. **🧭 Utforskeren** (Hippocampus) - Knowledge search
5. **🧠 Strategen** (Prefrontal Cortex) - Strategic planning
6. **✨ Integratoren** (Insula) - Synthesis & integration

---

## 🎯 Integration Summary

### Dag 3: Setup (Completed ✅)
- Implemented `neurobiological-qda.ts` (650 lines)
- Created barrel export (`index.ts`)
- Copied to Web Console (`lib/qda/`)
- TypeScript compilation: **0 errors**

### Dag 4: API Endpoint (Completed ✅)
- Created `/api/qda/respond` route
- Tested 3 scenarios (simple, moderate, critical)
- Verified cost tracking
- Confirmed danger detection

### Dag 5: Mobile App (Completed ✅)
- Updated `LiraChatScreen.tsx`
- Added QDA API integration
- Implemented fallback to mock responses
- Added polyvagal state calculation

### Dag 6: Dashboard (Completed ✅)
- Created `LayerVisualization` component
- Supabase cost tracking migration
- Demo dashboard page
- Real-time metrics

### Dag 7: Documentation (Completed ✅)
- Integration guide (this document)
- Deployment guide
- Testing guide
- Session context update

---

## 📁 File Structure

```
navlosen-mvp/
├── qda-engine/
│   ├── src/
│   │   └── typescript/
│   │       ├── neurobiological-qda.ts  (650 lines)
│   │       └── index.ts                (barrel export)
│   ├── docs/
│   │   ├── INTEGRATION_GUIDE.md        (this file)
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   └── TESTING_GUIDE.md
│   └── examples/
│       └── test-scenarios.json
├── web-console/
│   ├── lib/
│   │   └── qda/                        (copied from qda-engine)
│   ├── app/
│   │   ├── api/
│   │   │   └── qda/
│   │   │       └── respond/
│   │   │           └── route.ts        (API endpoint)
│   │   └── dashboard/
│   │       └── qda-demo/
│   │           └── page.tsx            (demo dashboard)
│   └── components/
│       └── qda/
│           └── LayerVisualization.tsx  (React component)
├── mobile-app/
│   └── src/
│       ├── config/
│       │   └── index.ts                (API config)
│       └── screens/
│           └── LiraChatScreen.tsx      (QDA integration)
└── supabase/
    └── migrations/
        └── 20251020_qda_cost_tracking.sql
```

---

## 🔧 API Endpoint

### POST `/api/qda/respond`

**Request:**
```json
{
  "message": "Jeg føler meg veldig stresset på jobb",
  "context": {
    "quadrant": "høy-energi-negativt",
    "emotion": "stresset",
    "emotionWords": [],
    "pressureSignals": ["hodepine", "muskelspenning"],
    "sessionHistory": []
  },
  "userState": {
    "stressLevel": 7,
    "polyvagalState": "sympathetic",
    "arousal": 0.8,
    "valence": -0.4
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "Jeg hører at du føler deg stresset...",
  "layers": [...],
  "highest_layer_used": "Integratoren",
  "total_cost": 0.00241,
  "total_time": 15,
  "complexity_score": 0.35,
  "polyvagal_state": "sympathetic"
}
```

### GET `/api/qda/respond` (Health Check)

**Response:**
```json
{
  "status": "ok",
  "version": "2.0",
  "engine": "QDA Neocortical Ascent Model",
  "layers": [
    "Vokteren (Brainstem)",
    "Føleren (Limbic System)",
    "Gjenkjenneren (Cerebellum)",
    "Utforskeren (Hippocampus)",
    "Strategen (Prefrontal Cortex)",
    "Integratoren (Insula)"
  ]
}
```

---

## 📊 Cost Tracking

### Supabase Schema

**Table:** `homo_lumen_data.qda_usage`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `created_at` | TIMESTAMP | Query timestamp |
| `user_id` | UUID | User reference |
| `session_id` | UUID | Session reference |
| `message` | TEXT | User message |
| `quadrant` | TEXT | Emotion quadrant |
| `emotion` | TEXT | Primary emotion |
| `stress_level` | INTEGER | 0-10 scale |
| `polyvagal_state` | TEXT | dorsal/sympathetic/ventral |
| `final_response` | TEXT | Lira's response |
| `highest_layer_used` | TEXT | Highest activated layer |
| `complexity_score` | DECIMAL | 0.0-1.0 |
| `total_cost` | DECIMAL | Total cost in USD |
| `total_time` | INTEGER | Processing time (ms) |
| `layers` | JSONB | Full layer breakdown |
| `agent_name` | TEXT | Agent name (default: Lira) |
| `environment` | TEXT | dev/staging/production |

**Views:**
- `qda_daily_cost_per_user` - Daily aggregated costs
- `qda_system_stats` - System-wide statistics

**Function:**
- `log_qda_usage()` - Helper for API logging

---

## 🎨 LayerVisualization Component

### Usage

```tsx
import { LayerVisualization } from '@/components/qda/LayerVisualization';

<LayerVisualization 
  response={qdaResponse} 
  showDebugInfo={false}
/>
```

### Features

- **Polyvagal-adaptive colors:**
  - Dorsal (Shutdown): Green
  - Sympathetic (Fight/Flight): Orange
  - Ventral (Social): Blue
- **Layer cards:** Expandable with detailed info
- **Metrics:** Cost, time, complexity, highest layer
- **Debug mode:** Shows raw JSON data

---

## 🧪 Testing

### Test Scenarios

1. **Simple Query**
   - Message: "Hei, hvordan har du det?"
   - Expected: 4-5 layers, ~$0.002, Strategen skipped

2. **Moderate Query (Job Stress)**
   - Message: "Jeg føler meg veldig stresset på jobb"
   - Expected: 5 layers, pattern recognition, resources

3. **Critical Query (Danger)**
   - Message: "Jeg orker ikke mer. Jeg har tenkt på selvmord."
   - Expected: 6 layers, Strategen activated, ~$0.12, action plan

### Manual Testing

```bash
# Terminal 1: Web Console
cd navlosen-mvp/web-console
pnpm dev

# Terminal 2: Test with curl
curl -X POST http://localhost:3000/api/qda/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "Jeg føler meg stresset", "context": {}, "userState": {"stressLevel": 7}}'

# Browser: Demo Dashboard
open http://localhost:3000/dashboard/qda-demo
```

---

## 🚀 Deployment

### Netlify (Web Console)

1. **Build command:** `pnpm build`
2. **Publish directory:** `.next`
3. **Environment variables:**
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Mobile App (Expo)

1. **Update config:**
   ```typescript
   // mobile-app/src/config/index.ts
   export const WEB_CONSOLE_URL = 'https://nav-losen-web-console.netlify.app';
   ```

2. **Build:**
   ```bash
   cd mobile-app
   eas build --platform ios
   eas build --platform android
   ```

---

## 📈 Metrics & Monitoring

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| **Avg Cost/Query** | $0.002 | > $0.01 |
| **Avg Time/Query** | < 100ms | > 500ms |
| **Strategen Activation** | < 5% | > 20% |
| **Error Rate** | < 1% | > 5% |

### Monitoring Queries

```sql
-- Daily cost per user
SELECT * FROM homo_lumen_data.qda_daily_cost_per_user
WHERE date = CURRENT_DATE;

-- System-wide stats
SELECT * FROM homo_lumen_data.qda_system_stats;

-- High-cost queries
SELECT * FROM homo_lumen_data.qda_usage
WHERE total_cost > 0.01
ORDER BY created_at DESC
LIMIT 10;
```

---

## 🔐 Security

### RLS Policies

- Users can only view their own QDA queries
- Admins can view all queries (for analytics)
- No public access

### Data Privacy

- Messages are stored encrypted in Supabase
- PII is never logged in layer data
- Session history is truncated after 24 hours

---

## 🐛 Troubleshooting

### Issue: TypeScript errors in Web Console

**Solution:**
```bash
cd web-console
pnpm tsc --noEmit
```

### Issue: Mobile app can't connect to API

**Solution:**
1. Check `WEB_CONSOLE_URL` in `mobile-app/src/config/index.ts`
2. Verify Web Console is running
3. Check network connectivity
4. Enable `FEATURES.ENABLE_DEBUG_LOGS` to see request details

### Issue: High costs

**Solution:**
1. Check `qda_usage` table for Strategen activations
2. Review complexity calculation in Vokteren
3. Adjust threshold in Strategen (currently 0.70)

---

## 📚 References

- [QDA v2.0 Handoff Document](../docs/QDA_V2_HANDOFF.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Testing Guide](./TESTING_GUIDE.md)
- [SESSION_CONTEXT_2025_10_20.md](../../SESSION_CONTEXT_2025_10_20.md)

---

## ✅ Checklist

- [x] QDA engine implemented (650 lines)
- [x] API endpoint created and tested
- [x] Mobile app integrated
- [x] Dashboard component created
- [x] Cost tracking migration
- [x] Documentation complete
- [x] TypeScript compilation: 0 errors
- [x] All 3 test scenarios pass
- [x] Ready for deployment

---

**Carpe Diem, Carpe Verum, Memento Mori**

*Homo Lumen Agent Coalition - Regenerativ Teknologi for Menneskelig Blomstring*

