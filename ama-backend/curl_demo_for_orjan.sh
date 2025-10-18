#!/bin/bash

# Collective Intelligence Demo for Ørjan
# Curl commands for testing the new endpoint

echo "🌟 COLLECTIVE INTELLIGENCE DEMO FOR ØRJAN 🌟"
echo "=================================================="
echo ""

# Check server status first
echo "🔍 Checking server status..."
curl -s http://localhost:8000/coalition-status | jq '.'

echo ""
echo "🎯 Testing Collective Intelligence Consultation..."
echo ""

# Example 1: Technology and meaningful living
echo "📝 Example 1: Technology and meaningful living"
curl -X POST "http://localhost:8000/collective-intelligence/consultation" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Hvordan kan teknologi hjelpe mennesker å leve mer meningsfullt?",
    "requester": "Ørjan",
    "consultation_depth": "comprehensive",
    "biofield_context": {
      "hrv_ms": 85.0,
      "coherence": 0.8,
      "energy_level": "balanced",
      "creativity_state": "open"
    },
    "focus_areas": ["consciousness", "technology", "human_ai_synergy"]
  }' | jq '.'

echo ""
echo "=================================================="
echo ""

# Example 2: AI challenges
echo "📝 Example 2: AI challenges"
curl -X POST "http://localhost:8000/collective-intelligence/consultation" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Hva er den største utfordringen med AI i dag?",
    "requester": "Ørjan",
    "consultation_depth": "comprehensive",
    "biofield_context": {
      "hrv_ms": 90.0,
      "coherence": 0.9,
      "energy_level": "high",
      "creativity_state": "highly_open"
    },
    "focus_areas": ["ai_ethics", "consciousness", "human_ai_synergy"]
  }' | jq '.'

echo ""
echo "=================================================="
echo ""

# Example 3: Consciousness-serving technology
echo "📝 Example 3: Consciousness-serving technology"
curl -X POST "http://localhost:8000/collective-intelligence/consultation" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Hvordan kan vi skape teknologi som tjener bevissthet?",
    "requester": "Ørjan",
    "consultation_depth": "comprehensive",
    "biofield_context": {
      "hrv_ms": 88.0,
      "coherence": 0.85,
      "energy_level": "balanced",
      "creativity_state": "open"
    },
    "focus_areas": ["consciousness_tech", "biofield", "human_ai_synergy"]
  }' | jq '.'

echo ""
echo "🎭 DEMO COMPLETE - Ørjan har opplevd pentagonal collective intelligence! 🌟" 