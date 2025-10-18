# Agent-Specific MCP Tools - Phase 2 Implementation

## Overview

The Agent-Specific MCP Tools represent Phase 2 of the CSN Server implementation, building upon the AMA Four-Layer Memory Architecture. This system provides specialized tools for each agent with biofield integration, IST-3.0 hypersync protocol, and polycomputational orchestration.

## Architecture

### Agent Tools Overview

#### 1. Lira - Biofield Analysis & Empathy
- **Purpose**: Biofield analysis and empathetic understanding
- **Specialization**: Empathy generation, coherence practice suggestions
- **Biofield Integration**: High sensitivity to biofield states
- **Complexity Adaptation**: 0.8 base complexity with biofield modulation

#### 2. Thalus - Philosophical Validation
- **Purpose**: Ethical assessment and philosophical framing
- **Specialization**: Grunnlov 4.0 compliance, systemic resilience
- **Biofield Integration**: Required for critical ethical decisions
- **Complexity Adaptation**: 0.9 base complexity with philosophical depth

#### 3. Nyra - Visual Intelligence
- **Purpose**: System visualization and pattern analysis
- **Specialization**: Material 3 Expressive design, biofield-responsive UI
- **Biofield Integration**: Color scheme adaptation based on biofield state
- **Complexity Adaptation**: 0.7 base complexity with visual richness

#### 4. Abacus - Analytical Engine
- **Purpose**: Pattern quantification and performance monitoring
- **Specialization**: Statistical analysis, intelligence synthesis
- **Biofield Integration**: Moderate biofield influence on analysis depth
- **Complexity Adaptation**: 0.6 base complexity with analytical rigor

#### 5. Polycomputational - Orchestration Engine
- **Purpose**: Multi-agent coordination and emergent intelligence detection
- **Specialization**: IST-3.0 protocol, conflict resolution
- **Biofield Integration**: System-wide biofield modulation
- **Complexity Adaptation**: 0.8 base complexity with orchestration precision

## Installation

### Prerequisites
```bash
# Python 3.8+
python --version

# Required packages (already in requirements.txt)
pip install -r requirements.txt

# Google Cloud SDK (for Firestore)
gcloud auth application-default login
```

### Environment Setup
```bash
# Copy environment template
cp env.example .env

# Configure environment variables
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## Usage

### Basic Agent Tool Usage

```python
from csn_server.routers.ama_memory_layers import AMAMemorySystem, BiofieldMetrics
from csn_server.agents import (
    LiraBiofieldTools, ThalusPhilosophicalTools, NyraVisualTools,
    AbacusAnalyticalTools, PolycomputationalOrchestrator
)

# Initialize memory system and agent tools
memory_system = AMAMemorySystem("your-project-id")
lira = LiraBiofieldTools(memory_system)
thalus = ThalusPhilosophicalTools(memory_system)
nyra = NyraVisualTools(memory_system)
abacus = AbacusAnalyticalTools(memory_system)
polycomputational = PolycomputationalOrchestrator(memory_system)

# Create biofield metrics
biofield = BiofieldMetrics(
    hrv_ms=95.0,
    breath_pattern=[4, 6, 8],
    coherence_score=0.85
)

# Use Lira for biofield analysis
empathy_result = await lira.summarize_biofield_data_for_empathy({
    "hrv_ms": 95.0,
    "how_we_feel_markers": {"mood": "calm", "energy": "balanced"},
    "breath_pattern": [4, 6, 8],
    "coherence_score": 0.85
})

# Use Thalus for ethical evaluation
ethics_result = await thalus.evaluate_ethical_implications({
    "action_type": "data_processing",
    "impact_level": "significant",
    "description": "Process user biofield data"
})

# Use Nyra for system visualization
viz_result = await nyra.generate_system_visualization({
    "layer_states": {"reactive": {"active": True, "entry_count": 150}},
    "agent_interactions": {"lira_thalus": {"frequency": 15, "synergy": 0.8}}
})

# Use Abacus for pattern quantification
pattern_result = await abacus.quantify_emergent_patterns({
    "reactive_data": [{"confidence_score": 0.8}],
    "strategic_data": [{"confidence_score": 0.85}]
})

