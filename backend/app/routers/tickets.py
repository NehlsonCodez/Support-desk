from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, APIRouter
from schemas import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketStatus,
    TicketStatusUpdate,
    TicketPriorityUpdate,
    UserRole,
    TicketAssignment,
)
from services import (
    create_ticket_service,
    update_ticket_priority_service,
    update_ticket_service,
    update_ticket_status_service,
    get_tickets_service,
    get_customer_tickets_service,
    get_assigned_tickets_service,
    get_ticket_service,
    assign_ticket_service,
    delete_ticket_service,
)
from dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/ticket", tags=["Tickets"])

@router.post("/create-ticket", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(data:TicketCreate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers are permitted to create tickets",
        )

    customer_id = current_user.id
    return await create_ticket_service(db, customer_id, data)

@router.get("/get-tickets", response_model=list[TicketResponse])
async def get_tickets(skip:int=0, limit:int=50, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    # Customers only see their own tickets; Admins and Agents see all tickets
    if current_user.role == UserRole.CUSTOMER:
        return await get_customer_tickets_service(current_user.id, db)

    return await get_tickets_service(db, skip, limit)

@router.get("/get-ticket/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    ticket = await get_ticket_service(ticket_id, db)

    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this ticket",
        )

    return ticket

@router.get("/get-customer-tickets/{customer_id}", response_model=list[TicketResponse])
async def get_customer_tickets(customer_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == UserRole.CUSTOMER and current_user.id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view other customer's tickets",
        )

    return await get_customer_tickets_service(customer_id, db)

@router.get("/get-assigned-tickets/{agent_id}", response_model=list[TicketResponse])
async def get_assigned_tickets(agent_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in (UserRole.ADMIN, UserRole.AGENT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to access assigned tickets",
        )

    if current_user.role == UserRole.AGENT and current_user.id != agent_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agents can only view their own assigned tickets",
        )

    return await get_assigned_tickets_service(agent_id, db)

@router.patch("/update-ticket/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id:int, data:TicketUpdate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    ticket = await get_ticket_service(ticket_id, db)

    if current_user.role == UserRole.CUSTOMER:
        if ticket.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this ticket",
            )
        if ticket.status in (TicketStatus.CLOSED, TicketStatus.RESOLVED):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot edit a resolved or closed ticket",
            )
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to update this ticket",
        )
    
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    return await update_ticket_service(ticket_id, db, update_data, current_user.id)

@router.patch("/update-ticket-priority/{ticket_id}", response_model=TicketResponse)
async def update_ticket_priority(ticket_id:int, data:TicketPriorityUpdate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to update ticket priority",
        )

    return await update_ticket_priority_service(ticket_id, db, data, current_user.id)

@router.patch("/update-ticket-status/{ticket_id}", response_model=TicketResponse)
async def update_ticket_status(ticket_id:int, data:TicketStatusUpdate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in (UserRole.ADMIN, UserRole.AGENT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and agents are permitted to update ticket status",
        )

    return await update_ticket_status_service(ticket_id, db, data, current_user.id)

@router.patch("/assign-ticket/{ticket_id}", response_model=TicketResponse)
async def assign_ticket(ticket_id:int, data:TicketAssignment, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to assign tickets",
        )

    return await assign_ticket_service(ticket_id, data, db, current_user.id)

@router.delete("/delete-ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    ticket = await get_ticket_service(ticket_id, db)

    if current_user.role == UserRole.ADMIN:
        pass
    elif current_user.role == UserRole.CUSTOMER and ticket.customer_id == current_user.id and ticket.status == TicketStatus.OPEN:
        pass
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this ticket",
        )

    await delete_ticket_service(ticket_id, db, current_user.id)
    return None