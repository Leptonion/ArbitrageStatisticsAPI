from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class ListingResponse(BaseModel):
    status: str = "success"
    total: int = 100
    current_page: int = 1
    per_page: int = 15
    data: list
    details: str


class RowResponse(BaseModel):
    status: str = "success"
    data: dict
    details: str


class ErrorResponse(BaseModel):
    status: str = "error"
    data: list | None
    details: str


class DBAgent(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int = 1
    full_name: str = "Antony Hatchet"
    position: str = "manager"
    start_date: datetime


class DBProvider(BaseModel):
    id: int = 1
    title: str = "John Doe Chanel"
    platform: str = "telegram"
    branch: str = "history"
    site: str = "some.site.com"
    contact: str = "+101234567"


class DBClient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = 1
    title: str = "John Doe ltd."
    add_date: datetime
    contact: str
    from_source: str = "site"


class DBPayment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = 1
    pay_value: float = 83.25
    create_date: datetime


class DBContract(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = 1
    title: str = "Contract-1111"
    price_per_day: float = 10.55
    start_date: datetime
    duration_days: int = 3
    doc_link: str = "somelink111.com"
    seller: DBProvider
    agent: DBAgent


class DBDeal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = 1
    full_price: float = 85.33
    start_date: datetime
    duration_days: int = 3
    client: DBClient
    agent: DBAgent
    contract: DBContract
    payments: List[DBPayment]
