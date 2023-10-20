from uuid import UUID

from sqlalchemy import UUID as SA_UUID, text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ChannelModel(Base):
    __tablename__ = 'channels'

    id: Mapped[UUID] = mapped_column(SA_UUID, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
