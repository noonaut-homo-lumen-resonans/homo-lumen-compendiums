"""
Orchestration API Router - Multi-Agent Live Streaming

Provides Server-Sent Events (SSE) endpoints for real-time agent activity monitoring.
Enables live "agent windows" in homo-lumen-resonans 3D interface.

Philosophy: "The collective thinks aloud - observe the symphony in real-time"
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, AsyncGenerator
from datetime import datetime
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/orchestrate", tags=["Agent Orchestration"])

# In-memory event store (for MVP - replace with Redis pub/sub later)
# Structure: {agent_id: [events]}
_agent_events: Dict[str, List[Dict[str, Any]]] = {}
_global_events: List[Dict[str, Any]] = []

# Agent status tracking
_agent_status: Dict[str, str] = {
    "orion": "idle",
    "thalus": "idle",
    "zara": "idle",
    "abacus": "idle",
    "lira": "idle",
    "nyra": "idle",
    "aurora": "idle",
    "manus": "idle",
    "code": "idle",
    # Add more agents as needed
}

# Response Models
class AgentEvent(BaseModel):
    """Individual agent event"""
    event_id: str
    agent_id: str
    event_type: str  # query_received, phase_start, connector_call, connector_response, synthesis_complete
    timestamp: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


class AgentStatus(BaseModel):
    """Current agent status"""
    agent_id: str
    status: str  # idle, thinking, responding, error
    current_activity: Optional[str] = None
    last_update: str


class AgentLog(BaseModel):
    """Agent activity log entry"""
    timestamp: str
    level: str  # info, debug, warning, error
    message: str
    metadata: Optional[Dict[str, Any]] = None


class OrchestrationQuery(BaseModel):
    """Query submission to orchestration system"""
    query_id: str
    question: str
    requester: str
    agents: List[str]  # Which agents to include
    depth: str = "comprehensive"  # comprehensive, quick, deep
    biofield_context: Optional[Dict[str, Any]] = None


# ============================================================================
# AGENT STATUS ENDPOINTS
# ============================================================================

@router.get("/agents", response_model=List[Dict[str, Any]])
async def list_agents():
    """
    List all available agents with their current status.
    """
    agents = []
    for agent_id, status in _agent_status.items():
        agents.append({
            "agent_id": agent_id,
            "status": status,
            "display_name": agent_id.capitalize(),
            "last_update": datetime.now().isoformat()
        })

    return agents


@router.get("/agents/{agent_id}/status", response_model=AgentStatus)
async def get_agent_status(agent_id: str):
    """
    Get current status of a specific agent.
    """
    if agent_id not in _agent_status:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    return AgentStatus(
        agent_id=agent_id,
        status=_agent_status[agent_id],
        current_activity=None,  # TODO: Track current activity
        last_update=datetime.now().isoformat()
    )


@router.post("/agents/{agent_id}/status")
async def update_agent_status(agent_id: str, status: str, activity: Optional[str] = None):
    """
    Update agent status (called by agents or orchestrator).

    Internal endpoint for agents to report their status.
    """
    if agent_id not in _agent_status:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    _agent_status[agent_id] = status

    # Broadcast status change as event
    event = {
        "event_id": f"status_{agent_id}_{datetime.now().timestamp()}",
        "agent_id": agent_id,
        "event_type": "status_change",
        "timestamp": datetime.now().isoformat(),
        "message": f"Status changed to: {status}",
        "metadata": {"status": status, "activity": activity}
    }

    # Store in agent-specific events
    if agent_id not in _agent_events:
        _agent_events[agent_id] = []
    _agent_events[agent_id].append(event)

    # Store in global events
    _global_events.append(event)

    return {"success": True, "agent_id": agent_id, "status": status}


# ============================================================================
# AGENT LOGS ENDPOINTS
# ============================================================================

@router.get("/agents/{agent_id}/logs", response_model=List[AgentLog])
async def get_agent_logs(agent_id: str, limit: int = 50):
    """
    Get recent activity logs for a specific agent.
    """
    if agent_id not in _agent_status:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    # Get events for this agent
    events = _agent_events.get(agent_id, [])

    # Convert events to logs
    logs = []
    for event in events[-limit:]:
        logs.append(AgentLog(
            timestamp=event["timestamp"],
            level="info",
            message=event["message"],
            metadata=event.get("metadata")
        ))

    return logs


# ============================================================================
# SERVER-SENT EVENTS (SSE) ENDPOINTS
# ============================================================================

async def event_generator(agent_id: Optional[str] = None) -> AsyncGenerator[str, None]:
    """
    Generate Server-Sent Events for agent activity.

    If agent_id is provided, only sends events for that agent.
    Otherwise, sends all global events.
    """
    last_event_index = 0

    while True:
        # Determine which events to send
        if agent_id:
            events = _agent_events.get(agent_id, [])
        else:
            events = _global_events

        # Send new events since last check
        new_events = events[last_event_index:]

        for event in new_events:
            # Format as SSE
            event_data = json.dumps(event)
            yield f"data: {event_data}\n\n"

        last_event_index = len(events)

        # Keep connection alive with heartbeat
        if not new_events:
            yield f": heartbeat\n\n"

        # Wait before next check (1 second polling)
        await asyncio.sleep(1)


@router.get("/agents/{agent_id}/stream")
async def stream_agent_events(agent_id: str):
    """
    Stream real-time events for a specific agent via Server-Sent Events (SSE).

    Usage:
        const eventSource = new EventSource('/api/orchestrate/agents/orion/stream');
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data);
        };
    """
    if agent_id not in _agent_status:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    return StreamingResponse(
        event_generator(agent_id=agent_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering in nginx
        }
    )


@router.get("/events")
async def stream_global_events():
    """
    Stream all orchestration events via Server-Sent Events (SSE).

    Includes events from all agents and system-wide orchestration events.
    """
    return StreamingResponse(
        event_generator(agent_id=None),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# ============================================================================
# QUERY ORCHESTRATION ENDPOINTS
# ============================================================================

@router.post("/query")
async def submit_orchestrated_query(query: OrchestrationQuery):
    """
    Submit a query to the orchestration system.

    This endpoint:
    1. Broadcasts query to specified agents
    2. Tracks query progress
    3. Emits events for each phase
    4. Returns query_id for tracking

    Frontend can then connect to SSE streams to watch live progress.
    """
    # Emit query_received event
    for agent_id in query.agents:
        event = {
            "event_id": f"query_{query.query_id}_{agent_id}",
            "agent_id": agent_id,
            "event_type": "query_received",
            "timestamp": datetime.now().isoformat(),
            "message": f"Query received: {query.question[:50]}...",
            "metadata": {
                "query_id": query.query_id,
                "question": query.question,
                "requester": query.requester,
                "depth": query.depth
            }
        }

        if agent_id not in _agent_events:
            _agent_events[agent_id] = []
        _agent_events[agent_id].append(event)
        _global_events.append(event)

        # Update agent status
        _agent_status[agent_id] = "thinking"

    # TODO: Actually route query to agents (integrate with CSN Server)
    # For now, just acknowledge receipt

    return {
        "success": True,
        "query_id": query.query_id,
        "message": "Query submitted to orchestration system",
        "agents": query.agents,
        "stream_url": "/api/orchestrate/events"
    }


# ============================================================================
# HELPER FUNCTIONS (for internal use)
# ============================================================================

def emit_agent_event(
    agent_id: str,
    event_type: str,
    message: str,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Helper function to emit an agent event.

    Can be called from other parts of the API to broadcast agent activity.
    """
    event = {
        "event_id": f"{event_type}_{agent_id}_{datetime.now().timestamp()}",
        "agent_id": agent_id,
        "event_type": event_type,
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "metadata": metadata or {}
    }

    if agent_id not in _agent_events:
        _agent_events[agent_id] = []
    _agent_events[agent_id].append(event)
    _global_events.append(event)

    logger.info(f"[{agent_id}] {event_type}: {message}")


# Example usage (for testing):
# emit_agent_event("orion", "connector_call", "→ NotebookLM: Searching 'OAuth scope'")
# emit_agent_event("orion", "connector_response", "← NotebookLM: 3 passages found", {"count": 3})
