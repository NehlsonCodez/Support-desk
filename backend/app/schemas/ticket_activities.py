from pydantic import BaseModel, ConfigDict
from datetime import datetime

#TICKET ACTIVITIES SCHEMA

class TicketActivityResponse(BaseModel):
    id: int
    ticket_id: int
    actor_id: int
    action: str
    old_value: str
    new_value: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)