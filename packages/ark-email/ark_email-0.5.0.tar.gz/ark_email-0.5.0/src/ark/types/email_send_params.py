# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmailSendParams", "Attachment"]


class EmailSendParams(TypedDict, total=False):
    from_: Required[Annotated[str, PropertyInfo(alias="from")]]
    """Sender email address. Must be from a verified domain.

    **Supported formats:**

    - Email only: `hello@yourdomain.com`
    - With display name: `Acme <hello@yourdomain.com>`
    - With quoted name: `"Acme Support" <support@yourdomain.com>`

    The domain portion must match a verified sending domain in your account.
    """

    subject: Required[str]
    """Email subject line"""

    to: Required[SequenceNotStr[str]]
    """Recipient email addresses (max 50)"""

    attachments: Optional[Iterable[Attachment]]
    """File attachments (accepts null)"""

    bcc: Optional[SequenceNotStr[str]]
    """BCC recipients (accepts null)"""

    cc: Optional[SequenceNotStr[str]]
    """CC recipients (accepts null)"""

    headers: Optional[Dict[str, str]]
    """Custom email headers (accepts null)"""

    html: Optional[str]
    """HTML body content (accepts null). Maximum 5MB (5,242,880 characters).

    Combined with attachments, the total message must not exceed 14MB.
    """

    reply_to: Annotated[Optional[str], PropertyInfo(alias="replyTo")]
    """Reply-to address (accepts null)"""

    tag: Optional[str]
    """Tag for categorization and filtering (accepts null)"""

    text: Optional[str]
    """
    Plain text body (accepts null, auto-generated from HTML if not provided).
    Maximum 5MB (5,242,880 characters).
    """

    idempotency_key: Annotated[str, PropertyInfo(alias="Idempotency-Key")]


class Attachment(TypedDict, total=False):
    content: Required[str]
    """Base64-encoded file content"""

    content_type: Required[Annotated[str, PropertyInfo(alias="contentType")]]
    """MIME type"""

    filename: Required[str]
    """Attachment filename"""
