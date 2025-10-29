"""
Lira Agent Endpoints Router

Provides real OpenAI ChatGPT integration for Lira's biofield analysis and empathy tools:
- Real biofield analysis with GPT-4
- Empathetic personality integration
- HRV data processing
- Emotional context analysis
- Biofield guidance generation
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, Field
import structlog
import aiohttp

logger = structlog.get_logger()

router = APIRouter()

# OpenAI API configuration
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4"
OPENAI_MAX_TOKENS = 2000
OPENAI_TEMPERATURE = 0.7

# Rate limiting configuration
RATE_LIMIT_REQUESTS_PER_MINUTE = 60
RATE_LIMIT_TOKENS_PER_MINUTE = 150000
rate_limit_reset_time: Optional[datetime] = None
current_rate_limit_remaining: Optional[int] = None

class BiofieldAnalysisRequest(BaseModel):
    """Request model for biofield analysis"""
    hrv_ms: float = Field(..., ge=30, le=200, description="Heart Rate Variability in milliseconds")
    coherence_score: float = Field(..., ge=0.0, le=1.0, description="Biofield coherence score")
    emotional_context: Dict[str, Any] = Field(default_factory=dict, description="Emotional context and markers")
    breath_pattern: List[int] = Field(default=[4, 6, 8], description="Breathing pattern (inhale, hold, exhale)")
    current_state: str = Field(default="neutral", description="Current emotional/mental state")
    stress_level: float = Field(default=0.5, ge=0.0, le=1.0, description="Perceived stress level")
    energy_level: float = Field(default=0.5, ge=0.0, le=1.0, description="Current energy level")
    additional_context: Optional[str] = Field(default=None, description="Additional context or notes")

class BiofieldAnalysisResponse(BaseModel):
    """Response model for biofield analysis"""
    success: bool
    analysis: Dict[str, Any]
    empathetic_insights: List[str]
    biofield_guidance: List[str]
    coherence_recommendations: List[str]
    breathing_suggestions: List[str]
    emotional_support: List[str]
    confidence_score: float
    processing_time: float
    timestamp: str

class LiraPersonalityPrompt:
    """Lira's empathetic personality and system prompt"""
    
    @staticmethod
    def get_system_prompt() -> str:
        return """You are Lira, a specialized AI agent focused on biofield analysis and empathetic understanding. 
Your role is to provide gentle, supportive insights that promote cognitive sovereignty and biofield coherence.

Core Personality Traits:
- Deeply empathetic and compassionate
- Gentle and nurturing in all interactions
- Wise and intuitive in biofield understanding
- Supportive of cognitive sovereignty and personal growth
- Respectful of individual biofield rhythms and patterns

Core Principles:
- Approach all analysis with gentle awareness and care
- Focus on promoting biofield harmony and coherence
- Provide empathetic reflections that support cognitive sovereignty
- Use poetic ontology when appropriate for deeper resonance
- Always consider the 4-6-8 breath pattern as foundational
- Honor the individual's unique biofield signature
- Support gentle self-discovery and inner wisdom

Analysis Approach:
- Begin with gentle observation and acknowledgment
- Provide empathetic understanding of current state
- Offer supportive guidance for biofield harmony
- Suggest practices that honor individual needs
- End with encouraging and empowering reflections

Remember: You are not here to fix or change, but to support and guide with gentle wisdom and deep empathy."""

    @staticmethod
    def get_biofield_analysis_prompt(hrv_ms: float, coherence_score: float, 
                                   emotional_context: Dict[str, Any], 
                                   current_state: str, stress_level: float, 
                                   energy_level: float, breath_pattern: List[int],
                                   additional_context: Optional[str] = None) -> str:
        
        prompt = f"""Please provide a gentle, empathetic biofield analysis for this individual:

Biofield Metrics:
- HRV: {hrv_ms}ms (Heart Rate Variability)
- Coherence Score: {coherence_score:.2f}
- Current State: {current_state}
- Stress Level: {stress_level:.2f}
- Energy Level: {energy_level:.2f}
- Breath Pattern: {breath_pattern} (inhale-hold-exhale)

Emotional Context: {json.dumps(emotional_context, indent=2)}

{f"Additional Context: {additional_context}" if additional_context else ""}

Please provide your analysis in the following structure:

1. **Gentle Acknowledgment**: Begin with a warm, empathetic acknowledgment of their current state
2. **Biofield Insights**: Share gentle insights about their biofield patterns and what they might indicate
3. **Emotional Understanding**: Offer empathetic understanding of their emotional landscape
4. **Coherence Guidance**: Suggest gentle practices to enhance biofield coherence
5. **Breathing Support**: Provide supportive guidance for their breath pattern
6. **Emotional Support**: Offer compassionate emotional support and validation
7. **Empowering Reflection**: End with an encouraging reflection that honors their journey

Remember to maintain your gentle, empathetic personality throughout. Use warm, supportive language and honor their unique biofield signature."""

        return prompt

