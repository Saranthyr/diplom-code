from contextlib import asynccontextmanager

from dependency_injector.resources import Resource
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDBConn(Resource):
    def init(self, uri) -> AsyncIOMotorDatabase:
        cl = AsyncIOMotorClient(uri)
        db = cl.get_database("comments")
        return db
