#!/usr/bin/env python3
"""
Simple example of Zara Real DeepSeek Integration

This script demonstrates basic usage of Zara's creative innovation and legal validation.
Make sure to set your DEEPSEEK_API_KEY environment variable.
"""

import os
import requests
import json

# Configuration
SERVER_URL = "http://localhost:8000"
ZARA_ENDPOINTS = {
    "creative_challenge": f"{SERVER_URL}/agent/zara/creative-challenge",
    "legal_validation": f"{SERVER_URL}/agent/zara/legal-validation",
    "daily_innovation": f"{SERVER_URL}/agent/zara/daily-innovation"
}

def check_api_key():
    """Check if DeepSeek API key is set"""
    if not os.getenv('DEEPSEEK_API_KEY'):
        print("❌ DEEPSEEK_API_KEY not set!")
        print("Please set: export DEEPSEEK_API_KEY='your-key'")
        print("Get key from: https://platform.deepseek.com/")
        print("⚠️ Note: Zara will use fallback mode without API key")
        return False
    return True

def test_zara_creative_challenge():
    """Test Zara's creative challenge"""
    
    print("🎨 Testing Zara Creative Challenge")
    print("=" * 50)
    
    # Test data
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
    
    try:
        response = requests.post(
            ZARA_ENDPOINTS["creative_challenge"],
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Creative challenge completed!")
            print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
            print(f"📊 Status: {result.get('status', 'Unknown')}")
            print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
            
            # Display creative solution
            creative_solution = result.get('creative_solution', '')
            if creative_solution:
                print(f"\n🎨 Zara's Creative Solution:")
                print(f"   {creative_solution[:300]}...")
                if len(creative_solution) > 300:
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

def test_zara_legal_validation():
    """Test Zara's legal validation"""
    
    print("\n⚖️ Testing Zara Legal Validation")
    print("=" * 50)
    
    # Test data
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
    
    try:
        response = requests.post(
            ZARA_ENDPOINTS["legal_validation"],
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Legal validation completed!")
            print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
            print(f"📊 Status: {result.get('status', 'Unknown')}")
            print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
            
            # Display legal analysis
            legal_analysis = result.get('legal_analysis', '')
            if legal_analysis:
                print(f"\n⚖️ Zara's Legal Analysis:")
                print(f"   {legal_analysis[:300]}...")
                if len(legal_analysis) > 300:
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

def test_zara_daily_innovation():
    """Test Zara's daily innovation"""
    
    print("\n🎨 Testing Zara Daily Innovation")
    print("=" * 40)
    
    print(f"\n🎨 Calling Zara's Real DeepSeek Daily Innovation...")
    
    try:
        response = requests.get(
            ZARA_ENDPOINTS["daily_innovation"],
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Daily innovation completed!")
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

def main():
    """Main function"""
    
    print("🎨 Zara Real DeepSeek Integration Example")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Zara Endpoints: {list(ZARA_ENDPOINTS.keys())}")
    
    # Check API key
    check_api_key()
    
    # Test Zara endpoints
    test_zara_creative_challenge()
    test_zara_legal_validation()
    test_zara_daily_innovation()
    
    print("\n🎊 Example completed!")
    print("\nTo run the server:")
    print("1. Set your DeepSeek API key: export DEEPSEEK_API_KEY='your-key'")
    print("2. Start server: python -m uvicorn minimal_server:app --reload")
    print("3. Run this example: python example_zara_usage.py")

if __name__ == "__main__":
    main() 