from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .MovieNotFoundException import MovieNotFoundException


def register_exception_handlers(app: FastAPI):
    """Adds all exceptions handlers to FastAPI app given including custom exceptions."""


    @app.exception_handler(RequestValidationError)
    async def validation_exception(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422, content={"error": "The HTTP request given is formatted incorrectly or provides incorrect data and could not be read.", "detail": str(exc)})
    

    @app.exception_handler(MovieNotFoundException)
    async def movie_not_found_exception(request: Request, exc: MovieNotFoundException):
        return JSONResponse(status_code=exc.exit_code, content=exc.message)


    @app.exception_handler(Exception)
    async def general_error(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"error": f"Unhandled exception occurred.", "detail": str(exc)})
