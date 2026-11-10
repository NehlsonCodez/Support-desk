from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.dependencies import get_db, get_current_user, require_admin
from schemas import UserResponse, UserUpdate, PasswordUpdate, UserRole, UserRoleUpdate
from services import (
    get_user_service,
    get_users_service,
    get_users_by_role_service,
    update_user_service,
    update_user_role_service,
    update_user_password_service,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user=Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated_user = await update_user_service(current_user.id, db, data)
    return updated_user


@router.post("/change-password")
async def change_password(
    data: PasswordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await update_user_password_service(current_user.id, db, data)
    return {"detail": "Password updated successfully"}


@router.get("", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    return await get_users_service(db, skip=skip, limit=limit)


@router.get("/role/{role}", response_model=list[UserResponse])
async def list_users_by_role(
    role: UserRole,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Admins and Agents can view users filtered by role (e.g., listing agents)
    if current_user.role not in (UserRole.ADMIN, UserRole.AGENT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to filter users by role",
        )
    return await get_users_by_role_service(role, db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to view other user profiles",
        )

    user = await get_user_service(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin),
):
    updated_user = await update_user_role_service(user_id, db, data.role)
    return updated_user
