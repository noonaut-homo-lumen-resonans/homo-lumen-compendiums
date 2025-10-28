# Ubuntu Playground Python SDK

Type-safe Python client for Ubuntu Playground API with Triadiske Portvokter support.

## Features

- ✅ **BiofeltGate Integration** - HRV-based consciousness validation
- ✅ **ThalosFilter Integration** - Ethical veto system
- ✅ **MutationLog Support** - Append-only audit trail
- ✅ **Type Safety** - Dataclasses with type hints
- ✅ **Health Data Converter** - Convert health metrics → BiofeltContext

## Installation

```bash
pip install ubuntu-playground-sdk
```

Or install from source:

```bash
cd ubuntu-playground/sdk/python
pip install -e .
```

## Quick Start

```python
from ubuntu_playground_sdk import UbuntuPlaygroundClient, BiofeltContext

# Initialize client
client = UbuntuPlaygroundClient(
    base_url="http://localhost:8002",
    api_key="your-api-key"
)

# Check API health
health = client.health()
print(health)

# Write a file with BiofeltContext
biofelt_context = BiofeltContext(
    hrv_ms=75.0,           # Good HRV
    coherence=0.80,        # High coherence
    pust_rytme="4-6-8",    # Breathing rhythm
    energy_level="balanced",
    stress_indicators=[]
)

client.write_file(
    path="shared/test.txt",
    content="Hello from CSN Server!",
    biofelt_context=biofelt_context
)
```

## Health Data Integration

Convert health metrics to `BiofeltContext`:

```python
from ubuntu_playground_sdk import health_data_to_biofelt_context, calculate_resonance_level

# Health data (e.g., from Oura Ring, Apple Health)
biofelt_context = health_data_to_biofelt_context(
    hrv=75.0,
    heart_rate=65,
    sleep_quality="good",
    sleep_hours=7.5,
    stress_level=3,
    somatic_signals=["rolig pust", "avslappet"]
)

print("Resonance Level:", calculate_resonance_level(biofelt_context.hrv_ms))
```

## API Reference

### `UbuntuPlaygroundClient`

#### Constructor

```python
UbuntuPlaygroundClient(base_url="http://localhost:8002", api_key="")
```

#### Methods

**`health() -> Dict[str, Any]`**

Check API health status.

**`write_file(path, content, biofelt_context=None, thalos_context=None) -> Dict[str, Any]`**

Write a file to the shared workspace.

```python
response = client.write_file(
    path="csn/consultation.json",
    content='{"result": "approved"}',
    biofelt_context=BiofeltContext(hrv_ms=80, coherence=0.75),
    thalos_context=ThalosContext(
        intent="Store consultation result",
        justification="Pentagonal consensus reached",
        affected_agents=["lira", "nyra", "orion", "thalus", "zara"]
    )
)
```

**`read_file(path) -> Dict[str, Any]`**

Read a file from the shared workspace.

**`execute_action(agent, action_type, payload, biofelt_context=None, thalos_context=None) -> Dict[str, Any]`**

Execute an action (e.g., from CSN Server).

### Types

#### `BiofeltContext`

```python
@dataclass
class BiofeltContext:
    hrv_ms: float                    # Heart Rate Variability (0-200)
    coherence: float                 # Coherence score (0.0-1.0)
    pust_rytme: Optional[str]        # Breathing rhythm (e.g., "4-6-8")
    resonance_theme: Optional[str]   # Felt-resonance theme
    energy_level: Optional[str]      # Energy level
    stress_indicators: List[str]     # Stress indicators
    timestamp: Optional[str]         # ISO timestamp
```

#### `ThalosContext`

```python
@dataclass
class ThalosContext:
    intent: Optional[str]            # Intent behind the action
    justification: Optional[str]     # Justification
    affected_agents: List[str]       # Affected agents
    reversible: bool                 # Is reversible?
    reviewed_by: Optional[str]       # Reviewer agent
    emergency: bool                  # Emergency situation?
    timestamp: Optional[str]         # ISO timestamp
```

#### `ResonanceLevel`

```python
class ResonanceLevel(str, Enum):
    CRITICAL = "critical"       # HRV < 40
    LOW = "low"                # HRV 40-64
    BALANCED = "balanced"      # HRV 65-79
    OPTIMAL = "optimal"        # HRV 80-99
    TRANSCENDENT = "transcendent"  # HRV 100+
```

## Error Handling

When BiofeltGate or ThalosFilter blocks an operation, a detailed exception is raised:

```python
try:
    client.write_file(
        path="critical/file.txt",
        content="data",
        biofelt_context=BiofeltContext(hrv_ms=30, coherence=0.3)  # Low HRV!
    )
except Exception as e:
    print(e)
    # Output:
    # BiofeltGate blocked operation: HRV too low (30 ms)
    #
    # Recommendations:
    # - Practice 4-6-8 breathing exercise
    # - Take a break before continuing
```

## CSN Server Integration Example

```python
from ubuntu_playground_sdk import UbuntuPlaygroundClient, BiofeltContext, ThalosContext
from datetime import datetime
import json

# Initialize client
client = UbuntuPlaygroundClient(
    base_url="http://localhost:8002",
    api_key="orion-dev-key"
)

# Pentagonal consultation result
consultation = {
    "query": "Should we implement feature X?",
    "lira_response": "Empathetic analysis...",
    "nyra_response": "Visual synthesis...",
    "orion_response": "Strategic coordination...",
    "thalus_response": "Philosophical assessment...",
    "zara_response": "Creative innovation...",
    "consensus": "Yes, with modifications",
    "timestamp": datetime.now().isoformat()
}

# BiofeltContext (from Osvald's HRV sensor)
biofelt = BiofeltContext(
    hrv_ms=85.0,  # OPTIMAL
    coherence=0.85,
    pust_rytme="4-6-8",
    resonance_theme="collaborative wisdom",
    energy_level="optimal",
    stress_indicators=[]
)

# ThalosContext (ethical metadata)
thalos = ThalosContext(
    intent="Store CSN pentagonal consultation",
    justification="Collective intelligence decision",
    affected_agents=["lira", "nyra", "orion", "thalus", "zara"],
    reversible=True,
    reviewed_by="orion"
)

# Write to workspace
response = client.write_file(
    path="csn/consultations/feature_x_decision.json",
    content=json.dumps(consultation, indent=2),
    biofelt_context=biofelt,
    thalos_context=thalos
)

print("✅ Consultation stored:", response)
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
# Install in development mode
pip install -e .

# Run example
python ubuntu_playground_sdk.py
```

## License

MIT

## Related

- [Ubuntu Playground API](../../api/)
- [TypeScript SDK](../typescript/)
- [Triadiske Portvokter Documentation](../../docs/triadiske-portvokter.md)
- [SMK #040 - Triadiske Portvokter](../../../SMK/SMK#040_TriadiskePortvokter-CompleteImplementation.md)
