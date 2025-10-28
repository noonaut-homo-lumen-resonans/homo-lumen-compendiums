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
import os

logger = logging.getLogger(__name__)

# GENOMOS blockchain integration
try:
    from blockchain.agent_dna_chain import AgentDNAChain
    from blockchain.dna_block import GeneType
    BLOCKCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ GENOMOS blockchain not available - mutations will only be logged to JSONL")
    BLOCKCHAIN_AVAILABLE = False
    AgentDNAChain = None
    GeneType = None


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

    GENOMOS Integration:
    - All mutations are stored as MUTATION genes in the blockchain
    - Dual persistence: JSONL (legacy) + Blockchain (DNA)
    - Blockchain provides cryptographic verification and Merkle tree integrity
    """

    _log_entries: List[MutationEntry] = []
    _log_file_path: Optional[str] = None
    _blockchain: Optional['AgentDNAChain'] = None

    @staticmethod
    def initialize(log_file_path: str = "./data/mutation_log.jsonl", blockchain_db_path: Optional[str] = None):
        """
        Initialize MutationLog with dual persistent storage (JSONL + Blockchain).

        Args:
            log_file_path: Path to JSONL file for append-only logging (legacy)
            blockchain_db_path: Path to SQLite blockchain database (GENOMOS)
        """
        MutationLog._log_file_path = log_file_path

        # Create directory if not exists
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        # Create JSONL file if not exists
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w', encoding='utf-8') as f:
                pass  # Create empty file

        logger.info(f"📜 MutationLog initialized: {log_file_path}")

        # Initialize GENOMOS blockchain if available
        if BLOCKCHAIN_AVAILABLE and AgentDNAChain:
            try:
                if blockchain_db_path is None:
                    blockchain_db_path = "./data/genomos.db"

                MutationLog._blockchain = AgentDNAChain(db_path=blockchain_db_path)
                logger.info(f"🧬 GENOMOS blockchain initialized: {blockchain_db_path}")
                logger.info(f"🧬 Total genes in chain: {len(MutationLog._blockchain.chain)}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize GENOMOS blockchain: {e}")
                MutationLog._blockchain = None
        else:
            logger.info("📜 Running without GENOMOS blockchain (JSONL only)")

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

        # Append to GENOMOS blockchain (DNA persistence)
        if MutationLog._blockchain and GeneType:
            try:
                # Prepare mutation data for blockchain
                mutation_gene_data = {
                    "type": "mutation_log_entry",
                    "mutation_id": mutation_id,
                    "agent": agent,
                    "operation_type": operation_type.value,
                    "target": target,
                    "action": action,
                    "success": success,
                    "validation_outcome": validation_outcome.value,
                    "biofelt_resonance": biofelt_resonance,
                    "thalos_severity": thalos_severity,
                    "affected_agents": affected_agents or [],
                    "reversible": reversible,
                    "intent": intent,
                    "justification": justification,
                    "reviewed_by": reviewed_by,
                    "error_message": error_message,
                    "result_summary": result_summary,
                    "timestamp": entry.timestamp
                }

                # Add to blockchain as MUTATION gene
                block = MutationLog._blockchain.add_gene(
                    gene_type=GeneType.MUTATION,
                    data=mutation_gene_data,
                    agent=agent.lower(),
                    tags=["mutation", operation_type.value, validation_outcome.value]
                )

                logger.debug(f"🧬 Mutation added to blockchain: Block {block.index}")
            except Exception as e:
                logger.error(f"❌ Failed to write mutation to blockchain: {e}")
                # Non-fatal: continue even if blockchain write fails

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
    def migrate_jsonl_to_blockchain(jsonl_file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Migrate historical mutations from JSONL file to GENOMOS blockchain.

        This is a one-time migration function to populate the blockchain with
        existing mutation log entries.

        Args:
            jsonl_file_path: Path to JSONL file (defaults to _log_file_path)

        Returns:
            Dictionary with migration statistics
        """
        if not BLOCKCHAIN_AVAILABLE or not MutationLog._blockchain:
            return {
                "success": False,
                "error": "GENOMOS blockchain not available",
                "migrated": 0
            }

        if jsonl_file_path is None:
            jsonl_file_path = MutationLog._log_file_path

        if not jsonl_file_path or not os.path.exists(jsonl_file_path):
            return {
                "success": False,
                "error": f"JSONL file not found: {jsonl_file_path}",
                "migrated": 0
            }

        logger.info(f"🧬 Starting JSONL→Blockchain migration: {jsonl_file_path}")

        migrated_count = 0
        errors = []

        try:
            with open(jsonl_file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        # Parse JSONL entry
                        entry_dict = json.loads(line.strip())

                        # Prepare mutation data for blockchain
                        mutation_gene_data = {
                            "type": "mutation_log_entry",
                            "mutation_id": entry_dict.get("mutation_id"),
                            "agent": entry_dict.get("agent"),
                            "operation_type": entry_dict.get("operation_type"),
                            "target": entry_dict.get("target"),
                            "action": entry_dict.get("action"),
                            "success": entry_dict.get("success"),
                            "validation_outcome": entry_dict.get("validation_outcome"),
                            "biofelt_resonance": entry_dict.get("biofelt_resonance"),
                            "thalos_severity": entry_dict.get("thalos_severity"),
                            "affected_agents": entry_dict.get("affected_agents", []),
                            "reversible": entry_dict.get("reversible", True),
                            "intent": entry_dict.get("intent"),
                            "justification": entry_dict.get("justification"),
                            "reviewed_by": entry_dict.get("reviewed_by"),
                            "error_message": entry_dict.get("error_message"),
                            "result_summary": entry_dict.get("result_summary"),
                            "timestamp": entry_dict.get("timestamp")
                        }

                        # Add to blockchain
                        block = MutationLog._blockchain.add_gene(
                            gene_type=GeneType.MUTATION,
                            data=mutation_gene_data,
                            agent=entry_dict.get("agent", "unknown").lower(),
                            tags=["mutation", "migrated", entry_dict.get("operation_type")]
                        )

                        migrated_count += 1

                        if migrated_count % 10 == 0:
                            logger.info(f"🧬 Migrated {migrated_count} mutations...")

                    except Exception as e:
                        error_msg = f"Line {line_num}: {str(e)}"
                        errors.append(error_msg)
                        logger.warning(f"⚠️ Migration error: {error_msg}")

            logger.info(f"✅ Migration complete: {migrated_count} mutations migrated to blockchain")

            # Validate blockchain after migration
            is_valid = MutationLog._blockchain.validate_chain()

            return {
                "success": True,
                "migrated": migrated_count,
                "errors": errors,
                "blockchain_valid": is_valid,
                "total_genes": len(MutationLog._blockchain.chain),
                "merkle_root": MutationLog._blockchain.get_merkle_root()
            }

        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "migrated": migrated_count,
                "errors": errors
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
