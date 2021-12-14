from sqlite3_async_connect import Sqlite3Database
import asyncio
from config import DB_FILE


if __name__ == '__main__':
    db = Sqlite3Database(DB_FILE)
    table = db.find_table('contacts')
    asyncio.run(db.run_execute_program(f"SELECT * FROM {table.name} WHERE {table.columns[0]}<50", 5))

