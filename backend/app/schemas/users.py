from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from .enums import UserRole

class BaseUser(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr


class UserCreate(BaseUser):
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None


class UserRoleUpdate(BaseModel):
    role: UserRole

    model_config = ConfigDict(extra="forbid")


class PasswordUpdate(BaseModel):
    password: str 
    new_password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseUser):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

