# AMA Four-Layer Memory Architecture

## Overview

The AMA (Autonomous Memory Architecture) Four-Layer Memory System is a sophisticated memory management solution designed for CSN Server. It implements a hierarchical memory structure with biofield validation, Firestore integration, and comprehensive logging for transformative reversibility.

## Architecture

### Memory Layers

#### 1. Reactive Memory Layer (`memory_reactive`)
- **Purpose**: High-frequency writes with TTL policies
- **Characteristics**: 
  - Biofield-timestamps for validation
  - Priority-based expiration (1-10 scale)
  - Frequency tracking
  - TTL policies: High (1h), Medium (6h), Low (24h)
- **Use Cases**: User interactions, real-time events, session data

#### 2. Strategic Memory Layer (`memory_strategic`)
- **Purpose**: Pattern analysis and agent-synthesis aggregation
- **Characteristics**:
  - Pattern recognition and storage
  - Agent synthesis data aggregation
  - Confidence scoring (0-1 scale)
  - Cross-referencing capabilities
- **Use Cases**: Behavioral analysis, pattern recognition, agent collaboration

#### 3. Meta Memory Layer (`memory_meta`)
- **Purpose**: Deep insights and cross-platform correlations
- **Characteristics**:
  - Insight generation and storage
  - Cross-platform correlation mapping
  - Complexity assessment (0-1 scale)
  - Multi-dimensional data relationships
- **Use Cases**: System insights, cross-platform analysis, complex correlations

#### 4. Evolutionary Memory Layer (`memory_evolutionary`)
- **Purpose**: Read-only core principles with biofield validation
- **Characteristics**:
  - Core principles storage
  - **Required biofield validation**
  - Validation history tracking
  - Immutable once validated
- **Use Cases**: System principles, architectural decisions, validated knowledge

## Biofield Validation

### Requirements
- **Heart Rate Variability (HRV)**: ≥ 80ms
- **Breath Pattern**: Exact sequence [4, 6, 8]
- **Coherence Score**: ≥ 0.7 (0-1 scale)

### Validation Process
1. **HRV Check**: Measures heart rate variability in milliseconds
2. **Breath Pattern**: Confirms 4-6-8 breathing pattern
3. **Coherence**: Calculates biofield coherence score
4. **Overall Score**: Weighted average of all metrics

### Usage
- **Optional** for Reactive, Strategic, and Meta layers
- **Required** for Evolutionary layer
- Real-time validation with detailed scoring

## Installation

### Prerequisites
```bash
# Python 3.8+
python --version

# Google Cloud SDK (for Firestore)
gcloud auth application-default login

# Required packages
pip install -r requirements.txt
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

### Firestore Setup
```bash
# Create Firestore database
gcloud firestore databases create --project=your-project-id

# Set up collections (automatically created):
# - ama_memory_reactive
# - ama_memory_strategic  
# - ama_memory_meta
# - ama_memory_evolutionary
```

## Usage

### Basic Usage

```python
from csn_server.routers.ama_memory_layers import (
    AMAMemorySystem, BiofieldMetrics, MemoryLayer
)

# Initialize system
memory_system = AMAMemorySystem("your-project-id")

# Create biofield metrics
biofield = BiofieldMetrics(
    hrv_ms=95.0,
    breath_pattern=[4, 6, 8],
    coherence_score=0.85
)

# Create entries in different layers
reactive_id = await memory_system.create_reactive_entry(
    content={"event": "user_click"},
    priority=8,
    biofield_metrics=biofield
)

strategic_id = await memory_system.create_strategic_entry(
    content={"analysis": "user_behavior"},
    patterns=["morning_peak", "visual_preference"],
    agent_synthesis={"confidence": 0.87}
)

meta_id = await memory_system.create_meta_entry(
    content={"insight": "cross_platform"},
    insights=["Mobile users prefer quick actions"],
    correlations={"platform": ["web", "mobile"]}
)

evolutionary_id = await memory_system.create_evolutionary_entry(
    content={"principle": "user_centric"},
    core_principles=["Accessibility first"],
    biofield_metrics=biofield  # Required
)
```

### API Endpoints

#### Biofield Validation
```bash
POST /ama-memory/validate-biofield
{
  "hrv_ms": 95.0,
  "breath_pattern": [4, 6, 8],
  "coherence_score": 0.85
}
```

#### Reactive Memory
```bash
# Create entry
POST /ama-memory/reactive/create
{
  "content": {"event": "user_interaction"},
  "priority": 8,
  "biofield_metrics": {...}
}

# Get entry
GET /ama-memory/reactive/{entry_id}

# Update frequency
POST /ama-memory/reactive/{entry_id}/update-frequency

# Query entries
POST /ama-memory/reactive/query
{
  "filters": [{"field": "priority", "op": ">=", "value": 5}],
  "limit": 10
}
```

#### Strategic Memory
```bash
# Create entry
POST /ama-memory/strategic/create
{
  "content": {"analysis": "pattern"},
  "patterns": ["pattern1", "pattern2"],
  "agent_synthesis": {"confidence": 0.87}
}

# Get entry
GET /ama-memory/strategic/{entry_id}

# Query entries
POST /ama-memory/strategic/query
```

#### Meta Memory
```bash
# Create entry
POST /ama-memory/meta/create
{
  "content": {"insight": "correlation"},
  "insights": ["insight1", "insight2"],
  "correlations": {"group1": ["item1", "item2"]}
}

