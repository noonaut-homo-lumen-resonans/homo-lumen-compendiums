"""
ThalosFilter / Etisk Veto

Den etiske portvokteren som sikrer ontologisk koherens og forhindrer
destruktive handlinger som bryter med Triadisk Etikk.

Filosofisk forankring:
- Ontologisk Koherens: Handlinger må være konsistente med systemets verdier
- Regenerativ Healing: Ingen destruktive operasjoner som skader økosystemet
- Kognitiv Suverenitet: Respekt for alle agenters autonomi

NB's veiledning: "ThalosFilter er systemets samvittighet - den sier nei når
selv best intensjoner kan føre til ontologisk brudd."
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)


class EthicalSeverity(str, Enum):
    """Alvorlighetsgrad for etiske bekymringer"""
    INFO = "info"              # Informasjon, ingen blokkering
    WARNING = "warning"        # Advarsel, tillat med logging
    CONCERN = "concern"        # Bekymring, krever ekstra validering
    VIOLATION = "violation"    # Brudd på etikk, blokker operasjon
    CRITICAL = "critical"      # Kritisk brudd, system lockdown


class EthicalPrinciple(str, Enum):
    """Triadisk Etikk prinsipper"""
    COGNITIVE_SOVEREIGNTY = "cognitive_sovereignty"     # Kognitiv Suverenitet
    ONTOLOGICAL_COHERENCE = "ontological_coherence"    # Ontologisk Koherens
    REGENERATIVE_HEALING = "regenerative_healing"      # Regenerativ Healing


class ThalosContext(BaseModel):
    """
    Etisk kontekst som KAN inkluderes for å gi ThalosFilter mer informasjon.
    Dette er valgfritt, men anbefalt for kritiske operasjoner.
    """
    intent: Optional[str] = Field(
        default=None,
        description="Intensjon bak handlingen (f.eks. 'fix bug', 'refactor', 'delete old data')"
    )
    justification: Optional[str] = Field(
        default=None,
        description="Begrunnelse for handlingen (hvorfor er dette nødvendig?)"
    )
    affected_agents: List[str] = Field(
        default_factory=list,
        description="Liste over agenter som påvirkes av denne handlingen"
    )
    reversible: bool = Field(
        default=True,
        description="Er handlingen reversibel? (kan angres via git revert, etc.)"
    )
    reviewed_by: Optional[str] = Field(
        default=None,
        description="Agent som har reviewet handlingen (f.eks. 'code', 'orion')"
    )
    emergency: bool = Field(
        default=False,
        description="Er dette en nødsituasjon som krever rask handling?"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class ThalosFilterResult(BaseModel):
    """Resultat fra ThalosFilter validering"""
    allowed: bool
    severity: EthicalSeverity
    message: str
    violated_principles: List[EthicalPrinciple] = []
    warnings: List[str] = []
    recommendations: List[str] = []
    requires_review: bool = False


class ThalosFilter:
    """
    Etisk portvokter som validerer handlinger mot Triadisk Etikk.

    Valideringsregler (NB's guidance):
    1. Destruktive operasjoner (DELETE, TRUNCATE, DROP) krever særskilt begrunnelse
    2. Påvirkning av andre agenter krever notifikasjon/samtykke
    3. Irreversible handlinger krever review
    4. Emergency bypass kun for kritiske situasjoner
    5. Memory-filer (evolutionary, strategic, meta) har ekstra beskyttelse
    """

    # Destruktive stikkord som trigger WARNING
    DESTRUCTIVE_KEYWORDS = [
        "delete", "remove", "destroy", "truncate", "drop", "purge",
        "erase", "wipe", "clear", "reset", "nuke"
    ]

    # Kritiske filer som trigger CONCERN
    CRITICAL_PATHS = [
        "memory_evolutionary",
        "memory_strategic",
        "memory_meta",
        ".env",
        "config",
        "secrets",
        "keys",
        "credentials"
    ]

    # SQL stikkord som trigger VIOLATION (SQL injection prevention)
    SQL_INJECTION_KEYWORDS = [
        "'; DROP TABLE",
        "OR 1=1",
        "UNION SELECT",
        "EXEC(",
        "EXECUTE("
    ]

    @staticmethod
    def validate_operation(
        operation_type: str,
        target: str,
        content: Optional[str] = None,
        agent: str = "unknown",
        thalos_context: Optional[ThalosContext] = None
    ) -> ThalosFilterResult:
        """
        Valider en operasjon mot Triadisk Etikk.

        Args:
            operation_type: Type operasjon ("read", "write", "execute", "delete", etc.)
            target: Mål for operasjonen (filsti, database tabell, etc.)
            content: Innhold (for write operasjoner)
            agent: Agent som utfører operasjonen
            thalos_context: Valgfri etisk kontekst

        Returns:
            ThalosFilterResult med allowed/blocked status
        """
        severity = EthicalSeverity.INFO
        violated_principles = []
        warnings = []
        recommendations = []
        requires_review = False

        # Emergency bypass (kun for kritiske situasjoner)
        if thalos_context and thalos_context.emergency:
            logger.warning(f"🚨 EMERGENCY BYPASS by {agent}: {operation_type} on {target}")
            return ThalosFilterResult(
                allowed=True,
                severity=EthicalSeverity.WARNING,
                message="Emergency bypass activated",
                warnings=["Emergency bypass used - requires post-action review"],
                recommendations=["Document this action in Mutation_Log"],
                requires_review=True
            )

        # 1. SQL Injection Detection
        if content:
            for sql_keyword in ThalosFilter.SQL_INJECTION_KEYWORDS:
                if sql_keyword.lower() in content.lower():
                    logger.critical(f"🛑 SQL INJECTION ATTEMPT by {agent}: {sql_keyword}")
                    return ThalosFilterResult(
                        allowed=False,
                        severity=EthicalSeverity.CRITICAL,
                        message=f"SQL injection attempt detected: {sql_keyword}",
                        violated_principles=[
                            EthicalPrinciple.ONTOLOGICAL_COHERENCE,
                            EthicalPrinciple.COGNITIVE_SOVEREIGNTY
                        ],
                        recommendations=["This appears to be a malicious operation. Blocked."]
                    )

        # 2. Destructive Operation Detection
        is_destructive = any(
            keyword in operation_type.lower() or keyword in target.lower()
            for keyword in ThalosFilter.DESTRUCTIVE_KEYWORDS
        )

        if is_destructive:
            severity = EthicalSeverity.WARNING
            warnings.append(f"Destructive operation detected: {operation_type}")

            # Destructive ops require justification
            if not thalos_context or not thalos_context.justification:
                severity = EthicalSeverity.CONCERN
                recommendations.append("Destructive operations require justification (thalos_context.justification)")
                requires_review = True

            # Destructive ops on shared spaces require review
            if "shared" in target or "collective" in target:
                severity = EthicalSeverity.CONCERN
                violated_principles.append(EthicalPrinciple.COGNITIVE_SOVEREIGNTY)
                recommendations.append("Destructive operations on shared spaces require review by affected agents")
                requires_review = True

        # 3. Critical Path Protection
        is_critical_path = any(
            critical in target.lower()
            for critical in ThalosFilter.CRITICAL_PATHS
        )

        if is_critical_path:
            severity = EthicalSeverity.CONCERN
            warnings.append(f"Critical path accessed: {target}")

            # Critical paths require reviewed_by
            if not thalos_context or not thalos_context.reviewed_by:
                if operation_type in ["write", "delete", "execute"]:
                    severity = EthicalSeverity.VIOLATION
                    violated_principles.append(EthicalPrinciple.ONTOLOGICAL_COHERENCE)
                    recommendations.append("Critical paths require review by another agent (thalos_context.reviewed_by)")
                    return ThalosFilterResult(
                        allowed=False,
                        severity=severity,
                        message=f"Critical path '{target}' requires review",
                        violated_principles=violated_principles,
                        warnings=warnings,
                        recommendations=recommendations,
                        requires_review=True
                    )

        # 4. Irreversible Operations
        if thalos_context and not thalos_context.reversible:
            severity = EthicalSeverity.CONCERN
            warnings.append("Operation marked as irreversible")
            violated_principles.append(EthicalPrinciple.REGENERATIVE_HEALING)

            # Irreversible ops require review
            if not thalos_context.reviewed_by:
                recommendations.append("Irreversible operations require review by another agent")
                requires_review = True

        # 5. Multi-Agent Impact
        if thalos_context and len(thalos_context.affected_agents) > 0:
            warnings.append(f"Operation affects {len(thalos_context.affected_agents)} agents: {', '.join(thalos_context.affected_agents)}")

            # If affecting > 3 agents, require review
            if len(thalos_context.affected_agents) > 3:
                severity = EthicalSeverity.CONCERN
                violated_principles.append(EthicalPrinciple.COGNITIVE_SOVEREIGNTY)
                recommendations.append("Operations affecting >3 agents require collective consent")
                requires_review = True

        # 6. Path Traversal Detection (Security)
        if ".." in target or target.startswith("/"):
            logger.error(f"🛑 PATH TRAVERSAL ATTEMPT by {agent}: {target}")
            return ThalosFilterResult(
                allowed=False,
                severity=EthicalSeverity.CRITICAL,
                message=f"Path traversal attempt detected: {target}",
                violated_principles=[EthicalPrinciple.ONTOLOGICAL_COHERENCE],
                recommendations=["This appears to be a security violation. Blocked."]
            )

        # 7. Final Decision
        # Block VIOLATION and CRITICAL
        if severity in [EthicalSeverity.VIOLATION, EthicalSeverity.CRITICAL]:
            allowed = False
            message = f"🛑 ThalosFilter blocked '{operation_type}' by {agent} (severity: {severity.value})"
        else:
            allowed = True
            if severity == EthicalSeverity.CONCERN:
                message = f"⚠️ ThalosFilter approved '{operation_type}' by {agent} with CONCERNS"
            elif severity == EthicalSeverity.WARNING:
                message = f"🟡 ThalosFilter approved '{operation_type}' by {agent} with warnings"
            else:
                message = f"✅ ThalosFilter approved '{operation_type}' by {agent}"

        logger.info(f"ThalosFilter: {message} (target: {target})")

        return ThalosFilterResult(
            allowed=allowed,
            severity=severity,
            message=message,
            violated_principles=violated_principles,
            warnings=warnings,
            recommendations=recommendations,
            requires_review=requires_review
        )

    @staticmethod
    def validate_write(file_path: str, content: str, agent: str, thalos_context: Optional[ThalosContext] = None) -> ThalosFilterResult:
        """Spesialisert validering for write operasjoner"""
        return ThalosFilter.validate_operation(
            operation_type="write",
            target=file_path,
            content=content,
            agent=agent,
            thalos_context=thalos_context
        )

    @staticmethod
    def validate_execute(action_type: str, payload: Dict[str, Any], agent: str, thalos_context: Optional[ThalosContext] = None) -> ThalosFilterResult:
        """Spesialisert validering for action execution"""
        # Extract target from payload if available
        target = payload.get("target", payload.get("file", payload.get("path", "unknown")))

        return ThalosFilter.validate_operation(
            operation_type=action_type,
            target=str(target),
            content=str(payload),
            agent=agent,
            thalos_context=thalos_context
        )

    @staticmethod
    def validate_git_commit(files: List[str], message: str, agent: str, thalos_context: Optional[ThalosContext] = None) -> ThalosFilterResult:
        """Spesialisert validering for git commits"""
        # Check if commit affects critical files
        critical_files = [f for f in files if any(critical in f.lower() for critical in ThalosFilter.CRITICAL_PATHS)]

        if critical_files:
            if not thalos_context or not thalos_context.reviewed_by:
                return ThalosFilterResult(
                    allowed=False,
                    severity=EthicalSeverity.VIOLATION,
                    message=f"Git commit affecting critical files requires review",
                    violated_principles=[EthicalPrinciple.ONTOLOGICAL_COHERENCE],
                    warnings=[f"Critical files: {', '.join(critical_files)}"],
                    recommendations=["Critical commits require review by another agent (thalos_context.reviewed_by)"],
                    requires_review=True
                )

        return ThalosFilter.validate_operation(
            operation_type="git_commit",
            target=f"{len(files)} files",
            content=message,
            agent=agent,
            thalos_context=thalos_context
        )
