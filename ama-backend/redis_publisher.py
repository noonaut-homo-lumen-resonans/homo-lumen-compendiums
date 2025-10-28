"""
Redis Event Publisher for CSN Server

Publishes collective intelligence consultation events to Upstash Redis
so that Ubuntu Playground and other services can subscribe to real-time events.
"""
import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class CSNRedisPublisher:
    """Redis publisher using Upstash REST API"""

    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL")
        self.redis_token = os.getenv("REDIS_TOKEN")

        if not self.redis_url or not self.redis_token:
            print("⚠️  Redis credentials not found - publisher will run in mock mode")
            self.enabled = False
        else:
            print(f"✅ Redis publisher initialized: {self.redis_url}")
            self.enabled = True

        self.headers = {
            "Authorization": f"Bearer {self.redis_token}"
        } if self.redis_token else {}

    def _publish(self, channel: str, message: Dict[str, Any]) -> bool:
        """
        Publish message to Redis channel using Upstash REST API

        Args:
            channel: Redis channel name (e.g., "csn:consultations")
            message: Dictionary to publish (will be JSON serialized)

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled:
            print(f"🔇 Mock publish to {channel}: {json.dumps(message, indent=2)}")
            return False

        try:
            message_json = json.dumps(message)

            # Upstash REST API: POST /publish/{channel}/{message}
            # URL encode the message
            import urllib.parse
            encoded_message = urllib.parse.quote(message_json)

            response = requests.post(
                f"{self.redis_url}/publish/{channel}/{encoded_message}",
                headers=self.headers,
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                subscribers = result.get("result", 0)
                print(f"✅ Published to {channel} ({subscribers} subscribers)")
                return True
            else:
                print(f"❌ Publish failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Publish error: {e}")
            return False

    def publish_consultation(
        self,
        question: str,
        requester: str,
        agent_responses: Dict[str, str],
        essence_of_truth: str,
        biofield_context: Optional[Dict] = None
    ) -> bool:
        """
        Publish collective intelligence consultation event

        Args:
            question: The consultation question
            requester: Who requested the consultation
            agent_responses: Dictionary of agent responses
            essence_of_truth: Orion's synthesized truth
            biofield_context: Optional biofield data

        Returns:
            bool: True if published successfully
        """
        event = {
            "event_type": "consultation",
            "question": question,
            "requester": requester,
            "agent_count": len(agent_responses),
            "agents": list(agent_responses.keys()),
            "essence_of_truth": essence_of_truth[:200] + "..." if len(essence_of_truth) > 200 else essence_of_truth,
            "biofield_context": biofield_context or {},
            "timestamp": datetime.now().isoformat()
        }

        return self._publish("csn:consultations", event)

    def publish_agent_response(
        self,
        agent: str,
        response: str,
        question: str,
        requester: str
    ) -> bool:
        """
        Publish individual agent response event

        Args:
            agent: Agent name (e.g., "lira", "aurora")
            response: Agent's response text
            question: The question asked
            requester: Who requested

        Returns:
            bool: True if published successfully
        """
        event = {
            "event_type": "agent_response",
            "agent": agent,
            "response_preview": response[:150] + "..." if len(response) > 150 else response,
            "response_length": len(response),
            "question_preview": question[:100] + "..." if len(question) > 100 else question,
            "requester": requester,
            "timestamp": datetime.now().isoformat()
        }

        return self._publish(f"csn:agent:{agent}", event)

    def publish_error(
        self,
        error_type: str,
        error_message: str,
        context: Optional[Dict] = None
    ) -> bool:
        """
        Publish error event for monitoring

        Args:
            error_type: Type of error (e.g., "api_failure")
            error_message: Error message
            context: Optional context data

        Returns:
            bool: True if published successfully
        """
        event = {
            "event_type": "error",
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }

        return self._publish("csn:errors", event)

    def publish_health_check(self) -> bool:
        """
        Publish health check event

        Returns:
            bool: True if published successfully
        """
        event = {
            "event_type": "health_check",
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }

        return self._publish("csn:health", event)


# Global instance
redis_publisher = CSNRedisPublisher()


# Example usage
if __name__ == "__main__":
    print("Testing Redis Publisher...")

    # Test health check
    success = redis_publisher.publish_health_check()
    print(f"Health check published: {success}")

    # Test consultation event
    success = redis_publisher.publish_consultation(
        question="What is collective intelligence?",
        requester="Osvald",
        agent_responses={
            "lira": "Empathy response...",
            "orion": "Strategic response...",
            "aurora": "Research response..."
        },
        essence_of_truth="Collective intelligence is the emergent wisdom from multiple perspectives.",
        biofield_context={"hrv_ms": 85, "coherence": 0.75}
    )
    print(f"Consultation published: {success}")
