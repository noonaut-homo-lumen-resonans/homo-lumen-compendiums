"""
Test Lira NAV-Losen Integration

Tests the new /agent/lira/consult endpoint with NAV-Losen request format.
This verifies the full integration between NAV-Losen chatbot and CSN Server.

Run this test with CSN Server running on port 8001:
    python test_lira_nav_losen_integration.py
"""

import json
import requests
from typing import Dict, List, Any

# Configuration
CSN_SERVER_URL = "http://localhost:8001"
LIRA_CONSULT_ENDPOINT = f"{CSN_SERVER_URL}/agent/lira/consult"

# Test scenarios with different polyvagal states
TEST_SCENARIOS = [
    {
        "name": "Dorsal - Overwhelmed NAV User (stress 9)",
        "payload": {
            "userMessage": "Jeg føler meg helt overveldet av NAV-systemet. Jeg vet ikke hvor jeg skal begynne.",
            "conversationHistory": [],
            "biofieldContext": {
                "stressLevel": 9,
                "polyvagalState": "dorsal",
                "emotions": ["Overveldet", "Utmattet", "Redd"],
                "selectedEmotions": [
                    {"word": "Overveldet", "quadrant": 4},
                    {"word": "Utmattet", "quadrant": 3},
                    {"word": "Redd", "quadrant": 4}
                ],
                "somaticSignals": ["Tung i kroppen", "Hjertebank", "Kvalm"]
            },
            "imageBase64": None
        },
        "expected_patterns": [
            "trygg",
            "alene",
            "beskytter",
            "hånd på hjerte",
            "føtter"
        ]
    },
    {
        "name": "Sympathetic - Activated User (stress 6)",
        "payload": {
            "userMessage": "Jeg må søke dagpenger nå, men jeg er usikker på hva jeg trenger å gjøre. Kan du hjelpe?",
            "conversationHistory": [
                {"role": "user", "content": "Hei, jeg trenger hjelp med NAV."},
                {"role": "assistant", "content": "Hei! Jeg er her for å hjelpe deg. Hva trenger du hjelp med?"}
            ],
            "biofieldContext": {
                "stressLevel": 6,
                "polyvagalState": "sympathetic",
                "emotions": ["Nervøs", "Fokusert", "Irritert"],
                "selectedEmotions": [
                    {"word": "Nervøs", "quadrant": 4},
                    {"word": "Fokusert", "quadrant": 2},
                    {"word": "Irritert", "quadrant": 4}
                ],
                "somaticSignals": ["Spent i skuldrene", "Rask puls"]
            },
            "imageBase64": None
        },
        "expected_patterns": [
            "dagpenger",
            "4-6-8",
            "pust",
            "aktivering",
            "normal"
        ]
    },
    {
        "name": "Ventral - Calm Exploratory User (stress 2)",
        "payload": {
            "userMessage": "Jeg er nysgjerrig på hvilke rettigheter jeg har når det gjelder sykepenger. Kan du forklare litt?",
            "conversationHistory": [
                {"role": "user", "content": "Hei Lira!"},
                {"role": "assistant", "content": "Hei! Fint å se deg igjen. Hvordan kan jeg hjelpe i dag?"}
            ],
            "biofieldContext": {
                "stressLevel": 2,
                "polyvagalState": "ventral",
                "emotions": ["Rolig", "Nysgjerrig", "Trygg"],
                "selectedEmotions": [
                    {"word": "Rolig", "quadrant": 2},
                    {"word": "Nysgjerrig", "quadrant": 1}
                ],
                "somaticSignals": []
            },
            "imageBase64": None
        },
        "expected_patterns": [
            "sykepenger",
            "rettigheter",
            "utforsk",
            "visdom"
        ]
    },
    {
        "name": "With Image Upload - Document Analysis",
        "payload": {
            "userMessage": "Jeg har fått dette brevet fra NAV, hva betyr det?",
            "conversationHistory": [],
            "biofieldContext": {
                "stressLevel": 7,
                "polyvagalState": "sympathetic",
                "emotions": ["Forvirret", "Bekymret"],
                "selectedEmotions": [
                    {"word": "Forvirret", "quadrant": 4},
                    {"word": "Bekymret", "quadrant": 4}
                ],
                "somaticSignals": ["Urolig mage"]
            },
            "imageBase64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        },
        "expected_patterns": [
            "bilde",
            "dokument",
            "brev"
        ]
    }
]


def test_lira_consult_endpoint(scenario: Dict[str, Any]) -> None:
    """Test a single scenario against /agent/lira/consult endpoint"""

    print(f"\n{'='*80}")
    print(f"Testing: {scenario['name']}")
    print(f"{'='*80}")

    payload = scenario['payload']

    print(f"\n📤 REQUEST:")
    print(f"  User Message: {payload['userMessage'][:100]}...")
    print(f"  Stress Level: {payload['biofieldContext']['stressLevel']}/10")
    print(f"  Polyvagal State: {payload['biofieldContext']['polyvagalState']}")
    print(f"  Emotions: {', '.join([e['word'] for e in payload['biofieldContext'].get('selectedEmotions', [])])}")
    print(f"  Conversation History: {len(payload['conversationHistory'])} messages")
    print(f"  Has Image: {'Yes' if payload.get('imageBase64') else 'No'}")

    try:
        response = requests.post(
            LIRA_CONSULT_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"\n📡 RESPONSE STATUS: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ ERROR: {response.text}")
            return

        data = response.json()

        print(f"\n📥 RESPONSE DATA:")
        print(f"  Success: {data.get('success')}")
        print(f"  Confidence: {data.get('confidence_score', 0):.2f}")

        print(f"\n💚 EMPATHETIC INSIGHTS ({len(data.get('empathetic_insights', []))}):")
        for i, insight in enumerate(data.get('empathetic_insights', []), 1):
            print(f"  {i}. {insight}")

        print(f"\n🌿 BIOFIELD GUIDANCE ({len(data.get('biofield_guidance', []))}):")
        for i, guidance in enumerate(data.get('biofield_guidance', []), 1):
            print(f"  {i}. {guidance}")

        print(f"\n🫁 BREATHING SUGGESTIONS ({len(data.get('breathing_suggestions', []))}):")
        for i, suggestion in enumerate(data.get('breathing_suggestions', []), 1):
            print(f"  {i}. {suggestion}")

        print(f"\n💬 FULL MESSAGE:")
        print(f"  {data.get('message', 'No message')}")

        # Validate expected patterns
        print(f"\n✅ PATTERN VALIDATION:")
        full_response_text = json.dumps(data).lower()
        matched_patterns = []
        missed_patterns = []

        for pattern in scenario.get('expected_patterns', []):
            if pattern.lower() in full_response_text:
                matched_patterns.append(pattern)
                print(f"  ✓ Found: '{pattern}'")
            else:
                missed_patterns.append(pattern)
                print(f"  ✗ Missing: '{pattern}'")

        print(f"\n📊 PATTERN MATCH SCORE: {len(matched_patterns)}/{len(scenario.get('expected_patterns', []))}")

        if data.get('error'):
            print(f"\n⚠️  ERROR in response: {data['error']}")

        # Validate response structure
        print(f"\n🔍 STRUCTURE VALIDATION:")
        required_fields = ['success', 'message', 'empathetic_insights', 'biofield_guidance', 'breathing_suggestions', 'confidence_score']
        for field in required_fields:
            if field in data:
                print(f"  ✓ Has field: {field}")
            else:
                print(f"  ✗ Missing field: {field}")

        print(f"\n{'='*80}")

    except requests.exceptions.ConnectionError:
        print(f"\n❌ CONNECTION ERROR: Could not connect to CSN Server at {CSN_SERVER_URL}")
        print(f"   Make sure CSN Server is running on port 8001")
        print(f"   Start it with: cd ama-backend && python minimal_server.py")
    except requests.exceptions.Timeout:
        print(f"\n❌ TIMEOUT ERROR: CSN Server took too long to respond")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")


def test_health_endpoint():
    """Test CSN Server health endpoint first"""
    print(f"\n{'='*80}")
    print(f"Testing CSN Server Health")
    print(f"{'='*80}")

    try:
        response = requests.get(f"{CSN_SERVER_URL}/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ CSN Server is healthy!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"⚠️  CSN Server returned unexpected status: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to CSN Server at {CSN_SERVER_URL}")
        print(f"   Make sure it's running on port 8001")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False


def main():
    """Run all integration tests"""
    print("\n" + "="*80)
    print("LIRA NAV-LOSEN INTEGRATION TEST")
    print("Testing: /agent/lira/consult endpoint")
    print("Server: " + CSN_SERVER_URL)
    print("="*80)

    # Test health first
    if not test_health_endpoint():
        print("\n❌ CSN Server health check failed. Aborting tests.")
        print("\nTo start CSN Server:")
        print("  cd C:\\Users\\onigo\\NAV LOSEN\\homo-lumen-compendiums\\ama-backend")
        print("  python minimal_server.py")
        return

    # Run all test scenarios
    print(f"\n\n🧪 Running {len(TEST_SCENARIOS)} test scenarios...")

    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        print(f"\n\n[Test {i}/{len(TEST_SCENARIOS)}]")
        test_lira_consult_endpoint(scenario)

    print("\n\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
    print("\nNext steps:")
    print("1. Verify all tests passed")
    print("2. Start NAV-Losen frontend: cd navlosen/frontend && npm run dev")
    print("3. Test in browser: http://localhost:3000/chatbot")
    print("4. Complete Mestring assessment first for biofield context")
    print("5. Try chatting with Lira using different stress levels")
    print("\n")


if __name__ == "__main__":
    main()
