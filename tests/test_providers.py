from httpx import AsyncClient

from conftest import AuthData

"""Login test TOKEN"""


async def test_push_login(ac: AsyncClient):
    login = await ac.post("/auth/login",
                          data={"username": AuthData.login, "password": AuthData.password})

    ac.headers['Authorization'] = f"Bearer {login.json()['access_token']}"
    assert login.status_code == 200


"""/providers query Test cases"""


async def test_get_providers_list(ac: AsyncClient):
    response = await ac.get("/providers",
                            params={"sort": "-id"})
    assert response.status_code == 200

    response = await ac.get("/providers",
                            params={"sort": "id", "limit": 25, "page": 2,
                                    "filter_by_platform": "telegram,facebook",
                                    "filter_by_branch": "science,culture,fashion"})
    assert response.status_code == 200

    response = await ac.get("/providers")
    assert response.status_code == 200


async def test_get_provider(ac: AsyncClient):
    response = await ac.get("/providers/9")
    assert response.status_code == 200

    response = await ac.get("/providers/222223")
    assert response.status_code == 404


"""Logout test TOKEN"""


async def test_push_logout(ac: AsyncClient):
    logout = await ac.post("/auth/logout")

    ac.headers['Authorization'] = ""
    assert logout.status_code == 204
