from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from common.types import UserRole
from models.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    user_name: Mapped[str | None] = mapped_column(nullable=True)
    role: Mapped[UserRole] = mapped_column(server_default='USER')
