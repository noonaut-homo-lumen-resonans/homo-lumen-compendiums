"""
Knowledge Graph Models for GENOMOS Phase 6

Pydantic models for representing the GENOMOS knowledge network
in a format compatible with D3.js, Cytoscape.js, and other visualization tools.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class GraphNode(BaseModel):
    """
    A node in the knowledge graph.

    Can represent:
    - SMK documents
    - Consultations
    - Agent learning events
    - Agents themselves
    """
    id: str = Field(..., description="Unique node identifier")
    type: str = Field(..., description="Node type: smk, consultation, agent_learning, agent")
    label: str = Field(..., description="Display label for the node")
    title: Optional[str] = Field(None, description="Full title (for SMK documents)")

    # Metadata for visualization
    size: Optional[float] = Field(10.0, description="Visual size (for centrality, importance)")
    color: Optional[str] = Field(None, description="Color code for visualization")

    # Additional data
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional node properties")

    # Timestamps
    created_at: Optional[str] = Field(None, description="ISO timestamp")

    # Position (for layout)
    x: Optional[float] = Field(None, description="X coordinate for fixed layout")
    y: Optional[float] = Field(None, description="Y coordinate for fixed layout")


class GraphEdge(BaseModel):
    """
    An edge (connection) in the knowledge graph.

    Represents relationships like:
    - SMK references another SMK
    - Consultation cites SMK
    - Agent learning event related to consultation
    """
    id: str = Field(..., description="Unique edge identifier")
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    type: str = Field(..., description="Edge type: references, cites, discusses, triggers")

    # Edge metadata
    weight: float = Field(1.0, description="Edge weight (strength of relationship)")
    label: Optional[str] = Field(None, description="Display label for edge")

    # Additional data
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional edge properties")


class KnowledgeGraph(BaseModel):
    """
    Complete knowledge graph representation.

    Contains all nodes and edges, plus metadata about the graph.
    Compatible with D3.js force-directed layouts and Cytoscape.js.
    """
    nodes: List[GraphNode] = Field(..., description="All nodes in the graph")
    edges: List[GraphEdge] = Field(..., description="All edges in the graph")

    # Graph-level metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Graph-level statistics and info"
    )

    # Stats
    total_nodes: int = Field(..., description="Total number of nodes")
    total_edges: int = Field(..., description="Total number of edges")

    # Node type distribution
    node_types: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of nodes by type"
    )

    # Edge type distribution
    edge_types: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of edges by type"
    )

    # Timestamp
    generated_at: str = Field(..., description="ISO timestamp when graph was generated")

    class Config:
        schema_extra = {
            "example": {
                "nodes": [
                    {
                        "id": "smk-019",
                        "type": "smk",
                        "label": "Constitution V1.1",
                        "title": "Homo Lumen Constitution",
                        "size": 25.0,
                        "color": "#4CAF50"
                    },
                    {
                        "id": "consultation-001",
                        "type": "consultation",
                        "label": "Quantum Consciousness Query",
                        "size": 15.0,
                        "color": "#2196F3"
                    }
                ],
                "edges": [
                    {
                        "id": "edge-1",
                        "source": "consultation-001",
                        "target": "smk-019",
                        "type": "cites",
                        "weight": 1.0
                    }
                ],
                "total_nodes": 2,
                "total_edges": 1,
                "node_types": {"smk": 1, "consultation": 1},
                "edge_types": {"cites": 1},
                "generated_at": "2025-10-28T12:00:00"
            }
        }


class ConsultationSimilarity(BaseModel):
    """
    Represents similarity between two consultations.

    Used by the recommendation system to suggest related consultations.
    """
    consultation_id: str = Field(..., description="ID of the related consultation")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score (0-1)")

    # What makes them similar
    shared_smk: List[str] = Field(default_factory=list, description="SMK references both cite")
    shared_agents: List[str] = Field(default_factory=list, description="Agents involved in both")

    # Human-readable explanation
    reason: str = Field(..., description="Why these consultations are related")

    # Metadata
    consultation_summary: Optional[str] = Field(None, description="Brief summary of related consultation")
    timestamp: Optional[str] = Field(None, description="When related consultation occurred")

    class Config:
        schema_extra = {
            "example": {
                "consultation_id": "consultation-456",
                "similarity_score": 0.87,
                "shared_smk": ["019", "042", "043"],
                "shared_agents": ["lira", "orion"],
                "reason": "3 shared SMK references, similar quantum consciousness topic",
                "consultation_summary": "Discussion about quantum observer effect",
                "timestamp": "2025-10-27T10:30:00"
            }
        }


class GraphAnalytics(BaseModel):
    """
    Analytics about the knowledge graph structure.

    Includes centrality metrics, clusters, and patterns.
    """
    # Centrality scores (which SMKs are most referenced)
    smk_centrality: Dict[str, float] = Field(
        default_factory=dict,
        description="Centrality scores for each SMK"
    )

    # Most connected SMKs
    top_smks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Top N most referenced SMKs"
    )

    # Knowledge clusters
    clusters: List[List[str]] = Field(
        default_factory=list,
        description="Groups of tightly-connected SMKs"
    )

    # Co-occurrence patterns
    smk_co_occurrence: Dict[str, Dict[str, int]] = Field(
        default_factory=dict,
        description="Which SMKs appear together in consultations"
    )

    # Temporal patterns
    growth_over_time: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="How the graph has evolved over time"
    )


class BlockchainAnalytics(BaseModel):
    """
    Comprehensive blockchain analytics and statistics.

    GENOMOS Phase 8: Visualization & Analytics
    """
    # Overview stats
    total_blocks: int = Field(..., description="Total number of blocks in chain")
    total_genes: int = Field(..., description="Total genes (excluding genesis)")
    genesis_date: str = Field(..., description="When blockchain was initialized")
    latest_block_date: str = Field(..., description="Most recent block timestamp")
    chain_age_days: float = Field(..., description="Age of blockchain in days")

    # Gene distribution
    gene_distribution: Dict[str, int] = Field(
        ...,
        description="Count of each gene type"
    )

    # Agent activity
    agent_activity: Dict[str, int] = Field(
        ...,
        description="Number of genes created by each agent"
    )

    # Growth metrics
    avg_blocks_per_day: float = Field(..., description="Average growth rate")
    blocks_last_24h: int = Field(0, description="Blocks added in last 24 hours")
    blocks_last_7d: int = Field(0, description="Blocks added in last 7 days")

    # Top contributors
    top_agents: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most active agents"
    )

    # Metadata
    blockchain_health: str = Field("healthy", description="Overall blockchain status")
    generated_at: str = Field(..., description="When analytics were generated")


class TimelineDataPoint(BaseModel):
    """
    A single data point in the blockchain timeline.
    """
    date: str = Field(..., description="ISO date (YYYY-MM-DD)")
    cumulative_blocks: int = Field(..., description="Total blocks up to this date")
    new_blocks: int = Field(0, description="Blocks added on this date")
    gene_types: Dict[str, int] = Field(
        default_factory=dict,
        description="Gene types added on this date"
    )


class TimelineAnalytics(BaseModel):
    """
    Timeline showing blockchain growth over time.

    GENOMOS Phase 8: Visualization & Analytics
    """
    timeline: List[TimelineDataPoint] = Field(
        ...,
        description="Daily data points showing growth"
    )

    total_days: int = Field(..., description="Number of days covered")
    start_date: str = Field(..., description="First block date")
    end_date: str = Field(..., description="Last block date")

    # Growth trends
    peak_activity_date: Optional[str] = Field(None, description="Date with most blocks added")
    peak_activity_count: int = Field(0, description="Blocks added on peak day")

    generated_at: str = Field(..., description="When timeline was generated")
