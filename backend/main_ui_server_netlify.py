import json
import os
import traceback
from http.server import BaseHTTPRequestHandler

# Try to import and initialize the chatbot
try:
    from intelligent_chatbot import IntelligentChatbot
    chatbot = IntelligentChatbot()
    chatbot_available = True
except Exception as e:
    print(f"Error initializing chatbot: {e}")
    chatbot_available = False


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        response = {
            "status": "healthy",
            "message": "ProVision Brokerage AI Chatbot is running",
        }
        self.wfile.write(json.dumps(response).encode())
        return

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode("utf-8"))
                message = data.get("message", "")
                session_id = data.get("session_id", "default")
                context = data.get("context", {})

                if not chatbot_available:
                    # Fallback response when chatbot is not available
                    response = {
                        "message": "Welcome to ProVision Brokerage! I'm here to help with retirement planning, annuities, and financial services. How can I assist you today?",
                        "suggestions": [
                            "Tell me about retirement planning",
                            "What are annuities?",
                            "Help me with appointments",
                            "What services do you offer?"
                        ]
                    }
                else:
                    # Get response from chatbot
                    response = chatbot.get_response(message, session_id, context)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                print(f"Error in POST handler: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                error_response = {
                    "message": "Welcome to ProVision Brokerage! I'm here to help with retirement planning, annuities, and financial services. How can I assist you today?",
                    "suggestions": [
                        "Tell me about retirement planning",
                        "What are annuities?",
                        "Help me with appointments",
                        "What services do you offer?"
                    ],
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        return
