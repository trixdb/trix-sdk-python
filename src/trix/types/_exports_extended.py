"""Extended type exports for Trix SDK.

These are re-exported from types.__init__ for backward compatibility.
Separated to keep the main __init__.py within the 300-line guideline.
"""

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
    BotRunBatchRequest,
    BotRunBatchResult,
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
    NoteLink,
    NoteLinkCreate,
    NoteList,
    NoteMemoryLink,
    NoteMemoryLinkCreate,
    NoteMemoryList,
    NoteUpdate,
)

# =============================================================================
# Template Models
# =============================================================================
from .template import (
    Template,
    TemplateCreate,
    TemplateInstallResult,
    TemplateList,
    TemplateReview,
    TemplateReviewCreate,
    TemplateUpdate,
)

# =============================================================================
# Hub Models
# =============================================================================
from .hub import (
    AddConversationMemberParams,
    AddHubMemberParams,
    ConversationMember,
    ConversationMemberList,
    ConvRoleOverride,
    ConvRoleOverrideList,
    CreateRoleParams,
    HubCustomRole,
    HubCustomRoleList,
    HubMember,
    HubMemberList,
    UpdateConversationMemberParams,
    UpdateHubMemberParams,
    UpdateRoleParams,
)

# =============================================================================
# Crew Models
# =============================================================================
from .crew import (
    Crew,
    CrewCreate,
    CrewList,
    CrewMember,
    CrewUpdate,
)

# =============================================================================
# Bot Run Step Models
# =============================================================================
from .bot_run_step import (
    BotRunStep,
    BotRunStreamRequest,
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

# =============================================================================
# Invite Models
# =============================================================================
from .invite import (
    Invite,
    InviteAccept,
    InviteAcceptResult,
    InviteCreate,
    InviteCreateResult,
    InviteList,
    InviteRevokeResult,
)

# =============================================================================
# Skill Models
# =============================================================================
from .skill import (
    BotSkillAttachment,
    Skill,
    SkillCreate,
    SkillList,
    SkillUpdate,
)

# =============================================================================
# File Models (ADR-068)
# =============================================================================
from .file import (
    ChatFile,
    FileDownloadInfo,
    FileListResult,
    FileQuota,
    FileUploadBase64,
)

# =============================================================================
# Calendar Models (ADR-075)
# =============================================================================
from .calendar import (
    Calendar,
    CalendarConnection,
    CalendarConnectionsResponse,
    CalendarEvent,
    CalendarEventTime,
    CalendarEventsResponse,
    CalendarListResponse,
    CalendarSyncResult,
    SyncCalendarParams,
)

__all__ = [
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
    "BotRunBatchRequest",
    "BotRunBatchResult",
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
    "NoteLink",
    "NoteLinkCreate",
    "NoteList",
    "NoteMemoryLink",
    "NoteMemoryLinkCreate",
    "NoteMemoryList",
    "NoteUpdate",
    # Template
    "Template",
    "TemplateCreate",
    "TemplateInstallResult",
    "TemplateList",
    "TemplateReview",
    "TemplateReviewCreate",
    "TemplateUpdate",
    # Hub
    "AddConversationMemberParams",
    "AddHubMemberParams",
    "ConversationMember",
    "ConversationMemberList",
    "ConvRoleOverride",
    "ConvRoleOverrideList",
    "CreateRoleParams",
    "HubCustomRole",
    "HubCustomRoleList",
    "HubMember",
    "HubMemberList",
    "UpdateConversationMemberParams",
    "UpdateHubMemberParams",
    "UpdateRoleParams",
    # Crew
    "Crew",
    "CrewCreate",
    "CrewList",
    "CrewMember",
    "CrewUpdate",
    # Bot Run Step
    "BotRunStep",
    "BotRunStreamRequest",
    # Space Config
    "SpaceConfigAuditEvent",
    "SpaceConfigAuditResponse",
    "SpaceConfigCategory",
    "SpaceConfigPatch",
    "SpaceConfigResponse",
    "SpaceConfigValidation",
    # Invite
    "Invite",
    "InviteAccept",
    "InviteAcceptResult",
    "InviteCreate",
    "InviteCreateResult",
    "InviteList",
    "InviteRevokeResult",
    # Skill
    "BotSkillAttachment",
    "Skill",
    "SkillCreate",
    "SkillList",
    "SkillUpdate",
    # File
    "ChatFile",
    "FileDownloadInfo",
    "FileListResult",
    "FileQuota",
    "FileUploadBase64",
    # Calendar
    "Calendar",
    "CalendarConnection",
    "CalendarConnectionsResponse",
    "CalendarEvent",
    "CalendarEventTime",
    "CalendarEventsResponse",
    "CalendarListResponse",
    "CalendarSyncResult",
    "SyncCalendarParams",
]
