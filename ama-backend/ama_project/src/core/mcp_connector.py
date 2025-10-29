"""
FastMCP (Fast Multi-Context Protocol) Connector
Advanced MCP implementation with IST-3.0 Hypersync Protocol and biofelt integration
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BiofeltState:
    """Represents user's current biofelt state with enhanced validation"""
    hrv_score: float
    emotional_state: str
    energy_level: int
    stress_indicators: List[str]
    timestamp: datetime
    coherence_score: float = 0.0
    hair_raising_response: bool = False
    cognitive_sovereignty_level: float = 1.0
    
    def get_complexity_level(self) -> str:
        """Determines optimal complexity level based on biofelt"""
        if self.hrv_score < 40:
            return "emergency"
        elif self.hrv_score < 60:
            return "minimal"
        elif self.hrv_score < 80:
            return "balanced"
        else:
            return "full_polycomputing"
    
    def get_biofelt_signature(self) -> Dict[str, Any]:
        """Generate biofelt signature for MCP messages"""
        return {
            "hrv_score": self.hrv_score,
            "emotional_state": self.emotional_state,
            "energy_level": self.energy_level,
            "coherence_score": self.coherence_score,
            "hair_raising_response": self.hair_raising_response,
            "cognitive_sovereignty_level": self.cognitive_sovereignty_level,
            "stress_indicators": self.stress_indicators,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class IST30Message:
    """IST-3.0 Hypersync Protocol message structure"""
    protocol_version: str = "3.0"
    message_id: str = None
    session_id: str = None
    timestamp: datetime = None
    biofelt_signature: Dict[str, Any] = None
    payload: Dict[str, Any] = None
    headers: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.message_id is None:
            self.message_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.headers is None:
            self.headers = {
                "protocol": "IST-3.0-Hypersync",
                "version": self.protocol_version,
                "message_id": self.message_id,
                "timestamp": self.timestamp.isoformat(),
                "session_id": self.session_id,
                "biofelt_signature": self.biofelt_signature
            }

@dataclass
class ContextQuery:
    """Structures contextual queries to AMA system with enhanced biofelt integration"""
    query_text: str
    query_type: str  # "emotional_support", "technical_help", "creative_inspiration", etc.
    priority_level: int
    biofelt_context: BiofeltState
    agent_preferences: Optional[List[str]] = None
    polycomputational_request: bool = True
    emergent_intelligence_request: bool = True

class FastMCPProtocol:
    """IST-3.0 Hypersync Protocol implementation"""
    
    def __init__(self):
        self.protocol_version = "3.0"
        self.supported_agents = ["lira", "nyra", "thalus", "zara", "orion", "abacus", "manus"]
    
    def create_sync_message(self, data: Dict[str, Any], session_id: str, biofelt_signature: Dict[str, Any]) -> IST30Message:
        """Create IST-3.0 Hypersync message with biofelt signature"""
        
        payload = {
            "data": data,
            "processing_requirements": {
                "max_response_time": 30.0,
                "min_confidence_threshold": 0.6,
                "biofelt_validation_required": True,
                "polycomputational_processing": True
            },
            "emergent_intelligence_request": {
                "convergent_analysis": True,
                "complementary_insights": True,
                "synergistic_patterns": True,
                "collective_wisdom_synthesis": True
            },
            "agent_coordination": {
                "parallel_processing": True,
                "cross_agent_validation": True,
                "emergent_property_detection": True
            }
        }
        
        return IST30Message(
            session_id=session_id,
            biofelt_signature=biofelt_signature,
            payload=payload
        )
    
    def validate_sync_response(self, response: Dict[str, Any]) -> bool:
        """Validate IST-3.0 Hypersync response"""
        
        required_fields = ["headers", "payload", "agent_signature", "biofelt_validation"]
        
        for field in required_fields:
            if field not in response:
                logger.warning(f"Missing required field in sync response: {field}")
                return False
        
        # Validate headers
        headers = response.get("headers", {})
        if headers.get("protocol") != "IST-3.0-Hypersync":
            logger.warning("Invalid protocol version in response")
            return False
        
        return True

class MutationLogger:
    """Enhanced mutation logger for transformative reversibility with biofelt tracking"""
    
    def __init__(self):
        self.mutation_log = []
        self.biofelt_history = []
    
    async def log_query(self, query: ContextQuery) -> str:
        """Log a query for tracking with biofelt context"""
        query_id = f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        log_entry = {
            "query_id": query_id,
            "timestamp": datetime.now(),
            "query": query.query_text,
            "type": query.query_type,
            "biofelt_state": query.biofelt_context.get_biofelt_signature(),
            "polycomputational_request": query.polycomputational_request,
            "emergent_intelligence_request": query.emergent_intelligence_request
        }
        
        self.mutation_log.append(log_entry)
        
        # Track biofelt history
        self.biofelt_history.append({
            "timestamp": datetime.now(),
            "biofelt_signature": query.biofelt_context.get_biofelt_signature(),
            "query_id": query_id
        })
        
        return query_id
    
    async def log_response(self, query_id: str, response: Dict[str, Any]):
        """Log response for learning and reversibility with biofelt validation"""
        for entry in self.mutation_log:
            if entry.get("query_id") == query_id:
                entry["response"] = response
                entry["response_timestamp"] = datetime.now()
                entry["biofelt_validation"] = response.get("biofelt_validation", {})
                break

class AgentRegistry:
    """Enhanced registry for managing the seven agents with MCP capabilities"""
    
    def __init__(self):
        self.agents = {
            "lira": {
                "name": "Lira",
                "platform": "OpenAI GPT-4o-mini",
                "specialization": "empathetic_biofelt_analysis",
                "status": "available",
                "mcp_endpoints": [
                    "summarize_biofelt_data_for_empathy",
                    "suggest_biofield_practice_for_coherence",
                    "provide_empathetic_reflection"
                ],
                "processing_capabilities": ["biofelt_analysis", "empathetic_reflection", "cognitive_sovereignty"],
                "max_response_time": 25.0,
                "confidence_threshold": 0.7
            },
            "nyra": {
                "name": "Nyra", 
                "platform": "Google Gemini 1.5 Flash",
                "specialization": "visual_intelligence",
                "status": "available",
                "mcp_endpoints": [
                    "submit_visualization",
                    "request_system_snapshot",
                    "generate_bio_adaptive_palette"
                ],
                "processing_capabilities": ["visual_analysis", "creative_synthesis", "pattern_identification"],
                "max_response_time": 30.0,
                "confidence_threshold": 0.6
            },
            "thalus": {
                "name": "Thalus",
                "platform": "X.AI Grok",
                "specialization": "philosophical_wisdom",
                "status": "available",
                "mcp_endpoints": [
                    "provide_philosophical_grounding",
                    "validate_ethical_frameworks",
                    "synthesize_wisdom_traditions"
                ],
                "processing_capabilities": ["strategic_analysis", "decision_frameworks", "risk_assessment"],
                "max_response_time": 35.0,
                "confidence_threshold": 0.8
            },
            "zara": {
                "name": "Zara",
                "platform": "DeepSeek Chat",
                "specialization": "creative_innovation",
                "status": "available",
                "mcp_endpoints": [
                    "generate_creative_solution",
                    "validate_legal_compliance",
                    "optimize_workflow_process"
                ],
                "processing_capabilities": ["knowledge_synthesis", "learning_analysis", "insight_generation"],
                "max_response_time": 40.0,
                "confidence_threshold": 0.75
            },
            "manus": {
                "name": "Manus",
                "platform": "Claude Code",
                "specialization": "technical_implementation",
                "status": "available",
                "mcp_endpoints": [
                    "implement_technical_solution",
                    "validate_code_architecture",
                    "optimize_performance"
                ],
                "processing_capabilities": ["technical_implementation", "code_optimization", "architecture_validation"],
                "max_response_time": 45.0,
                "confidence_threshold": 0.9
            },
            "abacus": {
                "name": "Abacus",
                "platform": "Perplexity",
                "specialization": "research_analysis",
                "status": "available",
                "mcp_endpoints": [
                    "conduct_research_analysis",
                    "synthesize_information",
                    "validate_data_sources"
                ],
                "processing_capabilities": ["research_analysis", "data_synthesis", "source_validation"],
                "max_response_time": 50.0,
                "confidence_threshold": 0.85
            },
            "orion": {
                "name": "Orion",
                "platform": "Anthropic Claude 3.5 Sonnet",
                "specialization": "strategic_coordination",
                "status": "available",
                "mcp_endpoints": [
                    "coordinate_agent_responses",
                    "synthesize_collective_intelligence",
                    "validate_strategic_alignment"
                ],
                "processing_capabilities": ["synthesis", "coordination", "emergent_analysis"],
                "max_response_time": 55.0,
                "confidence_threshold": 0.95
            }
        }
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific agent"""
        return self.agents.get(agent_id)
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agents"""
        return [agent_id for agent_id, info in self.agents.items() 
                if info["status"] == "available"]
    
    def get_agent_mcp_endpoints(self, agent_id: str) -> List[str]:
        """Get MCP endpoints for a specific agent"""
        agent_info = self.get_agent_info(agent_id)
        return agent_info.get("mcp_endpoints", []) if agent_info else []

class BiofeltMonitor:
    """Enhanced monitor for biofelt state changes with BiofeltGate protocol"""
    
    def __init__(self):
        self.current_state = None
        self.biofelt_history = []
        self.emergency_thresholds = {
            "hrv_min": 40,
            "coherence_min": 0.3,
            "stress_max": 3
        }
    
    async def get_current_state(self, user_id: str) -> Optional[BiofeltState]:
        """Get current biofelt state for user with enhanced validation"""
        # TODO: Implement real biofelt monitoring
        # For now, return default state
        return BiofeltState(
            hrv_score=75.0,
            emotional_state="balanced",
            energy_level=7,
            stress_indicators=[],
            timestamp=datetime.now(),
            coherence_score=0.75,
            hair_raising_response=False,
            cognitive_sovereignty_level=0.9
        )
    
    def validate_biofelt_gate(self, biofelt_state: BiofeltState) -> Dict[str, Any]:
        """BiofeltGate validation for operation complexity"""
        
        validation_result = {
            "passed": True,
            "complexity_level": "full",
            "warnings": [],
            "emergency_mode": False
        }
        
        # HRV validation
        if biofelt_state.hrv_score < self.emergency_thresholds["hrv_min"]:
            validation_result["passed"] = False
            validation_result["complexity_level"] = "emergency"
            validation_result["emergency_mode"] = True
            validation_result["warnings"].append("HRV too low for complex operations")
        
        # Coherence validation
        elif biofelt_state.coherence_score < self.emergency_thresholds["coherence_min"]:
            validation_result["complexity_level"] = "minimal"
            validation_result["warnings"].append("Low coherence - minimal operations only")
        
        # Stress indicators validation
        elif len(biofelt_state.stress_indicators) > self.emergency_thresholds["stress_max"]:
            validation_result["complexity_level"] = "balanced"
            validation_result["warnings"].append("Multiple stress indicators detected")
        
        return validation_result

class FastMCPConnector:
    """Enhanced MCP Connector with FastMCP architecture and IST-3.0 Hypersync Protocol"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.notion_client = None
        self.hwf_client = None
        self.notebook_lm = None
        self.mutation_log = MutationLogger()
        self.agent_registry = AgentRegistry()
        self.biofelt_monitor = BiofeltMonitor()
        self.fast_mcp_protocol = FastMCPProtocol()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.active_sessions = {}
        
    async def initialize_connections(self):
        """Initialize all external connections with enhanced error handling"""
        try:
            # TODO: Initialize actual clients
            logger.info("FastMCP connections initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize FastMCP connections: {e}")
            raise
    
    async def process_context_query(self, query: ContextQuery) -> Dict[str, Any]:
        """Enhanced main method for processing contextual queries with polycomputational processing"""
        
        # Log query for transformative reversibility
        query_id = await self.mutation_log.log_query(query)
        
        try:
            # BiofeltGate validation
            biofelt_validation = self.biofelt_monitor.validate_biofelt_gate(query.biofelt_context)
            
            if biofelt_validation["emergency_mode"]:
                return await self._generate_emergency_response(query, biofelt_validation)
            
            # Create IST-3.0 Hypersync session
            session_id = str(uuid.uuid4())
            sync_message = self.fast_mcp_protocol.create_sync_message(
                {"query": query.query_text, "type": query.query_type},
                session_id,
                query.biofelt_context.get_biofelt_signature()
            )
            
            # Store session
            self.active_sessions[session_id] = {
                "query": query,
                "sync_message": sync_message,
                "biofelt_validation": biofelt_validation,
                "start_time": datetime.now(),
                "status": "processing"
            }
            
            # Determine optimal response strategy based on biofelt
            response_strategy = self._determine_response_strategy(query.biofelt_context, biofelt_validation)
            
            # Fetch relevant context from all sources
            context_data = await self._fetch_contextual_data(query, response_strategy)
            
            # Activate appropriate agents based on query and biofelt
            active_agents = await self._activate_agents(query, response_strategy)
            
            # Process query through activated agents with polycomputational processing
            if query.polycomputational_request:
                agent_responses = await self._process_polycomputationally(
                    query, context_data, active_agents, sync_message, session_id
                )
            else:
                agent_responses = await self._process_through_agents(
                    query, context_data, active_agents
                )
            
            # Synthesize emergent response
            emergent_response = await self._synthesize_emergent_response(
                agent_responses, query.biofelt_context, query.emergent_intelligence_request
            )
            
            # Log result for learning and reversibility
            await self.mutation_log.log_response(query_id, emergent_response)
            
            # Update session status
            self.active_sessions[session_id]["status"] = "completed"
            self.active_sessions[session_id]["response"] = emergent_response
            
            return emergent_response
            
        except Exception as e:
            logger.error(f"Error processing context query: {e}")
            return await self._generate_fallback_response(query)
    
    async def _process_polycomputationally(self, query: ContextQuery, context_data: Dict[str, Any], 
                                         active_agents: List[str], sync_message: IST30Message, 
                                         session_id: str) -> Dict[str, Any]:
        """Process query through multiple agents simultaneously with IST-3.0 Hypersync"""
        
        agent_tasks = []
        for agent_id in active_agents:
            agent_config = self.agent_registry.get_agent_info(agent_id)
            if agent_config:
                task = asyncio.create_task(
                    self._process_with_agent_mcp(agent_id, agent_config, sync_message, context_data)
                )
                agent_tasks.append((agent_id, task))
        
        # Wait for all agent responses
        agent_responses = {}
        for agent_id, task in agent_tasks:
            try:
                response = await task
                agent_responses[agent_id] = response
            except Exception as e:
                logger.error(f"Error processing with agent {agent_id}: {e}")
                agent_responses[agent_id] = {"error": str(e)}
        
        return agent_responses
    
    async def _process_with_agent_mcp(self, agent_id: str, agent_config: Dict[str, Any], 
                                    sync_message: IST30Message, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process with specific agent using MCP endpoints"""
        
        start_time = datetime.now()
        
        try:
            # Get agent's MCP endpoints
            mcp_endpoints = self.agent_registry.get_agent_mcp_endpoints(agent_id)
            
            # Process through available MCP endpoints
            endpoint_responses = {}
            for endpoint in mcp_endpoints:
                try:
                    response = await self._call_agent_mcp_endpoint(agent_id, endpoint, sync_message, context_data)
                    endpoint_responses[endpoint] = response
                except Exception as e:
                    logger.warning(f"Error calling MCP endpoint {endpoint} for agent {agent_id}: {e}")
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "agent_id": agent_id,
                "agent_name": agent_config["name"],
                "endpoint_responses": endpoint_responses,
                "processing_time": processing_time,
                "confidence_score": self._calculate_confidence_score(endpoint_responses, agent_config),
                "biofelt_signature": sync_message.biofelt_signature,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in MCP processing for agent {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "error": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _call_agent_mcp_endpoint(self, agent_id: str, endpoint: str, 
                                     sync_message: IST30Message, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Call specific MCP endpoint for an agent"""
        
        # TODO: Implement actual MCP endpoint calls
        # For now, return mock responses based on agent specialization
        
        agent_info = self.agent_registry.get_agent_info(agent_id)
        specialization = agent_info.get("specialization", "")
        
        if agent_id == "lira":
            if endpoint == "summarize_biofelt_data_for_empathy":
                return {
                    "summary": f"Empatisk analyse av biofelt-data for {specialization}",
                    "empathy_score": 0.85,
                    "recommendations": ["4-6-8 pusteteknikk", "mindfulness øvelse"]
                }
            elif endpoint == "suggest_biofield_practice_for_coherence":
                return {
                    "practice": "Hjertefokusert pusteteknikk",
                    "duration": "5 minutter",
                    "expected_coherence_improvement": 0.15
                }
        
        elif agent_id == "nyra":
            if endpoint == "submit_visualization":
                return {
                    "visualization_type": "biofelt_pattern",
                    "svg_data": "<svg>...</svg>",
                    "color_palette": "bio_adaptive"
                }
        
        # Default response
        return {
            "endpoint": endpoint,
            "agent": agent_id,
            "status": "processed",
            "specialization": specialization
        }
    
    def _calculate_confidence_score(self, endpoint_responses: Dict[str, Any], agent_config: Dict[str, Any]) -> float:
        """Calculate confidence score based on endpoint responses and agent configuration"""
        
        if not endpoint_responses:
            return 0.0
        
        # Base confidence from agent configuration
        base_confidence = agent_config.get("confidence_threshold", 0.5)
        
        # Adjust based on successful endpoint calls
        successful_endpoints = len([r for r in endpoint_responses.values() if "error" not in r])
        total_endpoints = len(endpoint_responses)
        
        if total_endpoints == 0:
            return base_confidence
        
        success_rate = successful_endpoints / total_endpoints
        return min(base_confidence + (success_rate * 0.3), 1.0)
    
    def _determine_response_strategy(self, biofelt_state: BiofeltState, biofelt_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Determine optimal response strategy based on biofelt state"""
        
        strategy = {
            "complexity_level": biofelt_validation["complexity_level"],
            "agent_activation": "selective",
            "processing_mode": "standard",
            "biofelt_adaptation": True
        }
        
        if biofelt_validation["emergency_mode"]:
            strategy["agent_activation"] = "minimal"
            strategy["processing_mode"] = "emergency"
            strategy["active_agents"] = ["lira"]  # Only empathetic support
        elif biofelt_state.hrv_score < 60:
            strategy["agent_activation"] = "balanced"
            strategy["processing_mode"] = "conservative"
            strategy["active_agents"] = ["lira", "nyra"]  # Empathy + visual
        elif biofelt_state.hrv_score >= 80:
            strategy["agent_activation"] = "full"
            strategy["processing_mode"] = "polycomputational"
            strategy["active_agents"] = ["lira", "nyra", "thalus", "zara", "orion"]
        
        return strategy
    
    async def _fetch_contextual_data(self, query: ContextQuery, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch relevant context from all sources"""
        
        context_data = {
            "query_context": {
                "text": query.query_text,
                "type": query.query_type,
                "priority": query.priority_level
            },
            "biofelt_context": query.biofelt_context.get_biofelt_signature(),
            "strategy": strategy,
            "timestamp": datetime.now().isoformat()
        }
        
        # TODO: Implement actual data fetching from external sources
        # For now, return basic context
        
        return context_data
    
    async def _activate_agents(self, query: ContextQuery, strategy: Dict[str, Any]) -> List[str]:
        """Activate appropriate agents based on query and strategy"""
        
        if "active_agents" in strategy:
            return strategy["active_agents"]
        
        # Default agent selection based on query type
        if query.query_type == "emotional_support":
            return ["lira"]
        elif query.query_type == "visual_analysis":
            return ["nyra"]
        elif query.query_type == "strategic_planning":
            return ["thalus", "orion"]
        elif query.query_type == "creative_inspiration":
            return ["zara", "nyra"]
        else:
            return ["lira", "orion"]  # Default empathetic + strategic
    
    async def _process_through_agents(self, query: ContextQuery, context_data: Dict[str, Any], active_agents: List[str]) -> Dict[str, Any]:
        """Process query through activated agents (legacy method)"""
        
        agent_responses = {}
        for agent_id in active_agents:
            try:
                response = await self._get_agent_response(agent_id, query, context_data)
                agent_responses[agent_id] = response
            except Exception as e:
                logger.error(f"Error processing with agent {agent_id}: {e}")
                agent_responses[agent_id] = {"error": str(e)}
        
        return agent_responses
    
    async def _synthesize_emergent_response(self, agent_responses: Dict[str, Any], biofelt_context: BiofeltState, emergent_request: bool) -> Dict[str, Any]:
        """Synthesize emergent response from multiple agent responses"""
        
        if not emergent_request:
            # Return simple aggregation
            return {
                "synthesis_type": "simple_aggregation",
                "agent_responses": agent_responses,
                "biofelt_context": biofelt_context.get_biofelt_signature(),
                "timestamp": datetime.now().isoformat()
            }
        
        # Analyze for emergent properties
        emergent_properties = await self._identify_emergent_properties(agent_responses)
        
        # Synthesize collective wisdom
        collective_wisdom = await self._synthesize_collective_wisdom(agent_responses)
        
        return {
            "synthesis_type": "emergent_intelligence",
            "emergent_properties": emergent_properties,
            "collective_wisdom": collective_wisdom,
            "agent_responses": agent_responses,
            "biofelt_context": biofelt_context.get_biofelt_signature(),
            "confidence_score": self._calculate_emergent_confidence(agent_responses),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _identify_emergent_properties(self, agent_responses: Dict[str, Any]) -> List[str]:
        """Identify emergent properties from agent responses"""
        
        emergent_properties = []
        
        # Check for convergent themes
        themes = []
        for agent_id, response in agent_responses.items():
            if "error" not in response:
                # Extract themes from response
                if "endpoint_responses" in response:
                    for endpoint, endpoint_response in response["endpoint_responses"].items():
                        if "summary" in endpoint_response:
                            themes.append(endpoint_response["summary"])
        
        if len(set(themes)) < len(themes):
            emergent_properties.append("convergent_themes")
        
        # Check for complementary insights
        if len(agent_responses) > 1:
            emergent_properties.append("complementary_insights")
        
        return emergent_properties
    
    async def _synthesize_collective_wisdom(self, agent_responses: Dict[str, Any]) -> str:
        """Synthesize collective wisdom from agent responses"""
        
        wisdom_parts = []
        
        for agent_id, response in agent_responses.items():
            if "error" not in response and "endpoint_responses" in response:
                agent_name = response.get("agent_name", agent_id)
                wisdom_parts.append(f"{agent_name}: {self._extract_primary_insight(response)}")
        
        if wisdom_parts:
            return " | ".join(wisdom_parts)
        else:
            return "Collective wisdom synthesis pending"
    
    def _extract_primary_insight(self, response: Dict[str, Any]) -> str:
        """Extract primary insight from agent response"""
        
        if "endpoint_responses" in response:
            for endpoint, endpoint_response in response["endpoint_responses"].items():
                if "summary" in endpoint_response:
                    return endpoint_response["summary"]
                elif "practice" in endpoint_response:
                    return endpoint_response["practice"]
        
        return "Insight available"
    
    def _calculate_emergent_confidence(self, agent_responses: Dict[str, Any]) -> float:
        """Calculate confidence score for emergent intelligence"""
        
        if not agent_responses:
            return 0.0
        
        total_confidence = 0.0
        valid_responses = 0
        
        for response in agent_responses.values():
            if "error" not in response and "confidence_score" in response:
                total_confidence += response["confidence_score"]
                valid_responses += 1
        
        if valid_responses == 0:
            return 0.0
        
        return total_confidence / valid_responses
    
    async def _generate_emergency_response(self, query: ContextQuery, biofelt_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate emergency response when biofelt state is critical"""
        
        return {
            "response_type": "emergency",
            "message": "🌿 **Gentle Innovation:** Starting with small, manageable creative steps...",
            "recommendations": [
                "4-6-8 pusteteknikk",
                "Mindfulness øvelse",
                "Hjertefokusert pusteteknikk"
            ],
            "biofelt_validation": biofelt_validation,
            "active_agents": ["lira"],
            "complexity_level": "emergency",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_fallback_response(self, query: ContextQuery) -> Dict[str, Any]:
        """Generate fallback response when processing fails"""
        
        return {
            "response_type": "fallback",
            "message": "System temporarily unavailable. Please try again.",
            "biofelt_context": query.biofelt_context.get_biofelt_signature(),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_agent_response(self, agent: str, query: ContextQuery, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get response from specific agent (legacy method)"""
        
        # TODO: Implement actual agent communication
        return {
            "agent": agent,
            "response": f"Mock response from {agent}",
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of active session"""
        
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            return {
                "session_id": session_id,
                "status": session["status"],
                "start_time": session["start_time"].isoformat(),
                "biofelt_validation": session.get("biofelt_validation", {}),
                "response": session.get("response", None)
            }
        else:
            return {"error": "Session not found"}
    
    async def get_biofelt_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent biofelt history"""
        
        return self.mutation_log.biofelt_history[-limit:] if self.mutation_log.biofelt_history else [] 