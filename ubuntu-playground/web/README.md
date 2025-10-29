# GENOMOS Mobile Web Interface

Mobile-friendly React components for submitting consultations and viewing history from the GENOMOS blockchain.

## Overview

This directory contains:

- **`MobileQueryPanel`** - Submit questions to AI agents
- **`ConsultationHistory`** - View past consultations from blockchain
- **`MobileConsultationPage`** - Complete page combining both components

## Quick Start

### Installation

```bash
cd web
npm install
```

### Usage in React App

```tsx
import { MobileConsultationPage } from './pages/MobileConsultationPage';

function App() {
  return (
    <MobileConsultationPage apiUrl="http://localhost:8000" />
  );
}
```

### Usage in React Native (WebView)

```tsx
import { WebView } from 'react-native-webview';

function ConsultationScreen() {
  return (
    <WebView
      source={{ uri: 'http://your-server.com/mobile-consultation' }}
      style={{ flex: 1 }}
    />
  );
}
```

## Components

### MobileQueryPanel

Submit questions to the GENOMOS consultation system:

```tsx
import { MobileQueryPanel } from './components/MobileQueryPanel';

<MobileQueryPanel
  apiUrl="http://localhost:8000"
  onConsultationStored={(consultationId) => {
    console.log('Stored:', consultationId);
  }}
/>
```

**Features:**
- ✅ Mobile-optimized textarea input
- ✅ Real-time submission to API
- ✅ Stores consultation in blockchain + SQLite + Google Sheets
- ✅ Success feedback with block number and hash
- ✅ Active agent indicators

### ConsultationHistory

View past consultations from the blockchain:

```tsx
import { ConsultationHistory } from './components/ConsultationHistory';

<ConsultationHistory
  apiUrl="http://localhost:8000"
  limit={20}
  searchQuery="optional search term"
/>
```

**Features:**
- ✅ Mobile-friendly card layout
- ✅ Real-time relative timestamps ("2h ago")
- ✅ Agent count, SMK references, validation badges
- ✅ Tap to view full consultation details
- ✅ Modal popup for detailed view

### MobileConsultationPage

Complete page with tabs:

```tsx
import { MobileConsultationPage } from './pages/MobileConsultationPage';

<MobileConsultationPage apiUrl="http://localhost:8000" />
```

**Features:**
- ✅ Tab navigation (Ask Question / History)
- ✅ Auto-switch to history after submission
- ✅ Auto-refresh history when new consultation added
- ✅ Sticky header and tab bar
- ✅ Responsive design (works on all screen sizes)

## API Endpoints Used

### Submit Consultation

```http
POST /api/store-consultation
Content-Type: application/json

{
  "consultation_id": "CONS_1234567890",
  "human_query": "What is the meaning of life?",
  "agent_responses": {
    "manus": {
      "response": "The meaning of life...",
      "confidence": 0.92,
      "processing_time_ms": 234
    }
  },
  "synthesis": {
    "summary": "Multiple perspectives converge...",
    "key_insights": ["..."],
    "related_smk": []
  }
}
```

**Response:**
```json
{
  "success": true,
  "consultation_id": "CONS_1234567890",
  "blockchain_block_index": 42,
  "blockchain_hash": "0xabcd1234...",
  "database_id": 15,
  "message": "Consultation stored in GENOMOS blockchain, SQLite, and Google Sheets"
}
```

### Get Consultations

```http
GET /api/dna/consultations?limit=20&query=search+term
```

**Response:**
```json
[
  {
    "consultation_id": "CONS_1234567890",
    "block_index": 42,
    "human_query": "What is the meaning of life?",
    "agent_count": 5,
    "synthesis_summary": "Multiple perspectives converge...",
    "related_smk": ["SMK#019", "SMK#042"],
    "has_biofelt_context": true,
    "has_thalos_validation": true,
    "timestamp": "2025-10-29T12:34:56Z",
    "hash": "0xabcd1234..."
  }
]
```

### Get Consultation Details

```http
GET /api/dna/consultations/{consultation_id}
```

