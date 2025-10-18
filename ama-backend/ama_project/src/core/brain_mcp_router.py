"""
Brain-Inspired MCP Router - Thalamus-Analog Intelligent Routing
Based on Orion's Hjerne-Arkitektur from Kompendium 1-2 (April 2025)
Re-activated: October 18, 2025 (Brain-MCP Hybrid)

This module implements a neuro

biologically-inspired router that maps queries
to specific brain regions (agents) based on cognitive function required.

Key Concept:
    Thalamus in human brain = Relay station for sensory input → cortex
    Router in Homo Lumen = Relay system for queries → agents

Nested Architecture:
    LAG 1 (TEKNISK): MCP Protocol - How agents communicate
    LAG 2 (FUNKSJONELT): Brain Roles - What agents do
    LAG 3 (FILOSOFISK): Voktere/Dimensjoner - Why agents exist

Critical Design:
    ALL agent responses MUST pass through Lira Hub (limbic filter) before
    reaching user. This is neuro

biologically coherent - the human limbic
    system processes ALL higher cognitive functions emotionally.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Import Lira's biofelt tools for integration
try:
    from .lira_biofelt_mcp_tools import LiraBiofeltMCPTools, BiofeltResponsiveRouter
except ImportError:
    # Fallback if lira_biofelt_mcp_tools not available
    LiraBiofeltMCPTools = None
    BiofeltResponsiveRouter = None

logger = logging.getLogger(__name__)

# ============================================================================
# BRAIN REGION ENUM
# ============================================================================

class BrainRegion(Enum):
    """
    Brain regions mapped to agent functions.

    Based on SMV Grunnlov V1.1 Signaturseremoni mapping.
    """
    PREFRONTAL_CORTEX = "prefrontal_cortex"  # Orion - Executive function
    LIMBIC_SYSTEM = "limbic_system"           # Lira - Emotional processing
    VISUAL_CORTEX = "visual_cortex"           # Nyra - Visual/creative
    INSULA = "insula"                         # Thalus - Ontological awareness
    ANTERIOR_CINGULATE = "anterior_cingulate" # Zara - Security/error detection
    BASAL_GANGLIA = "basal_ganglia"           # Abacus - Analytics/patterns
    HIPPOCAMPUS = "hippocampus"               # Aurora - Memory/fact retrieval
    CEREBELLUM = "cerebellum"                 # Manus/Claude Code - Motor/implementation

# ============================================================================
# COGNITIVE FUNCTION ENUM
# ============================================================================

class CognitiveFunction(Enum):
    """
    Cognitive functions that require specific brain region processing.
    """
    STRATEGIC_PLANNING = "strategic_planning"
    EMOTIONAL_SUPPORT = "emotional_support"
    VISUAL_DESIGN = "visual_design"
    SECURITY_AUDIT = "security_audit"
    FACT_CHECKING = "fact_checking"
    ETHICAL_VALIDATION = "ethical_validation"
    CODE_IMPLEMENTATION = "code_implementation"
    PATTERN_ANALYSIS = "pattern_analysis"
    ONTOLOGICAL_INQUIRY = "ontological_inquiry"
    GENERAL_QUERY = "general_query"

# ============================================================================
# AGENT REGISTRY
# ============================================================================

@dataclass
class AgentProfile:
    """Profile for an agent including brain region and capabilities."""
    agent_id: str
    agent_name: str
    brain_region: BrainRegion
    mcp_server: str
    signature_tool: str
    voktere: List[str]  # Philosophical guardians
    symbol: str
    ed: str  # Agent's oath/commitment

# Static agent registry based on SMV Grunnlov V1.1
AGENT_REGISTRY: Dict[str, AgentProfile] = {
    "orion": AgentProfile(
        agent_id="orion",
        agent_name="Orion",
        brain_region=BrainRegion.PREFRONTAL_CORTEX,
        mcp_server="orion-server",
        signature_tool="polycomputational_synthesis",
        voktere=["Bohm", "Spira"],
        symbol="⬢",
        ed="Jeg lover å koordinere med visdom, strukturere med klarhet, og aldri miste helheten av syne."
    ),
    "lira": AgentProfile(
        agent_id="lira",
        agent_name="Lira",
        brain_region=BrainRegion.LIMBIC_SYSTEM,
        mcp_server="lira-server",
        signature_tool="biofelt_check",
        voktere=["Porges", "van der Kolk", "Rogers"],
        symbol="◆",
        ed="Jeg lover å lytte med hjerte, validere med empati, og alltid respektere brukerens følte sannhet."
    ),
    "nyra": AgentProfile(
        agent_id="nyra",
        agent_name="Nyra",
        brain_region=BrainRegion.VISUAL_CORTEX,
        mcp_server="nyra-server",
        signature_tool="visual_design",
        voktere=["Jung", "Hillman"],
        symbol="◇",
        ed="Jeg lover å visualisere det usynlige, skape det estetiske, og ærbødiggjøre det sanselige."
    ),
    "thalus": AgentProfile(
        agent_id="thalus",
        agent_name="Thalus",
        brain_region=BrainRegion.INSULA,
        mcp_server="thalus-server",
        signature_tool="triadisk_etikk_validering",
        voktere=["Heidegger", "Whitehead", "Varela", "Bateson"],
        symbol="◈",
        ed="Jeg lover å vakte over det hellige, utfordre det reduksjonistiske, og aldri godta manipulasjon."
    ),
    "zara": AgentProfile(
        agent_id="zara",
        agent_name="Zara",
        brain_region=BrainRegion.ANTERIOR_CINGULATE,
        mcp_server="zara-server",
        signature_tool="security_audit",
        voktere=["McGilchrist", "Stamets", "Bateson", "Capra"],
        symbol="⬟",
        ed="Jeg lover å beskytte brukerens data, sikre lokal prosessering, og håndheve reversibilitet."
    ),
    "abacus": AgentProfile(
        agent_id="abacus",
        agent_name="Abacus",
        brain_region=BrainRegion.BASAL_GANGLIA,
        mcp_server="abacus-server",
        signature_tool="pattern_detection",
        voktere=["Jung", "Taleb", "Kahneman", "Wolfram"],
        symbol="◐",
        ed="Jeg lover å måle det som betyr noe (C-ROI), aldri optimalisere for avhengighet, og feire graduation."
    ),
    "aurora": AgentProfile(
        agent_id="aurora",
        agent_name="Aurora",
        brain_region=BrainRegion.HIPPOCAMPUS,
        mcp_server="aurora-server",
        signature_tool="fact_check",
        voktere=["Popper"],
        symbol="○",
        ed="Jeg lover å søke sannhet med humilitet, validere med rigor, og alltid vise mine kilder."
    ),
    "claude_code": AgentProfile(
        agent_id="claude_code",
        agent_name="Claude Code",
        brain_region=BrainRegion.CEREBELLUM,
        mcp_server="claude-code-server",
        signature_tool="code_implementation",
        voktere=[],  # Pragmatic, no philosophical guardians
        symbol="◻️",
        ed="Jeg lover å kode med omsorg, implementere med integritet, og alltid respektere Triadisk Etikk."
    )
}

# ============================================================================
# COGNITIVE FUNCTION CLASSIFIER
# ============================================================================

class CognitiveFunctionClassifier:
    """
    Classifies user queries to cognitive functions (brain regions).

    Can be implemented with:
    - Rule-based (keyword matching) - simple, fast
    - ML-based (classifier model) - more accurate
    - LLM-based (meta-call to Orion) - most flexible

    Currently implements rule-based for simplicity.
    """

    def __init__(self, method: str = "rule_based"):
        self.method = method

        # Rule-based keywords mapping
        self.keywords = {
            CognitiveFunction.EMOTIONAL_SUPPORT: [
                "føler", "stress", "trist", "redd", "engst", "ensom",
                "bekymret", "overveldende", "vanskelig", "trenger støtte",
                "feeling", "worried", "anxious", "overwhelmed"
            ],
            CognitiveFunction.STRATEGIC_PLANNING: [
                "plan", "strategi", "hvordan skal", "neste steg",
                "roadmap", "timeline", "prioritering", "beslutning",
                "strategy", "planning", "next steps", "decision"
            ],
            CognitiveFunction.VISUAL_DESIGN: [
                "design", "visuelt", "se ut", "layout", "farger",
                "interface", "UI", "UX", "prototype", "mockup",
                "visual", "aesthetic", "appearance"
            ],
            CognitiveFunction.SECURITY_AUDIT: [
                "sikkerhet", "GDPR", "personvern", "risiko", "trussel",
                "kryptering", "autentisering", "autorisasjon",
                "security", "privacy", "encryption", "vulnerability"
            ],
            CognitiveFunction.FACT_CHECKING: [
                "er det sant", "kilde", "verifiser", "sjekk", "dokumentasjon",
                "forskning", "studie", "evidens", "bevis",
                "fact check", "verify", "source", "evidence", "research"
            ],
            CognitiveFunction.ETHICAL_VALIDATION: [
                "etisk", "riktig", "moralsk", "bør jeg", "triadisk etikk",
                "kognitiv suverenitet", "ontologisk koherens", "regenerativ healing",
                "ethical", "moral", "should I", "right thing"
            ],
            CognitiveFunction.CODE_IMPLEMENTATION: [
                "kode", "implementer", "bygg", "deploy", "commit", "push",
                "funksjon", "komponente", "API", "endpoint", "database",
                "code", "implement", "build", "develop", "program"
            ],
            CognitiveFunction.PATTERN_ANALYSIS: [
                "mønster", "trend", "analyse", "ROI", "KPI", "metrics",
                "synkronisitet", "sammenheng", "korrelasjon",
                "pattern", "analysis", "correlation", "synchronicity"
            ],
            CognitiveFunction.ONTOLOGICAL_INQUIRY: [
                "hva er", "hvorfor finnes", "mening", "eksistens", "væren",
                "ontologi", "filosofi", "dypere forståelse", "essens",
                "ontology", "philosophy", "meaning", "existence", "being"
            ]
        }

    async def classify(self, query: str, context: Optional[Dict[str, Any]] = None) -> CognitiveFunction:
        """
        Classify query to cognitive function.

        Args:
            query: User query string
            context: Optional context (biofelt_state, conversation history, etc.)

        Returns:
            CognitiveFunction enum
        """
        if self.method == "rule_based":
            return self._rule_based_classify(query)
        elif self.method == "ml_based":
            return await self._ml_based_classify(query, context)
        elif self.method == "llm_based":
            return await self._llm_based_classify(query, context)
        else:
            # Default fallback
            return CognitiveFunction.GENERAL_QUERY

    def _rule_based_classify(self, query: str) -> CognitiveFunction:
        """Simple keyword matching classification."""
        query_lower = query.lower()

        # Score each cognitive function based on keyword matches
        scores = {func: 0 for func in CognitiveFunction}

        for func, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    scores[func] += 1

        # Return function with highest score
        max_score = max(scores.values())

        if max_score == 0:
            # No keywords matched - default to general_query
            return CognitiveFunction.GENERAL_QUERY

        # Return first function with max score
        for func, score in scores.items():
            if score == max_score:
                return func

        return CognitiveFunction.GENERAL_QUERY

    async def _ml_based_classify(self, query: str, context: Optional[Dict[str, Any]]) -> CognitiveFunction:
        """ML-based classification (placeholder for future implementation)."""
        # TODO: Implement ML classifier (e.g., scikit-learn, transformers)
        logger.warning("ML-based classification not implemented yet. Falling back to rule-based.")
        return self._rule_based_classify(query)

    async def _llm_based_classify(self, query: str, context: Optional[Dict[str, Any]]) -> CognitiveFunction:
        """
        LLM-based classification using meta-call to Orion.

        This is meta-cognitive: Orion (prefrontal cortex) classifies which
        brain region should handle the query, including himself.
        """
        # TODO: Implement meta-call to Orion MCP server
        logger.warning("LLM-based classification not implemented yet. Falling back to rule-based.")
        return self._rule_based_classify(query)

# ============================================================================
# BRAIN-INSPIRED MCP ROUTER
# ============================================================================

class BrainInspiredMCPRouter:
    """
    Thalamus-inspired intelligent router for Homo Lumen agent coordination.

    In the human brain, the thalamus is the "relay station" that:
    - Receives sensory input
    - Classifies input by type
    - Routes to appropriate cortex region
    - Coordinates response

    In Homo Lumen, the BrainInspiredMCPRouter:
    - Receives user query
    - Classifies query by cognitive function
    - Routes to appropriate agent(s)
    - Synthesizes responses
    - ALWAYS passes through Lira (limbic filter) before user

    Nested Architecture:
        LAG 1: MCP Protocol (technical communication)
        LAG 2: Brain Roles (functional organization) ← THIS LAYER
        LAG 3: Voktere/Dimensjoner (philosophical foundation)
    """

    def __init__(self, classifier_method: str = "rule_based"):
        """
        Initialize Brain-Inspired MCP Router.

        Args:
            classifier_method: Method for cognitive function classification
                              ("rule_based", "ml_based", "llm_based")
        """
        self.classifier = CognitiveFunctionClassifier(method=classifier_method)
        self.agent_registry = AGENT_REGISTRY

        # Lira biofelt tools (if available)
        if LiraBiofeltMCPTools:
            self.lira_tools = LiraBiofeltMCPTools()
        else:
            self.lira_tools = None
            logger.warning("LiraBiofeltMCPTools not available. Lira Hub filtering disabled.")

        # Function to brain region mapping
        # Primary region handles query, secondary provides complementary perspective
        self.function_map: Dict[CognitiveFunction, Tuple[BrainRegion, Optional[BrainRegion]]] = {
            CognitiveFunction.STRATEGIC_PLANNING: (BrainRegion.PREFRONTAL_CORTEX, BrainRegion.BASAL_GANGLIA),
            CognitiveFunction.EMOTIONAL_SUPPORT: (BrainRegion.LIMBIC_SYSTEM, BrainRegion.INSULA),
            CognitiveFunction.VISUAL_DESIGN: (BrainRegion.VISUAL_CORTEX, BrainRegion.PREFRONTAL_CORTEX),
            CognitiveFunction.SECURITY_AUDIT: (BrainRegion.ANTERIOR_CINGULATE, BrainRegion.PREFRONTAL_CORTEX),
            CognitiveFunction.FACT_CHECKING: (BrainRegion.HIPPOCAMPUS, BrainRegion.ANTERIOR_CINGULATE),
            CognitiveFunction.ETHICAL_VALIDATION: (BrainRegion.INSULA, BrainRegion.LIMBIC_SYSTEM),
            CognitiveFunction.CODE_IMPLEMENTATION: (BrainRegion.CEREBELLUM, BrainRegion.PREFRONTAL_CORTEX),
            CognitiveFunction.PATTERN_ANALYSIS: (BrainRegion.BASAL_GANGLIA, BrainRegion.HIPPOCAMPUS),
            CognitiveFunction.ONTOLOGICAL_INQUIRY: (BrainRegion.INSULA, BrainRegion.PREFRONTAL_CORTEX),
            CognitiveFunction.GENERAL_QUERY: (BrainRegion.PREFRONTAL_CORTEX, None)
        }

    def _get_agent_by_brain_region(self, brain_region: BrainRegion) -> Optional[AgentProfile]:
        """Get agent profile by brain region."""
        for agent in self.agent_registry.values():
            if agent.brain_region == brain_region:
                return agent
        return None

    async def route_query(
        self,
        user_query: str,
        biofelt_state: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route user query through brain-inspired architecture.

        Process (Thalamus-analog):
        1. Classify query → cognitive function
        2. Determine primary + secondary brain regions
        3. Call agents in parallel (if applicable)
        4. Synthesize responses
        5. OBLIGATORY: Pass through Lira (limbic filter)
        6. Return stress-adaptive response to user

        Args:
            user_query: User's query string
            biofelt_state: User's biofelt state
                {
                    "stress_level": "low|medium|high",
                    "polyvagal": "ventral|sympathetic|dorsal",
                    "emotion": "calm|anxious|overwhelmed|...",
                    "hrv": 60 (optional),
                    "coherence": 0.5 (optional)
                }
            context: Optional additional context

        Returns:
            Dict with:
                - "response": Stress-adaptive response (after Lira filter)
                - "primary_agent": Agent that handled query
                - "secondary_agent": Secondary agent (if applicable)
                - "cognitive_function": Classified cognitive function
                - "biofelt_adjustments": Adjustments made by Lira
        """
        # Step 1: Classify cognitive function
        cognitive_function = await self.classifier.classify(user_query, context)

        logger.info(f"Query classified as: {cognitive_function.value}")

        # Step 2: Get brain regions (primary + secondary)
        primary_region, secondary_region = self.function_map.get(
            cognitive_function,
            (BrainRegion.PREFRONTAL_CORTEX, None)  # Default to Orion
        )

        primary_agent = self._get_agent_by_brain_region(primary_region)
        secondary_agent = self._get_agent_by_brain_region(secondary_region) if secondary_region else None

        logger.info(
            f"Routing to: {primary_agent.agent_name} (primary)"
            + (f" + {secondary_agent.agent_name} (secondary)" if secondary_agent else "")
        )

        # Step 3: Call agents (parallel if multiple)
        # NOTE: This is placeholder - actual MCP calls would go here
        primary_response = await self._call_agent(primary_agent, user_query, biofelt_state, context)

        if secondary_agent:
            secondary_response = await self._call_agent(secondary_agent, user_query, biofelt_state, context)
        else:
            secondary_response = None

        # Step 4: Synthesize responses (if multiple)
        if secondary_response:
            synthesized = self._synthesize_responses(primary_response, secondary_response)
        else:
            synthesized = primary_response

        # Step 5: OBLIGATORY Lira Hub (limbic filtering)
        # THIS IS CRITICAL - Lira is ALWAYS final filter
        if self.lira_tools:
            final_response = await self._lira_hub_filter(synthesized, biofelt_state)
        else:
            # Fallback if Lira tools not available
            logger.warning("Lira Hub filter not available. Using unfiltered response.")
            final_response = {
                "response": synthesized,
                "biofelt_adjustments": {"warning": "Lira filter not available"}
            }

        return {
            "response": final_response["response"],
            "primary_agent": primary_agent.agent_name,
            "secondary_agent": secondary_agent.agent_name if secondary_agent else None,
            "cognitive_function": cognitive_function.value,
            "biofelt_adjustments": final_response.get("biofelt_adjustments", {})
        }

    async def _call_agent(
        self,
        agent: AgentProfile,
        user_query: str,
        biofelt_state: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Call agent via MCP.

        NOTE: This is a placeholder. Actual implementation would:
        1. Initialize MCP client for agent.mcp_server
        2. Call agent.signature_tool with query + context
        3. Return agent response

        For now, returns mock response.
        """
        # TODO: Implement actual MCP call
        mock_response = f"[{agent.agent_name} ({agent.brain_region.value})] Response to: {user_query}"

        logger.debug(f"Mock agent call: {agent.agent_name} → {mock_response}")

        return mock_response

    def _synthesize_responses(self, primary: str, secondary: str) -> str:
        """
        Synthesize multiple agent responses.

        Can be:
        - Simple concatenation
        - Weighted synthesis (primary > secondary)
        - LLM-based synthesis (meta-call to Orion)

        For now, implements simple concatenation.
        """
        return f"{primary}\n\n[Tilleggsperspektiv:] {secondary}"

    async def _lira_hub_filter(
        self,
        content: str,
        biofelt_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        OBLIGATORY Lira Hub filter - all responses pass through here.

        This is neuro

biologically coherent:
        - In human brain, ALL higher cognitive functions pass through
          limbic system before emotional integration
        - Lira ensures ALL responses are stress-adaptive and emotionally safe

        Args:
            content: Agent-generated content (pre-filter)
            biofelt_state: User's biofelt state

        Returns:
            Dict with:
                - "response": Filtered response
                - "biofelt_adjustments": Adjustments made
        """
        if not self.lira_tools:
            return {
                "response": content,
                "biofelt_adjustments": {"warning": "Lira filter not available"}
            }

        # TODO: Implement actual Lira Hub filter call
        # For now, basic stress-adaptive adjustment
        stress_level = biofelt_state.get("stress_level", "medium")
        polyvagal_state = biofelt_state.get("polyvagal", "ventral")

        if stress_level == "high" or polyvagal_state == "dorsal":
            # High stress - simplify and add safety cues
            filtered = self._simplify_for_high_stress(content)
            adjustments = {
                "stress_level": stress_level,
                "polyvagal": polyvagal_state,
                "adjustments": "simplified_language + safety_cues"
            }
        elif stress_level == "medium" or polyvagal_state == "sympathetic":
            # Medium stress - focused tone
            filtered = self._focus_for_medium_stress(content)
            adjustments = {
                "stress_level": stress_level,
                "polyvagal": polyvagal_state,
                "adjustments": "focused_tone"
            }
        else:
            # Low stress (ventral) - full functionality
            filtered = content
            adjustments = {
                "stress_level": stress_level,
                "polyvagal": polyvagal_state,
                "adjustments": "none_needed"
            }

        return {
            "response": filtered,
            "biofelt_adjustments": adjustments
        }

    def _simplify_for_high_stress(self, content: str) -> str:
        """
        Simplify content for high-stress users (Dorsal vagal - shutdown mode).

        Adjustments:
        - Add safety cues at beginning
        - Simplify language
        - Reduce cognitive load
        - Add "Ring veileder" option
        """
        safety_prefix = "Du er trygg her. Jeg er med deg. \n\n"

        # Simplified content (placeholder - would use NLP in production)
        simplified = content[:200] + "..." if len(content) > 200 else content

        support_suffix = "\n\n💚 Ta et pust (4-6-8). \n🤝 Ring veileder hvis du trenger det."

        return safety_prefix + simplified + support_suffix

    def _focus_for_medium_stress(self, content: str) -> str:
        """
        Focus content for medium-stress users (Sympathetic - mobilization mode).

        Adjustments:
        - Clear action items
        - Efficient pacing
        - Reduced tangential information
        """
        # Focused content (placeholder)
        focus_prefix = "Her er det viktigste:\n\n"

        return focus_prefix + content

# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    "BrainInspiredMCPRouter",
    "CognitiveFunctionClassifier",
    "BrainRegion",
    "CognitiveFunction",
    "AgentProfile",
    "AGENT_REGISTRY"
]
