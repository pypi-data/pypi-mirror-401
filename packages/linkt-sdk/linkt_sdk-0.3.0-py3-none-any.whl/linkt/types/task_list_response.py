# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .entity_type import EntityType
from .signal_type_config import SignalTypeConfig

__all__ = [
    "TaskListResponse",
    "Task",
    "TaskTaskConfig",
    "TaskTaskConfigSearchTaskConfigResponse",
    "TaskTaskConfigIngestTaskConfigResponse",
    "TaskTaskConfigProfilePromptConfigResponse",
    "TaskTaskConfigSignalTopicConfigResponse",
    "TaskTaskConfigSignalCsvConfigResponse",
    "TaskTaskConfigSignalSheetConfigResponse",
]


class TaskTaskConfigSearchTaskConfigResponse(BaseModel):
    """Search task configuration in API responses.

    Response model for search task configs that excludes backend-managed fields
    (version, config_type) from the API surface.

    Attributes:
        type: Config type discriminator (always "search").
        desired_contact_count: Number of contacts to find per company.
        user_feedback: Feedback to refine search behavior.
        webhook_url: Webhook URL for completion notification.
    """

    desired_contact_count: int
    """Number of contacts to find per company"""

    user_feedback: str
    """Feedback to refine search behavior"""

    type: Optional[Literal["search"]] = None

    webhook_url: Optional[str] = None
    """Webhook URL for completion notification"""


class TaskTaskConfigIngestTaskConfigResponse(BaseModel):
    """Ingest task configuration in API responses.

    Response model for CSV enrichment task configs that excludes backend-managed
    fields from the API surface.

    Attributes:
        type: Config type discriminator (always "ingest").
        file_id: ID of the CSV file.
        primary_column: Column containing entity names.
        csv_entity_type: Entity type in CSV.
        webhook_url: Webhook URL for completion notification.
    """

    csv_entity_type: str
    """Entity type in CSV"""

    file_id: str
    """ID of the CSV file"""

    primary_column: str
    """Column containing entity names"""

    type: Optional[Literal["ingest"]] = None

    webhook_url: Optional[str] = None
    """Webhook URL for completion notification"""


class TaskTaskConfigProfilePromptConfigResponse(BaseModel):
    """Profile prompt configuration in API responses.

    Response model for profile prompt task configs that excludes backend-managed
    fields from the API surface.

    Attributes:
        type: Config type discriminator (always "profile").
        prompt: Task prompt template.
        webhook_url: Webhook URL for completion notification.
    """

    prompt: str
    """Task prompt template"""

    type: Optional[Literal["profile"]] = None

    webhook_url: Optional[str] = None
    """Webhook URL for completion notification"""


class TaskTaskConfigSignalTopicConfigResponse(BaseModel):
    """Signal topic configuration in API responses.

    Response model for topic-based signal monitoring configs.

    Attributes:
        type: Config type discriminator (always "signal-topic").
        topic_criteria: Topic criteria for monitoring.
        signal_types: Types of signals to monitor.
        entity_type: Type of entity being monitored.
        monitoring_frequency: How often to check for signals.
        geographic_filters: Geographic regions to focus on.
        industry_filters: Industries to focus on.
        company_size_filters: Company size criteria.
        webhook_url: Webhook URL for completion notification.
    """

    entity_type: EntityType
    """Entity type"""

    monitoring_frequency: Literal["daily", "weekly", "monthly"]
    """Monitoring frequency"""

    signal_types: List[SignalTypeConfig]
    """Signal types"""

    topic_criteria: str
    """Topic criteria"""

    company_size_filters: Optional[List[str]] = None
    """Size filters"""

    geographic_filters: Optional[List[str]] = None
    """Geographic filters"""

    industry_filters: Optional[List[str]] = None
    """Industry filters"""

    type: Optional[Literal["signal-topic"]] = None

    webhook_url: Optional[str] = None
    """Webhook URL for completion notification"""


