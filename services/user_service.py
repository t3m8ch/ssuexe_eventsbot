import aiosqlite

from models.user_model import UserModel


class UserService:
    def __init__(self, db: aiosqlite.Connection):
        self._db = db

    async def create_or_update_user(self, *, user_id: int, full_name: str, user_name: str | None = None) -> UserModel:
        async with self._db.execute('SELECT * FROM users') as cursor:
            row = await cursor.fetchone()

            if row is None:
                await self._db.execute(
                    f'INSERT INTO users(id, full_name, user_name, role) '
                    f'values ({user_id}, \'{full_name}\', \'{user_name}\', \'USER\');'
                )
                await self._db.commit()
                return UserModel(id=user_id, full_name=full_name, user_name=user_name, role='USER')

            return UserModel(id=row['id'], full_name=row['full_name'], user_name=row['user_name'], role=row['role'])
