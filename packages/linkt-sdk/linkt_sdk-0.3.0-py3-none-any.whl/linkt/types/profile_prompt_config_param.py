# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ProfilePromptConfigParam"]


class ProfilePromptConfigParam(TypedDict, total=False):
    """Profile prompt task configuration.

    Configures a profile workflow with a custom prompt template.

    Attributes:
        type: Config type discriminator (always "profile").
        prompt: Jinja2 template for task instructions.
        webhook_url: Optional webhook URL for completion notification.

    Example:
        >>> config = ProfilePromptConfigRequest(prompt="Analyze {{ company_name }} and extract key metrics.")
    """

    prompt: Required[str]
    """Jinja2 template for task instructions"""

    type: Literal["profile"]
    """Config type discriminator"""

    webhook_url: Optional[str]
    """Optional webhook URL to notify when workflow completes"""
