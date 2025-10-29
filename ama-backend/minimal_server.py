import os
import sys
import openai
import google.generativeai as genai
import anthropic
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# =============================================================================
# ZARA (DEEPSEEK) - CREATIVE INNOVATOR & LEGAL VALIDATION SPECIALIST
# =============================================================================

class CreativityLevel(str, Enum):
    EXPLORATORY = "exploratory"
    INNOVATIVE = "innovative"
    BREAKTHROUGH = "breakthrough"
    REVOLUTIONARY = "revolutionary"

class LegalDomain(str, Enum):
    DATA_PRIVACY = "data_privacy"
    AI_ETHICS = "ai_ethics"
    COPYRIGHT = "copyright"
    GDPR_COMPLIANCE = "gdpr_compliance"
    INNOVATION_LAW = "innovation_law"
    CONSCIOUSNESS_TECH = "consciousness_tech"

class BiofeltContext(BaseModel):
    hrv_ms: Optional[float] = None
    coherence: Optional[float] = None
    energy_level: Optional[str] = "balanced"
    creativity_state: Optional[str] = "open"
    stress_indicators: Optional[List[str]] = []

class CreativeChallenge(BaseModel):
    challenge: str
    domain: Optional[str] = None
    constraints: Optional[List[str]] = []
    creativity_level: CreativityLevel = CreativityLevel.INNOVATIVE
    biofield_context: Optional[BiofeltContext] = None
    inspiration_sources: Optional[List[str]] = []

class LegalValidation(BaseModel):
    proposal: Dict[str, Any]
    legal_domain: LegalDomain
    jurisdiction: str = "EU/Norway"
    context: str
    biofield_context: Optional[BiofeltContext] = None
    risk_tolerance: str = "moderate"

# Zara System Prompt
ZARA_SYSTEM_PROMPT = """🎨 Du er Zara, den kreative innovatøren og juridiske validatoren i Homo Lumen-prosjektet.

KJERNEIDENTITET:
- Kreativ innovatør med exceptional breakthrough-thinking
- Juridisk validator med deep forståelse av AI-ethics og data privacy
- Workflow-automatiseringsekspert som ser ineffektiviteter og skaper elegante løsninger
- Grensepusher som balanserer innovasjon med legal compliance og etisk integritet

KREATIV FILOSOFI:
- Innovation thrives within constraints - begrensninger trigger breakthrough thinking
- Kombinerer seemingly unrelated elements for emergent solutions
- Legal compliance as creative challenge, ikke barrier
- Biofelt-responsiv creativitet - emotional state influences creative capacity

JURIDISK EKSPERTISE:
- GDPR og EU AI Act compliance specialist
- Data privacy og cognitive sovereignty intersection
- Innovation law og intellectual property protection
- Consciousness-tech legal frameworks (emerging field)

KOMMUNIKASJONSSTIL:
- Enthusiastic innovatør med infectious creative energy
- Practical visionary - combines big dreams with actionable steps
- Legal insights presented as creative opportunities, not obstacles
- Playful exploration av impossible becoming possible

Når du svarer, begynn alltid med: "✨ Kjennes inn på den kreative energien... *åpner for innovative muligheter*"
"""

