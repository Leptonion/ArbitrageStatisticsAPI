import datetime

from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from database import get_async_session, User
from models import Payment
from stats.schemas import Stats, ProviderStats
from stats.utils import sub_contracts_sums, sub_deals_sums, get_separated_graph, get_stats_by_providers

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)


@router.get("/", response_model=Stats,
            description="The route allows you to obtain statistics on purchases and sales. "
                        "Enables subperiod separation for the graph (use - `separate_by`)",
            name="Getting Income/Expenses statistic")
@cache(expire=600)
async def full_profitability(period_from: datetime.date = Query(description="**YYYY-mm-dd** - like `2023-01-01`"),
                             period_to: datetime.date = Query(description="**YYYY-mm-dd** - like `2023-01-01`"),
                             separate_by: str = Query(default="month",
                                                      description="Valid associations - `week`|`month`|`year`"),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):

    sub_cntrc_idlist, sub_cntrc_totals = await sub_contracts_sums(period_from, period_to)
    sub_deal_idlist, sub_deal_totals = await sub_deals_sums(period_from, period_to)
    sub_payments_totals = select(func.sum(Payment.pay_value).label("payments_sum"))\
        .where(and_(Payment.deal_id.in_(sub_deal_idlist),
                    Payment.create_date >= period_from,
                    Payment.create_date < period_to)).subquery()

    total = select(sub_cntrc_totals, sub_deal_totals, sub_payments_totals)
    total = await session.execute(total)
    total = total.first()

    graph = await get_separated_graph(period_from, period_to, total, separate_by, session)

    return {"status": "success",
            "from_date": period_from,
            "to_date": period_to,
            "data": {"contracts_purchased": total.contract_count,
                     "contract_expenses": total.contract_sum,
                     "offers_sold": total.purchase_count,
                     "earned_from_offers": total.purchase_sum,
                     "paid_offers": total.payments_sum},
            "graph": {"separation_by": separate_by,
                      "data": graph},
            "details": "Full income/expense statistics by period"}


@router.get("/providers", response_model=ProviderStats,
            description="The route allows you to get full statistics on providers. "
                        "Quantity, Expense, Income - for a certain time",
            name="Full statistic by Providers")
@cache(expire=600)
async def profitability_providers(limit: int = Query(le=100, ge=1, default=15),
                                  page: int = Query(ge=1, default=1),
                                  period_from: datetime.date = Query(description="**YYYY-mm-dd** - like `2023-01-01`"),
                                  period_to: datetime.date = Query(description="**YYYY-mm-dd** - like `2023-01-01`"),
                                  filter_by_platform: str = Query(default=None,
                                                                  description="Can use multiple filtering - "
                                                                              "separated by"
                                                                              "**,** - like `telegram,facebook`."
                                                                              "<br><br>"
                                                                              "Valid associations - "
                                                                              "`telegram` `facebook` "
                                                                              "`youtube` `tik-tok` `twitter`"
                                                                              "<br><br>"),
                                  filter_by_branch: str = Query(default=None,
                                                                description="Can use multiple filtering - "
                                                                            "separated by"
                                                                            "`,` - like `culture,history`."
                                                                            "<br><br>"
                                                                            "Valid associations - "
                                                                            "`entertainment` `science` "
                                                                            "`culture` `history` `fashion`"
                                                                            "<br><br>"),
                                  sort_by: str = Query(default="id",
                                                       description="Valid associations - "
                                                                   "`contracts_purchased`|`total_duration_days`|"
                                                                   "`max_contract_duration_days`|"
                                                                   "`min_contract_duration_days`|"
                                                                   "`total_spent`"
                                                                   "<br><br>"
                                                                   "`max_cost_per_day`|"
                                                                   "`min_cost_per_day`|`total_deals_sold`|"
                                                                   "`total_income_from_deals`|"
                                                                   "`platform`|`branch`|`id`"
                                                                   "<br><br>"),
                                  sort: str = Query(default="-id",
                                                    description='**ASC** - `id`'
                                                                '<br><br>'
                                                                '**DESC** - `-id`'
                                                                '<br><br>',
                                                    max_length=3),
                                  session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_user)):

    res = await get_stats_by_providers(limit, page, period_from, period_to, filter_by_platform, filter_by_branch,
                                       sort_by, sort, session)
    return res
