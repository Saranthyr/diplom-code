from api.internal.repos.postgres.region_attachments import RegionAttachmentRepository


class RegionAttachmentService:
    def __init__(
        self, region_attachment_repository: RegionAttachmentRepository
    ) -> None:
        self.repo = region_attachment_repository

    async def read_all(self, id):
        return await self.repo.read_all(id)
