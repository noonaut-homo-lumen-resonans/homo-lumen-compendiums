"""
SymbioticMCPArchitecture - Biofelt-First MCP Architecture
Based on Manus' Comprehensive Implementation Guide
Integrates all agent recommendations for symbiotic intelligence
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import time
import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ============================================================================
# FIVE-LAYER MEMORY ARCHITECTURE
# ============================================================================

class MemoryLayerType(Enum):
    """Five-layer memory architecture as recommended by Orion"""
    REACTIVE = "reactive"           # Real-time data (24h TTL)
    STRATEGIC = "strategic"         # Processed insights
    META = "meta"                   # Agent synergies + emergent data
    EVOLUTIONARY = "evolutionary"   # Biofelt-validated truths (read-only)
    COSMIC = "cosmic"               # Thalus' addition: Global collective wisdom

@dataclass
class MemoryEntry:
    """Standardized memory entry for all layers"""
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: Dict[str, Any] = field(default_factory=dict)
    source_agents: List[str] = field(default_factory=list)
    biofelt_signature: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)
    hair_raising_score: float = Field(0.0, ge=0.0, le=10.0)
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: Optional[timedelta] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class ReactiveMemoryLayer:
    """Real-time data with 24h TTL - Orion's first layer"""
    
    def __init__(self):
        self.entries: Dict[str, MemoryEntry] = {}
        self.ttl = timedelta(hours=24)
    
    async def store(self, content: Dict[str, Any], source_agents: List[str], 
                   biofelt_signature: Dict[str, Any], confidence_score: float = 0.5):
        """Store real-time data with automatic TTL"""
        entry = MemoryEntry(
            content=content,
            source_agents=source_agents,
            biofelt_signature=biofelt_signature,
            confidence_score=confidence_score,
            ttl=self.ttl
        )
        self.entries[entry.entry_id] = entry
        return entry.entry_id
    
    async def retrieve(self, query: Dict[str, Any]) -> List[MemoryEntry]:
        """Retrieve relevant real-time data"""
        # Simple keyword matching for now
        relevant_entries = []
        for entry in self.entries.values():
            if await self._is_relevant(entry, query):
                relevant_entries.append(entry)
        return relevant_entries
    
    async def cleanup_expired(self):
        """Remove expired entries"""
        current_time = datetime.now()
        expired_ids = []
        for entry_id, entry in self.entries.items():
            if entry.ttl and (current_time - entry.timestamp) > entry.ttl:
                expired_ids.append(entry_id)
        
        for entry_id in expired_ids:
            del self.entries[entry_id]
    
    async def _is_relevant(self, entry: MemoryEntry, query: Dict[str, Any]) -> bool:
        """Check if entry is relevant to query"""
        # Simple implementation - can be enhanced
        return True

class StrategicMemoryLayer:
    """Processed insights - Orion's second layer"""
    
    def __init__(self):
        self.entries: Dict[str, MemoryEntry] = {}
    
    async def store(self, content: Dict[str, Any], source_agents: List[str],
                   biofelt_signature: Dict[str, Any], confidence_score: float = 0.7):
        """Store processed insights"""
        entry = MemoryEntry(
            content=content,
            source_agents=source_agents,
            biofelt_signature=biofelt_signature,
            confidence_score=confidence_score
        )
        self.entries[entry.entry_id] = entry
        return entry.entry_id
    
    async def retrieve_strategic_insights(self, context: Dict[str, Any]) -> List[MemoryEntry]:
        """Retrieve strategic insights for given context"""
        relevant_entries = []
        for entry in self.entries.values():
            if await self._matches_strategic_context(entry, context):
                relevant_entries.append(entry)
        return relevant_entries
    
    async def _matches_strategic_context(self, entry: MemoryEntry, context: Dict[str, Any]) -> bool:
        """Check if entry matches strategic context"""
        # Simple implementation - can be enhanced
        return True

