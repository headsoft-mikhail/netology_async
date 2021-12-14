import asyncio
import aiosqlite
from aiostream import stream
from sender import send_email


class Table:
    def __init__(self, name, rows_count, column_names):
        self.name = name
        self.columns = [column_name for column_name in column_names]
        self.rows_count = rows_count

    def __str__(self):
        return f'{self.name}: {self.columns}'


class Sqlite3Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.tables = []
        asyncio.run(self.run_init())
        for table in self.tables:
            print('Table initialized:\n', table)

    def find_table(self, table_name):
        for table in self.tables:
            if table.name == table_name:
                return table

    async def get_rows_count(self, db, table_name):
        return (await ((await db.execute(f"SELECT COUNT(*) FROM {table_name}")).fetchone()))[0]

    async def get_column_names(self, db, table_name):
        return [item[0]
                for item
                in (await db.execute(f"SELECT * FROM {table_name} LIMIT 1")).description]

    async def init_tables(self):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("SELECT name FROM sqlite_master WHERE type = 'table'") as tables_cursor:
                table_names = await tables_cursor.fetchone()
                self.tables = [
                    Table(table_name, *(await asyncio.gather(self.get_rows_count(db, table_name),
                                                             self.get_column_names(db, table_name)
                                                             )
                                        )
                          )
                    for table_name
                    in table_names
                ]

    async def run_init(self):
        return await asyncio.gather(self.init_tables())

    async def fetch(self, query):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(query) as cursor:
                async for row in cursor:
                    yield row

    async def execute_program(self, query, chunk_rate):
        fetch_parts = stream.chunks(self.fetch(query), chunk_rate)
        async for part in fetch_parts:
            [print(item) for item in part]
            await asyncio.gather(
                *[
                    send_email(item[3],
                               'Hello',
                               f'Уважаемый {item[1]} {item[2]}! \n'
                               f'Спасибо, что пользуетесь нашим сервисом объявлений.')
                    for item in part
                ])

    async def run_execute_program(self, query, chunk_rate):
        return await asyncio.gather(self.execute_program(query, chunk_rate))


