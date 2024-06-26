from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from api.configuration.security import oauth2_scheme
from api.internal.services.region_main import RegionMainService
from api.pkg.models.pydantic.responses import TokenResponse
from api.pkg.models.containers import Container

router = APIRouter(prefix="/regions")


@router.get("/")
@inject
async def read_all(
    region_service: RegionMainService = Depends(Provide[Container.region_main_service]),
):
    return await region_service.read_all()


@router.get("/{id}")
@inject
async def read(
    id: int,
    region_service: RegionMainService = Depends(Provide[Container.region_main_service]),
):
    return await region_service.read(id)
