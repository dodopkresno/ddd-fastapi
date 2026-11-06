from typing import cast

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from ..checks import ReadinessCheck

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(request: Request) -> JSONResponse:
    checks = cast(tuple[ReadinessCheck, ...], request.app.state.readiness_checks)
    for check in checks:
        try:
            if not await check():
                return JSONResponse({"status": "not_ready"}, status_code=503)
        except Exception:
            return JSONResponse({"status": "not_ready"}, status_code=503)
    return JSONResponse({"status": "ready"})
