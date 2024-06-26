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
                        case "new_comment":
                            try:
                                await mailer.send_new_comment_notif(
                                    op["email"], op["post_name"]
                                )
                            except Exception as e:
                                print(traceback.print_exception(e))
                        case "response_comment":
                            try:
                                await mailer.send_comment_response_notif(
                                    op["email"], op["post_name"]
                                )
                            except Exception as e:
                                print(traceback.print_exception(e))
                        case "post_published":
                            try:
                                await mailer.send_post_published(
                                    op["email"], op["post_name"]
                                )
                            except Exception as e:
                                print(traceback.print_exception(e))
                        case "post_rejected":
                            try:
                                await mailer.send_post_rejected(
                                    op["email"], op["post_name"]
                                )
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
