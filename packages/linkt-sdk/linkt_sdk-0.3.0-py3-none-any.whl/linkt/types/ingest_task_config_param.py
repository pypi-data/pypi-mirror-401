# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["IngestTaskConfigParam"]


class IngestTaskConfigParam(TypedDict, total=False):
    """CSV enrichment task configuration.

    Enriches entities from an uploaded CSV file with additional
    data discovered by AI agents.

    Attributes:
        type: Config type discriminator (always "ingest").
        file_id: ID of the uploaded CSV file to process.
        primary_column: Column containing entity names for matching.
        csv_entity_type: Entity type in the CSV (e.g., 'person', 'company').
        webhook_url: Optional webhook URL for completion notification.

    Example:
        >>> config = IngestTaskConfigRequest(file_id="abc123", primary_column="company_name", csv_entity_type="company")
    """

    csv_entity_type: Required[str]
    """Entity type in the CSV (e.g., 'person', 'company')"""

    file_id: Required[str]
    """ID of the uploaded CSV file to process"""

    primary_column: Required[str]
    """Column containing entity names for matching"""

    type: Literal["ingest"]
    """Config type discriminator"""

    webhook_url: Optional[str]
    """Optional webhook URL to notify when workflow completes"""
