from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from .enums import TicketStatus, TicketPriority

class TicketCreate(BaseModel):
    title: str = Field(min_length=4, max_length=150)
    description: str = Field(min_length=5)
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=4, max_length=150)
    description: str | None = Field(default=None, min_length=5)


class TicketStatusUpdate(BaseModel):
    status: TicketStatus

    model_config = ConfigDict(extra="forbid")


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
    status: TicketStatus
    priority: TicketPriority
    assigned_agent_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

