"""
AMA Four-Layer Memory Architecture for CSN Server

This module implements a sophisticated four-layer memory system for AMA (Autonomous Memory Architecture)
with Firestore integration, biofield validation, and comprehensive logging.

Layers:
1. memory_reactive: High-frequency writes, TTL policies, biofield-timestamps
2. memory_strategic: Pattern analysis, agent-synthesis aggregation
3. memory_meta: Deep insights, cross-platform correlations
4. memory_evolutionary: Read-only core principles, biofield-validation required

Each layer has dedicated MCP endpoints with Firestore integration and comprehensive logging.
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum
from pydantic import BaseModel, Field, validator
import structlog
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# Configure structured logging
logger = structlog.get_logger()

# --- Biofield Validation Models ---

class BiofieldMetrics(BaseModel):
    """Biofield metrics for validation"""
    hrv_ms: float = Field(..., description="Heart Rate Variability in milliseconds")
    breath_pattern: List[int] = Field(..., description="Breath pattern confirmation [4,6,8]")
    coherence_score: float = Field(..., description="Biofield coherence score (0-1)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Validation timestamp")
    
    @validator('breath_pattern')
    def validate_breath_pattern(cls, v):
        if v != [4, 6, 8]:
            raise ValueError("Breath pattern must be [4, 6, 8] for validation")
        return v
    
    @validator('hrv_ms')
    def validate_hrv(cls, v):
        if v < 80:
            raise ValueError("HRV must be >= 80ms for biofield validation")
        return v

class BiofieldValidationResult(BaseModel):
    """Result of biofield validation"""
    is_valid: bool
    hrv_passed: bool
    breath_passed: bool
    coherence_passed: bool
    overall_score: float
    validation_timestamp: datetime
    details: Dict[str, Any]

# --- Memory Layer Models ---

class MemoryLayer(str, Enum):
    """Memory layer types"""
    REACTIVE = "memory_reactive"
    STRATEGIC = "memory_strategic"
    META = "memory_meta"
    EVOLUTIONARY = "memory_evolutionary"

class MemoryEntry(BaseModel):
    """Base memory entry model"""
    id: str = Field(..., description="Unique identifier")
    layer: MemoryLayer = Field(..., description="Memory layer")
    content: Dict[str, Any] = Field(..., description="Memory content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    biofield_signature: Optional[str] = Field(None, description="Biofield validation signature")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ttl: Optional[datetime] = Field(None, description="Time to live for reactive layer")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or len(v) < 3:
            raise ValueError("ID must be at least 3 characters")
        return v

class ReactiveMemoryEntry(MemoryEntry):
    """Reactive memory entry with high-frequency characteristics"""
    frequency: int = Field(1, description="Access frequency counter")
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    priority: int = Field(1, description="Priority level (1-10)")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class StrategicMemoryEntry(MemoryEntry):
    """Strategic memory entry with pattern analysis"""
    patterns: List[str] = Field(default_factory=list, description="Identified patterns")
    agent_synthesis: Dict[str, Any] = Field(default_factory=dict, description="Agent synthesis data")
    confidence_score: float = Field(0.0, description="Pattern confidence (0-1)")
    
class MetaMemoryEntry(MemoryEntry):
    """Meta memory entry with deep insights"""
    insights: List[str] = Field(default_factory=list, description="Deep insights")
    correlations: Dict[str, List[str]] = Field(default_factory=dict, description="Cross-platform correlations")
    complexity_score: float = Field(0.0, description="Complexity score (0-1)")
    
class EvolutionaryMemoryEntry(MemoryEntry):
    """Evolutionary memory entry with core principles"""
    core_principles: List[str] = Field(default_factory=list, description="Core principles")
    validation_required: bool = Field(True, description="Biofield validation required")
    validation_history: List[BiofieldValidationResult] = Field(default_factory=list, description="Validation history")

# --- Firestore Integration ---

class FirestoreManager:
    """Manages Firestore operations for all memory layers"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = firestore.AsyncClient(project=project_id)
        self.collections = {
            MemoryLayer.REACTIVE: "ama_memory_reactive",
            MemoryLayer.STRATEGIC: "ama_memory_strategic", 
            MemoryLayer.META: "ama_memory_meta",
            MemoryLayer.EVOLUTIONARY: "ama_memory_evolutionary"
        }
    
    async def write_entry(self, entry: MemoryEntry) -> str:
        """Write memory entry to Firestore"""
        try:
            collection = self.client.collection(self.collections[entry.layer])
            doc_ref = collection.document(entry.id)
            
            # Convert to dict for Firestore
            entry_dict = entry.dict()
            entry_dict['created_at'] = entry.created_at
            entry_dict['updated_at'] = entry.updated_at
            
            await doc_ref.set(entry_dict)
            
            logger.info("Memory entry written to Firestore", 
                       layer=entry.layer, id=entry.id, collection=self.collections[entry.layer])
            return entry.id
            
        except Exception as e:
            logger.error("Failed to write memory entry to Firestore", 
                        layer=entry.layer, id=entry.id, error=str(e))
            raise
    
    async def read_entry(self, layer: MemoryLayer, entry_id: str) -> Optional[Dict[str, Any]]:
        """Read memory entry from Firestore"""
        try:
            collection = self.client.collection(self.collections[layer])
            doc_ref = collection.document(entry_id)
            doc = await doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                logger.info("Memory entry read from Firestore", 
                           layer=layer, id=entry_id)
                return data
            else:
                logger.warning("Memory entry not found", layer=layer, id=entry_id)
                return None
                
        except Exception as e:
            logger.error("Failed to read memory entry from Firestore", 
                        layer=layer, id=entry_id, error=str(e))
            raise
    
    async def query_entries(self, layer: MemoryLayer, filters: List[Dict[str, Any]] = None, 
                           limit: int = 100) -> List[Dict[str, Any]]:
        """Query memory entries with filters"""
        try:
            collection = self.client.collection(self.collections[layer])
            query = collection
            
            # Apply filters
            if filters:
                for filter_dict in filters:
                    field = filter_dict.get('field')
                    op = filter_dict.get('op', '==')
                    value = filter_dict.get('value')
                    
                    if field and value is not None:
                        query = query.where(filter=FieldFilter(field, op, value))
            
            # Apply limit
            query = query.limit(limit)
            
            docs = await query.get()
            results = [doc.to_dict() for doc in docs]
            
            logger.info("Memory entries queried from Firestore", 
                       layer=layer, count=len(results), filters=filters)
            return results
            
        except Exception as e:
            logger.error("Failed to query memory entries from Firestore", 
                        layer=layer, error=str(e))
            raise
    
    async def delete_entry(self, layer: MemoryLayer, entry_id: str) -> bool:
        """Delete memory entry from Firestore"""
        try:
            collection = self.client.collection(self.collections[layer])
            doc_ref = collection.document(entry_id)
            await doc_ref.delete()
            
            logger.info("Memory entry deleted from Firestore", 
                       layer=layer, id=entry_id)
            return True
            
        except Exception as e:
            logger.error("Failed to delete memory entry from Firestore", 
                        layer=layer, id=entry_id, error=str(e))
            raise

