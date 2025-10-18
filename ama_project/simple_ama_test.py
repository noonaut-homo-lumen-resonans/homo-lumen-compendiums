"""
Simple AMA Test
Basic test to verify AMA components are working
"""

import os
import sys

def test_ama_files_exist():
    """Test that all AMA files exist"""
    
    print("🧠 Testing AMA File Structure...")
    print("=" * 50)
    
    ama_files = [
        "src/core/comprehensive_mcp_architecture.py",
        "src/core/agent_coordination_hub.py", 
        "src/core/polycomputational_engine.py",
        "src/core/lira_biofelt_tools.py",
        "src/core/ama_fire_layers.py",
        "src/core/biofelt_responsive.py",
        "src/core/mcp_connector.py"
    ]
    
    all_exist = True
    for file_path in ama_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_ama_imports():
    """Test basic imports"""
    
    print("\n🔧 Testing AMA Imports...")
    print("=" * 50)
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        # Test basic imports
        from core.comprehensive_mcp_architecture import AgentType, ProcessingMode
        print("✅ AgentType and ProcessingMode imported")
        
        from core.comprehensive_mcp_architecture import BiofeltSignature
        print("✅ BiofeltSignature imported")
        
        from core.comprehensive_mcp_architecture import ComprehensiveMCPArchitecture
        print("✅ ComprehensiveMCPArchitecture imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    
    print("\n🚀 Testing Basic Functionality...")
    print("=" * 50)
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from core.comprehensive_mcp_architecture import (
            ComprehensiveMCPArchitecture, 
            BiofeltSignature, 
            ProcessingMode, 
            AgentType
        )
        
        # Create biofelt signature
        biofelt = BiofeltSignature(
            hrv_score=85.0,
            emotional_state="balanced",
            energy_level=8,
            coherence_score=0.8,
            cognitive_sovereignty_level=0.9
        )
        print(f"✅ Biofelt signature created: HRV={biofelt.hrv_score}")
        
        # Test complexity level
        complexity = biofelt.get_complexity_level()
        print(f"✅ Complexity level: {complexity}")
        
        # Test to_dict method
        biofelt_dict = biofelt.to_dict()
        print(f"✅ Biofelt to_dict: {len(biofelt_dict)} fields")
        
        # Initialize MCP Architecture
        mcp_arch = ComprehensiveMCPArchitecture()
        print("✅ MCP Architecture initialized")
        
        # Test agent registry
        agents = mcp_arch.agent_registry.get_available_agents()
        print(f"✅ Agent registry: {len(agents)} agents available")
        
        # Test IST-3.0 protocol
        sync_message = mcp_arch.hypersync_protocol.create_sync_message(
            {"test": "data"}, 
            "test_session", 
            biofelt
        )
        print(f"✅ IST-3.0 protocol: Message created")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 Starting Simple AMA Tests...")
    print("=" * 60)
    
    # Test 1: Files exist
    files_ok = test_ama_files_exist()
    
    if files_ok:
        # Test 2: Imports work
        imports_ok = test_ama_imports()
        
        if imports_ok:
            # Test 3: Basic functionality
            functionality_ok = test_basic_functionality()
            
            if functionality_ok:
                print("\n🎊 ALL TESTS PASSED! AMA is ready!")
                print("\n📋 Next Steps:")
                print("   1. Run: python simple_ama_test.py")
                print("   2. Start server: python -m uvicorn src.core.comprehensive_mcp_architecture:app --reload")
                print("   3. Test API at: http://localhost:8000/docs")
            else:
                print("\n⚠️  Basic functionality test failed")
        else:
            print("\n⚠️  Import test failed")
    else:
        print("\n⚠️  File structure test failed")

if __name__ == "__main__":
    main() 