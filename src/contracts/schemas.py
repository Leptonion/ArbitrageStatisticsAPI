from typing import List

from pydantic import BaseModel

from general_schemas import RowResponse, DBContract, ListingResponse


class Contract(RowResponse):
    data: DBContract
    details: str = "Contact details by ID"


class Contracts(ListingResponse):
    data: List[DBContract]
    details: str = "List of Contracts"


"""Error Schemas"""


class ContractError(BaseModel):
    details: str = "Contract not found"