# Get entry
GET /ama-memory/meta/{entry_id}

# Query entries
POST /ama-memory/meta/query
```

#### Evolutionary Memory
```bash
# Create entry (requires biofield validation)
POST /ama-memory/evolutionary/create
{
  "content": {"principle": "core"},
  "core_principles": ["principle1", "principle2"],
  "biofield_metrics": {...}  # Required
}

# Get entry
GET /ama-memory/evolutionary/{entry_id}

# Re-validate entry
POST /ama-memory/evolutionary/{entry_id}/validate
{
  "hrv_ms": 95.0,
  "breath_pattern": [4, 6, 8],
  "coherence_score": 0.85
}

# Query entries
POST /ama-memory/evolutionary/query
```

#### System Management
```bash
# System status
GET /ama-memory/status

# Delete entry
DELETE /ama-memory/{layer}/{entry_id}

# Cleanup expired entries
POST /ama-memory/cleanup/expired-reactive
```

### Query Filters

```python
# Example filters for querying
filters = [
    {"field": "priority", "op": ">=", "value": 5},
    {"field": "confidence_score", "op": ">=", "value": 0.8},
    {"field": "created_at", "op": ">=", "value": "2024-01-01T00:00:00Z"}
]

# Supported operations: ==, !=, >, >=, <, <=, in, not-in
```

## Logging

### JSONL Logging
All operations are logged to `memory_operations.jsonl` with transformative reversibility:

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "operation": "create",
  "layer": "memory_reactive",
  "entry_id": "reactive_1704110400000",
  "data": {...},
  "biofield_metrics": {...},
  "validation_result": {...},
  "session_id": "abc12345",
  "transformative_reversibility": {
    "can_reverse": true,
    "reverse_operation": "delete",
    "required_data": {"entry_id": "reactive_1704110400000"}
  }
}
```

### Structured Logging
Uses `structlog` for comprehensive logging with:
- Request tracking
- Performance metrics
- Error handling
- Biofield validation results

## Configuration

### Settings
```python
# csn_server/config.py
class Settings(BaseSettings):
    google_cloud_project_id: str
    log_level: str = "INFO"
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
```

### Firestore Collections
- `ama_memory_reactive`: Reactive memory entries
- `ama_memory_strategic`: Strategic memory entries  
- `ama_memory_meta`: Meta memory entries
- `ama_memory_evolutionary`: Evolutionary memory entries

## Monitoring

### Health Check
```bash
GET /health
```
Returns comprehensive system status including:
- Memory layer health
- Firestore connectivity
- Biofield validation status
- Overall system health

### System Information
```bash
GET /system/info
```
Returns detailed system information including:
- Feature availability
- Memory layer descriptions
- Biofield requirements
- Configuration details

## Examples

### Complete Example
See `csn_server/examples/ama_memory_example.py` for a comprehensive demonstration.

### Running Examples
```bash
# Run memory system example
python csn_server/examples/ama_memory_example.py

# Start FastAPI server
python main_fastapi.py

# Run API examples (with server running)
# Uncomment in example file
```

## Error Handling

### Common Errors
- **Biofield Validation Failed**: HRV < 80ms, wrong breath pattern, or low coherence
- **Firestore Connection Error**: Check credentials and project ID
- **Invalid Layer**: Use correct layer names (reactive, strategic, meta, evolutionary)
- **Missing Required Fields**: Evolutionary layer requires biofield metrics

### Error Responses
```json
{
  "error": "Biofield validation failed",
  "detail": "HRV must be >= 80ms, got 65.0ms",
  "status_code": 400
}
```

## Performance

### Optimization Features
- **Batch Operations**: Efficient batch processing for multiple entries
- **Rate Limiting**: Built-in rate limiting with exponential backoff
- **TTL Policies**: Automatic cleanup of expired reactive entries
- **Indexing**: Firestore automatic indexing for query performance

### Best Practices
1. **Use appropriate layers** for different data types
2. **Validate biofield metrics** before evolutionary operations
3. **Monitor TTL policies** for reactive entries
4. **Use filters** for efficient querying
5. **Check system status** regularly

## Security

### Biofield Validation
- Ensures data integrity through physiological validation
- Prevents unauthorized access to evolutionary layer
- Maintains validation history for audit trails

### Firestore Security
- Uses Google Cloud IAM for access control
- Service account authentication
- Collection-level security rules

### API Security
- CORS configuration
- Request validation
- Error message sanitization

## Troubleshooting

### Common Issues

#### Biofield Validation Failing
```bash
# Check requirements
- HRV >= 80ms
- Breath pattern exactly [4, 6, 8]  
- Coherence score >= 0.7
```

#### Firestore Connection Issues
```bash
# Verify credentials
gcloud auth application-default login

# Check project ID
echo $GOOGLE_CLOUD_PROJECT_ID

# Test connection
gcloud firestore collections list
```

#### Memory Layer Not Working
```bash
# Check system status
curl http://localhost:8000/health

# Verify layer configuration
curl http://localhost:8000/system/info
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

### Adding New Features
1. Follow the existing layer pattern
2. Add comprehensive logging
3. Include biofield validation where appropriate
4. Update documentation
5. Add tests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the documentation
- Review the examples
- Check system logs
- Open an issue on GitHub

---

**AMA Four-Layer Memory Architecture** - Transforming memory management with biofield validation and hierarchical intelligence. 