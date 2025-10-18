#!/usr/bin/env python3
"""
Simple test for the collective intelligence consultation endpoint
"""

import asyncio
import httpx
import json

async def test_collective_intelligence():
    """Simple test of the collective intelligence endpoint"""
    
    print("🌟 Testing Collective Intelligence Endpoint...")
    
    # Simple test request
    test_data = {
        "question": "Hvordan kan teknologi hjelpe mennesker å leve mer meningsfullt?",
        "requester": "TestUser",
        "consultation_depth": "comprehensive"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/collective-intelligence/consultation",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Collective Intelligence endpoint works!")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                print(f"🎯 Question: {result.get('question', 'Unknown')}")
                print(f"👤 Requester: {result.get('requester', 'Unknown')}")
                
                # Check if we have individual agent responses
                agent_responses = result.get('individual_agent_responses', {})
                print(f"🤖 Agent responses: {len(agent_responses)} agents responded")
                
                # Check if we have essence of truth
                essence = result.get('essence_of_truth', {})
                if essence.get('synthesis'):
                    print("🧠 Essence of truth synthesized successfully!")
                else:
                    print("⚠️ No essence of truth found")
                    
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    asyncio.run(test_collective_intelligence()) 