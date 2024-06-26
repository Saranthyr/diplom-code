from datetime import timedelta
import os
from typing import Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext
from sqlalchemy_file import File as SQLAFile

from api.internal.repos.postgres.files import FileRepository
from api.pkg.models.base.exception import BaseAPIException
from api.configuration.security import decode_token


class FileService:
    def __init__(self, file_repo: FileRepository) -> None:
        self.repository = file_repo

    async def create_file(self, file):
        sqlafile = SQLAFile(await file.read(), file.filename)
        return await self.repository.create(sqlafile, file.filename)

    async def read_file(self, id):
        return await self.repository.read(id)

    async def delete_file(self, id):
        return await self.repository.delete(id)
