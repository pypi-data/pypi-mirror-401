# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.api_meta import APIMeta

__all__ = ["EmailRetrieveDeliveriesResponse", "Data", "DataDelivery"]


class DataDelivery(BaseModel):
    id: str
    """Delivery attempt ID"""

    status: str
    """Delivery status (lowercase)"""

    timestamp: float
    """Unix timestamp"""

    timestamp_iso: datetime = FieldInfo(alias="timestampIso")
    """ISO 8601 timestamp"""

    code: Optional[int] = None
    """SMTP response code"""

    details: Optional[str] = None
    """Status details"""

    output: Optional[str] = None
    """SMTP server response from the receiving mail server"""

    sent_with_ssl: Optional[bool] = FieldInfo(alias="sentWithSsl", default=None)
    """Whether TLS was used"""


class Data(BaseModel):
    deliveries: List[DataDelivery]

    message_id: str = FieldInfo(alias="messageId")
    """Internal message ID"""

    message_token: str = FieldInfo(alias="messageToken")
    """Message token"""


class EmailRetrieveDeliveriesResponse(BaseModel):
    data: Data

    meta: APIMeta

    success: Literal[True]
