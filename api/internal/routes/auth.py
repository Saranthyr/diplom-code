from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.auth import AuthService
from api.pkg.models.pydantic.body import UserActivate, UserRegister
from api.pkg.models.pydantic.responses import TokenResponse
from api.pkg.models.containers import Container

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
async def register(
    body: UserRegister = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.register(**body.model_dump())


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> TokenResponse:
    return await auth_service.login(
        username=form_data.username, password=form_data.password
    )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@inject
async def refresh(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    refresh_token: Annotated[str, Header()],
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.refresh(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post("/activate")
@inject
async def activate(
    body: UserActivate = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await auth_service.activate_account(**body.model_dump())
