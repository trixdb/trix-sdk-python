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
    ClusterScale,  # noqa: F401
    Direction,  # noqa: F401
    EnrichmentOperation,  # noqa: F401
    EnrichmentStatus,  # noqa: F401
    EnrichmentType,  # noqa: F401
    ExtractionType,  # noqa: F401
    FactNodeType,  # noqa: F401
    FactSourceMethod,  # noqa: F401
    MemoryType,  # noqa: F401
    OriginType,  # noqa: F401
    ProtectionLevel,  # noqa: F401
    RelationshipType,  # noqa: F401
    ResourceRelationshipType,  # noqa: F401
    RetentionPolicy,  # noqa: F401
    SearchMode,  # noqa: F401
    SessionStatus,  # noqa: F401
    SessionType,  # noqa: F401
    SourceType,  # noqa: F401
    WebhookEvent,  # noqa: F401
)

# =============================================================================
# Base Models
# =============================================================================
from .base import BaseResponse, BulkResult, PaginatedResponse, Pagination  # noqa: E402, F401

# =============================================================================
# Memory Models
# =============================================================================
from .memory import (  # noqa: E402
    Memory, MemoryConfig, MemoryCreate, MemoryList,  # noqa: F401
    MemoryOptions, MemoryStats, MemoryUpdate,  # noqa: F401
)

# =============================================================================
# Relationship Models
# =============================================================================
from .relationship import (  # noqa: E402
    ReinforceGroupResult, RelatedMemoriesResult, RelatedMemory,  # noqa: F401
    Relationship, RelationshipCreate, RelationshipList,  # noqa: F401
    RelationshipTypeInfo, RelationshipTypesResult, RelationshipUpdate,  # noqa: F401
)

# =============================================================================
# Cluster Models
# =============================================================================
from .cluster import (  # noqa: E402
    Cluster, ClusterCreate, ClusterList, ClusterMembership,  # noqa: F401
    ClusterQuality, ClusterStats, ClusterTopic, ClusterTopics,  # noqa: F401
    ClusterUpdate, IncrementalClusterResult,  # noqa: F401
)

# =============================================================================
# Space & Persona Models
# =============================================================================
from .space import Space, SpaceCreate, SpaceList, SpaceUpdate  # noqa: E402, F401
from .persona import (  # noqa: E402
    Persona, PersonaAddSpace, PersonaCreate, PersonaGoal,  # noqa: F401
    PersonaList, PersonaSpace, PersonaUpdate,  # noqa: F401
)

# =============================================================================
# Graph Models
# =============================================================================
from .graph import (  # noqa: E402
    GraphContext, GraphExpansionResult, GraphExpansionScoring,  # noqa: F401
    GraphExpansionStats, GraphNeighbor, GraphNeighbors, GraphNode,  # noqa: F401
    GraphStats, GraphTraversal, HybridScoringWeights, ShortestPath,  # noqa: F401
)

# =============================================================================
# Search Models
# =============================================================================
from .search import (  # noqa: E402
    EmbedAllResponse, EmbeddingResponse, SearchConfig,  # noqa: F401
    SearchResult, SearchResults,  # noqa: F401
)

# =============================================================================
# Webhook Models
# =============================================================================
from .webhook import (  # noqa: E402
    Webhook, WebhookCreate, WebhookDelivery, WebhookDeliveryList,  # noqa: F401
    WebhookEventInfo, WebhookEventList, WebhookEventStats,  # noqa: F401
    WebhookEventTypeInfo, WebhookEventTypesResult, WebhookFilter,  # noqa: F401
    WebhookList, WebhookStats, WebhookUpdate,  # noqa: F401
)

# =============================================================================
# Agent & Session Models
# =============================================================================
from .agent import (  # noqa: E402
    AgentContext, AgentSession, SessionList,  # noqa: F401
    SessionMemory, SessionMemoryList, SessionMessage,  # noqa: F401
)
from .session import (  # noqa: E402
    CompleteSessionParams, CreateSessionParams, Session,  # noqa: F401
    SessionsResponse, SessionStats, UpdateSessionParams,  # noqa: F401
)

# =============================================================================
# Feedback, Highlight, Transcript Models
# =============================================================================
from .feedback import FeedbackResponse, FeedbackResult, FeedbackSubmit  # noqa: E402, F401
from .highlight import (  # noqa: E402
    ExtractedHighlights, Highlight, HighlightCreate, HighlightLinkResult,  # noqa: F401
    HighlightList, HighlightSearchResult, HighlightTypeInfo,  # noqa: F401
    HighlightTypesResult, HighlightUpdate, HighlightWithScore,  # noqa: F401
)
from .transcript import (  # noqa: E402
    ContentSafetyLabel, TimestampRange, Transcript,  # noqa: F401
    TranscriptChapter, TranscriptEntity, TranscriptSegment, WordTimestamp,  # noqa: F401
)

# =============================================================================
# Knowledge domain exports (goal, fact, entity, enrichment, topic, etc.)
# =============================================================================
from ._exports_knowledge import *  # noqa: E402, F401, F403
from ._exports_knowledge import __all__ as _knowledge_all  # noqa: E402

# =============================================================================
# Extended type exports (task, bot, workflow, note, template, hub, etc.)
# =============================================================================
from ._exports_extended import *  # noqa: E402, F401, F403
from ._exports_extended import __all__ as _extended_all  # noqa: E402

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
