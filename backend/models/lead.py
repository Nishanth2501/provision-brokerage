"""
Lead model - Stores lead information and qualification data
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from core.database import Base


class Lead(Base):
    """Lead model for tracking prospects"""

    __tablename__ = "leads"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String(200), nullable=True)
    email = Column(String(200), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    state = Column(String(50), nullable=True)

    # Qualification Data
    age_range = Column(String(20), nullable=True)  # "20-30", "31-50", "51-65", "65+"
    retirement_timeline = Column(
        String(20), nullable=True
    )  # "1-5", "6-10", "11-15", "15+"
    investable_assets = Column(
        String(50), nullable=True
    )  # "<100k", "100-500k", "500k-1M", "1M+"
    current_annuity = Column(String(20), nullable=True)  # "Yes", "No", "Unsure"
    concerns = Column(Text, nullable=True)  # "Income", "Growth", "Legacy", "Taxes"
    goals = Column(Text, nullable=True)  # "Travel", "Family", "Business", "Charity"

    # Scoring
    lead_score = Column(Float, default=0.0)  # 0-100
    qualification_status = Column(
        String(20), default="Cold"
    )  # High/Qualified/Warm/Cold

    # Source Tracking
    source = Column(String(50), default="website")  # website/facebook/seminar/direct
    utm_params = Column(
        JSON, nullable=True
    )  # {"utm_source": "...", "utm_campaign": "..."}

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Lead(id={self.id}, email={self.email}, score={self.lead_score}, status={self.qualification_status})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "state": self.state,
            "age_range": self.age_range,
            "retirement_timeline": self.retirement_timeline,
            "investable_assets": self.investable_assets,
            "current_annuity": self.current_annuity,
            "concerns": self.concerns,
            "goals": self.goals,
            "lead_score": self.lead_score,
            "qualification_status": self.qualification_status,
            "source": self.source,
            "utm_params": self.utm_params,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
