"""Knowledge domain type exports for Trix SDK.

Covers: goal, fact, entity, enrichment, topic, resource, image types.
Re-exported from types.__init__ for backward compatibility.
"""

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

__all__ = [
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
]
