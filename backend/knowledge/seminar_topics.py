"""
Seminar Topics Library for ProVision Brokerage
Pre-built seminar content and descriptions
"""

from datetime import datetime, timedelta

SEMINAR_TOPICS = {
    "retirement_planning_strategies": {
        "title": "Retirement Planning Strategies for a Secure Future",
        "description": "Learn proven strategies to maximize your retirement income and minimize taxes. We'll cover Social Security optimization, withdrawal strategies, and creating guaranteed income streams.",
        "duration": 60,
        "target_audience": "Pre-retirees (55-70) and recent retirees",
        "key_topics": [
            "Social Security claiming strategies to maximize benefits",
            "4% rule vs. dynamic withdrawal strategies",
            "Creating guaranteed income with annuities",
            "Tax-efficient withdrawal ordering",
            "Healthcare and Medicare planning",
        ],
        "takeaways": [
            "Personalized Social Security analysis",
            "Retirement income planning worksheet",
            "Free 15-minute consultation offer",
        ],
        "call_to_action": "Book your free retirement readiness assessment",
    },
    "understanding_annuities": {
        "title": "Understanding Annuities: Your Guide to Guaranteed Retirement Income",
        "description": "Demystify annuities and discover how they can provide lifetime income security. Learn about fixed, variable, and indexed annuities, and which type might be right for you.",
        "duration": 60,
        "target_audience": "Adults 50+ considering guaranteed income solutions",
        "key_topics": [
            "What are annuities and how do they work?",
            "Fixed vs. Variable vs. Indexed annuities explained",
            "Pros and cons of each annuity type",
            "Income riders and living benefits",
            "Real-world case studies and examples",
        ],
        "takeaways": [
            "Annuity comparison guide",
            "Suitability assessment questionnaire",
            "Free personalized annuity analysis",
        ],
        "call_to_action": "Schedule your personal annuity review",
    },
    "social_security_maximization": {
        "title": "Social Security Maximization: Boost Your Benefits by Thousands",
        "description": "Discover little-known strategies to increase your Social Security benefits by up to 76%. Learn when to claim, spousal strategies, and how to coordinate with other retirement income.",
        "duration": 45,
        "target_audience": "Anyone within 10 years of claiming (ages 55-72)",
        "key_topics": [
            "The $100,000 claiming decision: 62 vs. 70",
            "Spousal and survivor benefit strategies",
            "Working while receiving benefits",
            "Taxation of Social Security benefits",
            "Coordinating with pensions and annuities",
        ],
        "takeaways": [
            "Personal claiming age analysis",
            "Social Security benefits calculator",
            "Free claiming strategy consultation",
        ],
        "call_to_action": "Get your personalized Social Security report",
    },
    "tax_efficient_retirement": {
        "title": "Tax-Efficient Retirement Income Planning",
        "description": "Learn how to keep more of your retirement savings by minimizing taxes. Discover strategies for Roth conversions, qualified charitable distributions, and smart withdrawal sequencing.",
        "duration": 60,
        "target_audience": "Retirees and pre-retirees with significant retirement accounts",
        "key_topics": [
            "Required Minimum Distributions (RMDs) at age 73",
            "Roth conversion opportunities",
            "Qualified Charitable Distributions (QCDs)",
            "Tax-bracket management in retirement",
            "State tax considerations for retirees",
        ],
        "takeaways": [
            "Tax planning checklist",
            "Roth conversion calculator",
            "Free tax-efficiency review",
        ],
        "call_to_action": "Schedule your retirement tax planning session",
    },
    "medicare_healthcare_costs": {
        "title": "Medicare & Healthcare Costs in Retirement",
        "description": "Navigate Medicare enrollment, understand your coverage options, and plan for healthcare expenses that could reach $315,000 in retirement.",
        "duration": 60,
        "target_audience": "Adults approaching 65 or already on Medicare",
        "key_topics": [
            "Medicare Parts A, B, C, and D explained",
            "Medigap vs. Medicare Advantage",
            "IRMAA surcharges and how to avoid them",
            "Long-term care planning options",
            "HSA strategies for healthcare expenses",
        ],
        "takeaways": [
            "Medicare enrollment checklist",
            "Healthcare cost estimator",
            "Free Medicare plan comparison",
        ],
        "call_to_action": "Get your personalized Medicare review",
    },
    "estate_planning_basics": {
        "title": "Estate Planning Basics: Protecting Your Legacy",
        "description": "Learn essential estate planning strategies to protect your assets, minimize taxes, and ensure your wishes are honored. Suitable for all adults, not just the wealthy.",
        "duration": 60,
        "target_audience": "Adults of all ages concerned about legacy planning",
        "key_topics": [
            "Wills vs. Trusts: What you need and when",
            "Powers of attorney and healthcare directives",
            "Beneficiary designations and avoiding probate",
            "Life insurance in estate planning",
            "Charitable giving strategies",
        ],
        "takeaways": [
            "Estate planning document checklist",
            "Beneficiary review worksheet",
            "Free estate planning consultation",
        ],
        "call_to_action": "Schedule your estate planning review",
    },
    "market_volatility_protection": {
        "title": "Protecting Your Retirement from Market Volatility",
        "description": "Learn strategies to protect your retirement savings from market downturns while still participating in growth. Discover the power of guaranteed income and downside protection.",
        "duration": 60,
        "target_audience": "Retirees and near-retirees concerned about market risk",
        "key_topics": [
            "Sequence of returns risk explained",
            "The bucket strategy for retirement income",
            "Indexed annuities: growth with protection",
            "Bond ladder strategies",
            "Rebalancing and risk management",
        ],
        "takeaways": [
            "Risk tolerance assessment",
            "Portfolio protection strategies guide",
            "Free retirement portfolio review",
        ],
        "call_to_action": "Book your portfolio protection analysis",
    },
    "women_and_retirement": {
        "title": "Women & Retirement: Unique Challenges and Solutions",
        "description": "Address the specific retirement planning challenges women face, including longer lifespans, career gaps, and healthcare needs. Empower yourself with knowledge and strategies.",
        "duration": 60,
        "target_audience": "Women of all ages planning for retirement",
        "key_topics": [
            "Longevity planning: women live longer, plan accordingly",
            "Spousal and survivor Social Security benefits",
            "Career gap strategies and catch-up contributions",
            "Widow's planning and financial preparation",
            "Healthcare and long-term care considerations",
        ],
        "takeaways": [
            "Women's retirement planning checklist",
            "Longevity income calculator",
            "Free personalized retirement plan",
        ],
        "call_to_action": "Schedule your women's retirement planning session",
    },
}


