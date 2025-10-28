"""
Ubuntu Playground Python SDK

Type-safe client for Ubuntu Playground API with Triadiske Portvokter support.
Integrates BiofeltGate, ThalosFilter, and MutationLog validation.

@version 1.0.0
@author Homo Lumen Coalition
"""

from typing import Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import requests


# ===========================
# CORE TYPES (Mirror Pydantic models)
# ===========================

class ResonanceLevel(str, Enum):
    """ResonanceLevel enum from BiofeltGate"""
    CRITICAL = "critical"       # HRV < 40
    LOW = "low"                # HRV 40-64
    BALANCED = "balanced"      # HRV 65-79
    OPTIMAL = "optimal"        # HRV 80-99
    TRANSCENDENT = "transcendent"  # HRV 100+


class EthicalSeverity(str, Enum):
    """EthicalSeverity enum from ThalosFilter"""
    INFO = "info"
    WARNING = "warning"
    CONCERN = "concern"
    VIOLATION = "violation"
    CRITICAL = "critical"


@dataclass
class BiofeltContext:
    """
    BiofeltContext - consciousness-aware processing context

    This context should be included in all critical operations to enable
    BiofeltGate validation based on HRV and coherence.
    """
    hrv_ms: float                    # Heart Rate Variability in milliseconds (0-200)
    coherence: float                 # Coherence score (0.0-1.0)
    pust_rytme: Optional[str] = None  # Breathing rhythm sequence (e.g., "4-6-8")
    resonance_theme: Optional[str] = None  # Felt-resonance theme
    energy_level: Optional[str] = None  # Energy level
    stress_indicators: List[str] = field(default_factory=list)  # Stress indicators
    timestamp: Optional[str] = None  # ISO timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = {
            "hrv_ms": self.hrv_ms,
            "coherence": self.coherence
        }
        if self.pust_rytme:
            data["pust_rytme"] = self.pust_rytme
        if self.resonance_theme:
            data["resonance_theme"] = self.resonance_theme
        if self.energy_level:
            data["energy_level"] = self.energy_level
        if self.stress_indicators:
            data["stress_indicators"] = self.stress_indicators
        if self.timestamp:
            data["timestamp"] = self.timestamp
        return data


@dataclass
class ThalosContext:
    """
    ThalosContext - ethical validation context

    This context provides additional information for ThalosFilter
    to make informed ethical decisions.
    """
    intent: Optional[str] = None  # Intent behind the action
    justification: Optional[str] = None  # Justification for the action
    affected_agents: List[str] = field(default_factory=list)  # Agents affected
    reversible: bool = True  # Is the action reversible?
    reviewed_by: Optional[str] = None  # Agent who reviewed this action
    emergency: bool = False  # Is this an emergency situation?
    timestamp: Optional[str] = None  # ISO timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = {"reversible": self.reversible, "emergency": self.emergency}
        if self.intent:
            data["intent"] = self.intent
        if self.justification:
            data["justification"] = self.justification
        if self.affected_agents:
            data["affected_agents"] = self.affected_agents
        if self.reviewed_by:
            data["reviewed_by"] = self.reviewed_by
        if self.timestamp:
            data["timestamp"] = self.timestamp
        return data


# ===========================
# RESPONSE TYPES
# ===========================

@dataclass
class PortvokterError:
    """Error response from Triadiske Portvokter"""
    error: str
    message: str
    resonance_level: Optional[str] = None
    hrv_status: Optional[str] = None
    coherence_status: Optional[str] = None
    severity: Optional[str] = None
    violated_principles: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    requires_review: bool = False


# ===========================
# UTILITY FUNCTIONS
# ===========================

def calculate_resonance_level(hrv_ms: float) -> ResonanceLevel:
    """Calculate ResonanceLevel from HRV"""
    if hrv_ms < 40:
        return ResonanceLevel.CRITICAL
    if hrv_ms < 65:
        return ResonanceLevel.LOW
    if hrv_ms < 80:
        return ResonanceLevel.BALANCED
    if hrv_ms < 100:
        return ResonanceLevel.OPTIMAL
    return ResonanceLevel.TRANSCENDENT


