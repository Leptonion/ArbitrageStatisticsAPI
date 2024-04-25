from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from database import get_async_session, User
from models import Provider
from providers.schemas import Providers, ProviderError
from providers.schemas import Provider as SchemProvider
from providers.utils import db_get_providers_list

router = APIRouter(
    prefix="/providers",
    tags=["Providers"],
)


@router.get("", response_model=Providers,
            description="Get paginated list of all Providers",
            name="List of Providers")
@cache(expire=60)
async def get_providers_list(limit: int = Query(le=100, ge=1, default=15),
                             page: int = Query(ge=1, default=1),
                             sort: str = Query(default="-id",
                                               description='**ASC** - `id`'
                                                           '<br><br>'
                                                           '**DESC** - `-id`'
                                                           '<br><br>',
                                               max_length=3),
                             filter_by_platform: str = Query(default=None,
                                                             description="Can use multiple filtering - "
                                                                         "separated by"
                                                                         "`,` - like `telegram,facebook`."
                                                                         "<br><br>"
                                                                         "Valid associations - "
                                                                         "`telegram` `facebook` `youtube` "
                                                                         "`tik-tok` `twitter`"
                                                                         "<br><br>"),
                             filter_by_branch: str = Query(default=None,
                                                           description="Can use multiple filtering - "
                                                                       "separated by"
                                                                       "`,` - like `science,culture`."
                                                                       "<br><br>"
                                                                       "Valid associations - "
                                                                       "`entertainment` `science` `culture` "
                                                                       "`history` `fashion`"
                                                                       "<br><br>"),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):

    count, sellers_list = await db_get_providers_list(limit, page, sort,
                                                      filter_by_platform,
                                                      filter_by_branch,
                                                      session)

    return {
        "status": "success",
        "total": count,
        "current_page": page,
        "per_page": limit,
        "data": sellers_list,
        "details": "List of providers"
    }


@router.get("/{provider_id}", response_model=SchemProvider,
            responses={404: {"model": ProviderError, "description": "Provider not found"}},
            description="Provider details by provider ID", name="Provider by ID")
@cache(expire=60)
async def get_provider_by_id(provider_id: int,
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):

    query = select(Provider).where(Provider.id == provider_id)
    result = await session.execute(query)
    result = result.scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail="Provider not found!")

    return {"status": "success",
            "data": result,
            "details": "Provider information by ID"}
