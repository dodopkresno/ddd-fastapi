from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import Settings
from .core.errors import ErrorResponse, register_handlers
from .core.logging import configure_logging
from .core.middleware import RequestIdMiddleware
from .modules.health.checks import ReadinessCheck
from .modules.health.presentation.router import router as health_router
from .modules.items.infrastructure.repository import InMemoryItemRepository
from .modules.items.presentation.router import router as items_router


def create_app(
    settings: Settings | None = None,
    *,
    readiness_checks: tuple[ReadinessCheck, ...] = (),
) -> FastAPI:
    config = settings if settings is not None else Settings()
    configure_logging(config.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.item_repository = InMemoryItemRepository()
        app.state.readiness_checks = readiness_checks
        try:
            yield
        finally:
            del app.state.item_repository
            del app.state.readiness_checks

    development = config.environment == "development"
    app = FastAPI(
        title="DDD FastAPI Starter",
        lifespan=lifespan,
        docs_url="/docs" if development else None,
        redoc_url=None,
        openapi_url="/openapi.json" if development else None,
        responses={code: {"model": ErrorResponse} for code in (404, 422, 500)},
    )
    app.state.settings = config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "X-Request-ID"],
        expose_headers=["X-Request-ID", "Location"],
    )
    app.add_middleware(RequestIdMiddleware)
    register_handlers(app)
    app.include_router(health_router)
    app.include_router(items_router)
    return app
