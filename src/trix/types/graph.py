"""Graph-related types for Trix SDK."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse
from .memory import Memory
from .relationship import Relationship


class GraphNode(BaseResponse):
    """Node in the memory graph."""

    memory: Memory
    relationships: List[Relationship] = Field(default_factory=list)
    depth: int = 0


class GraphTraversal(BaseResponse):
    """Result of graph traversal."""

    nodes: List[GraphNode]
    total_nodes: int


class GraphContext(BaseResponse):
    """Contextual graph around a query."""

    query: str
    memories: List[Memory]
    relationships: List[Relationship]
    relevance_scores: Dict[str, float] = Field(default_factory=dict)


class ShortestPath(BaseResponse):
    """Shortest path between memories."""

    source_id: str
    target_id: str
    path: List[str]
    relationships: List[Relationship]
    distance: int


class HybridScoringWeights(BaseModel):
    """Weights used in hybrid scoring."""

    semantic: float
    graph: float
    co_activation: float
    recency: float
    salience: float


class GraphExpansionScoring(BaseModel):
    """Scoring metadata for graph expansion."""

    applied: bool
    weights: Optional[HybridScoringWeights] = None


class GraphExpansionStats(BaseModel):
    """Statistics from graph expansion."""

    seed_count: int
    expanded_count: int
    final_count: int
    relationships_found: Optional[int] = None
    hops_used: Optional[int] = None


class GraphExpansionResult(BaseResponse):
    """Result of graph expansion from seed memories."""

    seed_memories: List[str]
    expanded_memories: List[Memory]
    relationships: List[Relationship]
    stats: GraphExpansionStats
    scoring: Optional[GraphExpansionScoring] = None


class GraphNeighbor(BaseModel):
    """A neighbor in the graph."""

    id: str
    type: str
    relationship: Relationship


class GraphNeighbors(BaseResponse):
    """Graph neighbors result."""

    node_id: str
    neighbors: List[GraphNeighbor]


class GraphStats(BaseResponse):
    """Graph statistics."""

    node_count: int
    edge_count: int
    avg_degree: float
    density: float
    components: int
