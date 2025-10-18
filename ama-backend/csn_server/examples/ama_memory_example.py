"""
AMA Four-Layer Memory System - Comprehensive Example

This example demonstrates the complete AMA memory system with all four layers,
biofield validation, Firestore integration, and comprehensive logging.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Example usage of the AMA Memory System
async def demonstrate_ama_memory_system():
    """Demonstrate all features of the AMA memory system"""
    
    print("🌟 AMA Four-Layer Memory System Demonstration")
    print("=" * 60)
    
    # Initialize the memory system
    from csn_server.routers.ama_memory_layers import (
        AMAMemorySystem, BiofieldMetrics, MemoryLayer
    )
    
    # Use a test project ID for demonstration
    project_id = "csn-demo-project"
    memory_system = AMAMemorySystem(project_id)
    
    print(f"✅ AMA Memory System initialized with project: {project_id}")
    
    # 1. Biofield Validation Example
    print("\n🔬 Biofield Validation Example")
    print("-" * 40)
    
    # Valid biofield metrics
    valid_biofield = BiofieldMetrics(
        hrv_ms=95.0,  # > 80ms required
        breath_pattern=[4, 6, 8],  # Exact pattern required
        coherence_score=0.85  # > 0.7 required
    )
    
    # Invalid biofield metrics
    invalid_biofield = BiofieldMetrics(
        hrv_ms=65.0,  # < 80ms - will fail
        breath_pattern=[4, 6, 8],  # Correct pattern
        coherence_score=0.85  # Good coherence
    )
    
    try:
        validation_result = await memory_system.validate_biofield(valid_biofield)
        print(f"✅ Valid biofield validation: {validation_result.is_valid}")
        print(f"   HRV: {validation_result.hrv_passed}")
        print(f"   Breath: {validation_result.breath_passed}")
        print(f"   Coherence: {validation_result.coherence_passed}")
        print(f"   Overall Score: {validation_result.overall_score:.2f}")
    except Exception as e:
        print(f"❌ Biofield validation failed: {e}")
    
    # 2. Reactive Memory Layer Example
    print("\n⚡ Reactive Memory Layer Example")
    print("-" * 40)
    
    reactive_content = {
        "event_type": "user_interaction",
        "user_id": "user_123",
        "action": "button_click",
        "timestamp": datetime.utcnow().isoformat(),
        "session_data": {
            "page": "/dashboard",
            "duration": 45.2
        }
    }
    
    try:
        entry_id = await memory_system.create_reactive_entry(
            content=reactive_content,
            priority=8,  # High priority
            biofield_metrics=valid_biofield
        )
        print(f"✅ Reactive entry created: {entry_id}")
        
        # Update frequency
        await memory_system.reactive_manager.update_frequency(entry_id)
        print(f"✅ Frequency updated for: {entry_id}")
        
    except Exception as e:
        print(f"❌ Reactive memory creation failed: {e}")
    
    # 3. Strategic Memory Layer Example
    print("\n🧠 Strategic Memory Layer Example")
    print("-" * 40)
    
    strategic_content = {
        "analysis_type": "user_behavior_pattern",
        "user_id": "user_123",
        "timeframe": "last_7_days",
        "data_points": 150
    }
    
    patterns = [
        "morning_peak_activity",
        "preference_for_visual_content",
        "consistent_session_duration"
    ]
    
    agent_synthesis = {
        "primary_agent": "behavior_analyzer",
        "confidence": 0.87,
        "recommendations": [
            "optimize_morning_ui",
            "increase_visual_content",
            "maintain_session_flow"
        ],
        "cross_references": ["user_123", "similar_users_group"]
    }
    
    try:
        entry_id = await memory_system.create_strategic_entry(
            content=strategic_content,
            patterns=patterns,
            agent_synthesis=agent_synthesis,
            biofield_metrics=valid_biofield
        )
        print(f"✅ Strategic entry created: {entry_id}")
        print(f"   Patterns identified: {len(patterns)}")
        print(f"   Agent synthesis confidence: {agent_synthesis['confidence']}")
        
    except Exception as e:
        print(f"❌ Strategic memory creation failed: {e}")
    
    # 4. Meta Memory Layer Example
    print("\n🔍 Meta Memory Layer Example")
    print("-" * 40)
    
    meta_content = {
        "insight_type": "cross_platform_correlation",
        "scope": "global_user_behavior",
        "data_sources": ["web", "mobile", "api"],
        "analysis_period": "30_days"
    }
    
    insights = [
        "Users prefer mobile for quick actions, web for detailed work",
        "API usage peaks during business hours globally",
        "Cross-platform users have 3x higher engagement",
        "Mobile-first users show different feature preferences"
    ]
    
    correlations = {
        "platform_usage": ["web_engagement", "mobile_engagement", "api_usage"],
        "time_patterns": ["business_hours", "weekend_usage", "timezone_peaks"],
        "user_segments": ["power_users", "casual_users", "enterprise_users"]
    }
    
    try:
        entry_id = await memory_system.create_meta_entry(
            content=meta_content,
            insights=insights,
            correlations=correlations,
            biofield_metrics=valid_biofield
        )
        print(f"✅ Meta entry created: {entry_id}")
        print(f"   Insights generated: {len(insights)}")
        print(f"   Correlation groups: {len(correlations)}")
        
    except Exception as e:
        print(f"❌ Meta memory creation failed: {e}")
    
    # 5. Evolutionary Memory Layer Example
    print("\n🌱 Evolutionary Memory Layer Example")
    print("-" * 40)
    
    evolutionary_content = {
        "principle_type": "system_architecture",
        "domain": "user_experience",
        "validation_level": "core",
        "applicability": "universal"
    }
    
    core_principles = [
        "User-centric design always prioritizes accessibility",
        "Performance optimization should never compromise security",
        "Data privacy is non-negotiable across all features",
        "Scalability must be considered from day one",
        "Error handling should be graceful and informative"
    ]
    
    try:
        entry_id = await memory_system.create_evolutionary_entry(
            content=evolutionary_content,
            core_principles=core_principles,
            biofield_metrics=valid_biofield  # Required for evolutionary layer
        )
        print(f"✅ Evolutionary entry created: {entry_id}")
        print(f"   Core principles: {len(core_principles)}")
        print(f"   Biofield validation: PASSED")
        
    except Exception as e:
        print(f"❌ Evolutionary memory creation failed: {e}")
    
    # 6. Query Examples
    print("\n🔍 Query Examples")
    print("-" * 40)
    
    try:
        # Query reactive entries
        reactive_entries = await memory_system.query_layer(
            MemoryLayer.REACTIVE,
            filters=[{"field": "priority", "op": ">=", "value": 5}],
            limit=10
        )
        print(f"✅ Reactive entries (priority >= 5): {len(reactive_entries)}")
        
        # Query strategic entries
        strategic_entries = await memory_system.query_layer(
            MemoryLayer.STRATEGIC,
            filters=[{"field": "confidence_score", "op": ">=", "value": 0.8}],
            limit=10
        )
        print(f"✅ Strategic entries (confidence >= 0.8): {len(strategic_entries)}")
        
        # Query meta entries
        meta_entries = await memory_system.query_layer(
            MemoryLayer.META,
            limit=10
        )
        print(f"✅ Meta entries: {len(meta_entries)}")
        
        # Query evolutionary entries
        evolutionary_entries = await memory_system.query_layer(
            MemoryLayer.EVOLUTIONARY,
            limit=10
        )
        print(f"✅ Evolutionary entries: {len(evolutionary_entries)}")
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
    
    # 7. System Status
    print("\n📊 System Status")
    print("-" * 40)
    
    try:
        status = await memory_system.get_system_status()
        print(f"✅ System status retrieved")
        print(f"   Timestamp: {status['timestamp']}")
        print(f"   Biofield validation requirements:")
        print(f"     - Min HRV: {status['biofield_validation']['min_hrv']}ms")
        print(f"     - Breath pattern: {status['biofield_validation']['required_breath_pattern']}")
        print(f"     - Min coherence: {status['biofield_validation']['min_coherence']}")
        
        print(f"   Layer status:")
        for layer, layer_status in status['layers'].items():
            status_icon = "✅" if layer_status.get('active', False) else "❌"
            print(f"     {status_icon} {layer}: {layer_status.get('entry_count', 0)} entries")
            
    except Exception as e:
        print(f"❌ System status failed: {e}")
    
    # 8. Biofield Validation Failure Example
    print("\n⚠️ Biofield Validation Failure Example")
    print("-" * 40)
    
    try:
        # Try to create evolutionary entry with invalid biofield
        failed_entry_id = await memory_system.create_evolutionary_entry(
            content={"test": "invalid_biofield"},
            core_principles=["test_principle"],
            biofield_metrics=invalid_biofield  # This will fail
        )
        print(f"❌ This should have failed!")
        
    except Exception as e:
        print(f"✅ Correctly rejected invalid biofield: {e}")
    
    print("\n🎉 AMA Memory System Demonstration Complete!")
    print("=" * 60)

# Example of using the FastAPI endpoints
async def demonstrate_api_endpoints():
    """Demonstrate how to use the FastAPI endpoints"""
    
    print("\n🌐 FastAPI Endpoints Demonstration")
    print("=" * 60)
    
    import aiohttp
    
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        
        # 1. Health check
        print("\n🔍 Health Check")
        print("-" * 40)
        
        async with session.get(f"{base_url}/health") as response:
            if response.status == 200:
                health_data = await response.json()
                print(f"✅ Health check passed: {health_data['status']}")
            else:
                print(f"❌ Health check failed: {response.status}")
        
        # 2. Biofield validation
        print("\n🔬 Biofield Validation API")
        print("-" * 40)
        
        biofield_data = {
            "hrv_ms": 95.0,
            "breath_pattern": [4, 6, 8],
            "coherence_score": 0.85
        }
        
        async with session.post(f"{base_url}/ama-memory/validate-biofield", 
                              json=biofield_data) as response:
            if response.status == 200:
                validation_data = await response.json()
                print(f"✅ Biofield validation: {validation_data['success']}")
            else:
                print(f"❌ Biofield validation failed: {response.status}")
        
        # 3. Create reactive entry
        print("\n⚡ Create Reactive Entry API")
        print("-" * 40)
        
        reactive_data = {
            "content": {
                "event_type": "api_demo",
                "timestamp": datetime.utcnow().isoformat()
            },
            "priority": 7,
            "biofield_metrics": biofield_data
        }
        
        async with session.post(f"{base_url}/ama-memory/reactive/create", 
                              json=reactive_data) as response:
            if response.status == 200:
                result = await response.json()
                print(f"✅ Reactive entry created: {result['entry_id']}")
            else:
                print(f"❌ Reactive entry creation failed: {response.status}")
        
        # 4. System status
        print("\n📊 System Status API")
        print("-" * 40)
        
        async with session.get(f"{base_url}/ama-memory/status") as response:
            if response.status == 200:
                status_data = await response.json()
                print(f"✅ System status: {status_data['overall_status']}")
                print(f"   Active layers: {len([l for l in status_data['layers'].values() if l.get('active')])}")
            else:
                print(f"❌ System status failed: {response.status}")

# Main execution
if __name__ == "__main__":
    print("🚀 Starting AMA Memory System Examples")
    
    # Run the memory system demonstration
    asyncio.run(demonstrate_ama_memory_system())
    
    # Run the API endpoints demonstration (if server is running)
    print("\n" + "=" * 80)
    print("Note: API endpoints demonstration requires the FastAPI server to be running")
    print("Start the server with: python main_fastapi.py")
    print("Then uncomment the following line to run API examples:")
    # asyncio.run(demonstrate_api_endpoints())
    
    print("\n📚 Example completed successfully!")
    print("Check the memory_operations.jsonl file for detailed operation logs.") 