#!/usr/bin/env python3
"""
Test script for Zara Real DeepSeek Integration

This script demonstrates the real DeepSeek integration for Zara's creative innovation and legal validation.
Make sure to set your DEEPSEEK_API_KEY environment variable before running.
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
ZARA_ENDPOINTS = {
    "creative_challenge": f"{SERVER_URL}/agent/zara/creative-challenge",
    "legal_validation": f"{SERVER_URL}/agent/zara/legal-validation",
    "coordinate_with_coalition": f"{SERVER_URL}/agent/zara/coordinate-with-coalition",
    "daily_innovation": f"{SERVER_URL}/agent/zara/daily-innovation",
    "health": f"{SERVER_URL}/agent/zara/health"
}

def check_environment():
    """Check if required environment variables are set"""
    if not os.getenv('DEEPSEEK_API_KEY'):
        print("❌ DEEPSEEK_API_KEY environment variable not set!")
        print("Please set it with: export DEEPSEEK_API_KEY='your-api-key-here'")
        print("Get your API key from: https://platform.deepseek.com/")
        print("⚠️ Note: Zara will use fallback mode without API key")
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

async def test_zara_creative_challenge():
    """Test Zara creative challenge endpoint"""
    
    print("\n🎨 Testing Zara Creative Challenge")
    print("=" * 50)
    
    # Test data for creative challenge
    test_data = {
        "challenge": "Design a consciousness-tech interface that seamlessly integrates biofield monitoring with AI coordination while preserving human cognitive sovereignty",
        "domain": "Consciousness Technology & Human-AI Symbiosis",
        "constraints": ["Must preserve cognitive sovereignty", "Real-time biofield integration", "EU GDPR compliance", "Scalable architecture"],
        "creativity_level": "breakthrough",
        "biofield_context": {"hrv_ms": 88, "coherence": 0.82, "energy_level": "high", "creativity_state": "highly_open"},
        "inspiration_sources": ["Biomimicry", "Quantum consciousness", "Regenerative design", "Bioelectric systems"]
    }
    
    print("📊 Input Data:")
    print(f"   Challenge: {test_data['challenge'][:50]}...")
    print(f"   Domain: {test_data['domain']}")
    print(f"   Constraints: {', '.join(test_data['constraints'])}")
    print(f"   Creativity Level: {test_data['creativity_level']}")
    print(f"   HRV: {test_data['biofield_context']['hrv_ms']}ms")
    print(f"   Coherence: {test_data['biofield_context']['coherence']:.2f}")
    
    print(f"\n🎨 Calling Zara's Real DeepSeek Creative Challenge...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ZARA_ENDPOINTS["creative_challenge"],
                json=test_data,
                timeout=30.0
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Creative challenge completed in {processing_time:.2f}s")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"📊 Status: {result.get('status', 'Unknown')}")
                print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                
                # Display creative solution
                creative_solution = result.get('creative_solution', '')
                if creative_solution:
                    print(f"\n🎨 Zara's Creative Solution:")
                    print(f"   {creative_solution[:400]}...")
                    if len(creative_solution) > 400:
                        print(f"   [Solution continues...]")
                
                # Display additional info
                print(f"\n🚀 Creativity Level: {result.get('creativity_level', 'Unknown')}")
                print(f"💡 Innovation Approach: {result.get('innovation_approach', 'Unknown')}")
                print(f"💚 Biofield Adapted: {result.get('biofield_adapted', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*50)

async def test_zara_legal_validation():
    """Test Zara legal validation endpoint"""
    
    print("\n⚖️ Testing Zara Legal Validation")
    print("=" * 50)
    
    # Test data for legal validation
    test_data = {
        "proposal": {
            "technology": "Advanced biofield-AI integration system",
            "data_collection": "Real-time HRV, coherence, and emotional state monitoring",
            "ai_processing": "Multi-agent coordination with biofield-responsive adaptation",
            "deployment": "Global consciousness-tech network"
        },
        "legal_domain": "ai_ethics",
        "jurisdiction": "EU/Norway",
        "context": "Evaluating legal compliance for consciousness-tech deployment with biofield monitoring",
        "biofield_context": {"hrv_ms": 85, "coherence": 0.78, "energy_level": "balanced"},
        "risk_tolerance": "moderate"
    }
    
    print("📊 Input Data:")
    print(f"   Technology: {test_data['proposal']['technology']}")
    print(f"   Legal Domain: {test_data['legal_domain']}")
    print(f"   Jurisdiction: {test_data['jurisdiction']}")
    print(f"   Context: {test_data['context'][:50]}...")
    print(f"   HRV: {test_data['biofield_context']['hrv_ms']}ms")
    print(f"   Coherence: {test_data['biofield_context']['coherence']:.2f}")
    
    print(f"\n⚖️ Calling Zara's Real DeepSeek Legal Validation...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ZARA_ENDPOINTS["legal_validation"],
                json=test_data,
                timeout=30.0
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Legal validation completed in {processing_time:.2f}s")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"📊 Status: {result.get('status', 'Unknown')}")
                print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                
                # Display legal analysis
                legal_analysis = result.get('legal_analysis', '')
                if legal_analysis:
                    print(f"\n⚖️ Zara's Legal Analysis:")
                    print(f"   {legal_analysis[:400]}...")
                    if len(legal_analysis) > 400:
                        print(f"   [Analysis continues...]")
                
                # Display additional info
                print(f"\n📜 Legal Domain: {result.get('legal_domain', 'Unknown')}")
                print(f"🌍 Jurisdiction: {result.get('jurisdiction', 'Unknown')}")
                print(f"🎨 Compliance Creative: {result.get('compliance_creative', 'Unknown')}")
                print(f"⚠️ Risk Assessment: {result.get('risk_assessment', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*50)

async def test_zara_coordinate_with_coalition():
    """Test Zara coordination with other agents"""
    
    print("\n🤝 Testing Zara Agent Coalition Coordination")
    print("=" * 60)
    
    # Test data for coalition coordination
    test_data = {
        "agent_context": {
            "orion_context": "Strategic synthesis of multi-agent perspectives for global consciousness-tech deployment",
            "lira_insights": "Empathetic validation of excitement about consciousness-tech expansion, biofelt optimization recommendations",
            "nyra_insights": "Visual intelligence mapping of dual AI coordination with beautiful organic aesthetics",
            "thalus_wisdom": "Philosophical grounding in SMV Grunnloven 4.0, ethical validation of consciousness-tech evolution"
        },
        "task": "Creative synthesis av collective intelligence for breakthrough consciousness-tech innovation"
    }
    
    print("📊 Input Data:")
    print(f"   Task: {test_data['task'][:50]}...")
    print(f"   Orion Context: {test_data['agent_context']['orion_context'][:50]}...")
    print(f"   Lira Insights: {test_data['agent_context']['lira_insights'][:50]}...")
    print(f"   Nyra Insights: {test_data['agent_context']['nyra_insights'][:50]}...")
    print(f"   Thalus Wisdom: {test_data['agent_context']['thalus_wisdom'][:50]}...")
    
    print(f"\n🤝 Calling Zara's Real DeepSeek Coalition Coordination...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ZARA_ENDPOINTS["coordinate_with_coalition"],
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
                
                # Display creative synthesis
                creative_synthesis = result.get('creative_synthesis', '')
                if creative_synthesis:
                    print(f"\n🤝 Zara's Creative Synthesis:")
                    print(f"   {creative_synthesis[:400]}...")
                    if len(creative_synthesis) > 400:
                        print(f"   [Synthesis continues...]")
                
                # Display additional info
                print(f"\n🔄 Integrated Perspectives: {', '.join(result.get('integrated_perspectives', []))}")
                print(f"🚀 Innovation Amplification: {result.get('innovation_amplification', 'Unknown')}")
                print(f"🌟 Collective Creativity: {result.get('collective_creativity', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*60)

async def test_zara_daily_innovation():
    """Test Zara daily innovation endpoint"""
    
    print("\n🎨 Testing Zara Daily Innovation")
    print("=" * 40)
    
    print(f"\n🎨 Calling Zara's Real DeepSeek Daily Innovation...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                ZARA_ENDPOINTS["daily_innovation"],
                timeout=30.0
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Daily innovation completed in {processing_time:.2f}s")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
                
                # Display daily innovation
                daily_innovation = result.get('daily_innovation', '')
                if daily_innovation:
                    print(f"\n🎨 Zara's Daily Innovation:")
                    print(f"   {daily_innovation}")
                
                # Display additional info
                print(f"\n🎨 Creative Spark: {result.get('creative_spark', 'Unknown')}")
                print(f"⚡ Innovation Energy: {result.get('innovation_energy', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")
    
    print("\n" + "="*40)

async def test_zara_health():
    """Test Zara health endpoint"""
    
    print("\n🏥 Testing Zara Health Check")
    print("=" * 30)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                ZARA_ENDPOINTS["health"],
                timeout=10.0
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Health check successful!")
                print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
                print(f"📊 Status: {result.get('status', 'Unknown')}")
                print(f"🚀 Innovation Engine: {result.get('innovation_engine', 'Unknown')}")
                print(f"⚖️ Legal Validation: {result.get('legal_validation', 'Unknown')}")
                print(f"🔗 DeepSeek API: {result.get('deepseek_api', 'Unknown')}")
                print(f"🎨 Creativity Frameworks: {result.get('creativity_frameworks', 'Unknown')}")
                print(f"⚡ Workflow Optimization: {result.get('workflow_optimization', 'Unknown')}")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
            else:
                print(f"❌ Health check failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during health check: {e}")
    
    print("\n" + "="*30)

async def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🚨 Testing Error Handling")
    print("=" * 30)
    
    async with httpx.AsyncClient() as client:
        # Test with invalid data
        print("Testing with invalid data...")
        try:
            response = await client.post(
                ZARA_ENDPOINTS["creative_challenge"],
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
    
    print("🎨 Zara Real DeepSeek Integration Test")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Zara Endpoints: {list(ZARA_ENDPOINTS.keys())}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Check environment
    check_environment()
    
    # Test server health
    if not await test_server_health():
        return
    
    # Test Zara endpoints
    await test_zara_health()
    await test_zara_creative_challenge()
    await test_zara_legal_validation()
    await test_zara_coordinate_with_coalition()
    await test_zara_daily_innovation()
    
    # Test error handling
    await test_error_handling()
    
    print("\n🎊 All tests completed!")
    print("\nTo run the server:")
    print("1. Set your DeepSeek API key: export DEEPSEEK_API_KEY='your-key'")
    print("2. Get API key from: https://platform.deepseek.com/")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start server: python -m uvicorn minimal_server:app --reload")
    print("5. Run this test: python test_zara_deepseek_integration.py")

if __name__ == "__main__":
    asyncio.run(main()) 