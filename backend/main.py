"""
ProVision Brokerage - FastAPI Server
Main REST API server with endpoints for chat, leads, appointments, and seminars.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db, init_db
from utils.chatbot import ProVisionChatbot
from services.lead_service import LeadService
from services.seminar_service import SeminarService
from services.conversation_service import ConversationService

# Initialize FastAPI app
app = FastAPI(
    title="ProVision Brokerage API",
    description="AI-powered insurance sales assistant with lead qualification and appointment booking",
    version="2.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Pydantic Models (Request/Response schemas)
# ============================================================================


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str
    session_id: Optional[str] = None
    channel: str = "web"
    user_email: Optional[EmailStr] = None
    user_name: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    session_id: str
    message: str
    qualification_progress: int
    total_questions: int
    is_qualified: bool
    lead_score: int
    next_action: Optional[str] = None
    next_question: Optional[Dict[str, Any]] = None
    booking_url: Optional[str] = None


class BookingRequest(BaseModel):
    """Request model for appointment booking."""

    session_id: str
    name: str
    email: EmailStr
    phone: str
    start_time: datetime
    notes: Optional[str] = None


class SeminarRegistrationRequest(BaseModel):
    """Request model for seminar registration."""

    seminar_id: int
    lead_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_email: Optional[EmailStr] = None
    guest_phone: Optional[str] = None
    reminder_preference: str = "email"


# ============================================================================
# Startup/Shutdown Events
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print(" Database initialized")
    print(f" Server running in {'DEBUG' if settings.DEBUG else 'PRODUCTION'} mode")
    print(f" CORS origins: {settings.cors_origins_list}")


# ============================================================================
# Root & Health Check
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "ProVision Brokerage API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "chat": "POST /api/chat",
            "leads": "GET /api/leads",
            "appointments": "GET /api/appointments",
            "seminars": "GET /api/seminars",
            "analytics": "GET /api/analytics/overview",
        },
        "message": " AI-powered insurance sales assistant is ready!",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "groq_configured": bool(settings.GROQ_API_KEY),
        "calcom_configured": bool(settings.CALCOM_API_KEY),
        "database": "connected",
    }


@app.get("/api/admin/check-database")
async def check_database(db: Session = Depends(get_db)):
    """
    Admin endpoint to check database contents.
    Returns counts of all data in the database.
    """
    try:
        from models.seminar import Seminar
        from models.lead import Lead
        from models.conversation import Conversation
        from models.appointment import Appointment
        from models.seminar_registration import SeminarRegistration
        
        seminar_count = db.query(Seminar).count()
        lead_count = db.query(Lead).count()
        conversation_count = db.query(Conversation).count()
        appointment_count = db.query(Appointment).count()
        registration_count = db.query(SeminarRegistration).count()
        
        # Get seminar details
        seminars = db.query(Seminar).order_by(Seminar.date).all()
        seminar_list = [
            {
                "id": s.id,
                "title": s.title,
                "date": s.date.isoformat() if s.date else None,
                "location_type": s.location_type,
                "registered": s.registered_count,
                "capacity": s.capacity,
                "status": s.status
            }
            for s in seminars
        ]
        
        return {
            "status": "success",
            "database_summary": {
                "seminars": seminar_count,
                "leads": lead_count,
                "conversations": conversation_count,
                "appointments": appointment_count,
                "registrations": registration_count
            },
            "seminars_list": seminar_list,
            "message": f"Found {seminar_count} seminars in database"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking database: {str(e)}")


@app.post("/api/admin/seed-seminars")
async def seed_seminars(db: Session = Depends(get_db)):
    """
    Admin endpoint to seed sample seminars.
    Run this once to populate the database with sample seminar data.
    """
    try:
        from utils.seed_seminars import create_sample_seminars
        
        # Clear and seed
        from models.seminar import Seminar
        db.query(Seminar).delete()
        db.commit()
        
        # Import required modules
        from datetime import timedelta
        from knowledge.seminar_topics import SEMINAR_TOPICS
        
        seminar_schedule = [
            {
                "topic_key": "retirement_planning_strategies",
                "date_offset": 5,
                "time": "18:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/123456789",
                "capacity": 50,
            },
            {
                "topic_key": "understanding_annuities",
                "date_offset": 12,
                "time": "19:00",
                "location_type": "virtual",
                "location_details": "Zoom Meeting Link: https://zoom.us/j/987654321",
                "capacity": 40,
            },
            {
                "topic_key": "social_security_maximization",
                "date_offset": 18,
                "time": "18:30",
                "location_type": "hybrid",
                "location_details": "In-person: 123 Main St | Zoom: https://zoom.us/j/555555555",
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
        ]
        
        from models.seminar import Seminar
        seminars_created = 0
        
        for schedule_item in seminar_schedule:
            topic_key = schedule_item["topic_key"]
            topic_data = SEMINAR_TOPICS.get(topic_key)
            
            if not topic_data:
                continue
            
            # Calculate seminar date/time
            date_offset = schedule_item["date_offset"]
            time_str = schedule_item["time"]
            hour, minute = map(int, time_str.split(":"))
            
            seminar_date = datetime.utcnow() + timedelta(days=date_offset)
            seminar_date = seminar_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
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
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Successfully created {seminars_created} sample seminars",
            "count": seminars_created
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error seeding seminars: {str(e)}")


# ============================================================================
# Chat Endpoints
# ============================================================================


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint - processes user messages and returns AI responses.

    This endpoint:
    - Creates/retrieves conversation sessions
    - Generates AI responses using Groq
    - Tracks lead qualification progress
    - Calculates lead scores
    - Offers appointment booking when qualified
    """
    try:
        # Create chatbot instance
        chatbot = ProVisionChatbot(db)

        # Process message
        response = await chatbot.process_message(
            message=request.message,
            session_id=request.session_id,
            channel=request.channel,
            user_email=request.user_email,
            user_name=request.user_name,
        )

        return ChatResponse(**response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """Get conversation history for a session."""
    try:
        conversation_service = ConversationService(db)
        conversation = conversation_service.get_conversation(session_id)

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return {
            "session_id": conversation.session_id,
            "messages": conversation.messages,
            "qualification_progress": conversation.qualification_progress,
            "is_qualified": conversation.is_qualified,
            "appointment_booked": conversation.appointment_booked,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving history: {str(e)}"
        )


@app.get("/api/chat/summary/{session_id}")
async def get_conversation_summary(session_id: str, db: Session = Depends(get_db)):
    """Get conversation summary with statistics."""
    try:
        chatbot = ProVisionChatbot(db)
        summary = chatbot.get_conversation_summary(session_id)

        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])

        return summary

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting summary: {str(e)}")


