# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["WebhookUpdateParams"]


class WebhookUpdateParams(TypedDict, total=False):
    all_events: Annotated[bool, PropertyInfo(alias="allEvents")]

    enabled: bool

    events: SequenceNotStr[str]

    name: str

    url: str
