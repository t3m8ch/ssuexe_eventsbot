from typing import Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class MediaItemModel(Base):
    __tablename__ = 'media'

    file_id: Mapped[str] = mapped_column(primary_key=True)
    media_type: Mapped[Literal['video', 'photo']] = mapped_column(nullable=False)
    event_id: Mapped[str] = mapped_column(ForeignKey('events.id'), nullable=False)
