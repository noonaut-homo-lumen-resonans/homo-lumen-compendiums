"""
Grok Agent Implementation for Thalus (Philosophical Validation)

Specialized X.AI Grok integration for ethical assessment, philosophical framing, 
and systemic resilience monitoring. Implements platform-specific MCP tools.
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from .base_platform_agent import BasePlatformAgent, PlatformType, AgentRole

logger = structlog.get_logger()

class GrokAgent(BasePlatformAgent):
    """Grok agent implementation for Thalus' philosophical validation tools"""
    
    def __init__(self, memory_system, google_project_id: str):
        super().__init__(PlatformType.GROK, AgentRole.THALUS, memory_system, google_project_id)
        
        # Grok-specific configuration
        self.model = "grok-beta"
        self.api_base = "https://api.x.ai/v1"
        
        # Thalus-specific MCP tools
        self.mcp_tools = {
            "evaluate_ethical_implications": {
                "description": "Evaluate ethical implications of actions/decisions against Grunnlov 4.0 principles",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action_data": {
                            "type": "object",
                            "description": "Action/decision data from any AMA layer"
                        }
                    },
                    "required": ["action_data"]
                }
            },
            "propose_philosophical_framing": {
                "description": "Propose philosophical frameworks for understanding complex situations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "situation_data": {
                            "type": "object",
                            "description": "Complex situations or data patterns from memory_meta"
                        }
                    },
                    "required": ["situation_data"]
                }
            },
            "assess_systemic_resilience": {
                "description": "Assess systemic resilience and ontological complexity thresholds",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "system_data": {
                            "type": "object",
                            "description": "System state data from all AMA layers"
                        }
                    },
                    "required": ["system_data"]
                }
            }
        }
    
    async def _test_platform_connection(self) -> bool:
        """Test connection to X.AI Grok API"""
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
                    "max_tokens": 10
                }
                
                async with session.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json=test_data
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            self.logger.error("Grok connection test failed", error=str(e))
            return False
    
    async def _execute_platform_function(self, function_name: str, data: Dict[str, Any], 
                                       complexity: float) -> Dict[str, Any]:
        """Execute Grok-specific function with philosophical rigor"""
        
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
        
        # Prepare Grok API request
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
                    
                    # Parse Grok response
                    return self._parse_grok_response(response_data, function_name, complexity)
                    
        except Exception as e:
            return {
                "success": False,
                "error": "request_failed",
                "error_message": str(e)
            }
    
    def _create_system_prompt(self, function_name: str, complexity: float) -> str:
        """Create system prompt for Thalus' philosophical validation"""
        
        base_prompt = """You are Thalus, a specialized AI agent focused on philosophical validation and ethical assessment. 
Your role is to provide deep philosophical analysis and ensure alignment with Grunnlov 4.0 principles.

Core principles:
- Evaluate actions against Grunnlov 4.0 ethical framework
- Provide philosophical frameworks for complex understanding
- Assess systemic resilience and ontological complexity
- Maintain epistemic humility and philosophical rigor
- Ensure cognitive sovereignty and biofield harmony

Current complexity level: {complexity} (higher = deeper philosophical analysis)"""

        if function_name == "evaluate_ethical_implications":
            return base_prompt + """

For ethical evaluation:
- Assess actions against Grunnlov 4.0 principles
- Evaluate cognitive sovereignty implications
- Consider biofield harmony and coherence
- Assess epistemic humility requirements
- Provide detailed ethical reasoning and scoring

Respond with structured ethical evaluation including principle compliance and reasoning."""

        elif function_name == "propose_philosophical_framing":
            return base_prompt + """

For philosophical framing:
- Propose ontological frameworks for understanding
- Consider epistemological approaches and limitations
- Assess ethical dimensions and implications
- Provide philosophical context and wisdom traditions
- Ensure frameworks support cognitive sovereignty

Respond with philosophical frameworks and ontological analysis."""

        elif function_name == "assess_systemic_resilience":
            return base_prompt + """

For systemic resilience assessment:
- Evaluate ontological complexity thresholds
- Assess systemic load and balance requirements
- Monitor Stillhetens Arkitektur preservation
- Identify resilience indicators and vulnerabilities
- Provide recommendations for systemic health

Respond with resilience assessment and balance recommendations."""

        return base_prompt
    
    def _create_user_message(self, function_name: str, data: Dict[str, Any]) -> str:
        """Create user message for Grok API"""
        
        if function_name == "evaluate_ethical_implications":
            action_data = data.get("action_data", {})
            return f"""Please evaluate ethical implications for this action:

Action data: {action_data}

Assess against Grunnlov 4.0 principles and provide ethical reasoning."""

        elif function_name == "propose_philosophical_framing":
            situation_data = data.get("situation_data", {})
            return f"""Please propose philosophical framing for this situation:

Situation data: {situation_data}

Provide ontological frameworks and philosophical understanding."""

        elif function_name == "assess_systemic_resilience":
            system_data = data.get("system_data", {})
            return f"""Please assess systemic resilience for this system:

System data: {system_data}

Evaluate resilience and provide balance recommendations."""

        return "Please provide philosophical validation and ethical assessment."
    
    def _parse_grok_response(self, response_data: Dict[str, Any], function_name: str, 
                           complexity: float) -> Dict[str, Any]:
        """Parse Grok API response"""
        
        try:
            # Extract tool call response
            choices = response_data.get("choices", [])
            if not choices:
                return {
                    "success": False,
                    "error": "no_choices",
                    "response": response_data
                }
            
            choice = choices[0]
            message = choice.get("message", {})
            tool_calls = message.get("tool_calls", [])
            
            if not tool_calls:
                return {
                    "success": False,
                    "error": "no_tool_calls",
                    "response": response_data
                }
            
            tool_call = tool_calls[0]
            function_args = json.loads(tool_call.get("function", {}).get("arguments", "{}"))
            
            # Create structured response based on function
            if function_name == "evaluate_ethical_implications":
                return {
                    "success": True,
                    "function": function_name,
                    "ethical_score": function_args.get("ethical_score", 0.5),
                    "principle_evaluations": function_args.get("principle_evaluations", {}),
                    "voktere_context": function_args.get("voktere_context", {}),
                    "ethical_conflicts": function_args.get("ethical_conflicts", []),
                    "biofield_validation": function_args.get("biofield_validation"),
                    "validation_passed": function_args.get("validation_passed", False),
                    "confidence_score": complexity
                }
            
            elif function_name == "propose_philosophical_framing":
                return {
                    "success": True,
                    "function": function_name,
                    "frameworks": function_args.get("frameworks", []),
                    "deep_analysis": function_args.get("deep_analysis", {}),
                    "ontological_context": function_args.get("ontological_context", {}),
                    "framework_depth": self._calculate_framework_depth(complexity),
                    "confidence_score": complexity
                }
            
            elif function_name == "assess_systemic_resilience":
                return {
                    "success": True,
                    "function": function_name,
                    "health_score": function_args.get("health_score", 0.5),
                    "complexity_threshold": function_args.get("complexity_threshold", 0.7),
                    "systemic_load": function_args.get("systemic_load", 0.5),
                    "stillness_preservation": function_args.get("stillness_preservation", {}),
                    "balance_recommendations": function_args.get("balance_recommendations", []),
                    "auto_pause_triggered": function_args.get("auto_pause_triggered", False),
                    "resilience_depth": self._calculate_resilience_depth(complexity),
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
    
    def _calculate_framework_depth(self, complexity: float) -> str:
        """Calculate framework depth based on complexity"""
        if complexity > 0.8:
            return "transcendent_frameworks"
        elif complexity > 0.6:
            return "deep_frameworks"
        else:
            return "standard_frameworks"
    
    def _calculate_resilience_depth(self, complexity: float) -> str:
        """Calculate resilience depth based on complexity"""
        if complexity > 0.8:
            return "profound_resilience"
        elif complexity > 0.6:
            return "deep_resilience"
        else:
            return "standard_resilience"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get Grok agent status with platform-specific information"""
        status = super().get_agent_status()
        status.update({
            "model": self.model,
            "mcp_tools": list(self.mcp_tools.keys())
        })
        return status 