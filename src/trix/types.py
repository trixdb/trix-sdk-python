"""Pydantic models for Trix API types."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field, ConfigDict

# Type variable for generic responses
T = TypeVar("T")


# Enums
class MemoryType(str, Enum):
    """Memory content types."""

    TEXT = "text"
    MARKDOWN = "markdown"
    URL = "url"
    AUDIO = "audio"
    IMAGE = "image"


class SearchMode(str, Enum):
    """Search modes."""

    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    HYBRID = "hybrid"


class ClusterScale(str, Enum):
    """Multi-scale clustering levels."""

    FINE = "fine"  # Small, specific clusters
    MEDIUM = "medium"  # Balanced clusters
    COARSE = "coarse"  # Large, abstract clusters


class ProtectionLevel(str, Enum):
    """Memory protection levels to control decay and deletion."""

    NONE = "none"  # No protection, normal decay
    SOFT = "soft"  # Protected from auto-decay, can be manually deleted
    HARD = "hard"  # Protected from deletion, requires explicit unprotection


class RelationshipType(str, Enum):
    """Relationship types between memories."""

    RELATED_TO = "related_to"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    DERIVED_FROM = "derived_from"
    SIMILAR_TO = "similar_to"
    PRECEDES = "precedes"
    FOLLOWS = "follows"


class Direction(str, Enum):
    """Graph traversal direction."""

    OUTGOING = "outgoing"
    INCOMING = "incoming"
    BOTH = "both"


class ConsolidationStrategy(str, Enum):
    """Memory consolidation strategies."""

    SIMILARITY = "similarity"
    TEMPORAL = "temporal"
    IMPORTANCE = "importance"


class WebhookEvent(str, Enum):
    """Webhook event types."""

    MEMORY_CREATED = "memory.created"
    MEMORY_UPDATED = "memory.updated"
    MEMORY_DELETED = "memory.deleted"
    RELATIONSHIP_CREATED = "relationship.created"
    CLUSTER_CREATED = "cluster.created"


class OriginType(str, Enum):
    """Origin types for memory context classification.

    These represent the life domain context of a memory.
    """

    WORK = "work"
    PRIVATE = "private"
    SHARED = "shared"
    LEARNING = "learning"


class SourceType(str, Enum):
    """Source types for memory provenance tracking.

    These represent how/where the memory was captured.
    """

    EMAIL = "email"
    MEETING = "meeting"
    CHAT = "chat"
    DOCUMENT = "document"
    WEBPAGE = "webpage"
    AUDIO = "audio"
    VIDEO = "video"
    SCREENSHOT = "screenshot"
    MANUAL = "manual"
    AGENT = "agent"
    API = "api"
    IMPORT = "import"


class ResourceRelationshipType(str, Enum):
    """Relationship types for memory-resource associations.

    These describe the nature of the link between a memory and a resource.
    """

    PRIMARY = "primary"
    RELATED = "related"
    MENTIONED = "mentioned"
    DERIVED = "derived"


class JobStatus(str, Enum):
    """Job processing status."""

    WAITING = "waiting"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    DELAYED = "delayed"


class ExtractionType(str, Enum):
    """Highlight extraction types."""

    KEY_POINTS = "key_points"
    ENTITIES = "entities"
    QUOTES = "quotes"


class SessionType(str, Enum):
    """Session types for categorizing conversation contexts."""

    CONVERSATION = "conversation"
    PROJECT = "project"
    TASK = "task"
    TEMPORARY = "temporary"


class SessionStatus(str, Enum):
    """Session lifecycle status."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class RetentionPolicy(str, Enum):
    """Session retention policies."""

    PERMANENT = "permanent"
    AUTO_DELETE = "auto_delete"
    ON_COMPLETION = "on_completion"
    TEMPORARY = "temporary"


