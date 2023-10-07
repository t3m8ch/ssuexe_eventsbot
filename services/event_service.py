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
