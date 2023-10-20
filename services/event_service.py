from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.event_model import EventModel
from models.media_item_model import MediaItemModel


class EventService:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def schedule_event(self, *, text: str, media_items: list[MediaItemModel], publish_at: datetime) -> EventModel:
        event = EventModel(
            text=text,
            media_items=media_items,
            publish_at=publish_at.astimezone(ZoneInfo('Etc/UTC'))
        )

        self._db.add(event)

        await self._db.commit()
        return event

    async def get_event_by_id(self, event_id: UUID) -> EventModel:
        stmt = select(EventModel).where(EventModel.id == event_id).options(selectinload(EventModel.media_items))
        model = (await self._db.execute(stmt)).scalar()

        if not model:
            raise Exception(f'Event with id = {event_id} not found')

        return model

    async def get_events_with_datetime(self, from_: datetime, to: datetime) -> list[EventModel]:
        from_ = from_.astimezone(ZoneInfo('Etc/UTC'))
        to = to.astimezone(ZoneInfo('Etc/UTC'))

        stmt = select(EventModel).where(and_(from_ <= EventModel.publish_at, EventModel.publish_at <= to))
        return list((await self._db.execute(stmt)).scalars().all())
