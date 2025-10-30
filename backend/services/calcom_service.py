"""
Cal.com Service - Calendar Integration
Handles appointment booking via Cal.com API
"""

import httpx
from datetime import datetime, timedelta
from core.config import settings


class CalComService:
    """Service for Cal.com calendar integration"""

    def __init__(self):
        """Initialize Cal.com service"""
        self.api_key = settings.CALCOM_API_KEY
        self.event_type_id = settings.CALCOM_EVENT_TYPE_ID
        self.username = settings.CALCOM_USERNAME
        self.api_url = settings.CALCOM_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def get_availability(
        self, date_from: datetime = None, date_to: datetime = None
    ) -> dict:
        """
        Get available time slots

        Args:
            date_from: Start date for availability check
            date_to: End date for availability check

        Returns:
            Dict with available slots
        """
        if not date_from:
            date_from = datetime.now()
        if not date_to:
            date_to = date_from + timedelta(days=14)

        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "eventTypeId": self.event_type_id,
                    "startTime": date_from.isoformat(),
                    "endTime": date_to.isoformat(),
                }

                response = await client.get(
                    f"{self.api_url}/availability",
                    headers=self.headers,
                    params=params,
                    timeout=10.0,
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Cal.com availability error: {response.status_code}")
                    return {"available": False, "error": "Could not fetch availability"}

        except Exception as e:
            print(f"Error fetching availability: {e}")
            return {"available": False, "error": str(e)}

    async def create_booking(
        self,
        name: str,
        email: str,
        start_time: datetime,
        notes: str = "",
        phone: str = None,
    ) -> dict:
        """
        Create a booking/appointment

        Args:
            name: Attendee name
            email: Attendee email
            start_time: Appointment start time
            notes: Additional notes
            phone: Attendee phone (optional)

        Returns:
            Booking confirmation dict
        """
        try:
            async with httpx.AsyncClient() as client:
                booking_data = {
                    "eventTypeId": int(self.event_type_id),
                    "start": start_time.isoformat(),
                    "responses": {"name": name, "email": email, "notes": notes},
                    "timeZone": "America/New_York",
                    "language": "en",
                    "metadata": {},
                }

                if phone:
                    booking_data["responses"]["phone"] = phone

                response = await client.post(
                    f"{self.api_url}/bookings",
                    headers=self.headers,
                    json=booking_data,
                    timeout=15.0,
                )

                if response.status_code in [200, 201]:
                    result = response.json()
                    return {
                        "success": True,
                        "booking_id": result.get("id"),
                        "booking_uid": result.get("uid"),
                        "start_time": start_time.isoformat(),
                        "message": "Appointment booked successfully!",
                    }
                else:
                    print(
                        f"Cal.com booking error: {response.status_code} - {response.text}"
                    )
                    return {
                        "success": False,
                        "error": f"Booking failed: {response.status_code}",
                    }

        except Exception as e:
            print(f"Error creating booking: {e}")
            return {"success": False, "error": str(e)}

    def get_booking_url(self) -> str:
        """Get public booking URL"""
        return f"https://cal.com/{self.username}"

    async def test_connection(self) -> bool:
        """Test Cal.com API connection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/me", headers=self.headers, timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Cal.com connection test failed: {e}")
            return False


if __name__ == "__main__":
    import asyncio

    print("Testing Cal.com Service...")
    print("=" * 60)

    service = CalComService()

    # Test connection
    print("\n[1/2] Testing API connection...")
    if asyncio.run(service.test_connection()):
        print(" Connected to Cal.com API successfully")
        print(f"   Event Type ID: {service.event_type_id}")
        print(f"   Username: {service.username}")
    else:
        print(" Connection failed")

    # Test booking URL
    print("\n[2/2] Testing booking URL...")
    url = service.get_booking_url()
    print(f" Public booking URL: {url}")

    print("\n" + "=" * 60)
    print(" Cal.com Service is configured!")
