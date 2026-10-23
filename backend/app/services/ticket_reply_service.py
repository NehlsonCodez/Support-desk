from fastapi import HTTPException, status
from crud import create_ticket_reply, get_ticket_replies, get_ticket_reply_by_id, update_ticket_reply
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TicketReplyCreate, TicketReplyUpdate

async def create_ticket_reply_service(ticket_id:int,db:AsyncSession, data:TicketReplyCreate):
    
    reply_data = data.model_dump(exclude_unset=True)

    reply = await create_ticket_reply(ticket_id, db, reply_data)

    return reply

async def get_ticket_replies_services(ticket_id:int, db:AsyncSession, skip:int=0, limit:int=50):

    replies = await get_ticket_replies(ticket_id, db, skip, limit)

    return replies

async def get_ticket_reply_service(reply_id:int, db:AsyncSession):

    reply = await get_ticket_reply_by_id(reply_id, db)

    if reply is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="reply not found")

    return reply

async def update_ticket_reply_service(reply_id, db:AsyncSession, data:TicketReplyUpdate):
    
    update_data = data.model_dump(exclude_unset=True)

    updated_reply = await update_ticket_reply(reply_id, db, update_data)

    return updated_reply