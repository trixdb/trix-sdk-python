"""Pydantic models for Trix API types.

This module provides backward-compatible exports from the refactored type modules.
Types are organized into logical submodules for better maintainability:
- enums: All enum definitions
- base: Base response models and pagination
- memory, relationship, cluster, space, persona: Core domain types
- graph, search, webhook: Infrastructure types
- agent, session, feedback, highlight, transcript: Interaction types

Extended types are split into:
- _exports_knowledge: goal, fact, entity, enrichment, topic, resource, image
- _exports_extended: task, bot, workflow, note, template, hub, crew, etc.
"""

from typing import TypeVar

# Type variable for generic responses
T = TypeVar("T")

# =============================================================================
# Enums
# =============================================================================
from .enums import (  # noqa: E402
    ClusterScale,
    Direction,
    EnrichmentOperation,
    EnrichmentStatus,
    EnrichmentType,
    ExtractionType,
    FactNodeType,
    FactSourceMethod,
    MemoryType,
    OriginType,
    ProtectionLevel,
    RelationshipType,
    ResourceRelationshipType,
    RetentionPolicy,
    SearchMode,
    SessionStatus,
    SessionType,
    SourceType,
    WebhookEvent,
)

# =============================================================================
# Base Models
# =============================================================================
from .base import BaseResponse, BulkResult, PaginatedResponse, Pagination  # noqa: E402

# =============================================================================
# Memory Models
# =============================================================================
from .memory import (  # noqa: E402
    Memory, MemoryConfig, MemoryCreate, MemoryList,
    MemoryOptions, MemoryStats, MemoryUpdate,
)

# =============================================================================
# Relationship Models
# =============================================================================
from .relationship import (  # noqa: E402
    ReinforceGroupResult, RelatedMemoriesResult, RelatedMemory,
    Relationship, RelationshipCreate, RelationshipList,
    RelationshipTypeInfo, RelationshipTypesResult, RelationshipUpdate,
)

# =============================================================================
# Cluster Models
# =============================================================================
from .cluster import (  # noqa: E402
    Cluster, ClusterCreate, ClusterList, ClusterMembership,
    ClusterQuality, ClusterStats, ClusterTopic, ClusterTopics,
    ClusterUpdate, IncrementalClusterResult,
)

# =============================================================================
# Space & Persona Models
# =============================================================================
from .space import Space, SpaceCreate, SpaceList, SpaceUpdate  # noqa: E402
from .persona import (  # noqa: E402
    Persona, PersonaAddSpace, PersonaCreate, PersonaGoal,
    PersonaList, PersonaSpace, PersonaUpdate,
)

# =============================================================================
# Graph Models
# =============================================================================
from .graph import (  # noqa: E402
    GraphContext, GraphExpansionResult, GraphExpansionScoring,
    GraphExpansionStats, GraphNeighbor, GraphNeighbors, GraphNode,
    GraphStats, GraphTraversal, HybridScoringWeights, ShortestPath,
)

# =============================================================================
# Search Models
# =============================================================================
from .search import (  # noqa: E402
    EmbedAllResponse, EmbeddingResponse, SearchConfig,
    SearchResult, SearchResults,
)

# =============================================================================
# Webhook Models
# =============================================================================
from .webhook import (  # noqa: E402
    Webhook, WebhookCreate, WebhookDelivery, WebhookDeliveryList,
    WebhookEventInfo, WebhookEventList, WebhookEventStats,
    WebhookEventTypeInfo, WebhookEventTypesResult, WebhookFilter,
    WebhookList, WebhookStats, WebhookUpdate,
)

# =============================================================================
# Agent & Session Models
# =============================================================================
from .agent import (  # noqa: E402
    AgentContext, AgentSession, SessionList,
    SessionMemory, SessionMemoryList, SessionMessage,
)
from .session import (  # noqa: E402
    CompleteSessionParams, CreateSessionParams, Session,
    SessionsResponse, SessionStats, UpdateSessionParams,
)

