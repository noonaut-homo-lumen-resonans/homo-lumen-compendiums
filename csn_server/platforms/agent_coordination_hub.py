"""
Agent Coordination Hub for Multi-Platform AI Integration

Central orchestration service that coordinates all platform agents with:
- Parallel processing across multiple AI platforms
- Biofield-responsive platform selection
- Load balancing and rate limit management
- Emergent intelligence detection
- Fallback and failover mechanisms
"""

import asyncio
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import structlog

from .base_platform_agent import PlatformType, AgentRole
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent
from .grok_agent import GrokAgent
from .deepseek_agent import DeepSeekAgent
from .claude_agent import ClaudeAgent

logger = structlog.get_logger()

class CoordinationMode(str, Enum):
    """Coordination modes for multi-agent processing"""
    PARALLEL = "parallel"  # All agents process simultaneously
    SEQUENTIAL = "sequential"  # Agents process in sequence
    ADAPTIVE = "adaptive"  # Biofield-responsive selection
    EMERGENCY = "emergency"  # Limited processing for low biofield

class AgentCoordinationHub:
    """Central hub for coordinating all platform agents"""
    
    def __init__(self, memory_system, google_project_id: str):
        self.memory_system = memory_system
        self.google_project_id = google_project_id
        
        # Initialize all platform agents
        self.agents = {}
        self.agent_roles = {
            AgentRole.LIRA: PlatformType.OPENAI,
            AgentRole.NYRA: PlatformType.GEMINI,
            AgentRole.THALUS: PlatformType.GROK,
            AgentRole.ZARA: PlatformType.DEEPSEEK,
            AgentRole.ORION: PlatformType.CLAUDE,
            AgentRole.ABACUS: PlatformType.CLAUDE
        }
        
        # Performance tracking
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.parallel_operations = 0
        self.adaptive_operations = 0
        
        # Load balancing state
        self.platform_availability = {}
        self.rate_limit_states = {}
        self.last_health_check = None
        
        # Biofield thresholds for coordination
        self.biofield_thresholds = {
            "high_coherence": 80,  # Enable complex multi-platform processing
            "medium_coherence": 60,  # Standard agent selection
            "low_coherence": 50,  # Route primarily to Lira
            "emergency_pause": 40  # Pause multi-platform processing
        }
    
    async def initialize(self) -> bool:
        """Initialize all platform agents"""
        try:
            logger.info("Initializing Agent Coordination Hub")
            
            # Initialize each platform agent
            for role, platform in self.agent_roles.items():
                agent = await self._create_agent(platform, role)
                if agent:
                    self.agents[role] = agent
                    logger.info("Agent initialized", role=role.value, platform=platform.value)
                else:
                    logger.warning("Failed to initialize agent", role=role.value, platform=platform.value)
            
            # Perform initial health check
            await self._perform_health_check()
            
            logger.info("Agent Coordination Hub initialized", 
                       agent_count=len(self.agents),
                       available_agents=list(self.agents.keys()))
            
            return len(self.agents) > 0
            
        except Exception as e:
            logger.error("Failed to initialize Agent Coordination Hub", error=str(e))
            return False
    
    async def _create_agent(self, platform: PlatformType, role: AgentRole):
        """Create platform-specific agent"""
        try:
            if platform == PlatformType.OPENAI:
                agent = OpenAIAgent(self.memory_system, self.google_project_id)
            elif platform == PlatformType.GEMINI:
                agent = GeminiAgent(self.memory_system, self.google_project_id)
            elif platform == PlatformType.GROK:
                agent = GrokAgent(self.memory_system, self.google_project_id)
            elif platform == PlatformType.DEEPSEEK:
                agent = DeepSeekAgent(self.memory_system, self.google_project_id)
            elif platform == PlatformType.CLAUDE:
                agent = ClaudeAgent(self.memory_system, self.google_project_id, role)
            else:
                logger.error("Unknown platform", platform=platform.value)
                return None
            
            # Initialize the agent
            if await agent.initialize():
                return agent
            else:
                logger.error("Agent initialization failed", platform=platform.value, role=role.value)
                return None
                
        except Exception as e:
            logger.error("Failed to create agent", platform=platform.value, role=role.value, error=str(e))
            return None
    
    async def execute_multi_agent_operation(self, operation_data: Dict[str, Any], 
                                          coordination_mode: CoordinationMode = CoordinationMode.ADAPTIVE,
                                          complexity: float = 0.7) -> Dict[str, Any]:
        """Execute operation across multiple agents based on coordination mode"""
        
        start_time = time.time()
        
        try:
            # Get current biofield status
            current_biofield = await self._get_current_biofield()
            
            # Check for emergency conditions
            if current_biofield and current_biofield.hrv_ms < self.biofield_thresholds["emergency_pause"]:
                return await self._handle_emergency_mode(operation_data, current_biofield)
            
            # Determine coordination mode based on biofield if adaptive
            if coordination_mode == CoordinationMode.ADAPTIVE:
                coordination_mode = self._determine_adaptive_mode(current_biofield)
            
            # Execute based on coordination mode
            if coordination_mode == CoordinationMode.PARALLEL:
                result = await self._execute_parallel_operation(operation_data, complexity)
            elif coordination_mode == CoordinationMode.SEQUENTIAL:
                result = await self._execute_sequential_operation(operation_data, complexity)
            elif coordination_mode == CoordinationMode.EMERGENCY:
                result = await self._execute_emergency_operation(operation_data, current_biofield)
            else:
                result = await self._execute_adaptive_operation(operation_data, current_biofield, complexity)
            
            # Update performance metrics
            processing_time = time.time() - start_time
            self._update_performance_metrics(processing_time, result.get("success", False), coordination_mode)
            
            # Add coordination context
            result["coordination_context"] = {
                "mode": coordination_mode.value,
                "biofield_hrv": current_biofield.hrv_ms if current_biofield else None,
                "processing_time": processing_time,
                "agent_count": len(result.get("agent_results", {})),
                "complexity_used": complexity
            }
            
            # Log coordination operation
            await self._log_coordination_operation(operation_data, result, coordination_mode)
            
            return result
            
        except Exception as e:
            logger.error("Multi-agent operation failed", error=str(e))
            return {
                "success": False,
                "error": "coordination_failed",
                "error_message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_parallel_operation(self, operation_data: Dict[str, Any], 
                                        complexity: float) -> Dict[str, Any]:
        """Execute operation across all available agents in parallel"""
        
        # Determine which agents should process the operation
        relevant_agents = self._determine_relevant_agents(operation_data, complexity)
        
        if not relevant_agents:
            return {
                "success": False,
                "error": "no_relevant_agents",
                "suggestion": "Check operation data and agent availability"
            }
        
        # Create tasks for parallel execution
        tasks = []
        for role in relevant_agents:
            if role in self.agents:
                task = self._create_agent_task(role, operation_data, complexity)
                tasks.append(task)
        
        # Execute tasks in parallel
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            agent_results = {}
            successful_agents = []
            failed_agents = []
            
            for i, result in enumerate(results):
                role = relevant_agents[i]
                if isinstance(result, Exception):
                    failed_agents.append(role)
                    agent_results[role.value] = {"error": str(result)}
                else:
                    successful_agents.append(role)
                    agent_results[role.value] = result
            
            # Detect emergent intelligence
            emergent_intelligence = await self._detect_emergent_intelligence(agent_results)
            
            return {
                "success": len(successful_agents) > 0,
                "coordination_mode": "parallel",
                "agent_results": agent_results,
                "successful_agents": [role.value for role in successful_agents],
                "failed_agents": [role.value for role in failed_agents],
                "emergent_intelligence": emergent_intelligence,
                "synthesis": await self._synthesize_results(agent_results, emergent_intelligence)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "parallel_execution_failed",
                "error_message": str(e)
            }
    
    async def _execute_sequential_operation(self, operation_data: Dict[str, Any], 
                                          complexity: float) -> Dict[str, Any]:
        """Execute operation across agents sequentially"""
        
        relevant_agents = self._determine_relevant_agents(operation_data, complexity)
        agent_results = {}
        
        for role in relevant_agents:
            if role in self.agents:
                try:
                    result = await self.agents[role].execute_mcp_function(
                        operation_data.get("function_name", "default"),
                        operation_data.get("data", {}),
                        complexity
                    )
                    agent_results[role.value] = result
                    
                    # If successful, consider stopping early
                    if result.get("success", False) and result.get("confidence_score", 0) > 0.8:
                        break
                        
                except Exception as e:
                    agent_results[role.value] = {"error": str(e)}
        
        return {
            "success": len(agent_results) > 0,
            "coordination_mode": "sequential",
            "agent_results": agent_results,
            "synthesis": await self._synthesize_results(agent_results, {})
        }
    
    async def _execute_adaptive_operation(self, operation_data: Dict[str, Any], 
                                        current_biofield, complexity: float) -> Dict[str, Any]:
        """Execute operation with biofield-responsive agent selection"""
        
        # Select agents based on biofield state
        if current_biofield.hrv_ms >= self.biofield_thresholds["high_coherence"]:
            # High coherence: use multiple agents
            selected_agents = self._determine_relevant_agents(operation_data, complexity)
        elif current_biofield.hrv_ms >= self.biofield_thresholds["medium_coherence"]:
            # Medium coherence: use 2-3 agents
            selected_agents = self._determine_relevant_agents(operation_data, complexity)[:3]
        else:
            # Low coherence: primarily use Lira for empathetic support
            selected_agents = [AgentRole.LIRA]
        
        # Execute with selected agents
        agent_results = {}
        for role in selected_agents:
            if role in self.agents:
                try:
                    result = await self.agents[role].execute_mcp_function(
                        operation_data.get("function_name", "default"),
                        operation_data.get("data", {}),
                        complexity
                    )
                    agent_results[role.value] = result
                except Exception as e:
                    agent_results[role.value] = {"error": str(e)}
        
        return {
            "success": len(agent_results) > 0,
            "coordination_mode": "adaptive",
            "biofield_hrv": current_biofield.hrv_ms if current_biofield else None,
            "selected_agents": [role.value for role in selected_agents],
            "agent_results": agent_results,
            "synthesis": await self._synthesize_results(agent_results, {})
        }
    
    async def _execute_emergency_operation(self, operation_data: Dict[str, Any], 
                                         current_biofield) -> Dict[str, Any]:
        """Execute operation in emergency mode (low biofield)"""
        
        # Only use Lira for empathetic support
        if AgentRole.LIRA in self.agents:
            try:
                result = await self.agents[AgentRole.LIRA].execute_mcp_function(
                    "provide_empathetic_reflection",
                    {"context_data": {"emergency_mode": True, "biofield_data": current_biofield.dict()}},
                    0.3  # Low complexity for emergency
                )
                
                return {
                    "success": True,
                    "coordination_mode": "emergency",
                    "biofield_hrv": current_biofield.hrv_ms,
                    "agent_results": {AgentRole.LIRA.value: result},
                    "emergency_suggestions": [
                        "Take 5 deep breaths with 4-6-8 pattern",
                        "Step away from screen for 2 minutes",
                        "Practice grounding meditation",
                        "Return when feeling more centered"
                    ]
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": "emergency_operation_failed",
                    "error_message": str(e)
                }
        
        return {
            "success": False,
            "error": "no_emergency_agent_available"
        }
    
    def _determine_adaptive_mode(self, current_biofield) -> CoordinationMode:
        """Determine coordination mode based on biofield state"""
        if not current_biofield:
            return CoordinationMode.ADAPTIVE
        
        if current_biofield.hrv_ms >= self.biofield_thresholds["high_coherence"]:
            return CoordinationMode.PARALLEL
        elif current_biofield.hrv_ms >= self.biofield_thresholds["medium_coherence"]:
            return CoordinationMode.ADAPTIVE
        elif current_biofield.hrv_ms >= self.biofield_thresholds["low_coherence"]:
            return CoordinationMode.SEQUENTIAL
        else:
            return CoordinationMode.EMERGENCY
    
    def _determine_relevant_agents(self, operation_data: Dict[str, Any], complexity: float) -> List[AgentRole]:
        """Determine which agents are relevant for the operation"""
        
        operation_type = operation_data.get("function_name", "").lower()
        data_content = str(operation_data.get("data", {})).lower()
        
        relevant_agents = []
        
        # Biofield and empathy operations
        if "biofield" in operation_type or "empathy" in operation_type or "biofield" in data_content:
            relevant_agents.append(AgentRole.LIRA)
        
        # Visual and pattern operations
        if "visual" in operation_type or "pattern" in operation_type or "visual" in data_content:
            relevant_agents.append(AgentRole.NYRA)
        
        # Philosophical and ethical operations
        if "ethical" in operation_type or "philosophical" in operation_type or "ethical" in data_content:
            relevant_agents.append(AgentRole.THALUS)
        
        # Creative and innovative operations
        if "creative" in operation_type or "innovative" in operation_type or "creative" in data_content:
            relevant_agents.append(AgentRole.ZARA)
        
        # Analytical and quantitative operations
        if "analytical" in operation_type or "quantify" in operation_type or "analytical" in data_content:
            relevant_agents.append(AgentRole.ABACUS)
        
        # Coordination and synthesis operations
        if "coordinate" in operation_type or "synthesize" in operation_type:
            relevant_agents.append(AgentRole.ORION)
        
        # If no specific agents identified, use all available for high complexity
        if not relevant_agents and complexity > 0.7:
            relevant_agents = list(self.agents.keys())
        
        # Ensure at least one agent is selected
        if not relevant_agents:
            relevant_agents = [AgentRole.LIRA]  # Default to empathetic support
        
        return relevant_agents
    
    async def _create_agent_task(self, role: AgentRole, operation_data: Dict[str, Any], 
                               complexity: float) -> asyncio.Task:
        """Create async task for agent operation"""
        
        return asyncio.create_task(
            self.agents[role].execute_mcp_function(
                operation_data.get("function_name", "default"),
                operation_data.get("data", {}),
                complexity
            )
        )
    
    async def _detect_emergent_intelligence(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Detect emergent intelligence from cross-agent outputs"""
        
        emergent_insights = []
        novelty_scores = []
        synergy_scores = []
        
        # Analyze cross-correlations
        successful_results = {k: v for k, v in agent_results.items() if v.get("success", False)}
        
        if len(successful_results) >= 2:
            # Calculate synergy score
            confidence_scores = [result.get("confidence_score", 0.5) for result in successful_results.values()]
            synergy_score = sum(confidence_scores) / len(confidence_scores)
            
            if synergy_score > 0.8:
                emergent_insights.append({
                    "type": "high_synergy",
                    "synergy_score": synergy_score,
                    "description": "High synergy detected between agent outputs"
                })
            
            # Look for novel insights
            for agent_name, result in successful_results.items():
                if "emergent" in str(result).lower() or "novel" in str(result).lower():
                    novelty_scores.append(0.8)
                    emergent_insights.append({
                        "type": "novel_insight",
                        "agent": agent_name,
                        "description": f"Novel insight detected from {agent_name}"
                    })
        
        return {
            "emergent_insights": emergent_insights,
            "novelty_scores": novelty_scores,
            "synergy_scores": synergy_scores,
            "detection_quality": "high" if len(emergent_insights) > 0 else "low"
        }
    
    async def _synthesize_results(self, agent_results: Dict[str, Any], 
                                emergent_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from multiple agents"""
        
        successful_results = {k: v for k, v in agent_results.items() if v.get("success", False)}
        
        if not successful_results:
            return {
                "synthesis_quality": "none",
                "overall_confidence": 0.0,
                "key_insights": []
            }
        
        # Calculate overall confidence
        confidence_scores = [result.get("confidence_score", 0.5) for result in successful_results.values()]
        overall_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Extract key insights
        key_insights = []
        for agent_name, result in successful_results.items():
            if "insights" in result:
                key_insights.extend(result["insights"])
            elif "empathetic_insights" in result:
                key_insights.extend(result["empathetic_insights"])
        
        return {
            "synthesis_quality": "high" if overall_confidence > 0.7 else "medium" if overall_confidence > 0.5 else "low",
            "overall_confidence": overall_confidence,
            "key_insights": key_insights,
            "emergent_intelligence": emergent_intelligence,
            "agent_count": len(successful_results)
        }
    
    async def _get_current_biofield(self):
        """Get current biofield status from reactive memory"""
        try:
            recent_biofield = await self.memory_system.query_layer(
                "reactive",
                filters=[{"field": "content.event_type", "op": "==", "value": "biofield_measurement"}],
                limit=1
            )
            
            if recent_biofield:
                data = recent_biofield[0].get("content", {})
                return type('BiofieldMetrics', (), {
                    'hrv_ms': data.get("hrv_ms", 70.0),
                    'coherence_score': data.get("coherence_score", 0.5),
                    'dict': lambda self: {'hrv_ms': self.hrv_ms, 'coherence_score': self.coherence_score}
                })()
            
            return None
            
        except Exception as e:
            logger.error("Failed to get current biofield", error=str(e))
            return None
    
    async def _handle_emergency_mode(self, operation_data: Dict[str, Any], current_biofield) -> Dict[str, Any]:
        """Handle emergency mode due to low biofield coherence"""
        return {
            "success": False,
            "error": "emergency_pause",
            "biofield_hrv": current_biofield.hrv_ms,
            "suggestions": [
                "Take 5 deep breaths with 4-6-8 pattern",
                "Step away from screen for 2 minutes",
                "Practice grounding meditation",
                "Return when feeling more centered"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _update_performance_metrics(self, processing_time: float, success: bool, coordination_mode: CoordinationMode):
        """Update performance tracking metrics"""
        self.total_operations += 1
        
        if success:
            self.successful_operations += 1
        else:
            self.failed_operations += 1
        
        if coordination_mode == CoordinationMode.PARALLEL:
            self.parallel_operations += 1
        elif coordination_mode == CoordinationMode.ADAPTIVE:
            self.adaptive_operations += 1
    
    async def _log_coordination_operation(self, operation_data: Dict[str, Any], result: Dict[str, Any], 
                                        coordination_mode: CoordinationMode):
        """Log coordination operation to strategic memory"""
        try:
            log_entry = {
                "coordination_type": "multi_agent_operation",
                "operation_data": operation_data,
                "result": result,
                "coordination_mode": coordination_mode.value,
                "timestamp": datetime.utcnow().isoformat(),
                "performance_metrics": {
                    "total_operations": self.total_operations,
                    "success_rate": self.successful_operations / max(self.total_operations, 1)
                }
            }
            
            await self.memory_system.create_strategic_entry(
                content=log_entry,
                patterns=["multi_agent_coordination", coordination_mode.value],
                agent_synthesis={
                    "coordinator": "AgentCoordinationHub",
                    "success": result.get("success", False),
                    "agent_count": len(result.get("agent_results", {}))
                }
            )
            
        except Exception as e:
            logger.error("Failed to log coordination operation", error=str(e))
    
    async def _perform_health_check(self):
        """Perform health check on all agents"""
        self.platform_availability = {}
        
        for role, agent in self.agents.items():
            try:
                status = agent.get_agent_status()
                self.platform_availability[role.value] = status.get("status") == "active"
            except Exception as e:
                logger.error("Health check failed for agent", role=role.value, error=str(e))
                self.platform_availability[role.value] = False
        
        self.last_health_check = datetime.utcnow()
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get comprehensive coordination hub status"""
        return {
            "coordinator": "AgentCoordinationHub",
            "status": "active",
            "total_agents": len(self.agents),
            "available_agents": list(self.agents.keys()),
            "platform_availability": self.platform_availability,
            "performance_metrics": {
                "total_operations": self.total_operations,
                "successful_operations": self.successful_operations,
                "failed_operations": self.failed_operations,
                "success_rate": self.successful_operations / max(self.total_operations, 1),
                "parallel_operations": self.parallel_operations,
                "adaptive_operations": self.adaptive_operations
            },
            "biofield_thresholds": self.biofield_thresholds,
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None
        } 