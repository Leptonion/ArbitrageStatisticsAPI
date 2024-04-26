from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, func, and_, text
from sqlalchemy.ext.asyncio import AsyncSession

from models import Contract, Deal, Agent


async def db_get_agents_list(limit: int, page: int, sort: str, filter_by_position: str, session: AsyncSession):

    query = select(Agent)
    query = query.order_by(Agent.id.asc()) if sort == "id" else query.order_by(Agent.id.desc())
    query = query.where(Agent.position.in_(filter_by_position.split(","))) if filter_by_position else query
    count = select(func.count(query.c.id))
    query = query.limit(limit).offset(limit * (page - 1))
    agent_list = await session.execute(query)
    count = await session.execute(count)

    return count.scalars().one(), agent_list.scalars().all()


async def db_agent_achievement(agent_id: int,
                               period_from: datetime.date,
                               period_to: datetime.date,
                               session: AsyncSession):
    if period_from >= period_to:
        raise HTTPException(status_code=422, detail="Invalid date range - (period_from - period_to)!")

    contracts = select(func.count(Contract.id).label("contract_count"),
                       func.sum(Contract.price_per_day * Contract.duration_days).label("contract_sum")) \
        .where(Contract.agent_id == agent_id) \
        .where(and_(Contract.start_date >= period_from,
                    Contract.start_date < period_to)) \
        .subquery()

    purchases = select(func.count(Deal.id).label("purchase_count"),
                       func.sum(Deal.full_price).label("purchase_sum")) \
        .where(Deal.agent_id == agent_id) \
        .where(and_(Deal.start_date >= period_from,
                    Deal.start_date < period_to)) \
        .subquery()

    agent = select(Agent, contracts.alias("contracts"), purchases.alias("purchases")) \
        .where(Agent.id == agent_id)

    res = await session.execute(agent)
    res = res.first()

    if not res:
        raise HTTPException(status_code=404, detail="Agent not found!")

    return {
        "agent": res.Agent,
        "from_date": period_from,
        "to_date": period_to,
        "contracts_purchased": res.contract_count,
        "contract_expenses": round(float(res.contract_sum), 2),
        "offers_sold": res.purchase_count,
        "earned_from_offers": round(float(res.purchase_sum), 2)
    }
