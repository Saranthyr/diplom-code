import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler

from internal.commands import start, link
from pkg.models.containers import Container


# async def start(update, context):
#     await update.message.reply_text("Hi! Use /link <code> to link your account")


def main():
    container = Container()
    container.config.from_ini("/configs/config.ini")
    container.init_resources()
    container.wire(modules=["internal.commands", "__main__"])

    application = Application.builder().token(os.environ["BOT_TOKEN"]).build()

    application.add_handler(CommandHandler(["start", "help"], start))

    application.add_handler(CommandHandler("link", link))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    # logging.critical(os.environ['BOT_TOKEN'])
    main()
