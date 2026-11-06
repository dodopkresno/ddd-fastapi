from collections.abc import Iterator
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from ddd_fastapi.core.config import Settings
from ddd_fastapi.main import create_app
from ddd_fastapi.modules.items.presentation.router import get_service


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(create_app(Settings(environment="test"))) as client:
        yield client


def test_crud(client: TestClient) -> None:
    created = client.post("/api/v1/items", json={"name": " first "})
    assert created.status_code == 201
    item = created.json()
    url = created.headers["location"]
    assert client.get(url).json() == item
    assert client.get("/api/v1/items").json() == [item]
    assert client.put(url, json={"name": "updated"}).json()["name"] == "updated"
    assert client.delete(url).status_code == 204
    assert client.get(url).status_code == 404
    assert client.get("/api/v1/items").json() == []


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_items(client: TestClient, method: str) -> None:
    response = client.request(method, f"/api/v1/items/{UUID(int=1)}", json={"name": "ok"})
    assert response.status_code == 404
    assert response.json()["code"] == "item_not_found"


@pytest.mark.parametrize("body", [{}, {"name": " "}, {"name": "x" * 201}])
def test_validation(client: TestClient, body: dict[str, str]) -> None:
    response = client.post("/api/v1/items", json=body)
    assert response.status_code == 422
    assert set(response.json()) == {"code", "message", "request_id"}


def test_bad_path_and_pagination(client: TestClient) -> None:
    assert client.get("/api/v1/items/nope").status_code == 422
    assert client.get("/api/v1/items?limit=101").status_code == 422


def test_ids_and_unknown_route(client: TestClient) -> None:
    request_id = str(UUID(int=7))
    response = client.get("/missing", headers={"X-Request-ID": request_id})
    assert response.status_code == 404
    assert response.headers["x-request-id"] == response.json()["request_id"] == request_id
    generated = client.get("/health/live", headers={"X-Request-ID": "untrusted"})
    assert str(UUID(generated.headers["x-request-id"])) == generated.headers["x-request-id"]


def test_isolation(client: TestClient) -> None:
    client.post("/api/v1/items", json={"name": "only first app"})
    with TestClient(create_app(Settings())) as other:
        assert other.get("/api/v1/items").json() == []
    assert len(client.get("/api/v1/items").json()) == 1


def test_unexpected_error() -> None:
    app = create_app(Settings())

    def fail() -> None:
        raise RuntimeError("private secret")

    app.dependency_overrides[get_service] = fail
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/items")
        assert response.status_code == 500
        assert "private secret" not in response.text
        assert response.headers["x-request-id"] == response.json()["request_id"]


def test_cors() -> None:
    app = create_app(Settings(cors_origins=["https://example.com"]))
    with TestClient(app) as client:
        allowed = client.options(
            "/api/v1/items",
            headers={"Origin": "https://example.com", "Access-Control-Request-Method": "POST"},
        )
        assert allowed.headers["access-control-allow-origin"] == "https://example.com"
        denied = client.options(
            "/api/v1/items",
            headers={"Origin": "https://unknown.example", "Access-Control-Request-Method": "POST"},
        )
        assert denied.status_code == 400
