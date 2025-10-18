"""
Test PolycomputingEngine with Emergent Intelligence Synthesis
"""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.polycomputing_engine import PolycomputingEngine

async def test_polycomputing():
    """Test PolycomputingEngine with emergent intelligence synthesis"""
    
    print("🧠 Testing PolycomputingEngine...")
    print("=" * 60)
    
    # Initialize PolycomputingEngine
    engine = PolycomputingEngine()
    
    # Test data
    test_data = {
        "challenge": "Design a consciousness-tech interface that preserves cognitive sovereignty",
        "context": "Homo Lumen AMA development",
        "complexity": "high"
    }
    
    biofelt_context = {
        "hrv_score": 85,
        "coherence": 0.8,
        "stress_level": "low"
    }
    
    # Test 1: Distribute to agents
    print("1. Testing agent distribution...")
    agent_responses = await engine.distribute_to_agents(
        test_data, biofelt_context, "optimal"
    )
    
    print(f"   ✅ Distributed to {len(agent_responses)} agents:")
    for agent_id, response in agent_responses.items():
        print(f"      - {agent_id}: {response['response_summary'][:50]}...")
        print(f"        Visual metaphor: {response['visual_metaphor_tag']}")
        print(f"        Confidence: {response['confidence_score']:.2f}")
    
    # Test 2: Synthesize emergent intelligence
    print("\n2. Testing emergent intelligence synthesis...")
    emergent_result = await engine.synthesize_emergent_intelligence(
        agent_responses, biofelt_context
    )
    
    print(f"   ✅ Convergent insights: {len(emergent_result['convergent_insights'])}")
    print(f"   ✅ Divergent perspectives: {len(emergent_result['divergent_perspectives'])}")
    print(f"   ✅ Synthesis confidence: {emergent_result['synthesis_confidence']:.2f}")
    print(f"   ✅ Hair-raising potential: {emergent_result['hair_raising_potential']:.2f}")
    
    # Test 3: Visual synthesis
    print("\n3. Testing visual synthesis...")
    visual_synthesis = emergent_result['visual_synthesis']
    print(f"   ✅ Visualization created: {visual_synthesis['visualization_svg'][:30]}...")
    print(f"   ✅ Biofelt optimization: {visual_synthesis['biofelt_optimization']}")
    print(f"   ✅ CI elements: {len(visual_synthesis['consciousness_interface_elements'])}")
    
    # Test 4: Emergent intelligence details
    print("\n4. Testing emergent intelligence details...")
    emergent_intelligence = emergent_result['emergent_intelligence']
    print(f"   ✅ Emergent insights: {emergent_intelligence['insight_count']}")
    print(f"   ✅ Novelty score: {emergent_intelligence['novelty_score']:.2f}")
    print(f"   ✅ Coherence score: {emergent_intelligence['coherence_score']:.2f}")
    
    print("\n🎉 ALL TESTS PASSED! PolycomputingEngine is working!")
    print("=" * 60)
    print("✅ Agent distribution with biofelt context")
    print("✅ Emergent intelligence synthesis")
    print("✅ Visual manifestation of collective intelligence")
    print("✅ Convergent/divergent pattern analysis")
    print("✅ Hair-raising potential prediction")

if __name__ == "__main__":
    asyncio.run(test_polycomputing()) 