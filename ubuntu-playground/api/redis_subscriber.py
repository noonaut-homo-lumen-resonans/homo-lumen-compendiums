"""
Redis Event Subscriber for Ubuntu Playground

Subscribes to CSN Server events via Upstash Redis and logs them to SQLite.
Runs in a background thread to continuously listen for events.
"""
import os
import json
import time
import requests
import sqlite3
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env.local")


class UbuntuRedisSubscriber:
    """Redis subscriber using Upstash REST API polling"""

    def __init__(self, database_path: str = "./data/ubuntu-playground.db"):
        self.redis_url = os.getenv("REDIS_URL")
        self.redis_token = os.getenv("REDIS_TOKEN")
        self.database_path = Path(database_path)

        if not self.redis_url or not self.redis_token:
            print("⚠️  Redis credentials not found - subscriber will not run")
            self.enabled = False
        else:
            print(f"✅ Redis subscriber initialized: {self.redis_url}")
            self.enabled = True

        self.headers = {
            "Authorization": f"Bearer {self.redis_token}"
        } if self.redis_token else {}

        self.running = False
        self.channels = [
            "csn:consultations",
            "csn:errors",
            "csn:health"
        ]

        # Also subscribe to individual agent channels
        agents = ["lira", "nyra", "orion", "thalus", "zara", "aurora"]
        for agent in agents:
            self.channels.append(f"csn:agent:{agent}")

    def get_db_connection(self):
        """Get SQLite database connection"""
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.database_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize events table if it doesn't exist"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT NOT NULL,
                action TEXT NOT NULL,
                path TEXT,
                timestamp TEXT NOT NULL,
                metadata TEXT
            )
        """)

        conn.commit()
        conn.close()
        print("✅ Database initialized")

    def _poll_channel(self, channel: str) -> list:
        """
        Poll a Redis channel for messages using Upstash REST API

        Note: Upstash doesn't support traditional pub/sub over REST,
        so we use LPOP on a list-based queue instead.

        Alternative: Use Redis STREAMS (XREAD) for real message queuing.
        For MVP, we'll use a simple polling mechanism.

        Args:
            channel: Channel name to poll

        Returns:
            list: List of messages (empty if none)
        """
        if not self.enabled:
            return []

        try:
            # For MVP: Check if a "queue" key exists for this channel
            # Format: "queue:{channel}"
            queue_key = f"queue:{channel}"

            response = requests.post(
                f"{self.redis_url}/lpop/{queue_key}",
                headers=self.headers,
                timeout=5
            )

            if response.status_code == 200:
                result = response.json().get("result")
                if result:
                    return [result]

            return []

        except Exception as e:
            print(f"❌ Poll error for {channel}: {e}")
            return []

    def handle_event(self, channel: str, message: str):
        """
        Handle incoming event from Redis channel

        Args:
            channel: Channel name
            message: JSON string message
        """
        try:
            data = json.loads(message)
            event_type = data.get("event_type", "unknown")

            print(f"📥 Received event from {channel}: {event_type}")

            # Log to SQLite
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO events (agent, action, path, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data.get("agent", "system"),
                event_type,
                None,
                data.get("timestamp", datetime.now().isoformat()),
                json.dumps(data)
            ))

            conn.commit()
            conn.close()

            print(f"✅ Event logged to database: {event_type}")

            # Handle specific event types
            if event_type == "consultation":
                self._handle_consultation_event(data)
            elif event_type == "agent_response":
                self._handle_agent_response_event(data)
            elif event_type == "error":
                self._handle_error_event(data)

        except Exception as e:
            print(f"❌ Error handling event: {e}")

    def _handle_consultation_event(self, data: Dict[str, Any]):
        """Handle collective intelligence consultation event"""
        print(f"🤔 Consultation: {data.get('question', '')[:50]}...")
        print(f"👤 Requester: {data.get('requester')}")
        print(f"🧠 Agents: {', '.join(data.get('agents', []))}")

    def _handle_agent_response_event(self, data: Dict[str, Any]):
        """Handle individual agent response event"""
        agent = data.get("agent", "unknown")
        print(f"💬 {agent} responded ({data.get('response_length', 0)} chars)")

    def _handle_error_event(self, data: Dict[str, Any]):
        """Handle error event"""
        error_type = data.get("error_type", "unknown")
        error_message = data.get("error_message", "")
        print(f"⚠️  Error: {error_type} - {error_message}")

    def start_polling(self, poll_interval: int = 5):
        """
        Start polling Redis channels for events

        Args:
            poll_interval: Seconds between polls (default: 5)
        """
        if not self.enabled:
            print("⚠️  Redis subscriber not enabled (missing credentials)")
            return

        self.running = True
        self.init_database()

        print(f"🚀 Starting Redis subscriber (polling every {poll_interval}s)")
        print(f"📡 Subscribed to {len(self.channels)} channels")

        try:
            while self.running:
                for channel in self.channels:
                    messages = self._poll_channel(channel)
                    for message in messages:
                        self.handle_event(channel, message)

                time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("\n⛔ Subscriber stopped by user")
            self.running = False
        except Exception as e:
            print(f"❌ Subscriber error: {e}")
            self.running = False

    def stop(self):
        """Stop the subscriber"""
        self.running = False
        print("⛔ Subscriber stopping...")


# Global instance
ubuntu_subscriber = UbuntuRedisSubscriber()


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 UBUNTU PLAYGROUND REDIS SUBSCRIBER")
    print("=" * 60)
    print()

    # Start subscriber (runs forever until Ctrl+C)
    ubuntu_subscriber.start_polling(poll_interval=5)
