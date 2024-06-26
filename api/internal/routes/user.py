from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import HTMLResponse
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.user_main import UserMainService
from api.pkg.models.pydantic.body import UserPasswordUpdate, UserUpdate
from api.pkg.models.containers import Container
from api.pkg.models.pydantic.responses import UserResponse

router = APIRouter(prefix="/user")


@router.put("/update", status_code=status.HTTP_202_ACCEPTED)
@inject
async def update(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: UserUpdate = Depends(),
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.update_base(token, **body.model_dump())


@router.put("/update_password", response_model=UserResponse)
@inject
async def update_password(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: UserPasswordUpdate,
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.update_password(token, **body.model_dump())


@router.delete("/delete")
@inject
async def delete(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.delete(token)


@router.get(
    "/",
    response_model=UserResponse,
    response_model_exclude={"username", "password"},
    status_code=status.HTTP_200_OK,
)
@inject
async def read_curr(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.read(token)


@router.delete("/avatar")
@inject
async def delete_avatar(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.delete_avatar(token)


@router.put("/avatar")
@inject
async def put_avatar(
    token: Annotated[str, Depends(oauth2_scheme)],
    avatar: UploadFile,
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.update_avatar(token, avatar)


@router.put("/header")
@inject
async def put_header(
    token: Annotated[str, Depends(oauth2_scheme)],
    header: UploadFile,
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.update_header(token, header)


@router.delete("/header")
@inject
async def delete_header(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.delete_header(token)


@router.get("/notification_channel")
@inject
async def notification_get(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.notification_channel_get(token)


@router.post("/notification_channel")
@inject
async def notification_post(
    token: Annotated[str, Depends(oauth2_scheme)],
    channel: int,
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.notification_channel_post(token, channel)


@router.get("/{nickname}", status_code=status.HTTP_200_OK)
@inject
async def read(
    nickname: str,
    user_service: UserMainService = Depends(Provide[Container.user_main_service]),
):
    return await user_service.read_nickname(nickname)
