from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.channel_model import ChannelModel


class ChannelService:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_all_channels(self) -> list[ChannelModel]:
        return list((await self._db.execute(select(ChannelModel))).scalars().all())
