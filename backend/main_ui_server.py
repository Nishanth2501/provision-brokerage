"""
Main UI Server for ProVision Brokerage
Simple chatbot for the main UI tab
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from intelligent_chatbot import IntelligentChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ProVision Brokerage Main UI API",
    description="Simple chatbot for main UI tab",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "*",  # Allow all origins for demo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = IntelligentChatbot()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ProVision Brokerage Main UI API",
        "version": "1.0.0",
        "status": "running",
        "chatbot": "ready",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ProVision Brokerage Chatbot API",
        "version": "1.0.0",
        "chatbot": "ready",
        "type": "simple_chatbot",
    }


@app.post("/api/chat")
async def chat_endpoint(request: dict):
    """Chat endpoint for simple chatbot"""
    try:
        message = request.get("message", "")
        session_id = request.get("session_id", "default")
        context = request.get("context", {})

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Get chatbot response
        response = chatbot.get_response(message, session_id)

        return response

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/test")
async def test_chatbot():
    """Test the chatbot functionality"""
    try:
        test_results = chatbot.test_chatbot()
        return test_results

    except Exception as e:
        logger.error(f"Error testing chatbot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/qualification-questions")
async def get_qualification_questions():
    """Get qualification questions"""
    try:
        questions = chatbot.get_qualification_questions()
        return {"questions": questions}

    except Exception as e:
        logger.error(f"Error getting qualification questions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main_ui_server:app", host="0.0.0.0", port=8001, reload=True, log_level="info"
    )
