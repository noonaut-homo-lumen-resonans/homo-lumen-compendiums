"""
Aurora Agent Tests

Tests for Aurora (Perplexity) research intelligence endpoints.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.aurora
class TestAuroraResearchQuery:
    """Test Aurora research query endpoint"""

    def test_research_query_basic(self, csn_client: TestClient, sample_aurora_research_query: dict, api_keys_available: dict):
        """Test basic research query"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/research-query",
            json=sample_aurora_research_query
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert data["agent"] == "Aurora (Real Perplexity)"
        assert data["status"] == "🔍 Research Intelligence Complete"
        assert "research_result" in data
        assert "query" in data
        assert "depth" in data
        assert "timestamp" in data

    def test_research_query_with_sources(self, csn_client: TestClient, api_keys_available: dict):
        """Test research query requires sources"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/research-query",
            json={
                "query": "What is the current state of consciousness research?",
                "depth": "comprehensive",
                "sources_required": True
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Should have research result from Perplexity
        assert "research_result" in data
        result = data["research_result"]
        assert isinstance(result, str)
        assert len(result) > 0

    def test_research_query_with_biofield_context(self, csn_client: TestClient, sample_biofield_data: dict, api_keys_available: dict):
        """Test research query with biofield context"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/research-query",
            json={
                "query": "Consciousness and biofield coherence",
                "depth": "comprehensive",
                "sources_required": True,
                "biofield_context": sample_biofield_data
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Biofield context should be included in response
        assert "biofield_context" in data
        assert data["biofield_context"] == sample_biofield_data

    def test_research_query_fallback_mode(self, csn_client: TestClient):
        """Test Aurora fallback mode when API key missing"""
        # Temporarily remove API key
        import os
        original_key = os.getenv("PERPLEXITY_API_KEY")

        if original_key:
            pytest.skip("Cannot test fallback with API key present")

        response = csn_client.post(
            "/agent/aurora/research-query",
            json={
                "query": "Test query",
                "depth": "basic",
                "sources_required": False
            }
        )

        # Should still return 200 with fallback response
        assert response.status_code == 200
        data = response.json()
        assert "research_result" in data


@pytest.mark.integration
@pytest.mark.aurora
class TestAuroraFactCheck:
    """Test Aurora fact-checking endpoint"""

    def test_fact_check_basic(self, csn_client: TestClient, api_keys_available: dict):
        """Test basic fact-checking"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/fact-check",
            json={
                "claim": "HRV patterns correlate with emotional coherence",
                "context": "Biofield research",
                "evidence_threshold": "moderate"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["agent"] == "Aurora (Real Perplexity)"
        assert data["status"] == "✅ Fact-Check Complete"
        assert "fact_check_result" in data
        assert "claim" in data
        assert "evidence_threshold" in data

    def test_fact_check_evidence_levels(self, csn_client: TestClient, api_keys_available: dict):
        """Test different evidence threshold levels"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        thresholds = ["low", "moderate", "high"]

        for threshold in thresholds:
            response = csn_client.post(
                "/agent/aurora/fact-check",
                json={
                    "claim": "Test claim",
                    "context": "Test context",
                    "evidence_threshold": threshold
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["evidence_threshold"] == threshold


@pytest.mark.integration
@pytest.mark.aurora
class TestAuroraKnowledgeSynthesis:
    """Test Aurora knowledge synthesis endpoint"""

    def test_knowledge_synthesis_basic(self, csn_client: TestClient, api_keys_available: dict):
        """Test basic knowledge synthesis"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/knowledge-synthesis",
            json={
                "topics": ["consciousness", "collective intelligence", "AI"],
                "synthesis_depth": "comprehensive",
                "include_contradictions": True
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["agent"] == "Aurora (Real Perplexity)"
        assert data["status"] == "🔗 Knowledge Synthesis Complete"
        assert "synthesis_result" in data
        assert "topics" in data
        assert data["topics"] == ["consciousness", "collective intelligence", "AI"]

    def test_knowledge_synthesis_with_contradictions(self, csn_client: TestClient, api_keys_available: dict):
        """Test knowledge synthesis includes contradictions"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/knowledge-synthesis",
            json={
                "topics": ["consciousness", "materialism", "idealism"],
                "synthesis_depth": "comprehensive",
                "include_contradictions": True
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["include_contradictions"] == True


@pytest.mark.integration
@pytest.mark.aurora
class TestAuroraDailyInsights:
    """Test Aurora daily insights endpoint"""

    def test_daily_insights_basic(self, csn_client: TestClient, api_keys_available: dict):
        """Test daily insights generation"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/daily-insights",
            json={
                "domains": ["consciousness-tech", "collective intelligence", "shadow work"],
                "insight_count": 3,
                "priority": "high"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["agent"] == "Aurora (Real Perplexity)"
        assert data["status"] == "📊 Daily Insights Generated"
        assert "insights" in data
        assert "domains" in data
        assert data["domains"] == ["consciousness-tech", "collective intelligence", "shadow work"]

    def test_daily_insights_count(self, csn_client: TestClient, api_keys_available: dict):
        """Test daily insights count parameter"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        response = csn_client.post(
            "/agent/aurora/daily-insights",
            json={
                "domains": ["AI research"],
                "insight_count": 5,
                "priority": "medium"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert data["insight_count"] == 5


@pytest.mark.unit
@pytest.mark.aurora
class TestAuroraSystemPrompt:
    """Test Aurora system prompt and behavior"""

    def test_aurora_prompt_epistemology(self, csn_client: TestClient, api_keys_available: dict):
        """Test Aurora follows epistemological validation principles"""
        if not api_keys_available["perplexity"]:
            pytest.skip("Perplexity API key not configured")

        # Aurora should always provide evidence-based research
        response = csn_client.post(
            "/agent/aurora/research-query",
            json={
                "query": "What do we know about consciousness?",
                "depth": "comprehensive",
                "sources_required": True
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Aurora's research should be substantial (not just "I don't know")
        result = data["research_result"]
        assert len(result) > 50