class TaskTaskConfigSignalCsvConfigResponse(BaseModel):
    """Signal CSV configuration in API responses.

    Response model for CSV-based signal monitoring configs.

    Attributes:
        type: Config type discriminator (always "signal-csv").
        file_id: CSV file ID.
        signal_types: Types of signals to monitor.
        entity_type: Type of entity being monitored.
        primary_column: Primary column for entity names.
        monitoring_frequency: How often to check for signals.
        webhook_url: Webhook URL for completion notification.
    """

    entity_type: EntityType
    """Entity type"""

    file_id: str
    """CSV file ID"""

    monitoring_frequency: Literal["daily", "weekly", "monthly"]
    """Monitoring frequency"""

    primary_column: str
    """Primary column"""

    signal_types: List[SignalTypeConfig]
    """Signal types"""

    type: Optional[Literal["signal-csv"]] = None

    webhook_url: Optional[str] = None
    """Webhook URL for completion notification"""


class TaskTaskConfigSignalSheetConfigResponse(BaseModel):
    """Signal sheet configuration in API responses.

    Response model for sheet-based signal monitoring configs.

    Attributes:
        type: Config type discriminator (always "signal-sheet").
        source_icp_id: Source ICP ID containing entities to monitor.
        signal_types: Types of signals to monitor.
        entity_type: Type of entity being monitored.
        entity_filters: Optional MongoDB query to filter entities.
        monitoring_frequency: How often to check for signals.
        webhook_url: Webhook URL for completion notification.
    """

    entity_type: EntityType
    """Entity type"""

    monitoring_frequency: Literal["daily", "weekly", "monthly"]
    """Monitoring frequency"""

    signal_types: List[SignalTypeConfig]
    """Signal types"""

    source_icp_id: str
    """Source ICP ID"""

    entity_filters: Optional[Dict[str, object]] = None
    """Entity filters"""

    type: Optional[Literal["signal-sheet"]] = None

    webhook_url: Optional[str] = None
    """Webhook URL for completion notification"""


TaskTaskConfig: TypeAlias = Annotated[
    Union[
        TaskTaskConfigSearchTaskConfigResponse,
        TaskTaskConfigIngestTaskConfigResponse,
        TaskTaskConfigProfilePromptConfigResponse,
        TaskTaskConfigSignalTopicConfigResponse,
        TaskTaskConfigSignalCsvConfigResponse,
        TaskTaskConfigSignalSheetConfigResponse,
        None,
    ],
    PropertyInfo(discriminator="type"),
]


class Task(BaseModel):
    """Response model for task data.

    Uses TaskConfigResponse discriminated union for proper OpenAPI schema
    generation with type-based discrimination.

    Attributes:
        id: Task ID.
        name: Task name.
        description: Task description.
        icp_id: Task ICP ID.
        flow_name: Prefect flow name.
        deployment_name: Prefect deployment name.
        prompt: Template prompt for the task.
        task_config: Flow-specific task configuration.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: str
    """Task ID"""

    created_at: datetime
    """Creation timestamp"""

    deployment_name: str
    """Prefect deployment name"""

    description: str
    """Task description"""

    flow_name: str
    """Prefect flow name"""

    name: str
    """Task name"""

    updated_at: datetime
    """Last update timestamp"""

    icp_id: Optional[str] = None
    """Task ICP ID"""

    prompt: Optional[str] = None
    """Template prompt for the task. Can include placeholders for runtime parameters."""

    task_config: Optional[TaskTaskConfig] = None
    """Flow-specific task configuration"""


class TaskListResponse(BaseModel):
    """Response model for paginated task list.

    Attributes:
        tasks: List of tasks.
        total: Total number of tasks matching filters.
        page: Current page number (1-based).
        page_size: Number of items per page.
    """

    page: int
    """Current page number (1-based)"""

    page_size: int
    """Number of items per page"""

    tasks: List[Task]
    """List of tasks"""

    total: int
    """Total number of tasks matching filters"""
