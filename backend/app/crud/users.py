from sqlalchemy import select
from schemas import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

async def create_user(db:AsyncSession, data:dict):
    new_user = User(**data)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_user_by_id(user_id:int, db:AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    return user

async def get_user_by_email(email:str, db:AsyncSession):
    result = await db.execute(select(User).where(User.email==email))

    user = result.scalar_one_or_none()

    return user

async def get_users(db:AsyncSession):
    result = await db.execute(select(User))

    users = result.scalars().all()

    return users

async def get_users_by_role(role:UserRole, db:AsyncSession):
    result = await db.execute(select(User).where(User.role==role))

    user = result.scalars().all()

    return user

async def update_user(user_id:int, db:AsyncSession, data:dict):
    result = await db.query(select(User).where(User.id==user_id))

    user = result.scalar_one_or_none()

    if user is None:
        return None

    for key, value in data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user

async def delete_user():
    pass

