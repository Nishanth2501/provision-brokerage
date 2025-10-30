"""
Lead Service - Lead Management and Scoring
Handles database operations for leads, scoring, and search/filtering.
"""

from typing import Optional, Dict, List, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.lead import Lead
from services.qualification_service import QualificationService


class LeadService:
    """Service for managing leads and qualification scoring."""

    def __init__(self, db: Session):
        self.db = db
        self.qualification_service = QualificationService()

    def create_lead(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        source: str = "web_chat",
        utm_params: Optional[Dict[str, str]] = None,
        qualification_answers: Optional[Dict[str, Any]] = None,
    ) -> Lead:
        """
        Create a new lead.

        Args:
            name: Lead's name
            email: Lead's email (must be unique)
            phone: Optional phone number
            source: Lead source (web_chat, facebook, seminar, etc.)
            utm_params: Optional UTM tracking parameters
            qualification_answers: Optional qualification data

        Returns:
            Lead: Created lead object
        """
        # Check if lead already exists
        existing = self.get_lead_by_email(email)
        if existing:
            # Update existing lead instead
            return self.update_lead(
                existing.id,
                name=name,
                phone=phone,
                qualification_answers=qualification_answers,
            )

        # Extract qualification data if provided
        lead_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "source": source,
            "utm_params": utm_params or {},
            "lead_score": 0,
            "qualification_status": "Cold",
        }

        if qualification_answers:
            # Extract individual fields
            lead_data.update(
                {
                    "state": qualification_answers.get("state"),
                    "age_range": qualification_answers.get("age_range"),
                    "retirement_timeline": qualification_answers.get(
                        "retirement_timeline"
                    ),
                    "investable_assets": qualification_answers.get("investable_assets"),
                    "current_annuity": qualification_answers.get("current_annuity"),
                    "concerns": qualification_answers.get("concerns"),
                    "goals": qualification_answers.get("goals"),
                }
            )

            # Calculate score
            score = self.qualification_service.calculate_score(qualification_answers)
            classification = self.qualification_service.classify_lead(score)

            lead_data["lead_score"] = score
            lead_data["qualification_status"] = classification

        lead = Lead(**lead_data)

        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)

        return lead

    def get_lead(self, lead_id: int) -> Optional[Lead]:
        """
        Get lead by ID.

        Args:
            lead_id: Lead ID

        Returns:
            Lead or None if not found
        """
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def get_lead_by_email(self, email: str) -> Optional[Lead]:
        """
        Get lead by email.

        Args:
            email: Email address

        Returns:
            Lead or None if not found
        """
        return self.db.query(Lead).filter(Lead.email == email).first()

    def update_lead(
        self,
        lead_id: int,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        qualification_answers: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Lead:
        """
        Update lead information.

        Args:
            lead_id: Lead ID
            name: Optional updated name
            phone: Optional updated phone
            qualification_answers: Optional qualification data to update
            **kwargs: Other fields to update

        Returns:
            Lead: Updated lead
        """
        lead = self.get_lead(lead_id)

        if not lead:
            raise ValueError(f"Lead {lead_id} not found")

        # Update basic fields
        if name:
            lead.name = name
        if phone:
            lead.phone = phone

        # Update qualification data
        if qualification_answers:
            lead.state = qualification_answers.get("state", lead.state)
            lead.age_range = qualification_answers.get("age_range", lead.age_range)
            lead.retirement_timeline = qualification_answers.get(
                "retirement_timeline", lead.retirement_timeline
            )
            lead.investable_assets = qualification_answers.get(
                "investable_assets", lead.investable_assets
            )
            lead.current_annuity = qualification_answers.get(
                "current_annuity", lead.current_annuity
            )
            lead.concerns = qualification_answers.get("concerns", lead.concerns)
            lead.goals = qualification_answers.get("goals", lead.goals)

            # Recalculate score
            score = self.calculate_lead_score(lead)
            classification = self.qualification_service.classify_lead(score)

            lead.lead_score = score
            lead.qualification_status = classification

        # Update any other fields
        for key, value in kwargs.items():
            if hasattr(lead, key) and value is not None:
                setattr(lead, key, value)

        lead.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(lead)

        return lead

    def calculate_lead_score(self, lead: Lead) -> int:
        """
        Calculate lead score from lead data.

        Args:
            lead: Lead object

        Returns:
            int: Score (0-100)
        """
        # Build answers dict from lead
        answers = {}

        if lead.age_range:
            answers["age_range"] = lead.age_range
        if lead.retirement_timeline:
            answers["retirement_timeline"] = lead.retirement_timeline
        if lead.investable_assets:
            answers["investable_assets"] = lead.investable_assets
        if lead.current_annuity:
            answers["current_annuity"] = lead.current_annuity
        if lead.concerns:
            answers["concerns"] = lead.concerns
        if lead.goals:
            answers["goals"] = lead.goals

        return self.qualification_service.calculate_score(answers)

    def search_leads(
        self,
        query: Optional[str] = None,
        qualification_status: Optional[str] = None,
        source: Optional[str] = None,
        min_score: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Lead]:
        """
        Search and filter leads.

        Args:
            query: Optional search query (name or email)
            qualification_status: Optional status filter (High Value, Qualified, Warm, Cold)
            source: Optional source filter
            min_score: Optional minimum score filter
            limit: Maximum results to return
            offset: Pagination offset

        Returns:
            List of leads
        """
        db_query = self.db.query(Lead)

        # Text search
        if query:
            db_query = db_query.filter(
                or_(Lead.name.ilike(f"%{query}%"), Lead.email.ilike(f"%{query}%"))
            )

        # Status filter
        if qualification_status:
            db_query = db_query.filter(
                Lead.qualification_status == qualification_status
            )

        # Source filter
        if source:
            db_query = db_query.filter(Lead.source == source)

        # Score filter
        if min_score is not None:
            db_query = db_query.filter(Lead.lead_score >= min_score)

        # Order by score and date
        db_query = db_query.order_by(desc(Lead.lead_score), desc(Lead.created_at))

        return db_query.limit(limit).offset(offset).all()

    def get_high_value_leads(self, limit: int = 20) -> List[Lead]:
        """
        Get high value leads (score >= 80).

        Args:
            limit: Maximum results

        Returns:
            List of high value leads
        """
        return self.search_leads(min_score=80, limit=limit)

    def get_qualified_leads(self, limit: int = 50) -> List[Lead]:
        """
        Get qualified leads (score >= 60).

        Args:
            limit: Maximum results

        Returns:
            List of qualified leads
        """
        return self.search_leads(min_score=60, limit=limit)

    def get_recent_leads(self, days: int = 7, limit: int = 50) -> List[Lead]:
        """
        Get recent leads from past N days.

        Args:
            days: Number of days to look back
            limit: Maximum results

        Returns:
            List of recent leads
        """
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        return (
            self.db.query(Lead)
            .filter(Lead.created_at >= cutoff_date)
            .order_by(desc(Lead.created_at))
            .limit(limit)
            .all()
        )

    def get_lead_stats(self) -> Dict[str, Any]:
        """
        Get lead statistics.

        Returns:
            Dictionary with lead counts by status
        """
        total = self.db.query(Lead).count()
        high_value = (
            self.db.query(Lead)
            .filter(Lead.qualification_status == "High Value")
            .count()
        )
        qualified = (
            self.db.query(Lead).filter(Lead.qualification_status == "Qualified").count()
        )
        warm = self.db.query(Lead).filter(Lead.qualification_status == "Warm").count()
        cold = self.db.query(Lead).filter(Lead.qualification_status == "Cold").count()

        return {
            "total": total,
            "high_value": high_value,
            "qualified": qualified,
            "warm": warm,
            "cold": cold,
            "conversion_rate": round((high_value + qualified) / total * 100, 1)
            if total > 0
            else 0,
        }


# Test function
if __name__ == "__main__":
    from core.database import SessionLocal, init_db

    # Initialize database
    init_db()

    # Create test session
    db = SessionLocal()
    service = LeadService(db)

    # Test: Create lead
    print("\n1. Creating test lead...")
    lead = service.create_lead(
        name="John Smith",
        email="john.smith@example.com",
        phone="555-0123",
        source="web_chat",
        qualification_answers={
            "age_range": "50-59",
            "retirement_timeline": "5-10 years",
            "state": "FL",
            "investable_assets": "$250,000-$500,000",
            "current_annuity": "Yes - looking to review",
            "concerns": "Worried about market volatility",
            "goals": "Secure guaranteed income",
        },
    )
    print(
        f" Created lead: {lead.name} (Score: {lead.lead_score}, Status: {lead.qualification_status})"
    )

    # Test: Get lead
    print(f"\n2. Retrieving lead by ID {lead.id}...")
    retrieved = service.get_lead(lead.id)
    print(f" Retrieved: {retrieved.name} ({retrieved.email})")

    # Test: Update lead
    print("\n3. Updating lead...")
    updated = service.update_lead(
        lead.id,
        phone="555-9999",
        qualification_answers={
            **lead.to_dict(),
            "investable_assets": "$500,000-$1,000,000",
        },
    )
    print(
        f" Updated score: {updated.lead_score} (Status: {updated.qualification_status})"
    )

    # Test: Search leads
    print("\n4. Searching leads...")
    results = service.search_leads(query="John", min_score=60)
    print(f" Found {len(results)} leads")

    # Test: Get stats
    print("\n5. Getting lead statistics...")
    stats = service.get_lead_stats()
    print(
        f" Stats: {stats['total']} total, {stats['high_value']} high value, {stats['qualified']} qualified"
    )

    print("\n All lead service tests passed!")

    db.close()
