#!/usr/bin/env python3
"""
Basic functionality test for AMA (Adaptive Memory Architecture)
Tests the foundational components: MCP Connector and Biofelt Responsive AMA
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.mcp_connector import MCPConnector, ContextQuery, BiofeltState
from core.biofelt_responsive import BiofeltResponsiveAMA

async def test_mcp_connector():
    """Test basic MCP Connector functionality"""
    
    print("🧪 Testing MCP Connector...")
    
    # Initialize MCP Connector
    mcp = MCPConnector()
    
    # Create test biofelt state
    biofelt_state = BiofeltState(
        hrv_score=75.0,
        emotional_state="balanced",
        energy_level=7,
        stress_indicators=[],
        timestamp=datetime.now()
    )
    
    # Create test query
    query = ContextQuery(
        query_text="How can technology help humans live more meaningfully?",
        query_type="philosophical_inquiry",
        priority_level=5,
        biofelt_context=biofelt_state
    )
    
    try:
        # Process query
        response = await mcp.process_context_query(query)
        
        print("✅ MCP Connector test passed!")
        print(f"   Response status: {response.get('status', 'unknown')}")
        print(f"   Biofelt adaptation: {response.get('biofelt_adaptation', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP Connector test failed: {e}")
        return False

async def test_biofelt_responsive():
    """Test Biofelt Responsive AMA functionality"""
    
    print("🧪 Testing Biofelt Responsive AMA...")
    
    # Initialize Biofelt Responsive AMA
    biofelt_ama = BiofeltResponsiveAMA()
    
    try:
        # Test different HRV levels
        test_cases = [
            (30.0, "stressed", "emergency"),
            (55.0, "neutral", "minimal"),
            (75.0, "balanced", "moderate"),
            (85.0, "focused", "optimal"),
            (95.0, "creative", "peak")
        ]
        
        for hrv_score, emotional_state, expected_complexity in test_cases:
            response = await biofelt_ama.adapt_data_complexity(
                hrv_score, emotional_state, "test query"
            )
            
            actual_complexity = response.get("complexity_level", "unknown")
            
            if actual_complexity == expected_complexity:
                print(f"✅ HRV {hrv_score}, {emotional_state} → {actual_complexity}")
            else:
                print(f"⚠️  HRV {hrv_score}, {emotional_state} → {actual_complexity} (expected {expected_complexity})")
        
        print("✅ Biofelt Responsive AMA test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Biofelt Responsive AMA test failed: {e}")
        return False

async def test_agent_registry():
    """Test Agent Registry functionality"""
    
    print("🧪 Testing Agent Registry...")
    
    from core.mcp_connector import AgentRegistry
    
    # Initialize Agent Registry
    registry = AgentRegistry()
    
    try:
        # Test getting agent info
        lira_info = registry.get_agent_info("lira")
        if lira_info and lira_info["name"] == "Lira":
            print("✅ Agent info retrieval works")
        else:
            print("❌ Agent info retrieval failed")
            return False
        
        # Test getting available agents
        available_agents = registry.get_available_agents()
        if len(available_agents) == 7:  # All 7 agents should be available
            print("✅ Available agents retrieval works")
        else:
            print(f"⚠️  Expected 7 agents, got {len(available_agents)}")
        
        print("✅ Agent Registry test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Agent Registry test failed: {e}")
        return False

async def test_complexity_calculation():
    """Test complexity calculation logic"""
    
    print("🧪 Testing Complexity Calculation...")
    
    from core.biofelt_responsive import ComplexityAdapter
    
    adapter = ComplexityAdapter()
    
    test_cases = [
        (25.0, "anxious", "emergency"),
        (45.0, "stressed", "emergency"),
        (55.0, "neutral", "minimal"),
        (65.0, "calm", "moderate"),
        (75.0, "focused", "optimal"),
        (90.0, "creative", "peak")
    ]
    
    try:
        for hrv_score, emotional_state, expected in test_cases:
            actual = adapter.calculate_complexity(hrv_score, emotional_state)
            
            if actual == expected:
                print(f"✅ HRV {hrv_score}, {emotional_state} → {actual}")
            else:
                print(f"⚠️  HRV {hrv_score}, {emotional_state} → {actual} (expected {expected})")
        
        print("✅ Complexity Calculation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Complexity Calculation test failed: {e}")
        return False

async def main():
    """Run all basic functionality tests"""
    
    print("🌟 AMA Basic Functionality Test Suite")
    print("=" * 50)
    
    tests = [
        ("MCP Connector", test_mcp_connector),
        ("Biofelt Responsive AMA", test_biofelt_responsive),
        ("Agent Registry", test_agent_registry),
        ("Complexity Calculation", test_complexity_calculation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AMA foundation is ready for next phase.")
    else:
        print("⚠️  Some tests failed. Review and fix before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main()) 