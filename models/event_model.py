from datetime import datetime
from uuid import UUID

from sqlalchemy import UUID as SA_UUID, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.media_item_model import MediaItemModel


class EventModel(Base):
    __tablename__ = 'events'

    id: Mapped[UUID] = mapped_column(SA_UUID, primary_key=True, server_default=text('gen_random_uuid()'))
    text: Mapped[str] = mapped_column(nullable=False)
    media_items: Mapped[list[MediaItemModel]] = relationship(cascade='all, delete-orphan')
    publish_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
