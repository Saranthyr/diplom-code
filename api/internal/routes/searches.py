from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.auth import AuthService
from api.internal.services.search import SearchService
from api.pkg.models.pydantic.body import PostSearchQuery, UserRegister, UserSearchQuery
from api.pkg.models.pydantic.responses import TokenResponse
from api.pkg.models.containers import Container

router = APIRouter(prefix="/search")


@router.get("/posts")
@inject
async def posts(
    params: PostSearchQuery = Depends(PostSearchQuery),
    search_service: SearchService = Depends(Provide[Container.search_service]),
):
    return await search_service.posts(**params.model_dump())


@router.get("/users")
@inject
async def users(
    params: UserSearchQuery = Depends(UserSearchQuery),
    search_service: SearchService = Depends(Provide[Container.search_service]),
):
    return await search_service.users(**params.model_dump())
