import pytest
from httpx import AsyncClient


async def test_get_agents_list(ac: AsyncClient):
    response = await ac.post("/agents/", params={"sort": "-id"})

    assert response.status_code == 307
