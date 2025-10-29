"""
GENOMOS Visualization Models - Phase 12: Visualization & Monitoring

Pydantic models for blockchain visualization and monitoring.
Designed for React/D3.js/Three.js frontend integration.

Philosophy: "Visualize the genome - see the collective memory come alive"
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class TimelineBlock(BaseModel):
    """Block data for timeline visualization"""
    index: int
    timestamp: str
    gene_type: str
    agent: Optional[str]
    hash: str
    title: Optional[str] = None  # Short description
    color: str  # Hex color for visualization
    size: float = 1.0  # Visual size multiplier


class TimelineVisualization(BaseModel):
    """Complete timeline visualization data"""
    blocks: List[TimelineBlock]
    total_blocks: int
    start_date: str
    end_date: str
    time_span_days: float
    gene_type_colors: Dict[str, str]


class BlockExplorerBlock(BaseModel):
    """Detailed block data for block explorer"""
    index: int
    timestamp: str
    gene_type: str
    agent: Optional[str]
    tags: List[str]
    hash: str
    previous_hash: str
    data_preview: str  # First 200 chars of data
    data_size_bytes: int
    has_full_data: bool = True
    related_blocks: List[int] = Field(default_factory=list)  # Indexes of related blocks


class BlockExplorerPage(BaseModel):
    """Paginated block explorer data"""
    blocks: List[BlockExplorerBlock]
    page: int
    page_size: int
    total_blocks: int
    total_pages: int
    has_next: bool
    has_previous: bool


class AgentActivity(BaseModel):
    """Agent activity metrics"""
    agent_name: str
    total_blocks: int
    gene_types: Dict[str, int]  # Count per gene type
    first_activity: str  # ISO timestamp
    last_activity: str  # ISO timestamp
    activity_span_days: float
    avg_blocks_per_day: float
    recent_blocks: List[int]  # Last 10 block indexes


class AgentActivityDashboard(BaseModel):
    """Complete agent activity dashboard"""
    agents: List[AgentActivity]
    total_agents: int
    most_active_agent: str
    most_active_count: int
    generated_at: str


class GeneTypeDistribution(BaseModel):
    """Gene type distribution for pie/donut charts"""
    gene_type: str
    count: int
    percentage: float
    color: str
    description: Optional[str] = None


class DNAHelixNode(BaseModel):
    """3D DNA helix visualization node"""
    index: int
    gene_type: str
    position: Dict[str, float]  # {x, y, z}
    rotation: Dict[str, float]  # {x, y, z}
    color: str
    scale: float = 1.0
    metadata: Dict[str, Any]


class DNAHelixVisualization(BaseModel):
    """3D DNA helix structure for Three.js"""
    nodes: List[DNAHelixNode]
    connections: List[List[int]]  # [from_index, to_index] pairs
    helix_radius: float = 5.0
    helix_pitch: float = 2.0  # Distance between turns
    total_height: float
    camera_position: Dict[str, float]


class HeatmapCell(BaseModel):
    """Heatmap cell data"""
    row: str  # Y-axis label (e.g., gene type)
    column: str  # X-axis label (e.g., date or agent)
    value: float
    color_intensity: float  # 0.0 to 1.0
    tooltip: str


class HeatmapVisualization(BaseModel):
    """Heatmap visualization data"""
    cells: List[HeatmapCell]
    row_labels: List[str]
    column_labels: List[str]
    title: str
    color_scale: str = "blues"  # Color scheme
    min_value: float
    max_value: float


class RealTimeMetrics(BaseModel):
    """Real-time blockchain metrics"""
    current_block_index: int
    total_blocks: int
    blocks_added_last_hour: int
    blocks_added_last_day: int
    chain_valid: bool
    latest_hash: str
    merkle_root: str
    active_agents: List[str]
    timestamp: str


class NetworkGraph(BaseModel):
    """Network graph for knowledge relationships"""
    nodes: List[Dict[str, Any]]  # {id, label, type, color, size}
    edges: List[Dict[str, Any]]  # {source, target, label, weight}
    total_nodes: int
    total_edges: int
    layout: str = "force-directed"  # Layout algorithm


# Color schemes for different gene types
GENE_TYPE_COLORS = {
    "genesis": "#FFD700",      # Gold
    "smk": "#4169E1",          # Royal Blue
    "mutation": "#FF6347",     # Tomato
    "consultation": "#32CD32",  # Lime Green
    "agent_learning": "#9370DB", # Medium Purple
    "biofelt_context": "#FF69B4", # Hot Pink
    "pattern": "#FFA500",      # Orange
    "agent": "#20B2AA",        # Light Sea Green
    "contract": "#DC143C",     # Crimson
    "ipfs_backup": "#708090"   # Slate Gray
}


def get_gene_type_color(gene_type: str) -> str:
    """Get color for gene type."""
    return GENE_TYPE_COLORS.get(gene_type, "#CCCCCC")
