import json
import logging
import uuid

from sqlalchemy import select
from telegram.ext import ContextTypes
from dependency_injector.wiring import inject, Provide
from redis.asyncio import Redis as RedisSess


from pkg.models.containers import Container
from pkg.connectors.rabbitmq import RabbitMQ
from pkg.connectors.redis import RedisConn
from pkg.connectors.database import Database
from pkg.models.postgres import UserTelegeramChat


async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в бот сайта \"Внутренний туризм\". Пожалуйста, используйте комманду /link вместе с кодом активации бота, поступившим на Вашу почту.")
    context.job_queue.run_once(test, 1)


@inject
async def link(
    update,
    context: ContextTypes.DEFAULT_TYPE,
    redis=Provide[Container.redis_conn],
    database: Database = Provide[Container.db_conn],
):
    chat_id = update.effective_message.chat_id

    try:
        user_id = uuid.UUID((await redis.get(context.args[0])).decode("utf-8"))

        if user_id is None:
            await update.effective_message.reply_text("Неверный код!")

        async with database.session() as s:
            data = UserTelegeramChat(user_id=user_id, chat=chat_id)
            s.add(data)
            try:
                await s.commit()
            except Exception:
                pass
        await redis.delete(context.args[0])
        await update.effective_message.reply_text("Ваш аккаунт успешно привязан!")

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Использование: /link <code>")


@inject
async def test(
    context,
    database: Database = Provide[Container.db_conn],
    rmq: RabbitMQ = Provide[Container.rabbitmq_conn],
):
    async with rmq.connection() as conn:
        ch = await conn.channel()

        queue = await ch.declare_queue("telegram", auto_delete=True)

        async with queue.iterator() as iter:
            async for message in iter:
                async with message.process():
                    op = json.loads(message.body)
                    async with database.session() as s:
                        stmt = select(UserTelegeramChat.chat).where(
                            UserTelegeramChat.user_id == uuid.UUID(op["user_id"])
                        )
                        res = await s.execute(stmt)
                        chat_id = res.scalar_one()
                    op["chat_id"] = chat_id
                    await send_msg(context, op)


async def send_msg(context, data):
    match data["action"]:
        case "new_comment":
            text = f"Ваша статья {data['post_name']} получила новый комментарий"
        case "response_comment":
            text = f"Ваша комментарий под статьей {data['post_name']} получил новый ответ"
        case "post_published":
            text = f"Ваша статья {data['post_name']} была одобрена к публикации администрацией сайта"
        case "post_rejected":
            text = f"Ваша статья {data['post_name']} была отклонена к публикации администрацией сайта"
    await context.bot.send_message(data["chat_id"], text=text)
