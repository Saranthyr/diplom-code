class PostHashtagService:
    def __init__(self, post_hashtag_repo) -> None:
        self.repository = post_hashtag_repo

    async def read(self, id):
        return await self.repository.read(id)

    async def create(self, id, tag):
        return await self.repository.create(id, tag)

    async def delete(self, id, tag):
        return await self.repository.delete(id, tag)
