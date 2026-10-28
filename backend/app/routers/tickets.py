from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, APIRouter
from schemas import TicketCreate, TicketUpdate, TicketResponse, TicketStatus, TicketPriorityUpdate, UserRole, TicketAssignment
from services import create_ticket_service, update_ticket_priority_service, update_ticket_service, update_ticket_status_service, get_tickets_service, get_customer_tickets_service, get_assigned_tickets_service, get_ticket_service, assign_ticket_service
from dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/ticket", tags=["Tickets"])

@router.post("/create-ticket", response_model=TicketResponse)
async def create_ticket(customer_id:int, data:TicketCreate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in (UserRole.CUSTOMER, UserRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not permitted to perform this operation")

    if current_user.id != customer_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you cannot create ticket for another customer")

    return await create_ticket_service(db, customer_id, data)

@router.get("/get-tickets", response_model=list[TicketResponse])
async def get_tickets(skip:int=0, limit:int=50, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    return await get_tickets_service(db, skip, limit)

@router.get("/get-ticket", response_model=TicketResponse)
async def get_ticket(ticket_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    return await get_ticket_service(ticket_id, db)

@router.get("/get-customer-tickets", response_model=list[TicketResponse])
async def get_customer_tickets(customer_id:int, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    return await get_customer_tickets_service(customer_id, db)

@router.get("/get-assigned-tickets", response_model=list[TicketResponse])
async def get_assigned_tickets(agent_id, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in (UserRole.ADMIN, UserRole.AGENT):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not permmited to access this route")

    return await get_assigned_tickets_service(agent_id, db)

@router.patch("/update-ticket", response_model=TicketResponse)
async def update_ticket(ticket_id:int, data:TicketUpdate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    
    if current_user.role not in (UserRole.ADMIN, UserRole.CUSTOMER):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not permitted to update this ticket")
    
    update_data = data.model_dump(exclude_unset=True)

    return await update_ticket_service(ticket_id, db, update_data, current_user.id)


@router.patch("/update-ticket-priority", response_model=TicketResponse)
async def update_ticket_priority(ticket_id:int, data:TicketPriorityUpdate, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not permitted to update this priority")

    return await update_ticket_priority_service(ticket_id, db, data, current_user.id)

@router.patch("/update-ticket-status", response_model=TicketResponse)
async def update_ticket_status(ticket_id:int, ticket_status:TicketStatus, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not permitted to update this status")

    return await update_ticket_status_service(ticket_id, db, ticket_status, current_user.id)


@router.patch("/assign-ticket", response_model=TicketResponse)
async def assign_ticket(ticket_id:int, data:TicketAssignment, db:AsyncSession=Depends(get_db), current_user=Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not permitted to assign this ticket")

    return await assign_ticket_service(ticket_id, data, db, current_user.id)