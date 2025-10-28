"""
GENOMOS DNA API Router

REST API endpoints for querying the Agent DNA Blockchain.
Provides access to Genesis Block, SMK genes, Mutations, and blockchain metadata.

Philosophy: "The genome is the collective memory - queryable, verifiable, immutable"
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType, DNABlock

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/dna", tags=["GENOMOS DNA Blockchain"])

# Global blockchain instance (initialized on startup)
_blockchain: Optional[AgentDNAChain] = None


def initialize_dna_blockchain(db_path: str = "./data/genomos.db"):
    """Initialize the GENOMOS blockchain for API access"""
    global _blockchain
    try:
        _blockchain = AgentDNAChain(db_path=db_path)
        logger.info(f"🧬 GENOMOS DNA API initialized: {len(_blockchain.chain)} genes")
        return _blockchain
    except Exception as e:
        logger.error(f"❌ Failed to initialize GENOMOS blockchain: {e}")
        _blockchain = None
        return None


def get_blockchain() -> AgentDNAChain:
    """Get blockchain instance or raise error"""
    if _blockchain is None:
        raise HTTPException(
            status_code=503,
            detail="GENOMOS blockchain not available. Initialize blockchain first."
        )
    return _blockchain


# Response Models
class BlockResponse(BaseModel):
    """Response model for a single DNA block"""
    index: int
    timestamp: str
    gene_type: str
    agent: Optional[str]
    tags: List[str]
    hash: str
    previous_hash: str
    data: Dict[str, Any]


class GenesisResponse(BaseModel):
    """Response model for Genesis Block"""
    block_index: int
    constitution_version: str
    title: str
    ratified: str
    agents: List[str]
    core_principles: List[str]
    three_gates: List[str]
    hash: str
    timestamp: str


class SMKResponse(BaseModel):
    """Response model for SMK gene"""
    smk_number: str
    title: str
    block_index: int
    author: Any  # Can be string or list
    date: str
    version: str
    tags: List[str]
    references: List[str]
    hash: str
    timestamp: str


class MutationResponse(BaseModel):
    """Response model for Mutation gene"""
    mutation_id: str
    block_index: int
    agent: str
    operation_type: str
    target: str
    action: str
    success: bool
    validation_outcome: str
    timestamp: str
    hash: str


class BlockchainInfoResponse(BaseModel):
    """Response model for blockchain metadata"""
    total_genes: int
    genesis_hash: str
    latest_hash: str
    merkle_root: str
    is_valid: bool
    gene_counts: Dict[str, int]
    agents: List[str]
    database_path: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/info", response_model=BlockchainInfoResponse)
async def get_blockchain_info():
    """
    Get overall blockchain metadata and statistics.

    Returns information about the entire GENOMOS blockchain:
    - Total gene count
    - Genesis and latest hashes
    - Merkle root for verification
    - Gene type breakdown
    - Active agents
    """
    chain = get_blockchain()

    # Count genes by type
    gene_counts = {}
    agents = set()

    for block in chain.chain:
        gene_type = block.gene_type.value
        gene_counts[gene_type] = gene_counts.get(gene_type, 0) + 1

        if block.agent:
            agents.add(block.agent)

    return BlockchainInfoResponse(
        total_genes=len(chain.chain),
        genesis_hash=chain.chain[0].hash if chain.chain else "",
        latest_hash=chain.get_latest_block().hash,
        merkle_root=chain.get_merkle_root(),
        is_valid=chain.validate_chain(),
        gene_counts=gene_counts,
        agents=sorted(list(agents)),
        database_path=chain.db_path
    )


@router.get("/validate")
async def validate_blockchain():
    """
    Validate blockchain integrity.

    Performs cryptographic validation:
    - SHA-256 hash verification for each block
    - Chain linkage verification (previous_hash matches)
    - Merkle root calculation

    Returns validation status and any errors found.
    """
    chain = get_blockchain()

    is_valid = chain.validate_chain()
    merkle_root = chain.get_merkle_root()

    # Detailed validation
    errors = []
    for i in range(1, len(chain.chain)):
        current = chain.chain[i]
        previous = chain.chain[i - 1]

        if current.previous_hash != previous.hash:
            errors.append(f"Block {i}: Chain linkage broken")

        if not current.verify_hash():
            errors.append(f"Block {i}: Hash verification failed")

    return {
        "valid": is_valid and len(errors) == 0,
        "total_blocks": len(chain.chain),
        "merkle_root": merkle_root,
        "errors": errors,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/genesis", response_model=GenesisResponse)
async def get_genesis():
    """
    Get the Genesis Block (Constitution V1.1).

    The Genesis Block contains:
    - Homo Lumen Constitution
    - Core principles
    - Three Triadiske Portvokter
    - Founding agents
    - Ratification date
    """
    chain = get_blockchain()

    genesis = chain.chain[0]

    if genesis.gene_type != GeneType.GENESIS:
        raise HTTPException(
            status_code=500,
            detail="Genesis block not found or corrupted"
        )

    data = genesis.data

    return GenesisResponse(
        block_index=genesis.index,
        constitution_version=data.get("version", "1.1"),
        title=data.get("title", "Homo Lumen Constitution"),
        ratified=data.get("ratified", ""),
        agents=data.get("agents", []),
        core_principles=data.get("core_principles", []),
        three_gates=data.get("three_gates", []),
        hash=genesis.hash,
        timestamp=genesis.timestamp
    )


@router.get("/smk", response_model=List[SMKResponse])
async def get_all_smks(
    limit: int = Query(100, description="Maximum number of SMKs to return"),
    agent: Optional[str] = Query(None, description="Filter by author agent")
):
    """
    Get all SMK (Symbiotisk Minne Kompresjon) genes.

    SMKs are knowledge documents that form the collective memory.
    Each SMK is a permanent gene in the blockchain.

    Query parameters:
    - limit: Max number of results (default 100)
    - agent: Filter by author agent
    """
    chain = get_blockchain()

    smk_blocks = [
        block for block in chain.chain
        if block.gene_type == GeneType.SMK
    ]

    # Filter by agent if specified
    if agent:
        smk_blocks = [b for b in smk_blocks if b.agent == agent.lower()]

    # Apply limit
    smk_blocks = smk_blocks[:limit]

    results = []
    for block in smk_blocks:
        data = block.data
        results.append(SMKResponse(
            smk_number=data.get("smk_number", "unknown"),
            title=data.get("title", "Untitled"),
            block_index=block.index,
            author=data.get("author", "Unknown"),
            date=data.get("date", ""),
            version=data.get("version", "1.0"),
            tags=block.tags or [],
            references=data.get("references", []),
            hash=block.hash,
            timestamp=block.timestamp
        ))

    return results


@router.get("/smk/{smk_number}", response_model=SMKResponse)
async def get_smk_by_number(smk_number: str):
    """
    Get a specific SMK by number.

    Examples:
    - /api/dna/smk/019 - Constitution
    - /api/dna/smk/032 - CSN Server First Activation
    - /api/dna/smk/042 - Aurora Hexagonal Intelligence
    """
    chain = get_blockchain()

    # Find SMK with matching number
    for block in chain.chain:
        if block.gene_type == GeneType.SMK:
            if block.data.get("smk_number") == smk_number:
                data = block.data
                return SMKResponse(
                    smk_number=data.get("smk_number", smk_number),
                    title=data.get("title", "Untitled"),
                    block_index=block.index,
                    author=data.get("author", "Unknown"),
                    date=data.get("date", ""),
                    version=data.get("version", "1.0"),
                    tags=block.tags or [],
                    references=data.get("references", []),
                    hash=block.hash,
                    timestamp=block.timestamp
                )

    raise HTTPException(
        status_code=404,
        detail=f"SMK #{smk_number} not found in blockchain"
    )


@router.get("/mutations", response_model=List[MutationResponse])
async def get_mutations(
    agent: Optional[str] = Query(None, description="Filter by agent"),
    operation_type: Optional[str] = Query(None, description="Filter by operation type"),
    success: Optional[bool] = Query(None, description="Filter by success status"),
    limit: int = Query(100, description="Maximum number of results")
):
    """
    Query mutation genes (audit trail).

    Mutations represent all critical operations performed by agents.
    Each mutation is immutably recorded in the blockchain.

    Query parameters:
    - agent: Filter by agent name
    - operation_type: Filter by type (read, write, delete, etc.)
    - success: Filter by success status (true/false)
    - limit: Max results (default 100)
    """
    chain = get_blockchain()

    mutation_blocks = [
        block for block in chain.chain
        if block.gene_type == GeneType.MUTATION
    ]

    # Apply filters
    if agent:
        mutation_blocks = [b for b in mutation_blocks if b.agent == agent.lower()]

    if operation_type:
        mutation_blocks = [
            b for b in mutation_blocks
            if b.data.get("operation_type") == operation_type
        ]

    if success is not None:
        mutation_blocks = [
            b for b in mutation_blocks
            if b.data.get("success") == success
        ]

    # Sort by most recent first
    mutation_blocks = sorted(
        mutation_blocks,
        key=lambda b: b.timestamp,
        reverse=True
    )

    # Apply limit
    mutation_blocks = mutation_blocks[:limit]

    results = []
    for block in mutation_blocks:
        data = block.data
        results.append(MutationResponse(
            mutation_id=data.get("mutation_id", ""),
            block_index=block.index,
            agent=block.agent or "unknown",
            operation_type=data.get("operation_type", ""),
            target=data.get("target", ""),
            action=data.get("action", ""),
            success=data.get("success", False),
            validation_outcome=data.get("validation_outcome", ""),
            timestamp=data.get("timestamp", block.timestamp),
            hash=block.hash
        ))

    return results


@router.get("/blocks/{index}", response_model=BlockResponse)
async def get_block_by_index(index: int):
    """
    Get a specific block by index.

    Index 0 is always the Genesis Block.
    Subsequent blocks are SMKs, Mutations, and other gene types.
    """
    chain = get_blockchain()

    if index < 0 or index >= len(chain.chain):
        raise HTTPException(
            status_code=404,
            detail=f"Block index {index} out of range (0-{len(chain.chain)-1})"
        )

    block = chain.chain[index]

    return BlockResponse(
        index=block.index,
        timestamp=block.timestamp,
        gene_type=block.gene_type.value,
        agent=block.agent,
        tags=block.tags or [],
        hash=block.hash,
        previous_hash=block.previous_hash,
        data=block.data
    )


@router.get("/lineage/{smk_number}")
async def get_smk_lineage(smk_number: str):
    """
    Get the lineage (related SMKs) for a given SMK.

    Returns:
    - The SMK itself
    - All SMKs it references
    - All SMKs that reference it
    """
    chain = get_blockchain()

    # Find the target SMK
    target_smk = None
    for block in chain.chain:
        if block.gene_type == GeneType.SMK:
            if block.data.get("smk_number") == smk_number:
                target_smk = block
                break

    if not target_smk:
        raise HTTPException(
            status_code=404,
            detail=f"SMK #{smk_number} not found"
        )

    # Get references (SMKs this one points to)
    references = target_smk.data.get("references", [])

    # Get backlinks (SMKs that point to this one)
    backlinks = []
    for block in chain.chain:
        if block.gene_type == GeneType.SMK:
            if smk_number in block.data.get("references", []):
                backlinks.append(block.data.get("smk_number"))

    return {
        "smk_number": smk_number,
        "title": target_smk.data.get("title", "Untitled"),
        "block_index": target_smk.index,
        "references": references,
        "referenced_by": backlinks,
        "total_connections": len(references) + len(backlinks)
    }
