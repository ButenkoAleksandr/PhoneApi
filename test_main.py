from httpx import Response

import pytest
from redis import Redis
from fastapi.testclient import TestClient

from main import app


client: TestClient = TestClient(app)
redis: Redis = Redis()


@pytest.fixture()
def clear_redis() -> None:
    redis.flushall()


def test_write_data(clear_redis) -> None:
    data: dict[str, str] = {"phone": "89090000000", "address": "адрес"}
    response: Response = client.post("/write_data", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data written successfully"}
    assert redis.get("89090000000").decode('utf-8') == "адрес"


def test_update_data(clear_redis) -> None:
    redis.set("89090000000", "адрес")
    data: dict[str, str] = {"phone": "89090000000", "address": "адрес"}
    response: Response = client.put("/update_data", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data updated successfully"}
    assert redis.get("89090000000").decode('utf-8') == "адрес"


def test_check_data(clear_redis) -> None:
    redis.set("89090000000", "адрес")
    response: Response = client.get("/check_data?phone=89090000000")
    assert response.status_code == 200
    assert response.json() == {"phone": "89090000000", "address": "адрес"}