# Base Models
class BaseResponse(BaseModel):
    """Base response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# Pagination Models
class Pagination(BaseModel):
    """Pagination metadata for list responses.

    Supports both offset-based and cursor-based pagination.

    Attributes:
        total: Total number of items available.
        page: Current page number (1-indexed).
        limit: Maximum items per page.
        has_more: Whether more items exist beyond this page.
        cursor: Optional cursor for cursor-based pagination.
    """

    total: int
    page: int
    limit: int
    has_more: bool
    cursor: Optional[str] = None


class PaginatedResponse(BaseResponse, Generic[T]):
    """Generic paginated response wrapper.

    Used for list endpoints that return paginated data.

    Attributes:
        data: List of items for the current page.
        pagination: Pagination metadata.
    """

    data: List[T]
    pagination: Pagination


class BulkResult(BaseResponse):
    """Result of a bulk operation.

    Provides counts and error details for bulk create/update/delete operations.

    Attributes:
        success: Number of successfully processed items.
        failed: Number of items that failed to process.
        errors: List of error details for failed items.
    """

    success: int
    failed: int
    errors: List[Dict[str, Any]] = Field(default_factory=list)

    @property
    def total(self) -> int:
        """Total number of items in the bulk operation."""
        return self.success + self.failed

    @property
    def success_rate(self) -> float:
        """Success rate as a decimal (0.0 to 1.0)."""
        if self.total == 0:
            return 0.0
        return self.success / self.total


# Memory Models
class MemoryOptions(BaseModel):
    """Options for memory creation."""

    transcribe_audio: Optional[bool] = None
    language: Optional[str] = None
    skip_embedding: Optional[bool] = None


class Memory(BaseResponse):
    """Memory object."""

    id: str
    content: str
    type: MemoryType = MemoryType.TEXT
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    priority: Optional[int] = None
    space_id: Optional[str] = None
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime
    access_count: int = 0
    last_accessed_at: Optional[datetime] = None
    transcript: Optional[str] = None
    audio_url: Optional[str] = None
    # Origin/Context fields (provenance tracking)
    session_id: Optional[str] = None
    origin_type: Optional[OriginType] = None
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    source_metadata: Dict[str, Any] = Field(default_factory=dict)
    # Pinning and protection fields
    is_pinned: bool = False
    protection_level: Optional[str] = None  # "none", "soft", "hard"
    is_deleted: bool = False  # Soft delete flag
    deleted_at: Optional[datetime] = None
    quality_score: Optional[float] = None  # 0-1 quality score


class MemoryCreate(BaseModel):
    """Request to create a memory."""

    content: str
    type: Optional[MemoryType] = MemoryType.TEXT
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None
    space_id: Optional[str] = None
    options: Optional[MemoryOptions] = None
    # Origin/Context fields (provenance tracking)
    session_id: Optional[str] = None
    origin_type: Optional[OriginType] = None
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    source_metadata: Optional[Dict[str, Any]] = None
    resource_ids: Optional[List[str]] = None
    # Pinning and protection fields
    is_pinned: Optional[bool] = None
    protection_level: Optional[str] = None  # "none", "soft", "hard"


class MemoryUpdate(BaseModel):
    """Request to update a memory."""

    content: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None
    # Origin/Context fields (provenance tracking)
    origin_type: Optional[OriginType] = None
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    source_metadata: Optional[Dict[str, Any]] = None
    # Pinning and protection fields
    is_pinned: Optional[bool] = None
    protection_level: Optional[str] = None  # "none", "soft", "hard"


class MemoryList(BaseResponse):
    """List of memories with pagination."""

    data: List[Memory]
    total: int
    limit: int
    offset: int


class MemoryConfig(BaseResponse):
    """Memory system configuration."""

    max_content_length: int
    supported_types: List[str]
    embedding_model: str
    embedding_dimensions: int


# Relationship Models
class Relationship(BaseResponse):
    """Relationship between memories."""

    id: str
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    description: Optional[str] = None
    weight: float = 1.0
    strength: Optional[float] = None  # Used in graph expansion (alternative to weight)
    bidirectional: bool = False
    created_at: datetime
    updated_at: datetime
    reinforcement_count: int = 0


class RelationshipCreate(BaseModel):
    """Request to create a relationship."""

    relationship_type: RelationshipType
    description: Optional[str] = None
    weight: Optional[float] = 1.0
    bidirectional: Optional[bool] = False


class RelationshipUpdate(BaseModel):
    """Request to update a relationship."""

    weight: Optional[float] = None
    description: Optional[str] = None


class RelationshipList(BaseResponse):
    """List of relationships."""

    data: List[Relationship]


# Cluster Models
class Cluster(BaseResponse):
    """Cluster of related memories."""

    id: str
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    memory_count: int = 0
    scale: Optional[str] = None  # "fine", "medium", "coarse"
    memories: Optional[List["Memory"]] = None  # Included when requested
    created_at: datetime
    updated_at: datetime


class ClusterCreate(BaseModel):
    """Request to create a cluster."""

    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ClusterUpdate(BaseModel):
    """Request to update a cluster."""

    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ClusterList(BaseResponse):
    """List of clusters with pagination."""

    data: List[Cluster]
    cursor: Optional[str] = None


class ClusterMembership(BaseResponse):
    """Memory membership in a cluster."""

    cluster_id: str
    memory_id: str
    confidence: float = 1.0
    added_at: datetime


# Space Models
class Space(BaseResponse):
    """Organizational space for memories."""

    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SpaceCreate(BaseModel):
    """Request to create a space."""

    name: str
    description: Optional[str] = None


class SpaceUpdate(BaseModel):
    """Request to update a space."""

    name: Optional[str] = None
    description: Optional[str] = None


class SpaceList(BaseResponse):
    """List of spaces."""

    data: List[Space]


# Graph Models
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


# Search Models
class SearchResult(BaseResponse):
    """Search result with similarity score."""

    memory: Memory
    score: float
    highlights: Optional[List[str]] = None


class SearchResults(BaseResponse):
    """List of search results."""

    data: List[SearchResult]
    query: Optional[str] = None


class SearchConfig(BaseResponse):
    """Search system configuration."""

    default_limit: int
    max_limit: int
    min_similarity_threshold: float


class EmbeddingResponse(BaseResponse):
    """Embedding generation response."""

    memory_ids: List[str]
    embeddings: List[List[float]]


class EmbedAllResponse(BaseResponse):
    """Batch embedding response."""

    total_processed: int
    batch_size: int
    status: str


# Webhook Models
class WebhookFilter(BaseModel):
    """Webhook event filters."""

    space_ids: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class Webhook(BaseResponse):
    """Webhook configuration."""

    id: str
    name: str
    url: str
    events: List[WebhookEvent]
    space_id: Optional[str] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    filters: Optional[WebhookFilter] = None
    active: bool = True
    created_at: datetime
    updated_at: datetime


class WebhookCreate(BaseModel):
    """Request to create a webhook."""

    name: str
    url: str
    events: List[WebhookEvent]
    space_id: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    filters: Optional[WebhookFilter] = None


class WebhookUpdate(BaseModel):
    """Request to update a webhook."""

    name: Optional[str] = None
    url: Optional[str] = None
    events: Optional[List[WebhookEvent]] = None
    headers: Optional[Dict[str, str]] = None
    filters: Optional[WebhookFilter] = None
    active: Optional[bool] = None


class WebhookList(BaseResponse):
    """List of webhooks."""

    data: List[Webhook]


class WebhookDelivery(BaseResponse):
    """Webhook delivery attempt."""

    id: str
    webhook_id: str
    event_type: WebhookEvent
    status_code: Optional[int] = None
    success: bool
    payload: Dict[str, Any]
    error: Optional[str] = None
    attempted_at: datetime


class WebhookDeliveryList(BaseResponse):
    """List of webhook deliveries."""

    data: List[WebhookDelivery]


# Agent Models
class AgentSession(BaseResponse):
    """Agent conversation session."""

    session_id: str
    space_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    ended_at: Optional[datetime] = None
    summary: Optional[str] = None


class SessionMemory(BaseResponse):
    """Memory within an agent session."""

    id: str
    session_id: str
    content: str
    role: Optional[str] = None
    importance: Optional[float] = None
    created_at: datetime


class SessionMemoryList(BaseResponse):
    """List of session memories."""

    data: List[SessionMemory]
    total: int


class SessionList(BaseResponse):
    """List of agent sessions."""

    data: List[AgentSession]


class ConsolidationResult(BaseResponse):
    """Result of memory consolidation."""

    consolidated_count: int
    new_memories: List[Memory]
    removed_memory_ids: List[str]
    relationships_created: int
    dry_run: bool


class AgentContext(BaseResponse):
    """Contextual information for agent."""

    query: str
    memories: List[Memory]
    session_memories: List[SessionMemory]
    relevance_scores: Dict[str, float] = Field(default_factory=dict)


# Feedback Models
class FeedbackResult(BaseResponse):
    """Result object in feedback."""

    memory_id: str
    score: float
    rank: int


class FeedbackSubmit(BaseModel):
    """Submit detailed feedback."""

    query_context: str
    results: List[FeedbackResult]
    boost_amount: Optional[float] = None
    create_relationships: Optional[bool] = True


class FeedbackResponse(BaseResponse):
    """Feedback submission response."""

    relationships_created: int
    memories_boosted: int


# Highlight Models
class Highlight(BaseResponse):
    """Highlighted text within a memory."""

    id: str
    memory_id: str
    text: str
    note: Optional[str] = None
    importance: Optional[int] = None
    tags: List[str] = Field(default_factory=list)
    color: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class HighlightCreate(BaseModel):
    """Request to create a highlight."""

    text: str
    note: Optional[str] = None
    importance: Optional[int] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = None


class HighlightUpdate(BaseModel):
    """Request to update a highlight."""

    text: Optional[str] = None
    note: Optional[str] = None
    importance: Optional[int] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = None


class HighlightList(BaseResponse):
    """List of highlights."""

    data: List[Highlight]


class ExtractedHighlights(BaseResponse):
    """Automatically extracted highlights."""

    memory_id: str
    extraction_type: ExtractionType
    highlights: List[Dict[str, Any]]


# ============================================================================
# Transcript Types - Audio/Video Transcription
# ============================================================================


class TimestampRange(BaseModel):
    """Timestamp range for content safety labels."""

    start: float
    end: float


class ContentSafetyLabel(BaseModel):
    """Content safety detection result."""

    label: str
    confidence: float
    severity: str
    timestamp: Optional[TimestampRange] = None


class WordTimestamp(BaseModel):
    """Word-level timestamp with optional speaker label."""

    word: str
    start: float
    end: float
    confidence: Optional[float] = None
    speaker: Optional[str] = None


class TranscriptSegment(BaseModel):
    """Transcript segment with speaker information and word-level details."""

    id: Optional[str] = None
    start_time: float
    end_time: float
    text: str
    segment_index: int
    confidence: Optional[float] = None
    speaker: Optional[str] = None
    words: Optional[List[WordTimestamp]] = None
    word_confidence_avg: Optional[float] = None


class TranscriptEntity(BaseModel):
    """Detected entity in transcript."""

    id: Optional[str] = None
    entity_type: str
    text: str
    start_time: float
    end_time: float
    confidence: float
    metadata: Optional[Dict[str, Any]] = None


class TranscriptChapter(BaseModel):
    """Auto-generated chapter."""

    id: Optional[str] = None
    chapter_index: int
    headline: str
    summary: str
    gist: str
    start_time: float
    end_time: float


class Transcript(BaseResponse):
    """Full transcript with metadata, segments, entities, and chapters."""

    memory_id: str
    audio_file_id: Optional[str] = None
    text: str
    duration: Optional[float] = None
    language: Optional[str] = None
    language_confidence: Optional[float] = None
    provider: Optional[str] = None
    summary: Optional[str] = None
    content_safety_labels: Optional[List[ContentSafetyLabel]] = None
    provider_metadata: Optional[Dict[str, Any]] = None
    segments: Optional[List[TranscriptSegment]] = None
    entities: Optional[List[TranscriptEntity]] = None
    chapters: Optional[List[TranscriptChapter]] = None
    words: Optional[List[WordTimestamp]] = None


# Job Models
class Job(BaseResponse):
    """Background job."""

    id: str
    queue: str
    name: str
    data: Dict[str, Any]
    status: JobStatus
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class JobStats(BaseResponse):
    """Job queue statistics."""

    queue: str
    waiting: int
    active: int
    completed: int
    failed: int
    delayed: int


class JobList(BaseResponse):
    """List of jobs."""

    data: List[Job]


# ============================================================================
# Fact Types - Knowledge Graph Triples
# ============================================================================


class FactNodeType(str, Enum):
    """Type of subject/object in a fact."""

    ENTITY = "entity"
    TEXT = "text"
    MEMORY = "memory"


class FactSourceMethod(str, Enum):
    """Method used to create a fact."""

    MANUAL = "manual"
    EXTRACTED = "extracted"
    INFERRED = "inferred"


class FactSource(BaseModel):
    """Source attribution for a fact."""

    memory_id: Optional[str] = None
    session_id: Optional[str] = None
    method: Optional[FactSourceMethod] = None


class Fact(BaseResponse):
    """Fact object - represents a knowledge graph triple (Subject-Predicate-Object)."""

    id: str
    subject: str
    predicate: str
    object: str
    subject_type: Optional[FactNodeType] = None
    object_type: Optional[FactNodeType] = None
    confidence: float
    source: Optional[FactSource] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    space_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FactCreate(BaseModel):
    """Request to create a fact."""

    subject: str
    predicate: str
    object: str
    subject_type: Optional[FactNodeType] = None
    object_type: Optional[FactNodeType] = None
    confidence: Optional[float] = 1.0
    source: Optional[FactSource] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    space_id: Optional[str] = None


class FactUpdate(BaseModel):
    """Request to update a fact."""

    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    subject_type: Optional[FactNodeType] = None
    object_type: Optional[FactNodeType] = None
    confidence: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class FactList(BaseResponse):
    """List of facts with pagination."""

    data: List[Fact]
    total: int = 0
    limit: int = 10
    offset: int = 0


class ScoredFact(Fact):
    """Fact with relevance score."""

    score: float


class FactQueryResult(BaseResponse):
    """Result of fact query."""

    data: List[ScoredFact]


class ExtractedFact(BaseModel):
    """A fact extracted from memory content."""

    subject: str
    predicate: str
    object: str
    confidence: float


class FactExtractionResult(BaseResponse):
    """Result of fact extraction from a memory."""

    memory_id: str
    facts: List[ExtractedFact]
    saved: bool = False


class FactVerificationResult(BaseResponse):
    """Result of fact verification."""

    fact_id: str
    verified: bool
    confidence: float
    supporting_memories: List[str] = Field(default_factory=list)
    contradicting_memories: List[str] = Field(default_factory=list)


# ============================================================================
# Entity Types - Named Entity Management
# ============================================================================


class Entity(BaseResponse):
    """Entity object - represents a named entity."""

    id: str
    name: str
    type: str
    aliases: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    memory_ids: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    space_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class EntityCreate(BaseModel):
    """Request to create an entity."""

    name: str
    type: str
    aliases: Optional[List[str]] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    memory_ids: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    space_id: Optional[str] = None


class EntityUpdate(BaseModel):
    """Request to update an entity."""

    name: Optional[str] = None
    type: Optional[str] = None
    aliases: Optional[List[str]] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class EntityList(BaseResponse):
    """List of entities with pagination."""

    data: List[Entity]
    total: int = 0
    limit: int = 10
    offset: int = 0


class ScoredEntity(Entity):
    """Entity with relevance score."""

    score: float


class EntitySearchResult(BaseResponse):
    """Result of entity search."""

    data: List[ScoredEntity]


class EntityResolutionResult(BaseResponse):
    """Result of entity resolution."""

    text: str
    entity: Optional[Entity] = None
    confidence: float
    alternatives: List[Dict[str, Any]] = Field(default_factory=list)


class EntityMergeResult(BaseResponse):
    """Result of entity merge."""

    merged_entity: Entity
    deleted_id: str


class EntityMemoryLinkResult(BaseResponse):
    """Result of entity-memory link."""

    entity_id: str
    memory_id: str
    linked: bool


class ExtractedEntity(BaseModel):
    """An entity extracted from memory content."""

    name: str
    type: str
    confidence: float
    span_start: Optional[int] = None
    span_end: Optional[int] = None


class EntityExtractionResult(BaseResponse):
    """Result of entity extraction from a memory."""

    memory_id: str
    entities: List[ExtractedEntity]
    saved: bool = False
    linked: bool = False


class EntityTypeInfo(BaseModel):
    """Entity type with count."""

    name: str
    count: int


class EntityTypesResult(BaseResponse):
    """Result of getting entity types."""

    types: List[EntityTypeInfo]


class EntityFactsResult(BaseResponse):
    """Result of getting entity facts."""

    entity_id: str
    facts: List[Fact]


# ============================================================================
# Enrichment Types - Memory Enrichments
# ============================================================================


class EnrichmentStatus(str, Enum):
    """Enrichment processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class EnrichmentType(str, Enum):
    """Types of enrichments."""

    ENTITIES = "entities"
    SUMMARY = "summary"
    SENTIMENT = "sentiment"
    TOPICS = "topics"
    KEYWORDS = "keywords"
    CUSTOM = "custom"


