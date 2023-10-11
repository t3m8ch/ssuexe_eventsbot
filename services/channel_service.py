from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.channel_model import ChannelModel


class ChannelService:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_all_channels(self) -> list[ChannelModel]:
        return list((await self._db.execute(select(ChannelModel))).scalars().all())

    async def add_channel(self, *, name: str, chat_id: int):
        self._db.add(ChannelModel(name=name, chat_id=chat_id))
        await self._db.commit()

    async def get_channel_by_id(self, channel_id: str):
        return await self._db.get(ChannelModel, channel_id)
