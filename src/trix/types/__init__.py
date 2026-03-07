"""Pydantic models for Trix API types.

This module provides backward-compatible exports from the refactored type modules.
Types are organized into logical submodules for better maintainability:
- enums: All enum definitions
- base: Base response models and pagination
- memory: Memory-related types
- relationship: Relationship types
- cluster: Cluster types
- space: Space types
- graph: Graph traversal types
- search: Search-related types
- webhook: Webhook types
- agent: Agent/session types
- session: CLI session types
- feedback: Feedback types
- highlight: Highlight types
- transcript: Transcript types
- fact: Fact types
- entity: Entity types
- enrichment: Enrichment types
- topic: Topic types
- resource: Resource types
- image: Image/visual search types
"""

from typing import TypeVar

# Type variable for generic responses
T = TypeVar("T")

# =============================================================================
# Enums
# =============================================================================
from .enums import (
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
from .base import (
    BaseResponse,
    BulkResult,
    PaginatedResponse,
    Pagination,
)

# =============================================================================
# Memory Models
# =============================================================================
from .memory import (
    Memory,
    MemoryConfig,
    MemoryCreate,
    MemoryList,
    MemoryOptions,
    MemoryStats,
    MemoryUpdate,
)

# =============================================================================
# Relationship Models
# =============================================================================
from .relationship import (
    ReinforceGroupResult,
    RelatedMemoriesResult,
    RelatedMemory,
    Relationship,
    RelationshipCreate,
    RelationshipList,
    RelationshipTypeInfo,
    RelationshipTypesResult,
    RelationshipUpdate,
)

# =============================================================================
# Cluster Models
# =============================================================================
from .cluster import (
    Cluster,
    ClusterCreate,
    ClusterList,
    ClusterMembership,
    ClusterQuality,
    ClusterStats,
    ClusterTopic,
    ClusterTopics,
    ClusterUpdate,
    IncrementalClusterResult,
)

# =============================================================================
# Space Models
# =============================================================================
from .space import (
    Space,
    SpaceCreate,
    SpaceList,
    SpaceUpdate,
)

# =============================================================================
# Persona Models
# =============================================================================
from .persona import (
    Persona,
    PersonaAddSpace,
    PersonaCreate,
    PersonaGoal,
    PersonaList,
    PersonaSpace,
    PersonaUpdate,
)

# =============================================================================
# Graph Models
# =============================================================================
from .graph import (
    GraphContext,
    GraphExpansionResult,
    GraphExpansionScoring,
    GraphExpansionStats,
    GraphNeighbor,
    GraphNeighbors,
    GraphNode,
    GraphStats,
    GraphTraversal,
    HybridScoringWeights,
    ShortestPath,
)

# =============================================================================
# Search Models
# =============================================================================
from .search import (
    EmbedAllResponse,
    EmbeddingResponse,
    SearchConfig,
    SearchResult,
    SearchResults,
)

# =============================================================================
# Webhook Models
# =============================================================================
from .webhook import (
    Webhook,
    WebhookCreate,
    WebhookDelivery,
    WebhookDeliveryList,
    WebhookEventInfo,
    WebhookEventList,
    WebhookEventStats,
    WebhookEventTypeInfo,
    WebhookEventTypesResult,
    WebhookFilter,
    WebhookList,
    WebhookStats,
    WebhookUpdate,
)

# =============================================================================
# Agent Models
# =============================================================================
from .agent import (
    AgentContext,
    AgentSession,
    SessionList,
    SessionMemory,
    SessionMemoryList,
)

# =============================================================================
# Session Models
# =============================================================================
from .session import (
    CompleteSessionParams,
    CreateSessionParams,
    Session,
    SessionsResponse,
    SessionStats,
    UpdateSessionParams,
)

# =============================================================================
# Feedback Models
# =============================================================================
from .feedback import (
    FeedbackResponse,
    FeedbackResult,
    FeedbackSubmit,
)

# =============================================================================
# Highlight Models
# =============================================================================
from .highlight import (
    ExtractedHighlights,
    Highlight,
    HighlightCreate,
    HighlightLinkResult,
    HighlightList,
    HighlightSearchResult,
    HighlightTypeInfo,
    HighlightTypesResult,
    HighlightUpdate,
    HighlightWithScore,
)

# =============================================================================
# Transcript Models
# =============================================================================
from .transcript import (
    ContentSafetyLabel,
    TimestampRange,
    Transcript,
    TranscriptChapter,
    TranscriptEntity,
    TranscriptSegment,
    WordTimestamp,
)

# =============================================================================
# Goal Models
# =============================================================================
from .goal import (
    Goal,
    GoalContributor,
    GoalContributorCreate,
    GoalContributorUpdate,
    GoalCreate,
    GoalList,
    GoalMemoryLink,
    GoalMemoryListResponse,
    GoalProgressUpdate,
    GoalStatusTransition,
    GoalUpdate,
    ProgressHistoryEntry,
    ProgressHistoryList,
)

# =============================================================================
# Fact Models
# =============================================================================
from .fact import (
    ExtractedFact,
    Fact,
    FactCreate,
    FactExtractionResult,
    FactList,
    FactQueryResult,
    FactSource,
    FactUpdate,
    FactVerificationResult,
    ScoredFact,
)

# =============================================================================
# Entity Models
# =============================================================================
from .entity import (
    Entity,
    EntityCreate,
    EntityExtractionResult,
    EntityFactsResult,
    EntityList,
    EntityMemoryLinkResult,
    EntityMergeResult,
    EntityResolutionResult,
    EntitySearchResult,
    EntityTypeInfo,
    EntityTypesResult,
    EntityUpdate,
    ExtractedEntity,
    ScoredEntity,
)

# =============================================================================
# Enrichment Models
# =============================================================================
from .enrichment import (
    Enrichment,
    EnrichmentList,
    EnrichmentResult,
)

# =============================================================================
# Topic Models
# =============================================================================
from .topic import (
    Topic,
    TopicList,
    TopicSearchResult,
)

# =============================================================================
# Resource Models
# =============================================================================
from .resource import (
    MemoryResource,
    MemoryResourceLinkResult,
    MemoryResourceList,
    MemoryResourceUnlinkResult,
    Resource,
    ResourceCreate,
    ResourceList,
    ResourceUpdate,
)

# =============================================================================
# Image Models
# =============================================================================
from .image import (
    AutoTagResult,
    BatchAutoTagResult,
    DuplicateCheckResult,
    ImageCluster,
    ImageClusterResult,
    ImageTag,
    QuerySuggestion,
    QuerySuggestionsResult,
    VisualSearchResult,
    VisualSearchResults,
)

# =============================================================================
# Task Models
# =============================================================================
from .task import (
    AssigneeType,
    BulkDeleteResult,
    BulkTaskCreate,
    BulkTaskFailure,
    BulkTaskResult,
    BulkTaskUpdate,
    Label,
    SubtaskCreate,
    SuggestedTask,
    SuggestedTasksResult,
    Task,
    TaskCreate,
    TaskHandoffParams,
    TaskHandoffResult,
    TaskLink,
    TaskLinkCreate,
    TaskLinkType,
    TaskList,
    TaskStatus,
    TaskUpdate,
)

# =============================================================================
# Bot Models
# =============================================================================
from .bot import (
    Bot,
    BotAction,
    BotAddSpace,
    BotCreate,
    BotList,
    BotRun,
    BotRunList,
    BotRunRequest,
    BotSpace,
    BotTool,
    BotTrigger,
    BotTriggerCreate,
    BotUpdate,
)

# =============================================================================
# Workflow Models
# =============================================================================
from .workflow import (
    TriggerCreate,
    TriggerUpdate,
    Workflow,
    WorkflowCreate,
    WorkflowList,
    WorkflowRun,
    WorkflowRunList,
    WorkflowTrigger,
    WorkflowUpdate,
)

# =============================================================================
# Note Models
# =============================================================================
from .note import (
    Note,
    NoteBlock,
    NoteBlockCreate,
    NoteBlockUpdate,
    NoteCollaborator,
    NoteCollaboratorCreate,
    NoteCreate,
    NoteList,
    NoteUpdate,
)

# =============================================================================
# Space Config Models
# =============================================================================
from .space_config import (
    SpaceConfigAuditEvent,
    SpaceConfigAuditResponse,
    SpaceConfigCategory,
    SpaceConfigPatch,
    SpaceConfigResponse,
    SpaceConfigValidation,
)

__all__ = [
    # Type variable
    "T",
    # Enums
    "ClusterScale",
    "Direction",
    "EnrichmentOperation",
    "EnrichmentStatus",
    "EnrichmentType",
    "ExtractionType",
    "FactNodeType",
    "FactSourceMethod",
    "MemoryType",
    "OriginType",
    "ProtectionLevel",
    "RelationshipType",
    "ResourceRelationshipType",
    "RetentionPolicy",
    "SearchMode",
    "SessionStatus",
    "SessionType",
    "SourceType",
    "WebhookEvent",
    # Base
    "BaseResponse",
    "BulkResult",
    "PaginatedResponse",
    "Pagination",
    # Memory
    "Memory",
    "MemoryConfig",
    "MemoryCreate",
    "MemoryList",
    "MemoryOptions",
    "MemoryStats",
    "MemoryUpdate",
    # Relationship
    "ReinforceGroupResult",
    "RelatedMemoriesResult",
    "RelatedMemory",
    "Relationship",
    "RelationshipCreate",
    "RelationshipList",
    "RelationshipTypeInfo",
    "RelationshipTypesResult",
    "RelationshipUpdate",
    # Cluster
    "Cluster",
    "ClusterCreate",
    "ClusterList",
    "ClusterMembership",
    "ClusterQuality",
    "ClusterStats",
    "ClusterTopic",
    "ClusterTopics",
    "ClusterUpdate",
    "IncrementalClusterResult",
    # Space
    "Space",
    "SpaceCreate",
    "SpaceList",
    "SpaceUpdate",
    # Persona
    "Persona",
    "PersonaAddSpace",
    "PersonaCreate",
    "PersonaGoal",
    "PersonaList",
    "PersonaSpace",
    "PersonaUpdate",
    # Graph
    "GraphContext",
    "GraphExpansionResult",
    "GraphExpansionScoring",
    "GraphExpansionStats",
    "GraphNeighbor",
    "GraphNeighbors",
    "GraphNode",
    "GraphStats",
    "GraphTraversal",
    "HybridScoringWeights",
    "ShortestPath",
    # Search
    "EmbedAllResponse",
    "EmbeddingResponse",
    "SearchConfig",
    "SearchResult",
    "SearchResults",
    # Webhook
    "Webhook",
    "WebhookCreate",
    "WebhookDelivery",
    "WebhookDeliveryList",
    "WebhookEventInfo",
    "WebhookEventList",
    "WebhookEventStats",
    "WebhookEventTypeInfo",
    "WebhookEventTypesResult",
    "WebhookFilter",
    "WebhookList",
    "WebhookStats",
    "WebhookUpdate",
    # Agent
    "AgentContext",
    "AgentSession",
    "SessionList",
    "SessionMemory",
    "SessionMemoryList",
    # Session
    "CompleteSessionParams",
    "CreateSessionParams",
    "Session",
    "SessionsResponse",
    "SessionStats",
    "UpdateSessionParams",
    # Feedback
    "FeedbackResponse",
    "FeedbackResult",
    "FeedbackSubmit",
    # Highlight
    "ExtractedHighlights",
    "Highlight",
    "HighlightCreate",
    "HighlightLinkResult",
    "HighlightList",
    "HighlightSearchResult",
    "HighlightTypeInfo",
    "HighlightTypesResult",
    "HighlightUpdate",
    "HighlightWithScore",
    # Transcript
    "ContentSafetyLabel",
    "TimestampRange",
    "Transcript",
    "TranscriptChapter",
    "TranscriptEntity",
    "TranscriptSegment",
    "WordTimestamp",
    # Goal
    "Goal",
    "GoalContributor",
    "GoalContributorCreate",
    "GoalContributorUpdate",
    "GoalCreate",
    "GoalList",
    "GoalMemoryLink",
    "GoalMemoryListResponse",
    "GoalProgressUpdate",
    "GoalStatusTransition",
    "GoalUpdate",
    "ProgressHistoryEntry",
    "ProgressHistoryList",
    # Fact
    "ExtractedFact",
    "Fact",
    "FactCreate",
    "FactExtractionResult",
    "FactList",
    "FactQueryResult",
    "FactSource",
    "FactUpdate",
    "FactVerificationResult",
    "ScoredFact",
    # Entity
    "Entity",
    "EntityCreate",
    "EntityExtractionResult",
    "EntityFactsResult",
    "EntityList",
    "EntityMemoryLinkResult",
    "EntityMergeResult",
    "EntityResolutionResult",
    "EntitySearchResult",
    "EntityTypeInfo",
    "EntityTypesResult",
    "EntityUpdate",
    "ExtractedEntity",
    "ScoredEntity",
    # Enrichment
    "Enrichment",
    "EnrichmentList",
    "EnrichmentResult",
    # Topic
    "Topic",
    "TopicList",
    "TopicSearchResult",
    # Resource
    "MemoryResource",
    "MemoryResourceLinkResult",
    "MemoryResourceList",
    "MemoryResourceUnlinkResult",
    "Resource",
    "ResourceCreate",
    "ResourceList",
    "ResourceUpdate",
    # Image
    "AutoTagResult",
    "BatchAutoTagResult",
    "DuplicateCheckResult",
    "ImageCluster",
    "ImageClusterResult",
    "ImageTag",
    "QuerySuggestion",
    "QuerySuggestionsResult",
    "VisualSearchResult",
    "VisualSearchResults",
    # Task
    "AssigneeType",
    "BulkDeleteResult",
    "BulkTaskCreate",
    "BulkTaskFailure",
    "BulkTaskResult",
    "BulkTaskUpdate",
    "Label",
    "SubtaskCreate",
    "SuggestedTask",
    "SuggestedTasksResult",
    "Task",
    "TaskCreate",
    "TaskHandoffParams",
    "TaskHandoffResult",
    "TaskLink",
    "TaskLinkCreate",
    "TaskLinkType",
    "TaskList",
    "TaskStatus",
    "TaskUpdate",
    # Bot
    "Bot",
    "BotAction",
    "BotAddSpace",
    "BotCreate",
    "BotList",
    "BotRun",
    "BotRunList",
    "BotRunRequest",
    "BotSpace",
    "BotTool",
    "BotTrigger",
    "BotTriggerCreate",
    "BotUpdate",
    # Workflow
    "TriggerCreate",
    "TriggerUpdate",
    "Workflow",
    "WorkflowCreate",
    "WorkflowList",
    "WorkflowRun",
    "WorkflowRunList",
    "WorkflowTrigger",
    "WorkflowUpdate",
    # Note
    "Note",
    "NoteBlock",
    "NoteBlockCreate",
    "NoteBlockUpdate",
    "NoteCollaborator",
    "NoteCollaboratorCreate",
    "NoteCreate",
    "NoteList",
    "NoteUpdate",
    # Space Config
    "SpaceConfigAuditEvent",
    "SpaceConfigAuditResponse",
    "SpaceConfigCategory",
    "SpaceConfigPatch",
    "SpaceConfigResponse",
    "SpaceConfigValidation",
]
