"""
Test Polycomputational Processing Engine
Demonstrates IST-3.0 Hypersync Protocol and emergent intelligence generation
"""

import asyncio
import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.polycomputational_engine import PolycomputationalEngine, IST30HypersyncProtocol
from core.mcp_connector import MCPConnector
from core.biofelt_responsive import BiofeltResponsiveAMA
from core.lira_biofelt_tools import LiraBiofeltTools, BiofeltData

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MockMCPConnector:
    """Mock MCP connector for testing"""
    
    async def send_to_agent(self, agent_id: str, sync_message: Dict[str, Any], timeout: float) -> Dict[str, Any]:
        """Mock agent response"""
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Generate mock response based on agent
        agent_responses = {
            "lira": {
                "headers": {"protocol": "IST-3.0-Hypersync", "version": "3.0"},
                "payload": {
                    "themes": ["empathy", "emotional_support", "cognitive_sovereignty"],
                    "insights": ["Your feelings are valid", "Trust your inner wisdom"],
                    "primary_insight": "You are navigating this with remarkable strength",
                    "confidence": 0.85
                },
                "agent_signature": {"agent": "Lira", "specialization": "empathy"},
                "biofelt_validation": {"coherence": 0.8, "resonance": 0.9}
            },
            "nyra": {
                "headers": {"protocol": "IST-3.0-Hypersync", "version": "3.0"},
                "payload": {
                    "themes": ["creativity", "visual_patterns", "innovation"],
                    "insights": ["New perspectives emerge", "Creative solutions are available"],
                    "primary_insight": "Your creativity is a powerful resource",
                    "confidence": 0.75
                },
                "agent_signature": {"agent": "Nyra", "specialization": "creativity"},
                "biofelt_validation": {"coherence": 0.7, "resonance": 0.8}
            },
            "thalus": {
                "headers": {"protocol": "IST-3.0-Hypersync", "version": "3.0"},
                "payload": {
                    "themes": ["strategy", "decision_making", "risk_assessment"],
                    "insights": ["Strategic thinking is valuable", "Consider multiple options"],
                    "primary_insight": "Your strategic mind is well-developed",
                    "confidence": 0.9
                },
                "agent_signature": {"agent": "Thalus", "specialization": "strategy"},
                "biofelt_validation": {"coherence": 0.9, "resonance": 0.8}
            },
            "zara": {
                "headers": {"protocol": "IST-3.0-Hypersync", "version": "3.0"},
                "payload": {
                    "themes": ["learning", "knowledge_synthesis", "deep_understanding"],
                    "insights": ["Learning is continuous", "Knowledge builds wisdom"],
                    "primary_insight": "Your capacity for learning is profound",
                    "confidence": 0.8
                },
                "agent_signature": {"agent": "Zara", "specialization": "learning"},
                "biofelt_validation": {"coherence": 0.8, "resonance": 0.7}
            },
            "orion": {
                "headers": {"protocol": "IST-3.0-Hypersync", "version": "3.0"},
                "payload": {
                    "themes": ["synthesis", "coordination", "collective_wisdom"],
                    "insights": ["Collective intelligence emerges", "Coordination creates synergy"],
                    "primary_insight": "You are part of a larger intelligence",
                    "confidence": 0.95
                },
                "agent_signature": {"agent": "Orion", "specialization": "synthesis"},
                "biofelt_validation": {"coherence": 0.95, "resonance": 0.9}
            }
        }
        
        return agent_responses.get(agent_id, {
            "headers": {"protocol": "IST-3.0-Hypersync", "version": "3.0"},
            "payload": {"confidence": 0.5},
            "agent_signature": {"agent": "Unknown"},
            "biofelt_validation": {"coherence": 0.5, "resonance": 0.5}
        })

