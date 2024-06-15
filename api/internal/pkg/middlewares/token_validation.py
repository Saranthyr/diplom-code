from collections.abc import Callable, Awaitable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from jose.exceptions import ExpiredSignatureError

from app.configuration.security import validate_access_token
from app.pkg.models.exceptions.jwt import ExpiredJWT, InvalidJWT


class TokenValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            if "Authorization" in request.headers:
                token_header = request.headers["Authorization"]
                if token_header.startswith("Bearer "):
                    token = token_header.split("Bearer ")[-1]
                    try:
                        valid_access = await validate_access_token(token=token)
                    except ExpiredSignatureError:
                        raise ExpiredJWT
                elif token_header.startswith("Basic "):
                    pass
                else:
                    raise InvalidJWT
            return await call_next(request)
        except ExpiredJWT or InvalidJWT as exc:
            return JSONResponse(
                content={"message": exc.message}, status_code=exc.status_code
            )
