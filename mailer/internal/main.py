import time
from internal.code_gen import CodeGenerator
from internal.worker import MailerService
from internal.redis_service import Redis


class MainService:
    def __init__(
        self,
        mailer: MailerService,
        redis: Redis,
        code_gen: CodeGenerator,
    ) -> None:
        self.mailer = mailer
        self.code_gen = code_gen
        self.redis = redis

    async def send_verification_code(self, receiver: str) -> int:
        seed = await self.code_gen.generate_seed(receiver)
        code = await self.code_gen.generate_code(seed, int(time.time()))
        await self.mailer.send_mail(
            receiver, "Код регистрации", f"Ваш код для регистрации на сайте \"Внутренний туризм\": {code}"
        )
        await self.redis.set_code(receiver, str(code))
        return 0

    async def send_new_comment_notif(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver, "Новый комментарий", f"Новый комментарий под Вашей статьей {post_name}"
        )
        return 0

    async def send_comment_response_notif(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver,
            "Новый ответ на комментарий",
            f"Ваш комментарий под статьей {post_name} получил ответ",
        )

    async def send_post_published(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver,
            "Статья опубликована",
            f"Ваша статья {post_name} была одобрена к публикации администрацией сайта",
        )
        return 0

    async def send_post_rejected(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver,
            "Статья отклонена к публикации",
            f"Ваша статья {post_name} была отклонена к публикации администрацией сайта",
        )
        return 0
    
    async def send_activation_success(self, receiver: str, code: str) -> int:
        await self.mailer.send_mail(
            receiver,
            "Добро пожаловать на сайт \"Внутренний туризм\"",
            f"Аккаунт успешно активирован! Ваш код для активации Telegram бота(t.me/travel_diplom_bot) - {code}",
        )
        return 0