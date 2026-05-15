import asyncpg
import os

_pool = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        for var in ("POSTGRES_HOST", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"):
            if not os.environ.get(var):
                raise RuntimeError(f"{var} environment variable is required but not set")

        _pool = await asyncpg.create_pool(
            host=os.environ["POSTGRES_HOST"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            database=os.environ["POSTGRES_DB"],
        )
    return _pool


async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
