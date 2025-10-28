# Ubuntu Playground TypeScript SDK

Type-safe client for Ubuntu Playground API with Triadiske Portvokter support.

## Features

- ✅ **BiofeltGate Integration** - HRV-based consciousness validation
- ✅ **ThalosFilter Integration** - Ethical veto system
- ✅ **MutationLog Support** - Append-only audit trail
- ✅ **Type Safety** - Full TypeScript support with interfaces
- ✅ **NAV Losen Compatible** - Utility to convert HealthConnectData → BiofeltContext

## Installation

```bash
npm install @homo-lumen/ubuntu-playground-sdk
```

## Quick Start

```typescript
import UbuntuPlaygroundClient, { BiofeltContext } from '@homo-lumen/ubuntu-playground-sdk';

// Initialize client
const client = new UbuntuPlaygroundClient(
  "http://localhost:8002",
  "your-api-key"
);

// Check API health
const health = await client.health();
console.log(health);

// Write a file with BiofeltContext
const biofeltContext: BiofeltContext = {
  hrv_ms: 75,           // Good HRV
  coherence: 0.80,      // High coherence
  pust_rytme: "4-6-8",  // Breathing rhythm
  energy_level: "balanced",
  stress_indicators: []
};

await client.writeFile({
  path: "shared/test.txt",
  content: "Hello from NAV Losen!",
  biofelt_context: biofeltContext
});
```

## NAV Losen Integration

Convert NAV Losen `HealthConnectData` to `BiofeltContext`:

```typescript
import { healthDataToBiofeltContext, calculateResonanceLevel } from '@homo-lumen/ubuntu-playground-sdk';

// NAV Losen health data
const healthData = {
  hrv: 75,
  heartRate: 65,
  sleepQuality: "good" as const,
  sleepHours: 7.5
};

const stressLevel = 3;
const somaticSignals = ["rolig pust", "avslappet"];

// Convert to BiofeltContext
const biofeltContext = healthDataToBiofeltContext(
  healthData,
  stressLevel,
  somaticSignals
);

console.log("Resonance Level:", calculateResonanceLevel(biofeltContext.hrv_ms));
```

## API Reference

### `UbuntuPlaygroundClient`

#### Constructor

```typescript
new UbuntuPlaygroundClient(baseUrl?: string, apiKey: string)
```

#### Methods

**`health(): Promise<HealthResponse>`**

Check API health status.

**`writeFile(request: WriteRequest): Promise<WriteResponse>`**

Write a file to the shared workspace.

```typescript
interface WriteRequest {
  path: string;
  content: string;
  biofelt_context?: BiofeltContext;
  thalos_context?: ThalosContext;
}
```

**`readFile(request: ReadRequest): Promise<ReadResponse>`**

Read a file from the shared workspace.

**`executeAction(request: ExecuteActionRequest): Promise<ExecuteActionResponse>`**

Execute an action (e.g., from CSN Server).

### Types

#### `BiofeltContext`

```typescript
interface BiofeltContext {
  hrv_ms: number;              // Heart Rate Variability (0-200)
  coherence: number;           // Coherence score (0.0-1.0)
  pust_rytme?: string;         // Breathing rhythm (e.g., "4-6-8")
  resonance_theme?: string;    // Felt-resonance theme
  energy_level?: string;       // Energy level
  stress_indicators?: string[]; // Stress indicators
  timestamp?: string;          // ISO timestamp
}
```

#### `ThalosContext`

```typescript
interface ThalosContext {
  intent?: string;             // Intent behind the action
  justification?: string;      // Justification
  affected_agents?: string[];  // Affected agents
  reversible?: boolean;        // Is reversible?
  reviewed_by?: string;        // Reviewer agent
  emergency?: boolean;         // Emergency situation?
  timestamp?: string;          // ISO timestamp
}
```

#### `ResonanceLevel`

```typescript
enum ResonanceLevel {
  CRITICAL = "critical",       // HRV < 40
  LOW = "low",                // HRV 40-64
  BALANCED = "balanced",      // HRV 65-79
  OPTIMAL = "optimal",        // HRV 80-99
  TRANSCENDENT = "transcendent" // HRV 100+
}
```

## Error Handling

When BiofeltGate or ThalosFilter blocks an operation, a detailed error is thrown:

```typescript
try {
  await client.writeFile({
    path: "critical/file.txt",
    content: "data",
    biofelt_context: { hrv_ms: 30, coherence: 0.3 } // Low HRV!
  });
} catch (error) {
  console.error(error.message);
  // Error includes recommendations:
  // "BiofeltGate blocked operation: HRV too low (30 ms)
  //
  // Recommendations:
  // - Practice 4-6-8 breathing exercise
  // - Take a break before continuing"
}
```

## Architecture

This SDK integrates with the **Triadiske Portvokter** (Triadic Gates) architecture:

1. **BiofeltGate** - Consciousness-aware processing (HRV validation)
2. **ThalosFilter** - Ethical veto system (principle-based validation)
3. **MutationLog** - Append-only audit trail (complete operation history)

### Philosophy

> "Koden puster med Osvalds puls (4-6-8)"
> — NB, on Triadiske Portvokter

The system validates operations through three lenses:
- **Consciousness**: "Are we in the right state?" (BiofeltGate)
- **Conscience**: "Is this the right thing to do?" (ThalosFilter)
- **Memory**: "Will we remember and learn from this?" (MutationLog)

## Development

```bash
# Build TypeScript
npm run build

# Run example
ts-node index.ts
```

## License

MIT

## Related

- [Ubuntu Playground API](../../api/)
- [Triadiske Portvokter Documentation](../../docs/triadiske-portvokter.md)
- [SMK #040 - Triadiske Portvokter](../../../SMK/SMK#040_TriadiskePortvokter-CompleteImplementation.md)
- [CODE_LK_V1721](../../../CODE_LK_V1721_UPDATE.md)