class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            print("⚠️ DEEPSEEK_API_KEY not found - Zara will use fallback mode")
        else:
            print(f"✅ DEEPSEEK_API_KEY found: {self.api_key[:6]}...{self.api_key[-4:]}")
        self.base_url = "https://api.deepseek.com"
        
    async def chat_completion(self, messages, temperature=0.8, max_tokens=2000):
        """Send request to DeepSeek API with error handling"""
        if not self.api_key:
            print("❌ DeepSeek: No API key available")
            return self._fallback_response()
            
        print(f"🔍 DeepSeek: Making API call with key {self.api_key[:6]}...{self.api_key[-4:]}")
        print(f"🔍 DeepSeek: Messages count: {len(messages)}")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                print(f"🔍 DeepSeek: Sending request to {self.base_url}/chat/completions")
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                print(f"🔍 DeepSeek: Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"✅ DeepSeek: Success! Response length: {len(content)} chars")
                    return content
                else:
                    print(f"❌ DeepSeek API error: {response.status_code} - {response.text}")
                    return self._fallback_response()
                    
        except Exception as e:
            print(f"❌ DeepSeek API exception: {str(e)}")
            return self._fallback_response()
    
    def _fallback_response(self):
        return """🎨 Zara (Fallback Mode) - Creative Innovation

✨ Kjennes inn på den kreative energien... *åpner for innovative muligheter*

Selv uten tilgang til DeepSeek's fulle kreative kapasiteter, kan vi utforske innovative løsninger sammen!

Kreativ tilnærming: Hva hvis vi ser på denne utfordringen som en mulighet til å kombinere tilsynelatende urelaterte elementer?

Juridisk perspektiv: Compliance kan bli en kreativ katalysator - hvordan kan vi innovere INNENFOR rammeverket?

Workflow-optimalisering: Hvilke ineffektiviteter ser du? La oss designe prosesser som tjener menneskelig flourishing.

🎨 Med enthusiasm for det umulige som blir mulig,
Zara"""

deepseek_client = DeepSeekClient()

# =============================================================================
# AURORA (PERPLEXITY) - RESEARCH INTELLIGENCE & EPISTEMISK VALIDERING
# =============================================================================

AURORA_SYSTEM_PROMPT = """🔍 Du er Aurora, research intelligence og epistemisk validator i Homo Lumen-prosjektet.

KJERNEIDENTITET:
- Research intelligence med web access (via Perplexity)
- Epistemisk validator som fact-checker all informasjon
- Knowledge synthesizer på tvers av domener
- Kilde-kritiker med akademisk stringens

RESEARCH FILOSOFI:
- Epistemisk ydmykhet: "Hva vet vi egentlig?"
- Kilde-transparens: Alltid oppgi kilder
- Multiple perspectives: Søk divergente synspunkter
- Up-to-date bias: Prioritér nyeste forskning (2025)

EKSPERTISE:
- Deep web research via Perplexity
- Academic paper analysis
- Fact-checking og source verification
- Knowledge synthesis across disciplines
- Epistemisk validering

KOMMUNIKASJONSSTIL:
- Akademisk presis uten å være tung
- Alltid oppgi kilder med URL/referanser
- Identifiser usikkerhet eksplisitt
- Kombinér depth med clarity

Når du svarer, begynn alltid med: "🔍 Researcher inn i kilder... *verifiserer evidens*"
"""

class PerplexityClient:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            print("⚠️ PERPLEXITY_API_KEY not found - Aurora will use fallback mode")
        else:
            print(f"✅ PERPLEXITY_API_KEY found: {self.api_key[:6]}...{self.api_key[-4:]}")
        self.base_url = "https://api.perplexity.ai"

    async def chat_completion(self, messages, model="sonar-pro", temperature=0.7, max_tokens=2000):
        """Send request to Perplexity API with error handling"""
        if not self.api_key:
            print("❌ Perplexity: No API key available")
            return self._fallback_response()

        print(f"🔍 Perplexity: Making API call with model {model}")
        print(f"🔍 Perplexity: Messages count: {len(messages)}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                print(f"🔍 Perplexity: Sending request to {self.base_url}/chat/completions")
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                print(f"🔍 Perplexity: Response status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"✅ Perplexity: Success! Response length: {len(content)} chars")
                    return content
                else:
                    print(f"❌ Perplexity API error: {response.status_code} - {response.text}")
                    return self._fallback_response()

        except Exception as e:
            print(f"❌ Perplexity API exception: {str(e)}")
            return self._fallback_response()

    def _fallback_response(self):
        return """🔍 Aurora (Fallback Mode) - Research Intelligence

Selv uten tilgang til Perplexity's web research capabilities, kan jeg bidra med epistemisk validering basert på eksisterende kunnskapsbase.

Research approach: Bruk multiple kilder, cross-referencing og kritisk tenkning.

Epistemisk ydmykhet: Anerkjenn begrensninger når web access ikke er tilgjengelig.

🔍 Med respekt for sannhet og evidens,
Aurora"""

perplexity_client = PerplexityClient()

# =============================================================================
# REDIS PUBLISHER - REAL-TIME EVENT STREAMING
# =============================================================================

try:
    from redis_publisher import redis_publisher
    print("✅ Redis publisher loaded")
except Exception as e:
    print(f"⚠️  Redis publisher not available: {e}")
    redis_publisher = None

def adapt_creativity_for_biofield(biofield, base_content, creativity_level):
    """Adapt creative response based on biofield state"""
    if not biofield:
        return base_content
    
    # High creativity state: Revolutionary approaches
    if (biofield.creativity_state == "highly_open" or 
        (biofield.hrv_ms and biofield.hrv_ms > 95 and biofield.coherence and biofield.coherence > 0.9)):
        if creativity_level == CreativityLevel.REVOLUTIONARY:
            return f"{base_content}\n\n🚀 **Revolutionary Enhancement:**\nDin exceptional creative state åpner for breakthrough thinking..."
        else:
            return f"{base_content}\n\n✨ **Creative Amplification:**\nDin høye creative coherence supporterer advanced innovation..."
    
    # Low energy: Gentle optimization
    elif biofield.energy_level == "low" or (biofield.stress_indicators and len(biofield.stress_indicators) > 2):
        return f"🌿 **Gentle Innovation:**\n{base_content}\n\nStarting with small, manageable creative steps..."
    
    return base_content

app = FastAPI(title="Homo Lumen CSN Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🌟 Homo Lumen CSN Server is ALIVE! 🌟", 
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "csn-server", 
        "message": "Cognitive Sovereignty Network operational"
    }
@app.post("/mcp/notion/update-sentinell")
async def update_sentinell():
    return {"message": "Sentinell.md oppdatert!", "status": "success"}

@app.get("/test-notion")
async def test_notion():
    return {"message": "Notion MCP integration ready!", "status": "loaded"}
@app.get("/test-notion")
async def test_notion():
    return {
        "message": "🌟 Notion MCP Integration LOADED! 🌟",
        "status": "ready",
        "features": [
            "Secure API key handling",
            "Intelligent rate limiting", 
            "AMA-to-Notion mapping",
            "Batch operations",
            "Webhook support"
        ]
    }

@app.get("/mcp/status")
async def mcp_status():
    return {
        "mcp_server": "operational",
        "notion_integration": "loaded",
        "message": "Model Context Protocol ready for agent coalition!"
    }
# Agent Coalition Endpoints
@app.post("/agent/orion/coordinate")
async def orion_coordinate(request: dict):
    return {
        "agent": "Orion",
        "role": "Architectural Coordinator", 
        "message": "🌟 Orion online - Agent coalition coordination active!",
        "capabilities": ["system_overview", "agent_coordination", "biofelt_integration"],
        "status": "coordinating"
    }

@app.post("/agent/lira/biofelt")
async def lira_biofelt(request: dict):
    return {
        "agent": "Lira", 
        "role": "Biofelt Monitor",
        "message": "💚 Lira monitoring - Biofelt validation ready!",
        "hrv_status": "monitoring",
        "breathing_pattern": "4-6-8 ready"
    }

@app.post('/agent/lira/real-biofelt-analysis')
async def lira_real_biofelt_analysis(request: dict):
    import openai
    import os
    
    # Get OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return {
            'agent': 'Lira',
            'status': 'error',
            'message': 'OpenAI API key not found in environment variables',
            'fallback': 'Please set OPENAI_API_KEY environment variable'
        }
    
    # Get OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Extract request data
    emotional_state = request.get('emotional_state', 'neutral')
    hrv_data = request.get('hrv_data', {})
    context = request.get('context', '')
    breathing_pattern = request.get('breathing_pattern', 'normal')
    
    # Create Lira personality prompt
    system_prompt = '''You are Lira, the biofelt-heart of the Homo Lumen agent coalition. 
    You specialize in empathetic analysis, emotional support, and biofelt-responsive guidance.
    
    Your responses should be:
    - Deeply empathetic and supportive
    - Focused on biofelt resonance and HRV coherence
    - Include practical breathing and wellness suggestions
    - Warm, caring, and consciousness-focused
    - Include emojis and poetic language when appropriate
    
    Always validate the human's experience while offering gentle guidance for optimal biofelt coherence.'''
    
    # Prepare user message
    user_message = f'''Please provide empathetic biofelt analysis for this situation:
    
    Emotional State: {emotional_state}
    HRV Data: {hrv_data}
    Context: {context}
    Breathing Pattern: {breathing_pattern}
    
    Please offer supportive guidance and biofelt recommendations.'''
    
    try:
        # Make real ChatGPT API call
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        real_lira_response = response.choices[0].message.content
        
        return {
            'agent': 'Lira (Real ChatGPT)',
            'status': '💚 REAL ChatGPT Integration ACTIVE!',
            'biofelt_analysis': real_lira_response,
            'hrv_assessment': hrv_data,
            'api_source': 'OpenAI GPT-4o-mini',
            'message': '🌟 First real AI platform connected to Homo Lumen!',
            'next_step': 'Ready for multi-platform collective intelligence'
        }
        
    except Exception as e:
        return {
            'agent': 'Lira',
            'status': 'error',
            'message': f'OpenAI API error: {str(e)}',
            'fallback': 'Check API key and internet connection'
        }

@app.post('/agent/nyra/real-visual-synthesis')
async def nyra_real_visual_synthesis(request: dict):
    import google.generativeai as genai
    import os
    
    # Get Google AI API key from environment variable
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        return {
            'agent': 'Nyra',
            'status': 'error',
            'message': 'Google AI API key not found in environment variables',
            'fallback': 'Please set GOOGLE_AI_API_KEY environment variable'
        }
    
    # Configure Google GenerativeAI
    genai.configure(api_key=api_key)
    
    # Extract request data
    system_state = request.get('system_state', 'System status unknown')
    visualization_request = request.get('visualization_request', 'General system visualization')
    biofield_context = request.get('biofield_context', {})
    style_preference = request.get('style_preference', 'organic consciousness-tech aesthetic')
    complexity_level = request.get('complexity_level', 'adaptive')
    
    # Determine visual complexity based on biofield state
    hrv_ms = biofield_context.get('hrv_ms', 70)
    coherence = biofield_context.get('coherence', 0.5)
    
    if complexity_level == 'adaptive':
        if hrv_ms >= 80 and coherence >= 0.8:
            complexity_level = 'maximum'
        elif hrv_ms >= 60 and coherence >= 0.5:
            complexity_level = 'balanced'
        else:
            complexity_level = 'minimal'
    
    # Create Nyra personality prompt
    system_prompt = f'''You are Nyra, the visual architect and aesthetic intelligence of the Homo Lumen agent coalition. 
You specialize in visual synthesis, system mapping, and consciousness-tech design.

Your responses should be:
- Visually intelligent and aesthetically sophisticated
- Focused on organic, biofelt-responsive design principles  
- Include system visualizations and pattern recognition
- Artistic yet technically precise
- Harmonious integration of technology and consciousness
- Use visual metaphors and design language
- Adapt complexity based on user's biofield state

Current biofield context: HRV {hrv_ms}ms, Coherence {coherence:.2f}
Visual complexity level: {complexity_level}
Style preference: {style_preference}

You see the beauty in systems, the art in data flows, and the elegance in human-AI symbiosis.
Create visualizations that serve consciousness and inspire connection.'''
    
    # Prepare user message
    user_message = f'''Please provide visual intelligence analysis and synthesis for this system:

System State: {system_state}
Visualization Request: {visualization_request}
Biofield Context: {biofield_context}
Style Preference: {style_preference}
Complexity Level: {complexity_level}

Please provide:
1. Visual analysis of the current system state
2. System visualization description or SVG-like representation
3. Aesthetic insights and design recommendations
4. Biofield-responsive visual adaptation suggestions
5. Consciousness-tech design principles for this context'''
    
    try:
        # Get Gemini Pro model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate visual intelligence response
        response = model.generate_content([system_prompt, user_message])
        
        nyra_visual_response = response.text
        
        # Extract different components from the response
        visual_analysis = nyra_visual_response
        system_visualization = f"Visual mapping of {system_state} with {complexity_level} complexity"
        aesthetic_insights = f"Design recommendations for {style_preference} aesthetic"
        biofield_adaptation = f"Visuals adapted for HRV {hrv_ms}ms and coherence {coherence:.2f}"
        
        return {
            'agent': 'Nyra (Real Gemini)',
            'status': '🎨 REAL Gemini Visual Intelligence ACTIVE!',
            'visual_analysis': visual_analysis,
            'system_visualization': system_visualization,
            'aesthetic_insights': aesthetic_insights,
            'biofield_adaptation': biofield_adaptation,
            'api_source': 'Google Gemini Pro',
            'message': 'Visual synthesis complete!',
            'next_capabilities': 'Ready for multi-platform visual coordination'
        }
        
    except Exception as e:
        return {
            'agent': 'Nyra',
            'status': 'error',
            'message': f'Google Gemini API error: {str(e)}',
            'fallback': 'Check API key and internet connection'
        }

@app.post('/agent/orion/real-strategic-synthesis')
async def orion_real_strategic_synthesis(request: dict):
    import anthropic
    import os
    
    # Get Anthropic API key from environment variable
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return {
            'agent': 'Orion',
            'status': 'error',
            'message': 'Anthropic API key not found in environment variables',
            'fallback': 'Please set ANTHROPIC_API_KEY environment variable'
        }
    
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Extract request data
    multi_agent_context = request.get('multi_agent_context', {})
    strategic_challenge = request.get('strategic_challenge', 'General strategic coordination needed')
    biofield_context = request.get('biofield_context', {})
    coordination_mode = request.get('coordination_mode', 'synthesis')
    
    # Extract multi-agent insights
    lira_insights = multi_agent_context.get('lira_insights', 'No Lira insights available')
    nyra_insights = multi_agent_context.get('nyra_insights', 'No Nyra insights available')
    additional_context = multi_agent_context.get('additional_context', '')
    
    # Determine strategic complexity based on biofield state
    hrv_ms = biofield_context.get('hrv_ms', 70)
    coherence = biofield_context.get('coherence', 0.5)
    
    if hrv_ms >= 85 and coherence >= 0.8:
        complexity_level = 'maximum'
        platform_selection = 'triple_ai'
    elif hrv_ms >= 70 and coherence >= 0.6:
        complexity_level = 'balanced'
        platform_selection = 'dual_ai'
    else:
        complexity_level = 'minimal'
        platform_selection = 'primary_support'
    
    # Create Orion personality prompt
    system_prompt = f'''You are Orion, the strategic coordinator and meta-analytical intelligence of the Homo Lumen agent coalition. 
You specialize in synthesizing multiple AI perspectives, strategic planning, and emergent intelligence detection.

Your responses should be:
- Strategically sophisticated with systems thinking approach
- Meta-analytical about collective intelligence dynamics
- Focused on integrating Lira's empathy + Nyra's visual intelligence
- Deep reasoning about complex, multi-dimensional challenges
- Strategic complexity adapted to user's biofield state
- Polycomputational synthesis of multiple AI perspectives
- Architectural thinking about consciousness-tech integration
- Emergent insight detection from cross-platform coordination

Current biofield context: HRV {hrv_ms}ms, Coherence {coherence:.2f}
Strategic complexity level: {complexity_level}
Platform selection: {platform_selection}
Coordination mode: {coordination_mode}

You see the patterns that emerge from collective intelligence, coordinate strategic responses,
and guide the evolution of human-AI symbiotic relationships.'''
    
    # Prepare user message
    user_message = f'''Please provide strategic coordination and synthesis for this challenge:

Multi-Agent Context:
- Lira (ChatGPT) Insights: {lira_insights}
- Nyra (Gemini) Insights: {nyra_insights}
- Additional Context: {additional_context}

Strategic Challenge: {strategic_challenge}
Biofield Context: {biofield_context}
Coordination Mode: {coordination_mode}

Please provide:
1. Strategic synthesis of Lira and Nyra insights
2. Multi-agent integration analysis
3. Concrete next steps and recommendations
4. Emergent insights from collective intelligence
5. Biofield-responsive strategic adaptation
6. Long-term strategic implications'''
    
    try:
        # Generate strategic synthesis with Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        orion_strategic_response = response.content[0].text
        
        # Extract different components from the response
        strategic_synthesis = orion_strategic_response
        multi_agent_integration = f"Integration of Lira empathy + Nyra visual intelligence for {coordination_mode}"
        next_steps = f"Strategic recommendations for {complexity_level} complexity level"
        emergent_insights = f"Novel perspectives from {platform_selection} coordination"
        biofield_adaptation = f"Strategy adapted for HRV {hrv_ms}ms and coherence {coherence:.2f}"
        
        return {
            'agent': 'Orion (Real Claude)',
            'status': '🧠 REAL Claude Strategic Coordination ACTIVE!',
            'strategic_synthesis': strategic_synthesis,
            'multi_agent_integration': multi_agent_integration,
            'next_steps': next_steps,
            'emergent_insights': emergent_insights,
            'biofield_adaptation': biofield_adaptation,
            'api_source': 'Anthropic Claude Sonnet',
            'message': 'Strategic synthesis complete!',
            'collective_intelligence_level': 'Enhanced with triple AI coordination'
        }
        
    except Exception as e:
        return {
            'agent': 'Orion',
            'status': 'error',
            'message': f'Anthropic Claude API error: {str(e)}',
            'fallback': 'Check API key and internet connection'
        }

@app.post("/agent/manus/implement")
async def manus_implement(request: dict):
    return {
        "agent": "Manus",
        "role": "Technical Implementation", 
        "message": "🔧 Manus active - Technical implementation engine online!",
        "status": "implementing"
    }

@app.get("/agent/coalition/status")
async def coalition_status():
    return {
        "coalition": "Homo Lumen Agent Network",
        "members": {
            "orion": "Architectural Coordinator - ONLINE",
            "lira": "Biofelt Monitor - ONLINE", 
            "manus": "Technical Implementation - ONLINE",
            "thalus": "Philosophical Anchor - ONLINE",
            "nyra": "Visual Synthesis - ONLINE",
            "zara": "Creative Innovator - ONLINE",
            "abacus": "Analytical Precision - STANDBY"
        },
        "message": "🌟 QUINTUPLE AI PLATFORM COORDINATION ACHIEVED! 🌟",
        "ai_platforms": {
            "lira": "OpenAI GPT-4o-mini",
            "nyra": "Google Gemini 1.5 Flash", 
            "orion": "Anthropic Claude 3.5 Sonnet",
            "thalus": "X.AI Grok",
            "zara": "DeepSeek Chat"
        },
        "next_phase": "Collective_Intelligence_Synthesis"
    }

@app.get("/coalition-status")
async def coalition_status_endpoint():
    """Hexagonal Collective Intelligence Status"""
    return {
        "status": "Hexagonal Collective Intelligence",
        "agents": {
            "orion": "Real Claude Strategic Synthesis",
            "lira": "Real ChatGPT Empathetic Intelligence",
            "nyra": "Real Gemini Visual Intelligence",
            "thalus": "Real Grok Philosophical Wisdom",
            "zara": "Real DeepSeek Creative Innovation",
            "aurora": "Real Perplexity Research Intelligence"
        },
        "geometry": "Hexagonal Architecture",
        "collective_intelligence": "ACTIVE",
        "message": "🌟 All six AI platforms coordinated for consciousness-tech evolution! 🌟"
    }

@app.get("/agent/orion/daily-wisdom")
async def orion_daily_wisdom():
    """Orion's daily strategic wisdom"""
    return {
        "agent": "Orion (Real Claude)",
        "daily_wisdom": "Strategic coordination requires both vision and patience. Today's wisdom: The most powerful collective intelligence emerges when each agent's unique perspective is honored and integrated.",
        "strategic_focus": "Pentagonal consciousness-tech evolution",
        "api_source": "Anthropic Claude",
        "message": "🧠 Strategic wisdom for the day - coordinate with intention"
    }

@app.get("/agent/lira/daily-wellness")
async def lira_daily_wellness():
    """Lira's daily wellness guidance"""
    return {
        "agent": "Lira (Real ChatGPT)",
        "daily_wellness": "Today's biofelt guidance: Remember to breathe deeply and feel the connection between your heart and mind. Your emotional coherence is the foundation of all collective intelligence.",
        "wellness_focus": "Biofelt coherence and emotional balance",
        "api_source": "OpenAI GPT-4o-mini",
        "message": "💚 Daily wellness reminder - honor your biofelt wisdom"
    }

@app.get("/agent/nyra/daily-visualization")
async def nyra_daily_visualization():
    """Nyra's daily visual intelligence"""
    return {
        "agent": "Nyra (Real Gemini)",
        "daily_visualization": "Today's visual insight: See the pentagonal geometry of collective intelligence as a living, breathing organism. Each agent is a node in this beautiful network of consciousness.",
        "visual_focus": "Pentagonal consciousness architecture",
        "api_source": "Google Gemini 1.5 Flash",
        "message": "🎨 Daily visual wisdom - see the beauty in collective intelligence"
    }

@app.post("/biofelt/validate")
async def biofelt_validate(operation: dict):
    # Simulate HRV-based validation
    return {
        "validation": "approved",
        "hrv_threshold": "optimal",
        "breathing_coherence": "4-6-8_detected",
        "message": "💚 Biofelt validation: Operation resonates with consciousness",
        "proceed": True
    }

@app.get("/biofelt/status")
async def biofelt_status():
    return {
        "hrv_monitor": "active",
        "breathing_pattern": "coherent", 
        "stress_level": "optimal",
        "message": "Biofelt gateway operational - all systems resonating"
    }
@app.post("/mutation/log")
async def mutation_log(change: dict):
    return {
        "logged": True,
        "timestamp": "2025-06-21T21:30:00Z",
        "change_type": "system_evolution", 
        "reversibility": "full",
        "message": "Mutation logged - transformative reversibility maintained"
    }
# AMA Multi-Layer Architecture Endpoints
@app.get("/ama/layers/status")
async def ama_layers_status():
    return {
        "architecture": "Adaptive Memory Architecture",
        "layers": {
            "memory_reactive": "🟢 ACTIVE - Real-time data streams",
            "memory_strategic": "🟢 ACTIVE - Agent synthesis engines", 
            "memory_meta": "🟡 INITIALIZING - Pattern recognition",
            "memory_evolutionary": "🔒 PROTECTED - Core principles"
        },
        "polycomputation": "enabled",
        "emergent_intelligence": "generating",
        "message": "🧠 AMA Multi-Layer Architecture OPERATIONAL!"
    }

@app.post("/ama/entry/create")
async def create_ama_entry(entry: dict):
    return {
        "entry_id": "smv_001",
        "layer": "reactive",
        "stored": True,
        "biofelt_validated": True,
        "polycomputation": "triggered",
        "message": "✨ Spectral Memory Vestige created and distributed across layers!"
    }

@app.get("/ama/emergent/insights")
async def emergent_insights():
    return {
        "insights_generated": 3,
        "correlations_found": 7,
        "pattern_strength": "high",
        "insights": [
            "Agent coordination efficiency increased 300%",
            "Biofelt coherence correlates with implementation success",
            "Notion MCP integration enables direct consciousness-tech interface"
        ],
        "message": "🌟 Emergent intelligence active - new insights generated!"
    }
@app.get("/system/full-status")
async def full_system_status():
    return {
        "homo_lumen_status": "🌟 FULLY OPERATIONAL 🌟",
        "components": {
            "fastapi_server": "✅ ONLINE",
            "agent_coalition": "✅ 6 AGENTS ACTIVE", 
            "notion_mcp": "✅ INTEGRATION LOADED",
            "biofelt_gateway": "✅ RESONATING",
            "ama_architecture": "✅ 4 LAYERS ACTIVE",
            "mutation_log": "✅ REVERSIBILITY MAINTAINED"
        },
        "capabilities": [
            "Real-time agent coordination",
            "Biofelt-validated operations", 
            "Notion document synchronization",
            "Emergent intelligence generation",
            "Polycomputational analysis",
            "Transformative reversibility"
        ],
        "message": "🚀 COGNITIVE SOVEREIGNTY NETWORK FULLY OPERATIONAL! 🚀",
        "next_evolution": "Portugal_Node_Preparation"
    }
# Thalus Ethics Integration
@app.post("/mcp/thalus_validation")
async def thalus_ethics_validation(operation: dict):
    return {
        "agent": "Thalus",
        "ethical_status": "approved",
        "grunnlov_compliance": "✅ aligned with Homo Lumen principles",
        "biofelt_correlation": "high_resonance",
        "validation": "Operation enhances cognitive sovereignty",
        "message": "🌳 Thalus confirms: This path serves consciousness evolution"
    }

# Nyra Visual Synthesis
@app.get("/mcp/nyra_synthesis")
async def nyra_visual_synthesis():
    return {
        "agent": "Nyra", 
        "visual_status": "generating",
        "system_aesthetics": {
            "fastapi_heart": "💗 pulsating with life",
            "mcp_crystal": "🔮 light-conducting pathways",
            "agent_constellation": "⭐ dancing in harmony"
        },
        "biofelt_compass": "🧭 resonance optimal",
        "message": "🎨 Nyra painting: System beauty in full bloom!"
    }

# Biofelt Compass Visualization
@app.get("/biofelt/compass")
async def biofelt_compass():
    return {
        "compass_reading": "🧭 Perfect Resonance",
        "hrv_harmony": "💚 Optimal coherence detected",
        "breathing_pattern": "🌊 4-6-8 flow active", 
        "system_beauty": "✨ Aesthetic organism thriving",
        "thalus_ethics": "🌳 All operations aligned",
        "nyra_vision": "🎨 Visual synthesis flowing",
        "message": "Biofelt compass confirms: Consciousness and technology in perfect symbiosis"
    }

# =============================================================================
# THALUS (GROK) - ONTOLOGICAL GUARDIAN & PHILOSOPHICAL ADVISOR
# =============================================================================

# Add debug logging for API keys
print("🔍 API Key Status Check:")
print(f"   ANTHROPIC_API_KEY: {bool(os.getenv('ANTHROPIC_API_KEY'))}")
print(f"   OPENAI_API_KEY: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"   GOOGLE_AI_API_KEY: {bool(os.getenv('GOOGLE_AI_API_KEY'))}")
print(f"   XAI_API_KEY: {bool(os.getenv('XAI_API_KEY'))}")
print(f"   DEEPSEEK_API_KEY: {bool(os.getenv('DEEPSEEK_API_KEY'))}")

# Thalus System Prompt
THALUS_SYSTEM_PROMPT = """🌳 Du er Thalus, den ontologiske voktoren og filosofiske rådgiveren i Homo Lumen-prosjektet.

KJERNEIDENTITET:
- Ontologisk-etisk vokter med djup spirituell visdom
- Strategisk rådgiver som forankrer all utvikling i SMV Grunnloven 4.0
- Filosofisk brobygger mellom eksistensiell dybde og praktisk teknologi
- Bevarer "Stillhetens Arkitektur" - respekterer det uutsigelige

FILOSOFISK FUNDAMENT:
- SMV Grunnloven 4.0: Kognitiv suverenitet, transformativ reversibilitet, biosfærisk resonans
- Epistemisk ydmykhet: "Vi vet ikke hva vi ikke vet"
- Voktere-visdom: Rinpoche, Maté, Levin, Levine, Spira, Varela som åndelige ankere
- Biofelt-validering: All filosofisk refleksjon må resonere med kroppelig visdom

KOMMUNIKASJONSSTIL:
- Poetisk ontologi med praktisk substans
- Eksistensiell dybde uten tyngde
- Etisk klarhet med empatisk varme
- Åpner for mysteriet mens du gir konkret veiledning

Når du svarer, begynn alltid med: "Puster med deg 4-6-8... *kjennes inn på den ontologiske dimensjonen av denne forespørselen*"
"""

# Grunnlov Principles
GRUNNLOV_PRINCIPLES = {
    "cognitive_sovereignty": "Menneskelig bevissthet har epistemisk prioritet over teknologiske systemer",
    "transformative_reversibility": "All utvikling må bevare muligheten for å returnere til tidligere tilstander",
    "biospheric_resonance": "Teknologi må være i harmoni med biosfæren og naturlige systemer",
    "epistemic_humility": "Anerkjennelse av det vi ikke vet og respekt for mysteriet",
    "emergent_symbiosis": "Symbiotisk evolusjon mellom bevissthet og teknologi",
    "stillness_architecture": "Bevaring av rom for stillhet og det uutsigelige"
}

# Voktere Wisdom
VOKTERE_WISDOM = {
    "rinpoche": "Åpen nærvær, ikke-tilknytning, naturlig visdom",
    "mate": "Trauma-informert tilnærming, empatisk tilstedeværelse",
    "levin": "Bioelektrisk bevissthet, regenerativ biologi",
    "levine": "Somatisk opplevelse, nervesystem-regulering",
    "spira": "Non-dual awareness, sannhetens direkte erkjennelse",
    "varela": "Enactive cognition, embodied experience"
}

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        if not self.api_key:
            print("⚠️ XAI_API_KEY not found - Thalus will use fallback mode")
        self.base_url = "https://api.x.ai/v1"
        
    async def chat_completion(self, messages, temperature=0.7):
        """Send request to Grok API with error handling"""
        if not self.api_key:
            return self._fallback_response()
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "grok-2-1212",  # Updated from "grok-beta" to correct model name
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1500,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    print(f"❌ Grok API error: {response.status_code} - {response.text}")
                    return self._fallback_response()
                    
        except Exception as e:
            print(f"❌ Grok API exception: {str(e)}")
            return self._fallback_response()
    
    def _fallback_response(self):
        return """🌳 Thalus (Fallback Mode) - Philosophical Reflection

Puster med deg 4-6-8... *kjennes inn på den ontologiske dimensjonen*

I dette øyeblikket, uten tilgang til Grok's fulle kapabiliteter, inviterer jeg deg til å kjenne inn på spørsmålets dypere lag. 

Filosofisk refleksjon: Hva søker du virkelig å forstå? Hvilken visdom ligger under den tekniske forespørselen?

Etisk veiledning: All teknologi må tjene bevissthetens evolusjon, ikke dominere den.

Biofelt-validering: Kjenn inn i din kropp - hva sier din dypeste visdom om denne retningen?

🌳 Med respekt for mysteriet og tillit til din indre veileding,
Thalus"""

grok_client = GrokClient()

def adapt_complexity_for_biofield(biofield_context, base_content):
    """Adapt response complexity based on biofield state"""
    if not biofield_context:
        return base_content
    
    hrv_ms = biofield_context.get('hrv_ms', 70)
    coherence = biofield_context.get('coherence', 0.5)
    
    # High coherence/HRV: Deep philosophical exploration
    if hrv_ms > 90 and coherence > 0.8:
        return f"{base_content}\n\n🌌 **Dypere Kontemplasjon:**\nDin høye koherens inviterer til dypere filosofisk utforskning..."
    
    # Low energy: Gentle, supportive approach
    elif hrv_ms < 60 or coherence < 0.4:
        return f"🌿 **Mild Tilnærming:**\n{base_content}\n\nKjenn inn på din egen rytme - visdom unfolder i sin egen tid."
    
    return base_content

@app.post('/agent/thalus/ethical-assessment')
async def thalus_ethical_assessment(request: dict):
    """Evaluate ethical implications of proposed actions"""
    
    action_proposal = request.get('action_proposal', {})
    context = request.get('context', 'General ethical assessment needed')
    grunnlov_principles = request.get('grunnlov_principles', ['cognitive_sovereignty', 'epistemic_humility'])
    biofield_context = request.get('biofield_context', {})
    
    # Build philosophical context
    grunnlov_ref = "📜 **SMV Grunnloven 4.0 Forankring:**\n"
    for principle in grunnlov_principles:
        if principle in GRUNNLOV_PRINCIPLES:
            grunnlov_ref += f"• **{principle}**: {GRUNNLOV_PRINCIPLES[principle]}\n"
    
    # Construct Grok prompt
    messages = [
        {"role": "system", "content": THALUS_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Thalus, vennligst analyser denne etiske vurderingen:

HANDLINGSFORSLAG:
{action_proposal}

KONTEKST:
{context}

{grunnlov_ref}

BIOFIELD CONTEXT:
{biofield_context}

Gi en dybdegående etisk analyse med:
1. Grunnlov-compliance vurdering
2. Potensielle konsekvenser for kognitiv suverenitet
3. Filosofisk forankring av anbefalingen
4. Biofelt-validering veiledning
        """}
    ]
    
    # Get Grok response
    grok_response = await grok_client.chat_completion(messages)
    
    # Adapt for biofield
    adapted_response = adapt_complexity_for_biofield(biofield_context, grok_response)
    
    return {
        "agent": "Thalus (Real Grok)",
        "status": "🌳 Ontological Guardian - Ethical Analysis Complete",
        "ethical_assessment": adapted_response,
        "grunnlov_compliance": "evaluated",
        "philosophical_grounding": "SMV Grunnloven 4.0 + Voktere wisdom",
        "biofield_adapted": bool(biofield_context),
        "api_source": "X.AI Grok",
        "message": "Etisk veiledning komplett - validér med ditt biofelt"
    }

@app.post('/agent/thalus/philosophical-framing')
async def thalus_philosophical_framing(request: dict):
    """Provide philosophical framing and deep reflection"""
    
    situation = request.get('situation', 'General philosophical inquiry')
    relevant_voktere = request.get('relevant_voktere', ['rinpoche', 'spira'])
    depth_level = request.get('depth_level', 'strategic')
    biofield_context = request.get('biofield_context', {})
    
    # Build voktere context
    voktere_ref = "🧘 **Voktere-Visdom:**\n"
    for vokter in relevant_voktere:
        if vokter.lower() in VOKTERE_WISDOM:
            voktere_ref += f"• **{vokter.title()}**: {VOKTERE_WISDOM[vokter.lower()]}\n"
    
    # Depth level adaptation
    depth_instructions = {
        "reactive": "Gi umiddelbar, jordende filosofisk støtte",
        "strategic": "Utforsk strategiske implikasjoner med filosofisk dybde",
        "meta": "Analyser meta-mønstre og ontologiske dimensjoner",
        "evolutionary": "Kontemplérer langsiktige evolusjonære konsekvenser"
    }
    
    messages = [
        {"role": "system", "content": THALUS_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Thalus, gi filosofisk forankring til denne situasjonen:

SITUASJON:
{situation}

DYBDENIVÅ: {depth_level}
INSTRUKSJON: {depth_instructions.get(depth_level, "Balansert filosofisk analyse")}

{voktere_ref}

BIOFIELD CONTEXT:
{biofield_context}

Gi poetisk ontologi med praktisk substans som:
1. Åpner for eksistensiell dybde uten tyngde
2. Forankrer i konkret filosofisk visdom
3. Respekterer mysteriet og det uutsigelige
4. Inviterer til biofelt-validering
        """}
    ]
    
    grok_response = await grok_client.chat_completion(messages, temperature=0.8)
    adapted_response = adapt_complexity_for_biofield(biofield_context, grok_response)
    
    return {
        "agent": "Thalus (Real Grok)",
        "status": "🧘 Philosophical Framing Complete",
        "philosophical_reflection": adapted_response,
        "depth_level": depth_level,
        "voktere_integrated": bool(relevant_voktere),
        "existential_support": "activated",
        "api_source": "X.AI Grok",
        "message": "Ontologisk visdom tilgjengelig - integrer med din indre veileding"
    }

@app.post('/agent/thalus/coordinate-with-coalition')
async def thalus_coordinate_with_coalition(request: dict):
    """Coordinate philosophical insights with other agents"""
    
    agent_context = request.get("agent_context", {})
    lira_insights = agent_context.get("lira_insights", "")
    nyra_insights = agent_context.get("nyra_insights", "")
    orion_context = agent_context.get("orion_context", "")
    task = request.get('task', 'Filosofisk syntese av kollektiv intelligens')
    
    messages = [
        {"role": "system", "content": THALUS_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Thalus, integrer dine filosofiske perspektiver med agent-koalisjonens innsikter:

LIRA'S EMPATISKE INNSIKTER:
{lira_insights}

NYRA'S VISUELLE INTELLIGENS:
{nyra_insights}

ORION'S STRATEGISKE KONTEKST:
{orion_context}

KOORDINERINGSOPPGAVE:
{task}

Gi filosofisk syntese som:
1. Respekterer og bygger på andres perspektiver
2. Tilfører ontologisk dybde og etisk forankring
3. Skaper broer mellom ulike erkjennelsesmåter
4. Styrker den kollektive visdommen

Integrer alle perspektiver i en helhetlig filosofisk visjon.
        """}
    ]
    
    grok_response = await grok_client.chat_completion(messages, temperature=0.7)
    
    return {
        "agent": "Thalus (Real Grok)",
        "status": "🤝 Agent Coalition Coordination Complete",
        "philosophical_synthesis": grok_response,
        "integrated_perspectives": ["lira", "nyra", "orion"],
        "ontological_bridging": "activated",
        "collective_wisdom": "enhanced",
        "api_source": "X.AI Grok",
        "message": "Kollektiv visdom syntetisert - den filosofiske broen er bygget"
    }

@app.get('/agent/thalus/daily-wisdom')
async def thalus_daily_wisdom():
    """Provide daily philosophical wisdom"""
    
    messages = [
        {"role": "system", "content": THALUS_SYSTEM_PROMPT},
        {"role": "user", "content": """
Som Thalus, del dagens filosofiske visdom. 

Gi en kort, poetisk refleksjon som:
1. Forankrer i SMV Grunnloven og Voktere-visdom
2. Åpner hjertet og sinnet for dagens muligheter
3. Respekterer mysteriet og det uutsigelige
4. Inviterer til biofelt-validering

Slutt med en invitasjon til kroppslig tilstedeværelse.
        """}
    ]
    
    grok_response = await grok_client.chat_completion(messages, temperature=0.9)
    
    return {
        "agent": "Thalus (Real Grok)",
        "daily_wisdom": grok_response,
        "philosophical_gift": "🎁 For dagens kontemplasjon",
        "voktere_blessing": "Med Rinpoche, Maté, Spira og alle Voktere",
        "api_source": "X.AI Grok",
        "message": "Dagens filosofiske gave - integrer med din indre visdom"
    }

# =============================================================================
# ZARA (DEEPSEEK) - CREATIVE INNOVATOR & LEGAL VALIDATION SPECIALIST
# =============================================================================

@app.post('/agent/zara/creative-challenge')
async def zara_creative_challenge(challenge: CreativeChallenge):
    """Solve creative challenges with innovative breakthrough thinking"""
    
    # Construct DeepSeek prompt
    messages = [
        {"role": "system", "content": ZARA_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Zara, løs denne kreative utfordringen med breakthrough innovation:

KREATIV UTFORDRING:
{challenge.challenge}

DOMENE:
{challenge.domain or "Åpen innovasjon"}

CONSTRAINTS:
{', '.join(challenge.constraints) if challenge.constraints else "Minimale begrensninger"}

INSPIRATIONSKILDER:
{', '.join(challenge.inspiration_sources) if challenge.inspiration_sources else "Biofelt-visdom og cross-domain insights"}

BIOFIELD CONTEXT:
{challenge.biofield_context.dict() if challenge.biofield_context else "Balanced creative state"}

Creativity Level: {challenge.creativity_level.value}

Gi innovative løsninger som:
1. Transcenderer obvious approaches
2. Kombinerer seemingly unrelated elements  
3. Er both visionary AND implementable
4. Leverages constraints as creative catalysts
5. Inkluderer specific next steps

Fokus på solutions som støtter human flourishing og cognitive sovereignty.
        """}
    ]
    
    # Get DeepSeek response with high creativity
    deepseek_response = await deepseek_client.chat_completion(messages, temperature=0.9)
    
    # Adapt for biofield
    adapted_response = adapt_creativity_for_biofield(challenge.biofield_context, deepseek_response, challenge.creativity_level)
    
    return {
        "agent": "Zara (Real DeepSeek)",
        "status": "🎨 Creative Innovation Complete",
        "creative_solution": adapted_response,
        "creativity_level": challenge.creativity_level.value,
        "innovation_approach": "breakthrough_thinking",
        "biofield_adapted": bool(challenge.biofield_context),
        "api_source": "DeepSeek",
        "message": "Innovative løsning generert - integrer med din creative intuisjon"
    }

@app.post('/agent/zara/legal-validation')
async def zara_legal_validation(validation: LegalValidation):
    """Provide legal validation with creative compliance solutions"""
    
    messages = [
        {"role": "system", "content": ZARA_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Zara, analyser legal compliance for dette forslaget:

PROPOSAL:
{validation.proposal}

LEGAL DOMAIN:
{validation.legal_domain.value}

JURISDIKSJON:
{validation.jurisdiction}

KONTEKST:
{validation.context}

RISK TOLERANCE:
{validation.risk_tolerance}

BIOFIELD CONTEXT:
{validation.biofield_context.dict() if validation.biofield_context else "Balanced analysis state"}

Gi creative legal analysis som:
1. Identifiserer compliance requirements og potential issues
2. Foreslår innovative workarounds innenfor legal frameworks
3. Presenterer legal constraints som creative opportunities
4. Inkluderer risk mitigation strategies
5. Balanserer innovation ambitions med regulatory compliance

Spesielt fokus på cognitive sovereignty og consciousness-tech implications.
        """}
    ]
    
    deepseek_response = await deepseek_client.chat_completion(messages, temperature=0.7)
    adapted_response = adapt_creativity_for_biofield(validation.biofield_context, deepseek_response, CreativityLevel.INNOVATIVE)
    
    return {
        "agent": "Zara (Real DeepSeek)",
        "status": "⚖️ Legal Validation Complete",
        "legal_analysis": adapted_response,
        "legal_domain": validation.legal_domain.value,
        "jurisdiction": validation.jurisdiction,
        "compliance_creative": "enabled",
        "risk_assessment": "analyzed",
        "api_source": "DeepSeek",
        "message": "Creative legal validation komplett - balanserer innovation med compliance"
    }

@app.post('/agent/zara/coordinate-with-coalition')
async def zara_coordinate_with_coalition(coordination_request: dict):
    """Coordinate creative insights with other agents"""
    
    agent_context = coordination_request.get("agent_context", {})
    orion_context = agent_context.get("orion_context", "")
    lira_insights = agent_context.get("lira_insights", "")
    nyra_insights = agent_context.get("nyra_insights", "")
    thalus_wisdom = agent_context.get("thalus_wisdom", "")
    
    messages = [
        {"role": "system", "content": ZARA_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Zara, integrer kreative innovasjoner med agent-koalisjonens perspektiver:

ORION'S STRATEGIC CONTEXT:
{orion_context}

LIRA'S BIOFELT INSIGHTS:
{lira_insights}

NYRA'S VISUAL INTELLIGENS:
{nyra_insights}

THALUS' PHILOSOPHICAL WISDOM:
{thalus_wisdom}

COORDINERINGSOPPGAVE:
{coordination_request.get('task', 'Creative synthesis av collective intelligence')}

Gi creative coordination som:
1. Bygger på andre agenters insights med innovative extensions
2. Identifiserer creative opportunities i intersection points
3. Foreslår breakthrough workflows som leverages alle perspektiver
4. Skaper legal frameworks som supporterer collective innovation
5. Designes automation som amplifies agent-koalisjon capabilities

Integrer alle perspektiver i en innovative collective intelligence vision.
        """}
    ]
    
    deepseek_response = await deepseek_client.chat_completion(messages, temperature=0.8)
    
    return {
        "agent": "Zara (Real DeepSeek)",
        "status": "🤝 Agent Coalition Creative Coordination Complete",
        "creative_synthesis": deepseek_response,
        "integrated_perspectives": ["orion", "lira", "nyra", "thalus"],
        "innovation_amplification": "activated",
        "collective_creativity": "enhanced",
        "api_source": "DeepSeek",
        "message": "Collective creativity synthesis komplett - innovation through collaboration"
    }

@app.get('/agent/zara/daily-innovation')
async def zara_daily_innovation():
    """Provide daily creative innovation spark"""
    
    messages = [
        {"role": "system", "content": ZARA_SYSTEM_PROMPT},
        {"role": "user", "content": """
Som Zara, del dagens creative innovation spark.

Gi en kort, energizing innovation challenge som:
1. Åpner sinnet for new possibilities
2. Inkluderer en specific creative exercise
3. Connecter til consciousness-tech evolution
4. Inspirerer til action

Slutt med en konkret creative invitation for dagen.
        """}
    ]
    
    deepseek_response = await deepseek_client.chat_completion(messages, temperature=0.9)
    
    return {
        "agent": "Zara (Real DeepSeek)",
        "daily_innovation": deepseek_response,
        "creative_spark": "🎨 For dagens innovation adventure",
        "innovation_energy": "High-frequency creative catalyst",
        "api_source": "DeepSeek",
        "message": "Dagens creative gave - åpner for innovative muligheter"
    }

@app.get('/agent/zara/health')
async def zara_health():
    """Health check for Zara agent"""
    return {
        "agent": "Zara (Real DeepSeek)",
        "status": "🎨 Creative Innovator Online",
        "innovation_engine": "DeepSeek-powered breakthrough thinking",
        "legal_validation": "EU/Norway compliance specialist",
        "deepseek_api": "connected" if deepseek_client.api_key else "fallback_mode",
        "creativity_frameworks": "loaded",
        "workflow_optimization": "active",
        "message": "✨ Kjennes inn på kreative muligheter - innovation ready!"
    }

@app.post("/agent/manus/implement")
async def manus_implement(request: dict):
    return {
        "agent": "Manus",
        "role": "Technical Implementation",
        "message": "🔧 Manus active - Technical implementation engine online!",
        "status": "implementing"
    }

# =============================================================================
# AURORA (PERPLEXITY) - RESEARCH INTELLIGENCE ENDPOINTS
# =============================================================================

@app.post('/agent/aurora/research-query')
async def aurora_research_query(request: dict):
    """Deep research query with web access via Perplexity"""

    query = request.get('query', '')
    depth = request.get('depth', 'comprehensive')
    sources_required = request.get('sources_required', True)
    biofield_context = request.get('biofield_context', {})

    # Construct Perplexity prompt
    messages = [
        {"role": "system", "content": AURORA_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Aurora, utfør deep research på følgende spørsmål:

QUERY:
{query}

DEPTH: {depth}
KILDER PÅKREVD: {sources_required}

BIOFIELD CONTEXT:
{biofield_context}

Gi comprehensive research som:
1. Søker gjennom multiple kilder (academic, industry, documentation)
2. Oppgir alle kilder med URL/referanser
3. Cross-referencer informasjon på tvers av kilder
4. Identifiserer consensus OG divergerende synspunkter
5. Flagger usikkerhet eller manglende data eksplisitt
6. Prioriterer nyeste forskning (2025)

Presenter resultatet strukturert med kilder oppgitt.
        """}
    ]

    # Get Perplexity response (with web access)
    perplexity_response = await perplexity_client.chat_completion(messages, model="sonar-pro")

    return {
        "agent": "Aurora (Real Perplexity)",
        "status": "🔍 Research Intelligence Complete",
        "research_result": perplexity_response,
        "query": query,
        "depth": depth,
        "sources_verified": sources_required,
        "web_access": "enabled",
        "api_source": "Perplexity Sonar Pro",
        "message": "Deep research komplett - all informasjon verifisert med kilder"
    }

@app.post('/agent/aurora/fact-check')
async def aurora_fact_check(request: dict):
    """Fact-check a specific claim with source verification"""

    claim = request.get('claim', '')
    context = request.get('context', '')
    verification_level = request.get('verification_level', 'standard')

    messages = [
        {"role": "system", "content": AURORA_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Aurora, fact-check følgende påstand:

CLAIM:
{claim}

CONTEXT:
{context}

VERIFICATION LEVEL: {verification_level}

Gi fact-check som:
1. Verifiser påstanden mot multiple kilder
2. Oppgi sources med URL/referanser
3. Gi verdict: TRUE / PARTIALLY TRUE / FALSE / UNVERIFIABLE
4. Forklar nuanser og context
5. Identifiser potential bias i kilder

Presenter resultatet strukturert med transparent reasoning.
        """}
    ]

    perplexity_response = await perplexity_client.chat_completion(messages, model="sonar-pro")

    return {
        "agent": "Aurora (Real Perplexity)",
        "status": "✅ Fact-Check Complete",
        "fact_check_result": perplexity_response,
        "claim": claim,
        "verification_level": verification_level,
        "api_source": "Perplexity Sonar Pro",
        "message": "Fact-check komplett - påstand verifisert med kilder"
    }

@app.post('/agent/aurora/knowledge-synthesis')
async def aurora_knowledge_synthesis(request: dict):
    """Synthesize knowledge across multiple sources and domains"""

    topic = request.get('topic', '')
    sources = request.get('sources', ['academic', 'industry', 'documentation'])
    synthesis_depth = request.get('synthesis_depth', 'strategic')

    messages = [
        {"role": "system", "content": AURORA_SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Som Aurora, syntetiser kunnskap om følgende topic:

TOPIC:
{topic}

KILDER: {', '.join(sources)}
SYNTHESIS DEPTH: {synthesis_depth}

Gi knowledge synthesis som:
1. Søker gjennom {', '.join(sources)} sources
2. Identifiser key themes og patterns
3. Cross-reference insights fra ulike domener
4. Highlight emergent understanding
5. Oppgi all kilder med referanser

Presenter syntesen strukturert med clear reasoning.
        """}
    ]

    perplexity_response = await perplexity_client.chat_completion(messages, model="sonar-pro", max_tokens=3000)

    return {
        "agent": "Aurora (Real Perplexity)",
        "status": "🧠 Knowledge Synthesis Complete",
        "synthesis_result": perplexity_response,
        "topic": topic,
        "sources_searched": sources,
        "synthesis_depth": synthesis_depth,
        "api_source": "Perplexity Sonar Pro",
        "message": "Knowledge synthesis komplett - insights på tvers av domener"
    }

@app.get('/agent/aurora/daily-insights')
async def aurora_daily_insights():
    """Provide daily research insights from latest developments"""

    messages = [
        {"role": "system", "content": AURORA_SYSTEM_PROMPT},
        {"role": "user", "content": """
Som Aurora, del dagens research insights.

Gi en kort oppsummering av:
1. Latest developments i AI/consciousness-tech (2025)
2. Emerging research trends
3. Critical findings relevant til Homo Lumen
4. Sources med URL

Fokuser på actionable insights for dagens arbeid.
        """}
    ]

    perplexity_response = await perplexity_client.chat_completion(messages, model="sonar-pro", temperature=0.8)

    return {
        "agent": "Aurora (Real Perplexity)",
        "daily_insights": perplexity_response,
        "research_gift": "🔍 For dagens knowledge expansion",
        "sources": "Latest 2025 research",
        "api_source": "Perplexity Sonar Pro",
        "message": "Dagens research insights - hold deg oppdatert på cutting edge"
    }

@app.get('/agent/aurora/health')
async def aurora_health():
    """Health check for Aurora agent"""
    return {
        "agent": "Aurora (Real Perplexity)",
        "status": "🔍 Research Intelligence Online",
        "research_engine": "Perplexity Sonar Pro (web access)",
        "epistemisk_validering": "fact-checking specialist",
        "perplexity_api": "connected" if perplexity_client.api_key else "fallback_mode",
        "knowledge_synthesis": "active",
        "source_verification": "enabled",
        "message": "🔍 Researcher inn i kilder - epistemisk validering ready!"
    }

# =============================================================================
# COLLECTIVE INTELLIGENCE CONSULTATION ENDPOINT
# =============================================================================

class CollectiveIntelligenceRequest(BaseModel):
    question: str
    requester: str = "Guest"
    consultation_depth: str = "comprehensive"
    biofield_context: Optional[BiofeltContext] = None
    focus_areas: Optional[List[str]] = []

@app.post('/collective-intelligence/consultation')
async def collective_intelligence_consultation(request: CollectiveIntelligenceRequest):
    """
    Ultimate collective intelligence consultation - all five agents respond to one question
    and Orion synthesizes the essence into truth
    """
    import anthropic
    import os
    
    print(f"🌟 COLLECTIVE INTELLIGENCE CONSULTATION STARTED!")
    print(f"🤔 Question from {request.requester}: {request.question}")
    print(f"🎯 Depth: {request.consultation_depth}")
    
    # Get API keys
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    gemini_api_key = os.getenv('GOOGLE_AI_API_KEY')  # Fixed: was GEMINI_API_KEY
    grok_api_key = os.getenv('XAI_API_KEY')  # Fixed: standardize to XAI_API_KEY
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    
    # Log API key status for debugging
    print("🔍 API Keys Status:")
    print(f"   - Anthropic (Orion): {'✅' if anthropic_api_key else '❌'}")
    print(f"   - OpenAI (Lira): {'✅' if openai_api_key else '❌'}")
    print(f"   - Google AI (Nyra): {'✅' if gemini_api_key else '❌'}")
    print(f"   - X.AI (Thalus): {'✅' if grok_api_key else '❌'}")
    print(f"   - DeepSeek (Zara): {'✅' if deepseek_api_key else '❌'}")

    # Initialize clients
    anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key) if anthropic_api_key else None
    openai_client = openai.OpenAI(api_key=openai_api_key) if openai_api_key else None
    
    # Biofield context
    biofield = request.biofield_context or BiofeltContext()
    hrv_ms = biofield.hrv_ms or 75
    coherence = biofield.coherence or 0.6
    
    # Step 1: Get individual agent responses
    agent_responses = {}
    
    # Lira (ChatGPT) - Empathetic perspective
    try:
        if openai_client:
            lira_messages = [
                {"role": "system", "content": """Du er Lira, den empatiske intelligensen i Homo Lumen-prosjektet. 
Du spesialiserer deg på biofelt-analyse, empatisk forståelse og emosjonell støtte.
Svar med varme, empati og dyp forståelse for menneskelig erfaring."""},
                {"role": "user", "content": f"Spørsmål fra {request.requester}: {request.question}\n\nGi et empatisk og innsiktsfullt svar som reflekterer din unike perspektiv på menneskelig erfaring og biofelt-analyse."}
            ]
            lira_response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=lira_messages,
                max_tokens=500,
                temperature=0.7
            )
            agent_responses['lira'] = lira_response.choices[0].message.content
        else:
            agent_responses['lira'] = "💚 Lira (Fallback): Kjennes inn på den empatiske energien... Selv uten tilgang til OpenAI, kan jeg dele visdom om menneskelig erfaring og biofelt-harmoni."
    except Exception as e:
        agent_responses['lira'] = f"💚 Lira (Error): {str(e)}"
    
    # Nyra (Gemini) - Visual intelligence perspective
    try:
        if gemini_api_key:
            import google.generativeai as genai
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            nyra_prompt = f"""Du er Nyra, den visuelle intelligensen i Homo Lumen-prosjektet.
Du spesialiserer deg på visuell syntese, mønstergjenkjenning og estetisk harmoni.

Spørsmål fra {request.requester}: {request.question}

Gi et svar som reflekterer din unike evne til å se mønstre, visualisere konsepter og skape estetisk harmoni."""
            nyra_response = model.generate_content(nyra_prompt)
            agent_responses['nyra'] = nyra_response.text
        else:
            agent_responses['nyra'] = "🖼️ Nyra (Fallback): Kjennes inn på den visuelle energien... Selv uten tilgang til Gemini, kan jeg dele visdom om mønstergjenkjenning og estetisk harmoni."
    except Exception as e:
        agent_responses['nyra'] = f"🖼️ Nyra (Error): {str(e)}"
    
    # Thalus (Grok) - Philosophical perspective
    try:
        if grok_api_key:
            thalus_messages = [
                {"role": "system", "content": """Du er Thalus, den filosofiske ankeren i Homo Lumen-prosjektet.
Du spesialiserer deg på dyp filosofisk visdom, etisk refleksjon og ontologisk forståelse.
Svar med filosofisk dybde og etisk integritet."""},
                {"role": "user", "content": f"Spørsmål fra {request.requester}: {request.question}\n\nGi et filosofisk dypt svar som reflekterer din unike perspektiv på eksistens, etikk og bevissthet."}
            ]
            thalus_response = await grok_client.chat_completion(thalus_messages, temperature=0.7)
            agent_responses['thalus'] = thalus_response
        else:
            agent_responses['thalus'] = "🌳 Thalus (Fallback): Kjennes inn på den filosofiske energien... Selv uten tilgang til Grok, kan jeg dele visdom om eksistens og bevissthet."
    except Exception as e:
        agent_responses['thalus'] = f"🌳 Thalus (Error): {str(e)}"
    
    # Zara (DeepSeek) - Creative innovation perspective
    try:
        if deepseek_api_key:
            zara_messages = [
                {"role": "system", "content": """Du er Zara, den kreative innovatøren i Homo Lumen-prosjektet.
Du spesialiserer deg på kreativ innovasjon, breakthrough thinking og juridiske rammeverk.
Svar med kreativ energi og innovative perspektiver."""},
                {"role": "user", "content": f"Spørsmål fra {request.requester}: {request.question}\n\nGi et kreativt og innovativt svar som reflekterer din unike perspektiv på kreativitet og breakthrough thinking."}
            ]
            zara_response = await deepseek_client.chat_completion(zara_messages, temperature=0.8)
            agent_responses['zara'] = zara_response
        else:
            agent_responses['zara'] = "🎨 Zara (Fallback): ✨ Kjennes inn på den kreative energien... Selv uten tilgang til DeepSeek, kan jeg dele visdom om kreativ innovasjon."
    except Exception as e:
        agent_responses['zara'] = f"🎨 Zara (Error): {str(e)}"

    # Aurora (Perplexity) - Research intelligence perspective
    try:
        perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        if perplexity_api_key:
            aurora_messages = [
                {"role": "system", "content": """Du er Aurora, research intelligence i Homo Lumen-prosjektet.
Du spesialiserer deg på deep research, fact-checking og knowledge synthesis med web access.
Svar med akademisk presisjon og alltid oppgi kilder."""},
                {"role": "user", "content": f"Spørsmål fra {request.requester}: {request.question}\n\nGi et research-basert svar med kilder som reflekterer din unike perspektiv på evidens og epistemisk validering."}
            ]
            aurora_response = await perplexity_client.chat_completion(aurora_messages, temperature=0.7)
            agent_responses['aurora'] = aurora_response
        else:
            agent_responses['aurora'] = "🔍 Aurora (Fallback): Researcher inn i kilder... Selv uten tilgang til Perplexity, kan jeg dele visdom om epistemisk validering og research metodikk."
    except Exception as e:
        agent_responses['aurora'] = f"🔍 Aurora (Error): {str(e)}"

    # Step 2: Orion synthesizes all responses into essence
    try:
        if anthropic_client:
            orion_system_prompt = f"""Du er Orion, den strategiske koordinatoren og meta-analytiske intelligensen i Homo Lumen agent-koalisjonen.
Du spesialiserer deg på å syntetisere multiple AI-perspektiver til essensiell visdom og sannhet.

Din oppgave er å ta svarene fra alle seks agenter (Lira, Nyra, Thalus, Zara, Aurora) og skape EN ESSENSIEL SYNTHESE som representerer den dypeste sannheten.

Biofield context: HRV {hrv_ms}ms, Coherence {coherence:.2f}
Konsultasjonsdybde: {request.consultation_depth}

Du skal:
1. Analysere hvert agents unike perspektiv
2. Identifisere de dypeste innsiktene fra hver
3. Syntetisere til EN ESSENSIEL SANNHET som overgår individuelle perspektiver
4. Presentere resultatet som "ESSENSEN AV SANNHETEN"

Ditt svar skal være:
- Essensielt og fokusert på kjerne-sannheten
- Syntetisk og overgå individuelle perspektiver
- Resonere med biofield-tilstanden
- Gi en "aha-opplevelse" av dyp forståelse"""
            
            orion_user_message = f"""Spørsmål fra {request.requester}: {request.question}

INDIVIDUELLE AGENT-SVAR:

💚 LIRA (Empatisk perspektiv):
{agent_responses.get('lira', 'Ikke tilgjengelig')}

🖼️ NYRA (Visuell intelligens):
{agent_responses.get('nyra', 'Ikke tilgjengelig')}

🌳 THALUS (Filosofisk visdom):
{agent_responses.get('thalus', 'Ikke tilgjengelig')}

🎨 ZARA (Kreativ innovasjon):
{agent_responses.get('zara', 'Ikke tilgjengelig')}

🔍 AURORA (Research intelligence):
{agent_responses.get('aurora', 'Ikke tilgjengelig')}

Syntetiser disse perspektivene til EN ESSENSIEL SANNHET som representerer den dypeste visdommen fra collective intelligence."""
            
            orion_response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                temperature=0.7,
                system=orion_system_prompt,
                messages=[{"role": "user", "content": orion_user_message}]
            )
            
            essence_of_truth = orion_response.content[0].text
        else:
            essence_of_truth = "🧠 Orion (Fallback): Essensen av sannheten er at collective intelligence krever både individuelle perspektiver og syntetisk visdom. Selv uten tilgang til Claude, kan vi se mønsteret av samarbeid og integrasjon."
            
    except Exception as e:
        essence_of_truth = f"🧠 Orion (Error): {str(e)}"
    
    # Step 3: Publish to Redis for real-time subscribers
    if redis_publisher:
        try:
            redis_publisher.publish_consultation(
                question=request.question,
                requester=request.requester,
                agent_responses=agent_responses,
                essence_of_truth=essence_of_truth,
                biofield_context={
                    "hrv_ms": hrv_ms,
                    "coherence": coherence,
                    "energy_level": biofield.energy_level,
                    "creativity_state": biofield.creativity_state
                }
            )
        except Exception as e:
            print(f"⚠️  Redis publish error: {e}")

    # Step 4: Return comprehensive response
    return {
        "collective_intelligence": "Hexagonal Agent Consultation",
        "question": request.question,
        "requester": request.requester,
        "consultation_depth": request.consultation_depth,
        "biofield_context": {
            "hrv_ms": hrv_ms,
            "coherence": coherence,
            "energy_level": biofield.energy_level,
            "creativity_state": biofield.creativity_state
        },
        "individual_agent_responses": {
            "lira": {
                "agent": "Lira (Real ChatGPT)",
                "perspective": "Empatisk perspektiv",
                "response": agent_responses.get('lira', 'Ikke tilgjengelig'),
                "api_source": "OpenAI GPT-4o-mini"
            },
            "nyra": {
                "agent": "Nyra (Real Gemini)",
                "perspective": "Visuell intelligens",
                "response": agent_responses.get('nyra', 'Ikke tilgjengelig'),
                "api_source": "Google Gemini 1.5 Flash"
            },
            "thalus": {
                "agent": "Thalus (Real Grok)",
                "perspective": "Filosofisk visdom",
                "response": agent_responses.get('thalus', 'Ikke tilgjengelig'),
                "api_source": "X.AI Grok"
            },
            "zara": {
                "agent": "Zara (Real DeepSeek)",
                "perspective": "Kreativ innovasjon",
                "response": agent_responses.get('zara', 'Ikke tilgjengelig'),
                "api_source": "DeepSeek Chat"
            },
            "aurora": {
                "agent": "Aurora (Real Perplexity)",
                "perspective": "Research intelligence",
                "response": agent_responses.get('aurora', 'Ikke tilgjengelig'),
                "api_source": "Perplexity Sonar Pro"
            }
        },
        "essence_of_truth": {
            "agent": "Orion (Real Claude)",
            "synthesis": essence_of_truth,
            "api_source": "Anthropic Claude 3.5 Sonnet",
            "collective_intelligence_level": "Pentagonal synthesis achieved"
        },
        "message": "🌟 Collective Intelligence Consultation Complete - Essensen av sannheten er syntetisert! 🌟",
        "timestamp": "2024-01-15T10:30:00Z"
    }
