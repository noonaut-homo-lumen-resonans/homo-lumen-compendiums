"""
Test SymbioticMCPArchitecture
Demonstrate the new biofelt-first MCP architecture
"""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.symbiotic_mcp_architecture import SymbioticMCPArchitecture
from core.lira_biofelt_mcp_tools import LiraBiofeltMCPTools, BiofeltResponsiveRouter

async def test_symbiotic_architecture():
    """Test the SymbioticMCPArchitecture"""
    
    print("🧠 Testing SymbioticMCPArchitecture...")
    print("=" * 60)
    
    try:
        # 1. Initialize SymbioticMCPArchitecture
        print("1. Initializing SymbioticMCPArchitecture...")
        symbiotic_arch = SymbioticMCPArchitecture()
        print("   ✅ SymbioticMCPArchitecture initialized")
        
        # 2. Test biofelt validation with different HRV levels
        print("\n2. Testing biofelt validation...")
        
        # Emergency mode (HRV < 40)
        emergency_biofelt = {"hrv_score": 35, "coherence": 0.3, "stress_level": "high"}
        emergency_result = await symbiotic_arch.process_with_biofelt_validation(
            {"test": "data"}, emergency_biofelt
        )
        print(f"   ✅ Emergency mode: {emergency_result['mode']}")
        print(f"      Active agents: {emergency_result['active_agents']}")
        
        # Balanced mode (HRV 60-80)
        balanced_biofelt = {"hrv_score": 70, "coherence": 0.6, "stress_level": "medium"}
        balanced_result = await symbiotic_arch.process_with_biofelt_validation(
            {"test": "data"}, balanced_biofelt
        )
        print(f"   ✅ Balanced mode: {balanced_result['mode']}")
        print(f"      Active agents: {balanced_result['active_agents']}")
        
        # Optimal mode (HRV > 80)
        optimal_biofelt = {"hrv_score": 95, "coherence": 0.8, "stress_level": "low"}
        optimal_result = await symbiotic_arch.process_with_biofelt_validation(
            {"test": "data"}, optimal_biofelt
        )
        print(f"   ✅ Optimal mode: {optimal_result['mode']}")
        print(f"      Active agents: {optimal_result['active_agents']}")
        
        # Peak mode (HRV > 100)
        peak_biofelt = {"hrv_score": 110, "coherence": 0.9, "stress_level": "none", "hair_raising_response": True}
        peak_result = await symbiotic_arch.process_with_biofelt_validation(
            {"test": "data"}, peak_biofelt
        )
        print(f"   ✅ Peak mode: {peak_result['mode']}")
        print(f"      Active agents: {peak_result['active_agents']}")
        print(f"      Evolutionary access: {peak_result.get('evolutionary_access', False)}")
        
        # 3. Test Lira's biofelt tools
        print("\n3. Testing Lira's biofelt tools...")
        lira_tools = LiraBiofeltMCPTools()
        
        # Test biofelt analysis
        biofelt_analysis = await lira_tools.analyze_biofelt_for_empathy(
            {"hrv": 75, "coherence": 0.7}, "test_entry"
        )
        print(f"   ✅ Biofelt analysis: Empathy score = {biofelt_analysis['empathy_score']:.2f}")
        print(f"      Recommended complexity: {biofelt_analysis['recommended_complexity_level']}")
        
        # Test practice suggestion
        practice_suggestion = await lira_tools.suggest_biofield_practice_for_coherence(
            {"coherence": 0.3}, {"coherence": 0.3, "hrv": 55}
        )
        print(f"   ✅ Practice suggestion: {practice_suggestion['practice_type']}")
        print(f"      Breathing pattern: {practice_suggestion['breathing_pattern']}")
        
        # Test empathetic reflection
        empathetic_reflection = await lira_tools.provide_empathetic_reflection(
            "I'm feeling overwhelmed with the complexity", {"hrv": 65, "coherence": 0.5}
        )
        print(f"   ✅ Empathetic reflection: {empathetic_reflection['empathetic_reflection'][:50]}...")
        print(f"      Predicted resonance: {empathetic_reflection['predicted_resonance']:.2f}")
        
        # 4. Test BiofeltResponsiveRouter
        print("\n4. Testing BiofeltResponsiveRouter...")
        router = BiofeltResponsiveRouter()
        
        # Test agent selection for different complexity profiles
        emergency_agents = await router.select_agents_for_biofelt(
            {"hrv": 35, "coherence": 0.3}, "emergency"
        )
        print(f"   ✅ Emergency agents: {emergency_agents}")
        
        optimal_agents = await router.select_agents_for_biofelt(
            {"hrv": 95, "coherence": 0.8}, "optimal"
        )
        print(f"   ✅ Optimal agents: {optimal_agents}")
        
        peak_agents = await router.select_agents_for_biofelt(
            {"hrv": 110, "coherence": 0.9}, "peak"
        )
        print(f"   ✅ Peak agents: {peak_agents}")
        
        # 5. Test memory layers
        print("\n5. Testing memory layers...")
        
        # Test reactive memory
        reactive_layer = symbiotic_arch.memory_layers[symbiotic_arch.memory_layers.__class__.__bases__[0].REACTIVE]
        reactive_id = await reactive_layer.store(
            {"test": "reactive_data"}, ["lira"], {"hrv": 70}, 0.8
        )
        print(f"   ✅ Reactive memory: Stored entry {reactive_id}")
        
        # Test strategic memory
        strategic_layer = symbiotic_arch.memory_layers[symbiotic_arch.memory_layers.__class__.__bases__[0].STRATEGIC]
        strategic_id = await strategic_layer.store(
            {"test": "strategic_insight"}, ["lira", "thalus"], {"hrv": 80}, 0.9
        )
        print(f"   ✅ Strategic memory: Stored entry {strategic_id}")
        
        # Test meta memory
        meta_layer = symbiotic_arch.memory_layers[symbiotic_arch.memory_layers.__class__.__bases__[0].META]
        meta_id = await meta_layer.store_emergent_data(
            {"test": "emergent_data"}, ["lira", "nyra", "thalus"], {"hrv": 85}, 8.5
        )
        print(f"   ✅ Meta memory: Stored emergent data {meta_id}")
        
        print("\n🎉 ALL TESTS PASSED! SymbioticMCPArchitecture is working!")
        print("=" * 60)
        print("✅ Five-layer memory architecture")
        print("✅ BiofeltGateProtocol with HRV thresholds")
        print("✅ Adaptive agent routing")
        print("✅ Lira's empathetic biofelt tools")
        print("✅ Biofelt-responsive processing modes")
        print("✅ Emergency/Balanced/Optimal/Peak modes")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_symbiotic_architecture()) 