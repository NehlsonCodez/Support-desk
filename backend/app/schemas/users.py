from pydantic import BaseModel, EmailStr, ConfigDict
from .enums import UserRole
class BaseUser(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(BaseUser):
    hashed_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)

