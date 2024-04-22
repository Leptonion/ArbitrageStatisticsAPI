import datetime
from itertools import pairwise

from dateutil import rrule
from sqlalchemy import select, func, and_, text
from sqlalchemy.ext.asyncio import AsyncSession

from models import Contract, Deal, Payment, Provider


async def sub_contracts_sums(period_from: datetime.date,
                             period_to: datetime.date):
    totals = select(func.count(Contract.id).label("contract_count"),
                    func.sum(Contract.price_per_day * Contract.duration_days).label("contract_sum")) \
        .where(and_(Contract.start_date >= period_from,
                    Contract.start_date < period_to)) \
        .subquery()

    id_list = select(Contract.id).where(and_(Contract.start_date >= period_from,
                                             Contract.start_date < period_to)).scalar_subquery()

    return id_list, totals


async def sub_deals_sums(period_from: datetime.date,
                         period_to: datetime.date):
    totals = select(func.count(Deal.id).label("purchase_count"),
                    func.sum(Deal.full_price).label("purchase_sum")) \
        .where(and_(Deal.start_date >= period_from,
                    Deal.start_date < period_to)) \
        .subquery()

    id_list = select(Deal.id).where(and_(Deal.start_date >= period_from,
                                         Deal.start_date < period_to)).scalar_subquery()

    return id_list, totals


async def date_range_per_week(start_date: datetime.date, end_date: datetime.date):
    if start_date.weekday() != 0:
        yield start_date
        start_date += datetime.timedelta(days=7 - start_date.weekday())

    while start_date < end_date:
        yield start_date
        start_date += datetime.timedelta(days=7)

    yield end_date


async def get_separated_graph(period_from: datetime.date,
                              period_to: datetime.date,
                              full_total,
                              separate_by: str,
                              session: AsyncSession):

    if separate_by == "week":
        date_range = [date async for date in date_range_per_week(period_from, period_to)]
    elif separate_by == "year":
        date_range = [date.date() for date in rrule.rrule(rrule.YEARLY, dtstart=period_from, until=period_to, byyearday=1)]
        if period_from != date_range[0]:
            date_range.insert(0, period_from)
        if period_to != date_range[-1]:
            date_range.append(period_to)
    else:
        date_range = [date.date() for date in rrule.rrule(rrule.MONTHLY, bymonthday=1, dtstart=period_from, until=period_to)]
        if period_from != date_range[0]:
            date_range.insert(0, period_from)
        if period_to != date_range[-1]:
            date_range.append(period_to)

    result = []

    for dt_range in pairwise(date_range):
        sub_cntrc_idlist, sub_cntrc_totals = await sub_contracts_sums(dt_range[0], dt_range[1])
        sub_deal_idlist, sub_deal_totals = await sub_deals_sums(dt_range[0], dt_range[1])
        sub_payments_totals = select(func.sum(Payment.pay_value).label("payments_sum")) \
            .where(and_(Payment.deal_id.in_(sub_deal_idlist),
                        Payment.create_date >= dt_range[0],
                        Payment.create_date < dt_range[1])).subquery()

        total = select(sub_cntrc_totals, sub_deal_totals, sub_payments_totals)
        total = await session.execute(total)
        total = total.first()

        if total.contract_count or total.purchase_count:
            result.append(
                {"from_date": dt_range[0],
                 "to_date": dt_range[1],
                 "contracts_purchased": total.contract_count,
                 "contract_expenses": total.contract_sum,
                 "offers_sold": total.purchase_count,
                 "earned_from_offers": total.purchase_sum,
                 "paid_offers": total.payments_sum,
                 "contracts_purchased_by_previous": total.contract_count - result[-1]['contracts_purchased'] if result else total.contract_count,
                 "contract_expenses_by_previous": total.contract_sum - result[-1]['contract_expenses'] if result else total.contract_sum,
                 "offers_sold_by_previous": total.purchase_count - result[-1]['offers_sold'] if result else total.purchase_count,
                 "earned_from_offers_by_previous": total.purchase_sum - result[-1]['earned_from_offers'] if result else total.purchase_sum,
                 "paid_offers_by_previous": total.payments_sum - result[-1]['paid_offers'] if result else total.payments_sum,
                 "contracts_purchased_percent": round((total.contract_count / full_total.contract_count) * 100, 2),
                 "contract_expenses_percent": round((total.contract_sum / full_total.contract_sum) * 100, 2),
                 "offers_sold_percent": round((total.purchase_count / full_total.purchase_count) * 100, 2),
                 "earned_from_offers_percent": round((total.purchase_sum / full_total.purchase_sum) * 100, 2),
                 "paid_offers_percent": round((total.payments_sum / full_total.payments_sum) * 100, 2)}
            )

    return result