**Response:**
```json
{
  "consultation_id": "CONS_1234567890",
  "block_index": 42,
  "timestamp": "2025-10-29T12:34:56Z",
  "human_query": "What is the meaning of life?",
  "agent_responses": {
    "manus": { "response": "...", "confidence": 0.92 },
    "lira": { "response": "...", "confidence": 0.88 }
  },
  "synthesis": {
    "summary": "...",
    "key_insights": ["..."],
    "related_smk": ["SMK#019"]
  },
  "biofelt_context": { ... },
  "thalos_validation": { ... },
  "hash": "0xabcd1234...",
  "previous_hash": "0xdef5678..."
}
```

## Design Philosophy

### Mobile-First Approach

All components are designed with mobile devices in mind:

- ✅ Touch-friendly tap targets (minimum 44x44px)
- ✅ Large, readable text (16px minimum)
- ✅ Responsive layouts (flexbox, mobile breakpoints)
- ✅ Optimized for thumb navigation
- ✅ Minimal data usage (lazy loading, pagination)

### Blockchain Integration

Every consultation is:

1. **Stored in blockchain** (immutable, cryptographically verified)
2. **Logged to SQLite** (fast queries, backward compatibility)
3. **Synced to Google Sheets** (collaboration, visualization)

This triple-redundancy ensures:
- 🔒 Immutability (blockchain)
- ⚡ Performance (SQLite)
- 📊 Accessibility (Google Sheets)

## Customization

### Styling

All components use inline styles for portability. To customize:

```tsx
<MobileQueryPanel
  apiUrl="http://localhost:8000"
  // Override styles by wrapping in custom div
/>
```

### Agent Configuration

Edit `AVAILABLE_AGENTS` in `MobileQueryPanel.tsx`:

```typescript
const AVAILABLE_AGENTS: Agent[] = [
  { name: 'manus', color: '#4CAF50' },
  { name: 'your-agent', color: '#9C27B0' },
];
```

## Testing

### Manual Testing Checklist

- [ ] Submit question on mobile browser
- [ ] View consultation in history
- [ ] Tap consultation for details
- [ ] Verify blockchain storage (check block number)
- [ ] Test search functionality
- [ ] Verify responsive design (various screen sizes)

### Integration Testing

```bash
# Start API server
cd ../api
uvicorn main:app --reload

# Open mobile browser
# Navigate to: http://localhost:3000/mobile-consultation
```

## Deployment

### Option 1: Standalone React App

```bash
npm run build
# Deploy build/ folder to hosting service
```

### Option 2: Embed in Existing App

```tsx
import { MobileQueryPanel } from '@genomos/mobile-web';

// Use in your existing React app
```

### Option 3: React Native WebView

```tsx
<WebView source={{ uri: 'https://your-domain.com/mobile' }} />
```

## Browser Support

- ✅ iOS Safari 13+
- ✅ Chrome Mobile 80+
- ✅ Samsung Internet 12+
- ✅ Firefox Mobile 68+

## Architecture Diagram

```
┌─────────────────────────────────────┐
│   Mobile Device (Browser/WebView)  │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  MobileConsultationPage       │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │  MobileQueryPanel       │ │ │
│  │  │  - Submit question      │ │ │
│  │  │  - Show success         │ │ │
│  │  └─────────────────────────┘ │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │  ConsultationHistory    │ │ │
│  │  │  - List consultations   │ │ │
│  │  │  - View details         │ │ │
│  │  └─────────────────────────┘ │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
              ↓ HTTPS
┌─────────────────────────────────────┐
│   FastAPI Backend (Ubuntu API)      │
│                                     │
│  POST /api/store-consultation       │
│  GET  /api/dna/consultations        │
│  GET  /api/dna/consultations/:id    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   GENOMOS Storage (Triple Redundancy│
│                                     │
│  ┌───────────┐  ┌──────────────┐   │
│  │ Blockchain│  │   SQLite     │   │
│  │ (immutable│  │  (queries)   │   │
│  └───────────┘  └──────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Google Sheets             │   │
│  │   (collaboration)           │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Future Enhancements

- [ ] Offline mode (IndexedDB cache)
- [ ] Push notifications for responses
- [ ] Voice input for questions
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Pattern recognition insights display
- [ ] SMK reference viewer (tap to expand)

## Contributing

See main repository README for contribution guidelines.

## License

MIT License - See LICENSE file in root directory.

## Support

For issues or questions:
- GitHub Issues: https://github.com/homo-lumen/genomos/issues
- Email: dev@cognitivesovereignty.network
