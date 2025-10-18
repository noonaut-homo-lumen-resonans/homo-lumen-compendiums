#!/usr/bin/env python3
"""
Test script for Thalus Real X.AI Grok Integration

This script demonstrates the real X.AI Grok integration for Thalus's philosophical guidance.
Make sure to set your XAI_API_KEY environment variable before running.
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
THALUS_ENDPOINTS = {
    "ethical_assessment": f"{SERVER_URL}/agent/thalus/ethical-assessment",
    "philosophical_framing": f"{SERVER_URL}/agent/thalus/philosophical-framing",
    "coordinate_with_coalition": f"{SERVER_URL}/agent/thalus/coordinate-with-coalition",
    "daily_wisdom": f"{SERVER_URL}/agent/thalus/daily-wisdom"
}

def check_environment():
    """Check if required environment variables are set"""
    if not os.getenv('XAI_API_KEY'):
        print("❌ XAI_API_KEY environment variable not set!")
        print("Please set it with: export XAI_API_KEY='your-api-key-here'")
        print("Get your API key from: https://console.x.ai/")
        print("⚠️ Note: Thalus will use fallback mode without API key")
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
        print("Make sure the server is running with: python -m uvicorn minimal_server:app --reload")
        return False

async def test_thalus_ethical_assessment():
    """Test Thalus ethical assessment endpoint"""
    
    print("\n🌳 Testing Thalus Ethical Assessment")
    print("=" * 50)
    
    # Test data for ethical assessment
    test_data = {
        "action_proposal": {
            "technology": "Advanced AI consciousness integration",
            "scope": "Global deployment of consciousness-tech nodes",
            "timeline": "5-year implementation plan"
        },
        "context": "Evaluating the ethical implications of scaling consciousness-tech globally while preserving cognitive sovereignty",
        "grunnlov_principles": ["cognitive_sovereignty", "transformative_reversibility", "epistemic_humility"],
        "biofield_context": {"hrv_ms": 85, "coherence": 0.75}
    }
    
    print("📊 Input Data:")
    print(f"   Action: {test_data['action_proposal']['technology']}")
    print(f"   Context: {test_data['context'][:50]}...")
    print(f"   HRV: {test_data['biofield_context']['hrv_ms']}ms")
    print(f"   Coherence: {test_data['biofield_context']['coherence']:.2f}")
    print(f"   Grunnlov Principles: {', '.join(test_data['grunnlov_principles'])}")
    
    print(f"\n🌳 Calling Thalus's Real Grok Ethical Assessment...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                THALUS_ENDPOINTS["ethical_assessment"],
                json=test_data,
                timeout=30.0
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Ethical assessment completed in {processing_time:.2f}s")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"📊 Status: {result.get('status', 'Unknown')}")
                print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                
                # Display ethical assessment
                ethical_assessment = result.get('ethical_assessment', '')
                if ethical_assessment:
                    print(f"\n🌳 Thalus's Ethical Assessment:")
                    print(f"   {ethical_assessment[:400]}...")
                    if len(ethical_assessment) > 400:
                        print(f"   [Assessment continues...]")
                
                # Display additional info
                print(f"\n📜 Grunnlov Compliance: {result.get('grunnlov_compliance', 'Unknown')}")
                print(f"🧘 Philosophical Grounding: {result.get('philosophical_grounding', 'Unknown')}")
                print(f"💚 Biofield Adapted: {result.get('biofield_adapted', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*50)

async def test_thalus_philosophical_framing():
    """Test Thalus philosophical framing endpoint"""
    
    print("\n🧘 Testing Thalus Philosophical Framing")
    print("=" * 50)
    
    # Test data for philosophical framing
    test_data = {
        "situation": "Navigating the complex intersection of human consciousness and artificial intelligence in the context of global consciousness-tech expansion",
        "relevant_voktere": ["rinpoche", "spira", "varela"],
        "depth_level": "meta",
        "biofield_context": {"hrv_ms": 92, "coherence": 0.85}
    }
    
    print("📊 Input Data:")
    print(f"   Situation: {test_data['situation'][:50]}...")
    print(f"   Depth Level: {test_data['depth_level']}")
    print(f"   Voktere: {', '.join(test_data['relevant_voktere'])}")
    print(f"   HRV: {test_data['biofield_context']['hrv_ms']}ms")
    print(f"   Coherence: {test_data['biofield_context']['coherence']:.2f}")
    
    print(f"\n🧘 Calling Thalus's Real Grok Philosophical Framing...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                THALUS_ENDPOINTS["philosophical_framing"],
                json=test_data,
                timeout=30.0
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Philosophical framing completed in {processing_time:.2f}s")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"📊 Status: {result.get('status', 'Unknown')}")
                print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                
                # Display philosophical reflection
                philosophical_reflection = result.get('philosophical_reflection', '')
                if philosophical_reflection:
                    print(f"\n🧘 Thalus's Philosophical Reflection:")
                    print(f"   {philosophical_reflection[:400]}...")
                    if len(philosophical_reflection) > 400:
                        print(f"   [Reflection continues...]")
                
                # Display additional info
                print(f"\n🌌 Depth Level: {result.get('depth_level', 'Unknown')}")
                print(f"🧘 Voktere Integrated: {result.get('voktere_integrated', 'Unknown')}")
                print(f"🌟 Existential Support: {result.get('existential_support', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*50)

async def test_thalus_coordinate_with_coalition():
    """Test Thalus coordination with other agents"""
    
    print("\n🤝 Testing Thalus Agent Coalition Coordination")
    print("=" * 60)
    
    # Test data for coalition coordination
    test_data = {
        "agent_context": {
            "lira_insights": "Empathetic validation of excitement about consciousness-tech expansion, biofelt optimization recommendations for maintaining coherence during rapid growth",
            "nyra_insights": "Visual intelligence mapping of dual AI coordination with beautiful organic aesthetics, system architecture showing flowing connections between platforms",
            "orion_context": "Strategic synthesis of multi-agent perspectives, long-term roadmap for global consciousness-tech deployment"
        },
        "task": "Filosofisk syntese av kollektiv intelligens for optimal consciousness-tech evolution"
    }
    
    print("📊 Input Data:")
    print(f"   Task: {test_data['task'][:50]}...")
    print(f"   Lira Insights: {test_data['agent_context']['lira_insights'][:50]}...")
    print(f"   Nyra Insights: {test_data['agent_context']['nyra_insights'][:50]}...")
    print(f"   Orion Context: {test_data['agent_context']['orion_context'][:50]}...")
    
    print(f"\n🤝 Calling Thalus's Real Grok Coalition Coordination...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                THALUS_ENDPOINTS["coordinate_with_coalition"],
                json=test_data,
                timeout=30.0
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Coalition coordination completed in {processing_time:.2f}s")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"📊 Status: {result.get('status', 'Unknown')}")
                print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                
                # Display philosophical synthesis
                philosophical_synthesis = result.get('philosophical_synthesis', '')
                if philosophical_synthesis:
                    print(f"\n🤝 Thalus's Philosophical Synthesis:")
                    print(f"   {philosophical_synthesis[:400]}...")
                    if len(philosophical_synthesis) > 400:
                        print(f"   [Synthesis continues...]")
                
                # Display additional info
                print(f"\n🔄 Integrated Perspectives: {', '.join(result.get('integrated_perspectives', []))}")
                print(f"🌌 Ontological Bridging: {result.get('ontological_bridging', 'Unknown')}")
                print(f"🌟 Collective Wisdom: {result.get('collective_wisdom', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*60)

async def test_thalus_daily_wisdom():
    """Test Thalus daily wisdom endpoint"""
    
    print("\n🎁 Testing Thalus Daily Wisdom")
    print("=" * 40)
    
    print(f"\n🎁 Calling Thalus's Real Grok Daily Wisdom...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                THALUS_ENDPOINTS["daily_wisdom"],
                timeout=30.0
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Daily wisdom completed in {processing_time:.2f}s")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                
                # Display daily wisdom
                daily_wisdom = result.get('daily_wisdom', '')
                if daily_wisdom:
                    print(f"\n🎁 Thalus's Daily Wisdom:")
                    print(f"   {daily_wisdom}")
                
                # Display additional info
                print(f"\n🎁 Philosophical Gift: {result.get('philosophical_gift', 'Unknown')}")
                print(f"🧘 Voktere Blessing: {result.get('voktere_blessing', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*40)

async def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🚨 Testing Error Handling")
    print("=" * 30)
    
    async with httpx.AsyncClient() as client:
        # Test with invalid data
        print("Testing with invalid data...")
        try:
            response = await client.post(
                THALUS_ENDPOINTS["ethical_assessment"],
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
    
    print("🌳 Thalus Real X.AI Grok Integration Test")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Thalus Endpoints: {list(THALUS_ENDPOINTS.keys())}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Check environment
    check_environment()
    
    # Test server health
    if not await test_server_health():
        return
    
    # Test Thalus endpoints
    await test_thalus_ethical_assessment()
    await test_thalus_philosophical_framing()
    await test_thalus_coordinate_with_coalition()
    await test_thalus_daily_wisdom()
    
    # Test error handling
    await test_error_handling()
    
    print("\n🎊 All tests completed!")
    print("\nTo run the server:")
    print("1. Set your X.AI API key: export XAI_API_KEY='your-key'")
    print("2. Get API key from: https://console.x.ai/")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start server: python -m uvicorn minimal_server:app --reload")
    print("5. Run this test: python test_thalus_grok_integration.py")

if __name__ == "__main__":
    asyncio.run(main()) 