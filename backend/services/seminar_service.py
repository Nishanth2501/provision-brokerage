"""
Seminar Service - Event Management
Handles seminars, registrations, and attendance tracking.
"""

from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.seminar import Seminar
from models.seminar_registration import SeminarRegistration
from models.lead import Lead


class SeminarService:
    """Service for managing seminars and registrations."""

    def __init__(self, db: Session):
        self.db = db

    def create_seminar(
        self,
        title: str,
        description: str,
        topic: str,
        date: datetime,
        duration: int = 60,
        location_type: str = "virtual",
        location_details: Optional[str] = None,
        capacity: int = 50,
        status: str = "scheduled",
    ) -> Seminar:
        """
        Create a new seminar.

        Args:
            title: Seminar title
            description: Full description
            topic: Topic category
            date: Seminar date/time
            duration: Duration in minutes (default 60)
            location_type: virtual, physical, or hybrid
            location_details: Location info (Zoom link, address, etc.)
            capacity: Maximum attendees
            status: scheduled, completed, cancelled

        Returns:
            Seminar: Created seminar
        """
        seminar = Seminar(
            title=title,
            description=description,
            topic=topic,
            date=date,
            duration=duration,
            location_type=location_type,
            location_details=location_details,
            capacity=capacity,
            registered_count=0,
            status=status,
        )

        self.db.add(seminar)
        self.db.commit()
        self.db.refresh(seminar)

        return seminar

    def get_seminar(self, seminar_id: int) -> Optional[Seminar]:
        """Get seminar by ID."""
        return self.db.query(Seminar).filter(Seminar.id == seminar_id).first()

    def list_upcoming_seminars(
        self, limit: int = 10, topic: Optional[str] = None
    ) -> List[Seminar]:
        """
        List upcoming seminars.

        Args:
            limit: Maximum results
            topic: Optional topic filter

        Returns:
            List of upcoming seminars
        """
        query = self.db.query(Seminar).filter(
            and_(Seminar.date >= datetime.utcnow(), Seminar.status.in_(["scheduled", "upcoming"]))
        )

        if topic:
            query = query.filter(Seminar.topic == topic)

        return query.order_by(Seminar.date).limit(limit).all()

    def register_attendee(
        self,
        seminar_id: int,
        lead_id: Optional[int] = None,
        guest_name: Optional[str] = None,
        guest_email: Optional[str] = None,
        guest_phone: Optional[str] = None,
        reminder_preference: str = "email",
    ) -> SeminarRegistration:
        """
        Register attendee for seminar.

        Args:
            seminar_id: Seminar ID
            lead_id: Optional lead ID (for existing leads)
            guest_name: Guest name (required if no lead_id)
            guest_email: Guest email (required if no lead_id)
            guest_phone: Optional phone
            reminder_preference: sms, whatsapp, email, all

        Returns:
            SeminarRegistration: Registration record
        """
        # Get seminar
        seminar = self.get_seminar(seminar_id)
        if not seminar:
            raise ValueError(f"Seminar {seminar_id} not found")

        # Check capacity
        if seminar.is_full:
            raise ValueError(f"Seminar is full (capacity: {seminar.capacity})")

        # Validate registration data
        if not lead_id and (not guest_name or not guest_email):
            raise ValueError("Must provide either lead_id or guest name/email")

        # Check for duplicate registration
        existing = (
            self.db.query(SeminarRegistration)
            .filter(
                and_(
                    SeminarRegistration.seminar_id == seminar_id,
                    or_(
                        SeminarRegistration.lead_id == lead_id if lead_id else False,
                        SeminarRegistration.guest_email == guest_email
                        if guest_email
                        else False,
                    ),
                )
            )
            .first()
        )

        if existing:
            raise ValueError("Already registered for this seminar")

        # Create registration
        registration = SeminarRegistration(
            seminar_id=seminar_id,
            lead_id=lead_id,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            reminder_preference=reminder_preference,
            confirmation_sent=False,
            reminder_sent=False,
            attendance_status="registered",
        )

        self.db.add(registration)

        # Update seminar registered count
        seminar.registered_count += 1

        self.db.commit()
        self.db.refresh(registration)

        return registration

    def get_registrations(self, seminar_id: int) -> List[SeminarRegistration]:
        """Get all registrations for a seminar."""
        return (
            self.db.query(SeminarRegistration)
            .filter(SeminarRegistration.seminar_id == seminar_id)
            .all()
        )

    def check_in_attendee(self, registration_id: int) -> SeminarRegistration:
        """
        Check in attendee at seminar.

        Args:
            registration_id: Registration ID

        Returns:
            SeminarRegistration: Updated registration
        """
        registration = (
            self.db.query(SeminarRegistration)
            .filter(SeminarRegistration.id == registration_id)
            .first()
        )

        if not registration:
            raise ValueError(f"Registration {registration_id} not found")

        registration.attendance_status = "attended"
        registration.check_in_time = datetime.utcnow()

        self.db.commit()
        self.db.refresh(registration)

        return registration

    def mark_no_show(self, registration_id: int) -> SeminarRegistration:
        """Mark attendee as no-show."""
        registration = (
            self.db.query(SeminarRegistration)
            .filter(SeminarRegistration.id == registration_id)
            .first()
        )

        if not registration:
            raise ValueError(f"Registration {registration_id} not found")

        registration.attendance_status = "no_show"

        self.db.commit()
        self.db.refresh(registration)

        return registration

    def add_feedback(
        self,
        registration_id: int,
        feedback: str,
        rating: int,
        follow_up_interest: bool = False,
    ) -> SeminarRegistration:
        """
        Add attendee feedback.

        Args:
            registration_id: Registration ID
            feedback: Feedback text
            rating: Rating (1-5)
            follow_up_interest: Whether interested in follow-up

        Returns:
            SeminarRegistration: Updated registration
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        registration = (
            self.db.query(SeminarRegistration)
            .filter(SeminarRegistration.id == registration_id)
            .first()
        )

        if not registration:
            raise ValueError(f"Registration {registration_id} not found")

        registration.feedback = feedback
        registration.rating = rating
        registration.follow_up_interest = follow_up_interest

        self.db.commit()
        self.db.refresh(registration)

        return registration

    def get_follow_up_leads(
        self, seminar_id: Optional[int] = None
    ) -> List[SeminarRegistration]:
        """
        Get attendees interested in follow-up.

        Args:
            seminar_id: Optional seminar ID to filter

        Returns:
            List of registrations with follow-up interest
        """
        query = self.db.query(SeminarRegistration).filter(
            and_(
                SeminarRegistration.attendance_status == "attended",
                SeminarRegistration.follow_up_interest == True,
            )
        )

        if seminar_id:
            query = query.filter(SeminarRegistration.seminar_id == seminar_id)

        return query.all()

    def get_seminar_stats(self, seminar_id: int) -> Dict[str, Any]:
        """
        Get seminar statistics.

        Args:
            seminar_id: Seminar ID

        Returns:
            Dictionary with stats
        """
        seminar = self.get_seminar(seminar_id)
        if not seminar:
            raise ValueError(f"Seminar {seminar_id} not found")

        registrations = self.get_registrations(seminar_id)
        attended = sum(1 for r in registrations if r.attendance_status == "attended")
        no_shows = sum(1 for r in registrations if r.attendance_status == "no_show")
        follow_ups = sum(1 for r in registrations if r.follow_up_interest)

        ratings = [r.rating for r in registrations if r.rating]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0

        return {
            "seminar_id": seminar_id,
            "title": seminar.title,
            "registered": seminar.registered_count,
            "capacity": seminar.capacity,
            "attended": attended,
            "no_shows": no_shows,
            "attendance_rate": round(attended / seminar.registered_count * 100, 1)
            if seminar.registered_count > 0
            else 0,
            "follow_up_leads": follow_ups,
            "average_rating": round(avg_rating, 1),
            "is_full": seminar.is_full,
        }


# Test function
if __name__ == "__main__":
    from core.database import SessionLocal, init_db
    from datetime import datetime, timedelta

    # Initialize database
    init_db()

    # Create test session
    db = SessionLocal()
    service = SeminarService(db)

    # Test: Create seminar
    print("\n1. Creating test seminar...")
    seminar = service.create_seminar(
        title="Retirement Planning Strategies for 2025",
        description="Learn proven strategies to maximize your retirement income",
        topic="retirement_planning",
        date=datetime.utcnow() + timedelta(days=14),
        duration=60,
        location_type="virtual",
        location_details="Zoom link will be sent via email",
        capacity=50,
    )
    print(f" Created seminar: {seminar.title}")
    print(f"   Date: {seminar.date.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Capacity: {seminar.capacity}")

    # Test: Register attendee
    print(f"\n2. Registering attendee...")
    registration = service.register_attendee(
        seminar_id=seminar.id,
        guest_name="Jane Doe",
        guest_email="jane.doe@example.com",
        guest_phone="555-1234",
        reminder_preference="email",
    )
    print(f" Registered: {registration.guest_name}")

    # Test: List upcoming seminars
    print("\n3. Listing upcoming seminars...")
    upcoming = service.list_upcoming_seminars(limit=5)
    print(f" Found {len(upcoming)} upcoming seminars")
    for s in upcoming:
        print(f"   - {s.title} ({s.date.strftime('%Y-%m-%d')})")

    # Test: Get stats
    print(f"\n4. Getting seminar statistics...")
    stats = service.get_seminar_stats(seminar.id)
    print(f" Stats:")
    print(f"   Registered: {stats['registered']}/{stats['capacity']}")
    print(f"   Attended: {stats['attended']}")
    print(f"   Attendance Rate: {stats['attendance_rate']}%")

    print("\n All seminar service tests passed!")

    db.close()
