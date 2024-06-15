from fastapi import status

from api.pkg.models.base.exception import BaseAPIException


class ExpiredJWT(BaseAPIException):
    message = "Expired Bearer"
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class InvalidJWT(BaseAPIException):
    message = "Invalid Bearer"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidRefresh(BaseAPIException):
    message = "Invalid refresh token"
    status_code = status.HTTP_401_UNAUTHORIZED
