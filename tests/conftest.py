from collections.abc import Iterator

import pytest

from ddd_fastapi.core.config import Settings


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    # Do not let developer .env files or shell settings affect the test suite.
    for name in ("APP_ENVIRONMENT", "APP_CORS_ORIGINS", "APP_LOG_LEVEL"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setitem(Settings.model_config, "env_file", None)
    yield
