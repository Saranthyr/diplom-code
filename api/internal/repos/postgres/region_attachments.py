from sqlalchemy import select

from api.pkg.models.postgres import PostAttachments, RegionPhoto


class RegionAttachmentRepository:
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def read_all(self, id):
        async with self.session_factory() as s:
            stmt = select(RegionPhoto.photo_id).where(RegionPhoto.region_id == id)
            res = await s.execute(stmt)
            return res.scalars().all()
