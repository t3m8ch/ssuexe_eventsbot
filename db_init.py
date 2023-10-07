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
    await connection.execute(
        'CREATE TABLE IF NOT EXISTS events ('
        'id TEXT PRIMARY KEY,'
        'text TEXT,'
        'publish_at TEXT'
        ');'
    )
    await connection.execute(
        'CREATE TABLE IF NOT EXISTS media_items ('
        'file_id TEXT PRIMARY KEY,'
        'event_id TEXT,'
        'media_type TEXT,'
        'FOREIGN KEY (event_id) REFERENCES events (id)'
        ');'
    )
