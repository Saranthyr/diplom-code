from fastapi import status

from api.pkg.models.base.exception import BaseAPIException


class IncorrectUsernameOrPassword(BaseAPIException):
    message = "Incorrect username or password"
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class PasswordsNotMatch(BaseAPIException):
    message = "Password not match"
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class UsernameInUse(BaseAPIException):
    message = "Username already used"
    status_code = status.HTTP_409_CONFLICT


class NicknameInUse(BaseAPIException):
    message = "Nickname already used"
    status_code = status.HTTP_409_CONFLICT


class UserNotFound(BaseAPIException):
    message = "User not found"
    status_code = status.HTTP_404_NOT_FOUND


class IncorrectCurrentPassword(BaseAPIException):
    message = "Current password don't match"
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class MissingCurrentPassword(BaseAPIException):
    message = "Missing current password"
    status_code = status.HTTP_400_BAD_REQUEST


class NoPermission(BaseAPIException):
    message = "You have no access to this route"
    status_code = status.HTTP_403_FORBIDDEN


class ActivationRequired(BaseAPIException):
    message = "Account activation required"
    status_code = status.HTTP_406_NOT_ACCEPTABLE
