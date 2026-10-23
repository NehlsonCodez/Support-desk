from jose import jwt, JWTError
from passlib.context import CryptContext
import hashlib
from datetime import datetime, timedelta, timezone
from core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash_password(password:str):
    password = hashlib.sha256(password.encode()).hexdigest()

    return pwd_context.hash(password)

async def verify_password(plain_password:str, hashed_password):
    plain_password = hashlib.sha256(plain_password.encode()).hexdigest()

    return pwd_context.verify(plain_password, hashed_password)


# create access token for an authenticated user
async def create_access_token(data:dict):
    #Copy the data so modifications don't affect the original dictionary
    to_encode = data.copy()

    #Calculate the token's expiration time
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MIN)

    #Add the expiration time to the JWT payload
    to_encode.update({"exp": expire})

    #generate jwt signed token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt