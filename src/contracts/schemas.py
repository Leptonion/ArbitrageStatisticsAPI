from typing import List

from general_schemas import RowResponse, DBContract, ListingResponse


class Contract(RowResponse):
    data: DBContract
    details: str = "Contact details by ID"


class Contracts(ListingResponse):
    data: List[DBContract]
    details: str = "List of Contracts"
