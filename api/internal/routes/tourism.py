from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.tourism import TourismService
from api.pkg.models.pydantic.body import UserRegister
from api.pkg.models.pydantic.responses import TokenResponse
from api.pkg.models.containers import Container

router = APIRouter(prefix="/tourism")


@router.get("/")
@inject
async def read_all(
    tourism_service: TourismService = Depends(Provide[Container.tourism_service]),
):
    return await tourism_service.read_all()


@router.get("/{id}")
@inject
async def read(
    id: int,
    tourism_service: TourismService = Depends(Provide[Container.tourism_service]),
):
    return await tourism_service.read(id)
