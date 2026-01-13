# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .entity_type import EntityType
from .signal_type_config_param import SignalTypeConfigParam

__all__ = ["SignalSheetConfigParam"]


class SignalSheetConfigParam(TypedDict, total=False):
    """Sheet-based signal monitoring configuration.

    Monitors signals for entities from an existing discovery ICP's sheet.

    Attributes:
        type: Config type discriminator (always "signal-sheet").
        source_icp_id: ID of the discovery ICP containing entities to monitor.
        signal_types: Types of signals to monitor.
        entity_type: Type of entity being monitored (default: company).
        entity_filters: Optional MongoDB query to filter entities.
        monitoring_frequency: How often to check (daily/weekly/monthly).
        webhook_url: Optional webhook URL for completion notification.

    Example:
        >>> config = SignalSheetConfigRequest(
        ...     source_icp_id="icp123",
        ...     signal_types=[SignalTypeConfig(type="leadership_change", ...)]
        ... )
    """

    signal_types: Required[Iterable[SignalTypeConfigParam]]
    """Types of signals to monitor"""

    source_icp_id: Required[str]
    """ID of the discovery ICP containing entities to monitor"""

    entity_filters: Optional[Dict[str, object]]
    """Optional MongoDB query to filter entities"""

    entity_type: EntityType
    """Type of entity being monitored"""

    monitoring_frequency: Literal["daily", "weekly", "monthly"]
    """How often to check for new signals"""

    type: Literal["signal-sheet"]
    """Config type discriminator"""

    webhook_url: Optional[str]
    """Optional webhook URL to notify when workflow completes"""