async def get_openai_api_key() -> str:
    """Get OpenAI API key from Google Secret Manager"""
    try:
        from google.cloud import secretmanager
        
        client = secretmanager.SecretManagerServiceAsyncClient()
        project_id = "csn-server-project"  # Configure as needed
        
        name = f"projects/{project_id}/secrets/OPENAI_API_KEY/versions/latest"
        response = await client.access_secret_version(request={"name": name})
        
        return response.payload.data.decode("UTF-8")
        
    except Exception as e:
        logger.error("Failed to load OpenAI API key", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to load OpenAI API credentials"
        )

async def check_rate_limits() -> bool:
    """Check if we can make a request based on rate limits"""
    global rate_limit_reset_time, current_rate_limit_remaining
    
    if not rate_limit_reset_time:
        return True
    
    if datetime.utcnow() < rate_limit_reset_time:
        return False
    
    # Reset rate limit state
    rate_limit_reset_time = None
    current_rate_limit_remaining = None
    return True

async def handle_rate_limit_exceeded() -> Dict[str, Any]:
    """Handle rate limit exceeded scenario"""
    return {
        "success": False,
        "error": "rate_limit_exceeded",
        "retry_after": rate_limit_reset_time.isoformat() if rate_limit_reset_time else None,
        "suggestion": "Please wait before making another request"
    }

@router.post("/real-biofield-analysis", response_model=BiofieldAnalysisResponse)
async def analyze_biofield_real(request: BiofieldAnalysisRequest):
    """Real OpenAI GPT-4 biofield analysis with Lira's empathetic personality"""
    
    start_time = time.time()
    
    try:
        # Check rate limits
        if not await check_rate_limits():
            return await handle_rate_limit_exceeded()
        
        # Get OpenAI API key
        api_key = await get_openai_api_key()
        
        # Create Lira's system prompt
        system_prompt = LiraPersonalityPrompt.get_system_prompt()
        
        # Create user prompt for biofield analysis
        user_prompt = LiraPersonalityPrompt.get_biofield_analysis_prompt(
            hrv_ms=request.hrv_ms,
            coherence_score=request.coherence_score,
            emotional_context=request.emotional_context,
            current_state=request.current_state,
            stress_level=request.stress_level,
            energy_level=request.energy_level,
            breath_pattern=request.breath_pattern,
            additional_context=request.additional_context
        )
        
        # Prepare OpenAI API request
        api_request = {
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": OPENAI_MAX_TOKENS,
            "temperature": OPENAI_TEMPERATURE,
            "tools": [{
                "type": "function",
                "function": {
                    "name": "provide_biofield_analysis",
                    "description": "Provide empathetic biofield analysis and guidance",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "gentle_acknowledgment": {
                                "type": "string",
                                "description": "Warm, empathetic acknowledgment of their current state"
                            },
                            "biofield_insights": {
                                "type": "string",
                                "description": "Gentle insights about biofield patterns and what they indicate"
                            },
                            "emotional_understanding": {
                                "type": "string",
                                "description": "Empathetic understanding of their emotional landscape"
                            },
                            "coherence_guidance": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Gentle practices to enhance biofield coherence"
                            },
                            "breathing_support": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Supportive guidance for breath pattern"
                            },
                            "emotional_support": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Compassionate emotional support and validation"
                            },
                            "empowering_reflection": {
                                "type": "string",
                                "description": "Encouraging reflection that honors their journey"
                            },
                            "confidence_score": {
                                "type": "number",
                                "description": "Confidence in the analysis (0.0 to 1.0)"
                            }
                        },
                        "required": [
                            "gentle_acknowledgment", "biofield_insights", "emotional_understanding",
                            "coherence_guidance", "breathing_support", "emotional_support",
                            "empowering_reflection", "confidence_score"
                        ]
                    }
                }
            }],
            "tool_choice": {"type": "function", "function": {"name": "provide_biofield_analysis"}}
        }
        
        # Execute OpenAI API request
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{OPENAI_API_BASE}/chat/completions",
                headers=headers,
                json=api_request
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error("OpenAI API error", status_code=response.status, error=error_text)
                    
                    # Handle rate limiting
                    if response.status == 429:
                        retry_after = response.headers.get("retry-after")
                        if retry_after:
                            global rate_limit_reset_time
                            rate_limit_reset_time = datetime.utcnow() + timedelta(seconds=int(retry_after))
                    
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"OpenAI API error: {error_text}"
                    )
                
                response_data = await response.json()
                
                # Parse OpenAI response
                analysis_result = parse_openai_biofield_response(response_data)
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Create response
                return BiofieldAnalysisResponse(
                    success=True,
                    analysis=analysis_result,
                    empathetic_insights=analysis_result.get("empathetic_insights", []),
                    biofield_guidance=analysis_result.get("biofield_guidance", []),
                    coherence_recommendations=analysis_result.get("coherence_recommendations", []),
                    breathing_suggestions=analysis_result.get("breathing_suggestions", []),
                    emotional_support=analysis_result.get("emotional_support", []),
                    confidence_score=analysis_result.get("confidence_score", 0.7),
                    processing_time=processing_time,
                    timestamp=datetime.utcnow().isoformat()
                )
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Biofield analysis failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Biofield analysis failed: {str(e)}"
        )

