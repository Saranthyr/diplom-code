from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from httpx import request

from api.configuration.security import oauth2_scheme
from api.internal.services.auth import AuthService
from api.internal.services.user import UserService
from api.pkg.models.pydantic.body import UserUpdate
from api.pkg.models.containers import Container
from api.pkg.models.pydantic.responses import UserResponse

router = APIRouter(prefix="/user")


@router.put("/update", status_code=status.HTTP_202_ACCEPTED)
@inject
async def update(
    token: Annotated[str, Depends(oauth2_scheme)],
    body: UserUpdate = Depends(),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return await user_service.update_user(token, **body.model_dump())


@router.get("/update", response_model=UserResponse)
@inject
async def read_update(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return await user_service.read_user(token)


@router.delete("/delete")
@inject
async def delete(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return await user_service.delete_user(token)


@router.get(
    "/",
    response_model=UserResponse,
    response_model_exclude={"username", "password"},
    status_code=status.HTTP_200_OK,
)
@inject
async def read_curr(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return await user_service.read_user(token)


@router.get("/{nickname}", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
@inject
async def read(
    nickname: str, user_service: UserService = Depends(Provide[Container.user_service])
):
    return templates.TemplateResponse(
        name="profile.html", context=await user_service.read_user(nickname)
    )