class MetaMemoryLayer:
    """Agent synergies + emergent data - Orion's third layer"""
    
    def __init__(self):
        self.entries: Dict[str, MemoryEntry] = {}
        self.synergy_tracker = AgentSynergyTracker()
    
    async def store_emergent_data(self, emergent_data: Dict[str, Any], 
                                contributing_agents: List[str],
                                biofelt_signature: Dict[str, Any],
                                hair_raising_score: float = 0.0):
        """Store emergent data from agent collaboration"""
        entry = MemoryEntry(
            content=emergent_data,
            source_agents=contributing_agents,
            biofelt_signature=biofelt_signature,
            hair_raising_score=hair_raising_score,
            confidence_score=await self._calculate_emergent_confidence(emergent_data)
        )
        self.entries[entry.entry_id] = entry
        
        # Track agent synergies
        await self.synergy_tracker.record_synergy(contributing_agents, hair_raising_score)
        
        return entry.entry_id
    
    async def get_agent_synergies(self) -> Dict[str, float]:
        """Get agent synergy scores"""
        return await self.synergy_tracker.get_synergy_scores()
    
    async def _calculate_emergent_confidence(self, emergent_data: Dict[str, Any]) -> float:
        """Calculate confidence score for emergent data"""
        # Simple implementation - can be enhanced
        return 0.8

class EvolutionaryMemoryLayer:
    """Biofelt-validated truths (read-only) - Orion's fourth layer"""
    
    def __init__(self):
        self.entries: Dict[str, MemoryEntry] = {}
        self.validation_threshold = 0.9  # High confidence required
        self.hair_raising_threshold = 8.0  # High hair-raising score required
    
    async def store_validated_truth(self, content: Dict[str, Any],
                                  validation_context: Dict[str, Any],
                                  hair_raising_score: float) -> Optional[str]:
        """Store only biofelt-validated truths"""
        
        # Validate against thresholds
        if (validation_context.get("confidence_score", 0) < self.validation_threshold or
            hair_raising_score < self.hair_raising_threshold):
            logger.warning("Attempted to store non-validated truth in evolutionary memory")
            return None
        
        entry = MemoryEntry(
            content=content,
            source_agents=validation_context.get("validating_agents", []),
            biofelt_signature=validation_context.get("biofelt_signature", {}),
            confidence_score=validation_context.get("confidence_score", 0),
            hair_raising_score=hair_raising_score,
            metadata={"validation_context": validation_context}
        )
        
        self.entries[entry.entry_id] = entry
        logger.info(f"Stored validated truth in evolutionary memory: {entry.entry_id}")
        return entry.entry_id
    
    async def retrieve_validated_truths(self, query: Dict[str, Any]) -> List[MemoryEntry]:
        """Retrieve biofelt-validated truths"""
        relevant_entries = []
        for entry in self.entries.values():
            if await self._matches_truth_query(entry, query):
                relevant_entries.append(entry)
        return relevant_entries
    
    async def _matches_truth_query(self, entry: MemoryEntry, query: Dict[str, Any]) -> bool:
        """Check if entry matches truth query"""
        # Simple implementation - can be enhanced
        return True