class EnrichmentOperation(str, Enum):
    """Enrichment operations that can be triggered."""

    TOPICS = "topics"
    SUMMARY = "summary"
    ENTITIES = "entities"
    QUALITY = "quality"


class Enrichment(BaseResponse):
    """Enrichment object for a memory."""

    type: str
    status: EnrichmentStatus
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class EnrichmentList(BaseResponse):
    """List of enrichments."""

    data: List[Enrichment]


class EnrichmentResult(BaseResponse):
    """Result of triggering enrichments."""

    memory_id: str
    triggered: List[str]
    job_ids: Optional[List[str]] = None
    status: str


# ============================================================================
# Topic Types - Topic Extraction
# ============================================================================


class Topic(BaseModel):
    """Extracted topic from a memory."""

    name: str
    relevance: float  # 0-1 relevance score
    category: str


class TopicList(BaseResponse):
    """List of topics extracted from a memory."""

    memory_id: str
    topics: List[Topic]


class TopicSearchResult(BaseResponse):
    """Result of searching by topic."""

    topic: str
    memories: List["Memory"]


# ============================================================================
# Memory Stats Types
# ============================================================================


class MemoryStats(BaseResponse):
    """Memory statistics."""

    total: int
    by_type: Optional[Dict[str, int]] = None
    by_tag: Optional[Dict[str, int]] = None
    timeline: Optional[List[Dict[str, Any]]] = None
    avg_content_length: Optional[float] = None
    total_size: Optional[int] = None