# ============================================================================
# Lead Endpoints
# ============================================================================


@app.get("/api/leads")
async def list_leads(
    query: Optional[str] = None,
    qualification_status: Optional[str] = None,
    min_score: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    List and filter leads.

    Query parameters:
    - query: Search by name or email
    - qualification_status: Filter by status (High Value, Qualified, Warm, Cold)
    - min_score: Minimum lead score (0-100)
    - limit: Maximum results (default 50)
    - offset: Pagination offset
    """
    try:
        lead_service = LeadService(db)
        leads = lead_service.search_leads(
            query=query,
            qualification_status=qualification_status,
            min_score=min_score,
            limit=limit,
            offset=offset,
        )

        return {"leads": [lead.to_dict() for lead in leads], "count": len(leads)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing leads: {str(e)}")


@app.get("/api/leads/{lead_id}")
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get lead details by ID."""
    try:
        lead_service = LeadService(db)
        lead = lead_service.get_lead(lead_id)

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        return lead.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting lead: {str(e)}")


@app.get("/api/leads/stats/summary")
async def get_lead_stats(db: Session = Depends(get_db)):
    """Get lead statistics summary."""
    try:
        lead_service = LeadService(db)
        stats = lead_service.get_lead_stats()
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


# ============================================================================
# Appointment Endpoints
# ============================================================================


@app.post("/api/appointments/book")
async def book_appointment(request: BookingRequest, db: Session = Depends(get_db)):
    """Book appointment via Cal.com."""
    try:
        chatbot = ProVisionChatbot(db)
        result = await chatbot.book_appointment(
            session_id=request.session_id,
            name=request.name,
            email=request.email,
            phone=request.phone,
            start_time=request.start_time,
            notes=request.notes,
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail="Booking failed")

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking error: {str(e)}")


@app.get("/api/appointments")
async def list_appointments(
    lead_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List appointments with optional filters."""
    try:
        from models.appointment import Appointment

        query = db.query(Appointment)

        if lead_id:
            query = query.filter(Appointment.lead_id == lead_id)

        if status:
            query = query.filter(Appointment.status == status)

        appointments = query.limit(limit).all()

        return {
            "appointments": [apt.to_dict() for apt in appointments],
            "count": len(appointments),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing appointments: {str(e)}"
        )


# ============================================================================
# Seminar Endpoints
# ============================================================================


@app.get("/api/seminars")
async def list_seminars(
    topic: Optional[str] = None, limit: int = 10, db: Session = Depends(get_db)
):
    """List upcoming seminars."""
    try:
        seminar_service = SeminarService(db)
        seminars = seminar_service.list_upcoming_seminars(limit=limit, topic=topic)

        return {
            "seminars": [seminar.to_dict() for seminar in seminars],
            "count": len(seminars),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing seminars: {str(e)}")


@app.get("/api/seminars/upcoming")
async def list_upcoming_seminars(
    limit: int = 20, db: Session = Depends(get_db)
):
    """List all upcoming seminars (alias for frontend)."""
    try:
        seminar_service = SeminarService(db)
        seminars = seminar_service.list_upcoming_seminars(limit=limit)

        return {
            "seminars": [seminar.to_dict() for seminar in seminars],
            "count": len(seminars),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing seminars: {str(e)}")


@app.get("/api/seminars/{seminar_id}")
async def get_seminar(seminar_id: int, db: Session = Depends(get_db)):
    """Get seminar details."""
    try:
        seminar_service = SeminarService(db)
        seminar = seminar_service.get_seminar(seminar_id)

        if not seminar:
            raise HTTPException(status_code=404, detail="Seminar not found")

        return seminar.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting seminar: {str(e)}")


@app.post("/api/seminars/register")
async def register_for_seminar(
    request: SeminarRegistrationRequest, db: Session = Depends(get_db)
):
    """Register for a seminar."""
    try:
        seminar_service = SeminarService(db)
        registration = seminar_service.register_attendee(
            seminar_id=request.seminar_id,
            lead_id=request.lead_id,
            guest_name=request.guest_name,
            guest_email=request.guest_email,
            guest_phone=request.guest_phone,
            reminder_preference=request.reminder_preference,
        )

        return {
            "success": True,
            "registration_id": registration.id,
            "message": "Successfully registered for seminar",
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")


@app.get("/api/seminars/{seminar_id}/stats")
async def get_seminar_stats(seminar_id: int, db: Session = Depends(get_db)):
    """Get seminar statistics."""
    try:
        seminar_service = SeminarService(db)
        stats = seminar_service.get_seminar_stats(seminar_id)
        return stats

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


# ============================================================================
# Analytics Endpoints
# ============================================================================


@app.get("/api/analytics/overview")
async def get_analytics_overview(db: Session = Depends(get_db)):
    """Get comprehensive analytics overview."""
    try:
        lead_service = LeadService(db)

        # Lead stats
        lead_stats = lead_service.get_lead_stats()

        # Recent leads
        recent_leads = lead_service.get_recent_leads(days=7, limit=10)

        # High value leads
        high_value_leads = lead_service.get_high_value_leads(limit=10)

        return {
            "lead_stats": lead_stats,
            "recent_leads": [lead.to_dict() for lead in recent_leads],
            "high_value_leads": [lead.to_dict() for lead in high_value_leads],
            "generated_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating analytics: {str(e)}"
        )


# ============================================================================
# Run Server (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 70)
    print(" STARTING PROVISION BROKERAGE SERVER")
    print("=" * 70)
    print(f"Environment: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
    print(f"Groq Model: {settings.GROQ_MODEL}")
    print(f"Cal.com Event: {settings.CALCOM_EVENT_TYPE_ID}")
    print(f"Database: {settings.DATABASE_URL}")
    print("=" * 70 + "\n")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
