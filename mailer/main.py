import asyncio
import json
import traceback

from dependency_injector.wiring import Provide, inject

from internal.main import MainService
from pkg.connectors import RabbitMQ
from pkg.models.containers import Container


@inject
async def runner(
    rmq: RabbitMQ = Provide[Container.rabbitmq_conn],
    mailer: MainService = Provide[Container.main_service],
):
    async with rmq.connection() as conn:
        channel = await conn.channel()

        queue = await channel.declare_queue("mailer", auto_delete=True)

        async with queue.iterator() as iter:
            async for message in iter:
                async with message.process():
                    op = json.loads(message.body)

                    match op["action"]:
                        case "code":
                            try:
                                await mailer.send_verification_code(op["email"])
                            except Exception as e:
                                print(traceback.print_exception(e))


def main():
    container = Container()
    container.config.from_ini("/configs/config.ini")
    container.init_resources()
    container.wire(modules=[__name__])

    asyncio.run(runner())


if __name__ == "__main__":
    main()
