from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate, UserLogin
from core import hash_password, verify_password, create_access_token
from crud import create_user, get_user_by_email, get_user_by_id

async def create_user_service(db:AsyncSession, data:UserCreate):
    user_exist = await get_user_by_email(data.email, db)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An account with this email already exists")

    user_data = data.model_dump(exclude_unset=True)

    raw_password = user_data.pop("password", None)
    if not raw_password and "hashed_password" in user_data:
        raw_password = user_data.pop("hashed_password")

    user_data["hashed_password"] = await hash_password(raw_password)

    new_user = await create_user(db, user_data)

    return new_user
    

async def login_user_service(db:AsyncSession, data):
    identifier = getattr(data, "username", None) or getattr(data, "email", None)
    if not identifier:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email is required")

    db_user = await get_user_by_email(identifier, db)

    if not db_user or not await verify_password(data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user account")

    token = await create_access_token(data={"sub": str(db_user.id)})

    return token


        