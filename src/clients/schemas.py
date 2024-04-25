from typing import List

from pydantic import BaseModel

from general_schemas import RowResponse, DBClient, ListingResponse


class Client(RowResponse):
    data: DBClient
    details: str = "Client information by ID"


class Clients(ListingResponse):
    data: List[DBClient]
    details: str = "List of Clients"


"""Error Schemas"""


class ClientError(BaseModel):
    details: str = "Client not found"