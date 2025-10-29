# Testing Guide - Homo Lumen Collective Intelligence System

## Overview

This guide covers the pytest testing infrastructure for the Homo Lumen Collective Intelligence System, including workspace integration tests, agent endpoint tests, and Redis pub/sub tests.

**Test Coverage:**
- Ubuntu Playground API (workspace operations, agent permissions)
- CSN Server (collective intelligence consultations, Aurora agent)
- Redis pub/sub event streaming
- All 6 hexagonal agents (Lira, Nyra, Orion, Thalus, Zara, Aurora)

---

## Quick Start

### Installation

```bash
# Install test dependencies
cd "c:\Users\onigo\NAV LOSEN\homo-lumen-compendiums"
pip install -r requirements-test.txt
```

### Run Tests

```bash
# Run all unit tests (fast, no external dependencies)
pytest -m unit -v

# Run all integration tests (requires running services)
pytest -m integration -v

# Run specific test files
pytest ubuntu-playground/api/tests/test_workspace.py -v
pytest ama-backend/tests/test_aurora.py -v

# Run with coverage report
pytest --cov --cov-report=html

# Run specific markers
pytest -m aurora -v  # Aurora agent tests only
pytest -m hexagonal -v  # Hexagonal collective intelligence tests
pytest -m redis -v  # Redis pub/sub tests
```

---

## Test Structure

```
homo-lumen-compendiums/
├── pytest.ini                          # Pytest configuration
├── requirements-test.txt               # Test dependencies
├── test-reports/                       # Generated test reports
│   ├── coverage/                       # HTML coverage reports
│   ├── coverage.xml                    # XML coverage data
│   └── junit.xml                       # JUnit test results
├── ubuntu-playground/api/tests/
│   ├── conftest.py                     # Fixtures for Ubuntu Playground
│   ├── test_workspace.py               # Workspace file operations tests
│   ├── test_agents.py                  # Agent endpoint tests
│   └── test_redis_subscriber.py        # Redis subscriber tests
└── ama-backend/tests/
    ├── conftest.py                     # Fixtures for CSN Server
    ├── test_collective_intelligence.py # Collective intelligence tests
    └── test_aurora.py                  # Aurora (Perplexity) agent tests
```

---

## Test Categories

### Unit Tests (Fast)
Tests that don't require external services:
- Biofield generation logic
- Event storage validation
- Configuration validation
- Data structure tests

**Run:**
```bash
pytest -m unit
```

### Integration Tests
Tests that require running services:
- Workspace file operations (requires Ubuntu Playground)
- Agent endpoints (requires CSN Server)
- Collective intelligence consultations (requires all agents)
- Redis pub/sub (requires Upstash Redis)

**Run:**
```bash
# Start services first
cd ama-backend
python -m uvicorn minimal_server:app --host 0.0.0.0 --port 8001 --reload

# In another terminal
cd ubuntu-playground/api
python -m uvicorn main.local:app --host 0.0.0.0 --port 8002 --reload

# Run integration tests
pytest -m integration
```

---

## Test Markers

Use markers to run specific test subsets:

| Marker | Description | Example |
|--------|-------------|---------|
| `unit` | Fast tests, no external dependencies | `pytest -m unit` |
| `integration` | Requires running services | `pytest -m integration` |
| `slow` | Tests that take >5 seconds | `pytest -m slow` |
| `workspace` | Workspace file operations | `pytest -m workspace` |
| `agents` | Agent endpoint tests | `pytest -m agents` |
| `redis` | Redis pub/sub tests | `pytest -m redis` |
| `collective` | Collective intelligence | `pytest -m collective` |
| `aurora` | Aurora agent specific tests | `pytest -m aurora` |
| `hexagonal` | Hexagonal architecture tests | `pytest -m hexagonal` |

**Examples:**
```bash
# Only Aurora tests
pytest -m aurora

# Integration tests excluding slow tests
pytest -m "integration and not slow"

# All workspace and agent tests
pytest -m "workspace or agents"
```

---

## Test Coverage

### Ubuntu Playground API Tests

**test_workspace.py** (12 tests)
- `TestWorkspaceFileOperations` (5 tests)
  - Create file in workspace
  - Read file from workspace
  - Update existing file
  - Delete file
  - List files in directory

