from fastapi import status

from api.pkg.models.base.exception import BaseAPIException


class PostRegionNameInUse(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = "Post with this name already exists in region"


class NotYourPost(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Not your post"