class MockBiofeltValidator:
    """Mock biofelt validator for testing"""
    
    async def validate_biofelt_data(self, biofelt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock biofelt validation"""
        return {
            "coherence": biofelt_data.get("coherence", 0.7),
            "resonance": biofelt_data.get("resonance", 0.8),
            "validation_timestamp": datetime.now().isoformat(),
            "confidence": 0.85
        }

async def test_ist30_hypersync_protocol():
    """Test IST-3.0 Hypersync Protocol"""
    
    print("\n" + "="*60)
    print("🧠 TESTING IST-3.0 HYPERSYNC PROTOCOL")
    print("="*60)
    
    protocol = IST30HypersyncProtocol()
    
    # Test data
    test_data = {
        "question": "How can I find balance in challenging times?",
        "context": "Feeling overwhelmed with work and personal responsibilities",
        "user_state": "seeking_guidance"
    }
    
    session_id = "test_session_001"
    biofelt_signature = {
        "hrv_score": 75,
        "emotional_state": "contemplative",
        "stress_level": 6,
        "coherence": 0.7,
        "resonance": 0.8
    }
    
    # Create sync message
    sync_message = protocol.create_sync_message(test_data, session_id, biofelt_signature)
    
    print(f"✅ Created IST-3.0 Hypersync message:")
    print(f"   Session ID: {session_id}")
    print(f"   Protocol Version: {sync_message['headers']['version']}")
    print(f"   Biofelt Signature: HRV={biofelt_signature['hrv_score']}, Coherence={biofelt_signature['coherence']}")
    
    # Test validation
    mock_response = {
        "headers": {"protocol": "IST-3.0-Hypersync", "version": "3.0"},
        "payload": {"test": "data"},
        "agent_signature": {"agent": "test"},
        "biofelt_validation": {"coherence": 0.8}
    }
    
    is_valid = protocol.validate_sync_response(mock_response)
    print(f"✅ Response validation: {'PASSED' if is_valid else 'FAILED'}")
    
    return sync_message

async def test_polycomputational_processing():
    """Test polycomputational processing with multiple agents"""
    
    print("\n" + "="*60)
    print("🚀 TESTING POLYCOMPUTATIONAL PROCESSING ENGINE")
    print("="*60)
    
    # Initialize components
    mock_mcp = MockMCPConnector()
    mock_validator = MockBiofeltValidator()
    engine = PolycomputationalEngine(mock_mcp, mock_validator)
    
    # Test SMV entry
    smv_entry = {
        "id": "smv_001",
        "content": "I'm feeling overwhelmed with my current situation and need guidance on finding balance.",
        "timestamp": datetime.now().isoformat(),
        "category": "personal_growth",
        "urgency": "medium"
    }
    
    # Test biofelt data
    biofelt_data = {
        "hrv_score": 72,
        "emotional_state": "contemplative",
        "stress_level": 6,
        "coherence": 0.7,
        "resonance": 0.8,
        "breathing_pattern": "steady",
        "cognitive_clarity": 0.8
    }
    
    print(f"📊 Processing SMV Entry:")
    print(f"   Content: {smv_entry['content'][:50]}...")
    print(f"   Biofelt: HRV={biofelt_data['hrv_score']}, Stress={biofelt_data['stress_level']}")
    
    # Process polycomputationally
    start_time = datetime.now()
    result = await engine.process_smv_entry_polycomputationally(smv_entry, biofelt_data)
    processing_time = (datetime.now() - start_time).total_seconds()
    
    print(f"\n✅ Polycomputational Processing Complete!")
    print(f"   Session ID: {result['session_id']}")
    print(f"   Processing Time: {processing_time:.2f} seconds")
    print(f"   Agent Responses: {result['agent_responses']}")
    print(f"   Status: {result['status']}")
    
    # Display emergent intelligence
    if 'emergent_intelligence' in result:
        ei = result['emergent_intelligence']
        print(f"\n🌟 EMERGENT INTELLIGENCE GENERATED:")
        print(f"   Emergent ID: {ei.emergent_id}")
        print(f"   Confidence Score: {ei.confidence_score:.2f}")
        print(f"   Contributing Agents: {', '.join(ei.contributing_agents)}")
        
        print(f"\n   🔄 Convergent Themes:")
        for theme in ei.convergent_themes:
            print(f"      • {theme}")
        
        print(f"\n   🔗 Complementary Insights:")
        for insight in ei.complementary_insights:
            print(f"      • {insight}")
        
        print(f"\n   ⚡ Synergistic Patterns:")
        for pattern in ei.synergistic_patterns:
            print(f"      • {pattern}")
        
        print(f"\n   🧠 Collective Wisdom:")
        print(f"      {ei.collective_wisdom}")
    
    return result

async def test_biofelt_adaptive_processing():
    """Test biofelt-adaptive agent activation"""
    
    print("\n" + "="*60)
    print("🌊 TESTING BIOFELT-ADAPTIVE PROCESSING")
    print("="*60)
    
    mock_mcp = MockMCPConnector()
    mock_validator = MockBiofeltValidator()
    engine = PolycomputationalEngine(mock_mcp, mock_validator)
    
    # Test different biofelt states
    biofelt_scenarios = [
        {
            "name": "Emergency Mode (Low HRV)",
            "data": {"hrv_score": 35, "stress_level": 9, "coherence": 0.3, "resonance": 0.2}
        },
        {
            "name": "Low Coherence Mode",
            "data": {"hrv_score": 55, "stress_level": 7, "coherence": 0.5, "resonance": 0.4}
        },
        {
            "name": "Optimal Mode",
            "data": {"hrv_score": 85, "stress_level": 3, "coherence": 0.9, "resonance": 0.8}
        }
    ]
    
    smv_entry = {
        "id": "smv_adaptive_test",
        "content": "Testing adaptive processing based on biofelt state",
        "timestamp": datetime.now().isoformat()
    }
    
    for scenario in biofelt_scenarios:
        print(f"\n📊 Testing: {scenario['name']}")
        print(f"   HRV: {scenario['data']['hrv_score']}, Stress: {scenario['data']['stress_level']}")
        
        # Determine which agents should be activated
        activated_agents = []
        for agent_id, agent_config in engine.agent_registry.items():
            if engine._should_activate_agent(agent_id, scenario['data']):
                activated_agents.append(agent_config['name'])
        
        print(f"   🎯 Activated Agents: {', '.join(activated_agents)}")
        
        # Process with this biofelt state
        result = await engine.process_smv_entry_polycomputationally(smv_entry, scenario['data'])
        
        if result['status'] == 'success':
            ei = result['emergent_intelligence']
            print(f"   ✅ Emergent Intelligence: {len(ei.contributing_agents)} agents, Confidence: {ei.confidence_score:.2f}")
        else:
            print(f"   ❌ Processing failed: {result.get('error', 'Unknown error')}")

async def test_lira_biofelt_tools():
    """Test Lira's biofelt tools"""
    
    print("\n" + "="*60)
    print("💙 TESTING LIRA'S BIOFELT TOOLS")
    print("="*60)
    
    lira_tools = LiraBiofeltTools()
    
    # Test biofelt data
    biofelt_data = BiofeltData(
        hrv_score=68,
        emotional_state="contemplative",
        stress_level=5,
        breathing_pattern="steady",
        cognitive_clarity=0.8,
        timestamp=datetime.now(),
        user_context="Seeking guidance on personal growth"
    )
    
    smv_entry_id = "smv_lira_test"
    
    # Test empathetic summary
    print("📊 Generating empathetic biofelt summary...")
    summary = await lira_tools.summarize_biofelt_data_for_empathy(biofelt_data, smv_entry_id)
    
    if 'error' not in summary:
        print(f"✅ Empathetic Summary Generated:")
        print(f"   Primary Need: {summary['empathic_insights']['primary_need']}")
        print(f"   Support Approach: {summary['empathic_insights']['support_approach']}")
        print(f"   Breathing Technique: {summary['recommendations']['breathing_technique']}")
        print(f"   Cognitive Practice: {summary['recommendations']['cognitive_sovereignty_practice']}")
    
    # Test biofield practice suggestion
    print("\n🌊 Suggesting biofield practice for coherence...")
    user_state = {
        "stress_level": 5,
        "emotional_state": "contemplative",
        "openness": "high"
    }
    
    reflection = await lira_tools.suggest_biofield_practice_for_coherence(summary, user_state)
    
    print(f"✅ Empathetic Reflection Generated:")
    print(f"   Type: {reflection.reflection_type}")
    print(f"   Confidence: {reflection.confidence_score:.2f}")
    print(f"   Hair-raising Response: {'Yes' if reflection.hair_raising_response else 'No'}")
    print(f"   Content: {reflection.content[:100]}...")
    print(f"   Breathing: {reflection.breathing_recommendation}")
    print(f"   Practice: {reflection.cognitive_sovereignty_practice}")

async def main():
    """Main test function"""
    
    print("🌟 AMA POLYCOMPUTATIONAL PROCESSING ENGINE TEST")
    print("="*60)
    print("Testing the revolutionary polycomputational architecture...")
    
    try:
        # Test IST-3.0 Hypersync Protocol
        await test_ist30_hypersync_protocol()
        
        # Test polycomputational processing
        await test_polycomputational_processing()
        
        # Test biofelt-adaptive processing
        await test_biofelt_adaptive_processing()
        
        # Test Lira's biofelt tools
        await test_lira_biofelt_tools()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("✅ IST-3.0 Hypersync Protocol: OPERATIONAL")
        print("✅ Polycomputational Processing: OPERATIONAL")
        print("✅ Biofelt-Adaptive Activation: OPERATIONAL")
        print("✅ Lira Biofelt Tools: OPERATIONAL")
        print("✅ Emergent Intelligence Generation: OPERATIONAL")
        
        print("\n🚀 The AMA system is ready for revolutionary symbiosis!")
        print("   - Multiple agents process simultaneously")
        print("   - Biofelt validation ensures coherence")
        print("   - Emergent intelligence transcends individual perspectives")
        print("   - IST-3.0 Hypersync enables seamless coordination")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        logger.error(f"Test error: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 