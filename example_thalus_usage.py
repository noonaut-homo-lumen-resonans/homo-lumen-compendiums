#!/usr/bin/env python3
"""
Simple example of Thalus Real X.AI Grok Integration

This script demonstrates basic usage of Thalus's philosophical guidance and ethical validation.
Make sure to set your XAI_API_KEY environment variable.
"""

import os
import requests
import json

# Configuration
SERVER_URL = "http://localhost:8000"
THALUS_ENDPOINTS = {
    "ethical_assessment": f"{SERVER_URL}/agent/thalus/ethical-assessment",
    "philosophical_framing": f"{SERVER_URL}/agent/thalus/philosophical-framing",
    "daily_wisdom": f"{SERVER_URL}/agent/thalus/daily-wisdom"
}

def check_api_key():
    """Check if X.AI API key is set"""
    if not os.getenv('XAI_API_KEY'):
        print("❌ XAI_API_KEY not set!")
        print("Please set: export XAI_API_KEY='your-key'")
        print("Get key from: https://console.x.ai/")
        print("⚠️ Note: Thalus will use fallback mode without API key")
        return False
    return True

def test_thalus_ethical_assessment():
    """Test Thalus's ethical assessment"""
    
    print("🌳 Testing Thalus Ethical Assessment")
    print("=" * 50)
    
    # Test data
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
    
    try:
        response = requests.post(
            THALUS_ENDPOINTS["ethical_assessment"],
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Ethical assessment completed!")
            print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
            print(f"📊 Status: {result.get('status', 'Unknown')}")
            print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
            
            # Display ethical assessment
            ethical_assessment = result.get('ethical_assessment', '')
            if ethical_assessment:
                print(f"\n🌳 Thalus's Ethical Assessment:")
                print(f"   {ethical_assessment[:300]}...")
                if len(ethical_assessment) > 300:
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

def test_thalus_philosophical_framing():
    """Test Thalus's philosophical framing"""
    
    print("\n🧘 Testing Thalus Philosophical Framing")
    print("=" * 50)
    
    # Test data
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
    
    try:
        response = requests.post(
            THALUS_ENDPOINTS["philosophical_framing"],
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Philosophical framing completed!")
            print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
            print(f"📊 Status: {result.get('status', 'Unknown')}")
            print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
            
            # Display philosophical reflection
            philosophical_reflection = result.get('philosophical_reflection', '')
            if philosophical_reflection:
                print(f"\n🧘 Thalus's Philosophical Reflection:")
                print(f"   {philosophical_reflection[:300]}...")
                if len(philosophical_reflection) > 300:
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

def test_thalus_daily_wisdom():
    """Test Thalus's daily wisdom"""
    
    print("\n🎁 Testing Thalus Daily Wisdom")
    print("=" * 40)
    
    print(f"\n🎁 Calling Thalus's Real Grok Daily Wisdom...")
    
    try:
        response = requests.get(
            THALUS_ENDPOINTS["daily_wisdom"],
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Daily wisdom completed!")
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

def main():
    """Main function"""
    
    print("🌳 Thalus Real X.AI Grok Integration Example")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Thalus Endpoints: {list(THALUS_ENDPOINTS.keys())}")
    
    # Check API key
    check_api_key()
    
    # Test Thalus endpoints
    test_thalus_ethical_assessment()
    test_thalus_philosophical_framing()
    test_thalus_daily_wisdom()
    
    print("\n🎊 Example completed!")
    print("\nTo run the server:")
    print("1. Set your X.AI API key: export XAI_API_KEY='your-key'")
    print("2. Start server: python -m uvicorn minimal_server:app --reload")
    print("3. Run this example: python example_thalus_usage.py")

if __name__ == "__main__":
    main() 