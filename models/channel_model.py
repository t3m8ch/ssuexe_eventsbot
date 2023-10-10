import uuid

from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ChannelModel(Base):
    __tablename__ = 'channels'

    id: Mapped[str] = mapped_column(primary_key=True, insert_default=str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(nullable=False)
