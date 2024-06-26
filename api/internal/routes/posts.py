from typing import Annotated
from uuid import UUID
import uuid

from fastapi import APIRouter, Depends, File, Form, Header, UploadFile, status
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.post import PostService
from api.internal.services.post_main import PostServiceMain
from api.pkg.models.pydantic.body import (
    PostComment,
    PostCreate,
    PostHashtagCreateDelete,
    PostRate,
    PostUpdate,
)
from api.pkg.models.containers import Container

router = APIRouter(prefix="/posts")


@router.post("/create", status_code=status.HTTP_201_CREATED)
@inject
async def create(
    token: Annotated[str, Depends(oauth2_scheme)],
    thumbnail: UploadFile,
    body: PostCreate = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.create_post(token, thumbnail, **body.model_dump())


@router.put("/update")
@inject
async def update(
    token: Annotated[str, Depends(oauth2_scheme)],
    thumbnail: UploadFile | None = Form(None),
    body: PostUpdate = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.update_post(token, thumbnail, **body.model_dump())


@router.delete("/delete")
@inject
async def delete(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: uuid.UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.delete_post(token, id)


@router.get("/{id}")
@inject
async def read(
    id: uuid.UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.read_post(id)


@router.put("/add_attachment")
@inject
async def add_attachment(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: Annotated[uuid.UUID, Form()],
    attachment: UploadFile,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.create_attachment(id, attachment)


@router.delete("/delete_attachment")
@inject
async def delete_attachment(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: Annotated[uuid.UUID, Form()],
    attachment_id: Annotated[uuid.UUID, Form()],
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.delete_attachment(id, attachment_id)


@router.put("/add_hashtag")
@inject
async def add_hashtag(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostHashtagCreateDelete = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.create_hashtag(**body.model_dump())


@router.delete("/delete_hashtag")
@inject
async def delete_hashtag(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostHashtagCreateDelete = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.delete_hashtag(**body.model_dump())


@router.post("/draft")
@inject
async def draft(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: uuid.UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.draft(token, id)


@router.post("/archive")
@inject
async def archive(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: uuid.UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.archive(token, id)


@router.post("/rate")
@inject
async def rate(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostRate = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.rate(token, **body.model_dump())


@router.put("/comment")
@inject
async def comment(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: PostComment = Depends(),
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.create_comment(token, **body.model_dump())


@router.get("/{id}/comments")
@inject
async def get_all_comments(
    id: UUID,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.read_comment(id)


@router.get("/{id}/comments/{comment_id}")
@inject
async def get_comment_replies(
    id: UUID,
    comment_id: int,
    post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
):
    return await post_service.read_comment(id, comment_id)


# @router.get("/{id}")
# @inject
# async def read(
#     id: UUID,
#     post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
# ):
#     return await post_service.read_post(id)


# @router.delete("/{id}")
# @inject
# async def delete(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     id: UUID,
#     post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
# ):
#     return await post_service.delete(token, id)


# @router.post("/comment")
# @inject
# async def comment(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     body: PostComment = Depends(),
#     post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
# ):
#     return await post_service.comment(token, **body.model_dump())


# @router.post("/save_as_draft")
# @inject
# async def draft(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     body: PostDraft = Depends(),
#     post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
# ):
#     return await post_service.draft(token, **body.model_dump())


# @router.post("/archive")
# @inject
# async def archive(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     body: PostArchive = Depends(),
#     post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
# ):
#     return await post_service.archive(token, **body.model_dump())


# @router.post("/rate")
# @inject
# async def rate(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     body: PostArchive = Depends(),
#     post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
# ):
#     return await post_service.rate(token, **body.model_dump())


# @router.get("/all")
# @inject
# async def all(
#     post_service: PostServiceMain = Depends(Provide[Container.post_service_main]),
# ):
#     return await post_service.all()
