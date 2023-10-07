from dataclasses import dataclass
from datetime import datetime

from models.media_item_model import MediaItemModel


@dataclass
class EventModel:
    id: str
    text: str
    media: list[MediaItemModel]
    publish_at: datetime
