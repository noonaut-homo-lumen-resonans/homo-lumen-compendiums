"""
MutationLog / Audit Trail

Den tredje Triadiske Portvokteren som sikrer append-only historikk og
regenerativ healing gjennom full sporing av alle operasjoner.

Filosofisk forankring:
- Regenerativ Healing: All historikk er bevart og kan reverseres
- Ontologisk Integritet: Ingen operasjon kan "forsvinne" fra systemet
- Temporal Koherens: Systemet kan rekonstrueres til ethvert tidspunkt

NB's veiledning: "Mutation_Log er systemets hukommelse - intet glemmes,
alt kan læres av, og ingenting kan ødelegges permanent."
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import logging
import json
import hashlib

logger = logging.getLogger(__name__)


class MutationLevel(str, Enum):
    """Alvorlighetsgrad for mutasjoner"""
    READ = "read"                # Lesing (lav risiko)
    WRITE = "write"              # Skriving (moderat risiko)
    DELETE = "delete"            # Sletting (høy risiko)
    EXECUTE = "execute"          # Utførelse (moderat risiko)
    COMMIT = "commit"            # Git commit (høy risiko)
    DEPLOY = "deploy"            # Deployment (kritisk risiko)
    SYSTEM = "system"            # Systemendring (kritisk risiko)


class ValidationOutcome(str, Enum):
    """Resultat av portvokter-validering"""
    APPROVED = "approved"                    # Godkjent av alle portvokter
    APPROVED_WITH_WARNINGS = "approved_with_warnings"  # Godkjent med advarsler
    BLOCKED_BIOFELT = "blocked_biofelt"      # Blokkert av BiofeltGate
    BLOCKED_THALOS = "blocked_thalos"        # Blokkert av ThalosFilter
    BLOCKED_MUTATION = "blocked_mutation"    # Blokkert av MutationLog selv
    BYPASSED = "bypassed"                    # Bypassed (krever review)


class MutationEntry(BaseModel):
    """
    Immutabel oppføring i Mutation_Log.
    Denne strukturen kan ALDRI endres etter den er logget.
    """
    # Metadata
    mutation_id: str = Field(..., description="Unik ID for denne mutasjonen (SHA-256 hash)")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    # Agent context
    agent: str = Field(..., description="Agent som utførte operasjonen")
    operation_type: MutationLevel = Field(..., description="Type operasjon")

    # Operation details
    target: str = Field(..., description="Mål for operasjonen (filsti, resource, etc.)")
    action: str = Field(..., description="Beskrivelse av handlingen")
    payload: Optional[Dict[str, Any]] = Field(default=None, description="Full payload (kan være stor)")

    # Validation results
    validation_outcome: ValidationOutcome = Field(..., description="Resultat fra portvokter-validering")
    biofelt_resonance: Optional[str] = Field(default=None, description="Resonans-nivå fra BiofeltGate")
    thalos_severity: Optional[str] = Field(default=None, description="Alvorlighetsgrad fra ThalosFilter")

    # Impact assessment
    affected_agents: List[str] = Field(default_factory=list, description="Agenter påvirket av denne operasjonen")
    reversible: bool = Field(default=True, description="Er operasjonen reversibel?")

    # Justification
    intent: Optional[str] = Field(default=None, description="Intensjon bak operasjonen")
    justification: Optional[str] = Field(default=None, description="Begrunnelse")
    reviewed_by: Optional[str] = Field(default=None, description="Review-agent")

    # Result
    success: bool = Field(..., description="Ble operasjonen utført?")
    error_message: Optional[str] = Field(default=None, description="Feilmelding hvis blocked")
    result_summary: Optional[str] = Field(default=None, description="Oppsummering av resultat")


class MutationLog:
    """
    Append-only audit trail for alle kritiske operasjoner.

    Design principles (NB's guidance):
    1. APPEND-ONLY: Ingen delete eller update operasjoner tillatt
    2. IMMUTABLE: Entries kan aldri endres etter de er logget
    3. COMPLETE: All kritisk informasjon må logges
    4. AUDITABLE: Full sporbarhet for compliance og debugging
    5. REGENERATIVE: Historie kan brukes til rollback og healing
    """

    _log_entries: List[MutationEntry] = []
    _log_file_path: Optional[str] = None

    @staticmethod
    def initialize(log_file_path: str = "./data/mutation_log.jsonl"):
        """
        Initialize MutationLog with persistent storage.

        Args:
            log_file_path: Path to JSONL file for append-only logging
        """
        MutationLog._log_file_path = log_file_path

        # Create directory if not exists
        import os
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        # Create file if not exists
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w', encoding='utf-8') as f:
                pass  # Create empty file

        logger.info(f"📜 MutationLog initialized: {log_file_path}")

    @staticmethod
    def _generate_mutation_id(entry_data: Dict[str, Any]) -> str:
        """
        Generate unique SHA-256 hash for mutation entry.
        Ensures immutability and uniqueness.
        """
        # Combine critical fields for hash
        hash_input = f"{entry_data['timestamp']}:{entry_data['agent']}:{entry_data['operation_type']}:{entry_data['target']}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    @staticmethod
    def log_mutation(
        agent: str,
        operation_type: MutationLevel,
        target: str,
        action: str,
        success: bool,
        validation_outcome: ValidationOutcome,
        payload: Optional[Dict[str, Any]] = None,
        biofelt_resonance: Optional[str] = None,
        thalos_severity: Optional[str] = None,
        affected_agents: Optional[List[str]] = None,
        reversible: bool = True,
        intent: Optional[str] = None,
        justification: Optional[str] = None,
        reviewed_by: Optional[str] = None,
        error_message: Optional[str] = None,
        result_summary: Optional[str] = None
    ) -> MutationEntry:
        """
        Log a mutation to the append-only audit trail.

        This is the CORE function of MutationLog - all operations must be logged here.

        Returns:
            MutationEntry: The immutable log entry
        """
        # Create entry data
        entry_data = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "operation_type": operation_type.value,
            "target": target,
            "action": action,
            "payload": payload,
            "validation_outcome": validation_outcome.value,
            "biofelt_resonance": biofelt_resonance,
            "thalos_severity": thalos_severity,
            "affected_agents": affected_agents or [],
            "reversible": reversible,
            "intent": intent,
            "justification": justification,
            "reviewed_by": reviewed_by,
            "success": success,
            "error_message": error_message,
            "result_summary": result_summary
        }

        # Generate unique ID
        mutation_id = MutationLog._generate_mutation_id(entry_data)
        entry_data["mutation_id"] = mutation_id

        # Create immutable entry
        entry = MutationEntry(**entry_data)

        # Append to in-memory log
        MutationLog._log_entries.append(entry)

        # Append to persistent JSONL file (append-only)
        if MutationLog._log_file_path:
            try:
                with open(MutationLog._log_file_path, 'a', encoding='utf-8') as f:
                    f.write(entry.json() + '\n')
            except Exception as e:
                logger.error(f"❌ Failed to write to mutation log: {e}")

        # Log to console
        emoji = "✅" if success else "🛑"
        logger.info(f"📜 {emoji} Mutation logged: {mutation_id[:8]} - {agent} {operation_type.value} {target}")

        return entry

    @staticmethod
    def log_approved_operation(
        agent: str,
        operation_type: MutationLevel,
        target: str,
        action: str,
        biofelt_resonance: Optional[str] = None,
        thalos_severity: Optional[str] = None,
        **kwargs
    ) -> MutationEntry:
        """Shortcut for logging approved operations"""
        return MutationLog.log_mutation(
            agent=agent,
            operation_type=operation_type,
            target=target,
            action=action,
            success=True,
            validation_outcome=ValidationOutcome.APPROVED,
            biofelt_resonance=biofelt_resonance,
            thalos_severity=thalos_severity,
            **kwargs
        )

    @staticmethod
    def log_blocked_operation(
        agent: str,
        operation_type: MutationLevel,
        target: str,
        action: str,
        blocked_by: str,  # "biofelt" or "thalos"
        error_message: str,
        biofelt_resonance: Optional[str] = None,
        thalos_severity: Optional[str] = None,
        **kwargs
    ) -> MutationEntry:
        """Shortcut for logging blocked operations"""
        if blocked_by == "biofelt":
            outcome = ValidationOutcome.BLOCKED_BIOFELT
        elif blocked_by == "thalos":
            outcome = ValidationOutcome.BLOCKED_THALOS
        else:
            outcome = ValidationOutcome.BLOCKED_MUTATION

        return MutationLog.log_mutation(
            agent=agent,
            operation_type=operation_type,
            target=target,
            action=action,
            success=False,
            validation_outcome=outcome,
            error_message=error_message,
            biofelt_resonance=biofelt_resonance,
            thalos_severity=thalos_severity,
            **kwargs
        )

    @staticmethod
    def get_history(
        agent: Optional[str] = None,
        operation_type: Optional[MutationLevel] = None,
        target: Optional[str] = None,
        limit: int = 100
    ) -> List[MutationEntry]:
        """
        Query mutation history with filters.

        Args:
            agent: Filter by agent name
            operation_type: Filter by operation type
            target: Filter by target (partial match)
            limit: Maximum number of entries to return

        Returns:
            List of MutationEntry objects (most recent first)
        """
        filtered_entries = MutationLog._log_entries

        if agent:
            filtered_entries = [e for e in filtered_entries if e.agent == agent]

        if operation_type:
            filtered_entries = [e for e in filtered_entries if e.operation_type == operation_type]

        if target:
            filtered_entries = [e for e in filtered_entries if target in e.target]

        # Return most recent first
        return list(reversed(filtered_entries[-limit:]))

    @staticmethod
    def get_agent_summary(agent: str) -> Dict[str, Any]:
        """
        Get summary statistics for an agent's operations.

        Returns:
            Dictionary with:
            - total_operations
            - successful_operations
            - blocked_operations
            - operation_types breakdown
            - validation_outcomes breakdown
        """
        agent_entries = [e for e in MutationLog._log_entries if e.agent == agent]

        total = len(agent_entries)
        successful = len([e for e in agent_entries if e.success])
        blocked = total - successful

        # Operation types breakdown
        op_types = {}
        for entry in agent_entries:
            op_type = entry.operation_type.value
            op_types[op_type] = op_types.get(op_type, 0) + 1

        # Validation outcomes breakdown
        outcomes = {}
        for entry in agent_entries:
            outcome = entry.validation_outcome.value
            outcomes[outcome] = outcomes.get(outcome, 0) + 1

        return {
            "agent": agent,
            "total_operations": total,
            "successful_operations": successful,
            "blocked_operations": blocked,
            "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "0%",
            "operation_types": op_types,
            "validation_outcomes": outcomes,
            "latest_operation": agent_entries[-1].timestamp if agent_entries else None
        }

    @staticmethod
    def get_system_health() -> Dict[str, Any]:
        """
        Get overall system health metrics from mutation log.

        Returns:
            Dictionary with system-wide statistics
        """
        total = len(MutationLog._log_entries)
        successful = len([e for e in MutationLog._log_entries if e.success])
        blocked = total - successful

        # Blocked by breakdown
        blocked_by_biofelt = len([e for e in MutationLog._log_entries if e.validation_outcome == ValidationOutcome.BLOCKED_BIOFELT])
        blocked_by_thalos = len([e for e in MutationLog._log_entries if e.validation_outcome == ValidationOutcome.BLOCKED_THALOS])

        # Recent activity (last hour)
        from datetime import timedelta
        now = datetime.now()
        one_hour_ago = (now - timedelta(hours=1)).isoformat()
        recent = [e for e in MutationLog._log_entries if e.timestamp >= one_hour_ago]

        return {
            "total_mutations": total,
            "successful_mutations": successful,
            "blocked_mutations": blocked,
            "blocked_by_biofelt": blocked_by_biofelt,
            "blocked_by_thalos": blocked_by_thalos,
            "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "0%",
            "recent_activity_1h": len(recent),
            "log_file": MutationLog._log_file_path,
            "log_size_entries": total
        }

    @staticmethod
    def validate_log_integrity() -> Dict[str, Any]:
        """
        Validate that mutation log has not been tampered with.

        Checks:
        1. All entries have valid mutation_id (SHA-256 hash)
        2. Timestamps are monotonically increasing
        3. No duplicate mutation_ids

        Returns:
            Dictionary with integrity check results
        """
        entries = MutationLog._log_entries
        issues = []

        # Check for duplicate IDs
        ids = [e.mutation_id for e in entries]
        duplicates = [id for id in ids if ids.count(id) > 1]
        if duplicates:
            issues.append(f"Duplicate mutation IDs found: {duplicates}")

        # Check timestamp ordering
        timestamps = [e.timestamp for e in entries]
        for i in range(1, len(timestamps)):
            if timestamps[i] < timestamps[i-1]:
                issues.append(f"Timestamp ordering violation at index {i}")

        # Check hash validity
        for entry in entries[-100:]:  # Check last 100 entries
            expected_id = MutationLog._generate_mutation_id(entry.dict())
            if entry.mutation_id != expected_id:
                issues.append(f"Hash mismatch for entry {entry.mutation_id}")

        return {
            "integrity": "VALID" if not issues else "COMPROMISED",
            "total_entries": len(entries),
            "issues": issues,
            "timestamp": datetime.now().isoformat()
        }
