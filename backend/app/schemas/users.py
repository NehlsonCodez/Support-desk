from pydantic import BaseModel, EmailStr, ConfigDict, Field
from .enums import UserRole
class BaseUser(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(BaseUser):
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None

class PasswordUpdate(BaseModel):
    password: str 
    new_password: str = Field(min_length=8)

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)

