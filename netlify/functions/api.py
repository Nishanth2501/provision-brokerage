import json
import os
import sys
import traceback

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../backend"))


def handler(event, context):
    try:
        # Try to import and initialize the chatbot
        try:
            from intelligent_chatbot import IntelligentChatbot

            chatbot = IntelligentChatbot()
            chatbot_available = True
        except Exception as e:
            print(f"Error initializing chatbot: {e}")
            chatbot_available = False

        # Handle different HTTP methods
        if event["httpMethod"] == "GET":
            response = {
                "status": "healthy",
                "message": "ProVision Brokerage AI Chatbot is running",
            }
        elif event["httpMethod"] == "POST":
            # Parse the request body
            body = json.loads(event.get("body", "{}"))
            message = body.get("message", "")
            session_id = body.get("session_id", "default")
            context_data = body.get("context", {})

            if not chatbot_available:
                # Fallback response when chatbot is not available
                response = {
                    "message": "Welcome to ProVision Brokerage! I'm here to help with retirement planning, annuities, and financial services. How can I assist you today?",
                    "suggestions": [
                        "Tell me about retirement planning",
                        "What are annuities?",
                        "Help me with appointments",
                        "What services do you offer?",
                    ],
                }
            else:
                # Get response from chatbot
                response = chatbot.get_response(message, session_id, context_data)
        else:
            response = {
                "message": "Method not allowed",
                "suggestions": ["Use GET or POST methods"],
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps(response),
        }

    except Exception as e:
        print(f"Error in handler: {e}")
        print(f"Traceback: {traceback.format_exc()}")

        error_response = {
            "message": "Welcome to ProVision Brokerage! I'm here to help with retirement planning, annuities, and financial services. How can I assist you today?",
            "suggestions": [
                "Tell me about retirement planning",
                "What are annuities?",
                "Help me with appointments",
                "What services do you offer?",
            ],
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(error_response),
        }
