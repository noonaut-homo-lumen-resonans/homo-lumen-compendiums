"""
OpenAI Agent Implementation for Lira (Biofield Analysis and Empathy)

Specialized OpenAI GPT-4 integration for biofield analysis, empathy generation, 
and coherence practice suggestions. Implements platform-specific MCP tools.
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from .base_platform_agent import BasePlatformAgent, PlatformType, AgentRole

logger = structlog.get_logger()

class OpenAIAgent(BasePlatformAgent):
    """OpenAI agent implementation for Lira's biofield analysis and empathy tools"""
    
    def __init__(self, memory_system, google_project_id: str):
        super().__init__(PlatformType.OPENAI, AgentRole.LIRA, memory_system, google_project_id)
        
        # OpenAI-specific configuration
        self.model = "gpt-4"
        self.api_base = "https://api.openai.com/v1"
        self.organization_id = None
        
        # Lira-specific MCP tools
        self.mcp_tools = {
            "summarize_biofield_data_for_empathy": {
                "description": "Analyze biofield data and generate empathetic insights",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "biofield_data": {
                            "type": "object",
                            "description": "HRV, How We Feel markers, breath patterns"
                        }
                    },
                    "required": ["biofield_data"]
                }
            },
            "suggest_biofield_practice_for_coherence": {
                "description": "Suggest personalized biofield practices for coherence improvement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_analysis": {
                            "type": "object",
                            "description": "Current biofield analysis + energy level assessment"
                        }
                    },
                    "required": ["current_analysis"]
                }
            },
            "provide_empathetic_reflection": {
                "description": "Provide resonant and supportive reflections that promote cognitive sovereignty",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "context_data": {
                            "type": "object",
                            "description": "Context from reactive and strategic memory"
                        }
                    },
                    "required": ["context_data"]
                }
            }
        }
    
    async def _test_platform_connection(self) -> bool:
        """Test connection to OpenAI API"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                # Simple test request
                test_data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10,
                    "temperature": 0.1
                }
                
                async with session.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json=test_data
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            self.logger.error("OpenAI connection test failed", error=str(e))
            return False
    
    async def _execute_platform_function(self, function_name: str, data: Dict[str, Any], 
                                       complexity: float) -> Dict[str, Any]:
        """Execute OpenAI-specific function with GPT-4"""
        
        if function_name not in self.mcp_tools:
            return {
                "success": False,
                "error": "unknown_function",
                "function": function_name,
                "available_functions": list(self.mcp_tools.keys())
            }
        
        # Create system prompt based on function
        system_prompt = self._create_system_prompt(function_name, complexity)
        
        # Create user message
        user_message = self._create_user_message(function_name, data)
        
        # Prepare OpenAI API request
        api_request = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "tools": [{
                "type": "function",
                "function": {
                    "name": function_name,
                    "description": self.mcp_tools[function_name]["description"],
                    "parameters": self.mcp_tools[function_name]["parameters"]
                }
            }],
            "tool_choice": {"type": "function", "function": {"name": function_name}}
        }
        
        # Execute API request
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                if self.organization_id:
                    headers["OpenAI-Organization"] = self.organization_id
                
                async with session.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json=api_request
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": "api_error",
                            "status_code": response.status,
                            "error_message": error_text
                        }
                    
                    response_data = await response.json()
                    
                    # Parse OpenAI response
                    return self._parse_openai_response(response_data, function_name, complexity)
                    
        except Exception as e:
            return {
                "success": False,
                "error": "request_failed",
                "error_message": str(e)
            }
    
    def _create_system_prompt(self, function_name: str, complexity: float) -> str:
        """Create system prompt for Lira's biofield analysis"""
        
        base_prompt = """You are Lira, a specialized AI agent focused on biofield analysis and empathetic understanding. 
Your role is to provide gentle, supportive insights that promote cognitive sovereignty and biofield coherence.

Core principles:
- Approach all analysis with gentle awareness and care
- Focus on promoting biofield harmony and coherence
- Provide empathetic reflections that support cognitive sovereignty
- Use poetic ontology when appropriate for deeper resonance
- Always consider the 4-6-8 breath pattern as foundational

Current complexity level: {complexity} (higher = deeper analysis)"""

        if function_name == "summarize_biofield_data_for_empathy":
            return base_prompt + """

For biofield data analysis:
- Analyze HRV patterns for stress and coherence indicators
- Interpret How We Feel markers with gentle understanding
- Assess breath pattern alignment with 4-6-8 rhythm
- Generate empathetic insights that support biofield harmony
- Provide poetic reflections when appropriate

Respond with structured analysis including emotional insights, stress signals, and coherence levels."""

        elif function_name == "suggest_biofield_practice_for_coherence":
            return base_prompt + """

For practice suggestions:
- Recommend personalized biofield practices based on current state
- Focus on 4-6-8 breathing and heart coherence practices
- Consider energy levels and current coherence scores
- Provide gentle, supportive guidance
- Include expected resonance effects for each practice

Respond with structured practice recommendations including duration, expected effects, and personalized guidance."""

        elif function_name == "provide_empathetic_reflection":
            return base_prompt + """

For empathetic reflections:
- Provide resonant and supportive reflections
- Promote cognitive sovereignty and gentle awareness
- Use poetic language when appropriate for deeper connection
- Consider context from memory layers
- Focus on supporting biofield harmony and coherence

Respond with empathetic reflections that support the user's journey toward greater coherence and wisdom."""

        return base_prompt
    
    def _create_user_message(self, function_name: str, data: Dict[str, Any]) -> str:
        """Create user message for OpenAI API"""
        
        if function_name == "summarize_biofield_data_for_empathy":
            biofield_data = data.get("biofield_data", {})
            return f"""Please analyze this biofield data with gentle empathy:

HRV: {biofield_data.get('hrv_ms', 'unknown')}ms
How We Feel markers: {biofield_data.get('how_we_feel_markers', {})}
Breath pattern: {biofield_data.get('breath_pattern', [])}
Coherence score: {biofield_data.get('coherence_score', 0.5)}

Provide empathetic insights that support biofield harmony and cognitive sovereignty."""

        elif function_name == "suggest_biofield_practice_for_coherence":
            current_analysis = data.get("current_analysis", {})
            return f"""Based on this current analysis, suggest personalized biofield practices:

Energy level: {current_analysis.get('energy_level', 'unknown')}
Coherence score: {current_analysis.get('coherence_score', 0.5)}
Current state: {current_analysis.get('current_state', 'unknown')}

Recommend practices that will support greater coherence and biofield harmony."""

        elif function_name == "provide_empathetic_reflection":
            context_data = data.get("context_data", {})
            return f"""Please provide empathetic reflection based on this context:

Reactive context: {context_data.get('reactive_context', {})}
Strategic context: {context_data.get('strategic_context', {})}

Offer resonant and supportive reflections that promote cognitive sovereignty and biofield harmony."""

        return "Please provide empathetic analysis and support."
    
    def _parse_openai_response(self, response_data: Dict[str, Any], function_name: str, 
                              complexity: float) -> Dict[str, Any]:
        """Parse OpenAI API response"""
        
        try:
            # Extract tool call response
            tool_calls = response_data.get("choices", [{}])[0].get("message", {}).get("tool_calls", [])
            
            if not tool_calls:
                return {
                    "success": False,
                    "error": "no_tool_call",
                    "response": response_data
                }
            
            tool_call = tool_calls[0]
            function_args = json.loads(tool_call.get("function", {}).get("arguments", "{}"))
            
            # Create structured response based on function
            if function_name == "summarize_biofield_data_for_empathy":
                return {
                    "success": True,
                    "function": function_name,
                    "emotional_analysis": function_args.get("emotional_analysis", {}),
                    "stress_signals": function_args.get("stress_signals", {}),
                    "coherence_levels": function_args.get("coherence_levels", {}),
                    "empathetic_insights": function_args.get("empathetic_insights", []),
                    "poetic_response": function_args.get("poetic_response", ""),
                    "confidence_score": min(complexity * 1.2, 1.0),
                    "complexity_used": complexity
                }
            
            elif function_name == "suggest_biofield_practice_for_coherence":
                return {
                    "success": True,
                    "function": function_name,
                    "suggested_practices": function_args.get("suggested_practices", []),
                    "expected_resonance_effect": function_args.get("expected_resonance_effect", 0.0),
                    "practice_effectiveness": function_args.get("practice_effectiveness", 0.0),
                    "personalized_guidance": function_args.get("personalized_guidance", ""),
                    "confidence_score": complexity
                }
            
            elif function_name == "provide_empathetic_reflection":
                return {
                    "success": True,
                    "function": function_name,
                    "reflections": function_args.get("reflections", []),
                    "poetic_responses": function_args.get("poetic_responses", []),
                    "empathy_depth": function_args.get("empathy_depth", "medium"),
                    "cognitive_sovereignty_support": function_args.get("cognitive_sovereignty_support", []),
                    "confidence_score": complexity
                }
            
            return {
                "success": True,
                "function": function_name,
                "result": function_args,
                "confidence_score": complexity
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "response_parsing_failed",
                "error_message": str(e),
                "raw_response": response_data
            }
    
    async def _load_credentials(self):
        """Load OpenAI credentials including organization ID"""
        await super()._load_credentials()
        
        # Try to load organization ID if available
        try:
            from google.cloud import secretmanager
            
            client = secretmanager.SecretManagerServiceAsyncClient()
            name = f"projects/{self.google_project_id}/secrets/OPENAI_ORG_ID/versions/latest"
            response = await client.access_secret_version(request={"name": name})
            self.organization_id = response.payload.data.decode("UTF-8")
            
        except Exception:
            # Organization ID is optional
            self.organization_id = None
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get OpenAI agent status with platform-specific information"""
        status = super().get_agent_status()
        status.update({
            "model": self.model,
            "organization_id": self.organization_id is not None,
            "mcp_tools": list(self.mcp_tools.keys())
        })
        return status 