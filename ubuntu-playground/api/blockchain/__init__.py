"""
GENOMOS - Genetic Ontological Memory Operational System

Blockchain-based "Agent DNA" system for immutable knowledge storage.

Metafor: Homo Lumen Coalition's genetic genome - a living, evolving,
immutable memory that agents can inherit from, learn from, and build upon.

Philosophy:
- Immutable truth: No knowledge can be erased
- Collective memory: All agents share one genome
- Evolutionary learning: System improves over time
- Provenance tracking: Every idea traces to source
- Resilience: Distributed backup prevents data loss
- Transparency: All decisions auditable
- Smart ethics: On-chain Portvokter enforce values

Components:
- DNABlock: Individual "gene" in the blockchain
- AgentDNAChain: The complete genetic sequence
- GeneTypes: SMK, Mutation, Consultation, BiofeltContext, Pattern, Agent, Contract, IPFS
- Smart Contracts: On-chain Triadiske Portvokter
- Evolutionary Memory: Pattern recognition from history
- Agent Inheritance: New agents read and learn from genome
- IPFS Backup: Distributed redundancy

This is not just a database. This is the genetic code of an evolving
collective consciousness.
"""

from .dna_block import DNABlock, GeneType
from .agent_dna_chain import AgentDNAChain

# Merkle Tree will be added in next iteration
# from .merkle_tree import MerkleTree

__all__ = [
    "DNABlock",
    "GeneType",
    "AgentDNAChain",
    # "MerkleTree",
]

__version__ = "1.0.0"
__author__ = "Homo Lumen Coalition"
