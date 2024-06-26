from httpx import AsyncClient

from conftest import AuthData


"""Login test TOKEN"""


async def test_push_login(ac: AsyncClient):
    login = await ac.post("/auth/login",
                          data={"username": AuthData.login, "password": AuthData.password})

    ac.headers['Authorization'] = f"Bearer {login.json()['access_token']}"
    assert login.status_code == 200


"""/contracts query Test cases"""


async def test_get_contracts_list(ac: AsyncClient):
    response = await ac.get("/contracts",
                            params={"sort": "-id"})
    assert response.status_code == 200

    response = await ac.get("/contracts",
                            params={"sort": "id", "limit": 25, "page": 2,
                                    "period_from": "2023-01-01", "period_to": "2023-02-01"})
    assert response.status_code == 200

    response = await ac.get("/contracts")
    assert response.status_code == 200


async def test_get_contract(ac: AsyncClient):
    response = await ac.get("/contracts/9")
    assert response.status_code == 200

    response = await ac.get("/contracts/222223")
    assert response.status_code == 404


"""Logout test TOKEN"""


async def test_push_logout(ac: AsyncClient):
    logout = await ac.post("/auth/logout")

    ac.headers['Authorization'] = ""
    assert logout.status_code == 204
