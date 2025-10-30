"""
Seminar model - Stores seminar/webinar information
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from core.database import Base


class Seminar(Base):
    """Seminar model for event management"""

    __tablename__ = "seminars"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Seminar Details
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    topic = Column(
        String(100), nullable=True
    )  # "Retirement Planning", "Annuities", etc.

    # Scheduling
    date = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, default=60)  # minutes

    # Location
    location_type = Column(String(20), default="virtual")  # virtual/physical/hybrid
    location_details = Column(Text, nullable=True)  # URL or physical address

    # Capacity
    capacity = Column(Integer, default=50)
    registered_count = Column(Integer, default=0)

    # Status
    status = Column(String(20), default="upcoming")  # upcoming/completed/cancelled

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Seminar(id={self.id}, title={self.title}, date={self.date})>"

    @property
    def is_full(self):
        """Check if seminar is at capacity"""
        return self.registered_count >= self.capacity

    @property
    def available_seats(self):
        """Get number of available seats"""
        return max(0, self.capacity - self.registered_count)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "topic": self.topic,
            "date": self.date.isoformat() if self.date else None,
            "duration": self.duration,
            "location_type": self.location_type,
            "location_details": self.location_details,
            "capacity": self.capacity,
            "registered_count": self.registered_count,
            "available_seats": self.available_seats,
            "is_full": self.is_full,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