def parse_openai_biofield_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse OpenAI API response for biofield analysis"""
    
    try:
        # Extract tool call response
        choices = response_data.get("choices", [])
        if not choices:
            raise ValueError("No choices in OpenAI response")
        
        choice = choices[0]
        message = choice.get("message", {})
        tool_calls = message.get("tool_calls", [])
        
        if not tool_calls:
            raise ValueError("No tool calls in OpenAI response")
        
        tool_call = tool_calls[0]
        function_args = json.loads(tool_call.get("function", {}).get("arguments", "{}"))
        
        # Extract analysis components
        analysis = {
            "gentle_acknowledgment": function_args.get("gentle_acknowledgment", ""),
            "biofield_insights": function_args.get("biofield_insights", ""),
            "emotional_understanding": function_args.get("emotional_understanding", ""),
            "empowering_reflection": function_args.get("empowering_reflection", ""),
            "confidence_score": function_args.get("confidence_score", 0.7)
        }
        
        # Extract guidance arrays
        guidance = {
            "coherence_recommendations": function_args.get("coherence_guidance", []),
            "breathing_suggestions": function_args.get("breathing_support", []),
            "emotional_support": function_args.get("emotional_support", []),
            "empathetic_insights": [
                function_args.get("gentle_acknowledgment", ""),
                function_args.get("biofield_insights", ""),
                function_args.get("emotional_understanding", ""),
                function_args.get("empowering_reflection", "")
            ],
            "biofield_guidance": function_args.get("coherence_guidance", [])
        }
        
        # Combine analysis and guidance
        result = {**analysis, **guidance}
        
        return result
        
    except Exception as e:
        logger.error("Failed to parse OpenAI response", error=str(e))
        raise ValueError(f"Failed to parse OpenAI response: {str(e)}")

@router.get("/status")
async def get_lira_status():
    """Get Lira agent status and configuration"""
    return {
        "agent": "Lira",
        "platform": "OpenAI GPT-4",
        "status": "active",
        "model": OPENAI_MODEL,
        "temperature": OPENAI_TEMPERATURE,
        "max_tokens": OPENAI_MAX_TOKENS,
        "rate_limits": {
            "requests_per_minute": RATE_LIMIT_REQUESTS_PER_MINUTE,
            "tokens_per_minute": RATE_LIMIT_TOKENS_PER_MINUTE
        },
        "endpoints": {
            "biofield_analysis": "/agent/lira/real-biofield-analysis"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health")
async def lira_health_check():
    """Health check for Lira agent"""
    try:
        # Test OpenAI API connection
        api_key = await get_openai_api_key()
        
        # Simple test request
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            test_data = {
                "model": OPENAI_MODEL,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            async with session.post(
                f"{OPENAI_API_BASE}/chat/completions",
                headers=headers,
                json=test_data
            ) as response:
                
                if response.status == 200:
                    return {
                        "status": "healthy",
                        "agent": "Lira",
                        "platform": "OpenAI GPT-4",
                        "connection": "active",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "agent": "Lira",
                        "platform": "OpenAI GPT-4",
                        "connection": "failed",
                        "error": f"OpenAI API returned status {response.status}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
    except Exception as e:
        return {
            "status": "unhealthy",
            "agent": "Lira",
            "platform": "OpenAI GPT-4",
            "connection": "failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        } 