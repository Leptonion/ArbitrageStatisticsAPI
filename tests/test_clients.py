from httpx import AsyncClient

from conftest import AuthData

"""Login test TOKEN"""


async def test_push_login(ac: AsyncClient):
    login = await ac.post("/auth/login",
                          data={"username": AuthData.login, "password": AuthData.password})

    ac.headers['Authorization'] = f"Bearer {login.json()['access_token']}"
    assert login.status_code == 200


"""/agents query Test cases"""


async def test_get_clients_list(ac: AsyncClient):
    response = await ac.get("/clients",
                            params={"sort": "-id"})
    assert response.status_code == 200

    response = await ac.get("/clients",
                            params={"sort": "id", "limit": 25, "page": 2,
                                    "filter_by_source": "manager,site"})
    assert response.status_code == 200

    response = await ac.get("/clients",
                            params={"period_from": "2023-01-05", "period_to": "2023-02-01"})
    assert response.status_code == 200

    response = await ac.get("/clients")
    assert response.status_code == 200

    response = await ac.get("/clients",
                            params={"period_from": "2023-01-05", "period_to": "2023-01-01"})
    assert response.status_code == 200


async def test_get_client(ac: AsyncClient):
    response = await ac.get("/clients/9")
    assert response.status_code == 200

    response = await ac.get("/clients/12931293")
    assert response.status_code == 404


"""Logout test TOKEN"""


async def test_push_logout(ac: AsyncClient):
    logout = await ac.post("/auth/logout")

    ac.headers['Authorization'] = ""
    assert logout.status_code == 204
