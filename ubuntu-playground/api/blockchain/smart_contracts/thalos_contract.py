"""ThalosFilter Smart Contract - Portvokter #2"""

from typing import Dict, Any, List
from .base_contract import BaseContract, ContractResult, ContractViolation


class ThalosFilterContract(BaseContract):
    """
    ThalosFilter: Wisdom and context validation.

    Rules:
    - SMK references must exist
    - Related consultations must be linked
    - Knowledge coherence validation
    """

    def __init__(self):
        super().__init__(contract_name="ThalosFilter", version="1.0")

    def validate(self, data: Dict[str, Any]) -> ContractResult:
        violations: List[ContractViolation] = []

        # Rule TF-001: SMK reference validation
        related_smk = data.get("related_smk", [])
        if data.get("operation_type") in ["consultation", "agent_learning"]:
            if not related_smk:
                violations.append(self._create_violation(
                    rule_id="TF-001",
                    severity="warning",
                    message="No SMK references - consider linking relevant knowledge",
                    field="related_smk"
                ))

        # Rule TF-002: SMK format validation
        for smk_ref in related_smk:
            if not (smk_ref.startswith("SMK#") or smk_ref.startswith("SMK_")):
                violations.append(self._create_violation(
                    rule_id="TF-002",
                    severity="error",
                    message=f"Invalid SMK reference format: {smk_ref}",
                    field="related_smk",
                    actual_value=smk_ref,
                    expected_value="SMK#XXX or SMK_XXX"
                ))

        # Rule TF-003: Context completeness
        if data.get("operation_type") == "consultation":
            required_fields = ["human_query", "agent_responses"]
            missing = [f for f in required_fields if not data.get(f)]
            if missing:
                violations.append(self._create_violation(
                    rule_id="TF-003",
                    severity="error",
                    message=f"Missing required consultation fields: {', '.join(missing)}",
                    field="consultation_data"
                ))

        # Rule TF-004: Agent participation validation
        if data.get("operation_type") == "consultation":
            agent_responses = data.get("agent_responses", {})
            if len(agent_responses) < 2:
                violations.append(self._create_violation(
                    rule_id="TF-004",
                    severity="warning",
                    message="Consultation requires at least 2 agent perspectives for collective wisdom",
                    field="agent_responses",
                    actual_value=len(agent_responses),
                    expected_value="≥ 2"
                ))

        return self._create_result(violations, metadata={"smk_count": len(related_smk)})
