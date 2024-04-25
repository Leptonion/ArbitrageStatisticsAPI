from typing import List

from pydantic import BaseModel

from general_schemas import ListingResponse, DBProvider, RowResponse


class Provider(RowResponse):
    data: DBProvider
    details: str = "Provider information by ID"


class Providers(ListingResponse):
    data: List[DBProvider]
    details: str = "List of Providers"


"""Error Schemas"""


class ProviderError(BaseModel):
    details: str = "Provider not found"