- `TestAgentPermissions` (5 tests)
  - Agent can write to own workspace
  - Agent can write to shared workspace
  - Agent cannot write to other agent's workspace
  - Agent can read all workspaces (read:all permission)
  - Invalid API key rejected

- `TestWorkspaceEvents` (2 tests)
  - File operations logged to SQLite
  - Events have valid timestamps

**test_agents.py** (20+ tests)
- Aurora endpoints (research-query, fact-check, knowledge-synthesis, daily-insights)
- Collective intelligence consultations (all 6 agents)
- Coalition status and health checks
- Individual agent endpoints (Lira, Nyra, Orion, Thalus, Zara)

**test_redis_subscriber.py** (10 tests)
- Redis subscriber initialization
- Channel subscriptions
- Event logging to SQLite
- End-to-end event flow
- Event metadata validation

### CSN Server Tests

**test_collective_intelligence.py** (15+ tests)
- `TestCollectiveIntelligenceConsultation`
  - Basic consultation flow
  - All 6 agents respond
  - Essence of truth synthesis
  - Biofield context generation
  - Custom context handling

- `TestCoalitionStatus`
  - Coalition status endpoint
  - Health check endpoint

- `TestBiofieldGeneration`
  - Biofield randomness
  - Value ranges validation

- `TestConsultationRedisPublishing`
  - Redis event publishing

**test_aurora.py** (15+ tests)
- `TestAuroraResearchQuery`
  - Basic research query
  - Research with sources
  - Biofield context integration
  - Fallback mode

- `TestAuroraFactCheck`
  - Fact-checking with evidence levels
  - Different threshold levels

- `TestAuroraKnowledgeSynthesis`
  - Multi-topic synthesis
  - Contradiction handling

- `TestAuroraDailyInsights`
  - Insights generation
  - Priority levels

---

## Fixtures

### Ubuntu Playground Fixtures (`ubuntu-playground/api/tests/conftest.py`)

```python
@pytest.fixture
def test_workspace() -> Path:
    """Create temporary workspace directory with agent folders"""
    # Returns: /tmp/ubuntu_playground_test_xxxxx/

@pytest.fixture
def test_database() -> Path:
    """Create temporary SQLite database for testing"""
    # Returns: /tmp/ubuntu_test_xxxxx.db

@pytest.fixture
def client() -> TestClient:
    """FastAPI test client with mocked workspace"""
    # Returns: TestClient(app)

@pytest.fixture
def aurora_api_key() -> str:
    """Aurora agent API key"""
    # Returns: "aurora-test-key"

@pytest.fixture
def sample_file_content() -> str:
    """Sample file content for testing"""
    # Returns: Markdown test document

@pytest.fixture
def mock_redis_enabled() -> bool:
    """Check if Redis is configured"""
    # Returns: True if REDIS_URL and REDIS_TOKEN set
```

### CSN Server Fixtures (`ama-backend/tests/conftest.py`)

```python
@pytest.fixture
def csn_client() -> TestClient:
    """FastAPI test client for CSN Server"""
    # Returns: TestClient(app)

@pytest.fixture
def sample_consultation() -> dict:
    """Sample consultation request"""
    # Returns: {question, requester, context}

@pytest.fixture
def sample_aurora_research_query() -> dict:
    """Sample Aurora research query"""
    # Returns: {query, depth, sources_required, biofield_context}

@pytest.fixture
def sample_biofield_data() -> dict:
    """Sample biofield data"""
    # Returns: {hrv_ms, coherence, energy_level, creativity_state}

@pytest.fixture
def api_keys_available() -> dict:
    """Check which API keys are configured"""
    # Returns: {anthropic, openai, google_ai, xai, deepseek, perplexity, redis_url, redis_token}
```

---

## Running Tests in CI/CD

### GitHub Actions Example

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt

      - name: Run unit tests
        run: pytest -m unit --cov --junit-xml=test-reports/junit.xml

      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          files: ./test-reports/coverage.xml
