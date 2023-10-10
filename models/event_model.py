import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.media_item_model import MediaItemModel


class EventModel(Base):
    __tablename__ = 'events'

    id: Mapped[str] = mapped_column(primary_key=True, insert_default=str(uuid.uuid4()))
    text: Mapped[str] = mapped_column(nullable=False)
    media_items: Mapped[list[MediaItemModel]] = relationship(cascade='all, delete-orphan')
    publish_at: Mapped[datetime] = mapped_column(nullable=False)
