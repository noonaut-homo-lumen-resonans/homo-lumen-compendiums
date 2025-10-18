"""
Coordination Endpoints Router

Provides REST API endpoints for multi-platform agent coordination:
- Agent status and health monitoring
- Platform-specific operations
- Coordination mode management
- Performance metrics and analytics
- Biofield-responsive processing
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
import structlog

from platforms.agent_coordination_hub import AgentCoordinationHub, CoordinationMode
from platforms.base_platform_agent import AgentRole, PlatformType

logger = structlog.get_logger()

router = APIRouter()

# Global coordination hub reference (set by main app)
coordination_hub: Optional[AgentCoordinationHub] = None

class OperationRequest(BaseModel):
    """Request model for multi-agent operations"""
    function_name: str
    data: Dict[str, Any]
    coordination_mode: CoordinationMode = CoordinationMode.ADAPTIVE
    complexity: float = 0.7
    target_agents: Optional[List[str]] = None

class AgentStatusResponse(BaseModel):
    """Response model for agent status"""
    agent_role: str
    platform_type: str
    status: str
    model: str
    mcp_tools: List[str]
    last_activity: Optional[str] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class CoordinationStatusResponse(BaseModel):
    """Response model for coordination hub status"""
    status: str
    total_agents: int
    available_agents: List[str]
    platform_availability: Dict[str, bool]
    performance_metrics: Dict[str, Any]
    biofield_thresholds: Dict[str, float]
    last_health_check: Optional[str] = None

@router.get("/status", response_model=CoordinationStatusResponse)
async def get_coordination_status():
    """Get comprehensive coordination hub status"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        status = coordination_hub.get_coordination_status()
        return CoordinationStatusResponse(**status)
        
    except Exception as e:
        logger.error("Failed to get coordination status", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get coordination status: {str(e)}"
        )

@router.get("/agents", response_model=List[AgentStatusResponse])
async def get_all_agent_status():
    """Get status of all platform agents"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        agent_statuses = []
        
        for role, agent in coordination_hub.agents.items():
            try:
                status = agent.get_agent_status()
                agent_statuses.append(AgentStatusResponse(
                    agent_role=role.value,
                    platform_type=status.get("platform_type", "unknown"),
                    status=status.get("status", "unknown"),
                    model=status.get("model", "unknown"),
                    mcp_tools=status.get("mcp_tools", []),
                    last_activity=status.get("last_activity"),
                    performance_metrics=status.get("performance_metrics")
                ))
            except Exception as e:
                logger.error(f"Failed to get status for agent {role.value}", error=str(e))
                agent_statuses.append(AgentStatusResponse(
                    agent_role=role.value,
                    platform_type="unknown",
                    status="error",
                    model="unknown",
                    mcp_tools=[],
                    performance_metrics={"error": str(e)}
                ))
        
        return agent_statuses
        
    except Exception as e:
        logger.error("Failed to get agent statuses", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get agent statuses: {str(e)}"
        )

@router.get("/agents/{agent_role}", response_model=AgentStatusResponse)
async def get_agent_status(agent_role: str):
    """Get status of specific agent by role"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        # Convert string to AgentRole enum
        role = AgentRole(agent_role)
        
        if role not in coordination_hub.agents:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_role} not found"
            )
        
        agent = coordination_hub.agents[role]
        status = agent.get_agent_status()
        
        return AgentStatusResponse(
            agent_role=role.value,
            platform_type=status.get("platform_type", "unknown"),
            status=status.get("status", "unknown"),
            model=status.get("model", "unknown"),
            mcp_tools=status.get("mcp_tools", []),
            last_activity=status.get("last_activity"),
            performance_metrics=status.get("performance_metrics")
        )
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid agent role: {agent_role}"
        )
    except Exception as e:
        logger.error(f"Failed to get status for agent {agent_role}", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get agent status: {str(e)}"
        )

