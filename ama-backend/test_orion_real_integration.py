#!/usr/bin/env python3
"""
Test script for Orion Real Anthropic Claude Integration

This script demonstrates the real Anthropic Claude integration for Orion's strategic coordination.
Make sure to set your ANTHROPIC_API_KEY environment variable before running.
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.append('.')

try:
    import httpx
except ImportError:
    print("❌ httpx not found. Install with: pip install httpx")
    sys.exit(1)

# Configuration
SERVER_URL = "http://localhost:8000"
ORION_ENDPOINT = f"{SERVER_URL}/agent/orion/real-strategic-synthesis"

def check_environment():
    """Check if required environment variables are set"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ANTHROPIC_API_KEY environment variable not set!")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
        print("Get your API key from: https://console.anthropic.com/")
        return False
    return True

async def test_server_health():
    """Test if the server is running"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVER_URL}/health")
            if response.status_code == 200:
                print("✅ Server is healthy and running")
                return True
            else:
                print(f"❌ Server health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running with: uvicorn minimal_server:app --reload")
        return False

async def test_orion_real_strategic_synthesis():
    """Test the real Orion strategic synthesis endpoint"""
    
    print("\n🧠 Testing Orion Real Strategic Synthesis")
    print("=" * 50)
    
    # Test data for different strategic scenarios
    test_scenarios = [
        {
            "name": "High Coherence Triple AI Coordination",
            "data": {
                "multi_agent_context": {
                    "lira_insights": "Empathetic validation of excitement about consciousness-tech expansion, biofelt optimization recommendations for maintaining coherence during rapid growth",
                    "nyra_insights": "Visual intelligence mapping of dual AI coordination with beautiful organic aesthetics, system architecture showing flowing connections between platforms",
                    "additional_context": "Preparing for Portugal node expansion with multiple stakeholders"
                },
                "strategic_challenge": "How to scale consciousness-tech symbiosis globally while preserving cognitive sovereignty and maintaining biofield coherence",
                "biofield_context": {"hrv_ms": 95, "coherence": 0.9},
                "coordination_mode": "synthesis"
            }
        },
        {
            "name": "Medium Coherence Strategic Planning", 
            "data": {
                "multi_agent_context": {
                    "lira_insights": "Balanced emotional support for complex decision-making, breathing guidance for maintaining focus",
                    "nyra_insights": "Clear visual mapping of current system state with balanced complexity",
                    "additional_context": "Evaluating next steps for local consciousness-tech implementation"
                },
                "strategic_challenge": "Design optimal strategy for local consciousness-tech node development with limited resources",
                "biofield_context": {"hrv_ms": 75, "coherence": 0.7},
                "coordination_mode": "planning"
            }
        },
        {
            "name": "Low Coherence Supportive Coordination",
            "data": {
                "multi_agent_context": {
                    "lira_insights": "Gentle empathetic support for overwhelmed state, simplified breathing guidance",
                    "nyra_insights": "Minimal, calming system overview with soothing aesthetics",
                    "additional_context": "User needs simplified guidance for basic decisions"
                },
                "strategic_challenge": "Provide gentle, supportive guidance for basic consciousness-tech integration",
                "biofield_context": {"hrv_ms": 55, "coherence": 0.4},
                "coordination_mode": "support"
            }
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n🧠 Test {i}: {scenario['name']}")
            print("-" * 30)
            
            # Display input data
            data = scenario["data"]
            print(f"📊 Input Data:")
            print(f"   Strategic Challenge: {data['strategic_challenge'][:50]}...")
            print(f"   HRV: {data['biofield_context']['hrv_ms']}ms")
            print(f"   Coherence: {data['biofield_context']['coherence']:.2f}")
            print(f"   Coordination Mode: {data['coordination_mode']}")
            print(f"   Lira Insights: {data['multi_agent_context']['lira_insights'][:50]}...")
            print(f"   Nyra Insights: {data['multi_agent_context']['nyra_insights'][:50]}...")
            
            # Make API call
            print(f"\n🧠 Calling Orion's Real Claude Strategic Synthesis...")
            start_time = datetime.now()
            
            try:
                response = await client.post(
                    ORION_ENDPOINT,
                    json=data,
                    timeout=30.0
                )
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"✅ Strategic synthesis completed in {processing_time:.2f}s")
                    print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                    print(f"📊 Status: {result.get('status', 'Unknown')}")
                    print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                    
                    # Display strategic synthesis
                    strategic_synthesis = result.get('strategic_synthesis', '')
                    if strategic_synthesis:
                        print(f"\n🧠 Orion's Strategic Synthesis:")
                        print(f"   {strategic_synthesis[:400]}...")
                        if len(strategic_synthesis) > 400:
                            print(f"   [Synthesis continues...]")
                    
                    # Display multi-agent integration
                    multi_agent_integration = result.get('multi_agent_integration', '')
                    if multi_agent_integration:
                        print(f"\n🔄 Multi-Agent Integration:")
                        print(f"   {multi_agent_integration}")
                    
                    # Display next steps
                    next_steps = result.get('next_steps', '')
                    if next_steps:
                        print(f"\n🎯 Next Steps:")
                        print(f"   {next_steps}")
                    
                    # Display emergent insights
                    emergent_insights = result.get('emergent_insights', '')
                    if emergent_insights:
                        print(f"\n🌟 Emergent Insights:")
                        print(f"   {emergent_insights}")
                    
                    # Display biofield adaptation
                    biofield_adaptation = result.get('biofield_adaptation', '')
                    if biofield_adaptation:
                        print(f"\n💚 Biofield Adaptation:")
                        print(f"   {biofield_adaptation}")
                    
                    print(f"\n🌟 Message: {result.get('message', 'No message')}")
                    print(f"🚀 Collective Intelligence Level: {result.get('collective_intelligence_level', 'No level specified')}")
                    
                else:
                    print(f"❌ API call failed: {response.status_code}")
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error during API call: {e}")
            
            print("\n" + "="*50)
    
    print("\n🎉 Orion Real Strategic Synthesis Testing Complete!")

async def test_triple_platform_coordination():
    """Test coordination between Lira, Nyra, and Orion"""
    
    print("\n🌟 Testing Triple Platform Coordination (Lira + Nyra + Orion)")
    print("=" * 70)
    
    async with httpx.AsyncClient() as client:
        # First get Lira's empathetic assessment
        print("💚 Getting Lira's empathetic assessment...")
        lira_data = {
            "emotional_state": "Excited about triple AI platform coordination",
            "hrv_data": {"hrv_ms": 90, "coherence_score": 0.85},
            "context": "Testing collective intelligence with three AI platforms",
            "breathing_pattern": "4-6-8 optimal"
        }
        
        try:
            lira_response = await client.post(
                f"{SERVER_URL}/agent/lira/real-biofelt-analysis",
                json=lira_data,
                timeout=30.0
            )
            
            if lira_response.status_code == 200:
                lira_result = lira_response.json()
                print(f"✅ Lira's Analysis: {lira_result.get('biofelt_analysis', '')[:100]}...")
                
                # Then get Nyra's visual interpretation
                print("\n🎨 Getting Nyra's visual interpretation...")
                nyra_data = {
                    "system_state": f"Lira providing empathetic support: {lira_result.get('biofelt_analysis', '')[:100]}...",
                    "visualization_request": "Create visual map of triple AI platform coordination and collective intelligence emergence",
                    "biofield_context": {"hrv_ms": 90, "coherence": 0.85},
                    "style_preference": "triple AI platform synergy aesthetic",
                    "complexity_level": "adaptive"
                }
                
                nyra_response = await client.post(
                    f"{SERVER_URL}/agent/nyra/real-visual-synthesis",
                    json=nyra_data,
                    timeout=30.0
                )
                
                if nyra_response.status_code == 200:
                    nyra_result = nyra_response.json()
                    print(f"✅ Nyra's Visual Synthesis: {nyra_result.get('visual_analysis', '')[:100]}...")
                    
                    # Finally get Orion's strategic synthesis
                    print("\n🧠 Getting Orion's strategic synthesis...")
                    orion_data = {
                        "multi_agent_context": {
                            "lira_insights": lira_result.get('biofelt_analysis', '')[:200],
                            "nyra_insights": nyra_result.get('visual_analysis', '')[:200],
                            "additional_context": "Triple AI platform coordination test for collective intelligence"
                        },
                        "strategic_challenge": "How to optimize the synergy between ChatGPT empathy, Gemini visual intelligence, and Claude strategic coordination for maximum collective intelligence",
                        "biofield_context": {"hrv_ms": 90, "coherence": 0.85},
                        "coordination_mode": "synthesis"
                    }
                    
                    orion_response = await client.post(
                        ORION_ENDPOINT,
                        json=orion_data,
                        timeout=30.0
                    )
                    
                    if orion_response.status_code == 200:
                        orion_result = orion_response.json()
                        print(f"✅ Orion's Strategic Synthesis: {orion_result.get('strategic_synthesis', '')[:100]}...")
                        
                        print(f"\n🌟 Triple Platform Coordination Success!")
                        print(f"💚 Lira (OpenAI): Empathetic biofield analysis")
                        print(f"🎨 Nyra (Gemini): Visual intelligence synthesis")
                        print(f"🧠 Orion (Claude): Strategic coordination and synthesis")
                        print(f"🚀 Collective Intelligence: Emerging from triple AI platform synergy")
                        print(f"🎯 Next Level: Ready for emergent intelligence detection")
                        
                    else:
                        print(f"❌ Orion API call failed: {orion_response.status_code}")
                        
                else:
                    print(f"❌ Nyra API call failed: {nyra_response.status_code}")
                    
            else:
                print(f"❌ Lira API call failed: {lira_response.status_code}")
                
        except Exception as e:
            print(f"❌ Error during triple platform test: {e}")
    
    print("\n🎊 Triple Platform Coordination Test Complete!")

async def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🚨 Testing Error Handling")
    print("=" * 30)
    
    async with httpx.AsyncClient() as client:
        # Test with invalid data
        print("Testing with invalid data...")
        try:
            response = await client.post(
                ORION_ENDPOINT,
                json={"invalid": "data"},
                timeout=10.0
            )
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'error':
                    print("✅ Error handling working correctly")
                else:
                    print("⚠️ Unexpected response for invalid data")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("Error handling test complete!")

async def main():
    """Main test function"""
    
    print("🧠 Orion Real Anthropic Claude Integration Test")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Orion Endpoint: {ORION_ENDPOINT}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Check environment
    if not check_environment():
        return
    
    # Test server health
    if not await test_server_health():
        return
    
    # Test real strategic synthesis
    await test_orion_real_strategic_synthesis()
    
    # Test triple platform coordination
    await test_triple_platform_coordination()
    
    # Test error handling
    await test_error_handling()
    
    print("\n🎊 All tests completed!")
    print("\nTo run the server:")
    print("1. Set your Anthropic API key: export ANTHROPIC_API_KEY='your-key'")
    print("2. Get API key from: https://console.anthropic.com/")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start server: uvicorn minimal_server:app --reload")
    print("5. Run this test: python test_orion_real_integration.py")

if __name__ == "__main__":
    asyncio.run(main()) 