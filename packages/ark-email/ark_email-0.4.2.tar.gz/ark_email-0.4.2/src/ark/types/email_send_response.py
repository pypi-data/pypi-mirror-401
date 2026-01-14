# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.api_meta import APIMeta

__all__ = ["EmailSendResponse", "Data"]


class Data(BaseModel):
    id: str
    """Unique message ID (format: msg*{id}*{token})"""

    status: Literal["pending", "sent"]
    """Current delivery status"""

    to: List[str]
    """List of recipient addresses"""

    message_id: Optional[str] = FieldInfo(alias="messageId", default=None)
    """SMTP Message-ID header value"""


class EmailSendResponse(BaseModel):
    data: Data

    meta: APIMeta

    success: Literal[True]