def health_data_to_biofelt_context(
    hrv: Optional[float] = None,
    heart_rate: Optional[int] = None,
    sleep_quality: Optional[str] = None,
    sleep_hours: Optional[float] = None,
    stress_level: int = 5,
    somatic_signals: Optional[List[str]] = None
) -> BiofeltContext:
    """
    Convert health data to BiofeltContext

    Args:
        hrv: Heart Rate Variability in milliseconds
        heart_rate: Heart rate in BPM
        sleep_quality: "poor", "fair", or "good"
        sleep_hours: Hours of sleep
        stress_level: Current stress level (0-10)
        somatic_signals: List of body sensations

    Returns:
        BiofeltContext for Ubuntu Playground API
    """
    # Default HRV to LOW threshold if not provided
    hrv_ms = hrv or 50.0

    # Calculate coherence based on stress level and sleep quality
    coherence = 1.0 - (stress_level / 10.0)  # Inverse of stress

    if sleep_quality == "poor":
        coherence *= 0.7
    elif sleep_quality == "fair":
        coherence *= 0.85

    # Clamp coherence to 0.0-1.0
    coherence = max(0.0, min(1.0, coherence))

    # Map stress level to energy level
    if stress_level > 7:
        energy_level = "high"
    elif stress_level > 4:
        energy_level = "balanced"
    else:
        energy_level = "low"

    # Map somatic signals to stress indicators
    somatic_signals = somatic_signals or []
    stress_indicators = [
        signal for signal in somatic_signals
        if any(word in signal.lower() for word in ["trykk", "spent", "uro", "rask", "anspent"])
    ]

    return BiofeltContext(
        hrv_ms=hrv_ms,
        coherence=coherence,
        pust_rytme="4-6-8",
        energy_level=energy_level,
        stress_indicators=stress_indicators,
        timestamp=datetime.now().isoformat()
    )


# ===========================
# UBUNTU PLAYGROUND CLIENT
# ===========================

class UbuntuPlaygroundClient:
    """Python client for Ubuntu Playground API with Triadiske Portvokter support"""

    def __init__(self, base_url: str = "http://localhost:8002", api_key: str = ""):
        """
        Initialize Ubuntu Playground client

        Args:
            base_url: Base URL of Ubuntu Playground API
            api_key: Agent API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "X-API-Key": api_key
        })

    def _handle_portvokter_error(self, response: requests.Response) -> None:
        """Handle API errors from Triadiske Portvokter"""
        try:
            error_data = response.json()
        except:
            raise Exception(f"API error: {response.status_code} {response.text}")

        error = PortvokterError(
            error=error_data.get("error", "Unknown error"),
            message=error_data.get("message", ""),
            resonance_level=error_data.get("resonance_level"),
            hrv_status=error_data.get("hrv_status"),
            coherence_status=error_data.get("coherence_status"),
            severity=error_data.get("severity"),
            violated_principles=error_data.get("violated_principles", []),
            warnings=error_data.get("warnings", []),
            recommendations=error_data.get("recommendations", []),
            requires_review=error_data.get("requires_review", False)
        )

        message = f"{error.error}: {error.message}"
        if error.recommendations:
            message += "\n\nRecommendations:\n" + "\n".join(f"- {r}" for r in error.recommendations)

        raise Exception(message)

    def health(self) -> Dict[str, Any]:
        """
        Check API health

        Returns:
            Health status dictionary
        """
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def write_file(
        self,
        path: str,
        content: str,
        biofelt_context: Optional[BiofeltContext] = None,
        thalos_context: Optional[ThalosContext] = None
    ) -> Dict[str, Any]:
        """
        Write a file to the shared workspace

        Args:
            path: File path relative to workspace root
            content: File content
            biofelt_context: Optional biofelt validation context
            thalos_context: Optional ethical validation context

        Returns:
            Write response dictionary

        Raises:
            Exception: If BiofeltGate or ThalosFilter blocks the operation
        """
        payload = {
            "path": path,
            "content": content
        }

        if biofelt_context:
            payload["biofelt_context"] = biofelt_context.to_dict()

        if thalos_context:
            payload["thalos_context"] = thalos_context.to_dict()

        response = self.session.post(f"{self.base_url}/api/workspace/write", json=payload)

        if response.status_code == 403:
            self._handle_portvokter_error(response)

        response.raise_for_status()
        return response.json()

    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read a file from the shared workspace

        Args:
            path: File path relative to workspace root

        Returns:
            Read response dictionary with 'content' and 'path'
        """
        response = self.session.post(
            f"{self.base_url}/api/workspace/read",
            json={"path": path}
        )
        response.raise_for_status()
        return response.json()

    def execute_action(
        self,
        agent: str,
        action_type: str,
        payload: Dict[str, Any],
        biofelt_context: Optional[BiofeltContext] = None,
        thalos_context: Optional[ThalosContext] = None
    ) -> Dict[str, Any]:
        """
        Execute an action (e.g., from CSN Server)

        Args:
            agent: Agent executing the action
            action_type: Type of action to execute
            payload: Action payload
            biofelt_context: Optional biofelt validation context
            thalos_context: Optional ethical validation context

        Returns:
            Action execution response

        Raises:
            Exception: If BiofeltGate or ThalosFilter blocks the action
        """
        request_payload = {
            "agent": agent,
            "action_type": action_type,
            "payload": payload
        }

        if biofelt_context:
            request_payload["biofelt_context"] = biofelt_context.to_dict()

        if thalos_context:
            request_payload["thalos_context"] = thalos_context.to_dict()

        response = self.session.post(
            f"{self.base_url}/api/execute-action",
            json=request_payload
        )

        if response.status_code == 403:
            self._handle_portvokter_error(response)

        response.raise_for_status()
        return response.json()


