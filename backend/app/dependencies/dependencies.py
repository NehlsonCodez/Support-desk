from crud import get_user_by_id
from core import settings
from database import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token:str=Depends(oauth2_scheme), db:AsyncSession=Depends(get_db)):
    
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        detail="Could not authenticate candidate",
                                        headers={"WWW-Authenticate": "Bearer"})


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

    return user
