from datetime import datetime
from typing import List

from pydantic import BaseModel

from general_schemas import ListingResponse


class FullStats(BaseModel):
    contracts_purchased: int = 4
    contract_expenses: float = 751.13
    offers_sold: int = 111
    earned_from_offers: float = 11242.46
    paid_offers: float = 10256.95


class SeparationData(BaseModel):
    from_date: datetime
    to_date: datetime
    contracts_purchased: int = 4
    contract_expenses: float = 751.13
    offers_sold: int = 111
    earned_from_offers: float = 11242.46
    paid_offers: float = 10256.95
    contracts_purchased_by_previous: int = 47
    contract_expenses_by_previous: float = 9700.25
    offers_sold_by_previous: int = 135
    earned_from_offers_by_previous: float = 16245.63
    paid_offers_by_previous: float = 15245.63
    contracts_purchased_percent: float = 13.33
    contract_expenses_percent: float = 8.35
    offers_sold_percent: float = 2.04
    earned_from_offers_percent: float = 6.33
    paid_offers_percent: float = 17.33


class Graph(BaseModel):
    separation_by: str = "month"
    data: List[SeparationData]


class Stats(BaseModel):
    status: str = "success"
    from_date: datetime
    to_date: datetime
    data: FullStats
    graph: Graph
    details: str = "Full income/expense statistics by period"


class ProviderStatsData(BaseModel):
    provider: dict = {"id": 1,
                      "title": "Some Group.",
                      "platform": "youtube",
                      "branch": "science",
                      "site": "something.com",
                      "contact": "+100111111"}
    statistic: dict = {"contracts_purchased": 10,
                       "total_duration_days": 47,
                       "max_contract_duration_days": 25,
                       "min_contract_duration_days": 2,
                       "total_spent": 1032.45,
                       "max_cost_per_day": 22.15,
                       "min_cost_per_day": 12.05,
                       "total_deals_sold": 36,
                       "total_income_from_deals": 2343.15}


class ProviderStats(ListingResponse):
    from_date: datetime
    to_date: datetime
    sorted_by: str = "id"
    data: List[ProviderStatsData]
    details: str = "Detailed statistics on providers"
