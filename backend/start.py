#!/usr/bin/env python3
"""
ProVision Brokerage AI Chatbot Server
Start script for Render deployment
"""

import os
import sys
from main_ui_server import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    host = "0.0.0.0"

    print(f"Starting ProVision Brokerage AI Chatbot on {host}:{port}")
    print("Server is ready to handle requests!")

    app.run(host=host, port=port, debug=False)