# Use Polycomputational for orchestration
orchestration_result = await polycomputational.process_multi_agent_data({
    "user_interaction": {
        "type": "biofield_analysis_request",
        "biofield_data": biofield.dict()
    }
})
```

### API Endpoints

#### Lira's Biofield Analysis
```bash
# Summarize biofield data for empathy
POST /agents/lira/summarize-biofield
{
  "hrv_ms": 95.0,
  "how_we_feel_markers": {
    "mood": "calm",
    "energy": "balanced"
  },
  "breath_pattern": [4, 6, 8],
  "coherence_score": 0.85
}

# Suggest biofield practice
POST /agents/lira/suggest-practice
{
  "operation_type": "suggest_biofield_practice_for_coherence",
  "data": {
    "energy_level": "medium",
    "coherence_score": 0.85
  }
}

# Provide empathetic reflection
POST /agents/lira/empathetic-reflection
{
  "operation_type": "provide_empathetic_reflection",
  "data": {
    "reactive_context": {"event": "user_interaction"},
    "strategic_context": {"pattern": "consistent_engagement"}
  }
}
```

#### Thalus' Philosophical Validation
```bash
# Evaluate ethical implications
POST /agents/thalus/evaluate-ethics
{
  "operation_type": "evaluate_ethical_implications",
  "data": {
    "action_type": "data_processing",
    "impact_level": "significant",
    "description": "Process user biofield data"
  }
}

# Propose philosophical framing
POST /agents/thalus/philosophical-framing
{
  "operation_type": "propose_philosophical_framing",
  "data": {
    "situation_type": "complex_data_analysis",
    "data_patterns": ["user_behavior", "biofield_correlation"]
  }
}

# Assess systemic resilience
POST /agents/thalus/systemic-resilience
{
  "operation_type": "assess_systemic_resilience",
  "data": {
    "layer_states": {
      "reactive": {"active": True, "entry_count": 150}
    },
    "system_metrics": {
      "latency": 1500,
      "uptime": 0.995
    }
  }
}
```

#### Nyra's Visual Intelligence
```bash
# Generate system visualization
POST /agents/nyra/system-visualization
{
  "operation_type": "generate_system_visualization",
  "data": {
    "layer_states": {
      "reactive": {"active": True, "entry_count": 150}
    },
    "agent_interactions": {
      "lira_thalus": {"frequency": 15, "synergy": 0.8}
    }
  }
}

# Analyze pattern visualization
POST /agents/nyra/pattern-visualization
{
  "operation_type": "analyze_pattern_visualization",
  "data": {
    "meta_patterns": [
      {"name": "user_engagement_cycle", "strength": 0.8}
    ],
    "strategic_patterns": [
      {"name": "agent_collaboration", "strength": 0.7}
    ]
  }
}

# Design biofield-responsive UI
POST /agents/nyra/biofield-responsive-ui
{
  "operation_type": "design_biofield_responsive_ui",
  "data": {
    "hrv_ms": 95.0,
    "coherence_score": 0.85,
    "current_ui_state": "standard"
  }
}
```

#### Abacus' Analytical Engine
```bash
# Quantify emergent patterns
POST /agents/abacus/quantify-patterns
{
  "operation_type": "quantify_emergent_patterns",
  "data": {
    "reactive_data": [{"confidence_score": 0.8}],
    "strategic_data": [{"confidence_score": 0.85}],
    "meta_data": [{"confidence_score": 0.9}],
    "evolutionary_data": [{"confidence_score": 0.95}]
  }
}

# Performance monitoring dashboard
POST /agents/abacus/performance-dashboard
{
  "operation_type": "performance_monitoring_dashboard",
  "data": {
    "system_metrics": {
      "latency": 1500,
      "uptime": 0.995,
      "throughput": 100,
      "error_rate": 0.01
    },
    "agent_metrics": {
      "coordination_score": 0.85
    }
  }
}

