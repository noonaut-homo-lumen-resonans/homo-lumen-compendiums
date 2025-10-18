"""
Base Agent Class for CSN Server Agent-Specific MCP Tools

Provides common functionality and biofield integration for all agents.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import structlog

from ..routers.ama_memory_layers import (
    AMAMemorySystem, BiofieldMetrics, MemoryLayer, BiofieldValidationResult
)

logger = structlog.get_logger()

class BaseAgent(ABC):
    """Base class for all agent-specific MCP tools"""
    
    def __init__(self, memory_system: AMAMemorySystem, agent_name: str):
        self.memory_system = memory_system
        self.agent_name = agent_name
        self.logger = structlog.get_logger(agent=agent_name)
        
        # Agent-specific complexity adaptation
        self.base_complexity = 0.7
        self.min_complexity = 0.3
        self.max_complexity = 0.95
        
        # Performance tracking
        self.operation_count = 0
        self.total_processing_time = 0.0
        self.last_operation_time = None
    
    async def get_current_biofield(self) -> Optional[BiofieldMetrics]:
        """Get current biofield status from reactive memory"""
        try:
            # Query recent biofield data from reactive memory
            recent_biofield = await self.memory_system.query_layer(
                MemoryLayer.REACTIVE,
                filters=[{"field": "content.event_type", "op": "==", "value": "biofield_measurement"}],
                limit=1
            )
            
            if recent_biofield:
                data = recent_biofield[0].get("content", {})
                return BiofieldMetrics(
                    hrv_ms=data.get("hrv_ms", 70.0),
                    breath_pattern=data.get("breath_pattern", [4, 6, 8]),
                    coherence_score=data.get("coherence_score", 0.5)
                )
            
            return None
            
        except Exception as e:
            self.logger.error("Failed to get current biofield", error=str(e))
            return None
    
    def adapt_complexity_to_biofield(self, current_hrv: float) -> float:
        """Adapt agent complexity based on biofield state"""
        if current_hrv >= 80:  # High coherence
            complexity = min(self.max_complexity, self.base_complexity * 1.3)
        elif current_hrv >= 60:  # Medium coherence
            complexity = self.base_complexity
        else:  # Low coherence
            complexity = max(self.min_complexity, self.base_complexity * 0.7)
        
        self.logger.info("Complexity adapted", 
                        agent=self.agent_name, 
                        hrv=current_hrv, 
                        complexity=complexity)
        
        return complexity
    
    async def biofield_modulated_operation(self, operation_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute operation with biofield modulation"""
        start_time = time.time()
        
        try:
            # Get current biofield status
            current_biofield = await self.get_current_biofield()
            
            if not current_biofield:
                self.logger.warning("No biofield data available, using default processing")
                result = await self._execute_operation(operation_type, data, self.base_complexity)
            else:
                # Check for emergency pause conditions
                if current_biofield.hrv < 50 or current_biofield.coherence_score < 0.3:
                    self.logger.warning("Emergency pause triggered due to low biofield coherence")
                    return await self._suggest_pause_practice(current_biofield)
                
                # Adapt complexity based on biofield
                complexity = self.adapt_complexity_to_biofield(current_biofield.hrv_ms)
                
                # Execute operation with adapted complexity
                result = await self._execute_operation(operation_type, data, complexity)
                
                # Add biofield context to result
                result["biofield_context"] = {
                    "hrv_ms": current_biofield.hrv_ms,
                    "coherence_score": current_biofield.coherence_score,
                    "adapted_complexity": complexity,
                    "operation_type": operation_type
                }
            
            # Update performance metrics
            processing_time = time.time() - start_time
            self.operation_count += 1
            self.total_processing_time += processing_time
            self.last_operation_time = datetime.utcnow()
            
            result["performance_metrics"] = {
                "processing_time": processing_time,
                "agent": self.agent_name,
                "operation_count": self.operation_count,
                "avg_processing_time": self.total_processing_time / self.operation_count
            }
            
            return result
            
        except Exception as e:
            self.logger.error("Biofield modulated operation failed", 
                            operation_type=operation_type, error=str(e))
            raise
    
    @abstractmethod
    async def _execute_operation(self, operation_type: str, data: Dict[str, Any], complexity: float) -> Dict[str, Any]:
        """Execute the specific agent operation - to be implemented by subclasses"""
        pass
    
    async def _suggest_pause_practice(self, biofield: BiofieldMetrics) -> Dict[str, Any]:
        """Suggest pause practice when biofield coherence is low"""
        return {
            "operation_type": "pause_suggestion",
            "agent": self.agent_name,
            "status": "paused",
            "reason": "low_biofield_coherence",
            "biofield_metrics": {
                "hrv_ms": biofield.hrv_ms,
                "coherence_score": biofield.coherence_score
            },
            "suggestions": [
                "Take 5 deep breaths with 4-6-8 pattern",
                "Step away from screen for 2 minutes",
                "Practice grounding meditation",
                "Return when feeling more centered"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def log_agent_operation(self, operation: str, data: Dict[str, Any], result: Dict[str, Any]):
        """Log agent operation to strategic memory"""
        try:
            log_entry = {
                "agent": self.agent_name,
                "operation": operation,
                "input_data": data,
                "result": result,
                "timestamp": datetime.utcnow().isoformat(),
                "performance_metrics": result.get("performance_metrics", {})
            }
            
            await self.memory_system.create_strategic_entry(
                content=log_entry,
                patterns=[f"{self.agent_name}_{operation}"],
                agent_synthesis={
                    "agent": self.agent_name,
                    "confidence": result.get("confidence_score", 0.5),
                    "complexity_used": result.get("biofield_context", {}).get("adapted_complexity", 0.7)
                }
            )
            
        except Exception as e:
            self.logger.error("Failed to log agent operation", error=str(e))
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and performance metrics"""
        return {
            "agent_name": self.agent_name,
            "status": "active",
            "operation_count": self.operation_count,
            "total_processing_time": self.total_processing_time,
            "avg_processing_time": self.total_processing_time / max(self.operation_count, 1),
            "last_operation": self.last_operation_time.isoformat() if self.last_operation_time else None,
            "base_complexity": self.base_complexity,
            "complexity_range": [self.min_complexity, self.max_complexity]
        } 