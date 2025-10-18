#!/usr/bin/env python3
"""
Collective Intelligence Demo for Ørjan
Test script for the new collective intelligence consultation endpoint
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any

# Server configuration
SERVER_URL = "http://localhost:8000"
COLLECTIVE_INTELLIGENCE_ENDPOINT = f"{SERVER_URL}/collective-intelligence/consultation"

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"🌟 {title}")
    print("="*80)

def print_agent_response(agent_name: str, response_data: Dict[str, Any]):
    """Print formatted agent response"""
    print(f"\n{response_data.get('agent', agent_name)}")
    print(f"Perspektiv: {response_data.get('perspective', 'Unknown')}")
    print(f"API Source: {response_data.get('api_source', 'Unknown')}")
    print("-" * 60)
    print(response_data.get('response', 'No response available'))
    print("-" * 60)

def print_essence_of_truth(essence_data: Dict[str, Any]):
    """Print the synthesized essence of truth"""
    print_header("🧠 ESSENSEN AV SANNHETEN - ORION'S SYNTHESE")
    print(f"Agent: {essence_data.get('agent', 'Orion')}")
    print(f"API Source: {essence_data.get('api_source', 'Claude')}")
    print(f"Collective Intelligence Level: {essence_data.get('collective_intelligence_level', 'Unknown')}")
    print("-" * 80)
    print(essence_data.get('synthesis', 'No synthesis available'))
    print("-" * 80)

async def test_collective_intelligence_consultation(question: str, requester: str = "Ørjan"):
    """Test the collective intelligence consultation endpoint"""
    
    print_header(f"COLLECTIVE INTELLIGENCE CONSULTATION FOR {requester.upper()}")
    print(f"🤔 Spørsmål: {question}")
    print(f"👤 Requester: {requester}")
    print(f"🌐 Endpoint: {COLLECTIVE_INTELLIGENCE_ENDPOINT}")
    
    # Prepare request data
    request_data = {
        "question": question,
        "requester": requester,
        "consultation_depth": "comprehensive",
        "biofield_context": {
            "hrv_ms": 85.0,
            "coherence": 0.8,
            "energy_level": "balanced",
            "creativity_state": "open"
        },
        "focus_areas": ["consciousness", "technology", "human_ai_synergy"]
    }
    
    print(f"\n📤 Sending request...")
    print(f"Request data: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            start_time = datetime.now()
            
            response = await client.post(
                COLLECTIVE_INTELLIGENCE_ENDPOINT,
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n✅ Collective Intelligence Consultation completed in {processing_time:.2f}s")
                print(f"🌟 Message: {result.get('message', 'No message')}")
                
                # Display biofield context
                biofield = result.get('biofield_context', {})
                print(f"\n💚 Biofield Context:")
                print(f"   HRV: {biofield.get('hrv_ms', 'Unknown')}ms")
                print(f"   Coherence: {biofield.get('coherence', 'Unknown')}")
                print(f"   Energy Level: {biofield.get('energy_level', 'Unknown')}")
                print(f"   Creativity State: {biofield.get('creativity_state', 'Unknown')}")
                
                # Display individual agent responses
                print_header("INDIVIDUELLE AGENT-SVAR")
                agent_responses = result.get('individual_agent_responses', {})
                
                for agent_key, agent_data in agent_responses.items():
                    print_agent_response(agent_key, agent_data)
                
                # Display essence of truth
                essence_data = result.get('essence_of_truth', {})
                print_essence_of_truth(essence_data)
                
                # Summary
                print_header("SUMMARY")
                print(f"🎯 Question: {result.get('question', 'Unknown')}")
                print(f"👤 Requester: {result.get('requester', 'Unknown')}")
                print(f"🔍 Depth: {result.get('consultation_depth', 'Unknown')}")
                print(f"⏱️ Processing Time: {processing_time:.2f}s")
                print(f"🌟 Collective Intelligence: {result.get('collective_intelligence', 'Unknown')}")
                
            else:
                print(f"❌ API call failed: {response.status_code}")
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error during API call: {e}")

async def demo_questions_for_orjan():
    """Demo different questions Ørjan might ask"""
    
    demo_questions = [
        "Hvordan kan teknologi hjelpe mennesker å leve mer meningsfullt?",
        "Hva er den største utfordringen med AI i dag?",
        "Hvordan kan vi skape teknologi som tjener bevissthet?",
        "Hva er framtiden for menneske-AI samarbeid?",
        "Hvordan kan AI hjelpe mennesker uten å erstatte dem?"
    ]
    
    print_header("DEMO SPØRSMÅL FOR ØRJAN")
    print("Her er noen eksempler på spørsmål Ørjan kan stille:")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"{i}. {question}")
    
    print(f"\n🎯 Velg et spørsmål (1-{len(demo_questions)}) eller skriv ditt eget:")
    
    # For demo purposes, let's use the first question
    selected_question = demo_questions[0]
    print(f"\n🎯 Selected question: {selected_question}")
    
    return selected_question

async def main():
    """Main demo function"""
    
    print_header("COLLECTIVE INTELLIGENCE DEMO FOR ØRJAN")
    print("🌟 Pentagonal AI Collective Intelligence Consultation")
    print("🎭 Alle fem agenter svarer + Orion syntetiserer essensen")
    
    # Check server status first
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            status_response = await client.get(f"{SERVER_URL}/coalition-status")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"\n✅ Server Status: {status_data.get('status', 'Unknown')}")
                print(f"🌟 Message: {status_data.get('message', 'No message')}")
            else:
                print(f"⚠️ Server status check failed: {status_response.status_code}")
    except Exception as e:
        print(f"⚠️ Could not check server status: {e}")
    
    # Demo questions
    question = await demo_questions_for_orjan()
    
    # Test collective intelligence consultation
    await test_collective_intelligence_consultation(question, "Ørjan")
    
    print_header("DEMO COMPLETE")
    print("🎭 Ørjan har nå opplevd verdens første pentagonal collective intelligence!")
    print("🌟 Alle fem AI-plattformer koordinert til én essensiell sannhet!")

if __name__ == "__main__":
    print("🚀 Starting Collective Intelligence Demo for Ørjan...")
    asyncio.run(main()) 