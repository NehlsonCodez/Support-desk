from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


#TICKET REPLIES SCHEMAS
class TicketReplyCreate(BaseModel):
    message: str = Field(min_length=1, max_length=255)

class TicketReplyUpdate(BaseModel):
    message: str | None = Field(min_length=1, max_length=255)

class TicketReplyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    user_id: int
    message: str
    created_at: datetime
