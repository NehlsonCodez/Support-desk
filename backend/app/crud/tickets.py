from models import Ticket, TicketActivities, TicketReplies
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from schemas import TicketStatus, TicketPriority

async def create_ticket(db:AsyncSession, customer_id: int, ticket_data: dict):
    new_ticket = Ticket(customer_id=customer_id, **ticket_data)

    db.add(new_ticket)
    try:
        await db.commit()
        await db.refresh(new_ticket)
    except Exception:
        await db.rollback()
        raise

    return new_ticket


async def get_tickets(db:AsyncSession, skip:int=0, limit:int=50):
   result = await db.execute(select(Ticket).offset(skip).limit(limit))

   tickets = result.scalars().all()

   return tickets

async def get_ticket_by_id(ticket_id:int, db:AsyncSession):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))

    ticket = result.scalar_one_or_none()

    return ticket

async def get_customer_tickets(customer_id:int, db: AsyncSession):
    result = await db.execute(select(Ticket).where(Ticket.customer_id==customer_id))

    customer_tickets = result.scalars().all()

    return customer_tickets


async def get_assigned_tickets(agent_id:int, db:AsyncSession):
    result = await db.execute(select(Ticket).where(Ticket.assigned_agent_id==agent_id))

    tickets = result.scalars().all()

    return tickets

async def update_ticket_by_id(ticket_id, db, ticket_data:dict):
    result = await db.execute(select(Ticket).where(Ticket.id==ticket_id))

    ticket = result.scalar_one_or_none()

    if ticket is None:
        return None

    for key, value in ticket_data.items():
        setattr(ticket, key, value)

    try:
        await db.commit()
        await db.refresh(ticket)
    except Exception:
        await db.rollback()
        raise

    return ticket

async def update_ticket_status(ticket_id, db: AsyncSession, status:TicketStatus):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))

    ticket = result.scalar_one_or_none()

    if ticket is None:
        return None

    ticket.status = status

    try:
        await db.commit()
        await db.refresh(ticket)
    except Exception:
        await db.rollback()
        raise

    return ticket
    
async def update_ticket_priority(ticket_id, db:AsyncSession, priority:TicketPriority):
    result=await db.execute(select(Ticket).where(Ticket.id==ticket_id))

    ticket = result.scalar_one_or_none()

    if ticket is None:
        return None

    ticket.priority = priority

    try:
        await db.commit()
        await db.refresh(ticket)
    except Exception:
        await db.rollback()
        raise

    return ticket

update_ticket_prioriy = update_ticket_priority


async def assign_ticket(ticket_id:int, data, db:AsyncSession):
    result = await db.execute(select(Ticket).where(Ticket.id==ticket_id))

    ticket = result.scalar_one_or_none()

    if ticket is None:
        return None

    assigned_agent_id = data.assigned_agent_id if hasattr(data, "assigned_agent_id") else data.get("assigned_agent_id")
    ticket.assigned_agent_id = assigned_agent_id

    try:
        await db.commit()
        await db.refresh(ticket)
    except Exception:
        await db.rollback()
        raise

    return ticket


async def delete_ticket_by_id(ticket_id: int, db: AsyncSession):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if ticket is None:
        return False

    # Explicitly clean up child activities and replies to prevent FK violation
    await db.execute(delete(TicketActivities).where(TicketActivities.ticket_id == ticket_id))
    await db.execute(delete(TicketReplies).where(TicketReplies.ticket_id == ticket_id))

    await db.delete(ticket)
    
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return True