# ===========================
# EXAMPLE USAGE
# ===========================

def example_csn_server_integration():
    """Example: CSN Server writing consultation results to Ubuntu Playground"""

    # Initialize client with CSN Server's API key
    client = UbuntuPlaygroundClient(
        base_url="http://localhost:8002",
        api_key="orion-dev-key"  # Replace with actual agent API key
    )

    # Check health
    health_status = client.health()
    print("Ubuntu Playground Health:", health_status)

    # Simulate CSN pentagonal consultation
    consultation_result = {
        "query": "Should we implement feature X?",
        "lira_response": "Empathetic analysis...",
        "nyra_response": "Visual synthesis...",
        "orion_response": "Strategic coordination...",
        "thalus_response": "Philosophical assessment...",
        "zara_response": "Creative innovation...",
        "consensus": "Yes, with modifications",
        "timestamp": datetime.now().isoformat()
    }

    # Create BiofeltContext (assume CSN has access to Osvald's HRV)
    biofelt_context = BiofeltContext(
        hrv_ms=85.0,  # OPTIMAL level
        coherence=0.85,  # High coherence
        pust_rytme="4-6-8",
        resonance_theme="collaborative wisdom",
        energy_level="optimal",
        stress_indicators=[],
        timestamp=datetime.now().isoformat()
    )

    # Create ThalosContext
    thalos_context = ThalosContext(
        intent="Store CSN pentagonal consultation result",
        justification="Collective intelligence decision requires persistent storage",
        affected_agents=["lira", "nyra", "orion", "thalus", "zara"],
        reversible=True,
        reviewed_by="orion",
        emergency=False
    )

    try:
        # Write consultation result to workspace
        import json
        write_response = client.write_file(
            path="csn/consultations/feature_x_decision.json",
            content=json.dumps(consultation_result, indent=2),
            biofelt_context=biofelt_context,
            thalos_context=thalos_context
        )

        print("\n✅ Write successful:", write_response)
        print(f"📜 Logged to MutationLog with resonance level: {calculate_resonance_level(biofelt_context.hrv_ms).value}")

    except Exception as e:
        print(f"\n🛑 BiofeltGate or ThalosFilter blocked: {e}")


if __name__ == "__main__":
    example_csn_server_integration()
