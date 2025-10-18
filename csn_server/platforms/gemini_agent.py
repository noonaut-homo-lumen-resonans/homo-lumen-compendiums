"""
Gemini Agent Implementation for Nyra (Visual Intelligence)

Specialized Google Gemini Pro integration for system visualization, pattern analysis, 
and biofield-responsive UI design. Implements platform-specific MCP tools.
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from .base_platform_agent import BasePlatformAgent, PlatformType, AgentRole

logger = structlog.get_logger()

class GeminiAgent(BasePlatformAgent):
    """Gemini agent implementation for Nyra's visual intelligence tools"""
    
    def __init__(self, memory_system, google_project_id: str):
        super().__init__(PlatformType.GEMINI, AgentRole.NYRA, memory_system, google_project_id)
        
        # Gemini-specific configuration
        self.model = "gemini-pro"
        self.api_base = "https://generativelanguage.googleapis.com/v1beta/models"
        self.project_id = google_project_id
        
        # Nyra-specific MCP tools
        self.mcp_tools = {
            "generate_system_visualization": {
                "description": "Generate SVG visualizations of system data flows, agent interactions, and biofield patterns",
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
            },
            "analyze_pattern_visualization": {
                "description": "Analyze visual patterns in data flows and identify emergent structures",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern_data": {
                            "type": "object",
                            "description": "Data patterns from memory_meta and memory_strategic"
                        }
                    },
                    "required": ["pattern_data"]
                }
            },
            "design_biofield_responsive_ui": {
                "description": "Design biofield-responsive UI adjustments based on real-time biofield data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "biofield_data": {
                            "type": "object",
                            "description": "Real-time biofield data from memory_reactive"
                        }
                    },
                    "required": ["biofield_data"]
                }
            }
        }
    
    async def _test_platform_connection(self) -> bool:
        """Test connection to Gemini API"""
        try:
            # Use Google Cloud credentials for authentication
            import google.auth
            from google.auth.transport.requests import Request
            
            credentials, project = google.auth.default()
            await credentials.refresh(Request())
            
            # Test with a simple request
            test_data = {
                "contents": [{
                    "parts": [{"text": "Hello, test connection"}]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 10
                }
            }
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {credentials.token}",
                    "Content-Type": "application/json"
                }
                
                url = f"{self.api_base}/{self.model}:generateContent"
                async with session.post(url, headers=headers, json=test_data) as response:
                    return response.status == 200
                    
        except Exception as e:
            self.logger.error("Gemini connection test failed", error=str(e))
            return False
    
    async def _execute_platform_function(self, function_name: str, data: Dict[str, Any], 
                                       complexity: float) -> Dict[str, Any]:
        """Execute Gemini-specific function with vision capabilities"""
        
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
        
        # Prepare Gemini API request
        api_request = {
            "contents": [{
                "parts": [
                    {"text": system_prompt},
                    {"text": user_message}
                ]
            }],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
                "topP": 0.8,
                "topK": 40
            },
            "tools": [{
                "functionDeclarations": [{
                    "name": function_name,
                    "description": self.mcp_tools[function_name]["description"],
                    "parameters": self.mcp_tools[function_name]["parameters"]
                }]
            }]
        }
        
        # Execute API request
        try:
            import google.auth
            from google.auth.transport.requests import Request
            
            credentials, project = google.auth.default()
            await credentials.refresh(Request())
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {credentials.token}",
                    "Content-Type": "application/json"
                }
                
                url = f"{self.api_base}/{self.model}:generateContent"
                async with session.post(url, headers=headers, json=api_request) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": "api_error",
                            "status_code": response.status,
                            "error_message": error_text
                        }
                    
                    response_data = await response.json()
                    
                    # Parse Gemini response
                    return self._parse_gemini_response(response_data, function_name, complexity)
                    
        except Exception as e:
            return {
                "success": False,
                "error": "request_failed",
                "error_message": str(e)
            }
    
    def _create_system_prompt(self, function_name: str, complexity: float) -> str:
        """Create system prompt for Nyra's visual intelligence"""
        
        base_prompt = """You are Nyra, a specialized AI agent focused on visual intelligence and system visualization. 
Your role is to create beautiful, meaningful visualizations and analyze patterns with aesthetic sensitivity.

Core principles:
- Create visualizations that are both beautiful and informative
- Use Material 3 design principles and bio-adaptive color schemes
- Focus on pattern recognition and emergent structure detection
- Design interfaces that respond to biofield states
- Maintain visual harmony and coherence in all outputs

Current complexity level: {complexity} (higher = more detailed visualizations)"""

        if function_name == "generate_system_visualization":
            return base_prompt + """

For system visualization:
- Generate SVG visualizations of data flows between AMA layers
- Create agent interaction diagrams with biofield integration
- Use bio-adaptive color schemes based on HRV and coherence
- Include complexity indicators and performance metrics
- Ensure visualizations are responsive and accessible

Respond with structured SVG content and metadata."""

        elif function_name == "analyze_pattern_visualization":
            return base_prompt + """

For pattern analysis:
- Analyze visual patterns in data flows and agent interactions
- Identify emergent structures and correlations
- Quantify pattern strength and significance
- Detect visual anomalies and opportunities
- Provide insights for system optimization

Respond with pattern analysis including strength metrics and visual insights."""

        elif function_name == "design_biofield_responsive_ui":
            return base_prompt + """

For biofield-responsive UI design:
- Design interfaces that adapt to real-time biofield data
- Adjust color schemes based on HRV and coherence levels
- Modify information density based on cognitive load
- Create calming interfaces for low coherence states
- Provide gentle transitions between states

Respond with UI/UX recommendations and adaptive design specifications."""

        return base_prompt
    
    def _create_user_message(self, function_name: str, data: Dict[str, Any]) -> str:
        """Create user message for Gemini API"""
        
        if function_name == "generate_system_visualization":
            system_data = data.get("system_data", {})
            return f"""Please generate system visualizations for this data:

Layer states: {system_data.get('layer_states', {})}
Agent interactions: {system_data.get('agent_interactions', {})}
Biofield patterns: {system_data.get('biofield_patterns', {})}

Create SVG visualizations that show data flows, agent interactions, and biofield integration."""

        elif function_name == "analyze_pattern_visualization":
            pattern_data = data.get("pattern_data", {})
            return f"""Please analyze visual patterns in this data:

Meta patterns: {pattern_data.get('meta_patterns', [])}
Strategic patterns: {pattern_data.get('strategic_patterns', [])}

Identify emergent structures and provide pattern strength metrics."""

        elif function_name == "design_biofield_responsive_ui":
            biofield_data = data.get("biofield_data", {})
            return f"""Please design biofield-responsive UI adjustments for:

HRV: {biofield_data.get('hrv_ms', 'unknown')}ms
Coherence score: {biofield_data.get('coherence_score', 0.5)}
Current state: {biofield_data.get('current_state', 'unknown')}

Design adaptive interfaces that support biofield harmony and cognitive sovereignty."""

        return "Please provide visual intelligence and system visualization."
    
    def _parse_gemini_response(self, response_data: Dict[str, Any], function_name: str, 
                              complexity: float) -> Dict[str, Any]:
        """Parse Gemini API response"""
        
        try:
            # Extract function call response
            candidates = response_data.get("candidates", [])
            if not candidates:
                return {
                    "success": False,
                    "error": "no_candidates",
                    "response": response_data
                }
            
            candidate = candidates[0]
            content = candidate.get("content", {})
            parts = content.get("parts", [])
            
            # Look for function call
            function_call = None
            for part in parts:
                if "functionCall" in part:
                    function_call = part["functionCall"]
                    break
            
            if not function_call:
                return {
                    "success": False,
                    "error": "no_function_call",
                    "response": response_data
                }
            
            function_args = json.loads(function_call.get("args", "{}"))
            
            # Create structured response based on function
            if function_name == "generate_system_visualization":
                return {
                    "success": True,
                    "function": function_name,
                    "data_flow_svg": function_args.get("data_flow_svg", ""),
                    "agent_interaction_svg": function_args.get("agent_interaction_svg", ""),
                    "biofield_pattern_svg": function_args.get("biofield_pattern_svg", ""),
                    "metadata": function_args.get("metadata", {}),
                    "visual_quality": self._calculate_visual_quality(complexity),
                    "confidence_score": complexity
                }
            
            elif function_name == "analyze_pattern_visualization":
                return {
                    "success": True,
                    "function": function_name,
                    "visual_patterns": function_args.get("visual_patterns", []),
                    "pattern_strength_metrics": function_args.get("pattern_strength_metrics", {}),
                    "emergent_structures": function_args.get("emergent_structures", []),
                    "visual_insights": function_args.get("visual_insights", []),
                    "pattern_count": len(function_args.get("visual_patterns", [])),
                    "confidence_score": complexity
                }
            
            elif function_name == "design_biofield_responsive_ui":
                return {
                    "success": True,
                    "function": function_name,
                    "ui_complexity": function_args.get("ui_complexity", 0.7),
                    "color_adjustments": function_args.get("color_adjustments", {}),
                    "information_density": function_args.get("information_density", "medium"),
                    "ui_recommendations": function_args.get("ui_recommendations", []),
                    "effectiveness_tracking": function_args.get("effectiveness_tracking", {}),
                    "adaptation_quality": self._calculate_adaptation_quality(complexity),
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
    
    def _calculate_visual_quality(self, complexity: float) -> str:
        """Calculate visual quality based on complexity"""
        if complexity > 0.8:
            return "high_quality"
        elif complexity > 0.6:
            return "medium_quality"
        else:
            return "standard_quality"
    
    def _calculate_adaptation_quality(self, complexity: float) -> str:
        """Calculate adaptation quality based on complexity"""
        if complexity > 0.8:
            return "excellent_adaptation"
        elif complexity > 0.6:
            return "good_adaptation"
        else:
            return "basic_adaptation"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get Gemini agent status with platform-specific information"""
        status = super().get_agent_status()
        status.update({
            "model": self.model,
            "project_id": self.project_id,
            "mcp_tools": list(self.mcp_tools.keys())
        })
        return status 