# ============================================================================
# Cluster Extended Types
# ============================================================================


class ClusterStats(BaseResponse):
    """Cluster statistics."""

    total: int
    avg_size: float
    avg_quality: float
    by_space: Optional[Dict[str, int]] = None


class ClusterQuality(BaseResponse):
    """Cluster quality metrics."""

    cluster_id: str
    coherence: float
    separation: float
    silhouette_score: float
    outlier_count: int


class ClusterTopic(BaseModel):
    """A topic in a cluster."""

    label: str
    score: float
    keywords: List[str]


class ClusterTopics(BaseResponse):
    """Cluster topics."""

    cluster_id: str
    topics: List[ClusterTopic]


class IncrementalClusterResult(BaseResponse):
    """Result of incremental clustering."""

    job_id: str
    status: str
    estimated_memories: int


# ============================================================================
# Relationship Extended Types
# ============================================================================


class RelationshipTypeInfo(BaseModel):
    """Relationship type info."""

    name: str
    count: int
    description: Optional[str] = None


class RelationshipTypesResult(BaseResponse):
    """Result of getting relationship types."""

    types: List[RelationshipTypeInfo]


class RelatedMemory(BaseModel):
    """A related memory with relationship info."""

    memory: Memory
    relationship: "Relationship"
    score: float


