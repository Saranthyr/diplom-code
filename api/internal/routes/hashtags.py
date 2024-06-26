from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.hashtag import HashtagService
from api.pkg.models.pydantic.responses import TokenResponse
from api.pkg.models.containers import Container

router = APIRouter(prefix="/hashtags")


@router.get("/")
@inject
async def read_all(
    hashtag_service: HashtagService = Depends(Provide[Container.hashtag_service]),
):
    return await hashtag_service.read_all()
