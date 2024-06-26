from api.internal.services.files import FileService
from api.internal.services.tourism import TourismService
from api.pkg.models.pydantic.responses import TourismResponse


class TourismMainService:
    def __init__(
        self,
        tourism_service: TourismService,
        file_service: FileService,
    ) -> None:
        self.tourism_service = tourism_service
        self.file_service = file_service

    async def read(self, id):
        data = await self.tourism_service.read(id)

        photo = None
        if data["photo"] is not None:
            photo = (await self.file_service.read_file(data["photo"]))["url"]
        res = TourismResponse(**data)
        res.photo = photo
        return res

    async def read_all(self):
        return await self.tourism_service.read_all()
