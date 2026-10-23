from fastapi import HTTPException, status
from schemas import UserRole, UserUpdate, PasswordUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_user_by_id, get_users, get_users_by_role, update_user, update_user_role, update_user_password
from core import verify_password, hash_password

async def get_user_service(user_id:int, db:AsyncSession):
    user = await get_user_by_id(user_id, db)

    if user is None:
        return None
    
    return user

async def get_users_service(db:AsyncSession, skip:int=0, limit:int=50):
    users = await get_users(db, skip, limit)

    return users


async def get_users_by_role_service(role:UserRole, db:AsyncSession):
    users = await get_users_by_role(role, db)

    return users

async def update_user_service(user_id:int, db:AsyncSession, data:UserUpdate):
    user = await get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no field provided for for update")

    
    updated_user = await update_user(user_id, db, update_data)

    return updated_user


async def update_user_role_service(user_id:int, db:AsyncSession, role:UserRole):
    user = await get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    updated_role = await update_user_role(user_id, db, role)

    return updated_role

async def update_user_password_service(user_id:int, db:AsyncSession, data:PasswordUpdate):
    user = await get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    if not await verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    hashed_password = await hash_password(data.new_password)

    updated_password = await update_user_password(user_id, db, hashed_password)

    return updated_password

    