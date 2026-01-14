# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmailSendRawParams"]


class EmailSendRawParams(TypedDict, total=False):
    data: Required[str]
    """Base64-encoded RFC 2822 message"""

    mail_from: Required[Annotated[str, PropertyInfo(alias="mailFrom")]]
    """Envelope sender address"""

    rcpt_to: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="rcptTo")]]
    """Envelope recipient addresses"""
