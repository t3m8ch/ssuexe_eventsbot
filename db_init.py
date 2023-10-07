import aiosqlite


async def init_db(connection: aiosqlite.Connection):
    await connection.execute(
        'CREATE TABLE IF NOT EXISTS users ('
        'id INT PRIMARY KEY,'
        'full_name TEXT,'
        'user_name TEXT,'
        'role TEXT'
        ');'
    )
