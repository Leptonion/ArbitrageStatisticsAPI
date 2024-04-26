from httpx import AsyncClient

from tests.conftest import AuthData


"""Login test TOKEN"""


async def test_push_login(ac: AsyncClient):
    login = await ac.post("/auth/login",
                          data={"username": AuthData.login, "password": AuthData.password})

    ac.headers['Authorization'] = f"Bearer {login.json()['access_token']}"
    assert login.status_code == 200


"""/agents query Test cases"""


async def test_get_agents_list(ac: AsyncClient):
    response = await ac.get("/agents",
                            params={"sort": "-id"})
    assert response.status_code == 200

    response = await ac.get("/agents",
                            params={"sort": "id", "limit": 25, "page": 2,
                                    "filter_by_position": "manager,top-manager"})
    assert response.status_code == 200

    response = await ac.get("/agents")
    assert response.status_code == 200


async def test_get_agent(ac: AsyncClient):
    response = await ac.get("/agents/9")
    assert response.status_code == 200

    response = await ac.get("/agents/223")
    assert response.status_code == 404


async def test_agent_achievement(ac: AsyncClient):
    response = await ac.get("/agents/9/achievement")
    assert response.status_code == 422

    response = await ac.get("/agents/9/achievement",
                            params={"period_from": "2023-01-01", "period_to": "2023-02-01"})
    assert response.status_code == 200

    response = await ac.get("/agents/9/achievement",
                            params={"period_from": "2023-01-05", "period_to": "2023-01-01"})
    assert response.status_code == 422
    assert response.json()['detail'] == "Invalid date range - (period_from - period_to)!"

    response = await ac.get("/agents/223/achievement",
                            params={"period_from": "2023-01-01", "period_to": "2023-02-01"})
    assert response.status_code == 404
    assert response.json()['detail'] == "Agent not found!"


"""Logout test TOKEN"""


async def test_push_logout(ac: AsyncClient):
    logout = await ac.post("/auth/logout")

    ac.headers['Authorization'] = ""
    assert logout.status_code == 204
