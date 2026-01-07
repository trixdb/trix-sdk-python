"""Resource modules for Trix SDK."""

from .agent import AgentResource
from .clusters import ClustersResource
from .enrichments import EnrichmentsResource, AsyncEnrichmentsResource
from .entities import EntitiesResource, AsyncEntitiesResource
from .facts import FactsResource, AsyncFactsResource
from .feedback import FeedbackResource
from .graph import GraphResource
from .highlights import HighlightsResource
from .jobs import JobsResource
from .memories import MemoriesResource
from .relationships import RelationshipsResource
from .resources import ResourcesResource, AsyncResourcesResource
from .search import SearchResource
from .sessions import SessionsResource, AsyncSessionsResource
from .spaces import SpacesResource
from .webhooks import WebhooksResource

__all__ = [
    "AgentResource",
    "AsyncEnrichmentsResource",
    "AsyncEntitiesResource",
    "AsyncFactsResource",
    "AsyncResourcesResource",
    "AsyncSessionsResource",
    "ClustersResource",
    "EnrichmentsResource",
    "EntitiesResource",
    "FactsResource",
    "FeedbackResource",
    "GraphResource",
    "HighlightsResource",
    "JobsResource",
    "MemoriesResource",
    "RelationshipsResource",
    "ResourcesResource",
    "SearchResource",
    "SessionsResource",
    "SpacesResource",
    "WebhooksResource",
]
