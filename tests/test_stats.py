from httpx import AsyncClient

from conftest import AuthData

"""Login test TOKEN"""


async def test_push_login(ac: AsyncClient):
    login = await ac.post("/auth/login",
                          data={"username": AuthData.login, "password": AuthData.password})

    ac.headers['Authorization'] = f"Bearer {login.json()['access_token']}"
    assert login.status_code == 200


"""/stats query Test cases"""


async def test_get_stats(ac: AsyncClient):
    response = await ac.get("/stats")
    assert response.status_code == 422

    response = await ac.get("/stats",
                            params={"period_from": "2023-01-01",
                                    "period_to": "2023-02-01",
                                    "separate_by": "week"})
    assert response.status_code == 200


async def test_get_stats_providers(ac: AsyncClient):
    response = await ac.get("/stats/providers")
    assert response.status_code == 422

    response = await ac.get("/stats/providers",
                            params={"period_from": "2023-01-01", "period_to": "2023-02-01"})
    assert response.status_code == 200

    response = await ac.get("/stats/providers",
                            params={"period_from": "2023-01-01",
                                    "period_to": "2023-06-01",
                                    "page": 2, "limit": 25,
                                    "filter_by_platform": "telegram,facebook,youtube",
                                    "filter_by_branch": "culture,history,fashion",
                                    "sort_by": "contracts_purchased", "sort": "id"})
    assert response.status_code == 200


"""Logout test TOKEN"""


async def test_push_logout(ac: AsyncClient):
    logout = await ac.post("/auth/logout")

    ac.headers['Authorization'] = ""
    assert logout.status_code == 204
