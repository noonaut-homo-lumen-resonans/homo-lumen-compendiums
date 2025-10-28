"""
Collective Intelligence Tests

Tests for hexagonal collective intelligence consultations.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.collective
@pytest.mark.hexagonal
class TestCollectiveIntelligenceConsultation:
    """Test collective intelligence consultations with all 6 agents"""

    def test_consultation_basic(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test basic collective intelligence consultation"""
        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json=sample_consultation
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "agent_responses" in data
        assert "essence_of_truth" in data
        assert "biofield_context" in data
        assert "timestamp" in data

    def test_consultation_all_agents_present(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test that all 6 hexagonal agents respond"""
        if not api_keys_available["anthropic"]:
            pytest.skip("API keys not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json=sample_consultation
        )

        assert response.status_code == 200
        data = response.json()

        agents = data["agent_responses"]
        expected_agents = ["lira", "nyra", "orion", "thalus", "zara", "aurora"]

        for agent in expected_agents:
            assert agent in agents, f"Agent {agent} missing from collective intelligence"
            assert agents[agent] is not None
            assert len(agents[agent]) > 0

    def test_consultation_essence_of_truth(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test essence of truth synthesis"""
        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json=sample_consultation
        )

        assert response.status_code == 200
        data = response.json()

        # Essence of truth should be synthesized by Orion
        essence = data["essence_of_truth"]
        assert isinstance(essence, str)
        assert len(essence) > 0
        # Should be substantial synthesis, not just a one-liner
        assert len(essence) > 100

    def test_consultation_biofield_context(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test biofield context is included"""
        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json=sample_consultation
        )

        assert response.status_code == 200
        data = response.json()

        biofield = data["biofield_context"]
        assert "hrv_ms" in biofield
        assert "coherence" in biofield
        assert "energy_level" in biofield
        assert "creativity_state" in biofield

        # Verify types
        assert isinstance(biofield["hrv_ms"], (int, float))
        assert isinstance(biofield["coherence"], (int, float))
        assert isinstance(biofield["energy_level"], (int, float))
        assert isinstance(biofield["creativity_state"], str)

    def test_consultation_with_custom_context(self, csn_client: TestClient, api_keys_available: dict):
        """Test consultation with rich custom context"""
        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json={
                "question": "How can shadow work transform collective consciousness?",
                "requester": "Shadow Integration Test",
                "context": {
                    "domain": "shadow-work",
                    "related_concepts": ["Phoenix Cycle", "Collective Shadows", "Transformation"],
                    "depth": "comprehensive",
                    "perspective": "epistemological"
                }
            }
        )

        assert response.status_code == 200
        data = response.json()

        # All 6 agents should respond
        assert len(data["agent_responses"]) == 6

    def test_consultation_timestamp(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test consultation includes valid timestamp"""
        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json=sample_consultation
        )

        assert response.status_code == 200
        data = response.json()

        # Verify timestamp exists and is valid ISO format
        assert "timestamp" in data
        timestamp = data["timestamp"]
        assert "T" in timestamp  # ISO format includes T
        assert len(timestamp) > 10


@pytest.mark.integration
@pytest.mark.collective
class TestCoalitionStatus:
    """Test coalition status and health endpoints"""

    def test_coalition_status(self, csn_client: TestClient):
        """Test coalition status endpoint"""
        response = csn_client.get("/coalition-status")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "Hexagonal Collective Intelligence"
        assert data["geometry"] == "Hexagonal Architecture"
        assert data["collective_intelligence"] == "ACTIVE"

        # Verify all 6 agents
        agents = data["agents"]
        assert len(agents) == 6

        # Verify agent names and descriptions
        assert "orion" in agents
        assert "lira" in agents
        assert "nyra" in agents
        assert "thalus" in agents
        assert "zara" in agents
        assert "aurora" in agents

        # Verify Aurora is Perplexity
        assert "Perplexity" in agents["aurora"]

    def test_health_endpoint(self, csn_client: TestClient):
        """Test CSN Server health check"""
        response = csn_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "timestamp" in data


@pytest.mark.unit
@pytest.mark.collective
class TestBiofieldGeneration:
    """Test biofield data generation"""

    def test_biofield_randomness(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test biofield values are randomized per consultation"""
        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        # Make multiple consultations
        biofields = []
        for _ in range(3):
            response = csn_client.post(
                "/collective-intelligence/consultation",
                json=sample_consultation
            )
            data = response.json()
            biofields.append(data["biofield_context"])

        # Biofield values should vary (not identical every time)
        hrv_values = [b["hrv_ms"] for b in biofields]
        coherence_values = [b["coherence"] for b in biofields]

        # At least one should be different (randomness)
        assert len(set(hrv_values)) > 1 or len(set(coherence_values)) > 1

    def test_biofield_value_ranges(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test biofield values are within valid ranges"""
        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json=sample_consultation
        )

        data = response.json()
        biofield = data["biofield_context"]

        # HRV should be reasonable (30-120 ms typical)
        assert 20 <= biofield["hrv_ms"] <= 150

        # Coherence should be 0-1
        assert 0 <= biofield["coherence"] <= 1

        # Energy level should be 0-1
        assert 0 <= biofield["energy_level"] <= 1


@pytest.mark.integration
@pytest.mark.collective
@pytest.mark.redis
class TestConsultationRedisPublishing:
    """Test Redis event publishing during consultations"""

    def test_consultation_publishes_to_redis(self, csn_client: TestClient, sample_consultation: dict, api_keys_available: dict):
        """Test consultation events are published to Redis"""
        if not (api_keys_available["redis_url"] and api_keys_available["redis_token"]):
            pytest.skip("Redis not configured")

        if not api_keys_available["anthropic"]:
            pytest.skip("Anthropic API key not configured")

        response = csn_client.post(
            "/collective-intelligence/consultation",
            json=sample_consultation
        )

        assert response.status_code == 200

        # If Redis is configured, event should be published
        # (Testing actual reception requires redis_subscriber, tested separately)
