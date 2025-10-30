"""
ProVision Brokerage Company Information
Inspired by Next Level Advisors
"""

COMPANY_INFO = {
    "name": "ProVision Brokerage",
    "tagline": "AI-Powered Financial Advisor Automation",
    "mission": "Helping financial advisors generate more leads, fill their seminars, and book more appointments through intelligent AI automation",
    "value_proposition": {
        "main": "63% of advisors are missing opportunities due to outdated technology. ProVision Brokerage brings Next Level AI to your practice.",
        "benefits": [
            "Generate more qualified leads automatically",
            "Fill seminars with engaged prospects",
            "Book more high-value appointments",
            "Automate lead qualification and follow-up",
            "Multi-channel engagement (Web, SMS, WhatsApp, Facebook)",
            "24/7 intelligent client support",
        ],
    },
    "services": {
        "seminars": {
            "title": "AI-Powered Seminar Management",
            "description": "Launch high-converting landing pages and automate every RSVP from the moment a guest discovers your seminar.",
            "features": [
                "Responsive registration flows with compliance-ready disclosures",
                "Payment and ticketing options for premium or hybrid events",
                "Automatic calendar invites and nurture reminders",
                "Built-in segmentation to prioritize high-value prospects",
                "Real-time attendance tracking and engagement scoring",
                "Automated follow-up for interested attendees",
            ],
            "workflow": [
                "Pick your audience segment and registration template",
                "Configure reminders across SMS, WhatsApp, and email",
                "Publish the campaign in under five minutes",
                "Monitor real-time registrations and VIP alerts",
            ],
        },
        "appointments": {
            "title": "Smart Appointment Booking",
            "description": "AI-powered qualification and scheduling system that converts prospects into booked consultations.",
            "features": [
                "AI qualification questions before booking",
                "Real-time advisor availability calendar",
                "Automated confirmation and reminder system",
                "Multi-channel reminders (SMS, WhatsApp, Email)",
                "No-show reduction through smart follow-ups",
                "Source-based recommendations",
            ],
            "workflow": [
                "AI qualifies prospect with smart questions",
                "Show available time slots from calendar",
                "Instant booking confirmation",
                "Automated reminders before appointment",
                "Post-appointment follow-up automation",
            ],
        },
        "facebook": {
            "title": "Social Media Lead Capture",
            "description": "Facebook Messenger integration for seamless lead capture and qualification.",
            "features": [
                "Direct message conversations with AI",
                "Lead qualification in Messenger",
                "Quick response templates",
                "Booking escalation prompts",
                "Real-time typing indicators",
                "Message status tracking",
            ],
        },
        "website_leads": {
            "title": "Lead Management Dashboard",
            "description": "Comprehensive lead collection, tracking, and nurturing system with multi-channel integration.",
            "features": [
                "Visitor information capture forms",
                "Chat-driven lead collection",
                "Interest and urgency qualification",
                "Preferred channel selection",
                "Source tracking with UTM parameters",
                "SMS and WhatsApp follow-up automation",
                "Email sequence automation",
                "Lead nurturing workflows",
            ],
        },
        "client_service": {
            "title": "Enhanced Client Support",
            "description": "AI-powered self-service FAQ system with live agent escalation.",
            "features": [
                "Account management self-service",
                "Product information access",
                "Service request handling",
                "Document access and downloads",
                "Search functionality across knowledge base",
                "Live agent escalation when needed",
                "Transparent source citations",
            ],
        },
    },
    "target_audience": {
        "primary": "Financial advisors specializing in retirement planning and annuities",
        "secondary": "Independent insurance agents and wealth management firms",
        "pain_points": [
            "Manual lead qualification taking too much time",
            "Low seminar attendance and no-shows",
            "Difficulty booking qualified appointments",
            "Missing follow-ups due to busy schedule",
            "Lack of 24/7 client support",
            "Inconsistent lead quality from marketing",
        ],
    },
    "competitive_advantages": [
        "AI-powered lead qualification (not generic chatbots)",
        "Multi-channel automation (Web, SMS, WhatsApp, Facebook)",
        "Compliance-ready disclosures and documentation",
        "Real-time analytics and reporting",
        "Easy integration with existing tools (Cal.com, CRM)",
        "Transparent AI with source citations",
        "Purpose-built for financial advisors",
    ],
    "technology": {
        "ai_model": "Advanced language models (Groq/Llama 3.1)",
        "channels": ["Web Chat", "SMS", "WhatsApp", "Facebook Messenger"],
        "integrations": ["Cal.com", "Sinch", "CRM systems"],
        "features": [
            "Natural conversation",
            "Context awareness",
            "Lead scoring",
            "Appointment booking",
        ],
    },
    "statistics": {
        "industry_stat": "63% of advisors are missing opportunities due to outdated technology (Source: Kitces.com)",
        "value_props": [
            "3x more qualified leads through AI qualification",
            "50% reduction in no-shows with automated reminders",
            "24/7 availability without additional staff",
            "60% faster response time to prospects",
        ],
    },
    "demo_features": {
        "available_now": [
            "Web chat with AI agent",
            "Lead qualification system",
            "Appointment booking via Cal.com",
            "Conversation history tracking",
            "Lead scoring (0-100)",
        ],
        "coming_soon": [
            "SMS integration",
            "WhatsApp business integration",
            "Facebook Messenger integration",
            "Email automation",
            "CRM synchronization",
            "Advanced analytics dashboard",
        ],
    },
}


def get_company_info():
    """Get complete company information"""
    return COMPANY_INFO


def get_service_info(service_name):
    """Get information about a specific service"""
    services = COMPANY_INFO.get("services", {})
    return services.get(service_name, None)


def get_elevator_pitch():
    """Get short elevator pitch"""
    return (
        "ProVision Brokerage provides AI-powered automation for financial advisors. "
        "We help you generate more leads, fill your seminars, and book more appointments "
        "through intelligent multi-channel engagement. "
        "According to Kitces.com, 63% of advisors are missing opportunities due to outdated technology. "
        "We bring Next Level AI to your practice."
    )


def get_value_proposition():
    """Get main value proposition"""
    return COMPANY_INFO["value_proposition"]


if __name__ == "__main__":
    print("ProVision Brokerage - Company Information")
    print("=" * 50)
    print(get_elevator_pitch())
