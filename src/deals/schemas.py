from datetime import datetime
from typing import List

from pydantic import BaseModel

from general_schemas import RowResponse, DBDeal, ListingResponse


class Deal(RowResponse):
    data: DBDeal
    details: str = "Deal details by ID"


class Deals(ListingResponse):
    data: List[DBDeal]
    details: str = "List of Deals"

"""Error Schemas"""


class DealError(BaseModel):
    details: str = "Deal not found"
