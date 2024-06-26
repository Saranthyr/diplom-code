from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory, Resource, Configuration

from pkg.connectors.redis import RedisConn
from pkg.connectors import RabbitMQ
from pkg.connectors.database import Database


class Container(DeclarativeContainer):
    config = Configuration()

    rabbitmq_conn = Resource(RabbitMQ, uri=config.rmq.uri)
    db_conn = Resource(Database, uri=config.db.uri)
    redis_conn = Resource(RedisConn, uri=config.redis.uri)
