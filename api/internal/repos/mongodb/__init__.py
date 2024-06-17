import datetime
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from api.pkg.connectors.mongodb import MongoDBConn


class MongoDBBase:
    def __init__(self, mongodb_conn: AsyncIOMotorDatabase):
        self.mongodb_conn = mongodb_conn

    async def get_collection(self, id: UUID) -> AsyncIOMotorCollection:
        curr_coll = self.mongodb_conn.get_collection(str(id))
        await curr_coll.create_index({"reply_to": 1})
        return curr_coll

    async def insert_comment(
        self,
        user_id: UUID,
        content: str,
        created_at: datetime.datetime,
        collection: AsyncIOMotorCollection,
        parent: int | None = None,
    ) -> int:
        last_id = await collection.count_documents({})
        comment = {
            "_id": last_id + 1,
            "user": str(user_id),
            "content": content,
            "created_at": created_at,
            "reply_to": parent,
        }
        await collection.insert_one(comment)
        return 0

    async def comments_with_replies(
        self, collection: AsyncIOMotorCollection, base_comment: int | None = None
    ):
        data = collection.aggregate(
            [
                {"$match": {"parent_comment_id": base_comment}},
                {
                    "$lookup": {
                        "from": "comments",
                        "let": {"comment_id": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": ["$parent_comment_id", "$$comment_id"]
                                    }
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "comments",
                                    "let": {"reply_id": "$_id"},
                                    "pipeline": [
                                        {
                                            "$match": {
                                                "$expr": {
                                                    "$eq": [
                                                        "$parent_comment_id",
                                                        "$$reply_id",
                                                    ]
                                                }
                                            }
                                        }
                                    ],
                                    "as": "replies",
                                }
                            },
                        ],
                        "as": "replies",
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "content": 1,
                        "parent_comment_id": 1,
                        "user": 1,
                        "created_at": 1,
                        "replies": {
                            "$map": {
                                "input": "$replies",
                                "as": "reply",
                                "in": {
                                    "_id": "$$reply._id",
                                    "content": "$$reply.content",
                                    "parent_comment_id": "$$reply.parent_comment_id",
                                    "user": "$$reply.user",
                                    "replies": "$$reply.replies",
                                    "created_at": "$$reply.created_at"
                                },
                            }
                        },
                    }
                },
            ]
        )
        return await data.to_list(None)
