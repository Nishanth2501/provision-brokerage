"""
Seminar Registration model - Tracks seminar attendees
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class SeminarRegistration(Base):
    """Seminar registration model for RSVP tracking"""

    __tablename__ = "seminar_registrations"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Relationships
    seminar_id = Column(Integer, ForeignKey("seminars.id"), nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)

    # Guest Information
    guest_name = Column(String(200), nullable=False)
    guest_email = Column(String(200), nullable=False)
    guest_phone = Column(String(20), nullable=True)

    # Registration Details
    registration_date = Column(DateTime(timezone=True), server_default=func.now())

    # Communication Preferences
    reminder_preference = Column(String(20), default="email")  # sms/whatsapp/email/all
    confirmation_sent = Column(Integer, default=0)  # 0=no, 1=yes
    reminder_sent = Column(Integer, default=0)  # 0=no, 1=yes

    # Attendance
    attendance_status = Column(
        String(20), default="registered"
    )  # registered/attended/no-show/cancelled
    check_in_time = Column(DateTime(timezone=True), nullable=True)

    # Feedback
    feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 stars

    # Follow-up
    follow_up_interest = Column(String(20), nullable=True)  # high/medium/low

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<SeminarRegistration(id={self.id}, seminar_id={self.seminar_id}, guest={self.guest_name})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "seminar_id": self.seminar_id,
            "lead_id": self.lead_id,
            "guest_name": self.guest_name,
            "guest_email": self.guest_email,
            "guest_phone": self.guest_phone,
            "registration_date": self.registration_date.isoformat()
            if self.registration_date
            else None,
            "reminder_preference": self.reminder_preference,
            "confirmation_sent": bool(self.confirmation_sent),
            "reminder_sent": bool(self.reminder_sent),
            "attendance_status": self.attendance_status,
            "check_in_time": self.check_in_time.isoformat()
            if self.check_in_time
            else None,
            "feedback": self.feedback,
            "rating": self.rating,
            "follow_up_interest": self.follow_up_interest,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
