# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from .signal_csv_config_param import SignalCsvConfigParam
from .ingest_task_config_param import IngestTaskConfigParam
from .search_task_config_param import SearchTaskConfigParam
from .signal_sheet_config_param import SignalSheetConfigParam
from .signal_topic_config_param import SignalTopicConfigParam
from .profile_prompt_config_param import ProfilePromptConfigParam

__all__ = ["TaskCreateParams", "TaskConfig"]


class TaskCreateParams(TypedDict, total=False):
    deployment_name: Required[str]
    """The Prefect deployment name for this flow"""

    description: Required[str]
    """Detailed description of what this task accomplishes"""

    flow_name: Required[str]
    """The Prefect flow name (e.g., 'search', 'ingest', 'signal')"""

    name: Required[str]
    """Human-readable name for the task"""

    icp_id: Optional[str]
    """Optional ICP ID for signal monitoring tasks"""

    prompt: Optional[str]
    """Template prompt for the task. Can include placeholders for runtime parameters."""

    task_config: Optional[TaskConfig]
    """Flow-specific task configuration with type discriminator"""


TaskConfig: TypeAlias = Union[
    SearchTaskConfigParam,
    IngestTaskConfigParam,
    ProfilePromptConfigParam,
    SignalTopicConfigParam,
    SignalCsvConfigParam,
    SignalSheetConfigParam,
]
