"""
CSN Server - Main FastAPI Application with Multi-Platform Agent Coordination

Integrates AMA four-layer memory architecture with multi-platform agent coordination:
- AMA Memory System (reactive, strategic, meta, evolutionary)
- Multi-Platform Agent Coordination Hub
- Biofield-responsive processing
- MCP endpoints for all agents
- Structured logging and monitoring
"""

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
from datetime import datetime
import structlog

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from routers.ama_memory_layers import AMAMemorySystem
from routers.ama_memory_endpoints import router as ama_memory_router
from platforms.agent_coordination_hub import AgentCoordinationHub, CoordinationMode
from routers.coordination_endpoints import router as coordination_router
from routers.lira_agent_endpoints import router as lira_agent_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Global instances
memory_system: Optional[AMAMemorySystem] = None
coordination_hub: Optional[AgentCoordinationHub] = None

class StartupConfig(BaseModel):
    """Configuration for startup parameters"""
    google_project_id: str = "csn-server-project"
    enable_biofield_validation: bool = True
    enable_multi_platform_coordination: bool = True
    log_level: str = "INFO"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global memory_system, coordination_hub
    
    # Startup
    logger.info("Starting CSN Server with Multi-Platform Agent Coordination")
    
    try:
        # Initialize AMA Memory System
        logger.info("Initializing AMA Memory System")
        memory_system = AMAMemorySystem()
        await memory_system.initialize()
        logger.info("AMA Memory System initialized successfully")
        
        # Initialize Agent Coordination Hub
        if app.state.config.enable_multi_platform_coordination:
            logger.info("Initializing Multi-Platform Agent Coordination Hub")
            coordination_hub = AgentCoordinationHub(memory_system, app.state.config.google_project_id)
            
            if await coordination_hub.initialize():
                logger.info("Agent Coordination Hub initialized successfully", 
                           agent_count=len(coordination_hub.agents))
            else:
                logger.warning("Agent Coordination Hub initialization failed, continuing without multi-platform coordination")
                coordination_hub = None
        
        # Log system status
        await log_system_startup()
        
        logger.info("CSN Server startup completed successfully")
        
    except Exception as e:
        logger.error("Startup failed", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down CSN Server")
    
    try:
        if coordination_hub:
            logger.info("Shutting down Agent Coordination Hub")
            # Cleanup coordination hub resources
        
        if memory_system:
            logger.info("Shutting down AMA Memory System")
            # Cleanup memory system resources
        
        logger.info("CSN Server shutdown completed")
        
    except Exception as e:
        logger.error("Shutdown error", error=str(e))

# Create FastAPI app
app = FastAPI(
    title="CSN Server - Multi-Platform Agent Coordination",
    description="Advanced AI coordination system with AMA memory architecture and biofield-responsive processing",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with structured logging"""
    start_time = time.time()
    
    # Log request
    logger.info("Request started",
                method=request.method,
                url=str(request.url),
                client_ip=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"))
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info("Request completed",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                process_time=process_time)
    
    return response

# Error handling middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with structured logging"""
    logger.error("Unhandled exception",
                method=request.method,
                url=str(request.url),
                error=str(exc),
                error_type=type(exc).__name__)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Include routers
app.include_router(ama_memory_router, prefix="/api/ama", tags=["AMA Memory"])
app.include_router(coordination_router, prefix="/api/coordination", tags=["Agent Coordination"])
app.include_router(lira_agent_router, prefix="/agent/lira", tags=["Lira Agent"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "service": "CSN Server - Multi-Platform Agent Coordination",
        "version": "2.0.0",
        "status": "active",
        "features": [
            "AMA Four-Layer Memory Architecture",
            "Multi-Platform Agent Coordination",
            "Biofield-Responsive Processing",
            "MCP Protocol Integration",
            "Structured Logging and Monitoring"
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "ama_memory": "/api/ama",
            "coordination": "/api/coordination",
            "lira_agent": "/agent/lira",
            "health": "/health",
            "status": "/status"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Check AMA Memory System
    if memory_system:
        try:
            ama_status = await memory_system.get_system_status()
            health_status["components"]["ama_memory"] = {
                "status": "healthy" if ama_status.get("status") == "active" else "unhealthy",
                "layers": ama_status.get("layer_status", {})
            }
        except Exception as e:
            health_status["components"]["ama_memory"] = {
                "status": "unhealthy",
                "error": str(e)
            }
    else:
        health_status["components"]["ama_memory"] = {"status": "not_initialized"}
    
    # Check Agent Coordination Hub
    if coordination_hub:
        try:
            coord_status = coordination_hub.get_coordination_status()
            health_status["components"]["coordination_hub"] = {
                "status": "healthy" if coord_status.get("status") == "active" else "unhealthy",
                "agent_count": coord_status.get("total_agents", 0),
                "success_rate": coord_status.get("performance_metrics", {}).get("success_rate", 0)
            }
        except Exception as e:
            health_status["components"]["coordination_hub"] = {
                "status": "unhealthy",
                "error": str(e)
            }
    else:
        health_status["components"]["coordination_hub"] = {"status": "not_initialized"}
    
    # Determine overall health
    all_healthy = all(
        comp.get("status") == "healthy" 
        for comp in health_status["components"].values()
    )
    
    if not all_healthy:
        health_status["status"] = "degraded"
    
    return health_status

# System status endpoint
@app.get("/status")
async def system_status():
    """Comprehensive system status endpoint"""
    status = {
        "service": "CSN Server - Multi-Platform Agent Coordination",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # AMA Memory System status
    if memory_system:
        try:
            ama_status = await memory_system.get_system_status()
            status["components"]["ama_memory"] = ama_status
        except Exception as e:
            status["components"]["ama_memory"] = {
                "status": "error",
                "error": str(e)
            }
    
    # Agent Coordination Hub status
    if coordination_hub:
        try:
            coord_status = coordination_hub.get_coordination_status()
            status["components"]["coordination_hub"] = coord_status
        except Exception as e:
            status["components"]["coordination_hub"] = {
                "status": "error",
                "error": str(e)
            }
    
    return status

# Multi-agent operation endpoint
@app.post("/api/coordination/execute")
async def execute_multi_agent_operation(
    operation_data: Dict[str, Any],
    coordination_mode: CoordinationMode = CoordinationMode.ADAPTIVE,
    complexity: float = 0.7
):
    """Execute operation across multiple agents with coordination"""
    
    if not coordination_hub:
        raise HTTPException(
            status_code=503,
            detail="Agent Coordination Hub not available"
        )
    
    try:
        result = await coordination_hub.execute_multi_agent_operation(
            operation_data=operation_data,
            coordination_mode=coordination_mode,
            complexity=complexity
        )
        
        return {
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Multi-agent operation failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Operation failed: {str(e)}"
        )

# Biofield validation endpoint
@app.post("/api/biofield/validate")
async def validate_biofield(biofield_data: Dict[str, Any]):
    """Validate biofield data and get processing recommendations"""
    
    if not memory_system:
        raise HTTPException(
            status_code=503,
            detail="AMA Memory System not available"
        )
    
    try:
        # Create biofield metrics
        from routers.ama_memory_layers import BiofieldMetrics
        
        biofield_metrics = BiofieldMetrics(
            hrv_ms=biofield_data.get("hrv_ms", 70.0),
            coherence_score=biofield_data.get("coherence_score", 0.5),
            breath_pattern=biofield_data.get("breath_pattern", "4-6-8"),
            timestamp=datetime.utcnow()
        )
        
        # Validate biofield
        validation_result = await memory_system.validate_biofield(biofield_metrics)
        
        # Get coordination recommendations
        coordination_recommendations = {}
        if coordination_hub:
            if biofield_metrics.hrv_ms >= 80:
                coordination_recommendations["mode"] = "parallel"
                coordination_recommendations["description"] = "High coherence - enable complex multi-platform processing"
            elif biofield_metrics.hrv_ms >= 60:
                coordination_recommendations["mode"] = "adaptive"
                coordination_recommendations["description"] = "Medium coherence - standard agent selection"
            else:
                coordination_recommendations["mode"] = "sequential"
                coordination_recommendations["description"] = "Low coherence - route primarily to Lira for empathetic support"
        
        return {
            "success": True,
            "validation_result": validation_result.dict(),
            "coordination_recommendations": coordination_recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Biofield validation failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )

async def log_system_startup():
    """Log comprehensive system startup information"""
    startup_info = {
        "startup_timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # AMA Memory System startup info
    if memory_system:
        try:
            ama_status = await memory_system.get_system_status()
            startup_info["components"]["ama_memory"] = {
                "status": ama_status.get("status"),
                "layer_count": len(ama_status.get("layer_status", {})),
                "total_entries": ama_status.get("total_entries", 0)
            }
        except Exception as e:
            startup_info["components"]["ama_memory"] = {"error": str(e)}
    
    # Agent Coordination Hub startup info
    if coordination_hub:
        try:
            coord_status = coordination_hub.get_coordination_status()
            startup_info["components"]["coordination_hub"] = {
                "status": coord_status.get("status"),
                "agent_count": coord_status.get("total_agents", 0),
                "available_agents": coord_status.get("available_agents", [])
            }
        except Exception as e:
            startup_info["components"]["coordination_hub"] = {"error": str(e)}
    
    logger.info("System startup completed", startup_info=startup_info)

# Store configuration in app state
@app.on_event("startup")
async def store_config():
    """Store configuration in app state"""
    app.state.config = StartupConfig()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main_fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 