from crud import get_user_by_id
from core import settings
from database import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError



from schemas import UserRole

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token:str=Depends(oauth2_scheme), db:AsyncSession=Depends(get_db)):
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        subject = payload.get("sub")
        if subject is None:
            raise credential_exceptions
        user_id = int(subject)
    except (JWTError, ValueError):
        raise credential_exceptions

    user = await get_user_by_id(user_id, db)
    if user is None:
        raise credential_exceptions

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    return user

async def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user

async def require_agent_or_admin(current_user=Depends(get_current_user)):
    if current_user.role not in (UserRole.ADMIN, UserRole.AGENT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent or Admin privileges required",
        )
    return current_user
