from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppException,
    ResourceNotFoundException,
    ValidationException,
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """

    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(
        request: Request,
        exc: ResourceNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(ValidationException)
    async def validation_handler(
        request: Request,
        exc: ValidationException,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.message,
            },
        )