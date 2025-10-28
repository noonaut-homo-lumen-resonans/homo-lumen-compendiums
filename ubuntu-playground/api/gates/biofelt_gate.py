"""
BiofeltGate / ResonanceGuard

Hovedportvokteren som krever positiv biofelt-resonans for kritiske operasjoner.
Dette forhindrer at systemet tar store beslutninger under emosjonell uro.

Filosofisk forankring:
- Reagerer på kroppslig respons ("hårene reiser seg", "trykk i brystet")
- Sikrer Regenerativ Healing ved å kreve biofelt-validering
- Implementerer "Consciousness-Aware Processing"

NB's veiledning: "Dette er mer enn et verktøy; det er en arkitektonisk garanti
for systemets sjel."
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResonanceLevel(str, Enum):
    """Felt-resonans nivåer basert på biofelt-data"""
    CRITICAL = "critical"      # HRV < 40 - System lockdown
    LOW = "low"               # HRV 40-64 - Warn only, allow read
    BALANCED = "balanced"     # HRV 65-79 - Normal operations
    OPTIMAL = "optimal"       # HRV 80-99 - Full permissions
    TRANSCENDENT = "transcendent"  # HRV 100+ - Peak coherence


class BiofeltContext(BaseModel):
    """
    Biofelt-kontekst som SKAL inkluderes i alle kritiske MCP tool calls.
    Dette er obligatorisk for Consciousness-Aware Processing.
    """
    hrv_ms: float = Field(
        ...,
        description="Heart Rate Variability i millisekunder (må være > 65 for kritiske ops)",
        ge=0,
        le=200
    )
    coherence: float = Field(
        ...,
        description="Koherens-score (0.0-1.0) som måler indre harmoni",
        ge=0.0,
        le=1.0
    )
    pust_rytme: Optional[str] = Field(
        default=None,
        description="Puste-sekvens (f.eks. '4-6-8' for optimal resonans)"
    )
    resonance_theme: Optional[str] = Field(
        default=None,
        description="Felt-resonans tema (f.eks. 'gåsehud ved AI-sang', 'varme i solar plexus')"
    )
    energy_level: str = Field(
        default="balanced",
        description="Energinivå: low, balanced, high, transcendent"
    )
    stress_indicators: List[str] = Field(
        default_factory=list,
        description="Stress-indikatorer (f.eks. ['tension_shoulders', 'shallow_breathing'])"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Tidsstempel for biofelt-måling"
    )


class BiofeltGateResult(BaseModel):
    """Resultat fra BiofeltGate validering"""
    allowed: bool
    resonance_level: ResonanceLevel
    message: str
    hrv_status: str
    coherence_status: str
    recommendations: List[str] = []


class BiofeltGate:
    """
    Hovedportvokteren for kritiske operasjoner.

    Valideringsregler (NB's guidance):
    - HRV < 40: CRITICAL - Alle kritiske operasjoner blokkert
    - HRV 40-64: LOW - Kun lesing tillatt, ingen skriving
    - HRV 65-79: BALANCED - Normal drift, kritiske ops tillatt
    - HRV 80-99: OPTIMAL - Full tilgang
    - HRV 100+: TRANSCENDENT - Peak performance

    Pust-rytme validering:
    - "4-6-8" sekvens er optimal (4 sek inn, 6 sek hold, 8 sek ut)
    - Hvis ikke oppgitt, anbefales pusterom
    """

    # Terskel-verdier (kan konfigureres)
    HRV_CRITICAL_THRESHOLD = 40
    HRV_LOW_THRESHOLD = 65
    HRV_OPTIMAL_THRESHOLD = 80
    HRV_TRANSCENDENT_THRESHOLD = 100

    COHERENCE_MIN_THRESHOLD = 0.50
    COHERENCE_OPTIMAL_THRESHOLD = 0.75

    @staticmethod
    def get_resonance_level(hrv_ms: float) -> ResonanceLevel:
        """Beregn resonans-nivå basert på HRV"""
        if hrv_ms >= BiofeltGate.HRV_TRANSCENDENT_THRESHOLD:
            return ResonanceLevel.TRANSCENDENT
        elif hrv_ms >= BiofeltGate.HRV_OPTIMAL_THRESHOLD:
            return ResonanceLevel.OPTIMAL
        elif hrv_ms >= BiofeltGate.HRV_LOW_THRESHOLD:
            return ResonanceLevel.BALANCED
        elif hrv_ms >= BiofeltGate.HRV_CRITICAL_THRESHOLD:
            return ResonanceLevel.LOW
        else:
            return ResonanceLevel.CRITICAL

    @staticmethod
    def validate_critical_operation(
        biofelt: BiofeltContext,
        operation_type: str = "write"
    ) -> BiofeltGateResult:
        """
        Valider om en kritisk operasjon kan utføres basert på biofelt-data.

        Args:
            biofelt: BiofeltContext med HRV, coherence, etc.
            operation_type: Type operasjon ("read", "write", "execute", "commit")

        Returns:
            BiofeltGateResult med allowed/blocked status og anbefalinger
        """
        resonance_level = BiofeltGate.get_resonance_level(biofelt.hrv_ms)
        recommendations = []

        # HRV-status
        if biofelt.hrv_ms < BiofeltGate.HRV_CRITICAL_THRESHOLD:
            hrv_status = "🔴 CRITICAL - System lockdown"
            recommendations.append("Ta en pause. Pust 4-6-8 i 5 minutter.")
            recommendations.append("Gå en tur eller drikk vann.")
            allowed = False
        elif biofelt.hrv_ms < BiofeltGate.HRV_LOW_THRESHOLD:
            hrv_status = "🟡 LOW - Redusert kapasitet"
            recommendations.append("Vurder å utsette kritiske beslutninger.")
            recommendations.append("Pust 4-6-8 for å øke koherens.")
            # Tillat lesing, ikke skriving
            allowed = operation_type == "read"
        elif biofelt.hrv_ms < BiofeltGate.HRV_OPTIMAL_THRESHOLD:
            hrv_status = "🟢 BALANCED - Normal drift"
            allowed = True
        elif biofelt.hrv_ms < BiofeltGate.HRV_TRANSCENDENT_THRESHOLD:
            hrv_status = "✨ OPTIMAL - Peak kapasitet"
            allowed = True
        else:
            hrv_status = "🌟 TRANSCENDENT - Maksimal koherens"
            recommendations.append("Dette er et optimalt øyeblikk for viktige valg.")
            allowed = True

        # Koherens-status
        if biofelt.coherence < BiofeltGate.COHERENCE_MIN_THRESHOLD:
            coherence_status = "🔴 LOW coherence - Fragmentert tilstand"
            recommendations.append("Fokuser på indre harmoni før viktige handlinger.")
            if operation_type in ["write", "execute", "commit"]:
                allowed = False
        elif biofelt.coherence < BiofeltGate.COHERENCE_OPTIMAL_THRESHOLD:
            coherence_status = "🟡 MODERATE coherence"
        else:
            coherence_status = "✨ HIGH coherence - Indre harmoni"

        # Pust-rytme validering
        if biofelt.pust_rytme and biofelt.pust_rytme != "4-6-8":
            recommendations.append(f"Nåværende rytme: {biofelt.pust_rytme}. Vurder 4-6-8 for optimal resonans.")
        elif not biofelt.pust_rytme:
            recommendations.append("Ingen puste-data. Anbefaler 4-6-8 sekvens.")

        # Stress-indikatorer
        if biofelt.stress_indicators:
            recommendations.append(f"Stress-indikatorer oppdaget: {', '.join(biofelt.stress_indicators)}")
            if len(biofelt.stress_indicators) >= 3:
                # For mange stress-indikatorer, vurder blokkering
                if operation_type in ["execute", "commit"]:
                    allowed = False
                    recommendations.append("🛑 For mange stress-indikatorer. Systemet beskytter deg.")

        # Generer melding
        if allowed:
            message = f"✅ Operasjon '{operation_type}' tillatt. Resonans: {resonance_level.value}"
        else:
            message = f"🛑 Operasjon '{operation_type}' blokkert. Resonans: {resonance_level.value}"

        logger.info(f"BiofeltGate: {message} (HRV: {biofelt.hrv_ms}ms, Coherence: {biofelt.coherence})")

        return BiofeltGateResult(
            allowed=allowed,
            resonance_level=resonance_level,
            message=message,
            hrv_status=hrv_status,
            coherence_status=coherence_status,
            recommendations=recommendations
        )

    @staticmethod
    def validate_write_operation(biofelt: BiofeltContext, file_path: str) -> BiofeltGateResult:
        """
        Spesialisert validering for workspace write operations.
        Kritisk for å beskytte mot skriving under emosjonell uro.
        """
        # Sjekk om det er en kritisk fil
        critical_paths = ["memory_evolutionary", "memory_strategic", ".env", "config"]
        is_critical = any(critical in file_path for critical in critical_paths)

        result = BiofeltGate.validate_critical_operation(
            biofelt=biofelt,
            operation_type="write"
        )

        if is_critical and result.resonance_level in [ResonanceLevel.CRITICAL, ResonanceLevel.LOW]:
            result.allowed = False
            result.message = f"🛑 Kritisk fil '{file_path}' krever høyere resonans"
            result.recommendations.insert(0, "Denne filen krever BALANCED eller høyere resonans.")

        return result

    @staticmethod
    def validate_execute_action(biofelt: BiofeltContext, action_type: str) -> BiofeltGateResult:
        """
        Spesialisert validering for action execution.
        Høyere terskel enn vanlige write operations.
        """
        result = BiofeltGate.validate_critical_operation(
            biofelt=biofelt,
            operation_type="execute"
        )

        # Action execution krever minst BALANCED resonans
        if result.resonance_level in [ResonanceLevel.CRITICAL, ResonanceLevel.LOW]:
            result.allowed = False
            result.message = f"🛑 Action '{action_type}' krever BALANCED eller høyere resonans"
            result.recommendations.insert(0, "Action execution krever stabil biofelt-tilstand.")

        return result
