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
