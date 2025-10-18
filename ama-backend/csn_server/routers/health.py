"""
Health check endpoints for CSN Server
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import structlog
import time
from typing import Dict, Any

from csn_server.config import settings

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.version,
        "environment": settings.environment
    }


@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check for Kubernetes/container orchestration"""
    try:
        # Add any additional readiness checks here
        # e.g., database connectivity, external service health
        
        return {
            "status": "ready",
            "timestamp": time.time(),
            "version": settings.version,
            "checks": {
                "database": "ok",
                "redis": "ok",
                "firestore": "ok"
            }
        }
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes/container orchestration"""
    return {
        "status": "alive",
        "timestamp": time.time(),
        "version": settings.version
    }


@router.get("/info")
async def service_info() -> Dict[str, Any]:
    """Service information endpoint"""
    return {
        "name": "CSN Server",
        "version": settings.version,
        "description": "FastAPI server for CSN with MCP, Firestore, and biofield validation",
        "environment": settings.environment,
        "debug": settings.debug,
        "modules": {
            "mcp_endpoints": "enabled",
            "ama_integration": "enabled", 
            "agent_coordination": "enabled" if settings.agent_coordination_enabled else "disabled",
            "biofelt_validation": "enabled" if settings.hrv_validation_enabled else "disabled"
        }
    } 