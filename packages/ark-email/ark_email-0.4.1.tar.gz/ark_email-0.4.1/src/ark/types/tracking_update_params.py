# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TrackingUpdateParams"]


class TrackingUpdateParams(TypedDict, total=False):
    excluded_click_domains: Annotated[str, PropertyInfo(alias="excludedClickDomains")]
    """Comma-separated list of domains to exclude from click tracking"""

    ssl_enabled: Annotated[bool, PropertyInfo(alias="sslEnabled")]
    """Enable or disable SSL for tracking URLs"""

    track_clicks: Annotated[bool, PropertyInfo(alias="trackClicks")]
    """Enable or disable click tracking"""

    track_opens: Annotated[bool, PropertyInfo(alias="trackOpens")]
    """Enable or disable open tracking"""
