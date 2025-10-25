# ProVision Brokerage Backend

AI-powered financial advisor automation platform backend built with FastAPI.

## Features

- **AI Agent System**: Conversational AI for lead qualification and customer engagement
- **Lead Management**: Lead scoring, qualification, and routing
- **Seminar Management**: Event registration, attendance tracking, and analytics
- **Appointment Booking**: Calendar integration and automated scheduling
- **Analytics Dashboard**: Real-time metrics and reporting
- **Multi-channel Support**: Website, SMS, WhatsApp integration ready

## Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── database.py            # Database configuration
├── models/                # SQLAlchemy database models
│   ├── lead.py
│   ├── seminar.py
│   ├── appointment.py
│   └── conversation.py
├── schemas/               # Pydantic schemas for API
│   ├── chat.py
│   ├── lead.py
│   ├── seminar.py
│   ├── appointment.py
│   └── analytics.py
├── services/              # Business logic services
│   ├── ai_agent.py
│   ├── lead_qualification.py
│   ├── seminar_management.py
│   └── appointment_booking.py
├── api/                   # API endpoints
│   ├── chat.py
│   ├── leads.py
│   ├── seminars.py
│   ├── appointments.py
│   └── analytics.py
└── start.py              # Startup script
```

## Setup

### 1. Environment Setup

```bash
# Activate virtual environment
source ../.venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the backend directory:

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./provision_brokerage.db
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Run the Server

```bash
# Option 1: Using the startup script
python start.py

# Option 2: Direct FastAPI
python main.py

# Option 3: Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Chat API
- `POST /api/chat/message` - Send message to AI agent
- `GET /api/chat/conversation/{session_id}` - Get conversation history
- `GET /api/chat/conversations` - List all conversations
- `POST /api/chat/conversation/{session_id}/reset` - Reset conversation

### Leads API
- `POST /api/leads/` - Create new lead
- `GET /api/leads/{lead_id}` - Get lead by ID
- `GET /api/leads/` - List leads with filtering
- `PUT /api/leads/{lead_id}` - Update lead
- `POST /api/leads/{lead_id}/qualify` - Qualify lead
- `DELETE /api/leads/{lead_id}` - Delete lead

### Seminars API
- `POST /api/seminars/` - Create seminar
- `GET /api/seminars/{seminar_id}` - Get seminar
- `GET /api/seminars/` - List seminars
- `PUT /api/seminars/{seminar_id}` - Update seminar
- `POST /api/seminars/{seminar_id}/register` - Register for seminar
- `GET /api/seminars/{seminar_id}/registrations` - Get registrations
- `POST /api/seminars/{seminar_id}/check-in` - Check in attendee
- `GET /api/seminars/{seminar_id}/attendance` - Get attendance
- `GET /api/seminars/{seminar_id}/stats` - Get seminar statistics

### Appointments API
- `POST /api/appointments/` - Create appointment
- `GET /api/appointments/{appointment_id}` - Get appointment
- `GET /api/appointments/` - List appointments
- `PUT /api/appointments/{appointment_id}` - Update appointment
- `POST /api/appointments/{appointment_id}/cancel` - Cancel appointment
- `POST /api/appointments/{appointment_id}/complete` - Complete appointment
- `GET /api/appointments/available-times` - Get available times
- `POST /api/appointments/{appointment_id}/reminders` - Create reminder
- `POST /api/appointments/{appointment_id}/send-reminders` - Send reminders
- `GET /api/appointments/stats` - Get appointment statistics

### Analytics API
- `GET /api/analytics/overview` - Get analytics overview
- `GET /api/analytics/leads` - Get lead analytics
- `GET /api/analytics/seminars` - Get seminar analytics
- `GET /api/analytics/appointments` - Get appointment analytics
- `GET /api/analytics/conversations` - Get conversation analytics
- `GET /api/analytics/dashboard` - Get complete dashboard data
- `POST /api/analytics/reports` - Generate reports

## Database Models

### Lead
- Basic contact information
- Qualification data (age, assets, concerns, goals)
- Lead scoring and status
- Communication preferences
- Source tracking (UTM parameters)

### Seminar
- Event details (title, date, location)
- Capacity management
- Status tracking
- Marketing attribution

### SeminarRegistration
- Registration details
- Guest information
- Confirmation and reminder status
- Communication consent

### SeminarAttendance
- Check-in tracking
- Engagement scoring
- Feedback collection
- Follow-up interest

### Appointment
- Scheduling details
- Advisor assignment
- Status tracking
- Outcome recording

### Conversation
- Session management
- Channel tracking
- Qualification progress
- Message history

## AI Agent Features

### Qualification Questions
The AI agent asks up to 7 qualification questions:
1. Age range
2. Retirement timeline
3. State of residence
4. Investable assets
5. Current annuity status
6. Primary concerns
7. Retirement goals

### Lead Scoring
- Age scoring (25-30 points)
- Retirement timeline (15-30 points)
- Asset scoring (25-40 points)
- Current annuity status (10-20 points)
- Concerns scoring (15-25 points)
- Goals scoring (10-30 points)

### Qualification Thresholds
- High Value: 80+ points
- Qualified: 60-79 points
- Warm: 40-59 points
- Cold: <40 points

## Demo Data

The system includes demo data for testing:
- Sample leads with various qualification scores
- Demo seminars and registrations
- Sample appointments and conversations
- Analytics data for dashboard

## Testing

```bash
# Test API endpoints
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test123"}'
```

## Development

### Adding New Features
1. Create database models in `models/`
2. Create Pydantic schemas in `schemas/`
3. Implement business logic in `services/`
4. Create API endpoints in `api/`
5. Update main.py to include new routers

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## Production Deployment

1. Set `DEBUG=False` in environment
2. Use production database (PostgreSQL)
3. Configure proper CORS origins
4. Set up monitoring and logging
5. Use production OpenAI API key
6. Configure external service integrations

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure `OPENAI_API_KEY` is set in environment
   - Check API key is valid and has credits

2. **Database Connection Error**
   - Check `DATABASE_URL` is correct
   - Ensure database file permissions

3. **Import Errors**
   - Ensure virtual environment is activated
   - Check all dependencies are installed

4. **CORS Errors**
   - Update `CORS_ORIGINS` in environment
   - Check frontend URL is included

### Logs
Check logs for detailed error information:
```bash
tail -f logs/app.log
```
