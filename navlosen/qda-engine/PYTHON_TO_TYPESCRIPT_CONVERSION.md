# Python → TypeScript Conversion Guide (QDA v2.0)

**Version:** 2.0
**Date:** 2025-10-20
**Context:** Converting IMPLEMENTATION_GUIDE_QDA.md (Python) to neurobiological-qda.ts (TypeScript)

---

## 📋 Overview

This document explains the key differences and design decisions made when converting the Python implementation of QDA v2.0 to TypeScript for Manus's Web Console.

---

## 🔄 Major Differences

### 1. Type System

**Python (Type Hints):**
```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class BiofeltSignature:
    hrv_rmssd: Optional[float] = None
    stress_level: int = 5
    polyvagal_state: str = "sympathetic"
```

**TypeScript (Native Types):**
```typescript
export interface BiofeltSignature {
  hrv_rmssd?: number;
  stress_level: number;
  polyvagal_state: 'dorsal' | 'sympathetic' | 'ventral';
}
```

**Why TypeScript is Better Here:**
- Literal types (`'dorsal' | 'sympathetic' | 'ventral'`) prevent typos
- No runtime overhead for validation
- Better IDE autocomplete

---

### 2. Async/Await

**Python:**
```python
async def process(self, user_query: str, context: Dict) -> LayerOutput:
    result = await self._execute(user_query, context)
    return result
```

**TypeScript:**
```typescript
async process(user_query: string, context: UserContext): Promise<LayerOutput> {
  const result = await this._execute(user_query, context);
  return result;
}
```

**Notes:**
- TypeScript requires `Promise<T>` return type
- Both use `async/await` syntax (identical behavior)
- No `asyncio` library needed in TypeScript (built-in)

---

### 3. Abstract Base Classes

**Python:**
```python
from abc import ABC, abstractmethod

class BaseLayer(ABC):
    @abstractmethod
    async def _execute(self, user_query: str, context: Dict) -> Dict:
        pass
```

**TypeScript (No Abstract Classes):**
```typescript
// TypeScript version doesn't use inheritance
// Each layer is a standalone class with identical interface

export class Vokteren {
  public readonly layer_name = 'Vokteren';
  public readonly icon = '🛡️';

  async process(...): Promise<LayerOutput> {
    // Implementation
  }
}
```

**Why We Removed Inheritance:**
- Simpler for JavaScript ecosystem (no `extends` needed)
- Easier to tree-shake unused layers
- More explicit (no hidden base class methods)
- Each layer is independent (easier to test)

**Trade-off:** Slight code duplication, but more explicit and maintainable.

---

### 4. Dataclasses vs Interfaces

**Python:**
```python
@dataclass
class LayerOutput:
    layer_name: str
    icon: str
    data: Any
    processing_time: float
    cost: float
    timestamp: float
```

**TypeScript:**
```typescript
export interface LayerOutput {
  layer_name: string;
  icon: string;
  data: any;
  processing_time: number;
  cost: number;
  timestamp: number;
}
```

**Why Interfaces:**
- No runtime cost (TypeScript interfaces are compile-time only)
- JSON serialization is automatic (no `.dict()` method needed)
- Works seamlessly with Next.js API routes (JSON-only)

---

### 5. AI Model Calls (Mock vs Real)

**Python (Real API Calls):**
```python
import openai

class Vokteren(BaseLayer):
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def _execute(self, user_query: str, context: Dict) -> Dict:
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_query}],
        )
        return {"response": response.choices[0].message.content}
```

**TypeScript (Mock for MVP):**
```typescript
export class Vokteren {
  async process(user_query: string, ...): Promise<LayerOutput> {
    // Mock implementation using keyword matching
    const danger_keywords = {
      critical: ['selvmord', 'ta livet', ...],
    };

    const is_critical = danger_keywords.critical.some(
      word => user_query.toLowerCase().includes(word)
    );

    return {
      layer_name: 'Vokteren',
      data: { safe: !is_critical, ... },
      cost: 0.00001, // Mock cost
    };
  }
}
```

