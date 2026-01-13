# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .entity_type import EntityType
from .signal_type_config_param import SignalTypeConfigParam

__all__ = ["SignalCsvConfigParam"]


class SignalCsvConfigParam(TypedDict, total=False):
    """CSV-based signal monitoring configuration.

    Monitors signals for entities uploaded via CSV file.

    Attributes:
        type: Config type discriminator (always "signal-csv").
        file_id: ID of the uploaded CSV file.
        signal_types: Types of signals to monitor.
        entity_type: Type of entity being monitored (default: company).
        primary_column: Column containing entity names (default: "name").
        monitoring_frequency: How often to check (daily/weekly/monthly).
        webhook_url: Optional webhook URL for completion notification.

    Example:
        >>> config = SignalCSVConfigRequest(
        ...     file_id="abc123",
        ...     signal_types=[SignalTypeConfig(type="hiring_surge", ...)]
        ... )
    """

    file_id: Required[str]
    """ID of the uploaded CSV file"""

    signal_types: Required[Iterable[SignalTypeConfigParam]]
    """Types of signals to monitor"""

    entity_type: EntityType
    """Type of entity being monitored"""

    monitoring_frequency: Literal["daily", "weekly", "monthly"]
    """How often to check for new signals"""

    primary_column: str
    """Column containing entity names"""

    type: Literal["signal-csv"]
    """Config type discriminator"""

    webhook_url: Optional[str]
    """Optional webhook URL to notify when workflow completes"""
