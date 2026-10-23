from pydantic import BaseModel, ConfigDict
from datetime import datetime

#TICKET ACTIVITIES SCHEMA

class TicketActivityResponse(BaseModel):
    id: int
    ticket_id: int
    actor_id: int
    action: str
    old_value: str | None = None
    new_value: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)