```

---

## Coverage Reports

### Generate HTML Coverage Report

```bash
pytest --cov --cov-report=html
# Open test-reports/coverage/index.html in browser
```

### Generate Terminal Coverage Report

```bash
pytest --cov --cov-report=term-missing
```

### Coverage Goals

- **Unit Tests:** >80% coverage
- **Integration Tests:** >60% coverage
- **Overall:** >70% coverage

**Current Coverage:**
- Ubuntu Playground API: TBD (requires service running)
- CSN Server: TBD (requires API keys)
- Redis Infrastructure: TBD (requires Upstash setup)

---

## Troubleshooting

### ImportError: No module named 'main.local'

**Problem:** Python can't import `main.local.py` because of the dot in filename.

**Solution:** The conftest.py fixture uses `importlib` to handle this:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("main_local", Path(__file__).parent.parent / "main.local.py")
main_local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_local)
app = main_local.app
```

### Tests Require Running Services

**Problem:** Integration tests fail with connection errors.

**Solution:** Start services before running tests:

```bash
# Terminal 1: CSN Server
cd ama-backend
python -m uvicorn minimal_server:app --host 0.0.0.0 --port 8001

# Terminal 2: Ubuntu Playground
cd ubuntu-playground/api
python -m uvicorn main.local:app --host 0.0.0.0 --port 8002

# Terminal 3: Run tests
pytest -m integration
```

### API Keys Not Configured

**Problem:** Tests skip because API keys are missing.

**Solution:** Add API keys to `ama-backend/.env`:

```bash
PERPLEXITY_API_KEY=pplx-your-key-here
OPENAI_API_KEY=sk-proj-your-key-here
GOOGLE_AI_API_KEY=AIza-your-key-here
# ... etc
```

### Redis Tests Failing

**Problem:** Redis tests fail because Upstash not configured.

**Solution:** Follow `docs/UPSTASH_REDIS_SETUP.md` to set up Redis, then add to `.env`:

```bash
REDIS_URL=https://eu1-your-database.upstash.io
REDIS_TOKEN=your-token-here
```

---

## Writing New Tests

### Example: New Workspace Test

```python
@pytest.mark.unit
@pytest.mark.workspace
def test_my_new_feature(client: TestClient, aurora_api_key: str):
    """Test description"""
    response = client.post(
        "/workspace/aurora/test-file.md",
        json={"content": "Test content"},
        headers={"X-Agent-API-Key": aurora_api_key}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "created"
```

### Example: New Agent Test

```python
@pytest.mark.integration
@pytest.mark.agents
@pytest.mark.aurora
def test_aurora_new_endpoint(csn_client: TestClient, api_keys_available: dict):
    """Test Aurora new endpoint"""
    if not api_keys_available["perplexity"]:
        pytest.skip("Perplexity API key not configured")

    response = csn_client.post(
        "/agent/aurora/new-endpoint",
        json={"param": "value"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
```

---

## Best Practices

1. **Use Markers:** Always mark tests with appropriate markers (unit, integration, agent name)
2. **Skip Gracefully:** Use `pytest.skip()` when API keys or services are unavailable
3. **Isolate Tests:** Each test should be independent (no shared state)
4. **Clean Up:** Fixtures automatically clean up temp files/databases
5. **Descriptive Names:** Test names should clearly describe what is being tested
6. **Fast Unit Tests:** Unit tests should run in <1 second each
7. **Comprehensive Assertions:** Check all relevant response fields
8. **Error Cases:** Test both success and failure scenarios

---

## Performance

**Expected Test Execution Times:**
- Unit tests: <30 seconds total
- Integration tests: 2-5 minutes (depends on API response times)
- Full suite: 3-6 minutes

**Optimization Tips:**
- Run unit tests during development (`pytest -m unit`)
- Run integration tests before commits
- Use pytest-xdist for parallel execution: `pytest -n auto`

---

## Related Documentation

- [API Keys Guide](../API_KEYS_GUIDE.md) - Configure API keys for testing
- [Upstash Redis Setup](./UPSTASH_REDIS_SETUP.md) - Set up Redis for event streaming tests
- [Ubuntu Playground API](../ubuntu-playground/api/README.md) - API documentation
- [CSN Server](../ama-backend/README.md) - CSN Server documentation

---

**Documentation Version:** 1.0
**Last Updated:** 28. oktober 2025
**Status:** ✅ Testing Infrastructure Complete
