from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.auth import AuthService
from api.internal.services.post import PostService
from api.internal.services.post_main import PostServiceMain
from api.pkg.models.pydantic.body import (
    PostArchive,
    PostComment,
    PostCreate,
    PostDraft,
    UserRegister,
)
from api.pkg.models.pydantic.responses import TokenResponse
from api.pkg.models.containers import Container

router = APIRouter(prefix="/posts")


@router.put("/create", status_code=status.HTTP_202_ACCEPTED)
@inject
async def create(
    token: Annotated[str, Depends(oauth2_scheme)],
    thumbnail: UploadFile,
    body: PostCreate = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.create_post(token, thumbnail, **body.model_dump())


@router.get("/{id}")
@inject
async def read(
    id: UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.read_post(id)


@router.delete("/{id}")
@inject
async def delete(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.delete(token, id)


@router.post("/comment")
@inject
async def comment(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostComment = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.comment(token, **body.model_dump())


@router.post("/save_as_draft")
@inject
async def draft(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostDraft = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.draft(token, **body.model_dump())


@router.post("/archive")
@inject
async def archive(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostArchive = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.archive(token, **body.model_dump())


@router.post("/rate")
@inject
async def rate(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostArchive = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.rate(token, **body.model_dump())


@router.get("/{id}/comments")
@inject
async def get_all_comments(
    id: UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.all_comments(id)


@router.get("/{id}/comments/{comment_id}")
@inject
async def get_comment_replies(
    id: UUID,
    comment_id: int,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.all_comments(id, comment_id)


@router.get('/all')
@inject
async def all(post_service: PostServiceMain = Depends(Provide[Container.post_service_main])):
    return await post_service.all()
