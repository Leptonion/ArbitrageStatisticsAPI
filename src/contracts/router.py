import datetime

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from contracts.schemas import Contracts, ContractError
from contracts.schemas import Contract as SchemContract
from contracts.utils import db_get_contracts_list
from database import get_async_session, User
from models import Contract

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"]
)


@router.get("", response_model=Contracts,
            description="Get a paginated list of all signed Contracts",
            name="List of Contracts")
@cache(expire=60)
async def get_contracts_list(limit: int = Query(le=100, ge=1, default=15),
                             page: int = Query(ge=1, default=1),
                             sort: str = Query(default="-id",
                                               description='**ASC** - `id`'
                                                           '<br><br>'
                                                           '**DESC** - `-id`'
                                                           '<br><br>',
                                               max_length=3),
                             period_from: datetime.date = Query(default=None,
                                                                description="**YYYY-mm-dd** - like `2023-01-01`"),
                             period_to: datetime.date = Query(default=None,
                                                              description="**YYYY-mm-dd** - like `2023-01-01`"),
                             filter_by_provider: int = Query(default=None,
                                                             description="Filter by Provider_Id - `provider_id`"),
                             filter_by_agent: int = Query(default=None,
                                                          description="Filter by Agent_Id - `agent_id`"),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):

    count, contract_list = await db_get_contracts_list(limit, page, sort, period_from, period_to,
                                                       filter_by_provider, filter_by_agent, session)

    return {
        "status": "success",
        "total": count,
        "current_page": page,
        "per_page": limit,
        "data": contract_list,
        "details": "List of Contracts"
    }


@router.get("/{contract_id}", response_model=SchemContract,
            responses={404: {"model": ContractError, "description": "Contract not found"}},
            description="Contract details by contract ID", name="Contract by ID")
@cache(expire=60)
async def get_contract_by_id(contract_id: int, session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):

    query = select(Contract).where(Contract.id == contract_id)
    result = await session.execute(query)
    result = result.scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail="Contract not found!")

    return {"status": "success",
            "data": result,
            "details": "List of Contracts"}
