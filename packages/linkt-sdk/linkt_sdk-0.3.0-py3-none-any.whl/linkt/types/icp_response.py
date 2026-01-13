# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["IcpResponse", "EntityTarget"]


class EntityTarget(BaseModel):
    """Response model for entity target configuration.

    Synchronized with core.schema.mongo.icp.EntityTargetConfig to return
    all configuration fields stored in the database to API consumers.

    Attributes:
        root: If True, this is the root entity type of the search hierarchy.
        entity_type: The entity type this config targets (e.g., 'company', 'person').
        description: Business description of what makes a good target.
        desired_count: For non-root entities, the desired number of entities
            per parent. Returns None if not explicitly set in the ICP.

    Note:
        The `desired_count` field is included in responses to enable API
        consumers to see the full configuration. When None, the system
        applies its default minimum (typically 2).
    """

    description: str
    """Business description of targets"""

    entity_type: str
    """Entity type (company, person, etc.)"""

    root: bool
    """If this is the root entity type"""

    desired_count: Optional[int] = None
    """For non-root entities, desired count per parent"""


class IcpResponse(BaseModel):
    """Response model for ICP."""

    id: str

    created_at: datetime

    description: str

    entity_targets: List[EntityTarget]

    name: str

    updated_at: datetime
