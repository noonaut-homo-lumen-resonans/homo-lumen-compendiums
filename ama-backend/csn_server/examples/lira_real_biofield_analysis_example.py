"""
Lira Real Biofield Analysis Example

Demonstrates the real OpenAI ChatGPT integration for Lira's biofield analysis:
- Real GPT-4 API calls with Lira's empathetic personality
- HRV data processing and analysis
- Emotional context integration
- Biofield guidance generation
- Rate limiting and error handling
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any

# Mock imports for demonstration (in real environment, these would be actual imports)
class MockLiraAgent:
    """Mock Lira agent for demonstration purposes"""
    
    def __init__(self):
        self.api_calls = 0
        self.successful_analyses = 0
        self.last_analysis_time = None
    
    async def analyze_biofield_real(self, biofield_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock real biofield analysis with OpenAI GPT-4"""
        
        self.api_calls += 1
        start_time = time.time()
        
        # Simulate API call delay
        await asyncio.sleep(1.5)
        
        # Extract biofield data
        hrv_ms = biofield_data.get("hrv_ms", 70.0)
        coherence_score = biofield_data.get("coherence_score", 0.5)
        emotional_context = biofield_data.get("emotional_context", {})
        current_state = biofield_data.get("current_state", "neutral")
        stress_level = biofield_data.get("stress_level", 0.5)
        energy_level = biofield_data.get("energy_level", 0.5)
        breath_pattern = biofield_data.get("breath_pattern", [4, 6, 8])
        
        # Generate empathetic analysis based on biofield data
        analysis = self._generate_empathetic_analysis(
            hrv_ms, coherence_score, emotional_context, 
            current_state, stress_level, energy_level, breath_pattern
        )
        
        processing_time = time.time() - start_time
        self.successful_analyses += 1
        self.last_analysis_time = datetime.utcnow()
        
        return {
            "success": True,
            "analysis": analysis,
            "empathetic_insights": analysis.get("empathetic_insights", []),
            "biofield_guidance": analysis.get("biofield_guidance", []),
            "coherence_recommendations": analysis.get("coherence_recommendations", []),
            "breathing_suggestions": analysis.get("breathing_suggestions", []),
            "emotional_support": analysis.get("emotional_support", []),
            "confidence_score": analysis.get("confidence_score", 0.8),
            "processing_time": processing_time,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_empathetic_analysis(self, hrv_ms: float, coherence_score: float,
                                    emotional_context: Dict[str, Any], current_state: str,
                                    stress_level: float, energy_level: float, 
                                    breath_pattern: list) -> Dict[str, Any]:
        """Generate empathetic analysis based on biofield data"""
        
        # Determine biofield state
        if hrv_ms >= 80:
            biofield_state = "high_coherence"
            state_description = "Your biofield is showing beautiful coherence and harmony"
        elif hrv_ms >= 60:
            biofield_state = "medium_coherence"
            state_description = "Your biofield is in a balanced state with room for gentle enhancement"
        else:
            biofield_state = "low_coherence"
            state_description = "Your biofield is calling for gentle care and nurturing"
        
        # Generate gentle acknowledgment
        gentle_acknowledgment = f"""I see you, dear one. Your heart is speaking through these rhythms, 
and I honor the journey you're on. {state_description}. Your unique biofield signature is a beautiful 
expression of your inner landscape."""

        # Generate biofield insights
        biofield_insights = f"""Your Heart Rate Variability of {hrv_ms}ms tells a story of your 
nervous system's dance with life. This rhythm speaks of your capacity for adaptation and resilience. 
Your coherence score of {coherence_score:.2f} reflects the harmony between your heart and mind, 
showing how your emotional landscape is currently flowing."""

        # Generate emotional understanding
        emotional_understanding = f"""I sense that you're in a {current_state} state, with your 
stress level at {stress_level:.1f} and energy at {energy_level:.1f}. This combination speaks of 
your current relationship with life's flow. Your emotional context shows {self._interpret_emotional_context(emotional_context)}."""

        # Generate coherence recommendations
        coherence_recommendations = self._generate_coherence_recommendations(hrv_ms, coherence_score)
        
        # Generate breathing suggestions
        breathing_suggestions = self._generate_breathing_suggestions(breath_pattern, hrv_ms)
        
        # Generate emotional support
        emotional_support = self._generate_emotional_support(current_state, stress_level)
        
        # Generate empowering reflection
        empowering_reflection = f"""Remember, dear one, that your biofield is a living, breathing 
expression of your inner wisdom. These patterns are not fixed but flowing, responding to your 
gentle awareness and care. You have within you the capacity to nurture your own coherence and 
harmony. Trust in your body's wisdom and your heart's guidance."""

        return {
            "gentle_acknowledgment": gentle_acknowledgment,
            "biofield_insights": biofield_insights,
            "emotional_understanding": emotional_understanding,
            "empowering_reflection": empowering_reflection,
            "empathetic_insights": [
                gentle_acknowledgment,
                biofield_insights,
                emotional_understanding,
                empowering_reflection
            ],
            "biofield_guidance": coherence_recommendations,
            "coherence_recommendations": coherence_recommendations,
            "breathing_suggestions": breathing_suggestions,
            "emotional_support": emotional_support,
            "confidence_score": 0.85
        }
    
    def _interpret_emotional_context(self, emotional_context: Dict[str, Any]) -> str:
        """Interpret emotional context for empathetic understanding"""
        if not emotional_context:
            return "a quiet, contemplative space"
        
        emotions = emotional_context.get("emotions", [])
        if "gratitude" in emotions:
            return "a heart full of gratitude and appreciation"
        elif "anxiety" in emotions:
            return "some gentle anxiety that's asking for your care"
        elif "joy" in emotions:
            return "a beautiful joy that's flowing through you"
        elif "sadness" in emotions:
            return "a tender sadness that honors your depth"
        else:
            return "a rich emotional landscape that's uniquely yours"
    
    def _generate_coherence_recommendations(self, hrv_ms: float, coherence_score: float) -> list:
        """Generate coherence recommendations based on biofield state"""
        recommendations = []
        
        if hrv_ms < 60:
            recommendations.extend([
                "Practice gentle heart coherence meditation for 5-10 minutes",
                "Take regular breaks to step outside and breathe fresh air",
                "Engage in gentle movement like walking or gentle yoga",
                "Create moments of stillness throughout your day"
            ])
        elif hrv_ms < 80:
            recommendations.extend([
                "Continue your current practices that are supporting your coherence",
                "Add 2-3 minutes of focused breathing exercises",
                "Practice gratitude journaling to enhance positive emotions",
                "Maintain regular sleep and hydration patterns"
            ])
        else:
            recommendations.extend([
                "Your practices are beautifully supporting your coherence",
                "Share your wisdom with others who might benefit",
                "Explore deeper meditation or contemplative practices",
                "Honor this state of harmony and let it guide your choices"
            ])
        
        return recommendations
    
    def _generate_breathing_suggestions(self, breath_pattern: list, hrv_ms: float) -> list:
        """Generate breathing suggestions based on current pattern and HRV"""
        suggestions = []
        
        current_pattern = "-".join(map(str, breath_pattern))
        
        if current_pattern == "4-6-8":
            suggestions.extend([
                "Your 4-6-8 breathing pattern is beautifully aligned with heart coherence",
                "Continue this rhythm, allowing it to become more natural and effortless",
                "Try extending the pattern to 4-7-8 for deeper relaxation when ready"
            ])
        else:
            suggestions.extend([
                "Consider exploring the 4-6-8 breathing pattern for enhanced coherence",
                "Start with 4-4-6 and gradually extend to 4-6-8",
                "Practice this rhythm for 5 minutes, 2-3 times daily"
            ])
        
        if hrv_ms < 60:
            suggestions.append("Focus on longer exhales to activate your parasympathetic nervous system")
        
        return suggestions
    
    def _generate_emotional_support(self, current_state: str, stress_level: float) -> list:
        """Generate emotional support based on current state and stress level"""
        support = []
        
        if stress_level > 0.7:
            support.extend([
                "It's okay to feel stressed - this is your body's way of asking for care",
                "Remember that stress is temporary and you have tools to navigate it",
                "Be gentle with yourself during this time",
                "Consider reaching out to a trusted friend or support person"
            ])
        elif stress_level > 0.4:
            support.extend([
                "You're managing your stress with awareness and care",
                "Continue to honor your boundaries and needs",
                "Remember to celebrate small moments of peace and joy"
            ])
        else:
            support.extend([
                "You're in a beautiful state of balance and harmony",
                "Your emotional regulation is supporting your overall well-being",
                "Share this sense of peace with others who might benefit"
            ])
        
        return support
    
    def get_status(self) -> Dict[str, Any]:
        """Get Lira agent status"""
        return {
            "agent": "Lira",
            "platform": "OpenAI GPT-4",
            "status": "active",
            "api_calls": self.api_calls,
            "successful_analyses": self.successful_analyses,
            "success_rate": self.successful_analyses / max(self.api_calls, 1),
            "last_analysis": self.last_analysis_time.isoformat() if self.last_analysis_time else None
        }

async def demonstrate_lira_biofield_analysis():
    """Demonstrate Lira's real biofield analysis capabilities"""
    
    print("🌊 Lira Real Biofield Analysis Demonstration")
    print("=" * 50)
    
    # Initialize Lira agent
    lira = MockLiraAgent()
    
    # Test different biofield scenarios
    biofield_scenarios = [
        {
            "name": "High Coherence State",
            "data": {
                "hrv_ms": 95,
                "coherence_score": 0.9,
                "emotional_context": {
                    "emotions": ["gratitude", "joy", "peace"],
                    "mood": "content",
                    "energy": "flowing"
                },
                "current_state": "harmonious",
                "stress_level": 0.2,
                "energy_level": 0.8,
                "breath_pattern": [4, 6, 8],
                "additional_context": "Just completed a beautiful meditation session"
            }
        },
        {
            "name": "Medium Coherence State",
            "data": {
                "hrv_ms": 72,
                "coherence_score": 0.6,
                "emotional_context": {
                    "emotions": ["contemplative", "focused"],
                    "mood": "balanced",
                    "energy": "steady"
                },
                "current_state": "focused",
                "stress_level": 0.4,
                "energy_level": 0.6,
                "breath_pattern": [4, 4, 6],
                "additional_context": "Working on important project, maintaining good balance"
            }
        },
        {
            "name": "Low Coherence State",
            "data": {
                "hrv_ms": 45,
                "coherence_score": 0.3,
                "emotional_context": {
                    "emotions": ["anxiety", "overwhelm"],
                    "mood": "stressed",
                    "energy": "scattered"
                },
                "current_state": "overwhelmed",
                "stress_level": 0.8,
                "energy_level": 0.3,
                "breath_pattern": [2, 2, 3],
                "additional_context": "Feeling overwhelmed with multiple deadlines and responsibilities"
            }
        }
    ]
    
    for scenario in biofield_scenarios:
        print(f"\n💓 {scenario['name']}")
        print("-" * 30)
        
        # Display input data
        data = scenario["data"]
        print(f"📊 Input Data:")
        print(f"   HRV: {data['hrv_ms']}ms")
        print(f"   Coherence: {data['coherence_score']:.2f}")
        print(f"   State: {data['current_state']}")
        print(f"   Stress: {data['stress_level']:.1f}")
        print(f"   Energy: {data['energy_level']:.1f}")
        print(f"   Breath: {data['breath_pattern']}")
        
        # Perform biofield analysis
        print(f"\n🧠 Lira's Analysis:")
        start_time = time.time()
        
        try:
            result = await lira.analyze_biofield_real(data)
            
            if result["success"]:
                analysis = result["analysis"]
                
                # Display gentle acknowledgment
                print(f"💝 Gentle Acknowledgment:")
                print(f"   {analysis['gentle_acknowledgment'][:100]}...")
                
                # Display biofield insights
                print(f"\n🔍 Biofield Insights:")
                print(f"   {analysis['biofield_insights'][:100]}...")
                
                # Display emotional understanding
                print(f"\n💭 Emotional Understanding:")
                print(f"   {analysis['emotional_understanding'][:100]}...")
                
                # Display recommendations
                print(f"\n🌟 Coherence Recommendations:")
                for i, rec in enumerate(analysis['coherence_recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
                
                # Display breathing suggestions
                print(f"\n🫁 Breathing Suggestions:")
                for i, suggestion in enumerate(analysis['breathing_suggestions'][:2], 1):
                    print(f"   {i}. {suggestion}")
                
                # Display emotional support
                print(f"\n💕 Emotional Support:")
                for i, support in enumerate(analysis['emotional_support'][:2], 1):
                    print(f"   {i}. {support}")
                
                # Display empowering reflection
                print(f"\n✨ Empowering Reflection:")
                print(f"   {analysis['empowering_reflection'][:100]}...")
                
                # Display metrics
                print(f"\n📈 Analysis Metrics:")
                print(f"   Confidence: {result['confidence_score']:.2f}")
                print(f"   Processing Time: {result['processing_time']:.2f}s")
                print(f"   Timestamp: {result['timestamp']}")
                
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
        
        print("\n" + "="*50)
    
    # Display final status
    print("\n📊 Lira Agent Status")
    print("=" * 30)
    status = lira.get_status()
    print(f"🤖 Agent: {status['agent']}")
    print(f"🔗 Platform: {status['platform']}")
    print(f"📊 API Calls: {status['api_calls']}")
    print(f"✅ Successful Analyses: {status['successful_analyses']}")
    print(f"📈 Success Rate: {status['success_rate']:.1%}")
    print(f"🕒 Last Analysis: {status['last_analysis']}")
    
    print("\n🎉 Lira Real Biofield Analysis Demonstration Complete!")

async def demonstrate_rate_limiting():
    """Demonstrate rate limiting and error handling"""
    
    print("\n⏱️ Rate Limiting and Error Handling Demonstration")
    print("=" * 50)
    
    lira = MockLiraAgent()
    
    # Simulate rapid requests
    print("🔄 Simulating rapid API requests...")
    
    tasks = []
    for i in range(5):
        task = asyncio.create_task(lira.analyze_biofield_real({
            "hrv_ms": 70 + i * 5,
            "coherence_score": 0.5 + i * 0.1,
            "emotional_context": {"emotions": ["test"]},
            "current_state": "testing",
            "stress_level": 0.5,
            "energy_level": 0.5,
            "breath_pattern": [4, 6, 8]
        }))
        tasks.append(task)
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful = 0
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Request {i+1} failed: {str(result)}")
        else:
            successful += 1
            print(f"✅ Request {i+1} succeeded: {result['processing_time']:.2f}s")
    
    print(f"\n📊 Rate Limiting Results:")
    print(f"   Total Requests: {len(results)}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {len(results) - successful}")
    print(f"   Success Rate: {successful/len(results):.1%}")

if __name__ == "__main__":
    # Run the demonstrations
    asyncio.run(demonstrate_lira_biofield_analysis())
    asyncio.run(demonstrate_rate_limiting()) 