"""Resource modules for Trix SDK."""

from .agent import AgentResource
from .bots import AsyncBotsResource, BotsResource  # noqa: F401
from .calendar import AsyncCalendarResource, CalendarResource
from .clusters import ClustersResource
from .clusters_async import AsyncClustersResource  # noqa: F401
from .crews import AsyncCrewsResource, CrewsResource
from .enrichments import AsyncEnrichmentsResource, EnrichmentsResource
from .entities import EntitiesResource
from .entities_async import AsyncEntitiesResource
from .facts import FactsResource
from .facts_async import AsyncFactsResource
from .feedback import FeedbackResource
from .files import AsyncFilesResource, FilesResource
from .goals import GoalsResource
from .goals_async import AsyncGoalsResource
from .graph import GraphResource
from .habits import HabitsResource
from .habits_async import AsyncHabitsResource
from .highlights import HighlightsResource
from .hubs import AsyncHubsResource, HubsResource
from .hubs_roles import AsyncHubRolesResource, HubRolesResource
from .invites import AsyncInvitesResource, InvitesResource
from .knowledge import AsyncKnowledgeResource, KnowledgeResource
from .memories import AsyncMemoriesResource, MemoriesResource
from .notes import NotesResource
from .notes_async import AsyncNotesResource
from .presets import PresetsResource
from .presets_async import AsyncPresetsResource
from .relationships import RelationshipsResource
from .resources import AsyncResourcesResource, ResourcesResource
from .search import SearchResource
from .sessions import SessionsResource
from .sessions_async import AsyncSessionsResource
from .skills import AsyncSkillsResource, SkillsResource
from .space_config import AsyncSpaceConfigResource, SpaceConfigResource
from .spaces import SpacesResource
from .tasks import TasksResource
from .tasks_async import AsyncTasksResource
from .templates import AsyncTemplatesResource, TemplatesResource
from .webhooks import WebhooksResource
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
    "InvitesResource",
    "AsyncInvitesResource",
    "NotesResource",
    "AsyncNotesResource",
    "SkillsResource",
    "AsyncSkillsResource",
    "TemplatesResource",
    "AsyncTemplatesResource",
    "CrewsResource",
    "AsyncCrewsResource",
    "HubsResource",
    "AsyncHubsResource",
    "HubRolesResource",
    "AsyncHubRolesResource",
    "FilesResource",
    "AsyncFilesResource",
    "PresetsResource",
    "AsyncPresetsResource",
    "CalendarResource",
    "AsyncCalendarResource",
    "KnowledgeResource",
    "AsyncKnowledgeResource",
]