@router.post("/execute")
async def execute_coordinated_operation(request: OperationRequest):
    """Execute operation across multiple agents with coordination"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        # Validate function name
        if not request.function_name:
            raise HTTPException(
                status_code=400,
                detail="function_name is required"
            )
        
        # Prepare operation data
        operation_data = {
            "function_name": request.function_name,
            "data": request.data
        }
        
        # Execute operation
        result = await coordination_hub.execute_multi_agent_operation(
            operation_data=operation_data,
            coordination_mode=request.coordination_mode,
            complexity=request.complexity
        )
        
        return {
            "success": True,
            "operation_id": f"op_{datetime.utcnow().timestamp()}",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Coordinated operation failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Operation failed: {str(e)}"
        )

@router.post("/agents/{agent_role}/execute")
async def execute_single_agent_operation(
    agent_role: str,
    function_name: str,
    data: Dict[str, Any],
    complexity: float = Query(0.7, ge=0.0, le=1.0)
):
    """Execute operation on specific agent"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        # Convert string to AgentRole enum
        role = AgentRole(agent_role)
        
        if role not in coordination_hub.agents:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_role} not found"
            )
        
        agent = coordination_hub.agents[role]
        
        # Execute operation
        result = await agent.execute_mcp_function(
            function_name=function_name,
            data=data,
            complexity=complexity
        )
        
        return {
            "success": True,
            "agent_role": agent_role,
            "function_name": function_name,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid agent role: {agent_role}"
        )
    except Exception as e:
        logger.error(f"Single agent operation failed for {agent_role}", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Operation failed: {str(e)}"
        )

@router.get("/performance")
async def get_performance_metrics():
    """Get performance metrics for coordination hub"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        status = coordination_hub.get_coordination_status()
        performance = status.get("performance_metrics", {})
        
        return {
            "success": True,
            "performance_metrics": performance,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get performance metrics", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get performance metrics: {str(e)}"
        )

@router.post("/health-check")
async def perform_health_check(background_tasks: BackgroundTasks):
    """Perform health check on all agents"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        # Perform health check in background
        background_tasks.add_task(coordination_hub._perform_health_check)
        
        return {
            "success": True,
            "message": "Health check initiated",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to initiate health check", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initiate health check: {str(e)}"
        )

@router.get("/modes")
async def get_coordination_modes():
    """Get available coordination modes"""
    return {
        "success": True,
        "coordination_modes": [
            {
                "mode": mode.value,
                "description": get_coordination_mode_description(mode)
            }
            for mode in CoordinationMode
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/platforms")
async def get_platform_info():
    """Get information about supported platforms"""
    return {
        "success": True,
        "platforms": [
            {
                "platform": platform.value,
                "description": get_platform_description(platform),
                "agent_roles": get_platform_agents(platform)
            }
            for platform in PlatformType
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/biofield-thresholds")
async def get_biofield_thresholds():
    """Get biofield thresholds for coordination"""
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    return {
        "success": True,
        "biofield_thresholds": coordination_hub.biofield_thresholds,
        "timestamp": datetime.utcnow().isoformat()
    }

def get_coordination_mode_description(mode: CoordinationMode) -> str:
    """Get description for coordination mode"""
    descriptions = {
        CoordinationMode.PARALLEL: "All agents process simultaneously for maximum throughput",
        CoordinationMode.SEQUENTIAL: "Agents process in sequence for controlled execution",
        CoordinationMode.ADAPTIVE: "Biofield-responsive agent selection and processing",
        CoordinationMode.EMERGENCY: "Limited processing for low biofield coherence states"
    }
    return descriptions.get(mode, "Unknown coordination mode")

def get_platform_description(platform: PlatformType) -> str:
    """Get description for platform"""
    descriptions = {
        PlatformType.OPENAI: "OpenAI GPT-4 for biofield analysis and empathy",
        PlatformType.GEMINI: "Google Gemini Pro for visual intelligence",
        PlatformType.GROK: "X.AI Grok for philosophical validation",
        PlatformType.DEEPSEEK: "DeepSeek for creative innovation",
        PlatformType.CLAUDE: "Anthropic Claude for coordination and analytics"
    }
    return descriptions.get(platform, "Unknown platform")

def get_platform_agents(platform: PlatformType) -> List[str]:
    """Get agent roles for platform"""
    platform_agents = {
        PlatformType.OPENAI: ["LIRA"],
        PlatformType.GEMINI: ["NYRA"],
        PlatformType.GROK: ["THALUS"],
        PlatformType.DEEPSEEK: ["ZARA"],
        PlatformType.CLAUDE: ["ORION", "ABACUS"]
    }
    return platform_agents.get(platform, []) 