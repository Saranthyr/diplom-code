class NotificationService:
    def __init__(self, notification_repo) -> None:
        self.repository = notification_repo

    async def available(self, uid):
        if await self.repository.read(uid) is None:
            return False
        return True
