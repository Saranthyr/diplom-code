import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton, Factory, Resource

from api.configuration.storage import S3Storage
from api.internal.repos.mongodb import MongoDBBase
from api.internal.repos.postgres.files import FileRepository
from api.internal.repos.postgres.hashtags import HashtagRepository
from api.internal.repos.postgres.notification import NotificationRepository
from api.internal.repos.postgres.post_attachment import PostAttachmentRepository
from api.internal.repos.postgres.post_hashtags import PostHashtagRepository
from api.internal.repos.postgres.posts import PostRepository
from api.internal.repos.postgres.ratings import RatingRepository
from api.internal.repos.postgres.region_attachments import RegionAttachmentRepository
from api.internal.repos.postgres.regions import RegionRepository
from api.internal.repos.postgres.tourism_types import TourismTypeRepository
from api.internal.repos.postgres.users import UserRepository
from api.internal.repos.s3 import S3
from api.internal.services.notification import NotificationService
from api.internal.services.post_attachment import PostAttachmentService
from api.internal.services.post_hashtag import PostHashtagService
from api.internal.services.redis import Redis
from api.internal.services.auth import AuthService
from api.internal.services.files import FileService
from api.internal.services.hashtag import HashtagService
from api.internal.services.post import PostService
from api.internal.services.post_main import PostServiceMain
from api.internal.services.rating import RatingService
from api.internal.services.region import RegionService
from api.internal.services.region_attachment import RegionAttachmentService
from api.internal.services.region_main import RegionMainService
from api.internal.services.search import SearchService
from api.internal.services.tourism import TourismService
from api.internal.services.tourism_main import TourismMainService
from api.internal.services.user import UserService
from api.internal.services.comment import CommentService
from api.internal.services.user_main import UserMainService
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

    mongodb_conn = Resource(MongoDBConn, uri=config.mongodb.uri)

    # s3 = Factory(S3, s3_session=s3_session, s3_uri=config.s3.endpoint)

    mongodb = Factory(MongoDBBase, mongodb_conn=mongodb_conn)

    comments = Factory(CommentService, mongodb=mongodb)

    user_repo = Factory(UserRepository, session_factory=db.provided.session)

    ratings_repo = Factory(RatingRepository, session_factory=db.provided.session)

    post_repo = Factory(PostRepository, session_factory=db.provided.session)

    region_repo = Factory(RegionRepository, session_factory=db.provided.session)

    tourism_repo = Factory(TourismTypeRepository, session_factory=db.provided.session)

    hashtag_repo = Factory(HashtagRepository, session_factory=db.provided.session)

    file_repo = Factory(FileRepository, session_factory=db.provided.session)

    notification_repo = Factory(
        NotificationRepository, session_factory=db.provided.session
    )

    post_attachments_repo = Factory(
        PostAttachmentRepository, session_factory=db.provided.session
    )

    post_hashtag_repo = Factory(
        PostHashtagRepository, session_factory=db.provided.session
    )

    region_attachment_repo = Factory(
        RegionAttachmentRepository, session_factory=db.provided.session
    )

    ratings_service = Factory(RatingService, ratings_repo=ratings_repo)

    file_service = Factory(FileService, file_repo=file_repo)

    post_service = Factory(PostService, post_repository=post_repo)

    user_service = Factory(UserService, user_repository=user_repo)

    region_service = Factory(RegionService, region_repo=region_repo)

    tourism_service = Factory(TourismService, tourism_repo=tourism_repo)

    post_attachment_service = Factory(
        PostAttachmentService, post_attachment_repo=post_attachments_repo
    )

    post_hashtag_service = Factory(
        PostHashtagService, post_hashtag_repo=post_hashtag_repo
    )

    region_attachment_service = Factory(
        RegionAttachmentService, region_attachment_repository=region_attachment_repo
    )

    hashtag_service = Factory(HashtagService, hashtag_repo=hashtag_repo)

    notification_service = Factory(
        NotificationService, notification_repo=notification_repo
    )

    redis_service = Factory(Redis, redis_conn=redis)

    post_service_main = Factory(
        PostServiceMain,
        post_service=post_service,
        file_service=file_service,
        rating_service=ratings_service,
        comments=comments,
        post_attachment_service=post_attachment_service,
        post_hashtag_service=post_hashtag_service,
        hashtag_service=hashtag_service,
        user_service=user_service,
        region_service=region_service,
        tourism_service=tourism_service,
        rabbitmq=rabbitmq,
    )

    region_main_service = Factory(
        RegionMainService,
        region_service=region_service,
        file_service=file_service,
        region_file_service=region_attachment_service,
    )

    tourism_main_service = Factory(
        TourismMainService, tourism_service=tourism_service, file_service=file_service
    )

    user_main_service = Factory(
        UserMainService,
        user_service=user_service,
        file_service=file_service,
        notification_service=notification_service,
    )

    auth_service = Factory(
        AuthService, user_service=user_service, redis=redis_service, rmq=rabbitmq
    )

    search_service = Factory(
        SearchService,
        post_service=post_service,
        user_service=user_service,
        post_hashtag_service=post_hashtag_service,
        hashtag_service=hashtag_service,
        region_service=region_service,
        file_service=file_service,
        tourism_service=tourism_service,
    )
