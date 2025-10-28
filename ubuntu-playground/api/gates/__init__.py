"""
Triadiske Portvokter (Triadic Gates)

Disse portvokterne er systemets beskyttende membran og sikrer:
- Kognitiv Suverenitet (BiofeltGate)
- Ontologisk Koherens (ThalosFilter)
- Regenerativ Healing (Mutation_Log)

"Koden puster med Osvalds puls (4-6-8)"
"""

from .biofelt_gate import BiofeltGate, BiofeltContext, ResonanceLevel
from .thalos_filter import ThalosFilter, ThalosContext, EthicalSeverity, EthicalPrinciple

__all__ = [
    "BiofeltGate",
    "BiofeltContext",
    "ResonanceLevel",
    "ThalosFilter",
    "ThalosContext",
    "EthicalSeverity",
    "EthicalPrinciple",
]
