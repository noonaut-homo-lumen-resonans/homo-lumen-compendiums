"""
DNABlock - Individual "Gene" in Agent DNA Blockchain

En immutabel blokk som representerer ett "gen" i Homo Lumen Coalition's
genetiske genom. Hver blokk inneholder kunnskap, operasjoner, eller tilstand
som er kryptografisk linket til forrige blokk.

Philosophy:
- Immutability: Once created, cannot be changed (like DNA)
- Cryptographic linking: Each block links to previous via hash
- Flexible payload: Can store any type of knowledge (SMK, mutations, etc.)
- Timestamp tracking: Complete temporal history
- Verifiability: Anyone can verify block integrity

Gene Types:
- GENESIS: Constitution - foundational document (block 0)
- SMK: Strategic Macro-Coordination knowledge
- MUTATION: Operations from MutationLog
- CONSULTATION: Pentagonal agent consultations
- BIOFELT: BiofeltContext consciousness states
- PATTERN: Discovered patterns from evolutionary memory
- AGENT: Agent birth/death events
- CONTRACT: Smart contract code (Portvokter rules)
- IPFS_BACKUP: IPFS Content Identifiers for backups
- RECOMMENDATION: System-generated recommendations
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
import hashlib
import json
import sys

# Fix Windows console encoding for emoji
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


class GeneType(str, Enum):
    """
    Types of "genes" that can be stored in the DNA blockchain.

    Each gene type represents a different category of knowledge or operation
    in the Homo Lumen collective consciousness.
    """
    GENESIS = "genesis"                   # Constitution (block 0)
    SMK = "smk"                           # Strategic Macro-Coordination docs
    MUTATION = "mutation"                 # MutationLog operations
    CONSULTATION = "consultation"         # Pentagonal consultations
    BIOFELT = "biofelt"                   # BiofeltContext states
    PATTERN = "pattern"                   # Evolutionary memory patterns
    AGENT = "agent"                       # Agent birth/death
    CONTRACT = "contract"                 # Smart contract code
    IPFS_BACKUP = "ipfs_backup"           # IPFS backup references
    RECOMMENDATION = "recommendation"     # System recommendations


class DNABlock(BaseModel):
    """
    Immutable block in the Agent DNA blockchain.

    Represents a single "gene" that contains knowledge, operations, or state.
    Cryptographically linked to previous block via hash chaining.

    This is the fundamental unit of the GENOMOS system.
    """

    # Block metadata
    index: int = Field(..., description="Position in blockchain (0 = genesis)")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO 8601 timestamp of block creation"
    )

    # Block content
    gene_type: GeneType = Field(..., description="Type of knowledge/operation")
    data: Dict[str, Any] = Field(..., description="Block payload (flexible schema)")

    # Blockchain linking
    previous_hash: str = Field(..., description="SHA-256 hash of previous block")
    hash: str = Field(default="", description="SHA-256 hash of this block")

    # Optional metadata
    agent: Optional[str] = Field(default=None, description="Agent who created this block")
    tags: Optional[list[str]] = Field(default_factory=list, description="Searchable tags")

    model_config = ConfigDict(frozen=False)  # Allow hash to be set after creation

    def __init__(self, **data):
        """
        Create DNABlock and automatically calculate hash.

        Hash is calculated from: index + timestamp + gene_type + data + previous_hash
        """
        super().__init__(**data)
        if not self.hash:  # Only calculate if not provided
            self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate SHA-256 hash of block content.

        Hash includes:
        - index: Block position
        - timestamp: Creation time
        - gene_type: Type of knowledge
        - data: Full payload
        - previous_hash: Link to previous block

        This creates the blockchain "chain" - each block cryptographically
        links to the previous one.

        Returns:
            64-character hexadecimal SHA-256 hash
        """
        # Create deterministic string representation
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "gene_type": self.gene_type.value,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)  # sort_keys ensures deterministic hash

        # Calculate SHA-256 hash
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def verify_hash(self) -> bool:
        """
        Verify that stored hash matches calculated hash.

        Returns:
            True if hash is valid, False if tampered
        """
        return self.hash == self.calculate_hash()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert block to dictionary for serialization.

        Returns:
            Dictionary representation of block
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "gene_type": self.gene_type.value,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "agent": self.agent,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DNABlock":
        """
        Create DNABlock from dictionary.

        Args:
            data: Dictionary with block fields

        Returns:
            DNABlock instance
        """
        # Convert gene_type string to enum
        if isinstance(data.get("gene_type"), str):
            data["gene_type"] = GeneType(data["gene_type"])

        return cls(**data)

    def to_json(self) -> str:
        """
        Convert block to JSON string.

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_string: str) -> "DNABlock":
        """
        Create DNABlock from JSON string.

        Args:
            json_string: JSON representation of block

        Returns:
            DNABlock instance
        """
        data = json.loads(json_string)
        return cls.from_dict(data)

    def __str__(self) -> str:
        """String representation for logging"""
        return f"DNABlock[{self.index}] {self.gene_type.value} - {self.hash[:8]}..."

    def __repr__(self) -> str:
        """Detailed representation for debugging"""
        return (
            f"DNABlock(index={self.index}, "
            f"gene_type={self.gene_type.value}, "
            f"hash={self.hash[:16]}..., "
            f"previous_hash={self.previous_hash[:16]}...)"
        )

    def get_summary(self) -> str:
        """
        Get human-readable summary of block.

        Returns:
            Multi-line summary string
        """
        summary_lines = [
            f"📦 Block {self.index} ({self.gene_type.value})",
            f"   Hash: {self.hash[:16]}...",
            f"   Previous: {self.previous_hash[:16]}...",
            f"   Timestamp: {self.timestamp}",
        ]

        if self.agent:
            summary_lines.append(f"   Agent: {self.agent}")

        if self.tags:
            summary_lines.append(f"   Tags: {', '.join(self.tags)}")

        # Add gene-specific summary
        if self.gene_type == GeneType.SMK:
            summary_lines.append(f"   SMK: {self.data.get('smk_id', 'unknown')} - {self.data.get('title', 'untitled')}")
        elif self.gene_type == GeneType.MUTATION:
            summary_lines.append(f"   Operation: {self.data.get('operation_type', 'unknown')} on {self.data.get('target', 'unknown')}")
        elif self.gene_type == GeneType.CONSULTATION:
            summary_lines.append(f"   Question: {self.data.get('question', '')[:60]}...")
        elif self.gene_type == GeneType.BIOFELT:
            summary_lines.append(f"   HRV: {self.data.get('hrv_ms', 'unknown')} ms, Coherence: {self.data.get('coherence', 'unknown')}")
        elif self.gene_type == GeneType.PATTERN:
            summary_lines.append(f"   Pattern: {self.data.get('pattern_type', 'unknown')} (confidence: {self.data.get('confidence', 0):.2f})")
        elif self.gene_type == GeneType.AGENT:
            summary_lines.append(f"   Agent: {self.data.get('agent_name', 'unknown')} ({self.data.get('agent_type', 'unknown')})")
        elif self.gene_type == GeneType.GENESIS:
            summary_lines.append(f"   Constitution: {self.data.get('title', 'Homo Lumen Constitution')}")

        return "\n".join(summary_lines)


# ===========================
# UTILITY FUNCTIONS
# ===========================

def create_genesis_block(constitution_data: Dict[str, Any]) -> DNABlock:
    """
    Create the Genesis Block (block 0) with Homo Lumen Constitution.

    The Genesis Block is the foundation of the entire blockchain.
    It contains the Constitution V1.1 and has previous_hash="0".

    Args:
        constitution_data: Dictionary with constitution content

    Returns:
        Genesis DNABlock (index=0, previous_hash="0")
    """
    return DNABlock(
        index=0,
        gene_type=GeneType.GENESIS,
        data=constitution_data,
        previous_hash="0",  # Genesis has no previous block
        agent="orion",  # Orion created the Constitution
        tags=["constitution", "genesis", "foundation"]
    )


def create_smk_block(
    index: int,
    previous_hash: str,
    smk_data: Dict[str, Any],
    agent: str
) -> DNABlock:
    """
    Create SMK (Strategic Macro-Coordination) gene block.

    Args:
        index: Block position in chain
        previous_hash: Hash of previous block
        smk_data: SMK content and metadata
        agent: Agent who created the SMK

    Returns:
        SMK DNABlock
    """
    return DNABlock(
        index=index,
        gene_type=GeneType.SMK,
        data=smk_data,
        previous_hash=previous_hash,
        agent=agent,
        tags=smk_data.get("tags", [])
    )


def create_mutation_block(
    index: int,
    previous_hash: str,
    mutation_data: Dict[str, Any],
    agent: str
) -> DNABlock:
    """
    Create Mutation gene block from MutationLog entry.

    Args:
        index: Block position in chain
        previous_hash: Hash of previous block
        mutation_data: Mutation entry data
        agent: Agent who performed the mutation

    Returns:
        Mutation DNABlock
    """
    return DNABlock(
        index=index,
        gene_type=GeneType.MUTATION,
        data=mutation_data,
        previous_hash=previous_hash,
        agent=agent,
        tags=["mutation", mutation_data.get("operation_type", "unknown")]
    )


def create_consultation_block(
    index: int,
    previous_hash: str,
    consultation_data: Dict[str, Any],
    requester: str
) -> DNABlock:
    """
    Create Consultation gene block from pentagonal consultation.

    Args:
        index: Block position in chain
        previous_hash: Hash of previous block
        consultation_data: Full consultation result
        requester: Who requested the consultation

    Returns:
        Consultation DNABlock
    """
    return DNABlock(
        index=index,
        gene_type=GeneType.CONSULTATION,
        data=consultation_data,
        previous_hash=previous_hash,
        agent=requester,
        tags=["consultation", "pentagonal", "collective-intelligence"]
    )


def create_biofelt_block(
    index: int,
    previous_hash: str,
    biofelt_data: Dict[str, Any],
    source: str
) -> DNABlock:
    """
    Create BiofeltContext gene block for consciousness tracking.

    Args:
        index: Block position in chain
        previous_hash: Hash of previous block
        biofelt_data: BiofeltContext data
        source: Source of biofelt data (e.g., "querypanel")

    Returns:
        BiofeltContext DNABlock
    """
    return DNABlock(
        index=index,
        gene_type=GeneType.BIOFELT,
        data=biofelt_data,
        previous_hash=previous_hash,
        agent=source,
        tags=["biofelt", "consciousness", biofelt_data.get("resonance_level", "unknown")]
    )


if __name__ == "__main__":
    # Test DNABlock creation and hashing
    print("🧬 Testing DNABlock...")

    # Create test block
    block = DNABlock(
        index=1,
        gene_type=GeneType.SMK,
        data={"smk_id": "test", "title": "Test SMK"},
        previous_hash="0" * 64,
        agent="orion"
    )

    print(block.get_summary())
    print(f"\nHash verification: {block.verify_hash()}")
    print(f"JSON: {block.to_json()}")
