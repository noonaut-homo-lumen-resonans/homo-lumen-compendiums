"""
Base Platform Agent Class for Multi-Platform AI Integration

Provides common functionality for all platform-specific agents including:
- Credential management via Google Secret Manager
- Rate limiting and optimization strategies
- Unified MCP interface layer
- Error handling and fallback mechanisms
- Biofield-responsive processing
"""

import asyncio
import time
import json
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from enum import Enum
import structlog

from ..routers.ama_memory_layers import (
    AMAMemorySystem, BiofieldMetrics, MemoryLayer, BiofieldValidationResult
)

logger = structlog.get_logger()

class PlatformType(str, Enum):
    """Supported AI platforms"""
    OPENAI = "openai"
    GEMINI = "gemini"
    GROK = "grok"
    DEEPSEEK = "deepseek"
    CLAUDE = "claude"

class AgentRole(str, Enum):
    """Agent roles in the coalition"""
    LIRA = "lira"  # Biofield analysis and empathy
    NYRA = "nyra"  # Visual intelligence
    THALUS = "thalus"  # Philosophical validation
    ZARA = "zara"  # Creative innovation
    ORION = "orion"  # Coordination
    ABACUS = "abacus"  # Analytical processing

class BasePlatformAgent(ABC):
    """Base class for all platform-specific agents"""
    
    def __init__(self, platform_type: PlatformType, agent_role: AgentRole, 
                 memory_system: AMAMemorySystem, google_project_id: str):
        self.platform_type = platform_type
        self.agent_role = agent_role
        self.memory_system = memory_system
        self.google_project_id = google_project_id
        
        # Agent-specific configuration
        self.temperature = self._get_default_temperature()
        self.max_tokens = self._get_default_max_tokens()
        self.rate_limit_config = self._get_rate_limit_config()
        
        # Performance tracking
        self.request_count = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        self.last_request_time = None
        
        # Rate limiting state
        self.rate_limit_reset_time = None
        self.current_rate_limit_remaining = None
        
        # Credential management
        self.api_key = None
        self.credentials_loaded = False
        
        # Biofield thresholds
        self.biofield_thresholds = {
            "high_coherence": 80,  # HRV >= 80ms
            "medium_coherence": 60,  # HRV >= 60ms
            "low_coherence": 50,  # HRV < 50ms triggers pause
            "emergency_pause": 40  # HRV < 40ms triggers emergency
        }
    
    async def initialize(self) -> bool:
        """Initialize the agent with credentials and platform connection"""
        try:
            # Load credentials from Google Secret Manager
            await self._load_credentials()
            
            # Test platform connection
            connection_test = await self._test_platform_connection()
            
            if connection_test:
                self.logger.info("Platform agent initialized successfully", 
                               platform=self.platform_type.value,
                               agent_role=self.agent_role.value)
                return True
            else:
                self.logger.error("Platform connection test failed", 
                                platform=self.platform_type.value)
                return False
                
        except Exception as e:
            self.logger.error("Failed to initialize platform agent", 
                            platform=self.platform_type.value,
                            error=str(e))
            return False
    
    async def execute_mcp_function(self, function_name: str, data: Dict[str, Any], 
                                 complexity: float = 0.7) -> Dict[str, Any]:
        """Execute MCP function with biofield modulation and platform-specific handling"""
        
        start_time = time.time()
        
        try:
            # Get current biofield status
            current_biofield = await self._get_current_biofield()
            
            # Check for emergency pause conditions
            if current_biofield and current_biofield.hrv_ms < self.biofield_thresholds["emergency_pause"]:
                return await self._handle_emergency_pause(current_biofield)
            
            # Adapt processing based on biofield
            adapted_complexity = self._adapt_complexity_to_biofield(complexity, current_biofield)
            
            # Check rate limits
            if not await self._check_rate_limits():
                return await self._handle_rate_limit_exceeded()
            
            # Execute platform-specific function
            result = await self._execute_platform_function(function_name, data, adapted_complexity)
            
            # Update performance metrics
            response_time = time.time() - start_time
            self._update_performance_metrics(response_time, True)
            
            # Add biofield context to result
            result["biofield_context"] = {
                "hrv_ms": current_biofield.hrv_ms if current_biofield else None,
                "coherence_score": current_biofield.coherence_score if current_biofield else None,
                "adapted_complexity": adapted_complexity,
                "platform": self.platform_type.value,
                "agent_role": self.agent_role.value
            }
            
            # Log to AMA memory
            await self._log_agent_operation(function_name, data, result)
            
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            self._update_performance_metrics(response_time, False)
            
            self.logger.error("MCP function execution failed", 
                            function=function_name,
                            platform=self.platform_type.value,
                            error=str(e))
            
            return await self._handle_execution_error(function_name, data, str(e))
    
    @abstractmethod
    async def _execute_platform_function(self, function_name: str, data: Dict[str, Any], 
                                       complexity: float) -> Dict[str, Any]:
        """Execute platform-specific function - to be implemented by subclasses"""
        pass
    
    @abstractmethod
    async def _test_platform_connection(self) -> bool:
        """Test connection to the platform - to be implemented by subclasses"""
        pass
    
    async def _load_credentials(self):
        """Load platform credentials from Google Secret Manager"""
        try:
            from google.cloud import secretmanager
            
            client = secretmanager.SecretManagerServiceAsyncClient()
            
            # Get secret name based on platform
            secret_name = self._get_secret_name()
            
            # Access the secret
            name = f"projects/{self.google_project_id}/secrets/{secret_name}/versions/latest"
            response = await client.access_secret_version(request={"name": name})
            
            # Parse credentials based on platform
            self.api_key = self._parse_credentials(response.payload.data.decode("UTF-8"))
            self.credentials_loaded = True
            
            self.logger.info("Credentials loaded successfully", platform=self.platform_type.value)
            
        except Exception as e:
            self.logger.error("Failed to load credentials", 
                            platform=self.platform_type.value,
                            error=str(e))
            raise
    
    def _get_secret_name(self) -> str:
        """Get secret name for the platform"""
        secret_mapping = {
            PlatformType.OPENAI: "OPENAI_API_KEY",
            PlatformType.GEMINI: "GOOGLE_SERVICE_ACCOUNT_JSON",
            PlatformType.GROK: "XAI_API_KEY",
            PlatformType.DEEPSEEK: "DEEPSEEK_API_KEY",
            PlatformType.CLAUDE: "ANTHROPIC_API_KEY"
        }
        return secret_mapping.get(self.platform_type, "UNKNOWN_PLATFORM_KEY")
    
    def _parse_credentials(self, credential_data: str) -> Union[str, Dict[str, Any]]:
        """Parse credentials based on platform type"""
        if self.platform_type == PlatformType.GEMINI:
            # Google service account is JSON
            return json.loads(credential_data)
        else:
            # Other platforms use API keys as strings
            return credential_data
    
    def _get_default_temperature(self) -> float:
        """Get default temperature for the agent role"""
        temperature_mapping = {
            AgentRole.LIRA: 0.7,    # Empathy and biofield analysis
            AgentRole.NYRA: 0.8,    # Visual processing
            AgentRole.THALUS: 0.3,  # Philosophical rigor
            AgentRole.ZARA: 0.9,    # Maximized creativity
            AgentRole.ORION: 0.5,   # Balanced coordination
            AgentRole.ABACUS: 0.2   # Precision analytics
        }
        return temperature_mapping.get(self.agent_role, 0.5)
    
    def _get_default_max_tokens(self) -> int:
        """Get default max tokens for the agent role"""
        token_mapping = {
            AgentRole.LIRA: 2000,    # Empathetic responses
            AgentRole.NYRA: 3000,    # Visual descriptions
            AgentRole.THALUS: 2500,  # Philosophical analysis
            AgentRole.ZARA: 3000,    # Creative content
            AgentRole.ORION: 4000,   # Coordination tasks
            AgentRole.ABACUS: 2000   # Analytical reports
        }
        return token_mapping.get(self.agent_role, 2000)
    
    def _get_rate_limit_config(self) -> Dict[str, Any]:
        """Get rate limit configuration for the platform"""
        rate_limit_mapping = {
            PlatformType.OPENAI: {
                "requests_per_minute": 60,
                "tokens_per_minute": 150000,
                "retry_after_header": "x-ratelimit-reset-requests"
            },
            PlatformType.GEMINI: {
                "requests_per_minute": 60,
                "tokens_per_minute": 1000000,
                "retry_after_header": "retry-after"
            },
            PlatformType.GROK: {
                "requests_per_minute": 30,
                "tokens_per_minute": 100000,
                "retry_after_header": "x-ratelimit-reset"
            },
            PlatformType.DEEPSEEK: {
                "requests_per_minute": 50,
                "tokens_per_minute": 200000,
                "retry_after_header": "x-ratelimit-reset"
            },
            PlatformType.CLAUDE: {
                "requests_per_minute": 50,
                "tokens_per_minute": 200000,
                "retry_after_header": "x-ratelimit-reset"
            }
        }
        return rate_limit_mapping.get(self.platform_type, {})
    
    async def _get_current_biofield(self) -> Optional[BiofieldMetrics]:
        """Get current biofield status from reactive memory"""
        try:
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
    
    def _adapt_complexity_to_biofield(self, base_complexity: float, 
                                    biofield: Optional[BiofieldMetrics]) -> float:
        """Adapt complexity based on biofield state"""
        if not biofield:
            return base_complexity
        
        if biofield.hrv_ms >= self.biofield_thresholds["high_coherence"]:
            # High coherence allows higher complexity
            return min(base_complexity * 1.3, 1.0)
        elif biofield.hrv_ms >= self.biofield_thresholds["medium_coherence"]:
            # Medium coherence uses base complexity
            return base_complexity
        else:
            # Low coherence reduces complexity
            return max(base_complexity * 0.7, 0.3)
    
    async def _check_rate_limits(self) -> bool:
        """Check if we can make a request based on rate limits"""
        if not self.rate_limit_reset_time:
            return True
        
        if datetime.utcnow() < self.rate_limit_reset_time:
            return False
        
        # Reset rate limit state
        self.rate_limit_reset_time = None
        self.current_rate_limit_remaining = None
        return True
    
    async def _handle_rate_limit_exceeded(self) -> Dict[str, Any]:
        """Handle rate limit exceeded scenario"""
        return {
            "success": False,
            "error": "rate_limit_exceeded",
            "platform": self.platform_type.value,
            "agent_role": self.agent_role.value,
            "retry_after": self.rate_limit_reset_time.isoformat() if self.rate_limit_reset_time else None,
            "suggestion": "Retry after rate limit reset or use alternative agent"
        }
    
    async def _handle_emergency_pause(self, biofield: BiofieldMetrics) -> Dict[str, Any]:
        """Handle emergency pause due to low biofield coherence"""
        return {
            "success": False,
            "error": "emergency_pause",
            "platform": self.platform_type.value,
            "agent_role": self.agent_role.value,
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
    
    async def _handle_execution_error(self, function_name: str, data: Dict[str, Any], 
                                    error: str) -> Dict[str, Any]:
        """Handle execution errors with fallback strategies"""
        return {
            "success": False,
            "error": "execution_failed",
            "function": function_name,
            "platform": self.platform_type.value,
            "agent_role": self.agent_role.value,
            "error_message": error,
            "fallback_suggestion": "Try alternative agent or reduce complexity",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _update_performance_metrics(self, response_time: float, success: bool):
        """Update performance tracking metrics"""
        self.request_count += 1
        self.total_response_time += response_time
        self.last_request_time = datetime.utcnow()
        
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
    
    async def _log_agent_operation(self, function_name: str, data: Dict[str, Any], 
                                 result: Dict[str, Any]):
        """Log agent operation to strategic memory"""
        try:
            log_entry = {
                "platform": self.platform_type.value,
                "agent_role": self.agent_role.value,
                "function": function_name,
                "input_data": data,
                "result": result,
                "timestamp": datetime.utcnow().isoformat(),
                "performance_metrics": {
                    "request_count": self.request_count,
                    "success_rate": self.successful_requests / max(self.request_count, 1),
                    "avg_response_time": self.total_response_time / max(self.request_count, 1)
                }
            }
            
            await self.memory_system.create_strategic_entry(
                content=log_entry,
                patterns=[f"{self.platform_type.value}_{self.agent_role.value}_{function_name}"],
                agent_synthesis={
                    "platform": self.platform_type.value,
                    "agent_role": self.agent_role.value,
                    "confidence": result.get("confidence_score", 0.5),
                    "success": result.get("success", True)
                }
            )
            
        except Exception as e:
            self.logger.error("Failed to log agent operation", error=str(e))
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and performance metrics"""
        return {
            "platform": self.platform_type.value,
            "agent_role": self.agent_role.value,
            "status": "active" if self.credentials_loaded else "uninitialized",
            "request_count": self.request_count,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / max(self.request_count, 1),
            "avg_response_time": self.total_response_time / max(self.request_count, 1),
            "last_request": self.last_request_time.isoformat() if self.last_request_time else None,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "rate_limit_config": self.rate_limit_config
        } 