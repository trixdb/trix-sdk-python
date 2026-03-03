"""Resource modules for Trix SDK."""

from .agent import AgentResource
from .clusters import ClustersResource
from .enrichments import EnrichmentsResource, AsyncEnrichmentsResource
from .entities import EntitiesResource, AsyncEntitiesResource
from .facts import FactsResource, AsyncFactsResource
from .feedback import FeedbackResource
from .goals import GoalsResource
from .goals_async import AsyncGoalsResource
from .graph import GraphResource
from .highlights import HighlightsResource
from .memories import MemoriesResource, AsyncMemoriesResource
from .relationships import RelationshipsResource
from .resources import ResourcesResource, AsyncResourcesResource
from .search import SearchResource
from .sessions import SessionsResource, AsyncSessionsResource
from .spaces import SpacesResource
from .tasks import TasksResource
from .tasks_async import AsyncTasksResource
from .habits import HabitsResource
from .habits_async import AsyncHabitsResource
from .webhooks import WebhooksResource
from .bots import BotsResource, AsyncBotsResource
from .space_config import SpaceConfigResource, AsyncSpaceConfigResource
from .workflows import WorkflowsResource
from .workflows_async import AsyncWorkflowsResource

__all__ = [
    "AgentResource",
    "AsyncBotsResource",
    "AsyncEnrichmentsResource",
    "AsyncEntitiesResource",
    "AsyncFactsResource",
    "AsyncGoalsResource",
    "AsyncMemoriesResource",
    "AsyncResourcesResource",
    "AsyncSessionsResource",
    "AsyncTasksResource",
    "HabitsResource",
    "AsyncHabitsResource",
    "ClustersResource",
    "EnrichmentsResource",
    "EntitiesResource",
    "FactsResource",
    "FeedbackResource",
    "GoalsResource",
    "GraphResource",
    "HighlightsResource",
    "MemoriesResource",
    "RelationshipsResource",
    "ResourcesResource",
    "SearchResource",
    "SessionsResource",
    "SpacesResource",
    "TasksResource",
    "WebhooksResource",
    "SpaceConfigResource",
    "AsyncSpaceConfigResource",
    "WorkflowsResource",
    "AsyncWorkflowsResource",
]
