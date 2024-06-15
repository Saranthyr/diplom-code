class CommentService:
    def __init__(self, mongodb) -> None:
        self.mongodb = mongodb

    async def insert_comment(self, user_id, post_id, parent, contents):
        collection = await self.mongodb.get_collection(post_id)
        return await self.mongodb.insert_comment(user_id, contents, collection, parent)

    async def comments_with_replies(self, id, comment_id: int | None = None):
        collection = await self.mongodb.get_collection(id)
        return await self.mongodb.comments_with_replies(collection, comment_id)
