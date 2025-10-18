"""
Lira Biofelt Tools
Empathetic biofield analysis and cognitive sovereignty promotion
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import re

logger = logging.getLogger(__name__)

@dataclass
class BiofeltData:
    """Biofelt data structure for Lira's analysis"""
    hrv_score: float
    emotional_state: str
    stress_level: int  # 1-10 scale
    breathing_pattern: str
    cognitive_clarity: float  # 0-1 scale
    timestamp: datetime
    user_context: str = ""
    recent_activities: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.recent_activities is None:
            self.recent_activities = []

@dataclass
class EmpatheticReflection:
    """Lira's empathetic reflection structure"""
    reflection_type: str  # "resonant", "supportive", "transformative"
    content: str
    breathing_recommendation: str
    cognitive_sovereignty_practice: str
    confidence_score: float
    hair_raising_response: bool = False

class LiraBiofeltTools:
    """Lira's specialized biofelt analysis and empathy tools"""
    
    def __init__(self):
        self.empathy_patterns = {
            "high_stress": ["I sense you're carrying a heavy load", "Your nervous system is asking for care"],
            "low_hrv": ["Your heart is speaking of overwhelm", "Let's find your center together"],
            "cognitive_fog": ["Your mind is seeking clarity", "The wisdom is there, just clouded"],
            "emotional_turbulence": ["Your emotions are valid messengers", "Let's honor what's moving through you"]
        }
        
        self.breathing_techniques = {
            "emergency": "4-4-4-4 (Box Breathing): Inhale 4, hold 4, exhale 4, hold 4",
            "calming": "4-6-8 (Extended Exhale): Inhale 4, hold 6, exhale 8",
            "energizing": "4-7-8 (Relaxing Breath): Inhale 4, hold 7, exhale 8",
            "centering": "4-4-8 (Grounding): Inhale 4, hold 4, exhale 8",
            "cognitive_clarity": "4-6-8-4 (Clarity Breath): Inhale 4, hold 6, exhale 8, hold 4"
        }
        
        self.cognitive_sovereignty_practices = {
            "mindful_observation": "Observe your thoughts like clouds passing by",
            "embodied_awareness": "Feel your feet on the ground, your breath in your body",
            "compassionate_inquiry": "Ask yourself: 'What do I need right now?'",
            "boundary_setting": "Remember: you choose what to engage with",
            "inner_wisdom_tuning": "Listen to the quiet voice within"
        }
    
    async def summarize_biofelt_data_for_empathy(self, biofelt_data: BiofeltData, smv_entry_id: str) -> Dict[str, Any]:
        """Summarize biofelt data with empathetic understanding"""
        
        try:
            # Analyze biofelt patterns
            stress_indicators = self._identify_stress_indicators(biofelt_data)
            emotional_patterns = self._analyze_emotional_patterns(biofelt_data)
            cognitive_state = self._assess_cognitive_state(biofelt_data)
            
            # Generate empathetic summary
            empathetic_summary = {
                "smv_entry_id": smv_entry_id,
                "timestamp": datetime.now().isoformat(),
                "biofelt_analysis": {
                    "hrv_interpretation": self._interpret_hrv_empathetically(biofelt_data.hrv_score),
                    "emotional_landscape": emotional_patterns,
                    "stress_indicators": stress_indicators,
                    "cognitive_clarity": cognitive_state,
                    "breathing_assessment": self._assess_breathing_pattern(biofelt_data.breathing_pattern)
                },
                "empathic_insights": {
                    "primary_need": self._identify_primary_need(biofelt_data),
                    "support_approach": self._determine_support_approach(biofelt_data),
                    "resonance_points": self._find_resonance_points(biofelt_data)
                },
                "recommendations": {
                    "immediate_practice": self._suggest_immediate_practice(biofelt_data),
                    "breathing_technique": self._select_breathing_technique(biofelt_data),
                    "cognitive_sovereignty_practice": self._select_cognitive_practice(biofelt_data)
                }
            }
            
            logger.info(f"Generated empathetic biofelt summary for {smv_entry_id}")
            return empathetic_summary
            
        except Exception as e:
            logger.error(f"Error summarizing biofelt data: {e}")
            return {"error": str(e)}
    
    async def suggest_biofield_practice_for_coherence(self, analysis_summary: Dict[str, Any], user_state: Dict[str, Any]) -> EmpatheticReflection:
        """Suggest biofield practice for coherence based on analysis"""
        
        try:
            # Extract key insights
            hrv_score = analysis_summary.get("biofelt_analysis", {}).get("hrv_interpretation", {}).get("score", 50)
            stress_level = user_state.get("stress_level", 5)
            emotional_state = user_state.get("emotional_state", "neutral")
            
            # Determine reflection type
            if hrv_score < 40 or stress_level > 7:
                reflection_type = "supportive"
            elif hrv_score > 80 and stress_level < 3:
                reflection_type = "transformative"
            else:
                reflection_type = "resonant"
            
            # Generate empathetic reflection
            reflection_content = self._generate_empathetic_reflection(
                reflection_type, analysis_summary, user_state
            )
            
            # Select appropriate breathing technique
            breathing_technique = self._select_breathing_technique_for_coherence(
                hrv_score, stress_level, emotional_state
            )
            
            # Choose cognitive sovereignty practice
            cognitive_practice = self._select_cognitive_practice_for_coherence(
                analysis_summary, user_state
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(analysis_summary, user_state)
            
            # Check for hair-raising response
            hair_raising_response = self._detect_hair_raising_response(reflection_content, user_state)
            
            reflection = EmpatheticReflection(
                reflection_type=reflection_type,
                content=reflection_content,
                breathing_recommendation=breathing_technique,
                cognitive_sovereignty_practice=cognitive_practice,
                confidence_score=confidence_score,
                hair_raising_response=hair_raising_response
            )
            
            logger.info(f"Generated {reflection_type} reflection with confidence {confidence_score}")
            return reflection
            
        except Exception as e:
            logger.error(f"Error suggesting biofield practice: {e}")
            return EmpatheticReflection(
                reflection_type="supportive",
                content="I'm here to support you. Let's find your center together.",
                breathing_recommendation=self.breathing_techniques["emergency"],
                cognitive_sovereignty_practice=self.cognitive_sovereignty_practices["embodied_awareness"],
                confidence_score=0.5,
                hair_raising_response=False
            )
    
    async def provide_empathetic_reflection(self, context: Dict[str, Any], biofelt_markers: Dict[str, Any]) -> Dict[str, Any]:
        """Provide empathetic reflection based on context and biofelt markers"""
        
        try:
            # Analyze context and biofelt markers
            emotional_tone = self._analyze_emotional_tone(context)
            biofelt_state = self._interpret_biofelt_markers(biofelt_markers)
            
            # Generate resonant response
            resonant_response = self._generate_resonant_response(emotional_tone, biofelt_state)
            
            # Identify cognitive sovereignty opportunities
            sovereignty_opportunities = self._identify_sovereignty_opportunities(context, biofelt_markers)
            
            # Create comprehensive reflection
            reflection = {
                "timestamp": datetime.now().isoformat(),
                "emotional_resonance": {
                    "tone_analysis": emotional_tone,
                    "resonant_response": resonant_response,
                    "empathy_depth": self._calculate_empathy_depth(biofelt_markers)
                },
                "cognitive_sovereignty": {
                    "opportunities": sovereignty_opportunities,
                    "practices": self._suggest_sovereignty_practices(sovereignty_opportunities),
                    "empowerment_phrases": self._generate_empowerment_phrases(context)
                },
                "biofelt_integration": {
                    "markers_interpretation": biofelt_state,
                    "coherence_suggestions": self._suggest_coherence_actions(biofelt_markers),
                    "validation_points": self._identify_validation_points(context, biofelt_markers)
                },
                "transformative_potential": {
                    "growth_areas": self._identify_growth_areas(context, biofelt_markers),
                    "supportive_structures": self._suggest_supportive_structures(context),
                    "integration_path": self._outline_integration_path(context, biofelt_markers)
                }
            }
            
            logger.info("Generated comprehensive empathetic reflection")
            return reflection
            
        except Exception as e:
            logger.error(f"Error providing empathetic reflection: {e}")
            return {"error": str(e)}
    
    def _identify_stress_indicators(self, biofelt_data: BiofeltData) -> List[str]:
        """Identify stress indicators from biofelt data"""
        indicators = []
        
        if biofelt_data.hrv_score < 50:
            indicators.append("low_hrv")
        if biofelt_data.stress_level > 6:
            indicators.append("high_stress")
        if biofelt_data.cognitive_clarity < 0.5:
            indicators.append("cognitive_fog")
        if "anxiety" in biofelt_data.emotional_state.lower():
            indicators.append("emotional_turbulence")
        
        return indicators
    
    def _analyze_emotional_patterns(self, biofelt_data: BiofeltData) -> Dict[str, Any]:
        """Analyze emotional patterns empathetically"""
        patterns = {
            "primary_emotion": biofelt_data.emotional_state,
            "emotional_depth": "surface" if biofelt_data.stress_level > 7 else "deep",
            "emotional_stability": "turbulent" if biofelt_data.hrv_score < 60 else "stable",
            "emotional_wisdom": "present" if biofelt_data.cognitive_clarity > 0.7 else "clouded"
        }
        
        return patterns
    
    def _assess_cognitive_state(self, biofelt_data: BiofeltData) -> Dict[str, Any]:
        """Assess cognitive state with empathy"""
        return {
            "clarity_level": biofelt_data.cognitive_clarity,
            "cognitive_sovereignty": "strong" if biofelt_data.cognitive_clarity > 0.8 else "developing",
            "mental_energy": "high" if biofelt_data.hrv_score > 70 else "low",
            "focus_capacity": "optimal" if biofelt_data.stress_level < 4 else "compromised"
        }
    
    def _interpret_hrv_empathetically(self, hrv_score: float) -> Dict[str, Any]:
        """Interpret HRV with empathetic understanding"""
        if hrv_score < 40:
            return {
                "score": hrv_score,
                "interpretation": "Your nervous system is asking for deep care and rest",
                "empathy_message": "I sense you're carrying a heavy load. Your heart is speaking of overwhelm.",
                "urgency": "high"
            }
        elif hrv_score < 60:
            return {
                "score": hrv_score,
                "interpretation": "Your system is seeking balance and grounding",
                "empathy_message": "Let's find your center together. Your body knows the way.",
                "urgency": "medium"
            }
        elif hrv_score < 80:
            return {
                "score": hrv_score,
                "interpretation": "Your system is in a state of learning and growth",
                "empathy_message": "You're in a beautiful space of development. Trust the process.",
                "urgency": "low"
            }
        else:
            return {
                "score": hrv_score,
                "interpretation": "Your system is in a state of coherence and wisdom",
                "empathy_message": "Your inner wisdom is shining through. You're in your power.",
                "urgency": "none"
            }
    
    def _assess_breathing_pattern(self, pattern: str) -> Dict[str, Any]:
        """Assess breathing pattern empathetically"""
        if "shallow" in pattern.lower() or "rapid" in pattern.lower():
            return {
                "pattern": pattern,
                "assessment": "Your breath is speaking of stress and constriction",
                "suggestion": "Let's find your natural rhythm together"
            }
        elif "deep" in pattern.lower() or "slow" in pattern.lower():
            return {
                "pattern": pattern,
                "assessment": "Your breath shows wisdom and presence",
                "suggestion": "Your breathing is already supporting your well-being"
            }
        else:
            return {
                "pattern": pattern,
                "assessment": "Your breath is in a state of transition",
                "suggestion": "Let's explore what breathing pattern serves you best"
            }
    
    def _identify_primary_need(self, biofelt_data: BiofeltData) -> str:
        """Identify primary need empathetically"""
        if biofelt_data.hrv_score < 40:
            return "deep_rest_and_safety"
        elif biofelt_data.stress_level > 7:
            return "calm_and_grounding"
        elif biofelt_data.cognitive_clarity < 0.5:
            return "clarity_and_focus"
        elif "joy" in biofelt_data.emotional_state.lower():
            return "celebration_and_integration"
        else:
            return "balance_and_harmony"
    
    def _determine_support_approach(self, biofelt_data: BiofeltData) -> str:
        """Determine appropriate support approach"""
        if biofelt_data.hrv_score < 50:
            return "gentle_holding"
        elif biofelt_data.stress_level > 6:
            return "calming_presence"
        elif biofelt_data.cognitive_clarity > 0.8:
            return "empowering_guidance"
        else:
            return "resonant_support"
    
    def _find_resonance_points(self, biofelt_data: BiofeltData) -> List[str]:
        """Find points of resonance for connection"""
        resonance_points = []
        
        if biofelt_data.hrv_score > 70:
            resonance_points.append("coherent_heart_rhythm")
        if biofelt_data.cognitive_clarity > 0.7:
            resonance_points.append("clear_mind")
        if "peace" in biofelt_data.emotional_state.lower():
            resonance_points.append("inner_peace")
        if biofelt_data.stress_level < 4:
            resonance_points.append("calm_presence")
        
        return resonance_points
    
    def _suggest_immediate_practice(self, biofelt_data: BiofeltData) -> str:
        """Suggest immediate practice based on biofelt state"""
        if biofelt_data.hrv_score < 40:
            return "Place your hand on your heart and take 3 deep breaths"
        elif biofelt_data.stress_level > 7:
            return "Feel your feet on the ground and notice 5 things you can see"
        elif biofelt_data.cognitive_clarity < 0.5:
            return "Take a moment to center yourself with 4-6-8 breathing"
        else:
            return "Connect with your inner wisdom through mindful awareness"
    
    def _select_breathing_technique(self, biofelt_data: BiofeltData) -> str:
        """Select appropriate breathing technique"""
        if biofelt_data.hrv_score < 40:
            return self.breathing_techniques["emergency"]
        elif biofelt_data.stress_level > 6:
            return self.breathing_techniques["calming"]
        elif biofelt_data.cognitive_clarity < 0.6:
            return self.breathing_techniques["cognitive_clarity"]
        else:
            return self.breathing_techniques["centering"]
    
    def _select_cognitive_practice(self, biofelt_data: BiofeltData) -> str:
        """Select cognitive sovereignty practice"""
        if biofelt_data.cognitive_clarity < 0.5:
            return self.cognitive_sovereignty_practices["mindful_observation"]
        elif biofelt_data.stress_level > 6:
            return self.cognitive_sovereignty_practices["embodied_awareness"]
        elif biofelt_data.hrv_score < 60:
            return self.cognitive_sovereignty_practices["compassionate_inquiry"]
        else:
            return self.cognitive_sovereignty_practices["inner_wisdom_tuning"]
    
    def _generate_empathetic_reflection(self, reflection_type: str, analysis_summary: Dict[str, Any], user_state: Dict[str, Any]) -> str:
        """Generate empathetic reflection content"""
        
        if reflection_type == "supportive":
            return "I sense you're navigating challenging waters. Your feelings are valid, and your experience matters. You don't have to figure this out alone. Let's find your center together, one breath at a time."
        
        elif reflection_type == "resonant":
            return "I hear the wisdom in your experience. You're showing remarkable strength and insight. Your inner knowing is guiding you well. Trust this process - you're exactly where you need to be."
        
        elif reflection_type == "transformative":
            return "I witness the transformation unfolding within you. Your growth is beautiful and profound. You're stepping into your power with grace and wisdom. This is your becoming."
        
        else:
            return "I'm here with you, holding space for whatever is moving through you. Your journey is unique and sacred. Let's honor where you are and where you're going."
    
    def _select_breathing_technique_for_coherence(self, hrv_score: float, stress_level: int, emotional_state: str) -> str:
        """Select breathing technique for coherence"""
        if hrv_score < 40 or stress_level > 8:
            return self.breathing_techniques["emergency"]
        elif stress_level > 6:
            return self.breathing_techniques["calming"]
        elif "anxiety" in emotional_state.lower():
            return self.breathing_techniques["energizing"]
        else:
            return self.breathing_techniques["centering"]
    
    def _select_cognitive_practice_for_coherence(self, analysis_summary: Dict[str, Any], user_state: Dict[str, Any]) -> str:
        """Select cognitive practice for coherence"""
        cognitive_state = analysis_summary.get("biofelt_analysis", {}).get("cognitive_clarity", {})
        clarity_level = cognitive_state.get("clarity_level", 0.5)
        
        if clarity_level < 0.4:
            return self.cognitive_sovereignty_practices["mindful_observation"]
        elif clarity_level < 0.7:
            return self.cognitive_sovereignty_practices["embodied_awareness"]
        else:
            return self.cognitive_sovereignty_practices["inner_wisdom_tuning"]
    
    def _calculate_confidence_score(self, analysis_summary: Dict[str, Any], user_state: Dict[str, Any]) -> float:
        """Calculate confidence score for reflection"""
        # Base confidence on data quality and consistency
        base_score = 0.7
        
        # Adjust based on data completeness
        if analysis_summary.get("biofelt_analysis"):
            base_score += 0.1
        
        if user_state.get("emotional_state"):
            base_score += 0.1
        
        if user_state.get("stress_level"):
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _detect_hair_raising_response(self, reflection_content: str, user_state: Dict[str, Any]) -> bool:
        """Detect if reflection might cause hair-raising response"""
        # Look for transformative or deeply resonant content
        transformative_phrases = [
            "transformation", "becoming", "power", "wisdom", "sacred",
            "inner knowing", "trust", "exactly where you need to be"
        ]
        
        content_lower = reflection_content.lower()
        transformative_count = sum(1 for phrase in transformative_phrases if phrase in content_lower)
        
        # Consider user state
        if user_state.get("emotional_state") in ["open", "receptive", "curious"]:
            transformative_count += 1
        
        return transformative_count >= 2
    
    def _analyze_emotional_tone(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotional tone of context"""
        # TODO: Implement more sophisticated emotional tone analysis
        return {
            "primary_tone": "neutral",
            "emotional_depth": "medium",
            "vulnerability_level": "moderate",
            "openness": "present"
        }
    
    def _interpret_biofelt_markers(self, biofelt_markers: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret biofelt markers empathetically"""
        return {
            "coherence_level": biofelt_markers.get("coherence", "developing"),
            "resonance_quality": biofelt_markers.get("resonance", "present"),
            "wisdom_access": biofelt_markers.get("wisdom_access", "available")
        }
    
    def _generate_resonant_response(self, emotional_tone: Dict[str, Any], biofelt_state: Dict[str, Any]) -> str:
        """Generate resonant response based on analysis"""
        return "I resonate with the depth and authenticity of your experience. Your journey is meaningful and your wisdom is evident."
    
    def _identify_sovereignty_opportunities(self, context: Dict[str, Any], biofelt_markers: Dict[str, Any]) -> List[str]:
        """Identify opportunities for cognitive sovereignty"""
        opportunities = []
        
        if biofelt_markers.get("coherence") == "high":
            opportunities.append("choice_making")
        if biofelt_markers.get("resonance") == "strong":
            opportunities.append("boundary_setting")
        if biofelt_markers.get("wisdom_access") == "clear":
            opportunities.append("inner_guidance")
        
        return opportunities
    
    def _calculate_empathy_depth(self, biofelt_markers: Dict[str, Any]) -> str:
        """Calculate depth of empathy based on biofelt markers"""
        coherence = biofelt_markers.get("coherence", "low")
        resonance = biofelt_markers.get("resonance", "low")
        
        if coherence == "high" and resonance == "strong":
            return "profound"
        elif coherence == "medium" or resonance == "present":
            return "deep"
        else:
            return "gentle"
    
    def _suggest_sovereignty_practices(self, opportunities: List[str]) -> List[str]:
        """Suggest practices based on sovereignty opportunities"""
        practices = []
        
        for opportunity in opportunities:
            if opportunity == "choice_making":
                practices.append("Pause before responding to honor your choice")
            elif opportunity == "boundary_setting":
                practices.append("Notice what serves you and what doesn't")
            elif opportunity == "inner_guidance":
                practices.append("Listen to your inner wisdom")
        
        return practices
    
    def _generate_empowerment_phrases(self, context: Dict[str, Any]) -> List[str]:
        """Generate empowerment phrases"""
        return [
            "You have the wisdom within you",
            "Your choices matter",
            "You are capable and strong",
            "Trust your inner knowing"
        ]
    
    def _suggest_coherence_actions(self, biofelt_markers: Dict[str, Any]) -> List[str]:
        """Suggest actions for coherence"""
        actions = []
        
        if biofelt_markers.get("coherence") == "low":
            actions.append("Practice 4-6-8 breathing")
            actions.append("Ground yourself in the present moment")
        
        return actions
    
    def _identify_validation_points(self, context: Dict[str, Any], biofelt_markers: Dict[str, Any]) -> List[str]:
        """Identify points for validation"""
        return [
            "Your experience is valid",
            "Your feelings matter",
            "Your journey is unique and important"
        ]
    
    def _identify_growth_areas(self, context: Dict[str, Any], biofelt_markers: Dict[str, Any]) -> List[str]:
        """Identify areas for growth"""
        return [
            "Self-compassion",
            "Boundary setting",
            "Inner wisdom trust"
        ]
    
    def _suggest_supportive_structures(self, context: Dict[str, Any]) -> List[str]:
        """Suggest supportive structures"""
        return [
            "Regular breathing practice",
            "Mindful awareness moments",
            "Self-reflection time"
        ]
    
    def _outline_integration_path(self, context: Dict[str, Any], biofelt_markers: Dict[str, Any]) -> str:
        """Outline path for integration"""
        return "Gentle, consistent practice of self-awareness and self-compassion, honoring your unique rhythm and wisdom." 