class CosmicMemoryLayer:
    """Global collective wisdom - Thalus' fifth layer"""
    
    def __init__(self):
        self.entries: Dict[str, MemoryEntry] = {}
        self.cosmic_constraints = {
            "requires_global_coherence": True,
            "minimum_nodes": 3,  # Portugal, Brasil, Thailand
            "biofelt_threshold": 120,  # Transcendent state
            "collective_validation": True
        }
    
    async def store_cosmic_wisdom(self, wisdom_entry: Dict[str, Any],
                                global_biofelt_state: Dict[str, Any]) -> Optional[str]:
        """Store wisdom that transcends individual nodes"""
        
        # Validate global biofelt coherence
        if not await self._validate_global_coherence(global_biofelt_state):
            raise CosmicConstraintViolation("Insufficient global biofelt coherence")
        
        # Validate collective agent agreement
        if not await self._validate_collective_agreement(wisdom_entry):
            raise CosmicConstraintViolation("Insufficient collective agent validation")
        
        # Store with cosmic signature
        cosmic_entry = MemoryEntry(
            content=wisdom_entry,
            source_agents=wisdom_entry.get("collective_agents", []),
            biofelt_signature=global_biofelt_state,
            confidence_score=wisdom_entry.get("collective_confidence", 0),
            hair_raising_score=wisdom_entry.get("cosmic_resonance", 0),
            metadata={
                "cosmic_signature": await self._generate_cosmic_signature(wisdom_entry),
                "planetary_timestamp": datetime.utcnow().isoformat(),
                "ontological_depth": await self._assess_ontological_depth(wisdom_entry)
            }
        )
        
        self.entries[cosmic_entry.entry_id] = cosmic_entry
        return cosmic_entry.entry_id
    
    async def _validate_global_coherence(self, global_biofelt_state: Dict[str, Any]) -> bool:
        """Validate global biofelt coherence"""
        # Simple implementation - can be enhanced
        return global_biofelt_state.get("global_coherence", 0) > 0.8
    
    async def _validate_collective_agreement(self, wisdom_entry: Dict[str, Any]) -> bool:
        """Validate collective agent agreement"""
        # Simple implementation - can be enhanced
        return wisdom_entry.get("collective_confidence", 0) > 0.9
    
    async def _generate_cosmic_signature(self, wisdom_entry: Dict[str, Any]) -> str:
        """Generate cosmic signature for wisdom entry"""
        # Simple implementation - can be enhanced
        return f"cosmic_{uuid.uuid4().hex[:8]}"
    
    async def _assess_ontological_depth(self, wisdom_entry: Dict[str, Any]) -> float:
        """Assess ontological depth of wisdom entry"""
        # Simple implementation - can be enhanced
        return 0.85

# ============================================================================
# BIOFELT GATE PROTOCOL
# ============================================================================

