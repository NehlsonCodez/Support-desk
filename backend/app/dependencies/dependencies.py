from database import AsyncSessionLocal

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user():
    pass

