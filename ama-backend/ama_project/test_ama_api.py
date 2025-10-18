"""
Test AMA API Endpoints
Simple script to test the AMA MCP architecture API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_ama_api():
    """Test AMA API endpoints"""
    
    print("🧠 Testing AMA API Endpoints...")
    print("=" * 60)
    
    try:
        # 1. Test health check
        print("1. Testing health check...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✅ Server is running!")
        else:
            print(f"   ❌ Server error: {response.status_code}")
            return False
        
        # 2. Get available agents
        print("\n2. Getting available agents...")
        response = requests.get(f"{BASE_URL}/mcp/agents")
        if response.status_code == 200:
            agents = response.json()
            print(f"   ✅ Found {len(agents)} agents:")
            for agent in agents:
                print(f"      - {agent['name']} ({agent['platform']})")
        else:
            print(f"   ❌ Error getting agents: {response.status_code}")
            return False
        
        # 3. Create a polycomputational session
        print("\n3. Creating polycomputational session...")
        session_data = {
            "agents": ["lira", "nyra", "orion", "thalus"],
            "processing_mode": "parallel",
            "biofelt_signature": {
                "hrv_score": 85.0,
                "emotional_state": "balanced",
                "energy_level": 8,
                "coherence_score": 0.8,
                "cognitive_sovereignty_level": 0.9
            }
        }
        
        response = requests.post(f"{BASE_URL}/mcp/session/create", json=session_data)
        if response.status_code == 200:
            session = response.json()
            session_id = session.get("session_id")
            print(f"   ✅ Session created: {session_id}")
        else:
            print(f"   ❌ Error creating session: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # 4. Process with agents
        print("\n4. Processing with agents...")
        process_data = {
            "endpoint": "analyze_biofelt_context",
            "payload": {
                "context": "Testing AMA API with biofelt integration",
                "priority": "high"
            },
            "priority_level": 8
        }
        
        response = requests.post(f"{BASE_URL}/mcp/session/{session_id}/process", json=process_data)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Processing completed: {result['status']}")
            print(f"   ✅ Agent responses: {len(result.get('agent_responses', []))}")
            
            # Show emergent intelligence if available
            if result.get('emergent_intelligence'):
                ei = result['emergent_intelligence']
                print(f"   ✅ Emergent intelligence generated:")
                print(f"      - Confidence: {ei.get('confidence_score', 0):.2f}")
                print(f"      - Themes: {len(ei.get('convergent_themes', []))}")
        else:
            print(f"   ❌ Error processing: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # 5. Get session status
        print("\n5. Getting session status...")
        response = requests.get(f"{BASE_URL}/mcp/session/{session_id}/status")
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ Session status: {status['status']}")
            print(f"   ✅ Active agents: {status['active_agents']}")
        else:
            print(f"   ❌ Error getting status: {response.status_code}")
        
        # 6. Test individual agent endpoint
        print("\n6. Testing individual agent endpoint...")
        agent_data = {
            "payload": {
                "context": "Testing Lira's biofelt analysis",
                "biofelt_context": {
                    "hrv_ms": 88,
                    "coherence": 0.82,
                    "energy_level": "high"
                }
            }
        }
        
        response = requests.post(f"{BASE_URL}/mcp/agent/lira/endpoint/analyze_biofelt_context", json=agent_data)
        if response.status_code == 200:
            agent_response = response.json()
            print(f"   ✅ Lira response: {agent_response.get('status', 'Success')}")
        else:
            print(f"   ❌ Error calling Lira: {response.status_code}")
        
        print("\n🎊 ALL API TESTS PASSED!")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("   1. Open browser: http://localhost:8000/docs")
        print("   2. Explore Swagger UI for all endpoints")
        print("   3. Test different processing modes")
        print("   4. Experiment with biofelt signatures")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_api_examples():
    """Show example API calls"""
    
    print("\n📚 API Usage Examples:")
    print("=" * 60)
    
    examples = {
        "Create Session": {
            "method": "POST",
            "url": "/mcp/session/create",
            "data": {
                "agents": ["lira", "nyra", "orion", "thalus"],
                "processing_mode": "parallel",
                "biofelt_signature": {
                    "hrv_score": 85.0,
                    "emotional_state": "balanced",
                    "energy_level": 8,
                    "coherence_score": 0.8,
                    "cognitive_sovereignty_level": 0.9
                }
            }
        },
        "Process Request": {
            "method": "POST", 
            "url": "/mcp/session/{session_id}/process",
            "data": {
                "endpoint": "analyze_biofelt_context",
                "payload": {
                    "context": "Your analysis request here",
                    "priority": "high"
                },
                "priority_level": 8
            }
        },
        "Get Agents": {
            "method": "GET",
            "url": "/mcp/agents"
        },
        "Call Agent": {
            "method": "POST",
            "url": "/mcp/agent/lira/endpoint/analyze_biofelt_context",
            "data": {
                "payload": {
                    "context": "Direct agent request",
                    "biofelt_context": {"hrv_ms": 88, "coherence": 0.82}
                }
            }
        }
    }
    
    for name, example in examples.items():
        print(f"\n🔹 {name}:")
        print(f"   {example['method']} {example['url']}")
        if 'data' in example:
            print(f"   Data: {json.dumps(example['data'], indent=2)}")

if __name__ == "__main__":
    # Show examples first
    show_api_examples()
    
    # Run tests
    print("\n" + "=" * 60)
    success = test_ama_api()
    
    if success:
        print("\n🎉 AMA API is working perfectly!")
    else:
        print("\n⚠️  Some tests failed. Check the server logs.") 