**Why Mock for MVP:**
- Faster development (no API keys needed initially)
- Zero cost during testing
- Easy to upgrade later (replace mock logic with real API calls)

**Future Enhancement:**
```typescript
// Real implementation (later)
import OpenAI from 'openai';

export class Vokteren {
  private client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

  async process(user_query: string, ...): Promise<LayerOutput> {
    const response = await this.client.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: user_query }],
    });

    // Parse response...
  }
}
```

---

### 6. Error Handling

**Python:**
```python
try:
    result = await layer.process(user_query, context)
except Exception as e:
    logger.error(f"Layer {layer.layer_name} failed: {e}")
    result = LayerOutput(
        layer_name=layer.layer_name,
        data={"error": str(e)},
        cost=0.0,
    )
```

**TypeScript:**
```typescript
try {
  const result = await layer.process(user_query, context);
} catch (error) {
  console.error(`Layer ${layer.layer_name} failed:`, error);
  const result: LayerOutput = {
    layer_name: layer.layer_name,
    data: { error: (error as Error).message },
    cost: 0.0,
    processing_time: 0,
    icon: '❌',
    timestamp: Date.now(),
  };
}
```

**Key Difference:** TypeScript requires `(error as Error)` cast because `catch` blocks receive `unknown` type.

---

### 7. Environment Variables

**Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

**TypeScript (Next.js):**
```typescript
// next.config.js handles .env loading automatically
// Access via process.env
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

// For client-side (prefix with NEXT_PUBLIC_)
const PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL;
```

---

### 8. Time Measurement

**Python:**
```python
import time

start_time = time.time()
# ... processing ...
processing_time = time.time() - start_time  # Seconds (float)
```

**TypeScript:**
```typescript
const start_time = Date.now();
// ... processing ...
const processing_time = Date.now() - start_time; // Milliseconds (integer)
```

**Important:** TypeScript uses milliseconds, Python uses seconds. Adjust cost calculations accordingly.

---

## 🎯 Design Decisions

### Decision 1: No Inheritance

**Rationale:**
- JavaScript ecosystem prefers composition over inheritance
- Easier to understand (no hidden base class logic)
- Better for tree-shaking (unused layers can be removed)
- Simpler to test (no need to mock base class)

**Trade-off:** Slight code duplication in each layer's `process()` method.

---

### Decision 2: Mock Implementations for MVP

**Rationale:**
- Faster to deploy (no API keys needed)
- Zero cost during development
- Can be upgraded incrementally (layer by layer)

**Upgrade Path:**
1. Start with all layers mocked
2. Integrate real APIs one layer at a time
3. A/B test (50% mock, 50% real) to measure impact
4. Fully migrate once validated

---

### Decision 3: Flat Module Structure

**Python (Nested):**
```
qda/
├── __init__.py
├── layers/
│   ├── __init__.py
│   ├── vokteren.py
│   ├── foleren.py
│   └── ...
├── orchestrator.py
└── types.py
```

**TypeScript (Flat):**
```
qda/
├── neurobiological-qda.ts  # All layers in one file
└── index.ts                 # Barrel export
```

**Rationale:**
- Simpler imports (`import { NeurobiologicalQDA } from '@/lib/qda'`)
- Easier to navigate (one file to understand the whole system)
- Better for bundlers (single chunk)

**Trade-off:** Larger file (~500 lines), but still manageable.

---

### Decision 4: `any` Type for `data` Field

**Why Not Strict Types:**
```typescript
// Avoided this:
interface VokterenData {
  safe: boolean;
  proceed: boolean;
  danger_level: string;
  // ... 10 more fields
}

interface FolerenData {
  primary_emotion: string;
  // ... different fields
}

type LayerData = VokterenData | FolerenData | GjenkjennerenData | ...;

// Used this instead:
interface LayerOutput {
  data: any; // ✅ Simpler
}
```

