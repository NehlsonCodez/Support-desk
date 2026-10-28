from fastapi import APIRouter, Depends, HTTPException, status
from services import get_ticket_activity_service, get_ticket_activities_service
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TicketActivityResponse
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
    return await get_ticket_activities_service(ticket_id=ticket_id, db=db, skip=skip, limit=limit)

@router.get("/{activity_id}", response_model=TicketActivityResponse)
async def get_ticket_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await get_ticket_activity_service(activity_id=activity_id, db=db)