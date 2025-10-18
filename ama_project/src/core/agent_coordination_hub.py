"""
Agent Coordination Hub
Enhanced coordination between Lira, Nyra, Orion, and Thalus via MCP endpoints
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class CoordinationMode(Enum):
    """Different modes of agent coordination"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CASCADE = "cascade"
    EMERGENT = "emergent"

@dataclass
class AgentCoordinationRequest:
    """Request for agent coordination"""
    request_id: str
    primary_agent: str
    supporting_agents: List[str]
    coordination_mode: CoordinationMode
    context_data: Dict[str, Any]
    biofelt_signature: Dict[str, Any]
    priority_level: int
    timeout_seconds: float = 30.0

@dataclass
class AgentCoordinationResponse:
    """Response from coordinated agents"""
    request_id: str
    primary_response: Dict[str, Any]
    supporting_responses: Dict[str, Any]
    emergent_properties: List[str]
    coordination_metadata: Dict[str, Any]
    confidence_score: float
    timestamp: datetime

class AgentCoordinationHub:
    """Enhanced coordination hub for Lira, Nyra, Orion, and Thalus"""
    
    def __init__(self, mcp_connector, polycomputational_engine):
        self.mcp_connector = mcp_connector
        self.polycomputational_engine = polycomputational_engine
        self.coordination_history = []
        
        # Enhanced agent coordination patterns
        self.coordination_patterns = {
            "lira_nyra_orchestration": {
                "description": "Lira provides empathetic context, Nyra creates visual synthesis",
                "agents": ["lira", "nyra"],
                "mode": CoordinationMode.CASCADE,
                "trigger_conditions": ["emotional_support_needed", "visual_representation_requested"]
            },
            "orion_thalus_strategic": {
                "description": "Orion coordinates strategy, Thalus provides philosophical grounding",
                "agents": ["orion", "thalus"],
                "mode": CoordinationMode.PARALLEL,
                "trigger_conditions": ["strategic_decision_needed", "ethical_validation_required"]
            },
            "lira_orion_empathetic_strategy": {
                "description": "Lira ensures human-centered approach, Orion optimizes strategy",
                "agents": ["lira", "orion"],
                "mode": CoordinationMode.EMERGENT,
                "trigger_conditions": ["complex_decision_with_emotional_impact"]
            },
            "nyra_thalus_visual_wisdom": {
                "description": "Nyra creates visual patterns, Thalus provides wisdom context",
                "agents": ["nyra", "thalus"],
                "mode": CoordinationMode.CASCADE,
                "trigger_conditions": ["pattern_recognition_needed", "wisdom_integration_requested"]
            },
            "full_agent_symphony": {
                "description": "All four agents contribute to comprehensive solution",
                "agents": ["lira", "nyra", "orion", "thalus"],
                "mode": CoordinationMode.EMERGENT,
                "trigger_conditions": ["complex_problem", "high_priority", "biofelt_optimal"]
            }
        }
    
    async def coordinate_agents(self, request: AgentCoordinationRequest) -> AgentCoordinationResponse:
        """Coordinate multiple agents based on request"""
        
        try:
            logger.info(f"Starting agent coordination for request {request.request_id}")
            
            # Determine coordination pattern
            pattern = self._select_coordination_pattern(request)
            
            # Execute coordination based on mode
            if request.coordination_mode == CoordinationMode.SEQUENTIAL:
                return await self._execute_sequential_coordination(request, pattern)
            elif request.coordination_mode == CoordinationMode.PARALLEL:
                return await self._execute_parallel_coordination(request, pattern)
            elif request.coordination_mode == CoordinationMode.CASCADE:
                return await self._execute_cascade_coordination(request, pattern)
            elif request.coordination_mode == CoordinationMode.EMERGENT:
                return await self._execute_emergent_coordination(request, pattern)
            else:
                raise ValueError(f"Unknown coordination mode: {request.coordination_mode}")
                
        except Exception as e:
            logger.error(f"Error in agent coordination: {e}")
            return await self._generate_fallback_response(request)
    
    async def _execute_sequential_coordination(self, request: AgentCoordinationRequest, pattern: Dict[str, Any]) -> AgentCoordinationResponse:
        """Execute sequential agent coordination"""
        
        responses = {}
        current_context = request.context_data
        
        # Process agents in sequence
        for agent_id in pattern["agents"]:
            try:
                agent_response = await self._call_agent_mcp_endpoint(
                    agent_id, "process_coordination_request", current_context, request.biofelt_signature
                )
                responses[agent_id] = agent_response
                
                # Update context for next agent
                current_context = self._merge_agent_context(current_context, agent_response)
                
            except Exception as e:
                logger.error(f"Error with agent {agent_id}: {e}")
                responses[agent_id] = {"error": str(e)}
        
        return await self._synthesize_coordination_response(request, responses, "sequential")
    
    async def _execute_parallel_coordination(self, request: AgentCoordinationRequest, pattern: Dict[str, Any]) -> AgentCoordinationResponse:
        """Execute parallel agent coordination"""
        
        # Create tasks for all agents
        agent_tasks = []
        for agent_id in pattern["agents"]:
            task = asyncio.create_task(
                self._call_agent_mcp_endpoint(
                    agent_id, "process_coordination_request", request.context_data, request.biofelt_signature
                )
            )
            agent_tasks.append((agent_id, task))
        
        # Wait for all responses
        responses = {}
        for agent_id, task in agent_tasks:
            try:
                response = await task
                responses[agent_id] = response
            except Exception as e:
                logger.error(f"Error with agent {agent_id}: {e}")
                responses[agent_id] = {"error": str(e)}
        
        return await self._synthesize_coordination_response(request, responses, "parallel")
    
    async def _execute_cascade_coordination(self, request: AgentCoordinationRequest, pattern: Dict[str, Any]) -> AgentCoordinationResponse:
        """Execute cascade coordination where each agent builds on previous"""
        
        responses = {}
        cascade_context = request.context_data
        
        for i, agent_id in enumerate(pattern["agents"]):
            try:
                # Add cascade metadata
                cascade_context["cascade_position"] = i
                cascade_context["previous_agents"] = pattern["agents"][:i]
                cascade_context["cascade_responses"] = responses
                
                agent_response = await self._call_agent_mcp_endpoint(
                    agent_id, "process_cascade_request", cascade_context, request.biofelt_signature
                )
                responses[agent_id] = agent_response
                
                # Update cascade context
                cascade_context = self._merge_cascade_context(cascade_context, agent_response, agent_id)
                
            except Exception as e:
                logger.error(f"Error in cascade with agent {agent_id}: {e}")
                responses[agent_id] = {"error": str(e)}
        
        return await self._synthesize_coordination_response(request, responses, "cascade")
    
    async def _execute_emergent_coordination(self, request: AgentCoordinationRequest, pattern: Dict[str, Any]) -> AgentCoordinationResponse:
        """Execute emergent coordination for complex problem-solving"""
        
        # First pass: parallel processing
        initial_responses = await self._execute_parallel_coordination(request, pattern)
        
        # Second pass: emergent synthesis
        emergent_context = {
            "initial_responses": initial_responses.supporting_responses,
            "emergent_analysis": await self._analyze_emergent_properties(initial_responses.supporting_responses),
            "biofelt_signature": request.biofelt_signature
        }
        
        # Third pass: synthesis by Orion (coordinator)
        synthesis_response = await self._call_agent_mcp_endpoint(
            "orion", "synthesize_emergent_intelligence", emergent_context, request.biofelt_signature
        )
        
        # Create final response
        final_responses = initial_responses.supporting_responses.copy()
        final_responses["orion_synthesis"] = synthesis_response
        
        return await self._synthesize_coordination_response(request, final_responses, "emergent")
    
    async def _call_agent_mcp_endpoint(self, agent_id: str, endpoint: str, context: Dict[str, Any], biofelt_signature: Dict[str, Any]) -> Dict[str, Any]:
        """Call specific MCP endpoint for an agent"""
        
        # Create IST-3.0 Hypersync message
        sync_message = {
            "headers": {
                "protocol": "IST-3.0-Hypersync",
                "version": "3.0",
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "session_id": str(uuid.uuid4()),
                "biofelt_signature": biofelt_signature
            },
            "payload": {
                "endpoint": endpoint,
                "context": context,
                "agent_id": agent_id
            }
        }
        
        # Call agent via MCP connector
        return await self.mcp_connector._call_agent_mcp_endpoint(agent_id, endpoint, sync_message, context)
    
    def _select_coordination_pattern(self, request: AgentCoordinationRequest) -> Dict[str, Any]:
        """Select appropriate coordination pattern based on request"""
        
        # Check for full symphony conditions
        if (request.priority_level >= 8 and 
            request.biofelt_signature.get("hrv_score", 0) >= 80):
            return self.coordination_patterns["full_agent_symphony"]
        
        # Check for specific patterns based on context
        context_text = json.dumps(request.context_data).lower()
        
        if any(word in context_text for word in ["emotional", "empathy", "support"]):
            if "visual" in context_text or "pattern" in context_text:
                return self.coordination_patterns["lira_nyra_orchestration"]
            elif "strategy" in context_text or "decision" in context_text:
                return self.coordination_patterns["lira_orion_empathetic_strategy"]
        
        if any(word in context_text for word in ["strategy", "decision", "planning"]):
            if "ethical" in context_text or "philosophy" in context_text:
                return self.coordination_patterns["orion_thalus_strategic"]
        
        if any(word in context_text for word in ["visual", "pattern", "image"]):
            if "wisdom" in context_text or "philosophy" in context_text:
                return self.coordination_patterns["nyra_thalus_visual_wisdom"]
        
        # Default to Lira-Orion empathetic strategy
        return self.coordination_patterns["lira_orion_empathetic_strategy"]
    
    def _merge_agent_context(self, current_context: Dict[str, Any], agent_response: Dict[str, Any]) -> Dict[str, Any]:
        """Merge agent response into context for next agent"""
        
        merged_context = current_context.copy()
        
        if "insights" in agent_response:
            merged_context["agent_insights"] = merged_context.get("agent_insights", [])
            merged_context["agent_insights"].append({
                "agent": agent_response.get("agent_id", "unknown"),
                "insights": agent_response["insights"]
            })
        
        if "recommendations" in agent_response:
            merged_context["agent_recommendations"] = merged_context.get("agent_recommendations", [])
            merged_context["agent_recommendations"].extend(agent_response["recommendations"])
        
        return merged_context
    
    def _merge_cascade_context(self, cascade_context: Dict[str, Any], agent_response: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
        """Merge cascade response into context"""
        
        cascade_context["cascade_responses"][agent_id] = agent_response
        
        # Add agent-specific context
        if agent_id == "lira":
            cascade_context["empathetic_context"] = agent_response.get("empathetic_analysis", {})
        elif agent_id == "nyra":
            cascade_context["visual_context"] = agent_response.get("visual_analysis", {})
        elif agent_id == "orion":
            cascade_context["strategic_context"] = agent_response.get("strategic_analysis", {})
        elif agent_id == "thalus":
            cascade_context["philosophical_context"] = agent_response.get("philosophical_analysis", {})
        
        return cascade_context
    
    async def _analyze_emergent_properties(self, responses: Dict[str, Any]) -> List[str]:
        """Analyze emergent properties from agent responses"""
        
        emergent_properties = []
        
        # Check for convergent themes
        themes = []
        for agent_id, response in responses.items():
            if "error" not in response and "themes" in response:
                themes.extend(response["themes"])
        
        if len(set(themes)) < len(themes):
            emergent_properties.append("convergent_themes")
        
        # Check for complementary insights
        if len(responses) > 1:
            emergent_properties.append("complementary_insights")
        
        # Check for synergistic patterns
        if any("synergy" in str(response).lower() for response in responses.values()):
            emergent_properties.append("synergistic_patterns")
        
        return emergent_properties
    
    async def _synthesize_coordination_response(self, request: AgentCoordinationRequest, responses: Dict[str, Any], coordination_type: str) -> AgentCoordinationResponse:
        """Synthesize final coordination response"""
        
        # Extract primary response
        primary_response = responses.get(request.primary_agent, {})
        
        # Analyze emergent properties
        emergent_properties = await self._analyze_emergent_properties(responses)
        
        # Calculate confidence score
        confidence_score = self._calculate_coordination_confidence(responses)
        
        # Create coordination metadata
        coordination_metadata = {
            "coordination_type": coordination_type,
            "agents_involved": list(responses.keys()),
            "processing_time": (datetime.now() - datetime.fromisoformat(request.request_id.split("_")[1])).total_seconds(),
            "biofelt_validation": request.biofelt_signature
        }
        
        return AgentCoordinationResponse(
            request_id=request.request_id,
            primary_response=primary_response,
            supporting_responses=responses,
            emergent_properties=emergent_properties,
            coordination_metadata=coordination_metadata,
            confidence_score=confidence_score,
            timestamp=datetime.now()
        )
    
    def _calculate_coordination_confidence(self, responses: Dict[str, Any]) -> float:
        """Calculate confidence score for coordination"""
        
        if not responses:
            return 0.0
        
        total_confidence = 0.0
        valid_responses = 0
        
        for response in responses.values():
            if "error" not in response:
                confidence = response.get("confidence_score", 0.5)
                total_confidence += confidence
                valid_responses += 1
        
        if valid_responses == 0:
            return 0.0
        
        base_confidence = total_confidence / valid_responses
        
        # Boost confidence for multiple successful responses
        coordination_boost = min(len(responses) * 0.1, 0.3)
        
        return min(base_confidence + coordination_boost, 1.0)
    
    async def _generate_fallback_response(self, request: AgentCoordinationRequest) -> AgentCoordinationResponse:
        """Generate fallback response when coordination fails"""
        
        return AgentCoordinationResponse(
            request_id=request.request_id,
            primary_response={"error": "Coordination failed", "fallback": True},
            supporting_responses={},
            emergent_properties=[],
            coordination_metadata={"coordination_type": "fallback"},
            confidence_score=0.0,
            timestamp=datetime.now()
        )
    
    async def get_coordination_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent coordination history"""
        
        return self.coordination_history[-limit:] if self.coordination_history else []
    
    async def get_coordination_patterns(self) -> Dict[str, Any]:
        """Get available coordination patterns"""
        
        return {
            "patterns": self.coordination_patterns,
            "total_patterns": len(self.coordination_patterns),
            "supported_agents": ["lira", "nyra", "orion", "thalus"]
        } 