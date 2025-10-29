"""
Agent coordination endpoints for CSN Server
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import structlog
import asyncio
import json
from datetime import datetime

from csn_server.config import settings

logger = structlog.get_logger()
router = APIRouter()


class AgentMessage(BaseModel):
    """Agent message model"""
    agent_id: str
    message_type: str
    content: Dict[str, Any]
    target_agents: Optional[List[str]] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentRegistration(BaseModel):
    """Agent registration model"""
    agent_id: str
    agent_type: str
    capabilities: List[str]
    status: str = "active"
    metadata: Optional[Dict[str, Any]] = None


class AgentCoordinationRequest(BaseModel):
    """Agent coordination request"""
    operation: str  # "register", "unregister", "message", "broadcast"
    data: Dict[str, Any]


# In-memory storage for agents and messages
registered_agents: Dict[str, AgentRegistration] = {}
active_connections: Dict[str, WebSocket] = {}
message_queue: List[AgentMessage] = []


class ConnectionManager:
    """Manage WebSocket connections for agent communication"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, agent_id: str):
        await websocket.accept()
        self.active_connections[agent_id] = websocket
        logger.info("Agent connected", agent_id=agent_id)
    
    def disconnect(self, agent_id: str):
        if agent_id in self.active_connections:
            del self.active_connections[agent_id]
            logger.info("Agent disconnected", agent_id=agent_id)
    
    async def send_personal_message(self, message: str, agent_id: str):
        if agent_id in self.active_connections:
            await self.active_connections[agent_id].send_text(message)
    
    async def broadcast(self, message: str, exclude_agent: Optional[str] = None):
        for agent_id, connection in self.active_connections.items():
            if agent_id != exclude_agent:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error("Failed to send message to agent", 
                               agent_id=agent_id, error=str(e))
                    self.disconnect(agent_id)


manager = ConnectionManager()


