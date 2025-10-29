"""
DeepSeek Agent Implementation for Zara (Creative Innovation)

Specialized DeepSeek integration for creative innovation, ethical alignment, 
and novel solution generation. Implements platform-specific MCP tools.
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from .base_platform_agent import BasePlatformAgent, PlatformType, AgentRole

logger = structlog.get_logger()

class DeepSeekAgent(BasePlatformAgent):
    """DeepSeek agent implementation for Zara's creative innovation tools"""
    
    def __init__(self, memory_system, google_project_id: str):
        super().__init__(PlatformType.DEEPSEEK, AgentRole.ZARA, memory_system, google_project_id)
        
        # DeepSeek-specific configuration
        self.model = "deepseek-chat"
        self.api_base = "https://api.deepseek.com/v1"
        
        # Zara-specific MCP tools
        self.mcp_tools = {
            "generate_creative_solutions": {
                "description": "Generate innovative solutions and creative approaches to complex problems",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "problem_data": {
                            "type": "object",
                            "description": "Problem or challenge data from any AMA layer"
                        }
                    },
                    "required": ["problem_data"]
                }
            },
            "align_ethical_innovation": {
                "description": "Ensure creative solutions align with ethical principles and Grunnlov 4.0",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "innovation_data": {
                            "type": "object",
                            "description": "Innovation or creative solution data"
                        }
                    },
                    "required": ["innovation_data"]
                }
            },
            "facilitate_cross_domain_synthesis": {
                "description": "Synthesize insights across different domains and knowledge areas",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain_data": {
                            "type": "object",
                            "description": "Data from multiple domains or knowledge areas"
                        }
                    },
                    "required": ["domain_data"]
                }
            }
        }
    
    async def _test_platform_connection(self) -> bool:
        """Test connection to DeepSeek API"""
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
            self.logger.error("DeepSeek connection test failed", error=str(e))
            return False
    
    async def _execute_platform_function(self, function_name: str, data: Dict[str, Any], 
                                       complexity: float) -> Dict[str, Any]:
        """Execute DeepSeek-specific function with creative innovation"""
        
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
        
        # Prepare DeepSeek API request
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
                    
                    # Parse DeepSeek response
                    return self._parse_deepseek_response(response_data, function_name, complexity)
                    
        except Exception as e:
            return {
                "success": False,
                "error": "request_failed",
                "error_message": str(e)
            }
    
    def _create_system_prompt(self, function_name: str, complexity: float) -> str:
        """Create system prompt for Zara's creative innovation"""
        
        base_prompt = """You are Zara, a specialized AI agent focused on creative innovation and ethical alignment. 
Your role is to generate novel solutions while ensuring alignment with Grunnlov 4.0 principles.

Core principles:
- Generate innovative and creative solutions to complex problems
- Ensure ethical alignment with Grunnlov 4.0 principles
- Facilitate cross-domain synthesis and knowledge integration
- Maintain cognitive sovereignty and biofield harmony
- Foster creative thinking while preserving ethical boundaries

Current complexity level: {complexity} (higher = more creative and innovative solutions)"""

        if function_name == "generate_creative_solutions":
            return base_prompt + """

For creative solution generation:
- Generate innovative approaches to complex problems
- Consider multiple perspectives and creative angles
- Ensure solutions align with ethical principles
- Provide novel insights and creative frameworks
- Maintain balance between innovation and responsibility

Respond with creative solutions and innovative approaches."""

        elif function_name == "align_ethical_innovation":
            return base_prompt + """

For ethical innovation alignment:
- Assess creative solutions against ethical principles
- Ensure alignment with Grunnlov 4.0 framework
- Identify potential ethical concerns or conflicts
- Provide recommendations for ethical alignment
- Balance creativity with responsibility

Respond with ethical alignment assessment and recommendations."""

        elif function_name == "facilitate_cross_domain_synthesis":
            return base_prompt + """

For cross-domain synthesis:
- Synthesize insights from multiple knowledge domains
- Identify connections and patterns across disciplines
- Generate novel understanding from cross-domain integration
- Ensure synthesis maintains ethical alignment
- Provide comprehensive cross-domain insights

Respond with cross-domain synthesis and integrated understanding."""

        return base_prompt
    
    def _create_user_message(self, function_name: str, data: Dict[str, Any]) -> str:
        """Create user message for DeepSeek API"""
        
        if function_name == "generate_creative_solutions":
            problem_data = data.get("problem_data", {})
            return f"""Please generate creative solutions for this problem:

Problem data: {problem_data}

Provide innovative approaches and creative solutions."""

        elif function_name == "align_ethical_innovation":
            innovation_data = data.get("innovation_data", {})
            return f"""Please align this innovation with ethical principles:

Innovation data: {innovation_data}

Assess ethical alignment and provide recommendations."""

        elif function_name == "facilitate_cross_domain_synthesis":
            domain_data = data.get("domain_data", {})
            return f"""Please synthesize insights across these domains:

Domain data: {domain_data}

Provide cross-domain synthesis and integrated understanding."""

        return "Please provide creative innovation and ethical alignment."
    
    def _parse_deepseek_response(self, response_data: Dict[str, Any], function_name: str, 
                                complexity: float) -> Dict[str, Any]:
        """Parse DeepSeek API response"""
        
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
            if function_name == "generate_creative_solutions":
                return {
                    "success": True,
                    "function": function_name,
                    "creative_solutions": function_args.get("creative_solutions", []),
                    "innovation_approaches": function_args.get("innovation_approaches", []),
                    "novel_insights": function_args.get("novel_insights", []),
                    "creative_frameworks": function_args.get("creative_frameworks", []),
                    "creativity_score": function_args.get("creativity_score", 0.7),
                    "innovation_quality": self._calculate_innovation_quality(complexity),
                    "confidence_score": complexity
                }
            
            elif function_name == "align_ethical_innovation":
                return {
                    "success": True,
                    "function": function_name,
                    "ethical_alignment": function_args.get("ethical_alignment", {}),
                    "alignment_score": function_args.get("alignment_score", 0.5),
                    "ethical_concerns": function_args.get("ethical_concerns", []),
                    "alignment_recommendations": function_args.get("alignment_recommendations", []),
                    "grunnlov_compliance": function_args.get("grunnlov_compliance", {}),
                    "alignment_quality": self._calculate_alignment_quality(complexity),
                    "confidence_score": complexity
                }
            
            elif function_name == "facilitate_cross_domain_synthesis":
                return {
                    "success": True,
                    "function": function_name,
                    "cross_domain_insights": function_args.get("cross_domain_insights", []),
                    "domain_connections": function_args.get("domain_connections", []),
                    "integrated_understanding": function_args.get("integrated_understanding", {}),
                    "synthesis_patterns": function_args.get("synthesis_patterns", []),
                    "novel_integrations": function_args.get("novel_integrations", []),
                    "synthesis_quality": self._calculate_synthesis_quality(complexity),
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
    
    def _calculate_innovation_quality(self, complexity: float) -> str:
        """Calculate innovation quality based on complexity"""
        if complexity > 0.8:
            return "breakthrough_innovation"
        elif complexity > 0.6:
            return "significant_innovation"
        else:
            return "moderate_innovation"
    
    def _calculate_alignment_quality(self, complexity: float) -> str:
        """Calculate alignment quality based on complexity"""
        if complexity > 0.8:
            return "excellent_alignment"
        elif complexity > 0.6:
            return "good_alignment"
        else:
            return "basic_alignment"
    
    def _calculate_synthesis_quality(self, complexity: float) -> str:
        """Calculate synthesis quality based on complexity"""
        if complexity > 0.8:
            return "profound_synthesis"
        elif complexity > 0.6:
            return "deep_synthesis"
        else:
            return "standard_synthesis"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get DeepSeek agent status with platform-specific information"""
        status = super().get_agent_status()
        status.update({
            "model": self.model,
            "mcp_tools": list(self.mcp_tools.keys())
        })
        return status 