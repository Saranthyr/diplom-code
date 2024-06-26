from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.auth import AuthService
from api.internal.services.search import SearchService
from api.pkg.models.pydantic.body import SearchQueryParams, SearchQueryPostParams
from api.pkg.models.pydantic.responses import SearchGlobalResponse, TokenResponse
from api.pkg.models.containers import Container

router = APIRouter(prefix="/search")


@router.get("/")
@inject
async def search_global(
    params: Annotated[SearchQueryParams, Depends()],
    search_service: SearchService = Depends(Provide[Container.search_service]),
):
    return await search_service.search(**params.model_dump())


@router.post("/posts")
@inject
async def search_posts(
    params: Annotated[SearchQueryPostParams, Depends()],
    search_service: SearchService = Depends(Provide[Container.search_service]),
):
    return await search_service.post_search(**params.model_dump())
