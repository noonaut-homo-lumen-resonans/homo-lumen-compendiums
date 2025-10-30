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
import httpx

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


class ConsultationRequest(BaseModel):
    """Consultation request from frontend"""
    query: str
    enabled_connectors: Optional[List[str]] = []


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


@router.post("/consult")
async def submit_consultation(request: ConsultationRequest):
    """
    Submit a consultation query with enabled MCP connectors.

    This endpoint:
    1. Receives query + enabled_connectors from frontend
    2. Logs connector state (Fase 1: Foundation)
    3. Forwards to CSN Server for multi-agent consultation
    4. Returns consultation result

    Future: Will use enabled_connectors to filter agent tools (Fase 2+)
    """
    logger.info(f"📥 Consultation Request:")
    logger.info(f"  Query: {request.query[:100]}...")
    logger.info(f"  Enabled Connectors ({len(request.enabled_connectors)}): {request.enabled_connectors}")

    # Emit connector_selection event for tracking
    for connector_id in request.enabled_connectors:
        emit_agent_event(
            agent_id="system",
            event_type="connector_enabled",
            message=f"Connector enabled: {connector_id}",
            metadata={"connector_id": connector_id}
        )

    # Emit query_received for all 6 agents (Hexagonal Architecture)
    agents = ["orion", "lira", "nyra", "thalus", "zara", "aurora"]
    for agent_id in agents:
        emit_agent_event(
            agent_id=agent_id,
            event_type="query_received",
            message=f"{agent_id.capitalize()} received query",
            metadata={"query": request.query[:100]}
        )

    # Emit phase_start for agent processing
    for agent_id in agents:
        emit_agent_event(
            agent_id=agent_id,
            event_type="phase_start",
            message=f"{agent_id.capitalize()} started processing",
            metadata={"phase": "agent_processing"}
        )

    # Forward to CSN Server on port 8001
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:8001/consult",
                json={
                    "query": request.query,
                    "enabled_connectors": request.enabled_connectors
                }
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Consultation successful: {result.get('consultation_id', 'N/A')}")

                # Add connector info to result
                result["enabled_connectors"] = request.enabled_connectors
                result["connector_count"] = len(request.enabled_connectors)

                # Emit agent_response events for ALL 6 agents (Hexagonal Architecture)
                agent_responses = result.get("agent_responses", [])
                for agent_resp in agent_responses:
                    agent_name = agent_resp.get("agent", "").lower()
                    response_text = agent_resp.get("response", "")

                    if response_text and agent_name:
                        emit_agent_event(
                            agent_id=agent_name,
                            event_type="agent_response",
                            message=response_text,
                            metadata={
                                "consultation_id": result.get("consultation_id"),
                                "tool_results": result.get("tool_results", []),
                                "tool_usage": result.get("tool_usage_summary"),
                                "query": request.query
                            }
                        )

                # Emit synthesis_complete for all 6 agents (Hexagonal Architecture - PhaseTracker phase 5)
                agents = ["orion", "lira", "nyra", "thalus", "zara", "aurora"]
                for agent_id in agents:
                    emit_agent_event(
                        agent_id=agent_id,
                        event_type="synthesis_complete",
                        message=f"{agent_id.capitalize()} synthesis complete",
                        metadata={
                            "consultation_id": result.get("consultation_id"),
                            "tool_usage": result.get("tool_usage_summary")
                        }
                    )

                # Emit Orion's meta-synthesis (Essence of Truth)
                orion_synthesis = result.get("orion_synthesis", "")
                logger.info(f"🌟 Orion synthesis available: {bool(orion_synthesis)} (length: {len(orion_synthesis) if orion_synthesis else 0})")
                if orion_synthesis:
                    logger.info(f"✨ Emitting orion_synthesis event for consultation {result.get('consultation_id')}")
                    emit_agent_event(
                        agent_id="orion",
                        event_type="orion_synthesis",
                        message=orion_synthesis,
                        metadata={
                            "consultation_id": result.get("consultation_id"),
                            "synthesis_type": "essence_of_truth",
                            "agent_count": len(result.get("agent_responses", []))
                        }
                    )
                    logger.info(f"✅ Orion synthesis event emitted successfully")

                return result
            else:
                logger.error(f"❌ CSN Server error: {response.status_code}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"CSN Server returned error: {response.text}"
                )

    except httpx.ConnectError:
        logger.error("❌ Cannot connect to CSN Server (port 8001)")
        raise HTTPException(
            status_code=503,
            detail="CSN Server not available. Please ensure it's running on port 8001."
        )
    except Exception as e:
        logger.error(f"❌ Consultation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Consultation failed: {str(e)}"
        )


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
