"""
Agent-Specific MCP Tools FastAPI Endpoints

Comprehensive endpoints for all agent tools:
- Lira: Biofield analysis and empathy
- Thalus: Philosophical validation
- Nyra: Visual intelligence
- Abacus: Analytical engine
- Polycomputational: Orchestration
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import structlog
import asyncio

from ..agents import (
    LiraBiofieldTools, ThalusPhilosophicalTools, NyraVisualTools, 
    AbacusAnalyticalTools, PolycomputationalOrchestrator
)
from ..routers.ama_memory_layers import AMAMemorySystem, BiofieldMetrics, MemoryLayer

# Configure logging
logger = structlog.get_logger()

# Create router
router = APIRouter(prefix="/agents", tags=["Agent MCP Tools"])

# --- Request/Response Models ---

class BiofieldDataRequest(BaseModel):
    """Request model for biofield data analysis"""
    hrv_ms: float = Field(..., ge=0, description="Heart Rate Variability in milliseconds")
    how_we_feel_markers: Dict[str, Any] = Field(default_factory=dict, description="How We Feel subjective markers")
    breath_pattern: List[int] = Field(..., description="Breath pattern [4,6,8]")
    coherence_score: float = Field(..., ge=0, le=1, description="Biofield coherence score")

class AgentOperationRequest(BaseModel):
    """Generic request model for agent operations"""
    operation_type: str = Field(..., description="Type of operation to perform")
    data: Dict[str, Any] = Field(..., description="Operation data")
    complexity: Optional[float] = Field(0.7, ge=0, le=1, description="Operation complexity")

class ISTProtocolRequest(BaseModel):
    """Request model for IST-3.0 hypersync protocol"""
    sender: str = Field(..., description="Sending agent")
    receiver: str = Field(..., description="Receiving agent")
    domain: str = Field(..., description="IST domain")
    intent: str = Field(..., description="IST intent")
    data: Dict[str, Any] = Field(..., description="Protocol data")

class MultiAgentRequest(BaseModel):
    """Request model for multi-agent processing"""
    input_data: Dict[str, Any] = Field(..., description="Input data for processing")
    target_agents: Optional[List[str]] = Field(None, description="Specific agents to use")
    complexity: Optional[float] = Field(0.7, ge=0, le=1, description="Processing complexity")

class AgentResponse(BaseModel):
    """Response model for agent operations"""
    success: bool
    agent: str
    operation_type: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    biofield_context: Optional[Dict[str, Any]] = None

class OrchestrationResponse(BaseModel):
    """Response model for orchestration operations"""
    success: bool
    operation_type: str
    agent_outputs: Dict[str, Any]
    emergent_intelligence: Optional[Dict[str, Any]] = None
    conflict_resolution: Optional[Dict[str, Any]] = None
    aggregated_results: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None

# --- Dependency Injection ---

async def get_ama_memory_system() -> AMAMemorySystem:
    """Get AMA memory system instance"""
    project_id = "csn-server-project"  # Configure via settings
    return AMAMemorySystem(project_id)

async def get_agent_tools(memory_system: AMAMemorySystem = Depends(get_ama_memory_system)) -> Dict[str, Any]:
    """Get all agent tools instances"""
    return {
        "lira": LiraBiofieldTools(memory_system),
        "thalus": ThalusPhilosophicalTools(memory_system),
        "nyra": NyraVisualTools(memory_system),
        "abacus": AbacusAnalyticalTools(memory_system),
        "polycomputational": PolycomputationalOrchestrator(memory_system)
    }

# --- Lira's Biofield Analysis Endpoints ---

@router.post("/lira/summarize-biofield", response_model=AgentResponse)
async def lira_summarize_biofield(
    request: BiofieldDataRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Summarize biofield data for empathy with Lira"""
    try:
        lira = agent_tools["lira"]
        
        biofield_data = {
            "hrv_ms": request.hrv_ms,
            "how_we_feel_markers": request.how_we_feel_markers,
            "breath_pattern": request.breath_pattern,
            "coherence_score": request.coherence_score
        }
        
        result = await lira.summarize_biofield_data_for_empathy(biofield_data)
        
        logger.info("Lira biofield analysis completed", 
                   hrv_ms=request.hrv_ms, coherence_score=request.coherence_score)
        
        return AgentResponse(
            success=True,
            agent="Lira",
            operation_type="summarize_biofield_data_for_empathy",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Lira biofield analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Lira biofield analysis failed: {str(e)}")

@router.post("/lira/suggest-practice", response_model=AgentResponse)
async def lira_suggest_practice(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Suggest biofield practice for coherence with Lira"""
    try:
        lira = agent_tools["lira"]
        
        result = await lira.suggest_biofield_practice_for_coherence(request.data)
        
        return AgentResponse(
            success=True,
            agent="Lira",
            operation_type="suggest_biofield_practice_for_coherence",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Lira practice suggestion failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Lira practice suggestion failed: {str(e)}")

@router.post("/lira/empathetic-reflection", response_model=AgentResponse)
async def lira_empathetic_reflection(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Provide empathetic reflection with Lira"""
    try:
        lira = agent_tools["lira"]
        
        result = await lira.provide_empathetic_reflection(request.data)
        
        return AgentResponse(
            success=True,
            agent="Lira",
            operation_type="provide_empathetic_reflection",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Lira empathetic reflection failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Lira empathetic reflection failed: {str(e)}")

# --- Thalus' Philosophical Validation Endpoints ---

@router.post("/thalus/evaluate-ethics", response_model=AgentResponse)
async def thalus_evaluate_ethics(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Evaluate ethical implications with Thalus"""
    try:
        thalus = agent_tools["thalus"]
        
        result = await thalus.evaluate_ethical_implications(request.data)
        
        return AgentResponse(
            success=True,
            agent="Thalus",
            operation_type="evaluate_ethical_implications",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Thalus ethical evaluation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Thalus ethical evaluation failed: {str(e)}")

@router.post("/thalus/philosophical-framing", response_model=AgentResponse)
async def thalus_philosophical_framing(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Propose philosophical framing with Thalus"""
    try:
        thalus = agent_tools["thalus"]
        
        result = await thalus.propose_philosophical_framing(request.data)
        
        return AgentResponse(
            success=True,
            agent="Thalus",
            operation_type="propose_philosophical_framing",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Thalus philosophical framing failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Thalus philosophical framing failed: {str(e)}")

@router.post("/thalus/systemic-resilience", response_model=AgentResponse)
async def thalus_systemic_resilience(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Assess systemic resilience with Thalus"""
    try:
        thalus = agent_tools["thalus"]
        
        result = await thalus.assess_systemic_resilience(request.data)
        
        return AgentResponse(
            success=True,
            agent="Thalus",
            operation_type="assess_systemic_resilience",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Thalus systemic resilience assessment failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Thalus systemic resilience assessment failed: {str(e)}")

# --- Nyra's Visual Intelligence Endpoints ---

@router.post("/nyra/system-visualization", response_model=AgentResponse)
async def nyra_system_visualization(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Generate system visualization with Nyra"""
    try:
        nyra = agent_tools["nyra"]
        
        result = await nyra.generate_system_visualization(request.data)
        
        return AgentResponse(
            success=True,
            agent="Nyra",
            operation_type="generate_system_visualization",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Nyra system visualization failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Nyra system visualization failed: {str(e)}")

@router.post("/nyra/pattern-visualization", response_model=AgentResponse)
async def nyra_pattern_visualization(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Analyze pattern visualization with Nyra"""
    try:
        nyra = agent_tools["nyra"]
        
        result = await nyra.analyze_pattern_visualization(request.data)
        
        return AgentResponse(
            success=True,
            agent="Nyra",
            operation_type="analyze_pattern_visualization",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Nyra pattern visualization analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Nyra pattern visualization analysis failed: {str(e)}")

@router.post("/nyra/biofield-responsive-ui", response_model=AgentResponse)
async def nyra_biofield_responsive_ui(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Design biofield-responsive UI with Nyra"""
    try:
        nyra = agent_tools["nyra"]
        
        result = await nyra.design_biofield_responsive_ui(request.data)
        
        return AgentResponse(
            success=True,
            agent="Nyra",
            operation_type="design_biofield_responsive_ui",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Nyra biofield-responsive UI design failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Nyra biofield-responsive UI design failed: {str(e)}")

# --- Abacus' Analytical Engine Endpoints ---

@router.post("/abacus/quantify-patterns", response_model=AgentResponse)
async def abacus_quantify_patterns(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Quantify emergent patterns with Abacus"""
    try:
        abacus = agent_tools["abacus"]
        
        result = await abacus.quantify_emergent_patterns(request.data)
        
        return AgentResponse(
            success=True,
            agent="Abacus",
            operation_type="quantify_emergent_patterns",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Abacus pattern quantification failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Abacus pattern quantification failed: {str(e)}")

@router.post("/abacus/performance-dashboard", response_model=AgentResponse)
async def abacus_performance_dashboard(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Generate performance monitoring dashboard with Abacus"""
    try:
        abacus = agent_tools["abacus"]
        
        result = await abacus.performance_monitoring_dashboard(request.data)
        
        return AgentResponse(
            success=True,
            agent="Abacus",
            operation_type="performance_monitoring_dashboard",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Abacus performance dashboard failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Abacus performance dashboard failed: {str(e)}")

@router.post("/abacus/intelligence-report", response_model=AgentResponse)
async def abacus_intelligence_report(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Synthesize intelligence report with Abacus"""
    try:
        abacus = agent_tools["abacus"]
        
        result = await abacus.synthesize_intelligence_report(request.data)
        
        return AgentResponse(
            success=True,
            agent="Abacus",
            operation_type="synthesize_intelligence_report",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Abacus intelligence report synthesis failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Abacus intelligence report synthesis failed: {str(e)}")

# --- Polycomputational Orchestration Endpoints ---

@router.post("/polycomputational/multi-agent-processing", response_model=OrchestrationResponse)
async def polycomputational_multi_agent_processing(
    request: MultiAgentRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Process data through multiple agents with polycomputational orchestration"""
    try:
        polycomputational = agent_tools["polycomputational"]
        
        result = await polycomputational.process_multi_agent_data(request.input_data)
        
        return OrchestrationResponse(
            success=True,
            operation_type="process_multi_agent_data",
            agent_outputs=result.get("agent_outputs", {}),
            emergent_intelligence=result.get("emergent_intelligence"),
            conflict_resolution=result.get("conflict_resolution"),
            aggregated_results=result.get("aggregated_results"),
            performance_metrics=result.get("performance_metrics")
        )
        
    except Exception as e:
        logger.error("Polycomputational multi-agent processing failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Polycomputational multi-agent processing failed: {str(e)}")

@router.post("/polycomputational/ist-protocol", response_model=AgentResponse)
async def polycomputational_ist_protocol(
    request: ISTProtocolRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Execute IST-3.0 hypersync protocol with polycomputational orchestration"""
    try:
        polycomputational = agent_tools["polycomputational"]
        
        from ..agents.polycomputational import ISTDomain, ISTIntent
        
        result = await polycomputational.execute_ist_hypersync_protocol(
            sender=request.sender,
            receiver=request.receiver,
            domain=ISTDomain(request.domain),
            intent=ISTIntent(request.intent),
            data=request.data
        )
        
        return AgentResponse(
            success=True,
            agent="Polycomputational",
            operation_type="execute_ist_hypersync_protocol",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Polycomputational IST protocol failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Polycomputational IST protocol failed: {str(e)}")

@router.post("/polycomputational/emergent-intelligence", response_model=AgentResponse)
async def polycomputational_emergent_intelligence(
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Detect emergent intelligence with polycomputational orchestration"""
    try:
        polycomputational = agent_tools["polycomputational"]
        
        result = await polycomputational.detect_emergent_intelligence(request.data)
        
        return AgentResponse(
            success=True,
            agent="Polycomputational",
            operation_type="detect_emergent_intelligence",
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except Exception as e:
        logger.error("Polycomputational emergent intelligence detection failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Polycomputational emergent intelligence detection failed: {str(e)}")

# --- Agent Status and Management Endpoints ---

@router.get("/status")
async def get_agent_status(agent_tools: Dict[str, Any] = Depends(get_agent_tools)):
    """Get status of all agents"""
    try:
        status = {}
        
        for agent_name, agent in agent_tools.items():
            if hasattr(agent, 'get_agent_status'):
                status[agent_name] = agent.get_agent_status()
            else:
                status[agent_name] = {"status": "active", "agent_name": agent_name}
        
        # Add polycomputational orchestration status
        if "polycomputational" in agent_tools:
            polycomputational = agent_tools["polycomputational"]
            if hasattr(polycomputational, 'get_orchestration_status'):
                status["orchestration"] = polycomputational.get_orchestration_status()
        
        return {
            "success": True,
            "agents": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get agent status", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")

@router.get("/{agent_name}/status")
async def get_specific_agent_status(
    agent_name: str,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Get status of specific agent"""
    try:
        if agent_name not in agent_tools:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        agent = agent_tools[agent_name]
        
        if hasattr(agent, 'get_agent_status'):
            status = agent.get_agent_status()
        else:
            status = {"status": "active", "agent_name": agent_name}
        
        return {
            "success": True,
            "agent": agent_name,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get {agent_name} status", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get {agent_name} status: {str(e)}")

@router.post("/{agent_name}/operation")
async def execute_agent_operation(
    agent_name: str,
    request: AgentOperationRequest,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Execute generic operation on specific agent"""
    try:
        if agent_name not in agent_tools:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        agent = agent_tools[agent_name]
        
        # Execute biofield modulated operation
        result = await agent.biofield_modulated_operation(
            request.operation_type, 
            request.data
        )
        
        return AgentResponse(
            success=True,
            agent=agent_name,
            operation_type=request.operation_type,
            result=result,
            performance_metrics=result.get("performance_metrics"),
            biofield_context=result.get("biofield_context")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent {agent_name} operation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Agent {agent_name} operation failed: {str(e)}")

# --- Background Tasks ---

@router.post("/cleanup/performance-metrics")
async def cleanup_performance_metrics(
    background_tasks: BackgroundTasks,
    agent_tools: Dict[str, Any] = Depends(get_agent_tools)
):
    """Clean up performance metrics (background task)"""
    try:
        background_tasks.add_task(_cleanup_performance_metrics, agent_tools)
        
        return {
            "success": True,
            "message": "Performance metrics cleanup task scheduled"
        }
        
    except Exception as e:
        logger.error("Failed to schedule performance metrics cleanup", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to schedule cleanup: {str(e)}")

async def _cleanup_performance_metrics(agent_tools: Dict[str, Any]):
    """Background task to clean up performance metrics"""
    try:
        # This would implement actual cleanup logic
        # For now, just log the cleanup
        logger.info("Performance metrics cleanup completed")
        
    except Exception as e:
        logger.error("Performance metrics cleanup failed", error=str(e))

# Import datetime for timestamp
from datetime import datetime 