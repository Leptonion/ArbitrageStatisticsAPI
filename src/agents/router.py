import datetime

from fastapi import APIRouter, Depends, Query, Path
from fastapi_cache.decorator import cache
from sqlalchemy import select, func

from sqlalchemy.ext.asyncio import AsyncSession

from agents.schemas import Agents, Achievement
from agents.schemas import Agent as SchemAgent
from agents.utils import db_agent_achievement, db_get_agents_list
from auth.base_config import current_user
from database import get_async_session, User

from models import Agent

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


@router.get("", response_model=Agents,
            description="Get paginated list of all Agents",
            name="List of Agents")
@cache(expire=60)
async def get_agents_list(limit: int = Query(le=100, ge=1, default=15),
                          page: int = Query(ge=1, default=1),
                          sort: str = Query(default="-id",
                                            description='**ASC** - `id`'
                                                        '<br><br>'
                                                        '**DESC** - `-id`'
                                                        '<br><br>',
                                            max_length=3),
                          filter_by_position: str = Query(default=None,
                                                          description="Can use multiple filtering - "
                                                                      "separated by"
                                                                      "`,` - like `manager,top-manager`."
                                                                      "<br><br>"
                                                                      "Valid associations - "
                                                                      "`manager` `top-manager` `junior manager`"
                                                                      "<br><br>"),
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):

    count, agent_list = await db_get_agents_list(limit, page, sort, filter_by_position, session)

    return {
        "status": "success",
        "total": count,
        "current_page": page,
        "per_page": limit,
        "data": agent_list,
        "details": "List of agents"
    }


@router.get("/{agent_id}", response_model=SchemAgent,
            description="Agent details by agent ID", name="Agent by ID")
@cache(expire=60)
async def get_agent_by_id(agent_id: int,
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):

    query = select(Agent).where(Agent.id == agent_id)
    result = await session.execute(query)

    return {"status": "success",
            "data": result.scalars().first(),
            "details": "Agent information by ID"}


@router.get("/{agent_id}/achievement", response_model=Achievement,
            description="Agent's personal statistics. Contracts, transactions, profitability and expenses.",
            name="Agent's personal statistics")
@cache(expire=600)
async def get_agent_achievement(agent_id: int,
                                period_from: datetime.date = Query(description="**YYYY-mm-dd** - like `2023-01-01`"),
                                period_to: datetime.date = Query(description="**YYYY-mm-dd** - like `2023-01-01`"),
                                session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_user)):

    res = await db_agent_achievement(agent_id, period_from, period_to, session)

    return res