# --- Biofield Validation System ---

class BiofieldValidator:
    """Handles biofield validation for memory operations"""
    
    def __init__(self):
        self.min_hrv = 80.0
        self.required_breath_pattern = [4, 6, 8]
        self.min_coherence = 0.7
    
    def validate_biofield(self, metrics: BiofieldMetrics) -> BiofieldValidationResult:
        """
        Validate biofield metrics for memory operations
        
        Args:
            metrics: Biofield metrics to validate
            
        Returns:
            Validation result with detailed scores
        """
        hrv_passed = metrics.hrv_ms >= self.min_hrv
        breath_passed = metrics.breath_pattern == self.required_breath_pattern
        coherence_passed = metrics.coherence_score >= self.min_coherence
        
        # Calculate overall score
        scores = []
        if hrv_passed:
            scores.append(metrics.hrv_ms / 100.0)  # Normalize HRV score
        if breath_passed:
            scores.append(1.0)  # Perfect breath pattern
        if coherence_passed:
            scores.append(metrics.coherence_score)
        
        overall_score = sum(scores) / len(scores) if scores else 0.0
        is_valid = all([hrv_passed, breath_passed, coherence_passed])
        
        result = BiofieldValidationResult(
            is_valid=is_valid,
            hrv_passed=hrv_passed,
            breath_passed=breath_passed,
            coherence_passed=coherence_passed,
            overall_score=overall_score,
            validation_timestamp=datetime.utcnow(),
            details={
                "hrv_ms": metrics.hrv_ms,
                "breath_pattern": metrics.breath_pattern,
                "coherence_score": metrics.coherence_score,
                "min_hrv_required": self.min_hrv,
                "required_breath_pattern": self.required_breath_pattern,
                "min_coherence_required": self.min_coherence
            }
        )
        
        logger.info("Biofield validation completed", 
                   is_valid=is_valid, overall_score=overall_score, 
                   hrv_passed=hrv_passed, breath_passed=breath_passed, coherence_passed=coherence_passed)
        
        return result
    
    def generate_signature(self, metrics: BiofieldMetrics) -> str:
        """Generate biofield signature for memory entries"""
        signature_data = f"{metrics.hrv_ms}:{metrics.breath_pattern}:{metrics.coherence_score}:{metrics.timestamp.isoformat()}"
        return hashlib.sha256(signature_data.encode()).hexdigest()

