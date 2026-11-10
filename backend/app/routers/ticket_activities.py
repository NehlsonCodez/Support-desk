from fastapi import APIRouter, Depends, HTTPException, status
from services import get_ticket_activity_service, get_ticket_activities_service, get_ticket_service
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TicketActivityResponse, UserRole
from dependencies.dependencies import get_current_user, get_db

router = APIRouter(prefix="/ticket-activity", tags=["Ticket-Activity"])

@router.get("/ticket/{ticket_id}", response_model=list[TicketActivityResponse])
async def get_ticket_activities(
    ticket_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    ticket = await get_ticket_service(ticket_id, db)
    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view activity for this ticket",
        )

    return await get_ticket_activities_service(ticket_id=ticket_id, db=db, skip=skip, limit=limit)

@router.get("/{activity_id}", response_model=TicketActivityResponse)
async def get_ticket_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    activity = await get_ticket_activity_service(activity_id=activity_id, db=db)
    ticket = await get_ticket_service(activity.ticket_id, db)

    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this ticket activity",
        )

    return activity