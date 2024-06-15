from typing import Any, Dict, Optional, Union
from typing_extensions import Annotated, Doc

from fastapi import HTTPException
from starlette import status


class BaseAPIException(HTTPException):
    message: Optional[Union[str, Exception]] = "Some exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: Optional[Union[str, Exception]] = None):
        if message is not None:
            self.message = message

        if isinstance(message, Exception):
            self.message = str(message)

        super().__init__(status_code=self.status_code, detail=self.message)