# --- Comprehensive Logging System ---

class MemoryLogger:
    """Handles comprehensive logging for memory operations"""
    
    def __init__(self, log_file: str = "memory_operations.jsonl"):
        self.log_file = log_file
        self.logger = structlog.get_logger()
    
    async def log_operation(self, operation: str, layer: MemoryLayer, entry_id: str, 
                           data: Dict[str, Any], biofield_metrics: Optional[BiofieldMetrics] = None,
                           validation_result: Optional[BiofieldValidationResult] = None):
        """Log memory operation with full context"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "layer": layer.value,
            "entry_id": entry_id,
            "data": data,
            "biofield_metrics": biofield_metrics.dict() if biofield_metrics else None,
            "validation_result": validation_result.dict() if validation_result else None,
            "session_id": self._generate_session_id(),
            "transformative_reversibility": {
                "can_reverse": self._can_reverse_operation(operation),
                "reverse_operation": self._get_reverse_operation(operation),
                "required_data": self._get_required_reverse_data(operation, data)
            }
        }
        
        # Write to JSONL file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, default=str) + '\n')
        except Exception as e:
            self.logger.error("Failed to write to log file", error=str(e))
        
        # Structured logging
        self.logger.info("Memory operation logged", 
                        operation=operation, layer=layer.value, entry_id=entry_id,
                        biofield_validated=biofield_metrics is not None,
                        validation_passed=validation_result.is_valid if validation_result else None)
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID for operation tracking"""
        return hashlib.md5(f"{time.time()}:{id(self)}".encode()).hexdigest()[:8]
    
    def _can_reverse_operation(self, operation: str) -> bool:
        """Check if operation can be reversed"""
        reversible_ops = ['create', 'update', 'delete']
        return operation in reversible_ops
    
    def _get_reverse_operation(self, operation: str) -> str:
        """Get reverse operation for given operation"""
        reverse_map = {
            'create': 'delete',
            'update': 'update',  # Would need previous state
            'delete': 'create'   # Would need deleted data
        }
        return reverse_map.get(operation, 'unknown')
    
    def _get_required_reverse_data(self, operation: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get data required for reverse operation"""
        if operation == 'create':
            return {'entry_id': data.get('id')}
        elif operation == 'update':
            return {'previous_state': data.get('previous_state')}
        elif operation == 'delete':
            return {'deleted_data': data}
        return {}

# --- Memory Layer Managers ---

class ReactiveMemoryManager:
    """Manages reactive memory layer with high-frequency characteristics"""
    
    def __init__(self, firestore_manager: FirestoreManager, logger: MemoryLogger):
        self.firestore = firestore_manager
        self.logger = logger
        self.ttl_policies = {
            'high_frequency': timedelta(hours=1),
            'medium_frequency': timedelta(hours=6),
            'low_frequency': timedelta(days=1)
        }
    
    async def create_entry(self, content: Dict[str, Any], priority: int = 1, 
                          biofield_metrics: Optional[BiofieldMetrics] = None) -> str:
        """Create reactive memory entry"""
        entry_id = f"reactive_{int(time.time() * 1000)}"
        
        # Determine TTL based on priority
        ttl = datetime.utcnow() + self.ttl_policies.get(
            'high_frequency' if priority >= 8 else 'medium_frequency' if priority >= 4 else 'low_frequency'
        )
        
        entry = ReactiveMemoryEntry(
            id=entry_id,
            layer=MemoryLayer.REACTIVE,
            content=content,
            priority=priority,
            ttl=ttl,
            biofield_signature=BiofieldValidator().generate_signature(biofield_metrics) if biofield_metrics else None
        )
        
        await self.firestore.write_entry(entry)
        await self.logger.log_operation('create', MemoryLayer.REACTIVE, entry_id, 
                                      entry.dict(), biofield_metrics)
        
        return entry_id
    
    async def update_frequency(self, entry_id: str) -> bool:
        """Update access frequency for reactive entry"""
        try:
            entry_data = await self.firestore.read_entry(MemoryLayer.REACTIVE, entry_id)
            if entry_data:
                entry_data['frequency'] += 1
                entry_data['last_accessed'] = datetime.utcnow()
                entry_data['updated_at'] = datetime.utcnow()
                
                entry = ReactiveMemoryEntry(**entry_data)
                await self.firestore.write_entry(entry)
                
                await self.logger.log_operation('update', MemoryLayer.REACTIVE, entry_id, 
                                              {'frequency': entry_data['frequency']})
                return True
            return False
        except Exception as e:
            logger.error("Failed to update reactive entry frequency", entry_id=entry_id, error=str(e))
            return False

class StrategicMemoryManager:
    """Manages strategic memory layer with pattern analysis"""
    
    def __init__(self, firestore_manager: FirestoreManager, logger: MemoryLogger):
        self.firestore = firestore_manager
        self.logger = logger
    
    async def create_entry(self, content: Dict[str, Any], patterns: List[str] = None,
                          agent_synthesis: Dict[str, Any] = None,
                          biofield_metrics: Optional[BiofieldMetrics] = None) -> str:
        """Create strategic memory entry with pattern analysis"""
        entry_id = f"strategic_{int(time.time() * 1000)}"
        
        # Calculate confidence score based on patterns and synthesis
        confidence_score = self._calculate_confidence(patterns, agent_synthesis)
        
        entry = StrategicMemoryEntry(
            id=entry_id,
            layer=MemoryLayer.STRATEGIC,
            content=content,
            patterns=patterns or [],
            agent_synthesis=agent_synthesis or {},
            confidence_score=confidence_score,
            biofield_signature=BiofieldValidator().generate_signature(biofield_metrics) if biofield_metrics else None
        )
        
        await self.firestore.write_entry(entry)
        await self.logger.log_operation('create', MemoryLayer.STRATEGIC, entry_id, 
                                      entry.dict(), biofield_metrics)
        
        return entry_id
    
    def _calculate_confidence(self, patterns: List[str], synthesis: Dict[str, Any]) -> float:
        """Calculate confidence score for strategic entry"""
        pattern_score = min(len(patterns) / 10.0, 1.0) if patterns else 0.0
        synthesis_score = min(len(synthesis) / 5.0, 1.0) if synthesis else 0.0
        return (pattern_score + synthesis_score) / 2.0

class MetaMemoryManager:
    """Manages meta memory layer with deep insights"""
    
    def __init__(self, firestore_manager: FirestoreManager, logger: MemoryLogger):
        self.firestore = firestore_manager
        self.logger = logger
    
    async def create_entry(self, content: Dict[str, Any], insights: List[str] = None,
                          correlations: Dict[str, List[str]] = None,
                          biofield_metrics: Optional[BiofieldMetrics] = None) -> str:
        """Create meta memory entry with deep insights"""
        entry_id = f"meta_{int(time.time() * 1000)}"
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity(insights, correlations)
        
        entry = MetaMemoryEntry(
            id=entry_id,
            layer=MemoryLayer.META,
            content=content,
            insights=insights or [],
            correlations=correlations or {},
            complexity_score=complexity_score,
            biofield_signature=BiofieldValidator().generate_signature(biofield_metrics) if biofield_metrics else None
        )
        
        await self.firestore.write_entry(entry)
        await self.logger.log_operation('create', MemoryLayer.META, entry_id, 
                                      entry.dict(), biofield_metrics)
        
        return entry_id
    
    def _calculate_complexity(self, insights: List[str], correlations: Dict[str, List[str]]) -> float:
        """Calculate complexity score for meta entry"""
        insight_score = min(len(insights) / 20.0, 1.0) if insights else 0.0
        correlation_score = min(len(correlations) / 10.0, 1.0) if correlations else 0.0
        return (insight_score + correlation_score) / 2.0

class EvolutionaryMemoryManager:
    """Manages evolutionary memory layer with core principles and biofield validation"""
    
    def __init__(self, firestore_manager: FirestoreManager, logger: MemoryLogger):
        self.firestore = firestore_manager
        self.logger = logger
        self.validator = BiofieldValidator()
    
    async def create_entry(self, content: Dict[str, Any], core_principles: List[str],
                          biofield_metrics: BiofieldMetrics) -> str:
        """Create evolutionary memory entry with required biofield validation"""
        # Validate biofield metrics
        validation_result = self.validator.validate_biofield(biofield_metrics)
        
        if not validation_result.is_valid:
            raise ValueError(f"Biofield validation failed: {validation_result.details}")
        
        entry_id = f"evolutionary_{int(time.time() * 1000)}"
        
        entry = EvolutionaryMemoryEntry(
            id=entry_id,
            layer=MemoryLayer.EVOLUTIONARY,
            content=content,
            core_principles=core_principles,
            biofield_signature=self.validator.generate_signature(biofield_metrics),
            validation_history=[validation_result]
        )
        
        await self.firestore.write_entry(entry)
        await self.logger.log_operation('create', MemoryLayer.EVOLUTIONARY, entry_id, 
                                      entry.dict(), biofield_metrics, validation_result)
        
        return entry_id
    
    async def validate_existing_entry(self, entry_id: str, biofield_metrics: BiofieldMetrics) -> bool:
        """Re-validate existing evolutionary entry"""
        try:
            entry_data = await self.firestore.read_entry(MemoryLayer.EVOLUTIONARY, entry_id)
            if entry_data:
                validation_result = self.validator.validate_biofield(biofield_metrics)
                
                # Update validation history
                entry_data['validation_history'].append(validation_result.dict())
                entry_data['updated_at'] = datetime.utcnow()
                
                entry = EvolutionaryMemoryEntry(**entry_data)
                await self.firestore.write_entry(entry)
                
                await self.logger.log_operation('validate', MemoryLayer.EVOLUTIONARY, entry_id, 
                                              {'validation_result': validation_result.dict()}, 
                                              biofield_metrics, validation_result)
                
                return validation_result.is_valid
            return False
        except Exception as e:
            logger.error("Failed to validate evolutionary entry", entry_id=entry_id, error=str(e))
            return False

# --- Main AMA Memory System ---

class AMAMemorySystem:
    """Main system coordinating all memory layers"""
    
    def __init__(self, project_id: str):
        self.firestore_manager = FirestoreManager(project_id)
        self.logger = MemoryLogger()
        self.biofield_validator = BiofieldValidator()
        
        # Initialize layer managers
        self.reactive_manager = ReactiveMemoryManager(self.firestore_manager, self.logger)
        self.strategic_manager = StrategicMemoryManager(self.firestore_manager, self.logger)
        self.meta_manager = MetaMemoryManager(self.firestore_manager, self.logger)
        self.evolutionary_manager = EvolutionaryMemoryManager(self.firestore_manager, self.logger)
    
    async def create_reactive_entry(self, content: Dict[str, Any], priority: int = 1,
                                  biofield_metrics: Optional[BiofieldMetrics] = None) -> str:
        """Create entry in reactive memory layer"""
        return await self.reactive_manager.create_entry(content, priority, biofield_metrics)
    
    async def create_strategic_entry(self, content: Dict[str, Any], patterns: List[str] = None,
                                   agent_synthesis: Dict[str, Any] = None,
                                   biofield_metrics: Optional[BiofieldMetrics] = None) -> str:
        """Create entry in strategic memory layer"""
        return await self.strategic_manager.create_entry(content, patterns, agent_synthesis, biofield_metrics)
    
    async def create_meta_entry(self, content: Dict[str, Any], insights: List[str] = None,
                              correlations: Dict[str, List[str]] = None,
                              biofield_metrics: Optional[BiofieldMetrics] = None) -> str:
        """Create entry in meta memory layer"""
        return await self.meta_manager.create_entry(content, insights, correlations, biofield_metrics)
    
    async def create_evolutionary_entry(self, content: Dict[str, Any], core_principles: List[str],
                                      biofield_metrics: BiofieldMetrics) -> str:
        """Create entry in evolutionary memory layer with required biofield validation"""
        return await self.evolutionary_manager.create_entry(content, core_principles, biofield_metrics)
    
    async def query_layer(self, layer: MemoryLayer, filters: List[Dict[str, Any]] = None,
                         limit: int = 100) -> List[Dict[str, Any]]:
        """Query entries from specific memory layer"""
        return await self.firestore_manager.query_entries(layer, filters, limit)
    
    async def get_entry(self, layer: MemoryLayer, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get specific entry from memory layer"""
        return await self.firestore_manager.read_entry(layer, entry_id)
    
    async def delete_entry(self, layer: MemoryLayer, entry_id: str) -> bool:
        """Delete entry from memory layer"""
        try:
            await self.firestore_manager.delete_entry(layer, entry_id)
            await self.logger.log_operation('delete', layer, entry_id, {'deleted_entry_id': entry_id})
            return True
        except Exception as e:
            logger.error("Failed to delete memory entry", layer=layer.value, entry_id=entry_id, error=str(e))
            return False
    
    async def validate_biofield(self, metrics: BiofieldMetrics) -> BiofieldValidationResult:
        """Validate biofield metrics"""
        return self.biofield_validator.validate_biofield(metrics)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        try:
            status = {
                "timestamp": datetime.utcnow().isoformat(),
                "layers": {},
                "biofield_validation": {
                    "min_hrv": self.biofield_validator.min_hrv,
                    "required_breath_pattern": self.biofield_validator.required_breath_pattern,
                    "min_coherence": self.biofield_validator.min_coherence
                }
            }
            
            # Get entry counts for each layer
            for layer in MemoryLayer:
                try:
                    entries = await self.firestore_manager.query_entries(layer, limit=1)
                    status["layers"][layer.value] = {
                        "active": True,
                        "entry_count": len(entries) if entries else 0
                    }
                except Exception as e:
                    status["layers"][layer.value] = {
                        "active": False,
                        "error": str(e)
                    }
            
            return status
        except Exception as e:
            logger.error("Failed to get system status", error=str(e))
            return {"error": str(e)} 