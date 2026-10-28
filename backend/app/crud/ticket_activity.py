from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import TicketActivities


async def create_ticket_activity(
    db: AsyncSession,
    ticket_id: int,
    actor_id: int,
    action: str,
    old_value: str | None = None,
    new_value: str | None = None,
):
    ticket_activity = TicketActivities(
        ticket_id=ticket_id,
        actor_id=actor_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
    )

    db.add(ticket_activity)
    
    try:
        await db.commit()
        await db.refresh(ticket_activity)
    except Exception:
        await db.rollback()
        raise

    return ticket_activity

async def get_ticket_activities(ticket_id:int, db:AsyncSession, skip:int=0, limit:int=50):
    result = await db.execute(select(TicketActivities).
                            where(TicketActivities.ticket_id==ticket_id).
                            order_by(TicketActivities.created_at.desc()).
                            offset(skip).limit(limit))

    ticket_activities = result.scalars().all()

    return ticket_activities

async def get_ticket_activity_by_id(activity_id:int, db:AsyncSession):
    result = await db.execute(select(TicketActivities).where(TicketActivities.id == activity_id))

    ticket_activity = result.scalar_one_or_none()

    return ticket_activity