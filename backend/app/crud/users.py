from sqlalchemy import select
from schemas import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

async def create_user(db:AsyncSession, data:dict):
    new_user = User(**data)

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception:
        await db.rollback()
        raise

    return new_user


async def get_user_by_id(user_id:int, db:AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    return user

async def get_user_by_email(email:str, db:AsyncSession):
    result = await db.execute(select(User).where(User.email==email))

    user = result.scalar_one_or_none()

    return user

async def get_users(db:AsyncSession, skip:int=0, limit:int=50):
    result = await db.execute(select(User).offset(skip).limit(limit))

    users = result.scalars().all()

    return users

async def get_users_by_role(role:UserRole, db:AsyncSession):
    result = await db.execute(select(User).where(User.role==role))

    users = result.scalars().all()

    return users

async def update_user(user_id:int, db:AsyncSession, data:dict):
    result = await db.execute(select(User).where(User.id==user_id))

    user = result.scalar_one_or_none()

    if user is None:
        return None

    for key, value in data.items():
        setattr(user, key, value)

    try:
        await db.commit()
        await db.refresh(user)
    except Exception:
        await db.rollback()
        raise

    return user

async def update_user_role(user_id:int, db:AsyncSession, role:UserRole):
    result = await db.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    if user is None:
        return None

    user.role = role

    try:
        await db.commit()
        await db.refresh(user)
    except Exception:
        await db.rollback()
        raise

    return user
    

async def update_user_password(user_id:int, db:AsyncSession, hashed_password:str):
    result = await db.execute(select(User).where(User.id==user_id))

    user = result.scalar_one_or_none()

    if user is None:
        return None

    user.hashed_password = hashed_password
    try:
        await db.commit()
        await db.refresh(user)
    except Exception:
        await db.rollback()
        raise

    return user