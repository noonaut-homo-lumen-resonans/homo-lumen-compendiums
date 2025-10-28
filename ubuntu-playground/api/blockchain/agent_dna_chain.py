"""
AgentDNAChain - Complete Genetic Sequence for Homo Lumen Coalition

The blockchain that holds ALL knowledge, operations, and consciousness states
of the Homo Lumen collective. This is the "genome" that agents inherit from
and contribute to.

Philosophy:
- Genesis Block = Constitution (immutable foundation)
- Each block = gene (knowledge, operation, pattern, etc.)
- Chain = genome (complete hereditary information)
- Validation = genetic integrity check
- Persistence = DNA replication across storage

This is not just a database. This is living, evolving collective memory.
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import sqlite3
import logging
import json
from datetime import datetime

from .dna_block import DNABlock, GeneType, create_genesis_block

logger = logging.getLogger(__name__)


class AgentDNAChain:
    """
    Complete blockchain containing all Agent DNA.

    The chain starts with Genesis Block (Constitution) and grows as
    new knowledge, operations, and patterns are added.

    Features:
    - Genesis Block with Homo Lumen Constitution
    - Add genes (blocks) to chain
    - Validate entire chain integrity
    - Persist to SQLite database
    - Query blocks by index, hash, or gene type
    - Calculate Merkle root for efficient verification
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize Agent DNA Chain.

        Args:
            db_path: Path to SQLite database (default: ./data/genomos.db)
        """
        self.chain: List[DNABlock] = []
        self.db_path = db_path or "./data/genomos.db"

        # Initialize database
        self._init_database()

        # Load existing chain from database or create genesis
        self._load_or_create_genesis()

        logger.info(f"🧬 AgentDNAChain initialized: {len(self.chain)} blocks")

    def _init_database(self):
        """Initialize SQLite database schema for DNA storage."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create dna_blocks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dna_blocks (
                block_index INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                gene_type TEXT NOT NULL,
                data_json TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                block_hash TEXT NOT NULL UNIQUE,
                agent TEXT,
                tags_json TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for fast querying
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gene_type
            ON dna_blocks(gene_type)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_agent
            ON dna_blocks(agent)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hash
            ON dna_blocks(block_hash)
        """)

        conn.commit()
        conn.close()

        logger.info(f"📁 Database initialized: {self.db_path}")

    def _load_or_create_genesis(self):
        """Load chain from database or create Genesis Block."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if we have any blocks
        cursor.execute("SELECT COUNT(*) FROM dna_blocks")
        count = cursor.fetchone()[0]

        if count == 0:
            # Create Genesis Block
            logger.info("🌟 Creating Genesis Block (Constitution V1.1)...")
            genesis_data = {
                "type": "genesis_constitution",
                "version": "1.1",
                "title": "Homo Lumen Constitution V1.1",
                "ratified": "2025-10-12",
                "agents": [
                    "Lira", "Nyra", "Orion", "Thalus", "Zara",
                    "Aurora", "Abacus", "Falcon"
                ],
                "core_principles": [
                    "Kognitiv Suverenitet",
                    "Ontologisk Koherens",
                    "Regenerativ Healing"
                ],
                "three_gates": ["BiofeltGate", "ThalosFilter", "MutationLog"],
                "philosophy": {
                    "purpose": "Explore reality → Understanding → Freedom → Healing",
                    "method": "Remove falsehoods, Repair half-truths, Add context, State with sources",
                    "epistemic": "Triangulate evidence, Falsifiable claims, Traceable reasoning"
                },
                "source_smk": "SMK#019",
                "description": "The foundational document of Homo Lumen Coalition - our genetic code's first gene"
            }

            genesis = create_genesis_block(genesis_data)
            self.chain.append(genesis)

            # Save to database
            self._save_block_to_db(genesis)

            logger.info(f"✅ Genesis Block created: {genesis.hash[:16]}...")

        else:
            # Load chain from database
            cursor.execute("""
                SELECT block_index, timestamp, gene_type, data_json,
                       previous_hash, block_hash, agent, tags_json
                FROM dna_blocks
                ORDER BY block_index ASC
            """)

            rows = cursor.fetchall()
            for row in rows:
                block = DNABlock(
                    index=row[0],
                    timestamp=row[1],
                    gene_type=GeneType(row[2]),
                    data=json.loads(row[3]),
                    previous_hash=row[4],
                    hash=row[5],
                    agent=row[6],
                    tags=json.loads(row[7]) if row[7] else []
                )
                self.chain.append(block)

            logger.info(f"📖 Loaded {len(self.chain)} blocks from database")

        conn.close()

    def _save_block_to_db(self, block: DNABlock):
        """Save a single block to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO dna_blocks (
                block_index, timestamp, gene_type, data_json,
                previous_hash, block_hash, agent, tags_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            block.index,
            block.timestamp,
            block.gene_type.value,
            json.dumps(block.data),
            block.previous_hash,
            block.hash,
            block.agent,
            json.dumps(block.tags) if block.tags else None
        ))

        conn.commit()
        conn.close()

    def get_latest_block(self) -> DNABlock:
        """
        Get the most recent block in the chain.

        Returns:
            Latest DNABlock
        """
        return self.chain[-1]

    def add_gene(
        self,
        gene_type: GeneType,
        data: Dict[str, Any],
        agent: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> DNABlock:
        """
        Add a new "gene" (block) to the DNA chain.

        This is the primary method for adding knowledge, operations,
        or patterns to the collective genome.

        Args:
            gene_type: Type of gene (SMK, Mutation, Consultation, etc.)
            data: Block payload
            agent: Agent who created this gene
            tags: Searchable tags

        Returns:
            Newly created DNABlock

        Raises:
            ValueError: If chain validation fails
        """
        # Get previous block
        previous_block = self.get_latest_block()

        # Create new block
        new_block = DNABlock(
            index=len(self.chain),
            gene_type=gene_type,
            data=data,
            previous_hash=previous_block.hash,
            agent=agent,
            tags=tags or []
        )

        # Validate before adding
        if not self._is_valid_new_block(new_block, previous_block):
            raise ValueError(f"Invalid block: {new_block}")

        # Add to chain
        self.chain.append(new_block)

        # Save to database
        self._save_block_to_db(new_block)

        logger.info(f"➕ Gene added: Block {new_block.index} ({gene_type.value}) - {new_block.hash[:8]}...")

        return new_block

    def _is_valid_new_block(self, new_block: DNABlock, previous_block: DNABlock) -> bool:
        """
        Validate that a new block can be added to the chain.

        Checks:
        1. Index is sequential (previous + 1)
        2. Previous hash matches
        3. Block hash is valid

        Args:
            new_block: Block to validate
            previous_block: Current chain head

        Returns:
            True if valid, False otherwise
        """
        # Check index
        if new_block.index != previous_block.index + 1:
            logger.error(f"Invalid index: expected {previous_block.index + 1}, got {new_block.index}")
            return False

        # Check previous hash
        if new_block.previous_hash != previous_block.hash:
            logger.error(f"Invalid previous_hash: expected {previous_block.hash}, got {new_block.previous_hash}")
            return False

        # Check hash validity
        if not new_block.verify_hash():
            logger.error(f"Invalid hash for block {new_block.index}")
            return False

        return True

    def validate_chain(self) -> bool:
        """
        Validate the entire DNA chain integrity.

        Checks:
        1. Genesis block has previous_hash="0"
        2. Each block's previous_hash matches previous block's hash
        3. Each block's hash is valid
        4. Indexes are sequential

        Returns:
            True if chain is valid, False if compromised
        """
        if len(self.chain) == 0:
            return True

        # Check genesis block
        genesis = self.chain[0]
        if genesis.previous_hash != "0":
            logger.error("Genesis block has invalid previous_hash")
            return False

        if not genesis.verify_hash():
            logger.error("Genesis block hash is invalid")
            return False

        # Check all subsequent blocks
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check index
            if current.index != previous.index + 1:
                logger.error(f"Index mismatch at block {i}")
                return False

            # Check previous_hash linking
            if current.previous_hash != previous.hash:
                logger.error(f"Chain broken at block {i}: previous_hash mismatch")
                return False

            # Check hash validity
            if not current.verify_hash():
                logger.error(f"Invalid hash at block {i}")
                return False

        logger.info("✅ Chain validation passed")
        return True

    def get_block(self, index: int) -> Optional[DNABlock]:
        """
        Get block by index.

        Args:
            index: Block position in chain

        Returns:
            DNABlock or None if not found
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def get_block_by_hash(self, block_hash: str) -> Optional[DNABlock]:
        """
        Get block by hash.

        Args:
            block_hash: SHA-256 hash of block

        Returns:
            DNABlock or None if not found
        """
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None

    def get_genes_by_type(self, gene_type: GeneType) -> List[DNABlock]:
        """
        Get all blocks of a specific gene type.

        Args:
            gene_type: Type of gene to filter by

        Returns:
            List of matching DNABlocks
        """
        return [block for block in self.chain if block.gene_type == gene_type]

    def get_genes_by_agent(self, agent: str) -> List[DNABlock]:
        """
        Get all blocks created by a specific agent.

        Args:
            agent: Agent name

        Returns:
            List of matching DNABlocks
        """
        return [block for block in self.chain if block.agent == agent]

    def get_genes_by_tag(self, tag: str) -> List[DNABlock]:
        """
        Get all blocks with a specific tag.

        Args:
            tag: Tag to search for

        Returns:
            List of matching DNABlocks
        """
        return [block for block in self.chain if tag in block.tags]

    def get_chain_info(self) -> Dict[str, Any]:
        """
        Get statistics and metadata about the DNA chain.

        Returns:
            Dictionary with chain statistics
        """
        gene_type_counts = {}
        agent_counts = {}

        for block in self.chain:
            # Count gene types
            gene_type = block.gene_type.value
            gene_type_counts[gene_type] = gene_type_counts.get(gene_type, 0) + 1

            # Count agents
            if block.agent:
                agent_counts[block.agent] = agent_counts.get(block.agent, 0) + 1

        return {
            "total_blocks": len(self.chain),
            "genesis_block": self.chain[0].hash if self.chain else None,
            "latest_block": self.chain[-1].hash if self.chain else None,
            "gene_type_counts": gene_type_counts,
            "agent_counts": agent_counts,
            "chain_valid": self.validate_chain(),
            "database_path": self.db_path
        }

    def export_chain(self, output_file: str):
        """
        Export entire chain to JSON file.

        Args:
            output_file: Path to output JSON file
        """
        chain_data = [block.to_dict() for block in self.chain]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chain_data, f, indent=2, ensure_ascii=False)

        logger.info(f"📤 Chain exported to {output_file}")

    def import_chain(self, input_file: str):
        """
        Import chain from JSON file and replace current chain.

        WARNING: This replaces the existing chain!

        Args:
            input_file: Path to input JSON file

        Raises:
            ValueError: If imported chain is invalid
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            chain_data = json.load(f)

        # Create blocks from JSON
        imported_chain = [DNABlock.from_dict(block_dict) for block_dict in chain_data]

        # Validate imported chain
        temp_chain = self.chain
        self.chain = imported_chain

        if not self.validate_chain():
            self.chain = temp_chain
            raise ValueError("Imported chain is invalid")

        # Save all blocks to database
        for block in self.chain:
            self._save_block_to_db(block)

        logger.info(f"📥 Chain imported from {input_file}: {len(self.chain)} blocks")

    def get_merkle_root(self) -> str:
        """
        Calculate Merkle root hash for the entire chain.

        This provides an efficient way to verify chain integrity
        without checking every block.

        Returns:
            Merkle root hash (SHA-256)
        """
        import hashlib

        if len(self.chain) == 0:
            return "0" * 64

        # Get all block hashes
        hashes = [block.hash for block in self.chain]

        # Build Merkle tree
        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])  # Duplicate last hash if odd

            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i + 1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)

            hashes = new_hashes

        return hashes[0]

    def __len__(self) -> int:
        """Return number of blocks in chain."""
        return len(self.chain)

    def __str__(self) -> str:
        """String representation."""
        return f"AgentDNAChain({len(self.chain)} blocks, merkle_root={self.get_merkle_root()[:16]}...)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"AgentDNAChain(blocks={len(self.chain)}, db={self.db_path})"


if __name__ == "__main__":
    # Test AgentDNAChain
    print("🧬 Testing AgentDNAChain...")

    # Create chain
    chain = AgentDNAChain(db_path="./data/genomos_test.db")

    # Print genesis block
    genesis = chain.get_block(0)
    print("\n" + genesis.get_summary())

    # Add SMK block
    smk_block = chain.add_gene(
        gene_type=GeneType.SMK,
        data={
            "smk_id": "042",
            "title": "GENOMOS Implementation",
            "date": "2025-10-28",
            "description": "Blockchain-based Agent DNA system"
        },
        agent="orion",
        tags=["genomos", "blockchain", "agent-dna"]
    )
    print("\n" + smk_block.get_summary())

    # Add mutation block
    mutation_block = chain.add_gene(
        gene_type=GeneType.MUTATION,
        data={
            "mutation_id": "test123",
            "operation_type": "write",
            "target": "blockchain/test.py",
            "success": True
        },
        agent="lira",
        tags=["mutation", "write"]
    )
    print("\n" + mutation_block.get_summary())

    # Validate chain
    print(f"\n🔍 Chain valid: {chain.validate_chain()}")

    # Get chain info
    info = chain.get_chain_info()
    print(f"\n📊 Chain Info:")
    for key, value in info.items():
        print(f"   {key}: {value}")

    # Merkle root
    print(f"\n🌳 Merkle Root: {chain.get_merkle_root()}")
