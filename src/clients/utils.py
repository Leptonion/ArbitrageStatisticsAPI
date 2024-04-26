import datetime

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Client


async def db_get_clients_list(limit: int, page: int, sort: str, period_from: datetime.date,
                              period_to: datetime.date, filter_by_source: str, session: AsyncSession):

    query = select(Client)
    query = query.order_by(Client.id.asc()) if sort == "id" else query.order_by(Client.id.desc())
    query = query.where(Client.add_date >= period_from) if period_from else query
    query = query.where(Client.add_date < period_to) if period_to else query
    query = query.where(Client.from_source.in_(filter_by_source.split(","))) if filter_by_source else query
    count = select(func.count(query.c.id))
    query = query.limit(limit).offset(limit * (page - 1))
    client_list = await session.execute(query)
    count = await session.execute(count)

    return count.scalars().one(), client_list.scalars().all()
