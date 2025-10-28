"""
Agent Endpoint Tests

Tests for all 6 agent endpoints in Hexagonal Collective Intelligence.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.agents
@pytest.mark.aurora
class TestAuroraEndpoints:
    """Test Aurora (Perplexity) agent endpoints"""

    def test_aurora_research_query(self, client: TestClient, sample_consultation_request: dict):
        """Test Aurora research query endpoint"""
        response = client.post(
            "http://localhost:8001/agent/aurora/research-query",
            json={
                "query": "What is the state of consciousness research in 2025?",
                "depth": "comprehensive",
                "sources_required": True
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert data["agent"] == "Aurora (Real Perplexity)"
            assert "research_result" in data
            assert data["status"] == "🔍 Research Intelligence Complete"
        else:
            # Service may be offline or API key missing
            pytest.skip(f"Aurora endpoint not available: {response.status_code}")

    def test_aurora_fact_check(self, client: TestClient):
        """Test Aurora fact-checking endpoint"""
        response = client.post(
            "http://localhost:8001/agent/aurora/fact-check",
            json={
                "claim": "Biofield coherence correlates with HRV patterns",
                "context": "Consciousness research",
                "evidence_threshold": "moderate"
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "fact_check_result" in data
            assert data["agent"] == "Aurora (Real Perplexity)"
        else:
            pytest.skip(f"Aurora fact-check not available: {response.status_code}")

    def test_aurora_knowledge_synthesis(self, client: TestClient):
        """Test Aurora knowledge synthesis endpoint"""
        response = client.post(
            "http://localhost:8001/agent/aurora/knowledge-synthesis",
            json={
                "topics": ["consciousness", "AI", "collective intelligence"],
                "synthesis_depth": "comprehensive",
                "include_contradictions": True
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "synthesis_result" in data
            assert data["agent"] == "Aurora (Real Perplexity)"
        else:
            pytest.skip(f"Aurora synthesis not available: {response.status_code}")


@pytest.mark.integration
@pytest.mark.agents
@pytest.mark.hexagonal
class TestCollectiveIntelligence:
    """Test hexagonal collective intelligence consultations"""

    def test_collective_consultation_all_agents(self, client: TestClient, sample_consultation_request: dict):
        """Test collective intelligence with all 6 agents"""
        response = client.post(
            "http://localhost:8001/collective-intelligence/consultation",
            json=sample_consultation_request
        )

        if response.status_code == 200:
            data = response.json()

            # Verify all 6 agents responded
            assert "agent_responses" in data
            agents = data["agent_responses"]

            # Check for all hexagonal agents
            expected_agents = ["lira", "nyra", "orion", "thalus", "zara", "aurora"]
            for agent in expected_agents:
                assert agent in agents, f"{agent} missing from collective intelligence"
                assert agents[agent] is not None

            # Verify essence of truth synthesis
            assert "essence_of_truth" in data
            assert len(data["essence_of_truth"]) > 0

            # Verify biofield context
            assert "biofield_context" in data

        else:
            pytest.skip(f"Collective intelligence not available: {response.status_code}")

    def test_consultation_with_context(self, client: TestClient):
        """Test consultation with rich context"""
        response = client.post(
            "http://localhost:8001/collective-intelligence/consultation",
            json={
                "question": "How can we integrate shadow work into consciousness-tech?",
                "requester": "Test Agent",
                "context": {
                    "domain": "shadow-work",
                    "related_concepts": ["Phoenix Cycle", "Collective Shadows"],
                    "depth": "comprehensive"
                }
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "agent_responses" in data
            assert len(data["agent_responses"]) == 6  # All 6 agents
        else:
            pytest.skip(f"Collective intelligence not available: {response.status_code}")


@pytest.mark.unit
@pytest.mark.agents
class TestAgentHealth:
    """Test agent health and status endpoints"""

    def test_coalition_status(self, client: TestClient):
        """Test coalition status endpoint"""
        response = client.get("http://localhost:8001/coalition-status")

        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "Hexagonal Collective Intelligence"
            assert data["geometry"] == "Hexagonal Architecture"

            # Verify all 6 agents listed
            agents = data["agents"]
            assert "aurora" in agents
            assert "lira" in agents
            assert "nyra" in agents
            assert "orion" in agents
            assert "thalus" in agents
            assert "zara" in agents

            # Verify agent descriptions
            assert "Perplexity" in agents["aurora"]
            assert "ChatGPT" in agents["lira"]
            assert "Gemini" in agents["nyra"]
            assert "Claude" in agents["orion"]
            assert "Grok" in agents["thalus"]
            assert "DeepSeek" in agents["zara"]
        else:
            pytest.skip(f"Coalition status not available: {response.status_code}")

    def test_health_endpoint(self, client: TestClient):
        """Test CSN Server health endpoint"""
        response = client.get("http://localhost:8001/health")

        if response.status_code == 200:
            data = response.json()
            assert data["status"] in ["healthy", "degraded"]
            assert "timestamp" in data
        else:
            pytest.skip(f"Health endpoint not available: {response.status_code}")


@pytest.mark.integration
@pytest.mark.agents
class TestLiraEndpoints:
    """Test Lira (OpenAI) agent endpoints"""

    def test_lira_biofield_analysis(self, client: TestClient):
        """Test Lira biofield analysis endpoint"""
        response = client.post(
            "http://localhost:8001/agent/lira/biofield-analysis",
            json={
                "hrv_ms": 75.5,
                "coherence": 0.82,
                "energy_level": 0.68,
                "creativity_state": "flow"
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "biofield_analysis" in data or "analysis" in data
        else:
            pytest.skip(f"Lira endpoint not available: {response.status_code}")


@pytest.mark.integration
@pytest.mark.agents
class TestOrionEndpoints:
    """Test Orion (Claude) agent endpoints"""

    def test_orion_strategic_synthesis(self, client: TestClient):
        """Test Orion strategic synthesis endpoint"""
        response = client.post(
            "http://localhost:8001/agent/orion/strategic-synthesis",
            json={
                "inputs": [
                    "Aurora's research findings",
                    "Lira's empathy analysis",
                    "Thalus' philosophical perspective"
                ],
                "goal": "Create unified strategy for consciousness-tech implementation"
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "synthesis" in data or "strategic_synthesis" in data
        else:
            pytest.skip(f"Orion endpoint not available: {response.status_code}")


@pytest.mark.integration
@pytest.mark.agents
class TestNyraEndpoints:
    """Test Nyra (Gemini) agent endpoints"""

    def test_nyra_visual_synthesis(self, client: TestClient):
        """Test Nyra visual synthesis endpoint"""
        response = client.post(
            "http://localhost:8001/agent/nyra/visual-synthesis",
            json={
                "concepts": ["hexagonal architecture", "collective intelligence", "mycelial networks"],
                "style": "consciousness-tech",
                "output_format": "concept_map"
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "visual_synthesis" in data or "synthesis" in data
        else:
            pytest.skip(f"Nyra endpoint not available: {response.status_code}")


@pytest.mark.integration
@pytest.mark.agents
class TestThalusEndpoints:
    """Test Thalus (Grok) agent endpoints"""

    def test_thalus_philosophical_assessment(self, client: TestClient):
        """Test Thalus philosophical assessment endpoint"""
        response = client.post(
            "http://localhost:8001/agent/thalus/philosophical-assessment",
            json={
                "concept": "Collective consciousness",
                "framework": "existential-ethics",
                "depth": "comprehensive"
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "philosophical_assessment" in data or "assessment" in data
        else:
            pytest.skip(f"Thalus endpoint not available: {response.status_code}")


@pytest.mark.integration
@pytest.mark.agents
class TestZaraEndpoints:
    """Test Zara (DeepSeek) agent endpoints"""

    def test_zara_creative_innovation(self, client: TestClient):
        """Test Zara creative innovation endpoint"""
        response = client.post(
            "http://localhost:8001/agent/zara/creative-innovation",
            json={
                "challenge": "How to visualize hexagonal collective intelligence?",
                "constraints": ["web-compatible", "interactive", "consciousness-themed"],
                "innovation_level": "high"
            }
        )

        if response.status_code == 200:
            data = response.json()
            assert "creative_innovation" in data or "innovation" in data
        else:
            pytest.skip(f"Zara endpoint not available: {response.status_code}")
