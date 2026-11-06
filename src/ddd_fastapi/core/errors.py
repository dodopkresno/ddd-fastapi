import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from ..modules.items.domain.models import ItemNotFoundError, ItemValidationError
from .logging import request_id_context


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str


def error_response(request: Request, status: int, code: str, message: str) -> JSONResponse:
    request_id = str(getattr(request.state, "request_id", ""))
    return JSONResponse(
        status_code=status,
        content=ErrorResponse(code=code, message=message, request_id=request_id).model_dump(),
        headers={"X-Request-ID": request_id},
    )


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(ItemNotFoundError)
    async def not_found(request: Request, exc: ItemNotFoundError) -> JSONResponse:
        return error_response(request, 404, "item_not_found", str(exc))

    @app.exception_handler(ItemValidationError)
    async def domain_validation(request: Request, exc: ItemValidationError) -> JSONResponse:
        return error_response(request, 422, "domain_validation", str(exc))

    @app.exception_handler(RequestValidationError)
    async def validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        return error_response(request, 422, "validation_error", "Request validation failed")

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
        response = error_response(request, exc.status_code, "http_error", str(exc.detail))
        if exc.headers:
            response.headers.update(exc.headers)
        return response

    @app.exception_handler(Exception)
    async def unexpected(request: Request, exc: Exception) -> JSONResponse:
        token = request_id_context.set(str(getattr(request.state, "request_id", "")))
        try:
            logging.getLogger("ddd_fastapi").error("Unhandled error", exc_info=exc)
            return error_response(request, 500, "internal_error", "An unexpected error occurred")
        finally:
            request_id_context.reset(token)
