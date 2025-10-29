"""
Base Smart Contract - Phase 7: Smart Contract Portvokter

Base class for all GENOMOS smart contracts with validation logic.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ContractViolation(BaseModel):
    """Represents a contract rule violation"""
    rule_id: str
    severity: str  # "error", "warning", "info"
    message: str
    field: Optional[str] = None
    actual_value: Optional[Any] = None
    expected_value: Optional[Any] = None


class ContractResult(BaseModel):
    """Result of contract validation"""
    valid: bool
    contract_name: str
    violations: List[ContractViolation]
    metadata: Dict[str, Any] = {}
    timestamp: str = datetime.now().isoformat()


class BaseContract(ABC):
    """
    Base class for all smart contracts.

    Smart contracts encode immutable rules that must be enforced
    before operations are committed to the blockchain.
    """

    def __init__(self, contract_name: str, version: str = "1.0"):
        self.contract_name = contract_name
        self.version = version
        self.logger = logging.getLogger(f"contract.{contract_name}")

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> ContractResult:
        """
        Validate data against contract rules.

        Args:
            data: Data to validate

        Returns:
            ContractResult with validation outcome
        """
        pass

    def _create_violation(
        self,
        rule_id: str,
        severity: str,
        message: str,
        field: Optional[str] = None,
        actual_value: Optional[Any] = None,
        expected_value: Optional[Any] = None
    ) -> ContractViolation:
        """Helper to create contract violations"""
        return ContractViolation(
            rule_id=rule_id,
            severity=severity,
            message=message,
            field=field,
            actual_value=actual_value,
            expected_value=expected_value
        )

    def _create_result(
        self,
        violations: List[ContractViolation],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContractResult:
        """Helper to create contract results"""
        # Contract is valid only if no error-level violations
        valid = not any(v.severity == "error" for v in violations)

        return ContractResult(
            valid=valid,
            contract_name=self.contract_name,
            violations=violations,
            metadata=metadata or {},
            timestamp=datetime.now().isoformat()
        )
