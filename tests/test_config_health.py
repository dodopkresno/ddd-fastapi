import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from ddd_fastapi.core.config import Settings
from ddd_fastapi.main import create_app


def test_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENVIRONMENT", "production")
    settings = Settings()
    assert settings.environment == "production"
    with TestClient(create_app(settings)) as client:
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
    monkeypatch.setenv("APP_ENVIRONMENT", "invalid")
    with pytest.raises(ValidationError):
        Settings()


def test_restrictive_cors() -> None:
    assert Settings().cors_origins == []
    with pytest.raises(ValidationError):
        Settings(cors_origins=["*"])


def test_health_no_dependencies() -> None:
    with TestClient(create_app(Settings())) as client:
        assert client.get("/health/live").json() == {"status": "ok"}
        assert client.get("/health/ready").json() == {"status": "ready"}
        assert client.get("/openapi.json").status_code == 200


@pytest.mark.parametrize("result", [True, False, None])
def test_configured_readiness(result: bool | None) -> None:
    calls: list[bool] = []

    async def check() -> bool:
        calls.append(True)
        if result is None:
            raise RuntimeError("private dependency details")
        return result

    with TestClient(create_app(Settings(), readiness_checks=(check,))) as client:
        assert client.get("/health/live").status_code == 200
        assert calls == []
        response = client.get("/health/ready")
        assert response.status_code == (200 if result else 503)
        assert "private" not in response.text
        assert calls == [True]