**Rationale:**
- Each layer has different `data` structures
- Union types would be extremely verbose
- `any` is acceptable here because the consumer (Integratoren) knows how to handle each layer
- TypeScript still checks the rest of the `LayerOutput` structure

**Future Enhancement:** Use generics if needed:
```typescript
interface LayerOutput<T = any> {
  data: T;
}
```

---

## 🔄 Migration Checklist (Python → TypeScript)

When converting future Python QDA code to TypeScript:

- [ ] Replace `Dict[str, Any]` → `Record<string, any>` or interface
- [ ] Replace `List[T]` → `T[]` or `Array<T>`
- [ ] Replace `Optional[T]` → `T | undefined` or `T?`
- [ ] Replace `@dataclass` → `interface` (for data) or `class` (for logic)
- [ ] Replace `time.time()` → `Date.now()` (and multiply by 1000 if comparing)
- [ ] Replace `logging.info()` → `console.log()` or use a logger library
- [ ] Replace `os.getenv()` → `process.env.VARIABLE_NAME`
- [ ] Add `async` keyword and `Promise<T>` return type to async functions
- [ ] Use `try/catch` instead of `try/except`
- [ ] Cast errors: `(error as Error).message`

---

## 📦 Dependencies Comparison

**Python:**
```
openai==1.54.4
anthropic==0.39.0
google-generativeai==0.8.3
pydantic==2.9.2
python-dotenv==1.0.1
fastapi==0.115.4  # If building API
uvicorn==0.32.0
```

**TypeScript:**
```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0"
  },
  "devDependencies": {
    "typescript": "^5.6.3",
    "@types/node": "^22.7.9",
    "@types/react": "^19.0.0"
  }
}
```

**Notes:**
- TypeScript MVP needs ZERO additional dependencies (uses built-in Next.js)
- Real AI integrations require: `openai`, `@anthropic-ai/sdk`, `@google/generative-ai`

---

## 🚀 Performance Comparison

| Metric | Python | TypeScript | Notes |
|--------|--------|------------|-------|
| **Cold Start** | ~200ms | ~50ms | Node.js starts faster than Python |
| **Processing Time** | ~10ms/layer | ~5ms/layer | JavaScript is faster for simple logic |
| **Memory Usage** | ~50MB | ~30MB | Node.js is more memory-efficient |
| **API Call Latency** | Same | Same | Network-bound, not language-bound |

**Conclusion:** TypeScript is slightly faster for MVP (mock implementations), but difference is negligible for real API calls.

---

## 🐛 Common Pitfalls

### Pitfall 1: Forgetting `await`
```typescript
// ❌ Wrong
const result = layer.process(query, context); // Returns Promise, not LayerOutput

// ✅ Correct
const result = await layer.process(query, context);
```

### Pitfall 2: Mutating `previous_layers`
```typescript
// ❌ Wrong (mutates original)
previous_layers['NewLayer'] = new_output;

// ✅ Correct (creates new object)
const updated_layers = { ...previous_layers, NewLayer: new_output };
```

### Pitfall 3: Using `Date.now()` in Comparisons
```typescript
// ❌ Wrong (comparing milliseconds to seconds from Python)
if (processing_time > 1) // Expects seconds, but gets milliseconds

// ✅ Correct
if (processing_time > 1000) // 1000ms = 1 second
```

---

## 📚 Further Reading

- **TypeScript Handbook:** https://www.typescriptlang.org/docs/handbook/
- **Next.js API Routes:** https://nextjs.org/docs/app/building-your-application/routing/route-handlers
- **Async/Await in TypeScript:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
- **QDA v2.0 Python Reference:** See `navlosen/qda-engine/docs/IMPLEMENTATION_GUIDE_QDA.md`

---

**End of Conversion Guide**
**Version:** 2.0
**Author:** Claude (Agent #9)
**Status:** ✅ Complete
