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
            receiver, "Verification_code", f"Your verification code is {code}"
        )
        await self.redis.set_code(receiver, str(code))
        return 0

    async def send_new_comment_notif(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver, "New comment", f"New comment under your post {post_name}"
        )
        return 0

    async def send_comment_response_notif(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver,
            "New comment response",
            f"Your comment under post {post_name} received a response",
        )

    async def send_post_published(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver,
            "Post published",
            f"Your post {post_name} has been accepted for publishing by administation",
        )
        return 0

    async def send_post_rejected(self, receiver: str, post_name: str) -> int:
        await self.mailer.send_mail(
            receiver,
            "Post published",
            f"Your post {post_name} has been rejected for publishing by administation",
        )
        return 0
