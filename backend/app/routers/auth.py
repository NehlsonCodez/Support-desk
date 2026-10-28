from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from dependencies.dependencies import get_db
from services import create_user_service, login_user_service
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserResponse, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(data:UserCreate, db:AsyncSession=Depends(get_db)):
    return await create_user_service(db, data)

@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm=Depends(), db:AsyncSession=Depends(get_db)):

    token = await login_user_service(db, form_data)

    return {"access_token":token, "token_type":"bearer"}

    
