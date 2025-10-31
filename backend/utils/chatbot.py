"""
ProVision Brokerage Chatbot - Main Orchestrator
Coordinates all services to create an intelligent AI assistant for insurance sales.
"""

import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime

from sqlalchemy.orm import Session

from core.config import settings
from services.groq_service import GroqService
from services.qualification_service import QualificationService
from services.conversation_service import ConversationService
from services.lead_service import LeadService
from services.calcom_service import CalComService


class ProVisionChatbot:
    """
    Main chatbot orchestrator.

    Coordinates:
    - AI conversation (Groq)
    - Lead qualification (7-question flow)
    - Lead scoring (0-100)
    - Appointment booking (Cal.com)
    - Database persistence
    """

    def __init__(self, db: Session):
        """
        Initialize chatbot with all services.

        Args:
            db: Database session
        """
        self.db = db

        # Initialize services
        self.groq_service = GroqService()
        self.qualification_service = QualificationService()
        self.conversation_service = ConversationService(db)
        self.lead_service = LeadService(db)
        self.calcom_service = CalComService()

        print(" ProVision Chatbot initialized successfully!")

    async def process_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        channel: str = "web",
        user_email: Optional[str] = None,
        user_name: Optional[str] = None,
        page_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process a user message and generate AI response.

        This is the main entry point for the chatbot.

        Args:
            message: User's message
            session_id: Optional session ID (creates new if not provided)
            channel: Communication channel (web, sms, whatsapp, facebook)
            user_email: Optional user email
            user_name: Optional user name
            page_context: Optional page context (seminars, appointments, facebook, etc.)

        Returns:
            Dictionary with response, qualification status, and next actions
        """
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())

        # Get or create conversation
        conversation = self.conversation_service.get_or_create_conversation(
            session_id=session_id, channel=channel
        )

        # Save user message
        self.conversation_service.add_message(
            session_id=session_id, role="user", content=message
        )

        # Get conversation history
        message_history = self.conversation_service.get_message_history(session_id)

        # Build context for AI
        context = self._build_context(conversation, user_email, user_name)
        
        # Add page context if provided
        if page_context:
            context["page"] = page_context

        # Check if we're in qualification flow
        current_progress = conversation.qualification_progress
        qualification_answers = conversation.qualification_answers or {}

        # Extract qualification data from user message if in qualification flow
        if current_progress < 7:
            # Use AI to extract qualification intent (NOT async)
            qualification_intent = self.groq_service.extract_qualification_intent(
                message
            )

            # Get next question
            next_question = self.qualification_service.get_next_question(
                current_progress
            )

            # If AI found an answer, save it
            if qualification_intent and next_question:
                question_field = next_question["field"]

                # Extract answer from AI analysis
                if "answer" in qualification_intent:
                    qualification_answers[question_field] = qualification_intent[
                        "answer"
                    ]
                    current_progress += 1

                    # Update conversation
                    self.conversation_service.update_qualification(
                        session_id=session_id,
                        progress=current_progress,
                        answers=qualification_answers,
                    )

                    # Calculate score if qualification complete
                    if current_progress >= 7:
                        lead_score = self.qualification_service.calculate_score(
                            qualification_answers
                        )
                        is_qualified = (
                            self.qualification_service.should_offer_appointment(
                                lead_score
                            )
                        )

                        # Create or update lead
                        if user_email:
                            lead = self.lead_service.create_lead(
                                name=user_name or "Unknown",
                                email=user_email,
                                source=channel,
                                qualification_answers=qualification_answers,
                            )

                            # Link conversation to lead
                            self.conversation_service.link_to_lead(session_id, lead.id)

                            # Update context
                            context["lead_id"] = lead.id
                            context["lead_score"] = lead_score
                            context["is_qualified"] = is_qualified

        # Generate AI response
        ai_response = self.groq_service.generate_response(
            user_message=message,
            conversation_history=message_history[-10:],  # Last 10 messages for context
            context=context,
        )

        # Save AI response
        self.conversation_service.add_message(
            session_id=session_id, role="assistant", content=ai_response
        )

        # Build response object
        response = {
            "session_id": session_id,
            "message": ai_response,
            "qualification_progress": current_progress,
            "total_questions": 7,
            "is_qualified": context.get("is_qualified", False),
            "lead_score": context.get("lead_score", 0),
            "next_action": None,
        }

        # Determine next action
        if current_progress >= 7 and context.get("is_qualified"):
            response["next_action"] = "offer_appointment"
            response["booking_url"] = self.calcom_service.get_booking_url()
        elif current_progress < 7:
            next_q = self.qualification_service.get_next_question(current_progress)
            if next_q:
                response["next_action"] = "continue_qualification"
                response["next_question"] = next_q

        return response

    def _build_context(
        self,
        conversation,
        user_email: Optional[str] = None,
        user_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build context dictionary for AI.

        Args:
            conversation: Conversation object
            user_email: Optional user email
            user_name: Optional user name

        Returns:
            Context dictionary
        """
        context = {
            "session_id": conversation.session_id,
            "channel": conversation.channel,
            "qualification_progress": conversation.qualification_progress,
            "qualification_answers": conversation.qualification_answers or {},
            "is_qualified": conversation.is_qualified,
            "appointment_booked": conversation.appointment_booked,
        }

        if user_email:
            context["user_email"] = user_email
        if user_name:
            context["user_name"] = user_name

        # Add lead info if linked
        if conversation.lead_id:
            lead = self.lead_service.get_lead(conversation.lead_id)
            if lead:
                context["lead_id"] = lead.id
                context["lead_score"] = lead.lead_score
                context["qualification_status"] = lead.qualification_status

        # Add upcoming seminars info
        try:
            from services.seminar_service import SeminarService
            seminar_service = SeminarService(self.db)
            upcoming_seminars = seminar_service.list_upcoming_seminars(limit=5)
            
            if upcoming_seminars:
                seminars_info = []
                for seminar in upcoming_seminars:
                    seminar_data = {
                        "id": seminar.id,
                        "title": seminar.title,
                        "date": seminar.date.strftime("%B %d, %Y at %I:%M %p") if seminar.date else "TBD",
                        "location_type": seminar.location_type,
                        "available_seats": seminar.available_seats,
                        "is_full": seminar.is_full
                    }
                    seminars_info.append(seminar_data)
                
                context["upcoming_seminars"] = seminars_info
        except Exception as e:
            print(f"Warning: Could not fetch seminars for context: {e}")
            context["upcoming_seminars"] = []

        return context

    async def book_appointment(
        self,
        session_id: str,
        name: str,
        email: str,
        phone: str,
        start_time: datetime,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Book appointment for a lead.

        Args:
            session_id: Session ID
            name: Lead name
            email: Lead email
            phone: Lead phone
            start_time: Appointment start time
            notes: Optional notes

        Returns:
            Booking result
        """
        # Book with Cal.com
        booking_result = await self.calcom_service.create_booking(
            name=name, email=email, start_time=start_time, notes=notes, phone=phone
        )

        if booking_result["success"]:
            # Mark conversation as booked
            self.conversation_service.mark_appointment_booked(session_id)

            # Update lead if exists
            conversation = self.conversation_service.get_conversation(session_id)
            if conversation and conversation.lead_id:
                lead = self.lead_service.get_lead(conversation.lead_id)
                if lead:
                    # Create appointment record in database
                    from models.appointment import Appointment

                    appointment = Appointment(
                        lead_id=lead.id,
                        calcom_booking_id=booking_result.get("booking_id"),
                        scheduled_time=start_time,
                        status="scheduled",
                        source=conversation.channel,
                    )
                    self.db.add(appointment)
                    self.db.commit()

        return booking_result

    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get conversation summary with stats.

        Args:
            session_id: Session ID

        Returns:
            Conversation summary
        """
        conversation = self.conversation_service.get_conversation(session_id)

        if not conversation:
            return {"error": "Conversation not found"}

        summary = {
            "session_id": conversation.session_id,
            "channel": conversation.channel,
            "message_count": len(conversation.messages) if conversation.messages else 0,
            "qualification_progress": f"{conversation.qualification_progress}/7",
            "is_qualified": conversation.is_qualified,
            "appointment_booked": conversation.appointment_booked,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
        }

        # Add lead info if available
        if conversation.lead_id:
            lead = self.lead_service.get_lead(conversation.lead_id)
            if lead:
                summary["lead"] = {
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "score": lead.lead_score,
                    "status": lead.qualification_status,
                }

        return summary


# Test function
if __name__ == "__main__":
    import asyncio
    from core.database import SessionLocal, init_db

    async def test_chatbot():
        """Test chatbot functionality."""
        # Initialize database
        init_db()

        # Create session
        db = SessionLocal()

        # Create chatbot
        print("\n" + "=" * 60)
        print("TESTING PROVISION CHATBOT")
        print("=" * 60)

        chatbot = ProVisionChatbot(db)

        # Test conversation flow
        session_id = str(uuid.uuid4())

        # Message 1: Initial greeting
        print("\n1. Testing initial message...")
        response1 = await chatbot.process_message(
            message="Hi, I'm interested in retirement planning",
            session_id=session_id,
            channel="web",
            user_email="test@example.com",
            user_name="Test User",
        )
        print(f" Bot: {response1['message'][:100]}...")
        print(f"   Progress: {response1['qualification_progress']}/7")

        # Message 2: Answer age question
        print("\n2. Testing qualification answer...")
        response2 = await chatbot.process_message(
            message="I'm 55 years old", session_id=session_id
        )
        print(f" Bot: {response2['message'][:100]}...")
        print(f"   Progress: {response2['qualification_progress']}/7")

        # Get conversation summary
        print("\n3. Getting conversation summary...")
        summary = chatbot.get_conversation_summary(session_id)
        print(f" Summary:")
        print(f"   Messages: {summary['message_count']}")
        print(f"   Progress: {summary['qualification_progress']}")
        print(f"   Qualified: {summary['is_qualified']}")

        print("\n" + "=" * 60)
        print(" ALL CHATBOT TESTS PASSED!")
        print("=" * 60)

        db.close()

    # Run async test
    asyncio.run(test_chatbot())
