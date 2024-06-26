from sqlalchemy import select
from api.pkg.models.postgres import UserTelegeramChat


class NotificationRepository:
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def read(self, id):
        async with self.session_factory() as s:
            stmt = select(UserTelegeramChat).where(UserTelegeramChat.user_id == id)
            res = await s.execute(stmt)
            return res.one_or_none()
