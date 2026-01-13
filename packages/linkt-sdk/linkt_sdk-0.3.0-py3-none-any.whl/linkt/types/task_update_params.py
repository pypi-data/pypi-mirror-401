# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import TypeAlias, TypedDict

from .signal_csv_config_param import SignalCsvConfigParam
from .ingest_task_config_param import IngestTaskConfigParam
from .search_task_config_param import SearchTaskConfigParam
from .signal_sheet_config_param import SignalSheetConfigParam
from .signal_topic_config_param import SignalTopicConfigParam
from .profile_prompt_config_param import ProfilePromptConfigParam

__all__ = ["TaskUpdateParams", "TaskConfig"]


class TaskUpdateParams(TypedDict, total=False):
    deployment_name: Optional[str]
    """Updated deployment name"""

    description: Optional[str]
    """Updated task description"""

    icp_id: Optional[str]
    """Updated ICP Connection"""

    name: Optional[str]
    """Updated task name"""

    prompt: Optional[str]
    """Updated task prompt template"""

    task_config: Optional[TaskConfig]
    """Updated flow-specific task configuration with type discriminator"""


TaskConfig: TypeAlias = Union[
    SearchTaskConfigParam,
    IngestTaskConfigParam,
    ProfilePromptConfigParam,
    SignalTopicConfigParam,
    SignalCsvConfigParam,
    SignalSheetConfigParam,
]
