import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Deal


async def db_get_deals_list(limit: int, page: int, sort: str,
                            period_from: datetime.date, period_to: datetime.date,
                            filter_by_client: int, filter_by_agent: int,
                            filter_by_contract: int, session: AsyncSession):

    query = select(Deal)
    query = query.order_by(Deal.id.asc()) if sort == "id" else query.order_by(Deal.id.desc())
    query = query.where(Deal.start_date >= period_from) if period_from else query
    query = query.where(Deal.start_date < period_to) if period_to else query
    query = query.where(Deal.client_id == filter_by_client) if filter_by_client else query
    query = query.where(Deal.agent_id == filter_by_agent) if filter_by_agent else query
    query = query.where(Deal.contract_id == filter_by_contract) if filter_by_contract else query
    count = select(func.count(query.c.id))
    query = query.limit(limit).offset(limit * (page - 1))
    query = query.options(selectinload(Deal.payments))

    purchase_list = await session.execute(query)
    count = await session.execute(count)

    return count.scalars().one(), purchase_list.scalars().all()
