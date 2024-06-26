class PostAttachmentService:
    def __init__(self, post_attachment_repo) -> None:
        self.repository = post_attachment_repo

    async def read(self, id):
        return await self.repository.read(id)

    async def create(self, id, tag):
        return await self.repository.create(id, tag)

    async def delete(self, id, tag):
        return await self.repository.delete(id, tag)
