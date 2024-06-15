import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton, Factory, Resource

from api.configuration.storage import S3Storage
from api.internal.repos.mongodb import MongoDBBase
from api.internal.repos.postgres.files import FileRepository
from api.internal.repos.postgres.hashtags import HashtagRepository
from api.internal.repos.postgres.posts import PostRepository
from api.internal.repos.postgres.ratings import RatingRepository
from api.internal.repos.postgres.regions import RegionRepository
from api.internal.repos.postgres.tourism_types import TourismTypeRepository
from api.internal.repos.postgres.users import UserRepository
from api.internal.repos.s3 import S3
from api.internal.services.redis import Redis
from api.internal.services.auth import AuthService
from api.internal.services.files import FileService
from api.internal.services.hashtag import HashtagService
from api.internal.services.post import PostService
from api.internal.services.post_main import PostServiceMain
from api.internal.services.rating import RatingService
from api.internal.services.region import RegionService
from api.internal.services.search import SearchService
from api.internal.services.tourism import TourismService
from api.internal.services.user import UserService
from api.internal.services.comment import CommentService
from api.pkg.connectors import Database, MongoDBConn, RabbitMQ, RedisConn, S3Connector


class Container(DeclarativeContainer):
    config = Configuration()

    db = Resource(Database, uri=config.database.uri)

    redis = Resource(RedisConn, uri=config.redis.uri)

    rabbitmq = Resource(RabbitMQ, uri=config.rmq.uri)

    s3_session = Resource(
        S3Connector,
        aws_access_key_id=config.s3.aws_access_key_id,
        aws_secret_access_key=config.s3.aws_secret_access_key,
    )

    s3_storage = Resource(
        S3Storage,
        aws_access_key=config.s3.aws_access_key_id,
        aws_secret_key=config.s3.aws_secret_access_key,
        host=config.s3.host,
        port=config.s3.port,
    )

    redis_service = Factory(Redis, redis_conn=redis)

    mongodb_conn = Resource(MongoDBConn, uri=config.mongodb.uri)

    s3 = Factory(S3, s3_session=s3_session, s3_uri=config.s3.endpoint)

    mongodb = Factory(MongoDBBase, mongodb_conn=mongodb_conn)

    comments = Factory(CommentService, mongodb=mongodb)

    user_repo = Factory(UserRepository, session_factory=db.provided.session)

    ratings_repo = Factory(RatingRepository, session_factory=db.provided.session)

    post_repo = Factory(PostRepository, session_factory=db.provided.session)

    region_repo = Factory(RegionRepository, session_factory=db.provided.session)

    tourism_repo = Factory(TourismTypeRepository, session_factory=db.provided.session)

    hashtag_repo = Factory(HashtagRepository, session_factory=db.provided.session)

    file_repo = Factory(FileRepository, session_factory=db.provided.session)

    ratings_service = Factory(RatingService, ratings_repo=ratings_repo)

    file_service = Factory(FileService, file_repo=file_repo)

    post_service = Factory(PostService, post_repository=post_repo)

    post_service_main = Factory(
        PostServiceMain,
        post_service=post_service,
        file_service=file_service,
        rating_service=ratings_service,
        comments=comments,
        s3=s3,
    )

    user_service = Factory(UserService, user_repository=user_repo)

    region_service = Factory(RegionService, region_repo=region_repo)

    tourism_service = Factory(TourismService, tourism_repo=tourism_repo)

    auth_service = Factory(
        AuthService, user_service=user_service, redis=redis_service, rmq=rabbitmq
    )

    search_service = Factory(
        SearchService, post_service=post_service, user_service=user_service
    )