class RelatedMemoriesResult(BaseResponse):
    """Result of getting related memories."""

    memory_id: str
    related: List[RelatedMemory]


class ReinforceGroupResult(BaseResponse):
    """Result of reinforcing a group of relationships."""

    reinforced: int
    failed: int


# ============================================================================
# Graph Extended Types
# ============================================================================


class GraphNeighbor(BaseModel):
    """A neighbor in the graph."""

    id: str
    type: str
    relationship: "Relationship"


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


# ============================================================================
# Agent Core Memory Types
# ============================================================================


class CoreMemoryBlock(BaseModel):
    """Core memory block."""

    type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    updated_at: datetime


class CoreMemory(BaseResponse):
    """Core memory."""

    blocks: List[CoreMemoryBlock]
    updated_at: datetime


class CoreMemoryContext(BaseResponse):
    """Formatted core memory context."""

    formatted: str
    blocks: List[CoreMemoryBlock]


# ============================================================================
# Webhook Extended Types
# ============================================================================


class WebhookEventInfo(BaseModel):
    """Webhook event."""

    id: str
    type: str
    data: Dict[str, Any]
    created_at: datetime


class WebhookEventList(BaseResponse):
    """List of webhook events."""

    data: List[WebhookEventInfo]


class WebhookEventTypeInfo(BaseModel):
    """Webhook event type info."""

    name: str
    description: str
    event_schema: Optional[Dict[str, Any]] = Field(default=None, alias="schema")


