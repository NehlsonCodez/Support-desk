from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import TicketReplies

async def create_ticket_reply(ticket_id:int, db:AsyncSession, data:dict):
    ticket_reply = TicketReplies(**data, ticket_id=ticket_id)

    db.add(ticket_reply)

    try:
        await db.commit()
        await db.refresh(ticket_reply)
    except Exception:
        await db.rollback()
        raise

    return ticket_reply

async def get_ticket_replies(ticket_id:int, db:AsyncSession, skip:int=0, limit:int=50):
    result = await db.execute(select(TicketReplies).
                            where(TicketReplies.ticket_id==ticket_id).
                            order_by(TicketReplies.created_at.desc()).
                            offset(skip).limit(limit))

    ticket_replies = result.scalars().all()

    return ticket_replies

async def get_ticket_reply_by_id(reply_id:int, db:AsyncSession):
    result = await db.execute(select(TicketReplies).where(TicketReplies.id==reply_id))

    ticket_reply = result.scalar_one_or_none()

    return ticket_reply

async def update_ticket_reply(reply_id:int, db:AsyncSession, data:dict):
    result = await db.execute(select(TicketReplies).where(TicketReplies.id == reply_id))

    ticket_reply = result.scalar_one_or_none()

    if ticket_reply is None:
        return None

    for key, value in data.items():
        setattr(ticket_reply, key, value)


    try: 
        await db.commit()
        await db.refresh(ticket_reply)
    except Exception:
        await db.rollback()
        raise

    return ticket_reply

