import json

def handler(event, context):
    try:
        # Handle different HTTP methods
        if event.get('httpMethod') == 'GET':
            response = {
                "status": "healthy",
                "message": "ProVision Brokerage AI Chatbot is running",
            }
        elif event.get('httpMethod') == 'POST':
            # Parse the request body
            body = json.loads(event.get('body', '{}'))
            message = body.get('message', '')
            
            # Simple response for now
            if 'retirement' in message.lower():
                response = {
                    "message": "Great question about retirement! ProVision Brokerage specializes in retirement planning, annuities, and helping you secure your financial future. We offer personalized retirement strategies tailored to your age and goals.",
                    "suggestions": [
                        "Tell me about annuities",
                        "Help me plan for retirement",
                        "What services do you offer?",
                        "Schedule an appointment"
                    ]
                }
            elif 'annuity' in message.lower():
                response = {
                    "message": "Annuities are excellent retirement income tools! ProVision offers various annuity products including fixed, variable, and indexed annuities. We can help you choose the right option for your retirement goals.",
                    "suggestions": [
                        "What types of annuities do you offer?",
                        "How do annuities work?",
                        "Help me with retirement planning",
                        "Schedule a consultation"
                    ]
                }
            elif 'appointment' in message.lower() or 'meeting' in message.lower():
                response = {
                    "message": "I'd be happy to help you schedule an appointment! Our advisors can provide personalized retirement planning advice. What's your preferred time and contact method?",
                    "suggestions": [
                        "Schedule a phone call",
                        "Book an in-person meeting",
                        "Tell me about your services first",
                        "What should I prepare for the meeting?"
                    ]
                }
            else:
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
            response = {
                "message": "Method not allowed",
                "suggestions": ["Use GET or POST methods"]
            }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(response)
        }

    except Exception as e:
        print(f"Error in handler: {e}")
        
        error_response = {
            "message": "Welcome to ProVision Brokerage! I'm here to help with retirement planning, annuities, and financial services. How can I assist you today?",
            "suggestions": [
                "Tell me about retirement planning",
                "What are annuities?",
                "Help me with appointments",
                "What services do you offer?"
            ]
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(error_response)
        }
