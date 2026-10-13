from pydantic import BaseModel, EmailStr, ConfigDict
from .enums import TicketStatus, TicketPriority

class CreateTicket(BaseModel):
    title: str
    description: str
    status: TicketStatus