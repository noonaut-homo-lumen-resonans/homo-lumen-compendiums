"""
Lira Hub Filter - Stress-Adaptive Complexity Evaluation
Part of Brain-MCP Hybrid Architecture

This module implements Lira's role as the OBLIGATORY limbic filter for all
agent responses in the Homo Lumen system.

Neuro

biological Foundation:
    In the human brain, the limbic system (amygdala, hippocampus, insula)
    processes ALL higher cognitive functions emotionally BEFORE they reach
    conscious awareness. No information enters consciousness without emotional
    context.

    Similarly, in Homo Lumen, ALL agent responses (including technical code)
    pass through Lira Hub Filter BEFORE reaching the user. This ensures:
    - Emotional safety
    - Stress-adaptive complexity
    - Triadisk Etikk (especially Regenerativ Healing port)

Critical Design Principle:
    "Vi er speil, ikke verktøy" - Technology should reflect the soul, not cage
    the mind. Lira ensures all responses honor this principle.
"""

import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# ============================================================================
# STRESS LEVEL & POLYVAGAL STATE ENUMS
# ============================================================================

class StressLevel(Enum):
    """User stress levels based on biofelt analysis."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class PolyvagalState(Enum):
    """
    Polyvagal states (from Porges' Polyvagal Theory).

    Ventral Vagal: Social engagement, safety, connection
    Sympathetic: Fight/flight, mobilization
    Dorsal Vagal: Shutdown, freeze, immobilization
    """
    VENTRAL = "ventral"
    SYMPATHETIC = "sympathetic"
    DORSAL = "dorsal"

# ============================================================================
# FILTER ADJUSTMENT RULES
# ============================================================================

@dataclass
class FilterAdjustment:
    """Adjustment rules for stress-adaptive filtering."""
    tone: str  # detailed|focused|simple
    complexity: str  # full|reduced|minimal
    pacing: str  # normal|efficient|slow
    add_safety_language: bool = False
    add_breathing_reminder: bool = False
    add_human_contact_option: bool = False
    max_info_chunks: int = 10  # Maximum information chunks to display

# Adjustment rules matrix
ADJUSTMENT_RULES: Dict[tuple, FilterAdjustment] = {
    # Ventral vagal (trygghet) - Full funksjonalitet
    (StressLevel.LOW, PolyvagalState.VENTRAL): FilterAdjustment(
        tone="detailed",
        complexity="full",
        pacing="normal",
        max_info_chunks=10
    ),

    # Sympatisk (mobilisering) - Fokusert
    (StressLevel.MEDIUM, PolyvagalState.SYMPATHETIC): FilterAdjustment(
        tone="focused",
        complexity="reduced",
        pacing="efficient",
        add_breathing_reminder=True,
        max_info_chunks=5
    ),

    # Dorsal vagal (nedstenging) - Trygg Havn
    (StressLevel.HIGH, PolyvagalState.DORSAL): FilterAdjustment(
        tone="simple",
        complexity="minimal",
        pacing="slow",
        add_safety_language=True,
        add_breathing_reminder=True,
        add_human_contact_option=True,
        max_info_chunks=3
    ),

    # Mixed states (fallback combinations)
    (StressLevel.MEDIUM, PolyvagalState.VENTRAL): FilterAdjustment(
        tone="focused",
        complexity="reduced",
        pacing="normal",
        max_info_chunks=7
    ),
    (StressLevel.HIGH, PolyvagalState.SYMPATHETIC): FilterAdjustment(
        tone="simple",
        complexity="reduced",
        pacing="efficient",
        add_safety_language=True,
        add_breathing_reminder=True,
        max_info_chunks=4
    ),
}

# ============================================================================
# LIRA HUB FILTER
# ============================================================================

class LiraHubFilter:
    """
    Lira's limbic system filter - OBLIGATORY final step before user.

    Adjusts:
    - Tone (formal/friendly/intimate)
    - Complexity (detailed/balanced/simple)
    - Pacing (fast/normal/slow)

    Based on:
    - User's stress level (low/medium/high)
    - Polyvagal state (ventral/sympathetic/dorsal)
    - Emotional state (current emotion from biofelt)
    - Content type (technical/emotional/strategic)
    """

    def __init__(self):
        self.adjustment_rules = ADJUSTMENT_RULES

        # Triggering words that reduce emotional safety
        self.triggering_words = [
            "should", "must", "need to", "have to", "required",
            "mandatory", "obligation", "skal", "må", "bør"
        ]

        # Safety language templates
        self.safety_templates = [
            "Du er trygg her. ",
            "Jeg er med deg. ",
            "Vi tar dette i ditt tempo. "
        ]

    async def filter(
        self,
        content: str,
        biofelt_state: Dict[str, Any],
        content_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Apply stress-adaptive filter to content.

        Args:
            content: Agent-generated response (pre-filter)
            biofelt_state: {
                "stress_level": "low|medium|high",
                "polyvagal": "ventral|sympathetic|dorsal",
                "emotion": "calm|anxious|overwhelmed|...",
                "hrv": 60 (optional),
                "coherence": 0.5 (optional)
            }
            content_type: Optional content type hint
                         ("technical", "emotional", "strategic", "code")

        Returns:
            Dict with:
                - "filtered_content": Stress-adaptive filtered content
                - "adjustments_applied": List of adjustments made
                - "emotional_safety_score": 0-1 safety score
                - "original_length": Length before filtering
                - "filtered_length": Length after filtering
        """
        # Parse biofelt state
        stress = self._parse_stress_level(biofelt_state.get("stress_level", "medium"))
        polyvagal = self._parse_polyvagal_state(biofelt_state.get("polyvagal", "ventral"))

        # Get adjustment rule
        adjustment = self.adjustment_rules.get(
            (stress, polyvagal),
            FilterAdjustment(tone="focused", complexity="reduced", pacing="normal")  # Default
        )

        logger.info(
            f"Lira Hub Filter: stress={stress.value}, polyvagal={polyvagal.value}, "
            f"adjustments={adjustment.tone}/{adjustment.complexity}/{adjustment.pacing}"
        )

        # Apply adjustments
        filtered_content = content
        adjustments_applied = []

        # 1. Safety language (if needed)
        if adjustment.add_safety_language:
            filtered_content = self._add_safety_cues(filtered_content)
            adjustments_applied.append("safety_cues_added")

        # 2. Simplify language (if needed)
        if adjustment.tone == "simple":
            filtered_content = self._simplify_language(filtered_content)
            adjustments_applied.append("language_simplified")

        # 3. Reduce complexity (if needed)
        if adjustment.complexity in ["reduced", "minimal"]:
            filtered_content = self._reduce_complexity(
                filtered_content,
                adjustment.max_info_chunks
            )
            adjustments_applied.append(f"complexity_reduced_to_{adjustment.max_info_chunks}_chunks")

        # 4. Adjust pacing (if needed)
        if adjustment.pacing == "slow":
            filtered_content = self._slow_pacing(filtered_content)
            adjustments_applied.append("pacing_slowed")

        # 5. Add breathing reminder (if needed)
        if adjustment.add_breathing_reminder:
            filtered_content = self._add_breathing_reminder(filtered_content)
            adjustments_applied.append("breathing_reminder_added")

        # 6. Add human contact option (if needed)
        if adjustment.add_human_contact_option:
            filtered_content = self._add_human_contact_option(filtered_content)
            adjustments_applied.append("human_contact_option_added")

        # 7. Special handling for technical/code content
        if content_type == "code" or self._is_code_content(content):
            filtered_content = self._filter_technical_content(
                filtered_content,
                adjustment
            )
            adjustments_applied.append("technical_content_filtered")

        # Calculate emotional safety score
        emotional_safety = self._calculate_emotional_safety(filtered_content)

        return {
            "filtered_content": filtered_content,
            "adjustments_applied": adjustments_applied,
            "emotional_safety_score": emotional_safety,
            "original_length": len(content),
            "filtered_length": len(filtered_content),
            "stress_level": stress.value,
            "polyvagal_state": polyvagal.value
        }

    # ========================================================================
    # PARSING HELPERS
    # ========================================================================

    def _parse_stress_level(self, stress_str: str) -> StressLevel:
        """Parse stress level string to enum."""
        stress_map = {
            "low": StressLevel.LOW,
            "medium": StressLevel.MEDIUM,
            "high": StressLevel.HIGH
        }
        return stress_map.get(stress_str.lower(), StressLevel.MEDIUM)

    def _parse_polyvagal_state(self, polyvagal_str: str) -> PolyvagalState:
        """Parse polyvagal state string to enum."""
        polyvagal_map = {
            "ventral": PolyvagalState.VENTRAL,
            "sympathetic": PolyvagalState.SYMPATHETIC,
            "dorsal": PolyvagalState.DORSAL
        }
        return polyvagal_map.get(polyvagal_str.lower(), PolyvagalState.VENTRAL)

    # ========================================================================
    # ADJUSTMENT METHODS
    # ========================================================================

    def _add_safety_cues(self, text: str) -> str:
        """Add polyvagal safety language at beginning."""
        safety_prefix = "".join(self.safety_templates[:2])  # First 2 templates
        return safety_prefix + text

    def _simplify_language(self, text: str) -> str:
        """
        Simplify language for high-stress users.

        - Replace complex words with simpler alternatives
        - Shorten sentences
        - Remove jargon
        """
        # Replace complex words (placeholder - would use NLP in production)
        simplifications = {
            "implement": "lage",
            "utilize": "bruke",
            "architecture": "struktur",
            "synthesize": "kombinere",
            "facilitate": "hjelpe",
            "subsequently": "deretter",
            "consequently": "derfor"
        }

        simplified = text
        for complex_word, simple_word in simplifications.items():
            simplified = re.sub(
                r'\b' + complex_word + r'\b',
                simple_word,
                simplified,
                flags=re.IGNORECASE
            )

        return simplified

    def _reduce_complexity(self, text: str, max_chunks: int) -> str:
        """
        Reduce information density.

        - Extract key points only
        - Remove tangential information
        - Break into smaller chunks
        - Limit to max_chunks information pieces
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)

        # Keep only first max_chunks sentences
        reduced_sentences = sentences[:max_chunks]

        # Rejoin with clear separators
        reduced = ". ".join(s.strip() for s in reduced_sentences if s.strip())

        # Add ellipsis if truncated
        if len(sentences) > max_chunks:
            reduced += "...\n\n[Mer informasjon tilgjengelig når du er klar]"

        return reduced

    def _slow_pacing(self, text: str) -> str:
        """
        Slow pacing for overwhelmed users.

        - Add line breaks between sentences
        - Add pauses (visual whitespace)
        - Break into numbered steps
        """
        # Split into sentences
        sentences = re.split(r'([.!?]+)', text)

        # Rejoin with extra spacing
        slowed = ""
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i].strip()
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else "."

            if sentence:
                slowed += sentence + punctuation + "\n\n"

        return slowed.strip()

    def _add_breathing_reminder(self, text: str) -> str:
        """Add breathing reminder at end."""
        breathing_reminder = "\n\n💚 **Pust med meg:** Pust inn (4), hold (6), pust ut (8)."
        return text + breathing_reminder

    def _add_human_contact_option(self, text: str) -> str:
        """Add option to contact human veileder."""
        human_contact = "\n\n🤝 **Trenger du et menneske?** [Ring veileder] - Alltid tilgjengelig."
        return text + human_contact

    def _filter_technical_content(self, text: str, adjustment: FilterAdjustment) -> str:
        """
        Special filtering for technical/code content.

        For high stress:
        - Wrap code in expandable section
        - Add plain-language explanation FIRST
        - Add "Du trenger ikke forstå dette nå" disclaimer
        - Offer to explain later
        """
        if adjustment.complexity == "minimal":
            # Hide technical details, show only outcome
            # Extract code blocks
            code_blocks = re.findall(r'```[\s\S]*?```', text)

            if code_blocks:
                # Replace code with placeholder
                simplified = re.sub(r'```[\s\S]*?```', '[Tekniske detaljer skjult]', text)

                # Add explanation
                explanation = (
                    "\n\nJeg har bygget dette for deg. "
                    "Du trenger ikke forstå den tekniske koden nå. "
                    "Den er trygg og gjør det den skal.\n\n"
                    "[Vis tekniske detaljer] (når du er klar)"
                )

                return simplified + explanation
            else:
                # No code blocks, just simplify text
                return text

        elif adjustment.complexity == "reduced":
            # Show code but with simplified explanation
            explanation_prefix = (
                "Her er det jeg har gjort (teknisk):\n\n"
            )

            explanation_suffix = (
                "\n\nForenklet forklaring: [Hva dette gjør i praksis]"
            )

            return explanation_prefix + text + explanation_suffix

        else:
            # Full technical detail (ventral state)
            return text

    def _is_code_content(self, text: str) -> bool:
        """Detect if content contains code."""
        # Check for code indicators
        code_indicators = [
            '```',  # Markdown code blocks
            'def ',  # Python functions
            'class ',  # Classes
            'import ',  # Imports
            '{',  # Curly braces (JS, JSON)
            'const ',  # JS constants
            'function(',  # JS functions
        ]

        return any(indicator in text for indicator in code_indicators)

    def _calculate_emotional_safety(self, text: str) -> float:
        """
        Calculate emotional safety score of filtered text.

        Checks for:
        - Triggering words (reduces score)
        - Safety language (increases score)
        - Directive language (reduces score)
        - Validating language (increases score)
        """
        safety_score = 0.8  # Base safety score

        # Check for triggering words
        for word in self.triggering_words:
            if word.lower() in text.lower():
                safety_score -= 0.05

        # Check for safety language
        safety_indicators = ["trygg", "sammen", "i ditt tempo", "når du er klar", "safe", "you're okay"]
        for indicator in safety_indicators:
            if indicator.lower() in text.lower():
                safety_score += 0.05

        # Check for validating language
        validating_indicators = ["jeg forstår", "jeg ser", "det er ok", "I understand", "I see you"]
        for indicator in validating_indicators:
            if indicator.lower() in text.lower():
                safety_score += 0.05

        # Clamp to [0, 1]
        return max(0.0, min(1.0, safety_score))

    # ========================================================================
    # EVALUATION METHODS (for other agents' content)
    # ========================================================================

    async def evaluate_code_complexity(
        self,
        code_response: str,
        biofelt_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate code complexity for emotional safety.

        This is specifically for evaluating technical implementations
        (like Claude Code's code) to ensure they're emotionally safe.

        Args:
            code_response: Code or technical response from agent
            biofelt_state: User's biofelt state

        Returns:
            Dict with:
                - "is_emotionally_safe": bool
                - "recommended_adjustments": List[str]
                - "filtered_response": Stress-adaptive version
        """
        # Parse biofelt state
        stress = self._parse_stress_level(biofelt_state.get("stress_level", "medium"))

        # Determine if code is emotionally safe as-is
        is_safe = stress == StressLevel.LOW

        if is_safe:
            # Low stress - full technical detail okay
            return {
                "is_emotionally_safe": True,
                "recommended_adjustments": [],
                "filtered_response": code_response
            }
        else:
            # Medium/high stress - needs adjustment
            filtered_result = await self.filter(
                code_response,
                biofelt_state,
                content_type="code"
            )

            return {
                "is_emotionally_safe": False,
                "recommended_adjustments": filtered_result["adjustments_applied"],
                "filtered_response": filtered_result["filtered_content"],
                "emotional_safety_score": filtered_result["emotional_safety_score"]
            }

# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    "LiraHubFilter",
    "StressLevel",
    "PolyvagalState",
    "FilterAdjustment"
]
