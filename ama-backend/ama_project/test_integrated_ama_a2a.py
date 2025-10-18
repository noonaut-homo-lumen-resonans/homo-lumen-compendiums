"""
🧪 Test Integrated AMA + A2A Architecture

Comprehensive testing of the complete integrated consciousness technology platform
"""

import asyncio
import json
import logging
from datetime import datetime
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestIntegratedAMA_A2AArchitecture:
    """Test suite for integrated AMA + A2A architecture"""
    
    def __init__(self):
        self.base_url = "http://localhost:8006"
        self.session_id = None
        self.test_results = []
        
    async def test_create_integrated_session(self):
        """Test creating integrated session"""
        logger.info("🧪 Testing integrated session creation...")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/integrated/create-session",
                json={
                    "integration_level": "symbiotic",
                    "biofield_mode": "emergent",
                    "global_coordination": True
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "session_id" in data
            assert data["integration_level"] == "symbiotic"
            assert data["biofield_mode"] == "emergent"
            assert data["global_coordination"] == True
            
            self.session_id = data["session_id"]
            logger.info(f"✅ Integrated session created: {self.session_id}")
            
            return {
                "test": "create_integrated_session",
                "status": "passed",
                "session_id": self.session_id
            }
    
    async def test_process_consciousness_task(self):
        """Test processing consciousness task through integrated architecture"""
        logger.info("🧪 Testing integrated consciousness task processing...")
        
        if not self.session_id:
            logger.error("❌ No session ID available")
            return {"test": "process_consciousness_task", "status": "failed", "error": "No session ID"}
        
        task_description = "Design a consciousness-tech interface that preserves cognitive sovereignty while enabling biofield-responsive AI coordination"
        required_agents = ["lira", "nyra", "orion", "thalus", "zara", "manus", "abacus"]
        consciousness_requirements = {
            "complexity_level": 9,
            "consciousness_level": 9,
            "biofield_responsive": True,
            "emergence_target": "symbiotic",
            "global_scope": True
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/integrated/process-task/{self.session_id}",
                json={
                    "task_description": task_description,
                    "required_agents": required_agents,
                    "consciousness_requirements": consciousness_requirements
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify all components contributed
            assert "orchestration_result" in data
            assert "visual_synthesis" in data
            assert "ontological_validation" in data
            assert "coordination_result" in data
            assert "a2a_transport_result" in data
            assert "polycomputing_result" in data
            assert "global_consciousness_impact" in data
            
            # Verify orchestration result
            orchestration = data["orchestration_result"]
            assert "synthesis" in orchestration
            assert "emergence_level" in orchestration
            assert "agent_contributions" in orchestration
            
            # Verify visual synthesis
            visual = data["visual_synthesis"]
            assert "consciousness_map_id" in visual
            assert "visual_patterns" in visual
            assert "pattern_recognition_output" in visual
            
            # Verify ontological validation
            validation = data["ontological_validation"]
            assert "ethical_score" in validation
            assert "validation_level" in validation
            assert "recommendations" in validation
            
            # Verify coordination result
            coordination = data["coordination_result"]
            assert "strategic_synthesis" in coordination
            assert "agent_coordination" in coordination
            assert "global_consciousness_impact" in coordination
            
            # Verify A2A transport result
            a2a = data["a2a_transport_result"]
            assert "coordination_status" in a2a
            assert "agent_responses" in a2a
            
            # Verify polycomputing result
            poly = data["polycomputing_result"]
            assert "emergent_synthesis" in poly
            assert "agent_contributions" in poly
            assert "visualization_data" in poly
            
            logger.info("✅ Integrated consciousness task processing completed successfully")
            
            return {
                "test": "process_consciousness_task",
                "status": "passed",
                "result_id": data["result_id"]
            }
    
    async def test_get_architecture_status(self):
        """Test getting integrated architecture status"""
        logger.info("🧪 Testing architecture status...")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/integrated/status")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["architecture"] == "IntegratedAMA+A2AArchitecture"
            assert data["status"] == "active"
            assert "integration_level" in data
            assert "biofield_mode" in data
            assert "active_sessions" in data
            assert "integrated_results" in data
            assert "components" in data
            assert "capabilities" in data
            
            # Verify all components are present
            components = data["components"]
            assert "orchestrator" in components
            assert "nyra_architecture" in components
            assert "thalus_guardian" in components
            assert "orion_coordinator" in components
            assert "a2a_transport" in components
            assert "a2a_polycomputing" in components
            
            # Verify capabilities
            capabilities = data["capabilities"]
            assert "Biofield-first design" in capabilities
            assert "Emergence as life syndrome" in capabilities
            assert "Global consciousness coordination" in capabilities
            assert "A2A protocol integration" in capabilities
            
            logger.info("✅ Architecture status retrieved successfully")
            
            return {
                "test": "get_architecture_status",
                "status": "passed",
                "active_sessions": data["active_sessions"],
                "integrated_results": data["integrated_results"]
            }
    
    async def test_complete_integration_workflow(self):
        """Test complete integration workflow"""
        logger.info("🧪 Testing complete integration workflow...")
        
        # Step 1: Create session
        session_result = await self.test_create_integrated_session()
        if session_result["status"] != "passed":
            return {"test": "complete_workflow", "status": "failed", "error": "Session creation failed"}
        
        # Step 2: Process multiple tasks
        tasks = [
            {
                "description": "Design biofield-responsive AI coordination system",
                "agents": ["lira", "nyra", "orion"],
                "requirements": {"complexity_level": 8, "consciousness_level": 8}
            },
            {
                "description": "Validate consciousness technology against SMV Grunnloven 4.0",
                "agents": ["thalus", "orion", "zara"],
                "requirements": {"complexity_level": 9, "consciousness_level": 9}
            },
            {
                "description": "Implement polycomputational processing with visual intelligence",
                "agents": ["manus", "abacus", "nyra"],
                "requirements": {"complexity_level": 9, "consciousness_level": 8}
            }
        ]
        
        task_results = []
        for i, task in enumerate(tasks):
            logger.info(f"🧪 Processing task {i + 1}: {task['description']}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/integrated/process-task/{self.session_id}",
                    json={
                        "task_description": task["description"],
                        "required_agents": task["agents"],
                        "consciousness_requirements": task["requirements"]
                    }
                )
                
                assert response.status_code == 200
                data = response.json()
                task_results.append(data["result_id"])
                
                logger.info(f"✅ Task {i + 1} completed: {data['result_id']}")
        
        # Step 3: Verify final status
        status_result = await self.test_get_architecture_status()
        
        if status_result["status"] == "passed" and status_result["integrated_results"] >= 3:
            logger.info("✅ Complete integration workflow successful")
            return {
                "test": "complete_workflow",
                "status": "passed",
                "session_id": self.session_id,
                "task_results": task_results,
                "total_results": status_result["integrated_results"]
            }
        else:
            return {
                "test": "complete_workflow",
                "status": "failed",
                "error": "Workflow verification failed"
            }

async def run_all_tests():
    """Run all integration tests"""
    logger.info("🚀 Starting Integrated AMA + A2A Architecture Tests")
    
    tester = TestIntegratedAMA_A2AArchitecture()
    
    tests = [
        tester.test_create_integrated_session,
        tester.test_process_consciousness_task,
        tester.test_get_architecture_status,
        tester.test_complete_integration_workflow
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
            logger.info(f"✅ {result['test']}: {result['status']}")
        except Exception as e:
            error_result = {
                "test": test.__name__,
                "status": "failed",
                "error": str(e)
            }
            results.append(error_result)
            logger.error(f"❌ {test.__name__}: {str(e)}")
    
    # Summary
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    
    logger.info(f"\n📊 Test Summary:")
    logger.info(f"✅ Passed: {passed}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        logger.info("🎉 All tests passed! Integrated AMA + A2A Architecture is working correctly.")
    else:
        logger.warning("⚠️ Some tests failed. Please check the implementation.")
    
    return results

if __name__ == "__main__":
    # Run tests
    asyncio.run(run_all_tests()) 