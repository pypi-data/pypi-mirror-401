# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["SearchTaskConfigParam"]


class SearchTaskConfigParam(TypedDict, total=False):
    """Search task configuration for finding companies and contacts.

    Creates a v3.0 search workflow that uses AI agents to discover
    entities matching your ICP criteria.

    Attributes:
        type: Config type discriminator (always "search").
        desired_contact_count: Number of contacts to find per company (minimum: 1).
        user_feedback: Optional feedback to refine search behavior.
        webhook_url: Optional webhook URL for completion notification.

    Example:
        >>> config = SearchTaskConfigRequest(desired_contact_count=5)
        >>> mongo_config = config.to_mongo_config()
        >>> mongo_config.version
        'v3.0'
    """

    desired_contact_count: int
    """Number of contacts to find per company (minimum: 1)"""

    type: Literal["search"]
    """Config type discriminator"""

    user_feedback: str
    """Optional feedback to refine search behavior"""

    webhook_url: Optional[str]
    """Optional webhook URL to notify when workflow completes"""