# =============================================================================
# Feedback, Highlight, Transcript Models
# =============================================================================
from .feedback import FeedbackResponse, FeedbackResult, FeedbackSubmit  # noqa: E402
from .highlight import (  # noqa: E402
    ExtractedHighlights, Highlight, HighlightCreate, HighlightLinkResult,
    HighlightList, HighlightSearchResult, HighlightTypeInfo,
    HighlightTypesResult, HighlightUpdate, HighlightWithScore,
)
from .transcript import (  # noqa: E402
    ContentSafetyLabel, TimestampRange, Transcript,
    TranscriptChapter, TranscriptEntity, TranscriptSegment, WordTimestamp,
)

# =============================================================================
# Knowledge domain exports (goal, fact, entity, enrichment, topic, etc.)
# =============================================================================
from ._exports_knowledge import *  # noqa: F401, F403
from ._exports_knowledge import __all__ as _knowledge_all

# =============================================================================
# Extended type exports (task, bot, workflow, note, template, hub, etc.)
# =============================================================================
from ._exports_extended import *  # noqa: F401, F403
from ._exports_extended import __all__ as _extended_all

# Core __all__ — types defined directly in this file
_core_all = [
    "T",
    # Enums
    "ClusterScale", "Direction", "EnrichmentOperation", "EnrichmentStatus",
    "EnrichmentType", "ExtractionType", "FactNodeType", "FactSourceMethod",
    "MemoryType", "OriginType", "ProtectionLevel", "RelationshipType",
    "ResourceRelationshipType", "RetentionPolicy", "SearchMode",
    "SessionStatus", "SessionType", "SourceType", "WebhookEvent",
    # Base
    "BaseResponse", "BulkResult", "PaginatedResponse", "Pagination",
    # Memory
    "Memory", "MemoryConfig", "MemoryCreate", "MemoryList",
    "MemoryOptions", "MemoryStats", "MemoryUpdate",
    # Relationship
    "ReinforceGroupResult", "RelatedMemoriesResult", "RelatedMemory",
    "Relationship", "RelationshipCreate", "RelationshipList",
    "RelationshipTypeInfo", "RelationshipTypesResult", "RelationshipUpdate",
    # Cluster
    "Cluster", "ClusterCreate", "ClusterList", "ClusterMembership",
    "ClusterQuality", "ClusterStats", "ClusterTopic", "ClusterTopics",
    "ClusterUpdate", "IncrementalClusterResult",
    # Space
    "Space", "SpaceCreate", "SpaceList", "SpaceUpdate",
    # Persona
    "Persona", "PersonaAddSpace", "PersonaCreate", "PersonaGoal",
    "PersonaList", "PersonaSpace", "PersonaUpdate",
    # Graph
    "GraphContext", "GraphExpansionResult", "GraphExpansionScoring",
    "GraphExpansionStats", "GraphNeighbor", "GraphNeighbors", "GraphNode",
    "GraphStats", "GraphTraversal", "HybridScoringWeights", "ShortestPath",
    # Search
    "EmbedAllResponse", "EmbeddingResponse", "SearchConfig",
    "SearchResult", "SearchResults",
    # Webhook
    "Webhook", "WebhookCreate", "WebhookDelivery", "WebhookDeliveryList",
    "WebhookEventInfo", "WebhookEventList", "WebhookEventStats",
    "WebhookEventTypeInfo", "WebhookEventTypesResult", "WebhookFilter",
    "WebhookList", "WebhookStats", "WebhookUpdate",
    # Agent
    "AgentContext", "AgentSession", "SessionList",
    "SessionMemory", "SessionMemoryList", "SessionMessage",
    # Session
    "CompleteSessionParams", "CreateSessionParams", "Session",
    "SessionsResponse", "SessionStats", "UpdateSessionParams",
    # Feedback
    "FeedbackResponse", "FeedbackResult", "FeedbackSubmit",
    # Highlight
    "ExtractedHighlights", "Highlight", "HighlightCreate",
    "HighlightLinkResult", "HighlightList", "HighlightSearchResult",
    "HighlightTypeInfo", "HighlightTypesResult", "HighlightUpdate",
    "HighlightWithScore",
    # Transcript
    "ContentSafetyLabel", "TimestampRange", "Transcript",
    "TranscriptChapter", "TranscriptEntity", "TranscriptSegment",
    "WordTimestamp",
]

__all__ = _core_all + _knowledge_all + _extended_all
