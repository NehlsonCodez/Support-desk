from fastapi import HTTPException, status
from crud import create_ticket, get_ticket_by_id, get_assigned_tickets, get_customer_tickets, get_tickets, update_ticket_by_id, update_ticket_status, update_ticket_prioriy
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TicketCreate, TicketStatusUpdate, TicketPriorityUpdate, TicketStatus, TicketUpdate


async def create_ticket_service(db:AsyncSession,customer_id, data:TicketCreate):
    ticket_data = data.model_dump(exclude_unset=True)

    ticket = await create_ticket(db, customer_id, ticket_data)

    return ticket

async def get_tickets_service(db:AsyncSession, skip:int=0, limit:int=50):
    tickets = await get_tickets(db, skip, limit)

    return tickets

async def get_ticket_service(ticket_id:int, db:AsyncSession):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    return ticket
async def get_assigned_tickets_service(agent_id:int, db:AsyncSession):
    tickets = await get_assigned_tickets(agent_id, db)

    return tickets

async def get_customer_tickets_service(customer_id:int, db:AsyncSession):
    tickets = await get_customer_tickets(customer_id, db)

    return tickets

async def update_ticket_service(ticket_id:int, db:AsyncSession, data:TicketUpdate):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    ticket_data = data.model_dump(exclude_unset=True) 

    updated_ticket = await update_ticket_by_id(ticket_id, db, ticket_data)

    return updated_ticket

async def update_ticket_status_service(ticket_id:int, db:AsyncSession, data:TicketStatusUpdate):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    updated_status = await update_ticket_status(ticket_id, db, data.status)

    return updated_status

async def update_ticket_priority_service(ticket_id:int, db:AsyncSession, data:TicketPriorityUpdate):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    updated_priority = await update_ticket_prioriy(ticket_id, db, data.priority)

    return updated_priority