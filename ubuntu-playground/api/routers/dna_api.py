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
from models.knowledge_graph import KnowledgeGraph, GraphNode, GraphEdge, ConsultationSimilarity
from blockchain.consultation_recommender import find_related_consultations

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
