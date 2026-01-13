# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr
from .entity_type import EntityType
from .signal_type_config_param import SignalTypeConfigParam

__all__ = ["SignalTopicConfigParam"]


class SignalTopicConfigParam(TypedDict, total=False):
    """Topic-based signal monitoring configuration.

    Monitors for signals based on topic criteria without requiring
    pre-existing entities.

    Attributes:
        type: Config type discriminator (always "signal-topic").
        topic_criteria: Natural language description of what to monitor.
        signal_types: Types of signals to monitor.
        entity_type: Type of entity being monitored (default: company).
        monitoring_frequency: How often to check (daily/weekly/monthly).
        geographic_filters: Optional geographic regions to focus on.
        industry_filters: Optional industries to focus on.
        company_size_filters: Optional company size criteria.
        webhook_url: Optional webhook URL for completion notification.

    Example:
        >>> config = SignalTopicConfigRequest(
        ...     topic_criteria="AI startups raising Series A",
        ...     signal_types=[SignalTypeConfig(type="funding", ...)]
        ... )
    """

    signal_types: Required[Iterable[SignalTypeConfigParam]]
    """Types of signals to monitor"""

    topic_criteria: Required[str]
    """Natural language description of what to monitor"""

    company_size_filters: Optional[SequenceNotStr[str]]
    """Company size criteria"""

    entity_type: EntityType
    """Type of entity being monitored"""

    geographic_filters: Optional[SequenceNotStr[str]]
    """Geographic regions to focus on"""

    industry_filters: Optional[SequenceNotStr[str]]
    """Industries to focus on"""

    monitoring_frequency: Literal["daily", "weekly", "monthly"]
    """How often to check for new signals"""

    type: Literal["signal-topic"]
    """Config type discriminator"""

    webhook_url: Optional[str]
    """Optional webhook URL to notify when workflow completes"""
