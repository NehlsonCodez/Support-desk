from database.database import Base
from schemas import TicketStatus, TicketPriority
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime, func
from datetime import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(150), nullable=False)

    description: Mapped[str] = mapped_column(String(255), nullable = False)

    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.OPEN)

    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), default=TicketPriority.MEDIUM)

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    assigned_agent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    
    
    customer = relationship("User", back_populates="tickets_created", foreign_keys=[customer_id])

    assigned_agent = relationship("User", back_populates="tickets_assigned", foreign_keys=[assigned_agent_id])

    replies = relationship("TicketReplies", back_populates="ticket")

    activities = relationship("TicketActivities", back_populates="ticket")


class TicketReplies(Base):
    __tablename__ = "ticket_replies"

    id: Mapped[int] = mapped_column(primary_key=True)

    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    message: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    
    
    user = relationship("User", back_populates="replies")

    ticket = relationship("Ticket", back_populates="replies")




class TicketActivities(Base):
    __tablename__ = "ticket_activities"


    id: Mapped[int] = mapped_column(primary_key=True)

    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), index=True)

    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    action: Mapped[str] = mapped_column(String, nullable=False)

    old_value: Mapped[str] = mapped_column(String, nullable=True)

    new_value: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ticket = relationship("Ticket", back_populates="activities")

    actor = relationship("User", back_populates="activities")