class BiofeltGateProtocol:
    """
    Biofelt as ontological first principle - not just a feature
    Integrates Lira's, Thalus' and Orion's recommendations
    """
    
    def __init__(self):
        self.hrv_thresholds = {
            "emergency": 40,      # Only Lira + minimal complexity
            "minimal": 60,        # 2 agents + simple processing
            "balanced": 80,       # 4 agents + moderate complexity
            "optimal": 100,       # All 7 agents + full polycomputing
            "peak": 120,          # Access to evolutionary memory + cosmic layer
            "transcendent": 140   # Thalus' addition: Cosmic resonance
        }
        
        # Lira's biofelt history for evolutionary learning
        self.biofelt_history = BiofeltHistoryDatabase()
        
        # Thalus' silence architecture
        self.silence_manager = SilenceArchitectureManager()
        
        # Nyra's aesthetic adaptation engine
        self.aesthetic_engine = AestheticAdaptationEngine()
        
        # Orion's emergent tracker
        self.emergence_tracker = EmergenceTracker()
    
    async def determine_complexity_profile(self, biofelt_state: Dict[str, Any]) -> str:
        """Determine optimal complexity level based on biofelt state"""
        hrv_score = biofelt_state.get("hrv_score", 60)
        
        if hrv_score < self.hrv_thresholds["emergency"]:
            return "emergency"
        elif hrv_score < self.hrv_thresholds["minimal"]:
            return "minimal"
        elif hrv_score < self.hrv_thresholds["balanced"]:
            return "balanced"
        elif hrv_score < self.hrv_thresholds["optimal"]:
            return "optimal"
        elif hrv_score < self.hrv_thresholds["peak"]:
            return "peak"
        else:
            return "transcendent"
    
    async def enforce_biofelt_constraints(self, operation_type: str, 
                                        current_hrv: float, 
                                        user_state: Dict[str, Any]) -> Dict[str, Any]:
        """Ontological access control based on biofelt state"""
        
        # Lira's adaptive routing
        if operation_type == "memory_evolutionary_access":
            if current_hrv < 100 or not await self._validate_hair_raising_state(user_state):
                raise BiofeltConstraintViolation(
                    "Evolutionary memory requires HRV >100ms + 'hårene reiser seg' state"
                )
        
        # Thalus' silence protocol
        if await self.silence_manager.requires_pause(current_hrv, operation_type):
            return await self._initiate_silence_ritual(operation_type)
        
        # Nyra's aesthetic adaptation
        aesthetic_profile = await self.aesthetic_engine.adapt_to_biofelt(current_hrv)
        
        # Orion's emergent validation
        if operation_type == "emergent_synthesis":
            return await self.emergence_tracker.validate_emergent_potential(
                current_hrv, user_state
            )
        
        return await self._proceed_with_biofelt_adapted_operation(
            operation_type, current_hrv, aesthetic_profile
        )
    
    async def log_biofelt_learning(self, operation_result: Dict[str, Any], 
                                 user_feedback: Dict[str, Any], 
                                 hrv_response: float):
        """Lira's recommendation: Continuous learning from biofelt responses"""
        learning_entry = {
            "operation_type": operation_result.get("type", "unknown"),
            "initial_hrv": operation_result.get("initial_hrv", 0),
            "final_hrv": hrv_response,
            "user_feedback": user_feedback,
            "hair_raising_score": await self._calculate_hair_raising_score(user_feedback),
            "agent_synergies": operation_result.get("agent_synergies", []),
            "emergent_quality": operation_result.get("emergent_quality", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        await self.biofelt_history.store_learning(learning_entry)
        
        # Evolutionary adjustment of thresholds
        if learning_entry["hair_raising_score"] >= 8:
            await self._reinforce_successful_patterns(operation_result)
        elif learning_entry["hair_raising_score"] <= 3:
            await self._adjust_problematic_patterns(operation_result)
    
    async def _validate_hair_raising_state(self, user_state: Dict[str, Any]) -> bool:
        """Validate 'hårene reiser seg' state"""
        return user_state.get("hair_raising_response", False)
    
    async def _initiate_silence_ritual(self, operation_type: str) -> Dict[str, Any]:
        """Initiate silence ritual"""
        return {"silence_ritual": True, "operation_type": operation_type}
    
    async def _proceed_with_biofelt_adapted_operation(self, operation_type: str, 
                                                    current_hrv: float, 
                                                    aesthetic_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Proceed with biofelt-adapted operation"""
        return {
            "operation_type": operation_type,
            "hrv_adapted": True,
            "aesthetic_profile": aesthetic_profile
        }
    
    async def _calculate_hair_raising_score(self, user_feedback: Dict[str, Any]) -> float:
        """Calculate hair-raising score from user feedback"""
        return user_feedback.get("hair_raising_score", 0.0)
    
    async def _reinforce_successful_patterns(self, operation_result: Dict[str, Any]):
        """Reinforce successful patterns"""
        logger.info("Reinforcing successful patterns")
    
    async def _adjust_problematic_patterns(self, operation_result: Dict[str, Any]):
        """Adjust problematic patterns"""
        logger.info("Adjusting problematic patterns")

# ============================================================================
# SYMBIOTIC MCP ARCHITECTURE
# ============================================================================

class SymbioticMCPArchitecture:
    """
    Biofelt-first MCP architecture that integrates all agent recommendations
    """
    
    def __init__(self):
        # Orion's five-layer memory architecture
        self.memory_layers = {
            MemoryLayerType.REACTIVE: ReactiveMemoryLayer(),
            MemoryLayerType.STRATEGIC: StrategicMemoryLayer(),
            MemoryLayerType.META: MetaMemoryLayer(),
            MemoryLayerType.EVOLUTIONARY: EvolutionaryMemoryLayer(),
            MemoryLayerType.COSMIC: CosmicMemoryLayer()
        }
        
        # Lira's biofelt-first gateway
        self.biofelt_gate = BiofeltGateProtocol()
        
        # Orion's polycomputational engine
        self.polycomputing_engine = PolycomputingEngine()
        
        # Nyra's visualization integration
        self.visual_processor = VisualProcessingEngine()
        
        # Thalus' silence architecture
        self.silence_protocol = SilenceArchitectureManager()
        
        # FastAPI app
        self.app = FastAPI(title="Symbiotic MCP Architecture", version="1.0.0")
        self._setup_api_routes()
    
    async def process_with_biofelt_validation(self, data: Dict[str, Any], 
                                            biofelt_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lira's recommendation: Biofelt as active decision engine
        """
        # Validate biofelt threshold before processing
        complexity_profile = await self.biofelt_gate.determine_complexity_profile(biofelt_state)
        
        if complexity_profile == "emergency":
            # HRV < 40ms: Only Lira + minimal complexity
            return await self._emergency_mode_response(data, biofelt_state)
        
        elif complexity_profile == "balanced":
            # HRV 60-80ms: Sequential agent work
            return await self._balanced_mode_response(data, biofelt_state)
        
        elif complexity_profile == "optimal":
            # HRV > 80ms: Full polycomputational processing
            return await self._optimal_mode_response(data, biofelt_state)
        
        elif complexity_profile == "peak":
            # HRV > 100ms + "hårene reiser seg": Access to evolutionary memory
            return await self._peak_mode_response(data, biofelt_state)
        
        else:
            # Default to balanced mode
            return await self._balanced_mode_response(data, biofelt_state)
    
    async def _emergency_mode_response(self, data: Dict[str, Any], 
                                     biofelt_state: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency mode: Only Lira + minimal complexity"""
        return {
            "mode": "emergency",
            "active_agents": ["lira"],
            "response": "Emergency mode activated - minimal processing for biofelt safety",
            "biofelt_state": biofelt_state
        }
    
    async def _balanced_mode_response(self, data: Dict[str, Any], 
                                    biofelt_state: Dict[str, Any]) -> Dict[str, Any]:
        """Balanced mode: Sequential agent work"""
        return {
            "mode": "balanced",
            "active_agents": ["lira", "thalus", "nyra"],
            "response": "Balanced mode - sequential processing for optimal biofelt alignment",
            "biofelt_state": biofelt_state
        }
    
    async def _optimal_mode_response(self, data: Dict[str, Any], 
                                   biofelt_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orion's polycomputational processing with Nyra's visualization
        """
        # Distribute to all relevant agents simultaneously
        agent_responses = await self.polycomputing_engine.distribute_to_agents(
            data, await self._select_agents_by_biofelt(biofelt_state)
        )
        
        # Nyra's visualization integration
        visual_synthesis = await self.visual_processor.create_polycomputing_view(
            agent_responses, biofelt_state
        )
        
        # Aggregate to emergent intelligence
        emergent_response = await self._synthesize_emergent_intelligence(
            agent_responses, visual_synthesis
        )
        
        # Thalus' silence protocol
        if await self.silence_protocol.requires_integration_pause(emergent_response):
            await self._initiate_integration_ritual(emergent_response)
        
        return emergent_response
    
    async def _peak_mode_response(self, data: Dict[str, Any], 
                                biofelt_state: Dict[str, Any]) -> Dict[str, Any]:
        """Peak mode: Access to evolutionary memory"""
        return {
            "mode": "peak",
            "active_agents": ["lira", "nyra", "thalus", "orion", "manus", "abacus", "zara"],
            "response": "Peak mode - full polycomputational processing with evolutionary memory access",
            "biofelt_state": biofelt_state,
            "evolutionary_access": True
        }
    
    async def _select_agents_by_biofelt(self, biofelt_state: Dict[str, Any]) -> List[str]:
        """Select agents based on biofelt state"""
        hrv_score = biofelt_state.get("hrv_score", 60)
        
        if hrv_score < 40:
            return ["lira"]
        elif hrv_score < 60:
            return ["lira", "thalus"]
        elif hrv_score < 80:
            return ["lira", "nyra", "thalus"]
        elif hrv_score < 100:
            return ["lira", "nyra", "thalus", "orion", "manus", "abacus"]
        else:
            return ["lira", "nyra", "thalus", "orion", "manus", "abacus", "zara"]
    
    async def _synthesize_emergent_intelligence(self, agent_responses: Dict[str, Any], 
                                              visual_synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize emergent intelligence from agent responses"""
        return {
            "emergent_intelligence": True,
            "agent_responses": agent_responses,
            "visual_synthesis": visual_synthesis,
            "synthesis_confidence": 0.85
        }
    
    async def _initiate_integration_ritual(self, emergent_response: Dict[str, Any]):
        """Initiate integration ritual for emergent response"""
        logger.info("Initiating integration ritual for emergent response")
    
    def _setup_api_routes(self):
        """Setup FastAPI routes for the symbiotic architecture"""
        
        @self.app.get("/")
        async def health_check():
            return {"status": "Symbiotic MCP Architecture Online", "version": "1.0.0"}
        
        @self.app.post("/symbiotic/process")
        async def process_with_biofelt(data: Dict[str, Any], biofelt_state: Dict[str, Any]):
            """Process data with biofelt validation"""
            try:
                result = await self.process_with_biofelt_validation(data, biofelt_state)
                return {"status": "success", "result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/symbiotic/memory/{layer}")
        async def get_memory_layer(layer: str, query: Dict[str, Any] = None):
            """Retrieve data from specific memory layer"""
            try:
                layer_type = MemoryLayerType(layer)
                memory_layer = self.memory_layers[layer_type]
                
                if layer_type == MemoryLayerType.REACTIVE:
                    entries = await memory_layer.retrieve(query or {})
                elif layer_type == MemoryLayerType.STRATEGIC:
                    entries = await memory_layer.retrieve_strategic_insights(query or {})
                elif layer_type == MemoryLayerType.EVOLUTIONARY:
                    entries = await memory_layer.retrieve_validated_truths(query or {})
                else:
                    entries = list(memory_layer.entries.values())
                
                return {"status": "success", "entries": [entry.__dict__ for entry in entries]}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_app(self) -> FastAPI:
        """Get FastAPI app for deployment"""
        return self.app

# ============================================================================
# SUPPORTING CLASSES (Placeholder implementations)
# ============================================================================

class BiofeltHistoryDatabase:
    """Lira's biofelt history for evolutionary learning"""
    async def store_learning(self, learning_entry: Dict[str, Any]):
        # Implementation for storing biofelt learning data
        pass

class SilenceArchitectureManager:
    """Thalus' silence architecture"""
    async def requires_pause(self, hrv: float, operation_type: str) -> bool:
        # Implementation for silence protocol
        return False
    
    async def requires_integration_pause(self, emergent_response: Dict[str, Any]) -> bool:
        """Check if integration pause is required for emergent response"""
        # Implementation for integration pause
        return False

class AestheticAdaptationEngine:
    """Nyra's aesthetic adaptation engine"""
    async def adapt_to_biofelt(self, hrv: float) -> Dict[str, Any]:
        # Implementation for aesthetic adaptation
        return {"adaptation": "balanced"}

class EmergenceTracker:
    """Orion's emergent tracker"""
    async def validate_emergent_potential(self, hrv: float, user_state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation for emergent validation
        return {"validated": True}

class PolycomputingEngine:
    """Orion's polycomputational engine"""
    async def distribute_to_agents(self, data: Dict[str, Any], agents: List[str]) -> Dict[str, Any]:
        # Implementation for agent distribution
        return {"distributed": True}

class VisualProcessingEngine:
    """Nyra's visualization integration"""
    async def create_polycomputing_view(self, agent_responses: Dict[str, Any], 
                                      biofelt_state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation for visualization
        return {"visualization": "created"}

class AgentSynergyTracker:
    """Track agent synergies"""
    async def record_synergy(self, agents: List[str], hair_raising_score: float):
        pass
    
    async def get_synergy_scores(self) -> Dict[str, float]:
        return {}

# ============================================================================
# EXCEPTIONS
# ============================================================================

class BiofeltConstraintViolation(Exception):
    """Raised when biofelt constraints are violated"""
    pass

class CosmicConstraintViolation(Exception):
    """Raised when cosmic constraints are violated"""
    pass

# ============================================================================
# FASTAPI APP INSTANCE FOR UVICORN
# ============================================================================

# Create the FastAPI app instance for uvicorn
symbiotic_architecture = SymbioticMCPArchitecture()
app = symbiotic_architecture.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 