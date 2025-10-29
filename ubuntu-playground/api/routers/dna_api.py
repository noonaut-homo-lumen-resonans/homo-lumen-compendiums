"""
GENOMOS DNA API Router

REST API endpoints for querying the Agent DNA Blockchain.
Provides access to Genesis Block, SMK genes, Mutations, and blockchain metadata.

Philosophy: "The genome is the collective memory - queryable, verifiable, immutable"
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Generic, TypeVar
from datetime import datetime
import logging

from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType, DNABlock
from models.knowledge_graph import (
    KnowledgeGraph, GraphNode, GraphEdge, ConsultationSimilarity,
    BlockchainAnalytics, TimelineDataPoint, TimelineAnalytics
)
from blockchain.consultation_recommender import find_related_consultations
from blockchain.backup_manager import BackupManager
from blockchain.cache_manager import get_cache_manager, invalidate_lru_caches
from fastapi.responses import Response

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/dna", tags=["GENOMOS DNA Blockchain"])

# Global blockchain instance (initialized on startup)
_blockchain: Optional[AgentDNAChain] = None

# Global cache manager instance (Phase 10: Performance Optimization)
_cache_manager = get_cache_manager(ttl_seconds=300)  # 5 minute default TTL


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
    date: Optional[str] = "unknown"
    version: str = "1.0"
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


class ConsultationResponse(BaseModel):
    """Response model for Consultation gene"""
    consultation_id: str
    block_index: int
    human_query: str
    agent_count: int  # Number of agents who responded
    synthesis_summary: Optional[str]
    related_smk: List[str]
    has_biofelt_context: bool
    has_thalos_validation: bool
    timestamp: str
    hash: str


class AgentLearningResponse(BaseModel):
    """Response model for Agent Learning gene"""
    learning_id: str
    block_index: int
    agent_name: str
    learning_event_type: str
    context: str
    has_before_state: bool
    has_after_state: bool
    has_metrics: bool
    related_smk: List[str]
    related_consultations: List[str]
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


# PHASE 10: Performance Optimization - Pagination Support
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model (Phase 10: Performance Optimization)"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool


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
            date=data.get("date") or "unknown",
            version=data.get("version") or "1.0",
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


# ============================================================================
# CONSULTATION ENDPOINTS (GENOMOS Phase 7)
# ============================================================================

@router.get("/consultations", response_model=List[ConsultationResponse])
async def get_consultations(
    query: Optional[str] = Query(None, description="Search in human query text"),
    agent: Optional[str] = Query(None, description="Filter by agent name"),
    from_date: Optional[str] = Query(None, description="Filter consultations after this ISO date"),
    limit: int = Query(50, description="Maximum number of consultations to return")
):
    """
    Get all consultation genes from the blockchain.

    Query parameters:
    - query: Search term to filter by human query text
    - agent: Filter consultations where this agent participated
    - from_date: Only show consultations after this date (ISO format)
    - limit: Maximum results to return (default 50)
    """
    chain = get_blockchain()

    # Filter consultation blocks
    consultation_blocks = [
        block for block in chain.chain
        if block.gene_type == GeneType.CONSULTATION
    ]

    # Apply query filter
    if query:
        consultation_blocks = [
            b for b in consultation_blocks
            if query.lower() in b.data.get("human_query", "").lower()
        ]

    # Apply agent filter
    if agent:
        consultation_blocks = [
            b for b in consultation_blocks
            if agent.lower() in b.data.get("agent_responses", {}).keys()
        ]

    # Apply date filter
    if from_date:
        consultation_blocks = [
            b for b in consultation_blocks
            if b.timestamp >= from_date
        ]

    # Apply limit
    consultation_blocks = consultation_blocks[-limit:]  # Get most recent

    # Build responses
    results = []
    for block in consultation_blocks:
        data = block.data
        agent_responses = data.get("agent_responses", {})
        synthesis = data.get("synthesis", {})

        results.append(ConsultationResponse(
            consultation_id=data.get("consultation_id", "unknown"),
            block_index=block.index,
            human_query=data.get("human_query", ""),
            agent_count=len(agent_responses),
            synthesis_summary=synthesis.get("summary"),
            related_smk=synthesis.get("related_smk", []),
            has_biofelt_context="biofelt_context" in data,
            has_thalos_validation="thalos_validation" in data,
            timestamp=block.timestamp,
            hash=block.hash
        ))

    return results


@router.get("/consultations/{consultation_id}")
async def get_consultation(consultation_id: str):
    """
    Get a specific consultation by ID.

    Returns the full consultation data including all agent responses.
    """
    chain = get_blockchain()

    # Find consultation block
    for block in chain.chain:
        if block.gene_type == GeneType.CONSULTATION:
            if block.data.get("consultation_id") == consultation_id:
                return {
                    "consultation_id": consultation_id,
                    "block_index": block.index,
                    "timestamp": block.timestamp,
                    "human_query": block.data.get("human_query"),
                    "agent_responses": block.data.get("agent_responses", {}),
                    "synthesis": block.data.get("synthesis", {}),
                    "biofelt_context": block.data.get("biofelt_context"),
                    "thalos_validation": block.data.get("thalos_validation"),
                    "hash": block.hash,
                    "previous_hash": block.previous_hash
                }

    raise HTTPException(
        status_code=404,
        detail=f"Consultation {consultation_id} not found"
    )


@router.get("/consultations/related-to-smk/{smk_number}")
async def get_consultations_by_smk(
    smk_number: str,
    limit: int = Query(20, description="Maximum consultations to return")
):
    """
    Get all consultations that reference a specific SMK.

    Useful for seeing how a knowledge document has been used in conversations.
    """
    chain = get_blockchain()

    # Find consultations that reference this SMK
    related_consultations = []
    for block in chain.chain:
        if block.gene_type == GeneType.CONSULTATION:
            synthesis = block.data.get("synthesis", {})
            related_smk = synthesis.get("related_smk", [])

            # Check if SMK is referenced
            if f"SMK#{smk_number}" in related_smk or smk_number in related_smk:
                related_consultations.append({
                    "consultation_id": block.data.get("consultation_id"),
                    "human_query": block.data.get("human_query"),
                    "timestamp": block.timestamp,
                    "block_index": block.index,
                    "hash": block.hash[:16] + "..."
                })

    if not related_consultations:
        return {
            "smk_number": smk_number,
            "consultations": [],
            "total_references": 0
        }

    # Apply limit and return most recent first
    related_consultations = related_consultations[-limit:]

    return {
        "smk_number": smk_number,
        "consultations": related_consultations,
        "total_references": len(related_consultations)
    }


# ============================================================================
# AGENT LEARNING ENDPOINTS (GENOMOS Phase 5)
# ============================================================================

@router.get("/learning", response_model=List[AgentLearningResponse])
async def get_agent_learning(
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    learning_type: Optional[str] = Query(None, description="Filter by learning event type"),
    from_date: Optional[str] = Query(None, description="Filter learning events after this ISO date"),
    limit: int = Query(50, description="Maximum number of learning events to return")
):
    """
    Get all agent learning events from the blockchain.

    Query parameters:
    - agent_name: Filter by specific agent
    - learning_type: Filter by event type (feedback_correction, pattern_discovery, etc.)
    - from_date: Only show events after this date (ISO format)
    - limit: Maximum results to return (default 50)
    """
    chain = get_blockchain()

    # Filter learning blocks
    learning_blocks = [
        block for block in chain.chain
        if block.gene_type == GeneType.AGENT_LEARNING
    ]

    # Apply agent filter
    if agent_name:
        learning_blocks = [
            b for b in learning_blocks
            if b.data.get("agent_name", "").lower() == agent_name.lower()
        ]

    # Apply learning type filter
    if learning_type:
        learning_blocks = [
            b for b in learning_blocks
            if b.data.get("learning_event_type", "").lower() == learning_type.lower()
        ]

    # Apply date filter
    if from_date:
        learning_blocks = [
            b for b in learning_blocks
            if b.timestamp >= from_date
        ]

    # Apply limit
    learning_blocks = learning_blocks[-limit:]  # Get most recent

    # Build responses
    results = []
    for block in learning_blocks:
        data = block.data
        results.append(AgentLearningResponse(
            learning_id=data.get("learning_id", "unknown"),
            block_index=block.index,
            agent_name=data.get("agent_name", "unknown"),
            learning_event_type=data.get("learning_event_type", "unknown"),
            context=data.get("context", ""),
            has_before_state="before_state" in data,
            has_after_state="after_state" in data,
            has_metrics="metrics" in data,
            related_smk=data.get("related_smk", []),
            related_consultations=data.get("related_consultations", []),
            timestamp=block.timestamp,
            hash=block.hash
        ))

    return results


@router.get("/learning/{learning_id}")
async def get_learning_event(learning_id: str):
    """
    Get a specific learning event by ID.

    Returns the full learning data including before/after states and metrics.
    """
    chain = get_blockchain()

    # Find learning block
    for block in chain.chain:
        if block.gene_type == GeneType.AGENT_LEARNING:
            if block.data.get("learning_id") == learning_id:
                return {
                    "learning_id": learning_id,
                    "block_index": block.index,
                    "timestamp": block.timestamp,
                    "agent_name": block.data.get("agent_name"),
                    "learning_event_type": block.data.get("learning_event_type"),
                    "context": block.data.get("context"),
                    "before_state": block.data.get("before_state"),
                    "after_state": block.data.get("after_state"),
                    "trigger": block.data.get("trigger"),
                    "metrics": block.data.get("metrics"),
                    "related_smk": block.data.get("related_smk", []),
                    "related_consultations": block.data.get("related_consultations", []),
                    "hash": block.hash,
                    "previous_hash": block.previous_hash
                }

    raise HTTPException(
        status_code=404,
        detail=f"Learning event {learning_id} not found"
    )


@router.get("/learning/agent/{agent_name}/evolution")
async def get_agent_evolution(
    agent_name: str,
    limit: int = Query(100, description="Maximum learning events to return")
):
    """
    Get the learning evolution timeline for a specific agent.

    Returns all learning events for the agent in chronological order,
    showing how the agent has adapted and improved over time.
    """
    chain = get_blockchain()

    # Find all learning events for this agent
    agent_learning = []
    for block in chain.chain:
        if block.gene_type == GeneType.AGENT_LEARNING:
            if block.data.get("agent_name", "").lower() == agent_name.lower():
                agent_learning.append({
                    "learning_id": block.data.get("learning_id"),
                    "learning_event_type": block.data.get("learning_event_type"),
                    "context": block.data.get("context"),
                    "metrics": block.data.get("metrics"),
                    "timestamp": block.timestamp,
                    "block_index": block.index,
                    "hash": block.hash[:16] + "..."
                })

    if not agent_learning:
        return {
            "agent_name": agent_name,
            "learning_events": [],
            "total_events": 0,
            "evolution_summary": f"No learning events found for agent '{agent_name}'"
        }

    # Apply limit (most recent)
    agent_learning = agent_learning[-limit:]

    # Calculate evolution summary
    event_types = {}
    for event in agent_learning:
        event_type = event.get("learning_event_type", "unknown")
        event_types[event_type] = event_types.get(event_type, 0) + 1

    return {
        "agent_name": agent_name,
        "learning_events": agent_learning,
        "total_events": len(agent_learning),
        "event_type_distribution": event_types,
        "evolution_summary": f"{agent_name} has {len(agent_learning)} recorded learning events"
    }


# ============================================================================
# KNOWLEDGE GRAPH ENDPOINTS (GENOMOS Phase 6)
# ============================================================================

@router.get("/graph/smk-network", response_model=KnowledgeGraph)
async def get_smk_network():
    """
    Get the complete SMK reference network as a graph.

    Returns nodes (SMKs) and edges (references between SMKs)
    in a format suitable for D3.js, Cytoscape.js visualization.

    **GENOMOS Phase 6: Cross-References & Lineage Tracking**
    """
    chain = get_blockchain()

    nodes = []
    edges = []
    node_types = {}
    edge_types = {}

    # Create nodes for all SMKs
    smk_blocks = {}
    for block in chain.chain:
        if block.gene_type == GeneType.SMK:
            smk_num = block.data.get("smk_number", "unknown")
            title = block.data.get("title", f"SMK {smk_num}")

            # Calculate node size based on how many times it's referenced
            # (we'll update this in the edges loop)
            node_id = f"smk-{smk_num}"
            smk_blocks[smk_num] = block

            nodes.append(GraphNode(
                id=node_id,
                type="smk",
                label=f"SMK#{smk_num}",
                title=title,
                size=10.0,  # Base size, will be updated
                color="#4CAF50",  # Green for SMK
                created_at=block.timestamp,
                metadata={
                    "block_index": block.index,
                    "hash": block.hash[:16] + "..."
                }
            ))

            node_types["smk"] = node_types.get("smk", 0) + 1

    # Create edges for SMK references
    reference_counts = {}  # Track incoming references for sizing
    edge_id = 0

    for smk_num, block in smk_blocks.items():
        references = block.data.get("references", [])
        source_id = f"smk-{smk_num}"

        for ref_num in references:
            target_id = f"smk-{ref_num}"

            # Only create edge if target exists
            if ref_num in smk_blocks:
                edge_id += 1
                edges.append(GraphEdge(
                    id=f"edge-{edge_id}",
                    source=source_id,
                    target=target_id,
                    type="references",
                    weight=1.0,
                    label="references"
                ))

                edge_types["references"] = edge_types.get("references", 0) + 1

                # Track incoming references for node sizing
                reference_counts[ref_num] = reference_counts.get(ref_num, 0) + 1

    # Update node sizes based on reference counts (centrality)
    for node in nodes:
        if node.type == "smk":
            smk_num = node.id.replace("smk-", "")
            ref_count = reference_counts.get(smk_num, 0)
            # Size scales with references: 10 + (references * 3)
            node.size = 10.0 + (ref_count * 3.0)

    return KnowledgeGraph(
        nodes=nodes,
        edges=edges,
        total_nodes=len(nodes),
        total_edges=len(edges),
        node_types=node_types,
        edge_types=edge_types,
        generated_at=datetime.now().isoformat(),
        metadata={
            "description": "SMK reference network showing knowledge dependencies",
            "most_referenced": sorted(reference_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    )


@router.get("/graph/consultation-knowledge-flow", response_model=KnowledgeGraph)
async def get_consultation_knowledge_flow():
    """
    Get the knowledge flow graph showing how consultations connect to SMKs.

    Returns:
    - SMK nodes
    - Consultation nodes
    - Edges showing which consultations reference which SMKs

    **GENOMOS Phase 6: Cross-References & Lineage Tracking**
    """
    chain = get_blockchain()

    nodes = []
    edges = []
    node_types = {}
    edge_types = {}
    edge_id = 0

    # Add SMK nodes
    smk_nodes = {}
    for block in chain.chain:
        if block.gene_type == GeneType.SMK:
            smk_num = block.data.get("smk_number", "unknown")
            node_id = f"smk-{smk_num}"
            smk_nodes[smk_num] = node_id

            nodes.append(GraphNode(
                id=node_id,
                type="smk",
                label=f"SMK#{smk_num}",
                title=block.data.get("title", ""),
                size=15.0,
                color="#4CAF50",
                created_at=block.timestamp
            ))

            node_types["smk"] = node_types.get("smk", 0) + 1

    # Add consultation nodes and edges
    for block in chain.chain:
        if block.gene_type == GeneType.CONSULTATION:
            consultation_id = block.data.get("consultation_id", "unknown")
            node_id = f"consultation-{consultation_id}"

            # Truncate query for label
            query = block.data.get("human_query", "")
            label = query[:40] + "..." if len(query) > 40 else query

            nodes.append(GraphNode(
                id=node_id,
                type="consultation",
                label=label,
                title=query,
                size=12.0,
                color="#2196F3",  # Blue for consultations
                created_at=block.timestamp,
                metadata={
                    "block_index": block.index,
                    "agent_count": len(block.data.get("agent_responses", {}))
                }
            ))

            node_types["consultation"] = node_types.get("consultation", 0) + 1

            # Create edges to referenced SMKs
            synthesis = block.data.get("synthesis", {})
            related_smk = synthesis.get("related_smk", [])

            for smk_ref in related_smk:
                # Extract SMK number from "SMK#043" format
                import re
                match = re.search(r'(\d+)', smk_ref)
                if match:
                    smk_num = match.group(1).zfill(3)
                    if smk_num in smk_nodes:
                        edge_id += 1
                        edges.append(GraphEdge(
                            id=f"edge-{edge_id}",
                            source=node_id,
                            target=smk_nodes[smk_num],
                            type="cites",
                            weight=1.0,
                            label="cites"
                        ))

                        edge_types["cites"] = edge_types.get("cites", 0) + 1

    return KnowledgeGraph(
        nodes=nodes,
        edges=edges,
        total_nodes=len(nodes),
        total_edges=len(edges),
        node_types=node_types,
        edge_types=edge_types,
        generated_at=datetime.now().isoformat(),
        metadata={
            "description": "Consultation-to-SMK knowledge flow showing how documents are used in conversations"
        }
    )


@router.get("/consultations/{consultation_id}/related", response_model=List[ConsultationSimilarity])
async def get_related_consultations(
    consultation_id: str,
    limit: int = Query(10, description="Maximum number of similar consultations to return"),
    min_score: float = Query(0.1, ge=0.0, le=1.0, description="Minimum similarity score threshold")
):
    """
    Find consultations similar to the specified one.

    Uses multiple similarity metrics:
    - Shared SMK references (60% weight)
    - Shared agents (20% weight)
    - Query text similarity (20% weight)

    **GENOMOS Phase 6: Cross-References & Lineage Tracking**
    """
    try:
        chain = get_blockchain()
        related = find_related_consultations(
            consultation_id=consultation_id,
            blockchain=chain,
            limit=limit,
            min_score=min_score
        )
        return related
    except Exception as e:
        logger.error(f"Error finding related consultations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to find related consultations: {str(e)}")


# ============================================================================
# ANALYTICS ENDPOINTS (GENOMOS Phase 8)
# ============================================================================

@router.get("/analytics/overview", response_model=BlockchainAnalytics)
async def get_blockchain_analytics():
    """
    Get comprehensive blockchain analytics and statistics.

    Returns overview of blockchain health, growth metrics, gene distribution,
    and agent activity.

    **GENOMOS Phase 8: Visualization & Analytics**
    """
    chain = get_blockchain()
    now = datetime.now()

    # Calculate basic stats
    total_blocks = len(chain.chain)
    total_genes = total_blocks - 1  # Excluding genesis

    # Get dates
    genesis_block = chain.chain[0]
    latest_block = chain.chain[-1]
    genesis_date = genesis_block.timestamp
    latest_date = latest_block.timestamp

    # Calculate chain age
    genesis_dt = datetime.fromisoformat(genesis_date.replace('Z', '+00:00'))
    latest_dt = datetime.fromisoformat(latest_date.replace('Z', '+00:00'))
    chain_age_days = (latest_dt - genesis_dt).total_seconds() / 86400

    # Gene distribution
    gene_distribution = {}
    agent_activity = {}

    for block in chain.chain[1:]:  # Skip genesis
        gene_type = block.gene_type.value if hasattr(block.gene_type, 'value') else str(block.gene_type)
        gene_distribution[gene_type] = gene_distribution.get(gene_type, 0) + 1

        agent = block.agent if hasattr(block, 'agent') else "unknown"
        agent_activity[agent] = agent_activity.get(agent, 0) + 1

    # Calculate growth metrics
    avg_blocks_per_day = total_genes / max(chain_age_days, 1)

    # Count recent blocks
    blocks_last_24h = 0
    blocks_last_7d = 0
    cutoff_24h = now.timestamp() - 86400
    cutoff_7d = now.timestamp() - (86400 * 7)

    for block in chain.chain[1:]:
        try:
            block_dt = datetime.fromisoformat(block.timestamp.replace('Z', '+00:00'))
            block_ts = block_dt.timestamp()
            if block_ts >= cutoff_24h:
                blocks_last_24h += 1
            if block_ts >= cutoff_7d:
                blocks_last_7d += 1
        except:
            pass

    # Top agents
    top_agents = [
        {"agent": agent, "blocks": count}
        for agent, count in sorted(agent_activity.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    # Blockchain health assessment
    if chain.is_valid():
        blockchain_health = "healthy"
    else:
        blockchain_health = "corrupted"

    return BlockchainAnalytics(
        total_blocks=total_blocks,
        total_genes=total_genes,
        genesis_date=genesis_date,
        latest_block_date=latest_date,
        chain_age_days=round(chain_age_days, 2),
        gene_distribution=gene_distribution,
        agent_activity=agent_activity,
        avg_blocks_per_day=round(avg_blocks_per_day, 2),
        blocks_last_24h=blocks_last_24h,
        blocks_last_7d=blocks_last_7d,
        top_agents=top_agents,
        blockchain_health=blockchain_health,
        generated_at=now.isoformat()
    )


@router.get("/analytics/timeline", response_model=TimelineAnalytics)
async def get_blockchain_timeline():
    """
    Get blockchain growth timeline showing daily activity.

    Returns daily data points with cumulative and new block counts,
    plus gene type distribution per day.

    **GENOMOS Phase 8: Visualization & Analytics**
    """
    chain = get_blockchain()

    # Group blocks by date
    daily_data = {}

    for idx, block in enumerate(chain.chain):
        try:
            block_dt = datetime.fromisoformat(block.timestamp.replace('Z', '+00:00'))
            date_key = block_dt.date().isoformat()

            if date_key not in daily_data:
                daily_data[date_key] = {
                    "new_blocks": 0,
                    "gene_types": {}
                }

            daily_data[date_key]["new_blocks"] += 1

            # Track gene types (skip genesis)
            if idx > 0:
                gene_type = block.gene_type.value if hasattr(block.gene_type, 'value') else str(block.gene_type)
                daily_data[date_key]["gene_types"][gene_type] = daily_data[date_key]["gene_types"].get(gene_type, 0) + 1

        except Exception as e:
            logger.warning(f"Failed to parse timestamp for block {idx}: {e}")
            continue

    # Build timeline with cumulative counts
    sorted_dates = sorted(daily_data.keys())
    timeline = []
    cumulative = 0

    for date in sorted_dates:
        data = daily_data[date]
        cumulative += data["new_blocks"]

        timeline.append(TimelineDataPoint(
            date=date,
            cumulative_blocks=cumulative,
            new_blocks=data["new_blocks"],
            gene_types=data["gene_types"]
        ))

    # Find peak activity
    peak_date = None
    peak_count = 0
    for date, data in daily_data.items():
        if data["new_blocks"] > peak_count:
            peak_count = data["new_blocks"]
            peak_date = date

    return TimelineAnalytics(
        timeline=timeline,
        total_days=len(sorted_dates),
        start_date=sorted_dates[0] if sorted_dates else "",
        end_date=sorted_dates[-1] if sorted_dates else "",
        peak_activity_date=peak_date,
        peak_activity_count=peak_count,
        generated_at=datetime.now().isoformat()
    )


# ============================================================================
# PHASE 9: Export & Backup Systems
# ============================================================================

@router.get("/export/json")
async def export_blockchain_json(
    include_genesis: bool = Query(True, description="Include genesis block"),
    gene_types: Optional[str] = Query(None, description="Comma-separated gene types to filter (e.g., 'smk,consultation')"),
    pretty: bool = Query(True, description="Pretty-print JSON output")
):
    """
    Export blockchain to JSON format.

    GENOMOS Phase 9: Export & Backup Systems

    Query Parameters:
    - include_genesis: Whether to include the genesis block (default: True)
    - gene_types: Filter by specific gene types (None = all types)
    - pretty: Pretty-print JSON vs compact format (default: True)

    Returns:
    - JSON object with blockchain data, metadata, and blockchain info
    """
    try:
        # Parse gene types filter
        gene_type_list = None
        if gene_types:
            gene_type_list = [gt.strip() for gt in gene_types.split(",")]

        # Get blockchain instance and create backup manager
        blockchain = get_blockchain()
        backup_mgr = BackupManager(blockchain=blockchain)
        export_data = backup_mgr.export_to_json(
            include_genesis=include_genesis,
            gene_types=gene_type_list,
            pretty=pretty
        )

        return export_data

    except Exception as e:
        logger.error(f"Error exporting blockchain to JSON: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/export/csv")
async def export_blockchain_csv(
    include_genesis: bool = Query(True, description="Include genesis block"),
    gene_types: Optional[str] = Query(None, description="Comma-separated gene types to filter")
):
    """
    Export blockchain to CSV format.

    GENOMOS Phase 9: Export & Backup Systems

    Query Parameters:
    - include_genesis: Whether to include the genesis block (default: True)
    - gene_types: Filter by specific gene types (None = all types)

    Returns:
    - CSV file as text/csv download
    """
    try:
        # Parse gene types filter
        gene_type_list = None
        if gene_types:
            gene_type_list = [gt.strip() for gt in gene_types.split(",")]

        # Get blockchain instance and create backup manager
        blockchain = get_blockchain()
        backup_mgr = BackupManager(blockchain=blockchain)
        csv_content = backup_mgr.export_to_csv(
            output_path=None,  # Return string, don't save to file
            include_genesis=include_genesis,
            gene_types=gene_type_list
        )

        # Return as downloadable CSV
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=genomos_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )

    except Exception as e:
        logger.error(f"Error exporting blockchain to CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")


@router.post("/backup/create")
async def create_blockchain_backup(
    backup_dir: str = Query("./backups", description="Directory to store backup files"),
    include_metadata: bool = Query(True, description="Include blockchain metadata")
):
    """
    Create a complete blockchain backup with cryptographic verification.

    GENOMOS Phase 9: Export & Backup Systems

    Creates:
    - Timestamped JSON backup file (genomos_backup_YYYYMMDD_HHMMSS.json)
    - SHA-256 verification file (.sha256)

    Query Parameters:
    - backup_dir: Directory to store backup files (default: ./backups)
    - include_metadata: Include blockchain metadata (default: True)

    Returns:
    - Backup information including file paths, hash, and statistics
    """
    try:
        # Get blockchain instance and create backup manager
        blockchain = get_blockchain()
        backup_mgr = BackupManager(blockchain=blockchain)
        backup_info = backup_mgr.create_backup(
            backup_dir=backup_dir,
            include_metadata=include_metadata
        )

        logger.info(f"✅ Backup created: {backup_info['backup_file']}")
        logger.info(f"🔒 SHA-256: {backup_info['backup_hash'][:16]}...")

        return backup_info

    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Backup creation failed: {str(e)}")


@router.post("/backup/verify")
async def verify_blockchain_backup(
    backup_filepath: str = Query(..., description="Path to backup JSON file to verify")
):
    """
    Verify backup integrity using SHA-256 checksum.

    GENOMOS Phase 9: Export & Backup Systems

    Verifies:
    - Backup file exists
    - SHA-256 hash matches verification file
    - File integrity is intact

    Query Parameters:
    - backup_filepath: Path to the backup JSON file

    Returns:
    - Verification results with hash comparison
    """
    try:
        # Get blockchain instance and create backup manager
        blockchain = get_blockchain()
        backup_mgr = BackupManager(blockchain=blockchain)
        verification_result = backup_mgr.verify_backup(backup_filepath)

        if verification_result.get("valid") is True:
            logger.info(f"✅ Backup verification passed: {backup_filepath}")
        elif verification_result.get("valid") is False:
            logger.warning(f"❌ Backup verification FAILED: {backup_filepath}")
        else:
            logger.warning(f"⚠️ Backup verification inconclusive (no .sha256 file): {backup_filepath}")

        return verification_result

    except Exception as e:
        logger.error(f"Error verifying backup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Backup verification failed: {str(e)}")


@router.get("/backup/statistics")
async def get_backup_statistics():
    """
    Get statistics about blockchain for backup planning.

    GENOMOS Phase 9: Export & Backup Systems

    Returns:
    - Total blocks and gene distribution
    - Estimated backup size (bytes, KB, MB)
    - Blockchain health status
    - Genesis and latest hashes
    """
    try:
        # Get blockchain instance and create backup manager
        blockchain = get_blockchain()
        backup_mgr = BackupManager(blockchain=blockchain)
        stats = backup_mgr.get_backup_statistics()

        return stats

    except Exception as e:
        logger.error(f"Error getting backup statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


# ============================================================================
# PHASE 10: Performance Optimization - Cache Management
# ============================================================================

@router.get("/cache/stats")
async def get_cache_statistics():
    """
    Get cache performance statistics.

    GENOMOS Phase 10: Performance Optimization

    Returns:
    - Total entries, hits, misses, hit rate
    - Cache invalidations and evictions
    - Overall cache performance metrics
    """
    try:
        stats = _cache_manager.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache stats: {str(e)}")


@router.get("/cache/info")
async def get_cache_info():
    """
    Get detailed information about cached entries.

    GENOMOS Phase 10: Performance Optimization

    Returns:
    - List of all cached entries
    - TTL remaining for each entry
    - Creation and expiry timestamps
    """
    try:
        info = _cache_manager.get_cache_info()
        return {
            "total_entries": len(info),
            "entries": info
        }
    except Exception as e:
        logger.error(f"Error getting cache info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache info: {str(e)}")


@router.post("/cache/clear")
async def clear_cache():
    """
    Clear all cache entries.

    GENOMOS Phase 10: Performance Optimization

    Use this endpoint to manually clear the cache when needed.
    Cache entries will be rebuilt on next access.
    """
    try:
        _cache_manager.clear()
        invalidate_lru_caches()
        return {
            "success": True,
            "message": "Cache cleared successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


@router.delete("/cache/{key}")
async def invalidate_cache_key(key: str):
    """
    Invalidate a specific cache entry by key.

    GENOMOS Phase 10: Performance Optimization

    Args:
        key: Cache key to invalidate

    Returns:
        Success status and whether key was found
    """
    try:
        was_found = _cache_manager.invalidate(key)
        return {
            "success": True,
            "key": key,
            "was_found": was_found,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error invalidating cache key: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to invalidate cache: {str(e)}")


@router.delete("/cache/pattern/{pattern}")
async def invalidate_cache_pattern(pattern: str):
    """
    Invalidate all cache entries matching a pattern.

    GENOMOS Phase 10: Performance Optimization

    Args:
        pattern: Pattern to match (e.g., "smk_*", "consultation_*")

    Returns:
        Number of entries invalidated
    """
    try:
        count = _cache_manager.invalidate_pattern(pattern)
        return {
            "success": True,
            "pattern": pattern,
            "entries_invalidated": count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error invalidating cache pattern: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to invalidate pattern: {str(e)}")
