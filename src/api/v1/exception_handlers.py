from http import HTTPStatus

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.base.exceptions import ObjectNotFoundError


class ErrorContentSchema(BaseModel):
    message: str


async def pydantic_validation_exception_handler(
    _request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        content=ErrorContentSchema(message=str(exception.errors())).model_dump(),
    )


async def object_not_found_error(
    _request: Request,
    exception: ObjectNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=ErrorContentSchema(message=exception.public_message).model_dump(),
    )


async def exception_error(
    _request: Request,
    _exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=ErrorContentSchema(message="Something went wrong").model_dump(),
    )


def build_exceptions() -> dict:
    return {
        RequestValidationError: pydantic_validation_exception_handler,
        ObjectNotFoundError: object_not_found_error,
        Exception: exception_error,
    }


def build_exception_responses() -> dict:
    return {
        HTTPStatus.UNPROCESSABLE_CONTENT.value: {
            "model": ErrorContentSchema,
            "description": "Unprocessable content",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": ErrorContentSchema,
            "description": "Internal error",
        },
        HTTPStatus.BAD_GATEWAY.value: {
            "model": ErrorContentSchema,
            "description": "External service unavailable",
        },
        HTTPStatus.NOT_FOUND.value: {
            "model": ErrorContentSchema,
            "description": "Object not found",
        },
    }