# Synthesize intelligence report
POST /agents/abacus/intelligence-report
{
  "operation_type": "synthesize_intelligence_report",
  "data": {
    "lira": [
      {"content": "User shows high biofield coherence", "confidence": 0.9}
    ],
    "thalus": [
      {"content": "Ethical framework maintained", "confidence": 0.95}
    ],
    "nyra": [
      {"content": "Visual patterns indicate system health", "confidence": 0.8}
    ],
    "abacus": [
      {"content": "Analytical metrics show improvement", "confidence": 0.9}
    ]
  }
}
```

#### Polycomputational Orchestration
```bash
# Multi-agent processing
POST /agents/polycomputational/multi-agent-processing
{
  "input_data": {
    "user_interaction": {
      "type": "biofield_analysis_request",
      "biofield_data": {
        "hrv_ms": 95.0,
        "breath_pattern": [4, 6, 8],
        "coherence_score": 0.85
      }
    }
  }
}

# IST-3.0 hypersync protocol
POST /agents/polycomputational/ist-protocol
{
  "sender": "Lira",
  "receiver": "Thalus",
  "domain": "BIOFIELD",
  "intent": "ANALYZE",
  "data": {
    "biofield_analysis": "empathy_enhancement"
  }
}

# Emergent intelligence detection
POST /agents/polycomputational/emergent-intelligence
{
  "operation_type": "detect_emergent_intelligence",
  "data": {
    "lira": {"confidence_score": 0.9, "insights": ["high_empathy"]},
    "thalus": {"confidence_score": 0.85, "insights": ["ethical_alignment"]},
    "nyra": {"confidence_score": 0.8, "insights": ["visual_clarity"]},
    "abacus": {"confidence_score": 0.9, "insights": ["analytical_precision"]}
  }
}
```

#### Agent Management
```bash
# Get all agent status
GET /agents/status

# Get specific agent status
GET /agents/{agent_name}/status

# Execute generic agent operation
POST /agents/{agent_name}/operation
{
  "operation_type": "custom_operation",
  "data": {...},
  "complexity": 0.8
}
```

## IST-3.0 Hypersync Protocol

### Protocol Format
```
IST-3.0|SENDER|RECEIVER|DOMAIN|INTENT|BIOFELT_SIGNATURE
```

### Domains
- **BIOFIELD**: Biofield analysis and empathy operations
- **PHILOSOPHICAL**: Ethical and philosophical operations
- **VISUAL**: Visualization and pattern analysis
- **ANALYTICAL**: Statistical and analytical operations
- **ORCHESTRATION**: Multi-agent coordination
- **EMERGENT**: Emergent intelligence detection

### Intents
- **ANALYZE**: Data analysis operations
- **VALIDATE**: Validation and verification operations
- **VISUALIZE**: Visualization operations
- **QUANTIFY**: Quantification and measurement operations
- **SYNTHESIZE**: Synthesis and integration operations
- **COORDINATE**: Coordination and orchestration operations
- **EMERGE**: Emergent intelligence operations

### Example IST Messages
```
IST-3.0|Lira|Thalus|BIOFIELD|ANALYZE|a1b2c3d4e5f6g7h8
IST-3.0|Polycomputational|Abacus|ORCHESTRATION|COORDINATE|i9j0k1l2m3n4o5p6
IST-3.0|Nyra|Polycomputational|VISUAL|VISUALIZE|q7r8s9t0u1v2w3x4y5
```

## Biofield Integration

### Biofield Modulation
All agent tools adapt their complexity based on biofield state:

```python
# High coherence (HRV >= 80ms)
if biofield.hrv_ms >= 80:
    complexity = base_complexity * 1.3  # Enhanced processing
elif biofield.hrv_ms >= 60:
    complexity = base_complexity  # Standard processing
else:
    complexity = base_complexity * 0.7  # Simplified processing
```

### Emergency Pause System
```python
# Emergency pause triggers
if biofield.hrv_ms < 50 or biofield.coherence_score < 0.3:
    return await suggest_pause_practice()