class WebhookEventTypesResult(BaseResponse):
    """Result of getting webhook event types."""

    types: List[WebhookEventTypeInfo]


class WebhookEventStats(BaseModel):
    """Stats for a webhook event type."""

    count: int
    success_rate: float


class WebhookStats(BaseResponse):
    """Webhook statistics."""

    total_deliveries: int
    success_rate: float
    avg_latency: float
    by_event: Dict[str, WebhookEventStats]


# ============================================================================
# Highlight Extended Types
# ============================================================================


class HighlightWithScore(Highlight):
    """Highlight with search score."""

    score: float


class HighlightSearchResult(BaseResponse):
    """Highlight search result."""

    highlights: List[HighlightWithScore]


class HighlightTypeInfo(BaseModel):
    """Highlight type info."""

    name: str
    count: int
    color: Optional[str] = None


class HighlightTypesResult(BaseResponse):
    """Result of getting highlight types."""

    types: List[HighlightTypeInfo]


class HighlightLinkResult(BaseResponse):
    """Result of linking a highlight to a memory."""

    highlight_id: str
    memory_id: str
    linked: bool


# ============================================================================
# Resource Types - Project/Topic Management for Memory Context
# ============================================================================


class Resource(BaseResponse):
    """Resource object - represents a project, topic, or other grouping for memories."""

    id: str
    name: str
    type: str = "project"
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class ResourceCreate(BaseModel):
    """Request to create a resource."""

    name: str
    type: Optional[str] = "project"
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ResourceUpdate(BaseModel):
    """Request to update a resource."""

    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ResourceList(BaseResponse):
    """List of resources with pagination."""

    data: List[Resource]
    pagination: Pagination


