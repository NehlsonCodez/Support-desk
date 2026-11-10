from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.dependencies import get_db, get_current_user
from schemas import TicketReplyCreate, TicketReplyResponse, TicketReplyUpdate, UserRole, TicketStatus
from services import (
    create_ticket_reply_service,
    get_ticket_replies_services,
    get_ticket_reply_service,
    update_ticket_reply_service,
    delete_ticket_reply_service,
    get_ticket_service,
)

router = APIRouter(prefix="/ticket-reply", tags=["Ticket-Reply"])

@router.post("/create-ticket-reply/{ticket_id}", response_model=TicketReplyResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket_reply(ticket_id:int, data:TicketReplyCreate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    ticket = await get_ticket_service(ticket_id, db)

    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to reply to this ticket",
        )

    if ticket.status == TicketStatus.CLOSED and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot reply to a closed ticket",
        )

    new_reply = await create_ticket_reply_service(ticket_id, current_user.id, db, data)
    return new_reply

@router.get("/get-ticket-replies/{ticket_id}", response_model=list[TicketReplyResponse])
async def get_ticket_replies(ticket_id:int, skip:int=0, limit:int=50, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    ticket = await get_ticket_service(ticket_id, db)

    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view replies for this ticket",
        )

    return await get_ticket_replies_services(ticket_id, db, skip, limit)

@router.get("/get-ticket-reply/{reply_id}", response_model=TicketReplyResponse)
async def get_ticket_reply(reply_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    reply = await get_ticket_reply_service(reply_id, db)
    ticket = await get_ticket_service(reply.ticket_id, db)

    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this reply",
        )

    return reply

@router.patch("/update-ticket-reply/{reply_id}", response_model=TicketReplyResponse)
async def update_ticket_reply(reply_id:int, data:TicketReplyUpdate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    reply = await get_ticket_reply_service(reply_id, db)

    if current_user.role != UserRole.ADMIN and reply.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own replies",
        )

    return await update_ticket_reply_service(reply_id, db, data)

@router.delete("/delete-ticket-reply/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket_reply(reply_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    reply = await get_ticket_reply_service(reply_id, db)

    if current_user.role != UserRole.ADMIN and reply.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own replies",
        )

    await delete_ticket_reply_service(reply_id, db)
    return None