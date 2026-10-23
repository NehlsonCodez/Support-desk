from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from .enums import TicketStatus, TicketPriority

class TicketCreate(BaseModel):
    title: str
    description: str
    

class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    
    title: str | None = Field(default=None, min_length=10, max_length=150)

    description: str | None = Field(default=None, min_length=10)


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketAssignment(BaseModel):
    assigned_agent_id: int

    model_config = ConfigDict(extra="forbid")


class TicketPriorityUpdate(BaseModel):
    priority: TicketPriority

    model_config = ConfigDict(extra="forbid")


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    customer_id: int
    status: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