async def get_stats_by_providers(limit: int, page: int, period_from, period_to,
                                 filter_by_platform: str, filter_by_branch: str,
                                 sort_by: str, sort: str, session: AsyncSession):
    sort_types = {"-id": "DESC", "id": "ASC"}
    sort_dict = {"contracts_purchased": "contracts_count",
                 "total_duration_days": "days_purchased",
                 "max_contract_duration_days": "max_days_duration",
                 "min_contract_duration_days": "min_days_duration",
                 "total_spent": "sum_expense",
                 "max_cost_per_day": "max_expense_per_day",
                 "min_cost_per_day": "min_expense_per_day",
                 "total_deals_sold": "deals_count",
                 "total_income_from_deals": "deals_sum",
                 "platform": "platform",
                 "branch": "branch",
                 "id": "id"}

    if sort not in sort_types.keys():
        sort = "-id"

    if sort_by not in sort_dict.keys():
        sort_by = "id"

    deals_sub = select(Contract.provider_id,
                       func.count(Deal.id).label("deals_count"),
                       func.sum(Deal.full_price).label("deals_sum")).join(Deal)\
        .group_by(Contract.id).where(and_(Deal.start_date >= period_from,
                                          Deal.start_date < period_to))\
        .subquery()

    deals_stat = select(deals_sub.c.provider_id,
                        func.sum(deals_sub.c.deals_count).label("deals_count"),
                        func.sum(deals_sub.c.deals_sum).label("deals_sum"))\
        .group_by(deals_sub.c.provider_id).subquery()

    contracts_stat = select(Provider,
                            func.count(Contract.id).label("contracts_count"),
                            func.sum(Contract.duration_days).label("days_purchased"),
                            func.max(Contract.duration_days).label("max_days_duration"),
                            func.min(Contract.duration_days).label("min_days_duration"),
                            func.sum(Contract.price_per_day * Contract.duration_days).label("sum_expense"),
                            func.max(Contract.price_per_day).label("max_expense_per_day"),
                            func.min(Contract.price_per_day).label("min_expense_per_day")
                            ) \
        .join(Provider) \
        .group_by(Contract.provider_id, Provider.id) \
        .where(and_(Contract.start_date >= period_from,
                    Contract.start_date < period_to)) \
        .subquery()

    query = select(contracts_stat, deals_stat).where(contracts_stat.c.id == deals_stat.c.provider_id)
    query = query.where(contracts_stat.c.platform.in_(filter_by_platform.split(","))) if filter_by_platform else query
    query = query.where(contracts_stat.c.branch.in_(filter_by_branch.split(","))) if filter_by_branch else query
    query = query.order_by(text(f'{sort_dict[sort_by]} {sort_types[sort]}'))
    count = select(func.count(query.c.id))
    query = query.limit(limit).offset(limit * (page - 1))

    res = await session.execute(query)
    count = await session.execute(count)
    return {"status": "success",
            "total": count.scalar(),
            "current_page": page,
            "per_page": limit,
            "from_date": period_from,
            "to_date": period_to,
            "sorted_by": sort_by,
            "data": [{
                    "provider": {"id": row.id,
                                 "title": row.title,
                                 "platform": row.platform,
                                 "branch": row.branch,
                                 "site": row.site,
                                 "contact": row.contact},
                    "statistic": {"contracts_purchased": row.contracts_count,
                                  "total_duration_days": row.days_purchased,
                                  "max_contract_duration_days": row.max_days_duration,
                                  "min_contract_duration_days": row.min_days_duration,
                                  "total_spent": float(row.sum_expense),
                                  "max_cost_per_day": float(row.max_expense_per_day),
                                  "min_cost_per_day": float(row.min_expense_per_day),
                                  "total_deals_sold": float(row.deals_count),
                                  "total_income_from_deals": float(row.deals_sum)}
                } for row in res.all()],
            "details": "Detailed statistics on providers"}
