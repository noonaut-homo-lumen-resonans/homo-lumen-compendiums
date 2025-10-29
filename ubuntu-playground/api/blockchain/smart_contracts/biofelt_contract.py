"""BiofeltGate Smart Contract - Portvokter #1"""

from typing import Dict, Any, List
from .base_contract import BaseContract, ContractResult, ContractViolation


class BiofeltGateContract(BaseContract):
    """
    BiofeltGate: Emotional and physiological validation.

    Rules:
    - HRV must be within safe range (30-150 ms)
    - Emotional state required for consultations
    - Stress level warnings
    """

    def __init__(self):
        super().__init__(contract_name="BiofeltGate", version="1.0")

    def validate(self, data: Dict[str, Any]) -> ContractResult:
        violations: List[ContractViolation] = []

        # Rule BF-001: HRV range validation
        hrv = data.get("hrv_ms")
        if hrv is not None:
            if hrv < 30:
                violations.append(self._create_violation(
                    rule_id="BF-001",
                    severity="error",
                    message="HRV too low - physiological stress detected",
                    field="hrv_ms",
                    actual_value=hrv,
                    expected_value="≥ 30 ms"
                ))
            elif hrv > 150:
                violations.append(self._create_violation(
                    rule_id="BF-001",
                    severity="warning",
                    message="HRV unusually high - verify sensor",
                    field="hrv_ms",
                    actual_value=hrv,
                    expected_value="≤ 150 ms"
                ))

        # Rule BF-002: Emotional state required for consultations
        if data.get("operation_type") == "consultation":
            if not data.get("emotional_state"):
                violations.append(self._create_violation(
                    rule_id="BF-002",
                    severity="error",
                    message="Emotional state required for consultations",
                    field="emotional_state"
                ))

        # Rule BF-003: Stress level warning
        stress = data.get("stress_level", 0)
        if stress > 7:
            violations.append(self._create_violation(
                rule_id="BF-003",
                severity="warning",
                message="High stress detected - consider rest before proceeding",
                field="stress_level",
                actual_value=stress,
                expected_value="≤ 7"
            ))

        return self._create_result(violations, metadata={"hrv_ms": hrv, "stress_level": stress})
