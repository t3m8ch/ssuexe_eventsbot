import aiosqlite
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import UserModel


class UserService:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_or_update_user(self, *, user_id: int, full_name: str, user_name: str | None = None) -> UserModel:
        user = (await self._db.execute(select(UserModel).where(UserModel.id == user_id))).scalar()

        if not user:
            user = UserModel(id=user_id, full_name=full_name, user_name=user_name)
            self._db.add(user)
            await self._db.commit()
        else:
            user.id = user_id
            user.full_name = full_name
            user.user_name = user_name
            await self._db.commit()

        return user

    async def get_user_by_id(self, user_id: int) -> UserModel:
        user = (await self._db.execute(select(UserModel).where(UserModel.id == user_id))).scalar()

        if not user:
            raise Exception(f'User with id = {user_id} not found')

        return user

    async def get_users(self) -> list[UserModel]:
        return list((await self._db.execute(select(UserModel))).scalars().all())


def get_user_model_from_row(row) -> UserModel:
    return UserModel(id=row[0], full_name=row[1], user_name=row[2], role=row[3])
