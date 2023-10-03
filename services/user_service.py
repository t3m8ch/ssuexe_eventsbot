import aiosqlite

from models.user_model import UserModel


class UserService:
    def __init__(self, db: aiosqlite.Connection):
        self._db = db

    async def create_or_update_user(self, *, user_id: int, full_name: str, user_name: str | None = None) -> UserModel:
        async with self._db.execute(f'SELECT * FROM users WHERE id = {user_id}') as cursor:
            row = await cursor.fetchone()

            if row is None:
                await self._db.execute(
                    f'INSERT INTO users(id, full_name, user_name, role) '
                    f'values ({user_id}, \'{full_name}\', \'{user_name}\', \'USER\');'
                )
                await self._db.commit()
                return UserModel(id=user_id, full_name=full_name, user_name=user_name, role='USER')

            return get_user_model_from_row(row)

    async def get_user_by_id(self, user_id: int) -> UserModel:
        async with self._db.execute(f'SELECT * FROM users WHERE id = {user_id}') as cursor:
            row = await cursor.fetchone()

            if row is None:
                raise Exception(f'User with id = {user_id} not found')

            return get_user_model_from_row(row)


def get_user_model_from_row(row) -> UserModel:
    return UserModel(id=row[0], full_name=row[1], user_name=row[2], role=row[3])
