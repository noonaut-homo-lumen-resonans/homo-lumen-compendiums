"""MutationLog Smart Contract - Portvokter #3"""

from typing import Dict, Any, List
from .base_contract import BaseContract, ContractResult, ContractViolation


class MutationLogContract(BaseContract):
    """
    MutationLog: Operation validation and safety checks.

    Rules:
    - Operation must have required fields
    - Destructive operations require confirmation
    - File path validation
    """

    def __init__(self):
        super().__init__(contract_name="MutationLog", version="1.0")
        self.destructive_operations = ["delete", "overwrite", "replace_all"]

    def validate(self, data: Dict[str, Any]) -> ContractResult:
        violations: List[ContractViolation] = []

        # Rule ML-001: Required mutation fields
        if data.get("operation_type") == "mutation":
            required_fields = ["mutation_id", "operation", "target"]
            missing = [f for f in required_fields if not data.get(f)]
            if missing:
                violations.append(self._create_violation(
                    rule_id="ML-001",
                    severity="error",
                    message=f"Missing required mutation fields: {', '.join(missing)}",
                    field="mutation_data"
                ))

        # Rule ML-002: Destructive operation confirmation
        operation = data.get("operation", "")
        if any(destr in operation.lower() for destr in self.destructive_operations):
            if not data.get("confirmed", False):
                violations.append(self._create_violation(
                    rule_id="ML-002",
                    severity="error",
                    message=f"Destructive operation '{operation}' requires explicit confirmation",
                    field="confirmed",
                    actual_value=False,
                    expected_value=True
                ))

        # Rule ML-003: File path safety
        target = data.get("target", "")
        dangerous_paths = ["../", "..\\", "/etc/", "C:\\Windows", "system32"]
        if any(danger in target for danger in dangerous_paths):
            violations.append(self._create_violation(
                rule_id="ML-003",
                severity="error",
                message=f"Dangerous file path detected: {target}",
                field="target",
                actual_value=target
            ))

        # Rule ML-004: Success validation
        if data.get("operation_type") == "mutation":
            if data.get("success") is False:
                violations.append(self._create_violation(
                    rule_id="ML-004",
                    severity="warning",
                    message="Failed mutation logged - review and retry",
                    field="success"
                ))

        return self._create_result(violations, metadata={"operation": operation, "target": target})
