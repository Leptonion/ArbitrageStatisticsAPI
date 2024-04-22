import datetime

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from clients.schemas import Clients
from clients.schemas import Client as SchemClient
from clients.utils import db_get_clients_list
from database import get_async_session, User
from models import Client

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.get("", response_model=Clients,
            description="Get paginated list of all Clients",
            name="List of Clients")
@cache(expire=60)
async def get_clients_list(limit: int = Query(le=100, ge=1, default=15),
                           page: int = Query(ge=1, default=1),
                           sort: str = Query(default="-id",
                                             description='**ASC** - `id`'
                                                         '<br><br>'
                                                         '**DESC** - `-id`'
                                                         '<br><br>',
                                             max_length=3),
                           period_from: datetime.date = Query(default=None,
                                                              description="**YYYY-mm-dd** - "
                                                                          "like `2023-01-01`"),
                           period_to: datetime.date = Query(default=None,
                                                            description="**YYYY-mm-dd** - "
                                                                        "like `2023-01-01`"),
                           filter_by_source: str = Query(default=None,
                                                         description="Can use multiple filtering - "
                                                                     "separated by"
                                                                     "`,` - like `manager,site`."
                                                                     "<br><br>"
                                                                     "Valid associations - "
                                                                     "`manager` `site` `invitation` "
                                                                     "`promotion` `office`"
                                                                     "<br><br>"),
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):

    count, client_list = await db_get_clients_list(limit, page, sort, period_from, period_to,
                                                   filter_by_source, session)

    return {
        "status": "success",
        "total": count,
        "current_page": page,
        "per_page": limit,
        "data": client_list,
        "details": "List of clients"
    }


@router.get("/{client_id}", response_model=SchemClient,
            description="Client details by client ID", name="Client by ID")
@cache(expire=60)
async def get_client_by_id(client_id: int, session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):

    query = select(Client).where(Client.id == client_id)
    result = await session.execute(query)

    return {"status": "success",
            "data": result.scalars().first(),
            "details": "Client information by ID"}
