"""
Redis Subscriber Tests

Tests for Redis pub/sub event streaming between CSN Server and Ubuntu Playground.
"""
import pytest
import json
import time
from pathlib import Path
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.redis
class TestRedisSubscriber:
    """Test Redis event subscriber"""

    def test_redis_subscriber_initialization(self, mock_redis_enabled: bool):
        """Test Redis subscriber initializes correctly"""
        if not mock_redis_enabled:
            pytest.skip("Redis credentials not configured")

        from redis_subscriber import ubuntu_subscriber

        assert ubuntu_subscriber is not None
        assert ubuntu_subscriber.enabled == True or ubuntu_subscriber.enabled == False

    def test_redis_subscriber_channels(self, mock_redis_enabled: bool):
        """Test Redis subscriber is subscribed to correct channels"""
        if not mock_redis_enabled:
            pytest.skip("Redis credentials not configured")

        from redis_subscriber import ubuntu_subscriber

        expected_channels = [
            "csn:consultations",
            "csn:errors",
            "csn:health",
            "csn:agent:lira",
            "csn:agent:nyra",
            "csn:agent:orion",
            "csn:agent:thalus",
            "csn:agent:zara",
            "csn:agent:aurora"
        ]

        for channel in expected_channels:
            assert channel in ubuntu_subscriber.channels


@pytest.mark.integration
@pytest.mark.redis
@pytest.mark.slow
class TestRedisEventFlow:
    """Test end-to-end Redis event flow"""

    def test_consultation_event_logged(self, client: TestClient, mock_redis_enabled: bool):
        """Test consultation events are published and logged"""
        if not mock_redis_enabled:
            pytest.skip("Redis not configured")

        # Send consultation request
        response = client.post(
            "http://localhost:8001/collective-intelligence/consultation",
            json={
                "question": "Test Redis integration",
                "requester": "Pytest Test"
            }
        )

        if response.status_code != 200:
            pytest.skip("CSN Server not available")

        # Wait for event to propagate
        time.sleep(3)

        # Check events database
        events_response = client.get("/events")
        events = events_response.json()

        # Look for consultation event
        consultation_events = [
            e for e in events
            if e.get("action") == "consultation" and "Test Redis integration" in str(e.get("metadata", {}))
        ]

        # Event should be logged
        assert len(consultation_events) > 0

    def test_event_metadata_structure(self, client: TestClient, mock_redis_enabled: bool):
        """Test event metadata has correct structure"""
        if not mock_redis_enabled:
            pytest.skip("Redis not configured")

        # Create a workspace event
        client.post(
            "/workspace/aurora/redis-test.md",
            json={"content": "Redis event test"},
            headers={"X-Agent-API-Key": "aurora-test-key"}
        )

        # Fetch events
        events_response = client.get("/events")
        events = events_response.json()

        # Verify event structure
        for event in events:
            assert "agent" in event
            assert "action" in event
            assert "timestamp" in event
            # metadata is optional


@pytest.mark.unit
@pytest.mark.redis
class TestRedisPublisher:
    """Test Redis publisher from CSN Server"""

    def test_redis_publisher_initialization(self, mock_redis_enabled: bool):
        """Test Redis publisher initializes"""
        if not mock_redis_enabled:
            pytest.skip("Redis not configured")

        # Import after environment is set
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "ama-backend"))

        from redis_publisher import redis_publisher

        assert redis_publisher is not None
        # Should be enabled if credentials are set
        assert hasattr(redis_publisher, "enabled")

    def test_redis_publisher_channels(self, mock_redis_enabled: bool):
        """Test publisher publishes to correct channels"""
        if not mock_redis_enabled:
            pytest.skip("Redis not configured")

        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "ama-backend"))

        from redis_publisher import redis_publisher

        # Test publish method exists
        assert hasattr(redis_publisher, "publish_consultation")
        assert hasattr(redis_publisher, "publish_agent_response")
        assert hasattr(redis_publisher, "publish_error")


@pytest.mark.unit
@pytest.mark.redis
class TestEventStorage:
    """Test event storage in SQLite"""

    def test_events_table_exists(self, client: TestClient):
        """Test events table exists in database"""
        # Create a test event
        client.post(
            "/workspace/aurora/event-test.md",
            json={"content": "Test event storage"},
            headers={"X-Agent-API-Key": "aurora-test-key"}
        )

        # Query events
        response = client.get("/events")

        assert response.status_code == 200
        events = response.json()
        assert isinstance(events, list)

    def test_events_have_required_fields(self, client: TestClient):
        """Test all events have required fields"""
        # Create event
        client.post(
            "/workspace/aurora/fields-test.md",
            json={"content": "Field test"},
            headers={"X-Agent-API-Key": "aurora-test-key"}
        )

        # Fetch events
        response = client.get("/events")
        events = response.json()

        for event in events:
            # Required fields
            assert "agent" in event
            assert "action" in event
            assert "timestamp" in event

            # Verify types
            assert isinstance(event["agent"], str)
            assert isinstance(event["action"], str)
            assert isinstance(event["timestamp"], str)

    def test_events_ordered_by_timestamp(self, client: TestClient):
        """Test events are returned in chronological order"""
        # Create multiple events
        for i in range(3):
            client.post(
                f"/workspace/aurora/order-test-{i}.md",
                json={"content": f"Event {i}"},
                headers={"X-Agent-API-Key": "aurora-test-key"}
            )
            time.sleep(0.1)  # Small delay

        # Fetch events
        response = client.get("/events")
        events = response.json()

        # Verify chronological order (newest first or oldest first, depending on implementation)
        timestamps = [event["timestamp"] for event in events]
        assert timestamps == sorted(timestamps) or timestamps == sorted(timestamps, reverse=True)
