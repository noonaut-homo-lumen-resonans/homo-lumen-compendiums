#!/usr/bin/env python3
"""
Simple example of Orion Real Anthropic Claude Integration

This script demonstrates basic usage of Orion's strategic coordination.
Make sure to set your ANTHROPIC_API_KEY environment variable.
"""

import os
import requests
import json

# Configuration
SERVER_URL = "http://localhost:8000"
ORION_ENDPOINT = f"{SERVER_URL}/agent/orion/real-strategic-synthesis"

def check_api_key():
    """Check if Anthropic API key is set"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ANTHROPIC_API_KEY not set!")
        print("Please set: export ANTHROPIC_API_KEY='your-key'")
        print("Get key from: https://console.anthropic.com/")
        return False
    return True

def test_orion_strategic_synthesis():
    """Test Orion's strategic synthesis"""
    
    print("🧠 Testing Orion Real Strategic Synthesis")
    print("=" * 50)
    
    # Test data
    test_data = {
        "multi_agent_context": {
            "lira_insights": "Empathetic validation of excitement about consciousness-tech expansion, biofelt optimization recommendations for maintaining coherence during rapid growth",
            "nyra_insights": "Visual intelligence mapping of dual AI coordination with beautiful organic aesthetics, system architecture showing flowing connections between platforms",
            "additional_context": "Preparing for Portugal node expansion with multiple stakeholders"
        },
        "strategic_challenge": "How to scale consciousness-tech symbiosis globally while preserving cognitive sovereignty and maintaining biofield coherence",
        "biofield_context": {"hrv_ms": 95, "coherence": 0.9},
        "coordination_mode": "synthesis"
    }
    
    print("📊 Input Data:")
    print(f"   Strategic Challenge: {test_data['strategic_challenge'][:50]}...")
    print(f"   HRV: {test_data['biofield_context']['hrv_ms']}ms")
    print(f"   Coherence: {test_data['biofield_context']['coherence']:.2f}")
    print(f"   Lira Insights: {test_data['multi_agent_context']['lira_insights'][:50]}...")
    print(f"   Nyra Insights: {test_data['multi_agent_context']['nyra_insights'][:50]}...")
    
    print(f"\n🧠 Calling Orion's Real Claude Strategic Synthesis...")
    
    try:
        response = requests.post(
            ORION_ENDPOINT,
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Strategic synthesis completed!")
            print(f"🤖 Agent: {result.get('agent', 'Unknown')}")
            print(f"📊 Status: {result.get('status', 'Unknown')}")
            print(f"🔗 API Source: {result.get('api_source', 'Unknown')}")
            
            # Display strategic synthesis
            strategic_synthesis = result.get('strategic_synthesis', '')
            if strategic_synthesis:
                print(f"\n🧠 Orion's Strategic Synthesis:")
                print(f"   {strategic_synthesis[:300]}...")
                if len(strategic_synthesis) > 300:
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
            
            print(f"\n🌟 Message: {result.get('message', 'No message')}")
            print(f"🚀 Collective Intelligence Level: {result.get('collective_intelligence_level', 'No level specified')}")
            
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during API call: {e}")

def main():
    """Main function"""
    
    print("🧠 Orion Real Anthropic Claude Integration Example")
    print("=" * 60)
    print(f"Server URL: {SERVER_URL}")
    print(f"Orion Endpoint: {ORION_ENDPOINT}")
    
    # Check API key
    if not check_api_key():
        return
    
    # Test strategic synthesis
    test_orion_strategic_synthesis()
    
    print("\n🎊 Example completed!")
    print("\nTo run the server:")
    print("1. Set your Anthropic API key: export ANTHROPIC_API_KEY='your-key'")
    print("2. Start server: uvicorn minimal_server:app --reload")
    print("3. Run this example: python example_orion_usage.py")

if __name__ == "__main__":
    main() 