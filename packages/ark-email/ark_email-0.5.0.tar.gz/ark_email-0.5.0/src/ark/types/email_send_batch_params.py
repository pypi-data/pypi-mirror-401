# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmailSendBatchParams", "Email"]


class EmailSendBatchParams(TypedDict, total=False):
    emails: Required[Iterable[Email]]

    from_: Required[Annotated[str, PropertyInfo(alias="from")]]
    """Sender email for all messages"""

    idempotency_key: Annotated[str, PropertyInfo(alias="Idempotency-Key")]


class Email(TypedDict, total=False):
    subject: Required[str]

    to: Required[SequenceNotStr[str]]

    html: Optional[str]

    tag: Optional[str]

    text: Optional[str]
