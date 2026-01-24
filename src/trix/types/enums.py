"""Enum types for Trix SDK."""

from enum import Enum


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

    FINE = "fine"
    MEDIUM = "medium"
    COARSE = "coarse"


class ProtectionLevel(str, Enum):
    """Memory protection levels to control decay and deletion."""

    NONE = "none"
    SOFT = "soft"
    HARD = "hard"


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


class WebhookEvent(str, Enum):
    """Webhook event types."""

    MEMORY_CREATED = "memory.created"
    MEMORY_UPDATED = "memory.updated"
    MEMORY_DELETED = "memory.deleted"
    RELATIONSHIP_CREATED = "relationship.created"
    CLUSTER_CREATED = "cluster.created"


class OriginType(str, Enum):
    """Origin types for memory context classification."""

    WORK = "work"
    PRIVATE = "private"
    SHARED = "shared"
    LEARNING = "learning"


class SourceType(str, Enum):
    """Source types for memory provenance tracking."""

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
    """Relationship types for memory-resource associations."""

    PRIMARY = "primary"
    RELATED = "related"
    MENTIONED = "mentioned"
    DERIVED = "derived"


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
