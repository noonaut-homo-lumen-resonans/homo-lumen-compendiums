"""
AMA Memory Layer MCP Endpoints for CSN Server

This module provides FastAPI router endpoints for the AMA four-layer memory system,
including comprehensive MCP endpoints for each memory layer with biofield validation
and Firestore integration.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import structlog
import asyncio

from .ama_memory_layers import (
    AMAMemorySystem, BiofieldMetrics, MemoryLayer, BiofieldValidationResult,
    ReactiveMemoryEntry, StrategicMemoryEntry, MetaMemoryEntry, EvolutionaryMemoryEntry
)

# Configure logging
logger = structlog.get_logger()

# Create router
router = APIRouter(prefix="/ama-memory", tags=["AMA Memory Layers"])

# --- Request/Response Models ---

class BiofieldMetricsRequest(BaseModel):
    """Request model for biofield metrics"""
    hrv_ms: float = Field(..., ge=0, description="Heart Rate Variability in milliseconds")
    breath_pattern: List[int] = Field(..., description="Breath pattern [4,6,8]")
    coherence_score: float = Field(..., ge=0, le=1, description="Biofield coherence score")

class ReactiveMemoryRequest(BaseModel):
    """Request model for reactive memory creation"""
    content: Dict[str, Any] = Field(..., description="Memory content")
    priority: int = Field(1, ge=1, le=10, description="Priority level (1-10)")
    biofield_metrics: Optional[BiofieldMetricsRequest] = Field(None, description="Biofield metrics")

class StrategicMemoryRequest(BaseModel):
    """Request model for strategic memory creation"""
    content: Dict[str, Any] = Field(..., description="Memory content")
    patterns: List[str] = Field(default_factory=list, description="Identified patterns")
    agent_synthesis: Dict[str, Any] = Field(default_factory=dict, description="Agent synthesis data")
    biofield_metrics: Optional[BiofieldMetricsRequest] = Field(None, description="Biofield metrics")

class MetaMemoryRequest(BaseModel):
    """Request model for meta memory creation"""
    content: Dict[str, Any] = Field(..., description="Memory content")
    insights: List[str] = Field(default_factory=list, description="Deep insights")
    correlations: Dict[str, List[str]] = Field(default_factory=dict, description="Cross-platform correlations")
    biofield_metrics: Optional[BiofieldMetricsRequest] = Field(None, description="Biofield metrics")

class EvolutionaryMemoryRequest(BaseModel):
    """Request model for evolutionary memory creation"""
    content: Dict[str, Any] = Field(..., description="Memory content")
    core_principles: List[str] = Field(..., description="Core principles")
    biofield_metrics: BiofieldMetricsRequest = Field(..., description="Required biofield metrics")

class MemoryQueryRequest(BaseModel):
    """Request model for memory queries"""
    filters: List[Dict[str, Any]] = Field(default_factory=list, description="Query filters")
    limit: int = Field(100, ge=1, le=1000, description="Query limit")

class MemoryResponse(BaseModel):
    """Response model for memory operations"""
    success: bool
    entry_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    message: str
    biofield_validation: Optional[Dict[str, Any]] = None

class SystemStatusResponse(BaseModel):
    """Response model for system status"""
    timestamp: str
    layers: Dict[str, Dict[str, Any]]
    biofield_validation: Dict[str, Any]
    overall_status: str

# --- Dependency Injection ---

async def get_ama_memory_system() -> AMAMemorySystem:
    """Get AMA memory system instance"""
    # In production, this would be configured via environment variables
    project_id = "csn-server-project"  # Configure via settings
    return AMAMemorySystem(project_id)

# --- Biofield Validation Endpoints ---

@router.post("/validate-biofield", response_model=Dict[str, Any])
async def validate_biofield(
    metrics: BiofieldMetricsRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """
    Validate biofield metrics for memory operations
    
    Validates HRV >= 80ms, breath pattern [4,6,8], and coherence score >= 0.7
    """
    try:
        biofield_metrics = BiofieldMetrics(
            hrv_ms=metrics.hrv_ms,
            breath_pattern=metrics.breath_pattern,
            coherence_score=metrics.coherence_score
        )
        
        validation_result = await memory_system.validate_biofield(biofield_metrics)
        
        logger.info("Biofield validation requested", 
                   hrv_ms=metrics.hrv_ms, breath_pattern=metrics.breath_pattern,
                   coherence_score=metrics.coherence_score, is_valid=validation_result.is_valid)
        
        return {
            "success": True,
            "validation_result": validation_result.dict(),
            "message": "Biofield validation completed"
        }
        
    except Exception as e:
        logger.error("Biofield validation failed", error=str(e))
        raise HTTPException(status_code=400, detail=f"Biofield validation failed: {str(e)}")

# --- Reactive Memory Layer Endpoints ---

@router.post("/reactive/create", response_model=MemoryResponse)
async def create_reactive_entry(
    request: ReactiveMemoryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """
    Create entry in reactive memory layer
    
    High-frequency writes with TTL policies and biofield-timestamps
    """
    try:
        biofield_metrics = None
        if request.biofield_metrics:
            biofield_metrics = BiofieldMetrics(
                hrv_ms=request.biofield_metrics.hrv_ms,
                breath_pattern=request.biofield_metrics.breath_pattern,
                coherence_score=request.biofield_metrics.coherence_score
            )
        
        entry_id = await memory_system.create_reactive_entry(
            content=request.content,
            priority=request.priority,
            biofield_metrics=biofield_metrics
        )
        
        logger.info("Reactive memory entry created", entry_id=entry_id, priority=request.priority)
        
        return MemoryResponse(
            success=True,
            entry_id=entry_id,
            message="Reactive memory entry created successfully"
        )
        
    except Exception as e:
        logger.error("Failed to create reactive memory entry", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create reactive memory entry: {str(e)}")

@router.get("/reactive/{entry_id}", response_model=MemoryResponse)
async def get_reactive_entry(
    entry_id: str,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Get reactive memory entry by ID"""
    try:
        entry_data = await memory_system.get_entry(MemoryLayer.REACTIVE, entry_id)
        
        if not entry_data:
            raise HTTPException(status_code=404, detail="Reactive memory entry not found")
        
        return MemoryResponse(
            success=True,
            data=entry_data,
            message="Reactive memory entry retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get reactive memory entry", entry_id=entry_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get reactive memory entry: {str(e)}")

@router.post("/reactive/{entry_id}/update-frequency")
async def update_reactive_frequency(
    entry_id: str,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Update access frequency for reactive memory entry"""
    try:
        success = await memory_system.reactive_manager.update_frequency(entry_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Reactive memory entry not found")
        
        return {"success": True, "message": "Frequency updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update reactive frequency", entry_id=entry_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to update frequency: {str(e)}")

@router.post("/reactive/query", response_model=Dict[str, Any])
async def query_reactive_entries(
    request: MemoryQueryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Query reactive memory entries with filters"""
    try:
        entries = await memory_system.query_layer(
            MemoryLayer.REACTIVE,
            filters=request.filters,
            limit=request.limit
        )
        
        return {
            "success": True,
            "entries": entries,
            "count": len(entries),
            "message": "Reactive memory entries queried successfully"
        }
        
    except Exception as e:
        logger.error("Failed to query reactive memory entries", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to query reactive memory entries: {str(e)}")

# --- Strategic Memory Layer Endpoints ---

@router.post("/strategic/create", response_model=MemoryResponse)
async def create_strategic_entry(
    request: StrategicMemoryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """
    Create entry in strategic memory layer
    
    Pattern analysis and agent-synthesis aggregation
    """
    try:
        biofield_metrics = None
        if request.biofield_metrics:
            biofield_metrics = BiofieldMetrics(
                hrv_ms=request.biofield_metrics.hrv_ms,
                breath_pattern=request.biofield_metrics.breath_pattern,
                coherence_score=request.biofield_metrics.coherence_score
            )
        
        entry_id = await memory_system.create_strategic_entry(
            content=request.content,
            patterns=request.patterns,
            agent_synthesis=request.agent_synthesis,
            biofield_metrics=biofield_metrics
        )
        
        logger.info("Strategic memory entry created", entry_id=entry_id, 
                   pattern_count=len(request.patterns))
        
        return MemoryResponse(
            success=True,
            entry_id=entry_id,
            message="Strategic memory entry created successfully"
        )
        
    except Exception as e:
        logger.error("Failed to create strategic memory entry", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create strategic memory entry: {str(e)}")

@router.get("/strategic/{entry_id}", response_model=MemoryResponse)
async def get_strategic_entry(
    entry_id: str,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Get strategic memory entry by ID"""
    try:
        entry_data = await memory_system.get_entry(MemoryLayer.STRATEGIC, entry_id)
        
        if not entry_data:
            raise HTTPException(status_code=404, detail="Strategic memory entry not found")
        
        return MemoryResponse(
            success=True,
            data=entry_data,
            message="Strategic memory entry retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get strategic memory entry", entry_id=entry_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get strategic memory entry: {str(e)}")

@router.post("/strategic/query", response_model=Dict[str, Any])
async def query_strategic_entries(
    request: MemoryQueryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Query strategic memory entries with filters"""
    try:
        entries = await memory_system.query_layer(
            MemoryLayer.STRATEGIC,
            filters=request.filters,
            limit=request.limit
        )
        
        return {
            "success": True,
            "entries": entries,
            "count": len(entries),
            "message": "Strategic memory entries queried successfully"
        }
        
    except Exception as e:
        logger.error("Failed to query strategic memory entries", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to query strategic memory entries: {str(e)}")

# --- Meta Memory Layer Endpoints ---

@router.post("/meta/create", response_model=MemoryResponse)
async def create_meta_entry(
    request: MetaMemoryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """
    Create entry in meta memory layer
    
    Deep insights and cross-platform correlations
    """
    try:
        biofield_metrics = None
        if request.biofield_metrics:
            biofield_metrics = BiofieldMetrics(
                hrv_ms=request.biofield_metrics.hrv_ms,
                breath_pattern=request.biofield_metrics.breath_pattern,
                coherence_score=request.biofield_metrics.coherence_score
            )
        
        entry_id = await memory_system.create_meta_entry(
            content=request.content,
            insights=request.insights,
            correlations=request.correlations,
            biofield_metrics=biofield_metrics
        )
        
        logger.info("Meta memory entry created", entry_id=entry_id, 
                   insight_count=len(request.insights), correlation_count=len(request.correlations))
        
        return MemoryResponse(
            success=True,
            entry_id=entry_id,
            message="Meta memory entry created successfully"
        )
        
    except Exception as e:
        logger.error("Failed to create meta memory entry", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create meta memory entry: {str(e)}")

@router.get("/meta/{entry_id}", response_model=MemoryResponse)
async def get_meta_entry(
    entry_id: str,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Get meta memory entry by ID"""
    try:
        entry_data = await memory_system.get_entry(MemoryLayer.META, entry_id)
        
        if not entry_data:
            raise HTTPException(status_code=404, detail="Meta memory entry not found")
        
        return MemoryResponse(
            success=True,
            data=entry_data,
            message="Meta memory entry retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get meta memory entry", entry_id=entry_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get meta memory entry: {str(e)}")

@router.post("/meta/query", response_model=Dict[str, Any])
async def query_meta_entries(
    request: MemoryQueryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Query meta memory entries with filters"""
    try:
        entries = await memory_system.query_layer(
            MemoryLayer.META,
            filters=request.filters,
            limit=request.limit
        )
        
        return {
            "success": True,
            "entries": entries,
            "count": len(entries),
            "message": "Meta memory entries queried successfully"
        }
        
    except Exception as e:
        logger.error("Failed to query meta memory entries", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to query meta memory entries: {str(e)}")

# --- Evolutionary Memory Layer Endpoints ---

@router.post("/evolutionary/create", response_model=MemoryResponse)
async def create_evolutionary_entry(
    request: EvolutionaryMemoryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """
    Create entry in evolutionary memory layer
    
    Read-only core principles with required biofield validation
    """
    try:
        biofield_metrics = BiofieldMetrics(
            hrv_ms=request.biofield_metrics.hrv_ms,
            breath_pattern=request.biofield_metrics.breath_pattern,
            coherence_score=request.biofield_metrics.coherence_score
        )
        
        # Validate biofield metrics
        validation_result = await memory_system.validate_biofield(biofield_metrics)
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Biofield validation failed: HRV={biofield_metrics.hrv_ms}ms, "
                       f"breath_pattern={biofield_metrics.breath_pattern}, "
                       f"coherence={biofield_metrics.coherence_score}"
            )
        
        entry_id = await memory_system.create_evolutionary_entry(
            content=request.content,
            core_principles=request.core_principles,
            biofield_metrics=biofield_metrics
        )
        
        logger.info("Evolutionary memory entry created", entry_id=entry_id, 
                   principle_count=len(request.core_principles), validation_passed=True)
        
        return MemoryResponse(
            success=True,
            entry_id=entry_id,
            biofield_validation=validation_result.dict(),
            message="Evolutionary memory entry created successfully with biofield validation"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create evolutionary memory entry", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create evolutionary memory entry: {str(e)}")

@router.get("/evolutionary/{entry_id}", response_model=MemoryResponse)
async def get_evolutionary_entry(
    entry_id: str,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Get evolutionary memory entry by ID"""
    try:
        entry_data = await memory_system.get_entry(MemoryLayer.EVOLUTIONARY, entry_id)
        
        if not entry_data:
            raise HTTPException(status_code=404, detail="Evolutionary memory entry not found")
        
        return MemoryResponse(
            success=True,
            data=entry_data,
            message="Evolutionary memory entry retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get evolutionary memory entry", entry_id=entry_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get evolutionary memory entry: {str(e)}")

@router.post("/evolutionary/{entry_id}/validate")
async def validate_evolutionary_entry(
    entry_id: str,
    metrics: BiofieldMetricsRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Re-validate existing evolutionary memory entry"""
    try:
        biofield_metrics = BiofieldMetrics(
            hrv_ms=metrics.hrv_ms,
            breath_pattern=metrics.breath_pattern,
            coherence_score=metrics.coherence_score
        )
        
        is_valid = await memory_system.evolutionary_manager.validate_existing_entry(
            entry_id, biofield_metrics
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail="Biofield validation failed for existing entry"
            )
        
        return {
            "success": True,
            "entry_id": entry_id,
            "message": "Evolutionary memory entry re-validated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to validate evolutionary entry", entry_id=entry_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to validate evolutionary entry: {str(e)}")

@router.post("/evolutionary/query", response_model=Dict[str, Any])
async def query_evolutionary_entries(
    request: MemoryQueryRequest,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Query evolutionary memory entries with filters"""
    try:
        entries = await memory_system.query_layer(
            MemoryLayer.EVOLUTIONARY,
            filters=request.filters,
            limit=request.limit
        )
        
        return {
            "success": True,
            "entries": entries,
            "count": len(entries),
            "message": "Evolutionary memory entries queried successfully"
        }
        
    except Exception as e:
        logger.error("Failed to query evolutionary memory entries", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to query evolutionary memory entries: {str(e)}")

# --- System Management Endpoints ---

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status(
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Get overall AMA memory system status"""
    try:
        status = await memory_system.get_system_status()
        
        # Determine overall status
        active_layers = sum(1 for layer in status["layers"].values() if layer.get("active", False))
        overall_status = "healthy" if active_layers == 4 else "degraded" if active_layers > 0 else "unhealthy"
        
        return SystemStatusResponse(
            timestamp=status["timestamp"],
            layers=status["layers"],
            biofield_validation=status["biofield_validation"],
            overall_status=overall_status
        )
        
    except Exception as e:
        logger.error("Failed to get system status", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")

@router.delete("/{layer}/{entry_id}")
async def delete_memory_entry(
    layer: str,
    entry_id: str,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Delete memory entry from specified layer"""
    try:
        # Map layer string to enum
        layer_map = {
            "reactive": MemoryLayer.REACTIVE,
            "strategic": MemoryLayer.STRATEGIC,
            "meta": MemoryLayer.META,
            "evolutionary": MemoryLayer.EVOLUTIONARY
        }
        
        if layer not in layer_map:
            raise HTTPException(status_code=400, detail=f"Invalid layer: {layer}")
        
        memory_layer = layer_map[layer]
        success = await memory_system.delete_entry(memory_layer, entry_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Memory entry not found in {layer} layer")
        
        return {"success": True, "message": f"Memory entry deleted from {layer} layer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete memory entry", layer=layer, entry_id=entry_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to delete memory entry: {str(e)}")

# --- Background Tasks ---

@router.post("/cleanup/expired-reactive")
async def cleanup_expired_reactive_entries(
    background_tasks: BackgroundTasks,
    memory_system: AMAMemorySystem = Depends(get_ama_memory_system)
):
    """Clean up expired reactive memory entries (background task)"""
    try:
        # This would be implemented as a background task
        # For now, we'll just return a success message
        background_tasks.add_task(_cleanup_expired_entries, memory_system)
        
        return {
            "success": True,
            "message": "Cleanup task scheduled for expired reactive entries"
        }
        
    except Exception as e:
        logger.error("Failed to schedule cleanup task", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to schedule cleanup: {str(e)}")

async def _cleanup_expired_entries(memory_system: AMAMemorySystem):
    """Background task to clean up expired entries"""
    try:
        # Query for expired reactive entries
        from datetime import datetime
        expired_filter = [{"field": "ttl", "op": "<=", "value": datetime.utcnow()}]
        
        expired_entries = await memory_system.query_layer(
            MemoryLayer.REACTIVE, filters=expired_filter, limit=1000
        )
        
        deleted_count = 0
        for entry in expired_entries:
            try:
                await memory_system.delete_entry(MemoryLayer.REACTIVE, entry["id"])
                deleted_count += 1
            except Exception as e:
                logger.error("Failed to delete expired entry", entry_id=entry["id"], error=str(e))
        
        logger.info("Cleanup completed", deleted_count=deleted_count)
        
    except Exception as e:
        logger.error("Cleanup task failed", error=str(e)) 