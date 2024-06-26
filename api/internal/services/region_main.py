from api.internal.services.files import FileService
from api.internal.services.region import RegionService
from api.internal.services.region_attachment import RegionAttachmentService
from api.pkg.models.pydantic.responses import RegionResponse


class RegionMainService:
    def __init__(
        self,
        region_service: RegionService,
        file_service: FileService,
        region_file_service: RegionAttachmentService,
    ) -> None:
        self.region_service = region_service
        self.file_service = file_service
        self.region_file_service = region_file_service

    async def read_all(self):
        return await self.region_service.read_all()

    async def read(self, id):
        data = await self.region_service.read(id)

        attach = await self.region_file_service.read_all(id)
        attachments = []
        for file in attach:
            file = await self.file_service.read_file(file)
            attachments.append(file["url"])

        thumbnail = None
        if data["thumbnail"] is not None:
            file = await self.file_service.read_file(data["thumbnail"])
            thumbnail = file["url"]

        res = RegionResponse(**data, attachments=attachments)
        res.thumbnail = thumbnail
        return res
