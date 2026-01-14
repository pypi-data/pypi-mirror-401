# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from typing_extensions import Literal

from .._models import BaseModel
from .shared.api_meta import APIMeta

__all__ = ["EmailSendBatchResponse", "Data", "DataMessages"]


class DataMessages(BaseModel):
    id: str
    """Message ID"""

    token: str


class Data(BaseModel):
    accepted: int
    """Successfully accepted emails"""

    failed: int
    """Failed emails"""

    messages: Dict[str, DataMessages]
    """Map of recipient email to message info"""

    total: int
    """Total emails in the batch"""


class EmailSendBatchResponse(BaseModel):
    data: Data

    meta: APIMeta

    success: Literal[True]
