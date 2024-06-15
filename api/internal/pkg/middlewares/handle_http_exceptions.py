from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.pkg.models.base.exception import BaseAPIException


class HTTPExceptionHandler(BaseHTTPMiddleware):
    """Класс промежуточного ПО для обработки ошибок"""

    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Обработчик запроса"""
        try:
            response = await call_next(request)
            return response
        except BaseAPIException as exc:
            """В случае возникновения ошибки, на пользовательскую часть возвращается ответ, содержащий код ошибки и сообщение о ней"""
            return JSONResponse(
                status_code=exc.status_code, content={"message": exc.message}
            )
