# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["EntityTargetConfigParam"]


class EntityTargetConfigParam(TypedDict, total=False):
    """Request model for entity target configuration.

    Synchronized with core.schema.mongo.icp.EntityTargetConfig to ensure
    all fields available in the database model can be set via the API.

    Attributes:
        entity_type: The entity type to target (e.g., 'company', 'person').
        description: Business description of what makes a good target.
        root: If True, this is the root entity type of the search hierarchy.
            Only one entity target should be marked as root. Defaults to False
            for backward compatibility with existing API consumers.
        desired_count: For non-root entities, the desired number of entities
            per parent (minimum: 1). Uses `ge=1` Field constraint which
            generates `minimum: 1` in OpenAPI schema for SDK validation.
            If not specified, defaults to system minimum (typically 2).
        filters: Optional list of filter criteria to apply to the search.

    Note:
        The `root` and `desired_count` fields default to False and None
        respectively, making them optional in API requests for backward
        compatibility with existing integrations.
    """

    description: Required[str]
    """Business description of targets"""

    entity_type: Required[str]
    """Entity type to target (company, person, etc.)"""

    desired_count: Optional[int]
    """For non-root entities, desired count per parent (minimum: 1).

    If not specified, defaults to system minimum.
    """

    filters: SequenceNotStr[str]
    """Filters to apply"""

    root: bool
    """If this is the root entity type of the search.

    Only one entity target should be root.
    """
