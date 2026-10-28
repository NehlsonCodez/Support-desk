from fastapi import HTTPException, status
from crud import create_ticket_activity, get_ticket_activity_by_id, get_ticket_activities
from sqlalchemy.ext.asyncio import AsyncSession

async def create_ticket_activity_service(
    db: AsyncSession,
    ticket_id: int,
    actor_id: int,
    action: str,
    old_value: str | None = None,
    new_value: str | None = None,
):
    ticket_activity = await create_ticket_activity(
        db=db,
        ticket_id=ticket_id,
        actor_id=actor_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
    )

    return ticket_activity

async def get_ticket_activities_service(ticket_id:int, db:AsyncSession, skip:int=0, limit:int=50):

    ticket_activities = await get_ticket_activities(ticket_id, db, skip, limit)

    return ticket_activities

async def get_ticket_activity_service(activity_id:int, db:AsyncSession):
    ticket_activity = await get_ticket_activity_by_id(activity_id, db)

    if ticket_activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket activity not found")

    return ticket_activity
