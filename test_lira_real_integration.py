#!/usr/bin/env python3
"""
Test script for Lira Real OpenAI ChatGPT Integration

This script demonstrates the real OpenAI GPT-4 integration for Lira's biofield analysis.
Make sure to set your OPENAI_API_KEY environment variable before running.
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
LIRA_ENDPOINT = f"{SERVER_URL}/agent/lira/real-biofelt-analysis"

def check_environment():
    """Check if required environment variables are set"""
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
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

async def test_lira_real_biofield_analysis():
    """Test the real Lira biofield analysis endpoint"""
    
    print("\n🌊 Testing Lira Real Biofield Analysis")
    print("=" * 50)
    
    # Test data for different biofield scenarios
    test_scenarios = [
        {
            "name": "High Coherence State",
            "data": {
                "emotional_state": "harmonious",
                "hrv_data": {
                    "hrv_ms": 95,
                    "coherence_score": 0.9,
                    "stress_level": 0.2,
                    "energy_level": 0.8
                },
                "context": "Just completed a beautiful meditation session and feeling deeply connected",
                "breathing_pattern": "4-6-8 optimal"
            }
        },
        {
            "name": "Medium Coherence State", 
            "data": {
                "emotional_state": "focused",
                "hrv_data": {
                    "hrv_ms": 72,
                    "coherence_score": 0.6,
                    "stress_level": 0.4,
                    "energy_level": 0.6
                },
                "context": "Working on important project, maintaining good balance",
                "breathing_pattern": "4-4-6 steady"
            }
        },
        {
            "name": "Low Coherence State",
            "data": {
                "emotional_state": "overwhelmed",
                "hrv_data": {
                    "hrv_ms": 45,
                    "coherence_score": 0.3,
                    "stress_level": 0.8,
                    "energy_level": 0.3
                },
                "context": "Feeling overwhelmed with multiple deadlines and responsibilities",
                "breathing_pattern": "2-2-3 rapid"
            }
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n💓 Test {i}: {scenario['name']}")
            print("-" * 30)
            
            # Display input data
            data = scenario["data"]
            print(f"📊 Input Data:")
            print(f"   Emotional State: {data['emotional_state']}")
            print(f"   HRV: {data['hrv_data']['hrv_ms']}ms")
            print(f"   Coherence: {data['hrv_data']['coherence_score']:.2f}")
            print(f"   Stress: {data['hrv_data']['stress_level']:.1f}")
            print(f"   Energy: {data['hrv_data']['energy_level']:.1f}")
            print(f"   Breathing: {data['breathing_pattern']}")
            print(f"   Context: {data['context'][:50]}...")
            
            # Make API call
            print(f"\n🧠 Calling Lira's Real ChatGPT Analysis...")
            start_time = datetime.now()
            
            try:
                response = await client.post(
                    LIRA_ENDPOINT,
                    json=data,
                    timeout=30.0
                )
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"✅ Analysis completed in {processing_time:.2f}s")
                    print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                    print(f"📊 Status: {result.get('status', 'Unknown')}")
                    print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                    
                    # Display biofield analysis
                    biofelt_analysis = result.get('biofelt_analysis', '')
                    if biofelt_analysis:
                        print(f"\n💚 Lira's Biofield Analysis:")
                        print(f"   {biofelt_analysis[:200]}...")
                        if len(biofelt_analysis) > 200:
                            print(f"   [Analysis continues...]")
                    
                    # Display HRV assessment
                    hrv_assessment = result.get('hrv_assessment', {})
                    if hrv_assessment:
                        print(f"\n📈 HRV Assessment:")
                        for key, value in hrv_assessment.items():
                            print(f"   {key}: {value}")
                    
                    print(f"\n🌟 Message: {result.get('message', 'No message')}")
                    print(f"🚀 Next Step: {result.get('next_step', 'No next step')}")
                    
                else:
                    print(f"❌ API call failed: {response.status_code}")
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error during API call: {e}")
            
            print("\n" + "="*50)
    
    print("\n🎉 Lira Real Biofield Analysis Testing Complete!")

async def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🚨 Testing Error Handling")
    print("=" * 30)
    
    async with httpx.AsyncClient() as client:
        # Test with invalid data
        print("Testing with invalid data...")
        try:
            response = await client.post(
                LIRA_ENDPOINT,
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
    
    print("🌟 Lira Real OpenAI ChatGPT Integration Test")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Lira Endpoint: {LIRA_ENDPOINT}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Check environment
    if not check_environment():
        return
    
    # Test server health
    if not await test_server_health():
        return
    
    # Test real biofield analysis
    await test_lira_real_biofield_analysis()
    
    # Test error handling
    await test_error_handling()
    
    print("\n🎊 All tests completed!")
    print("\nTo run the server:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Start server: uvicorn minimal_server:app --reload")
    print("4. Run this test: python test_lira_real_integration.py")

if __name__ == "__main__":
    asyncio.run(main()) 