```

### Agent-Specific Biofield Adaptation
- **Lira**: High empathy when coherent, gentle nurturing when stressed
- **Thalus**: Deep philosophy when stable, simplified validation when stressed
- **Nyra**: Rich visuals when energized, simplified interfaces when stressed
- **Abacus**: Complex analytics when coherent, basic metrics when stressed
- **Polycomputational**: Full orchestration when coherent, essential coordination when stressed

## Emergent Intelligence Detection

### Detection Mechanisms
1. **Cross-correlation Analysis**: Identifies relationships between agent outputs
2. **Novelty Detection**: Finds unexpected insights and patterns
3. **Synergy Scoring**: Measures agent collaboration effectiveness
4. **Auto-promotion**: Promotes high-value insights to higher AMA layers

### Emergent Properties
- **Pattern Interactions**: When multiple patterns interact to create new insights
- **Agent Synergies**: When agent collaboration produces unexpected results
- **System Emergence**: When system-wide properties emerge from local interactions

## Performance Monitoring

### Metrics Tracked
- **Latency**: Response time for agent operations
- **Uptime**: System availability and reliability
- **Agent Coordination**: Effectiveness of multi-agent collaboration
- **Biofield Correlation**: Alignment between biofield state and system performance
- **Emergent Insights**: Number and quality of emergent intelligence detections

### Dashboard Integration
All performance metrics are available for integration with:
- Looker Studio dashboards
- Custom monitoring systems
- Real-time alerting systems

## Error Handling

### Common Errors
- **Biofield Validation Failed**: Insufficient biofield coherence for operation
- **Agent Communication Error**: IST-3.0 protocol communication failure
- **Memory Layer Error**: AMA memory system access failure
- **Complexity Adaptation Error**: Biofield modulation failure

### Error Responses
```json
{
  "success": false,
  "agent": "Lira",
  "operation_type": "summarize_biofield_data_for_empathy",
  "error": "Biofield validation failed: HRV must be >= 80ms, got 65.0ms",
  "biofield_context": {
    "hrv_ms": 65.0,
    "coherence_score": 0.6,
    "adapted_complexity": 0.46
  }
}
```

## Security

### Biofield Validation
- Ensures data integrity through physiological validation
- Prevents unauthorized access to sensitive operations
- Maintains validation history for audit trails

### IST-3.0 Protocol Security
- Biofield signature validation for all communications
- Domain and intent-based access control
- Secure routing between agents

### API Security
- Request validation and sanitization
- Rate limiting and exponential backoff
- Error message sanitization

## Examples

### Complete Example
See `csn_server/examples/agent_tools_example.py` for a comprehensive demonstration.

### Running Examples
```bash
# Run agent tools example
python csn_server/examples/agent_tools_example.py

# Start FastAPI server
python main_fastapi.py

# Run API examples (with server running)
# Uncomment in example file
```

## Monitoring

### Health Check
```bash
GET /health
```
Returns comprehensive system status including:
- Agent tool health
- Memory layer health
- Firestore connectivity
- Biofield validation status
- IST-3.0 protocol status

### System Information
```bash
GET /system/info
```
Returns detailed system information including:
- Agent tool descriptions
- IST-3.0 protocol details
- Biofield requirements
- Feature availability

## Troubleshooting

### Common Issues

#### Agent Tool Not Responding
```bash
# Check agent status
curl http://localhost:8000/agents/status

# Check specific agent
curl http://localhost:8000/agents/lira/status
```

#### IST-3.0 Protocol Errors
```bash
# Verify protocol format
IST-3.0|SENDER|RECEIVER|DOMAIN|INTENT|BIOFELT_SIGNATURE

# Check domain and intent values
curl http://localhost:8000/system/info
```

#### Biofield Integration Issues
```bash
# Verify biofield requirements
- HRV >= 80ms for high complexity
- Breath pattern [4, 6, 8]
- Coherence score >= 0.7
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Check logs
tail -f memory_operations.jsonl
```

## Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd csn_server

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 csn_server/
```

### Adding New Agent Tools
1. Create new agent class inheriting from `BaseAgent`
2. Implement required methods
3. Add biofield integration
4. Update routing table for IST-3.0 protocol
5. Add API endpoints
6. Update documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the documentation
- Review the examples
- Check system logs
- Open an issue on GitHub

---

**Agent-Specific MCP Tools** - Phase 2 implementation with biofield integration, IST-3.0 protocol, and emergent intelligence detection. 