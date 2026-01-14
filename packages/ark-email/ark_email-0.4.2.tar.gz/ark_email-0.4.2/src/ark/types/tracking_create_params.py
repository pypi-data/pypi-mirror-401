# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TrackingCreateParams"]


class TrackingCreateParams(TypedDict, total=False):
    domain_id: Required[Annotated[str, PropertyInfo(alias="domainId")]]
    """ID of the sending domain to attach this track domain to"""

    name: Required[str]
    """Subdomain name (e.g., 'track' for track.yourdomain.com)"""

    ssl_enabled: Annotated[bool, PropertyInfo(alias="sslEnabled")]
    """Enable SSL for tracking URLs (recommended)"""

    track_clicks: Annotated[bool, PropertyInfo(alias="trackClicks")]
    """Enable click tracking"""

    track_opens: Annotated[bool, PropertyInfo(alias="trackOpens")]
    """Enable open tracking (tracking pixel)"""
