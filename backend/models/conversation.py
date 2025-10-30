"""
Conversation model - Stores chat history and context
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class Conversation(Base):
    """Conversation model for tracking chat sessions"""

    __tablename__ = "conversations"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)

    # Relationships
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)

    # Channel Information
    channel = Column(String(20), default="web")  # web/sms/whatsapp/facebook

    # Conversation Data
    messages = Column(
        JSON, default=list
    )  # [{"role": "user", "content": "...", "timestamp": "..."}]
    qualification_progress = Column(Integer, default=0)  # 0-7 questions answered
    qualification_answers = Column(JSON, default=dict)  # {"age_range": "31-50", ...}
    context = Column(JSON, default=dict)  # Additional context data

    # State Management
    is_qualified = Column(Integer, default=0)  # 0=no, 1=yes
    appointment_booked = Column(Integer, default=0)  # 0=no, 1=yes

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Conversation(session_id={self.session_id}, channel={self.channel}, progress={self.qualification_progress})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "lead_id": self.lead_id,
            "channel": self.channel,
            "messages": self.messages,
            "qualification_progress": self.qualification_progress,
            "qualification_answers": self.qualification_answers,
            "context": self.context,
            "is_qualified": bool(self.is_qualified),
            "appointment_booked": bool(self.appointment_booked),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_updated": self.last_updated.isoformat()
            if self.last_updated
            else None,
        }
