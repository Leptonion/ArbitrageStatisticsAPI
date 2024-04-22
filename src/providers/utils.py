from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Provider


async def db_get_providers_list(limit: int, page: int, sort: str, filter_by_platform: str,
                                filter_by_branch: str, session: AsyncSession):

    query = select(Provider)
    query = query.order_by(Provider.id.asc()) if sort == "id" else query.order_by(Provider.id.desc())
    query = query.where(Provider.platform.in_(filter_by_platform.split(","))) if filter_by_platform else query
    query = query.where(Provider.branch.in_(filter_by_branch.split(","))) if filter_by_branch else query
    count = select(func.count(query.c.id))
    query = query.limit(limit).offset(limit * (page - 1))
    sellers_list = await session.execute(query)
    count = await session.execute(count)

    return count.scalars().one(), sellers_list.scalars().all()
