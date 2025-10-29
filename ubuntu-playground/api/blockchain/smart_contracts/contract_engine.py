"""Contract Execution Engine - Phase 7: Smart Contract Portvokter"""

from typing import Dict, Any, List
from .base_contract import BaseContract, ContractResult, ContractViolation
from .biofelt_contract import BiofeltGateContract
from .thalos_contract import ThalosFilterContract
from .mutation_contract import MutationLogContract
import logging

logger = logging.getLogger(__name__)


class ContractEngine:
    """
    Contract execution engine for GENOMOS.

    Runs all three portvokter contracts and aggregates results.
    """

    def __init__(self):
        self.contracts: List[BaseContract] = [
            BiofeltGateContract(),
            ThalosFilterContract(),
            MutationLogContract()
        ]
        logger.info(f"🔐 Contract Engine initialized: {len(self.contracts)} contracts loaded")

    def validate_all(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all contracts and aggregate results.

        Args:
            data: Data to validate

        Returns:
            Aggregated validation results from all contracts
        """
        results = []
        all_violations = []
        all_valid = True

        for contract in self.contracts:
            try:
                result = contract.validate(data)
                results.append({
                    "contract": contract.contract_name,
                    "version": contract.version,
                    "valid": result.valid,
                    "violations": [v.dict() for v in result.violations],
                    "metadata": result.metadata
                })

                # Aggregate violations
                all_violations.extend(result.violations)

                # If any contract fails, overall fails
                if not result.valid:
                    all_valid = False

            except Exception as e:
                logger.error(f"Contract {contract.contract_name} failed: {str(e)}")
                results.append({
                    "contract": contract.contract_name,
                    "version": contract.version,
                    "valid": False,
                    "error": str(e)
                })
                all_valid = False

        # Count by severity
        severity_counts = {"error": 0, "warning": 0, "info": 0}
        for violation in all_violations:
            severity_counts[violation.severity] = severity_counts.get(violation.severity, 0) + 1

        return {
            "overall_valid": all_valid,
            "total_violations": len(all_violations),
            "severity_counts": severity_counts,
            "contracts": results
        }

    def validate_by_contract(self, contract_name: str, data: Dict[str, Any]) -> ContractResult:
        """
        Run a specific contract by name.

        Args:
            contract_name: Name of contract to run
            data: Data to validate

        Returns:
            Contract validation result
        """
        for contract in self.contracts:
            if contract.contract_name.lower() == contract_name.lower():
                return contract.validate(data)

        raise ValueError(f"Contract not found: {contract_name}")

    def get_contracts_info(self) -> List[Dict[str, Any]]:
        """Get information about all loaded contracts."""
        return [
            {
                "name": contract.contract_name,
                "version": contract.version,
                "type": contract.__class__.__name__
            }
            for contract in self.contracts
        ]