@router.post("/register")
async def register_agent(registration: AgentRegistration) -> Dict[str, Any]:
    """Register a new agent"""
    try:
        if registration.agent_id in registered_agents:
            raise HTTPException(status_code=400, detail="Agent already registered")
        
        registered_agents[registration.agent_id] = registration
        registration.timestamp = datetime.now()
        
        logger.info("Agent registered", 
                   agent_id=registration.agent_id,
                   agent_type=registration.agent_type)
        
        return {
            "status": "registered",
            "agent_id": registration.agent_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Agent registration failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/unregister")
async def unregister_agent(agent_id: str) -> Dict[str, Any]:
    """Unregister an agent"""
    try:
        if agent_id not in registered_agents:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        del registered_agents[agent_id]
        manager.disconnect(agent_id)
        
        logger.info("Agent unregistered", agent_id=agent_id)
        
        return {
            "status": "unregistered",
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Agent unregistration failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Unregistration failed: {str(e)}")


@router.post("/message")
async def send_agent_message(message: AgentMessage) -> Dict[str, Any]:
    """Send a message to specific agents"""
    try:
        if message.agent_id not in registered_agents:
            raise HTTPException(status_code=404, detail="Source agent not registered")
        
        message.timestamp = datetime.now()
        message_queue.append(message)
        
        # Send to target agents if they're connected
        if message.target_agents:
            for target_id in message.target_agents:
                if target_id in manager.active_connections:
                    await manager.send_personal_message(
                        json.dumps({
                            "from": message.agent_id,
                            "type": message.message_type,
                            "content": message.content,
                            "timestamp": message.timestamp.isoformat(),
                            "metadata": message.metadata
                        }),
                        target_id
                    )
        
        logger.info("Agent message sent", 
                   from_agent=message.agent_id,
                   to_agents=message.target_agents,
                   message_type=message.message_type)
        
        return {
            "status": "sent",
            "message_id": f"msg_{len(message_queue)}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Agent message failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Message failed: {str(e)}")


@router.post("/broadcast")
async def broadcast_message(message: AgentMessage) -> Dict[str, Any]:
    """Broadcast a message to all connected agents"""
    try:
        if message.agent_id not in registered_agents:
            raise HTTPException(status_code=404, detail="Source agent not registered")
        
        message.timestamp = datetime.now()
        message_queue.append(message)
        
        # Broadcast to all connected agents except sender
        await manager.broadcast(
            json.dumps({
                "from": message.agent_id,
                "type": message.message_type,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "metadata": message.metadata,
                "broadcast": True
            }),
            exclude_agent=message.agent_id
        )
        
        logger.info("Agent broadcast sent", 
                   from_agent=message.agent_id,
                   message_type=message.message_type)
        
        return {
            "status": "broadcast",
            "message_id": f"msg_{len(message_queue)}",
            "recipients": len(manager.active_connections) - 1,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error("Agent broadcast failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Broadcast failed: {str(e)}")


@router.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket endpoint for real-time agent communication"""
    try:
        if agent_id not in registered_agents:
            await websocket.close(code=4004, reason="Agent not registered")
            return
        
        await manager.connect(websocket, agent_id)
        
        try:
            while True:
                # Receive message from agent
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Process incoming message
                await process_incoming_message(agent_id, message_data)
                
        except WebSocketDisconnect:
            manager.disconnect(agent_id)
        except Exception as e:
            logger.error("WebSocket error", agent_id=agent_id, error=str(e))
            manager.disconnect(agent_id)
            
    except Exception as e:
        logger.error("WebSocket connection failed", agent_id=agent_id, error=str(e))


async def process_incoming_message(agent_id: str, message_data: Dict[str, Any]):
    """Process incoming message from agent"""
    try:
        message_type = message_data.get("type", "unknown")
        content = message_data.get("content", {})
        target_agents = message_data.get("target_agents", [])
        
        # Create agent message
        message = AgentMessage(
            agent_id=agent_id,
            message_type=message_type,
            content=content,
            target_agents=target_agents,
            timestamp=datetime.now()
        )
        
        # Handle different message types
        if message_type == "coordinate":
            await handle_coordination_message(message)
        elif message_type == "status":
            await handle_status_message(message)
        elif message_type == "task":
            await handle_task_message(message)
        else:
            # Default: forward to target agents
            if target_agents:
                for target_id in target_agents:
                    if target_id in manager.active_connections:
                        await manager.send_personal_message(
                            json.dumps({
                                "from": agent_id,
                                "type": message_type,
                                "content": content,
                                "timestamp": message.timestamp.isoformat()
                            }),
                            target_id
                        )
        
        logger.info("Incoming message processed", 
                   agent_id=agent_id,
                   message_type=message_type)
        
    except Exception as e:
        logger.error("Failed to process incoming message", 
                   agent_id=agent_id, error=str(e))


async def handle_coordination_message(message: AgentMessage):
    """Handle coordination messages between agents"""
    # Implement coordination logic here
    # This could involve task distribution, load balancing, etc.
    pass


async def handle_status_message(message: AgentMessage):
    """Handle status update messages from agents"""
    # Update agent status in registry
    if message.agent_id in registered_agents:
        registered_agents[message.agent_id].status = message.content.get("status", "active")
        registered_agents[message.agent_id].metadata = message.content.get("metadata", {})


async def handle_task_message(message: AgentMessage):
    """Handle task-related messages between agents"""
    # Implement task distribution logic here
    pass


@router.get("/agents")
async def list_agents() -> Dict[str, Any]:
    """List all registered agents"""
    try:
        agents = []
        for agent_id, agent in registered_agents.items():
            agents.append({
                "id": agent_id,
                "type": agent.agent_type,
                "capabilities": agent.capabilities,
                "status": agent.status,
                "connected": agent_id in manager.active_connections,
                "metadata": agent.metadata
            })
        
        return {
            "agents": agents,
            "total": len(agents),
            "connected": len(manager.active_connections)
        }
    except Exception as e:
        logger.error("Failed to list agents", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")


@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str) -> Dict[str, Any]:
    """Get specific agent information"""
    try:
        if agent_id not in registered_agents:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        agent = registered_agents[agent_id]
        return {
            "id": agent_id,
            "type": agent.agent_type,
            "capabilities": agent.capabilities,
            "status": agent.status,
            "connected": agent_id in manager.active_connections,
            "metadata": agent.metadata
        }
    except Exception as e:
        logger.error("Failed to get agent", agent_id=agent_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get agent: {str(e)}")


@router.get("/messages")
async def get_message_history(limit: int = 100) -> Dict[str, Any]:
    """Get message history"""
    try:
        recent_messages = message_queue[-limit:] if message_queue else []
        
        return {
            "messages": [
                {
                    "id": f"msg_{i}",
                    "from": msg.agent_id,
                    "type": msg.message_type,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                    "target_agents": msg.target_agents
                }
                for i, msg in enumerate(recent_messages)
            ],
            "total": len(message_queue),
            "limit": limit
        }
    except Exception as e:
        logger.error("Failed to get message history", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")


@router.get("/status")
async def agent_coordination_status() -> Dict[str, Any]:
    """Get agent coordination service status"""
    try:
        return {
            "status": "running",
            "registered_agents": len(registered_agents),
            "connected_agents": len(manager.active_connections),
            "message_queue_size": len(message_queue),
            "enabled": settings.agent_coordination_enabled,
            "websocket_enabled": settings.websocket_enabled,
            "websocket_port": settings.websocket_port
        }
    except Exception as e:
        logger.error("Agent coordination status check failed", error=str(e))
        return {
            "status": "error",
            "error": str(e)
        } 