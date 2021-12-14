import asyncio
import aiopg
import config


async def fetch(pool: asyncpg.Pool, query):
    async with pool.acquire() as connection:
        async with connection.transaction():
            async for record in connection.cursor(query):
                yield record


async def main():
    pool = await asyncpg.create_pool(config.DB_FILE)
    async for record in fetch(pool, 'SELECT * from users'):
        print(record['id'], record['name'])
    await pool.close()

if __name__ == '__main__':
    asyncio.run(main())
