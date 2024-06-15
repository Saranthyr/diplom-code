from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory, Resource, Configuration

from pkg.connectors import RabbitMQ
from pkg.connectors import RedisConn
from internal.worker import MailerService
from internal.redis_service import Redis as RedisService
from internal.code_gen import CodeGenerator
from internal.main import MainService


class Container(DeclarativeContainer):
    config = Configuration()

    rabbitmq_conn = Resource(RabbitMQ, uri=config.rmq.uri)
    redis_conn = Resource(RedisConn, uri=config.redis.uri)

    mailer_service = Factory(
        MailerService,
        sender=config.mailer.sender,
        password=config.mailer.sender_password,
        host=config.mailer.host,
        port=config.mailer.port,
    )

    redis_service = Factory(RedisService, conn=redis_conn)

    code_gen = Factory(CodeGenerator)

    main_service = Factory(
        MainService,
        mailer=mailer_service,
        redis=redis_service,
        code_gen=code_gen,
    )
