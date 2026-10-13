from email.policy import default
from database.database import Base
from schemas import TicketStatus, TicketPriority
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime, func
from datetime import datetime

class Ticket(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(150), nullable=False)

    description: Mapped[str] = mapped_column(String(255), nullable = False)

    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.OPEN)

    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), default=TicketPriority.MEDIUM)

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    assigned_agent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), indext=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

