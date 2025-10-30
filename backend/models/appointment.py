"""
Appointment model - Stores booking information
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class Appointment(Base):
    """Appointment model for tracking bookings"""

    __tablename__ = "appointments"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Relationships
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)

    # Cal.com Integration
    calcom_event_id = Column(String(100), nullable=True)
    calcom_booking_id = Column(String(100), nullable=True)

    # Appointment Details
    advisor_name = Column(String(200), default="ProVision Advisor")
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, default=15)  # minutes

    # Status
    status = Column(
        String(20), default="scheduled"
    )  # scheduled/completed/cancelled/no-show

    # Source
    source = Column(String(50), default="chat")  # chat/seminar/direct/website

    # Outcome
    outcome = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return (
            f"<Appointment(id={self.id}, lead_id={self.lead_id}, status={self.status})>"
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "calcom_event_id": self.calcom_event_id,
            "calcom_booking_id": self.calcom_booking_id,
            "advisor_name": self.advisor_name,
            "scheduled_time": self.scheduled_time.isoformat()
            if self.scheduled_time
            else None,
            "duration": self.duration,
            "status": self.status,
            "source": self.source,
            "outcome": self.outcome,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
