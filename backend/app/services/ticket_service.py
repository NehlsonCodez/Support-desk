from fastapi import HTTPException, status
from crud import (
    create_ticket,
    get_ticket_by_id,
    get_assigned_tickets,
    get_customer_tickets,
    get_tickets,
    update_ticket_by_id,
    update_ticket_status,
    update_ticket_prioriy,
    assign_ticket,
    create_ticket_activity,
)
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import TicketCreate, TicketStatusUpdate, TicketPriorityUpdate, TicketUpdate, TicketAssignment, TicketStatus, TicketPriority


async def create_ticket_service(db:AsyncSession, customer_id:int, data:TicketCreate):
    ticket_data = data.model_dump(exclude_unset=True)

    ticket = await create_ticket(db, customer_id, ticket_data)

    status_val = ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status)
    await create_ticket_activity(
        db=db,
        ticket_id=ticket.id,
        actor_id=customer_id,
        action="TICKET_CREATED",
        new_value=status_val,
    )

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

async def update_ticket_service(ticket_id:int, db:AsyncSession, data:TicketUpdate | dict, actor_id:int):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    ticket_data = data.model_dump(exclude_unset=True) if hasattr(data, "model_dump") else data

    updated_ticket = await update_ticket_by_id(ticket_id, db, ticket_data)

    changed_fields = list(ticket_data.keys()) if isinstance(ticket_data, dict) else []
    if changed_fields:
        await create_ticket_activity(
            db=db,
            ticket_id=ticket_id,
            actor_id=actor_id,
            action="TICKET_UPDATED",
            new_value=", ".join(changed_fields),
        )

    return updated_ticket

async def update_ticket_status_service(ticket_id:int, db:AsyncSession, data:TicketStatusUpdate | TicketStatus, actor_id:int):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    new_status = data.status if hasattr(data, "status") else data
    old_status = ticket.status

    updated_status = await update_ticket_status(ticket_id, db, new_status)

    old_val = old_status.value if hasattr(old_status, "value") else str(old_status)
    new_val = new_status.value if hasattr(new_status, "value") else str(new_status)

    await create_ticket_activity(
        db=db,
        ticket_id=ticket_id,
        actor_id=actor_id,
        action="STATUS_CHANGED",
        old_value=old_val,
        new_value=new_val,
    )

    return updated_status

async def update_ticket_priority_service(ticket_id:int, db:AsyncSession, data:TicketPriorityUpdate | TicketPriority, actor_id:int):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    new_priority = data.priority if hasattr(data, "priority") else data
    old_priority = ticket.priority

    updated_priority = await update_ticket_prioriy(ticket_id, db, new_priority)

    old_val = old_priority.value if hasattr(old_priority, "value") else str(old_priority)
    new_val = new_priority.value if hasattr(new_priority, "value") else str(new_priority)

    await create_ticket_activity(
        db=db,
        ticket_id=ticket_id,
        actor_id=actor_id,
        action="PRIORITY_CHANGED",
        old_value=old_val,
        new_value=new_val,
    )

    return updated_priority

async def assign_ticket_service(ticket_id:int, data:TicketAssignment, db:AsyncSession, actor_id:int):
    ticket = await get_ticket_by_id(ticket_id, db)

    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")

    old_agent_id = ticket.assigned_agent_id
    new_agent_id = data.assigned_agent_id if hasattr(data, "assigned_agent_id") else (data.get("assigned_agent_id") if isinstance(data, dict) else None)

    assigned_ticket = await assign_ticket(ticket_id, data, db)

    await create_ticket_activity(
        db=db,
        ticket_id=ticket_id,
        actor_id=actor_id,
        action="AGENT_ASSIGNED",
        old_value=str(old_agent_id) if old_agent_id is not None else None,
        new_value=str(new_agent_id),
    )

    return assigned_ticket