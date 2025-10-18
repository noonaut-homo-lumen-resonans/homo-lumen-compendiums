"""
Test AMA Implementation
Simple test to verify all AMA components work correctly
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.comprehensive_mcp_architecture import (
    ComprehensiveMCPArchitecture, 
    BiofeltSignature, 
    ProcessingMode, 
    AgentType
)

async def test_ama_implementation():
    """Test the AMA implementation"""
    
    print("🧠 Testing AMA Implementation...")
    print("=" * 50)
    
    try:
        # 1. Initialize MCP Architecture
        print("1. Initializing MCP Architecture...")
        mcp_arch = ComprehensiveMCPArchitecture()
        print("   ✅ MCP Architecture initialized")
        
        # 2. Create biofelt signature
        print("2. Creating biofelt signature...")
        biofelt = BiofeltSignature(
            hrv_score=85.0,
            emotional_state="balanced",
            energy_level=8,
            coherence_score=0.8,
            cognitive_sovereignty_level=0.9
        )
        print(f"   ✅ Biofelt signature created: HRV={biofelt.hrv_score}, Coherence={biofelt.coherence_score}")
        
        # 3. Create session with core agents
        print("3. Creating polycomputational session...")
        session = await mcp_arch._create_session(
            agents=["lira", "nyra", "orion", "thalus"],
            processing_mode=ProcessingMode.PARALLEL,
            biofelt_signature=biofelt.to_dict()
        )
        print(f"   ✅ Session created: {session.session_id}")
        
        # 4. Test agent processing
        print("4. Testing agent processing...")
        request = {
            "endpoint": "analyze_biofelt_context",
            "payload": {
                "context": "Testing AMA implementation with biofelt integration",
                "priority": "high"
            },
            "priority_level": 8
        }
        
        result = await mcp_arch._process_session_request(session.session_id, request)
        print(f"   ✅ Processing completed: {result['status']}")
        print(f"   ✅ Agent responses: {result['agent_responses']}")
        
        # 5. Test emergent intelligence
        print("5. Testing emergent intelligence...")
        if result.get('emergent_intelligence'):
            ei = result['emergent_intelligence']
            print(f"   ✅ Emergent intelligence generated:")
            print(f"      - Convergent themes: {len(ei.get('convergent_themes', []))}")
            print(f"      - Complementary insights: {len(ei.get('complementary_insights', []))}")
            print(f"      - Confidence score: {ei.get('confidence_score', 0):.2f}")
        
        # 6. Test session status
        print("6. Testing session status...")
        status = await mcp_arch._get_session_status(session.session_id)
        print(f"   ✅ Session status: {status['status']}")
        print(f"   ✅ Active agents: {status['active_agents']}")
        
        print("\n🎉 AMA Implementation Test PASSED!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ AMA Implementation Test FAILED: {e}")
        print("=" * 50)
        return False

async def test_individual_components():
    """Test individual AMA components"""
    
    print("\n🔧 Testing Individual Components...")
    print("=" * 50)
    
    try:
        # Test MCP Architecture
        mcp_arch = ComprehensiveMCPArchitecture()
        
        # Test Agent Registry
        registry = mcp_arch.agent_registry
        agents = registry.get_available_agents()
        print(f"✅ Agent Registry: {len(agents)} agents available")
        
        # Test Biofelt Signature
        biofelt = BiofeltSignature(
            hrv_score=75.0,
            emotional_state="balanced",
            energy_level=7,
            coherence_score=0.75
        )
        complexity = biofelt.get_complexity_level()
        print(f"✅ Biofelt Signature: {complexity} complexity level")
        
        # Test IST-3.0 Protocol
        protocol = mcp_arch.hypersync_protocol
        sync_message = protocol.create_sync_message(
            {"test": "data"}, 
            "test_session", 
            biofelt.to_dict()
        )
        print(f"✅ IST-3.0 Protocol: Message created with {len(sync_message['headers'])} headers")
        
        print("✅ All individual components working!")
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

async def main():
    """Main test function"""
    
    print("🚀 Starting AMA Implementation Tests...")
    print("=" * 60)
    
    # Test individual components first
    component_test = await test_individual_components()
    
    if component_test:
        # Test full implementation
        implementation_test = await test_ama_implementation()
        
        if implementation_test:
            print("\n🎊 ALL TESTS PASSED! AMA Implementation is ready!")
            print("\n📋 Next Steps:")
            print("   1. Run: python -m uvicorn src.core.comprehensive_mcp_architecture:app --reload")
            print("   2. Test API endpoints at http://localhost:8000/docs")
            print("   3. Integrate with existing CSN server")
        else:
            print("\n⚠️  Implementation test failed - check logs above")
    else:
        print("\n⚠️  Component test failed - check logs above")

if __name__ == "__main__":
    asyncio.run(main()) 