class MemoryResource(BaseResponse):
    """Memory-resource link."""

    memory_id: str
    resource_id: str
    relationship_type: ResourceRelationshipType = ResourceRelationshipType.RELATED
    created_at: datetime
    resource: Optional[Resource] = None


class MemoryResourceList(BaseResponse):
    """List of memory-resource links."""

    data: List[MemoryResource]


class MemoryResourceLinkResult(BaseResponse):
    """Result of linking a resource to a memory."""

    memory_id: str
    resource_id: str
    relationship_type: ResourceRelationshipType
    linked: bool


class MemoryResourceUnlinkResult(BaseResponse):
    """Result of unlinking a resource from a memory."""

    memory_id: str
    resource_id: str
    unlinked: bool


# Session Models
class Session(BaseResponse):
    """CLI session for managing conversation/project/task contexts.

    Sessions provide lifecycle management for conversations, projects,
    and tasks with features like pause/resume, completion tracking,
    and automatic retention policies.

    Attributes:
        id: Unique session identifier.
        account_id: Account that owns the session.
        user_id: User that owns the session.
        created_by: User who created the session.
        name: Session name.
        description: Optional session description.
        type: Session type (conversation, project, task, temporary).
        status: Current lifecycle status (active, paused, completed, archived).
        space_id: Optional space association.
        origin_type: Optional origin context.
        tags: List of tags for categorization.
        retention_policy: Data retention policy.
        retention_days: Days to retain data (for auto_delete policy).
        summary: Optional session summary.
        is_private: Whether session is private to user.
        message_count: Number of messages in session.
        memory_count: Number of memories in session.
        metadata: Additional custom metadata.
        created_at: Session creation timestamp.
        updated_at: Last update timestamp.
        last_active_at: Last activity timestamp.
        paused_at: When session was paused (if applicable).
        completed_at: When session was completed (if applicable).
        archived_at: When session was archived (if applicable).
    """

    id: str
    account_id: str
    user_id: str
    created_by: str
    name: str
    description: Optional[str] = None
    type: SessionType
    status: SessionStatus
    space_id: Optional[str] = None
    origin_type: Optional[str] = None
    tags: Optional[List[str]] = None
    retention_policy: RetentionPolicy
    retention_days: Optional[int] = None
    summary: Optional[str] = None
    is_private: bool = False
    message_count: int = 0
    memory_count: int = 0
    metadata: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str
    last_active_at: str
    paused_at: Optional[str] = None
    completed_at: Optional[str] = None
    archived_at: Optional[str] = None


class CreateSessionParams(BaseModel):
    """Parameters for creating a new session.

    Attributes:
        name: Session name (required).
        description: Optional session description.
        type: Session type (default: conversation).
        space_id: Optional space to associate with.
        origin_type: Optional origin context.
        tags: List of tags.
        retention_policy: Retention policy (default: permanent).
        retention_days: Days to retain (for auto_delete).
        is_private: Whether session is private.
        metadata: Additional custom metadata.
    """

    name: str
    description: Optional[str] = None
    type: SessionType = SessionType.CONVERSATION
    space_id: Optional[str] = None
    origin_type: Optional[str] = None
    tags: Optional[List[str]] = None
    retention_policy: RetentionPolicy = RetentionPolicy.PERMANENT
    retention_days: Optional[int] = None
    is_private: bool = False
    metadata: Optional[Dict[str, Any]] = None


