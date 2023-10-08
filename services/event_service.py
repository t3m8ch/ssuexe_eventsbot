import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import aiosqlite

from models.event_model import EventModel
from models.media_item_model import MediaItemModel


class EventService:
    def __init__(self, db: aiosqlite.Connection):
        self._db = db

    async def schedule_event(self, *, text: str, media_items: list[MediaItemModel], publish_at: datetime) -> EventModel:
        event_id = str(uuid.uuid4())
        publish_at_str = publish_at.astimezone(ZoneInfo('Etc/UTC')).isoformat()

        await self._db.execute(
            'INSERT INTO events(id, text, publish_at) values (?, ?, ?)',
            [event_id, text, publish_at_str],
        )

        await self._db.executemany(
            'INSERT INTO media_items(file_id, event_id, media_type) values (?, ?, ?);',
            [[item.file_id, event_id, item.media_type] for item in media_items]
        )

        await self._db.commit()

        return EventModel(event_id, text, media_items, publish_at)

    async def get_event_by_id(self, event_id: str) -> EventModel:
        async with self._db.cursor() as cursor:
            event_row = await (await cursor.execute(
                'SELECT (id, text, publish_at) from events WHERE event_id = ?', event_id
            )).fetchone()

            if event_row is None:
                raise Exception(f'Event with id = {event_id} not found')

            media_items_rows = await (await cursor.execute(
                'SELECT (file_id, media_type) from media_items WHERE event_id = ?', event_id
            )).fetchmany()

            return EventModel(id=event_row[0], text=event_row[1], publish_at=event_row[2], media=[
                MediaItemModel(file_id=m[0], media_type=m[1]) for m in media_items_rows
            ])

    async def get_events_with_datetime(self, from_: datetime, to: datetime) -> list[EventModel]:
        raise NotImplementedError()
