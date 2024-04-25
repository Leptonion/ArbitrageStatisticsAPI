import datetime

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.base_config import current_user
from database import get_async_session, User
from deals.utils import db_get_deals_list
from models import Deal
from deals.schemas import Deals, DealError
from deals.schemas import Deal as SchemDeal

router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)


@router.get("", response_model=Deals,
            description="Get a paginated list of all completed Deals",
            name="List of Deals")
async def get_deals_list(limit: int = Query(le=100, ge=1, default=15),
                         page: int = Query(ge=1, default=1),
                         sort: str = Query(default="-id",
                                           description='**ASC** - `id`'
                                                       '<br><br>'
                                                       '**DESC** - `-id`'
                                                       '<br><br>',
                                           max_length=3),
                         period_from: datetime.date = Query(default=None, description="**YYYY-mm-dd** - "
                                                                                      "like `2023-01-01`"),
                         period_to: datetime.date = Query(default=None, description="**YYYY-mm-dd** - "
                                                                                    "like `2023-01-01`"),
                         filter_by_client: int = Query(default=None,
                                                       description="Filter by Client_Id - `client_id`"),
                         filter_by_agent: int = Query(default=None,
                                                      description="Filter by Agent_Id - `agent_id`"),
                         filter_by_contract: int = Query(default=None,
                                                         description="Filter by Contract_Id - `contract_id`"),
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):

    count, purchase_list = await db_get_deals_list(limit, page, sort, period_from, period_to, filter_by_client,
                                                   filter_by_agent, filter_by_contract, session)

    return {
        "status": "success",
        "total": count,
        "current_page": page,
        "per_page": limit,
        "data": purchase_list,
        "details": "List of deals"
    }


@router.get("/{deal_id}", response_model=SchemDeal,
            responses={404: {"model": DealError, "description": "Deal not found"}},
            description="Deal details by deal ID", name="Deal by ID")
async def get_deal_by_id(deal_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):

    query = select(Deal).where(Deal.id == deal_id).options(selectinload(Deal.payments))
    result = await session.execute(query)
    result = result.scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail="Deal not found!")

    return {"status": "success",
            "data": result,
            "details": "Deal details by ID"}
