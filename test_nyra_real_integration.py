#!/usr/bin/env python3
"""
Test script for Nyra Real Google Gemini Integration

This script demonstrates the real Google Gemini integration for Nyra's visual intelligence.
Make sure to set your GOOGLE_AI_API_KEY environment variable before running.
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
NYRA_ENDPOINT = f"{SERVER_URL}/agent/nyra/real-visual-synthesis"

def check_environment():
    """Check if required environment variables are set"""
    if not os.getenv('GOOGLE_AI_API_KEY'):
        print("❌ GOOGLE_AI_API_KEY environment variable not set!")
        print("Please set it with: export GOOGLE_AI_API_KEY='your-api-key-here'")
        print("Get your free API key from: https://aistudio.google.com/app/apikey")
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

async def test_nyra_real_visual_synthesis():
    """Test the real Nyra visual synthesis endpoint"""
    
    print("\n🎨 Testing Nyra Real Visual Synthesis")
    print("=" * 50)
    
    # Test data for different visual scenarios
    test_scenarios = [
        {
            "name": "High Coherence System Visualization",
            "data": {
                "system_state": "Homo Lumen with real ChatGPT Lira active, biofield optimal, collective intelligence emerging",
                "visualization_request": "Create visual map of current agent interactions and data flows",
                "biofield_context": {"hrv_ms": 95, "coherence": 0.9},
                "style_preference": "organic consciousness-tech aesthetic with flowing connections",
                "complexity_level": "adaptive"
            }
        },
        {
            "name": "Medium Coherence Design Analysis", 
            "data": {
                "system_state": "Balanced system operation with multiple agents coordinating",
                "visualization_request": "Analyze current system aesthetics and suggest improvements",
                "biofield_context": {"hrv_ms": 72, "coherence": 0.6},
                "style_preference": "harmonious balance between technology and nature",
                "complexity_level": "balanced"
            }
        },
        {
            "name": "Low Coherence Calming Visualization",
            "data": {
                "system_state": "System in gentle, supportive mode for user well-being",
                "visualization_request": "Create calming, simple system overview with soothing aesthetics",
                "biofield_context": {"hrv_ms": 45, "coherence": 0.3},
                "style_preference": "soft, minimal, healing-focused design",
                "complexity_level": "minimal"
            }
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n🎨 Test {i}: {scenario['name']}")
            print("-" * 30)
            
            # Display input data
            data = scenario["data"]
            print(f"📊 Input Data:")
            print(f"   System State: {data['system_state'][:50]}...")
            print(f"   Visualization Request: {data['visualization_request'][:50]}...")
            print(f"   HRV: {data['biofield_context']['hrv_ms']}ms")
            print(f"   Coherence: {data['biofield_context']['coherence']:.2f}")
            print(f"   Style: {data['style_preference']}")
            print(f"   Complexity: {data['complexity_level']}")
            
            # Make API call
            print(f"\n🧠 Calling Nyra's Real Gemini Visual Synthesis...")
            start_time = datetime.now()
            
            try:
                response = await client.post(
                    NYRA_ENDPOINT,
                    json=data,
                    timeout=30.0
                )
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"✅ Visual synthesis completed in {processing_time:.2f}s")
                    print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                    print(f"📊 Status: {result.get('status', 'Unknown')}")
                    print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                    
                    # Display visual analysis
                    visual_analysis = result.get('visual_analysis', '')
                    if visual_analysis:
                        print(f"\n🎨 Nyra's Visual Analysis:")
                        print(f"   {visual_analysis[:300]}...")
                        if len(visual_analysis) > 300:
                            print(f"   [Analysis continues...]")
                    
                    # Display system visualization
                    system_visualization = result.get('system_visualization', '')
                    if system_visualization:
                        print(f"\n🗺️ System Visualization:")
                        print(f"   {system_visualization}")
                    
                    # Display aesthetic insights
                    aesthetic_insights = result.get('aesthetic_insights', '')
                    if aesthetic_insights:
                        print(f"\n✨ Aesthetic Insights:")
                        print(f"   {aesthetic_insights}")
                    
                    # Display biofield adaptation
                    biofield_adaptation = result.get('biofield_adaptation', '')
                    if biofield_adaptation:
                        print(f"\n💚 Biofield Adaptation:")
                        print(f"   {biofield_adaptation}")
                    
                    print(f"\n🌟 Message: {result.get('message', 'No message')}")
                    print(f"🚀 Next Capabilities: {result.get('next_capabilities', 'No next capabilities')}")
                    
                else:
                    print(f"❌ API call failed: {response.status_code}")
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error during API call: {e}")
            
            print("\n" + "="*50)
    
    print("\n🎉 Nyra Real Visual Synthesis Testing Complete!")

async def test_cross_platform_coordination():
    """Test coordination between Lira and Nyra"""
    
    print("\n🌟 Testing Cross-Platform Coordination (Lira + Nyra)")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # First get Lira's empathetic assessment
        print("💚 Getting Lira's empathetic assessment...")
        lira_data = {
            "emotional_state": "Excited about visual intelligence integration",
            "hrv_data": {"hrv_ms": 85, "coherence_score": 0.8},
            "context": "Testing multi-platform collective intelligence",
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
                    "visualization_request": "Create visual map of empathy and visual intelligence synergy",
                    "biofield_context": {"hrv_ms": 85, "coherence": 0.8},
                    "style_preference": "empathy-visual intelligence fusion aesthetic",
                    "complexity_level": "adaptive"
                }
                
                nyra_response = await client.post(
                    NYRA_ENDPOINT,
                    json=nyra_data,
                    timeout=30.0
                )
                
                if nyra_response.status_code == 200:
                    nyra_result = nyra_response.json()
                    print(f"✅ Nyra's Visual Synthesis: {nyra_result.get('visual_analysis', '')[:100]}...")
                    
                    print(f"\n🌟 Cross-Platform Coordination Success!")
                    print(f"💚 Lira (OpenAI): Empathetic biofield analysis")
                    print(f"🎨 Nyra (Gemini): Visual intelligence synthesis")
                    print(f"🚀 Collective Intelligence: Emerging from dual-platform synergy")
                    
                else:
                    print(f"❌ Nyra API call failed: {nyra_response.status_code}")
                    
            else:
                print(f"❌ Lira API call failed: {lira_response.status_code}")
                
        except Exception as e:
            print(f"❌ Error during cross-platform test: {e}")
    
    print("\n🎊 Cross-Platform Coordination Test Complete!")

async def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🚨 Testing Error Handling")
    print("=" * 30)
    
    async with httpx.AsyncClient() as client:
        # Test with invalid data
        print("Testing with invalid data...")
        try:
            response = await client.post(
                NYRA_ENDPOINT,
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
    
    print("🎨 Nyra Real Google Gemini Integration Test")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Nyra Endpoint: {NYRA_ENDPOINT}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Check environment
    if not check_environment():
        return
    
    # Test server health
    if not await test_server_health():
        return
    
    # Test real visual synthesis
    await test_nyra_real_visual_synthesis()
    
    # Test cross-platform coordination
    await test_cross_platform_coordination()
    
    # Test error handling
    await test_error_handling()
    
    print("\n🎊 All tests completed!")
    print("\nTo run the server:")
    print("1. Set your Google AI API key: export GOOGLE_AI_API_KEY='your-key'")
    print("2. Get free API key from: https://aistudio.google.com/app/apikey")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start server: uvicorn minimal_server:app --reload")
    print("5. Run this test: python test_nyra_real_integration.py")

if __name__ == "__main__":
    asyncio.run(main()) 