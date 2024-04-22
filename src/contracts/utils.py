import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Contract


async def db_get_contracts_list(limit: int, page: int, sort: str,
                                period_from: datetime.date, period_to: datetime.date,
                                filter_by_seller: int, filter_by_agent: int, session: AsyncSession):

    query = select(Contract)
    query = query.order_by(Contract.id.asc()) if sort == "id" else query.order_by(Contract.id.desc())
    query = query.where(Contract.start_date >= period_from) if period_from else query
    query = query.where(Contract.start_date < period_to) if period_to else query
    query = query.where(Contract.provider_id == filter_by_seller) if filter_by_seller else query
    query = query.where(Contract.agent_id == filter_by_agent) if filter_by_agent else query
    count = select(func.count(query.c.id))
    query = query.limit(limit).offset(limit * (page - 1))

    contract_list = await session.execute(query)
    count = await session.execute(count)

    return count.scalars().one(), contract_list.scalars().all()
