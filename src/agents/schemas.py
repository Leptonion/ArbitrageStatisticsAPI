from datetime import datetime
from typing import List

from pydantic import BaseModel

from general_schemas import ListingResponse, RowResponse, DBAgent


class Agent(RowResponse):
    status: str = "success"
    data: DBAgent | None
    details: str = "Agent information by ID"


class Agents(ListingResponse):
    data: List[DBAgent]
    details: str = "List of agents"


class Achievement(BaseModel):
    agent: DBAgent
    from_date: datetime
    to_date: datetime
    contracts_purchased: int = 4
    contract_expenses: float = 751.13
    offers_sold: int = 111
    earned_from_offers: float = 11242.46

    class Config:
        arbitrary_types_allowed = True


"""Error Schemas"""


class AgentError(BaseModel):
    details: str = "Agent not found"