def get_seminar_topics():
    """Get list of all available seminar topics"""
    return list(SEMINAR_TOPICS.keys())


def get_seminar_info(topic_key):
    """Get detailed information about a specific seminar"""
    return SEMINAR_TOPICS.get(topic_key, {})


def generate_sample_seminars(count=5):
    """Generate sample upcoming seminar schedule"""
    from datetime import datetime, timedelta
    import random

    seminars = []
    topic_keys = list(SEMINAR_TOPICS.keys())

    for i in range(count):
        # Generate seminars for next 4-8 weeks
        days_ahead = random.randint(7 + (i * 7), 14 + (i * 7))
        seminar_date = datetime.now() + timedelta(days=days_ahead)

        # Pick a topic
        topic_key = topic_keys[i % len(topic_keys)]
        topic_info = SEMINAR_TOPICS[topic_key]

        # Create seminar object
        seminar = {
            "title": topic_info["title"],
            "description": topic_info["description"],
            "topic": topic_key.replace("_", " ").title(),
            "date": seminar_date,
            "duration": topic_info["duration"],
            "location_type": "virtual",
            "location_details": "Zoom link will be provided upon registration",
            "capacity": random.choice([25, 50, 75, 100]),
            "registered_count": random.randint(0, 20),
            "status": "upcoming",
        }

        seminars.append(seminar)

    return seminars


def get_seminar_follow_up_message(topic_key, attendee_name):
    """Generate personalized follow-up message after seminar"""
    topic_info = SEMINAR_TOPICS.get(topic_key, {})

    return f"""Dear {attendee_name},

Thank you for attending our seminar "{topic_info.get("title", "Retirement Planning")}". 

We hope you found the information valuable and actionable. As promised, here are your next steps:

 Review your personalized takeaway materials
 Schedule your complimentary consultation
 Start implementing the strategies we discussed

{topic_info.get("call_to_action", "Book your free consultation today")}

Click here to schedule: [BOOKING_LINK]

Best regards,
ProVision Brokerage Team
"""


if __name__ == "__main__":
    print("Seminar Topics Library")
    print("=" * 60)
    print(f"\nTotal Topics: {len(SEMINAR_TOPICS)}")
    print("\nAvailable Topics:")
    for key, info in SEMINAR_TOPICS.items():
        print(f"   {info['title']} ({info['duration']} min)")