class UpdateSessionParams(BaseModel):
    """Parameters for updating a session.

    All fields are optional. Only provided fields will be updated.

    Attributes:
        name: New session name.
        description: New description.
        tags: New tags list.
        retention_policy: New retention policy.
        retention_days: New retention days.
        is_private: New privacy setting.
        metadata: New metadata.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    retention_policy: Optional[RetentionPolicy] = None
    retention_days: Optional[int] = None
    is_private: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class CompleteSessionParams(BaseModel):
    """Parameters for completing a session.

    Attributes:
        summary: Optional completion summary.
    """

    summary: Optional[str] = None


class SessionsResponse(BaseResponse):
    """Paginated list of sessions.

    Attributes:
        data: List of session objects.
        total: Total number of sessions matching filters.
        limit: Maximum items per page.
        offset: Current offset in result set.
    """

    data: List[Session]
    total: int
    limit: int
    offset: int


class SessionStats(BaseResponse):
    """Session statistics.

    Attributes:
        total: Total number of sessions.
        active: Number of active sessions.
        paused: Number of paused sessions.
        completed: Number of completed sessions.
        archived: Number of archived sessions.
        by_type: Distribution by session type.
        total_messages: Total messages across all sessions.
        total_memories: Total memories across all sessions.
    """

    total: int
    active: int
    paused: int
    completed: int
    archived: int
    by_type: Dict[str, int]
    total_messages: int
    total_memories: int


# ============================================================================
# Image Types - Visual Search and Image Processing
# ============================================================================


class VisualSearchResult(BaseResponse):
    """Result of visual similarity search.

    Attributes:
        memory: The matching memory object.
        score: Similarity score (0-1).
        distance: Distance metric value (lower is more similar).
    """

    memory: "Memory"
    score: float
    distance: Optional[float] = None


class VisualSearchResults(BaseResponse):
    """List of visual search results.

    Attributes:
        data: List of visual search results.
        query_type: Type of query performed (image, text).
    """

    data: List[VisualSearchResult]
    query_type: Optional[str] = None


class ImageCluster(BaseModel):
    """A cluster of visually similar images.

    Attributes:
        cluster_id: Unique identifier for the cluster.
        representative_id: Memory ID of the representative image.
        memory_ids: List of memory IDs in this cluster.
        size: Number of images in the cluster.
        centroid: Optional cluster centroid embedding.
    """

    cluster_id: int
    representative_id: Optional[str] = None
    memory_ids: List[str]
    size: int
    centroid: Optional[List[float]] = None


class ImageClusterResult(BaseResponse):
    """Result of image clustering operation.

    Attributes:
        clusters: List of image clusters.
        total_images: Total number of images clustered.
        num_clusters: Number of clusters created.
        silhouette_score: Optional quality metric for clustering.
    """

    clusters: List[ImageCluster]
    total_images: int
    num_clusters: int
    silhouette_score: Optional[float] = None


class ImageTag(BaseModel):
    """Auto-generated tag for an image.

    Attributes:
        name: Tag name/label.
        confidence: Confidence score (0-1).
        category: Optional category for the tag.
    """

    name: str
    confidence: float
    category: Optional[str] = None


class AutoTagResult(BaseResponse):
    """Result of auto-tagging an image.

    Attributes:
        image_id: Memory ID of the tagged image.
        tags: List of generated tags.
        applied: Whether tags were applied to the memory.
    """

    image_id: str
    tags: List[ImageTag]
    applied: bool = False


class BatchAutoTagResult(BaseResponse):
    """Result of batch auto-tagging images.

    Attributes:
        results: List of auto-tag results.
        success: Number of successfully tagged images.
        failed: Number of failed images.
    """

    results: List[AutoTagResult]
    success: int
    failed: int


class DuplicateCheckResult(BaseResponse):
    """Result of duplicate image check.

    Attributes:
        is_duplicate: Whether the image is a duplicate.
        duplicates: List of potential duplicate memory IDs with scores.
        threshold: Similarity threshold used.
    """

    is_duplicate: bool
    duplicates: List[Dict[str, Any]] = Field(default_factory=list)
    threshold: float = 0.95


class QuerySuggestion(BaseModel):
    """A suggested search query.

    Attributes:
        query: The suggested query text.
        type: Type of suggestion (tag, topic, etc.).
        count: Number of matching memories.
    """

    query: str
    type: str
    count: Optional[int] = None


class QuerySuggestionsResult(BaseResponse):
    """Result of query suggestions.

    Attributes:
        suggestions: List of query suggestions.
    """

    suggestions: List[QuerySuggestion]
