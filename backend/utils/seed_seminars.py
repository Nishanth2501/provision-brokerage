"""
Seed Seminar Data - Populate database with sample seminars
Run this script to add synthetic/test seminar data
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import datetime, timedelta
from core.database import SessionLocal, init_db
from models.seminar import Seminar
from knowledge.seminar_topics import SEMINAR_TOPICS


def create_sample_seminars():
    """Create sample seminars for the next 3 months"""
    db = SessionLocal()

    try:
        # Clear existing seminars (optional - comment out if you want to keep existing)
        print("Clearing existing seminars...")
        db.query(Seminar).delete()
        db.commit()

        print("\n Seeding seminar data...")

        # Define seminar schedule (next 3 months, various dates)
        seminar_schedule = [
            {
                "topic_key": "retirement_planning_strategies",
                "date_offset": 5,  # 5 days from now
                "time": "18:00",  # 6 PM
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/123456789",
                "capacity": 50,
            },
            {
                "topic_key": "understanding_annuities",
                "date_offset": 12,  # 12 days from now
                "time": "19:00",  # 7 PM
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/987654321",
                "capacity": 40,
            },
            {
                "topic_key": "social_security_maximization",
                "date_offset": 18,
                "time": "18:30",
                "location_type": "hybrid",
                "location_details": "In-person: 123 Main St, Suite 200, Anytown, USA | Zoom: https://zoom.us/j/555555555",
                "capacity": 60,
            },
            {
                "topic_key": "tax_efficient_retirement",
                "date_offset": 25,
                "time": "18:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/111222333",
                "capacity": 45,
            },
            {
                "topic_key": "medicare_healthcare_costs",
                "date_offset": 32,
                "time": "19:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/444555666",
                "capacity": 50,
            },
            {
                "topic_key": "estate_planning_basics",
                "date_offset": 40,
                "time": "18:30",
                "location_type": "physical",
                "location_details": "ProVision Brokerage Office, 456 Financial Ave, Suite 500, Anytown, USA 12345",
                "capacity": 30,
            },
            {
                "topic_key": "market_volatility_protection",
                "date_offset": 47,
                "time": "18:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/777888999",
                "capacity": 55,
            },
            {
                "topic_key": "women_and_retirement",
                "date_offset": 54,
                "time": "19:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/123123123",
                "capacity": 40,
            },
            # Add some with existing registrations
            {
                "topic_key": "retirement_planning_strategies",
                "date_offset": 61,
                "time": "18:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/456456456",
                "capacity": 50,
                "registered_count": 15,  # Already has registrations
            },
            {
                "topic_key": "understanding_annuities",
                "date_offset": 68,
                "time": "19:00",
                "location_type": "hybrid",
                "location_details": "In-person: 123 Main St | Zoom: https://zoom.us/j/789789789",
                "capacity": 60,
                "registered_count": 28,
            },
            {
                "topic_key": "social_security_maximization",
                "date_offset": 75,
                "time": "18:30",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/321321321",
                "capacity": 40,
                "registered_count": 35,  # Almost full
            },
            {
                "topic_key": "tax_efficient_retirement",
                "date_offset": 82,
                "time": "18:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/654654654",
                "capacity": 45,
                "registered_count": 8,
            },
        ]

        seminars_created = 0

        for schedule_item in seminar_schedule:
            topic_key = schedule_item["topic_key"]
            topic_data = SEMINAR_TOPICS.get(topic_key)

            if not topic_data:
                print(f"  Warning: Topic '{topic_key}' not found in SEMINAR_TOPICS")
                continue

            # Calculate seminar date/time
            date_offset = schedule_item["date_offset"]
            time_str = schedule_item["time"]
            hour, minute = map(int, time_str.split(":"))

            seminar_date = datetime.utcnow() + timedelta(days=date_offset)
            seminar_date = seminar_date.replace(
                hour=hour, minute=minute, second=0, microsecond=0
            )

            # Create seminar
            seminar = Seminar(
                title=topic_data["title"],
                description=topic_data["description"],
                topic=topic_key.replace("_", " ").title(),
                date=seminar_date,
                duration=topic_data.get("duration", 60),
                location_type=schedule_item["location_type"],
                location_details=schedule_item["location_details"],
                capacity=schedule_item["capacity"],
                registered_count=schedule_item.get("registered_count", 0),
                status="upcoming",
            )

            db.add(seminar)
            seminars_created += 1

            # Print progress
            status_emoji = (
                ""
                if seminar.available_seats > 20
                else ("" if seminar.available_seats > 5 else "")
            )
            print(f"{status_emoji} {seminar.title[:50]}")
            print(f"    {seminar_date.strftime('%B %d, %Y at %I:%M %p')}")
            print(f"    {schedule_item['location_type'].upper()}")
            print(
                f"    {seminar.registered_count}/{seminar.capacity} registered ({seminar.available_seats} seats left)"
            )
            print()

        # Commit all seminars
        db.commit()

        print(f"\n Successfully created {seminars_created} sample seminars!")
        print(f" Database now has seminars scheduled over the next 3 months")

        # Print summary
        total_seminars = db.query(Seminar).count()
        upcoming = db.query(Seminar).filter(Seminar.status == "upcoming").count()
        virtual = db.query(Seminar).filter(Seminar.location_type == "virtual").count()
        physical = db.query(Seminar).filter(Seminar.location_type == "physical").count()
        hybrid = db.query(Seminar).filter(Seminar.location_type == "hybrid").count()

        print(f"\n SUMMARY:")
        print(f"   Total Seminars: {total_seminars}")
        print(f"   Upcoming: {upcoming}")
        print(f"   Virtual: {virtual}")
        print(f"   In-Person: {physical}")
        print(f"   Hybrid: {hybrid}")

    except Exception as e:
        print(f" Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_all_seminars():
    """Clear all seminars from database"""
    db = SessionLocal()
    try:
        count = db.query(Seminar).count()
        db.query(Seminar).delete()
        db.commit()
        print(f" Cleared {count} seminars from database")
    except Exception as e:
        print(f" Error clearing seminars: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    # Initialize database first
    print(" Initializing database...")
    init_db()

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_all_seminars()
    else:
        create_sample_seminars()
        print(
            "\n TIP: Run 'python utils/seed_seminars.py --clear' to remove all seminars"
        )
