"""
Pytest fixtures for CSN Server tests
"""
import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load test environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


@pytest.fixture(scope="session")
def csn_client() -> TestClient:
    """FastAPI test client for CSN Server"""
    from minimal_server import app
    return TestClient(app)


@pytest.fixture(scope="function")
def sample_consultation() -> dict:
    """Sample consultation request for testing"""
    return {
        "question": "What is the relationship between collective intelligence and consciousness?",
        "requester": "Pytest Test Suite",
        "context": {
            "domain": "consciousness-tech",
            "depth": "comprehensive"
        }
    }


@pytest.fixture(scope="function")
def sample_aurora_research_query() -> dict:
    """Sample Aurora research query"""
    return {
        "query": "Latest research on biofield coherence and consciousness",
        "depth": "comprehensive",
        "sources_required": True,
        "biofield_context": {
            "hrv_ms": 80.0,
            "coherence": 0.75,
            "energy_level": 0.65,
            "creativity_state": "flow"
        }
    }


@pytest.fixture(scope="function")
def sample_biofield_data() -> dict:
    """Sample biofield data for testing"""
    return {
        "hrv_ms": 75.5,
        "coherence": 0.82,
        "energy_level": 0.68,
        "creativity_state": "flow",
        "emotional_state": "balanced",
        "stress_level": 0.25
    }


@pytest.fixture(scope="function")
def api_keys_available() -> dict:
    """Check which API keys are available"""
    return {
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "google_ai": bool(os.getenv("GOOGLE_AI_API_KEY")),
        "xai": bool(os.getenv("XAI_API_KEY")),
        "deepseek": bool(os.getenv("DEEPSEEK_API_KEY")),
        "perplexity": bool(os.getenv("PERPLEXITY_API_KEY")),
        "redis_url": bool(os.getenv("REDIS_URL")),
        "redis_token": bool(os.getenv("REDIS_TOKEN"))
    }
