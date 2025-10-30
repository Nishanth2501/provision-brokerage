"""
Start script for ProVision Brokerage backend
Runs the FastAPI application using uvicorn
"""

import uvicorn
from main import app

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False  # Disable reload in production
    )
