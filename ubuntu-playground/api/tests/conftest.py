"""
Pytest fixtures for Ubuntu Playground API tests
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load test environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env.test")


@pytest.fixture(scope="session")
def test_workspace() -> Generator[Path, None, None]:
    """Create temporary workspace for testing"""
    temp_dir = Path(tempfile.mkdtemp(prefix="ubuntu_playground_test_"))

    # Create agent directories
    agents = ["manus", "code", "lira", "orion", "abacus", "nyra", "thalus", "aurora", "thalamus", "scribe", "zara", "shared"]
    for agent in agents:
        (temp_dir / agent).mkdir(parents=True, exist_ok=True)

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def test_database() -> Generator[Path, None, None]:
    """Create temporary SQLite database for testing"""
    temp_db = Path(tempfile.mktemp(suffix=".db", prefix="ubuntu_test_"))

    yield temp_db

    # Cleanup
    if temp_db.exists():
        temp_db.unlink()


@pytest.fixture(scope="function")
def client(test_workspace: Path, test_database: Path) -> TestClient:
    """FastAPI test client with mocked workspace"""
    # Mock environment variables
    os.environ["WORKSPACE_ROOT"] = str(test_workspace)
    os.environ["DATABASE_PATH"] = str(test_database)
    os.environ["CSN_SERVER_URL"] = "http://localhost:8001"

    # Import app AFTER setting environment variables
    # Use importlib because main.local.py has a dot in the name
    import importlib.util
    spec = importlib.util.spec_from_file_location("main_local", Path(__file__).parent.parent / "main.local.py")
    main_local = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_local)
    app = main_local.app

    return TestClient(app)


@pytest.fixture(scope="function")
def aurora_api_key() -> str:
    """Aurora agent API key for testing"""
    return "aurora-test-key"


@pytest.fixture(scope="function")
def lira_api_key() -> str:
    """Lira agent API key for testing"""
    return "lira-test-key"


@pytest.fixture(scope="function")
def sample_file_content() -> str:
    """Sample file content for testing"""
    return """# Test Document

This is a test document for Ubuntu Playground workspace testing.

## Content
- Test line 1
- Test line 2
- Test line 3

## Metadata
Created by: Test Agent
Purpose: Integration testing
"""


@pytest.fixture(scope="function")
def sample_consultation_request() -> dict:
    """Sample collective intelligence consultation request"""
    return {
        "question": "What is the best approach to implement consciousness-tech?",
        "requester": "Test User",
        "context": {
            "domain": "consciousness-tech",
            "depth": "comprehensive"
        }
    }


@pytest.fixture(scope="function")
def mock_redis_enabled() -> bool:
    """Check if Redis is available for testing"""
    redis_url = os.getenv("REDIS_URL")
    redis_token = os.getenv("REDIS_TOKEN")
    return bool(redis_url and redis_token)
