"""
Qualification Service - Lead Scoring Engine
Handles qualification questions and lead scoring logic
"""

from core.config import settings


class QualificationService:
    """Service for lead qualification and scoring"""

    # Qualification questions in order
    QUESTIONS = [
        {
            "id": 1,
            "question": "To help me provide the best guidance, what's your age range?",
            "field": "age_range",
            "options": ["20-30", "31-50", "51-65", "65+"],
            "context": "This helps us tailor advice to your life stage and time horizon.",
        },
        {
            "id": 2,
            "question": "When are you planning to retire (or have you already retired)?",
            "field": "retirement_timeline",
            "options": [
                "Already retired",
                "1-5 years",
                "6-10 years",
                "11-15 years",
                "15+ years",
            ],
            "context": "Your retirement timeline shapes the strategies that work best for you.",
        },
        {
            "id": 3,
            "question": "What state do you currently reside in?",
            "field": "state",
            "context": "State regulations affect product availability and tax considerations.",
        },
        {
            "id": 4,
            "question": "Approximately how much do you have in investable assets (retirement accounts, savings, investments)?",
            "field": "investable_assets",
            "options": [
                "Less than $100k",
                "$100k-$500k",
                "$500k-$1M",
                "Over $1M",
                "Prefer not to say",
            ],
            "context": "This helps us recommend appropriate strategies and solutions.",
        },
        {
            "id": 5,
            "question": "Do you currently own an annuity or guaranteed income product?",
            "field": "current_annuity",
            "options": ["Yes", "No", "Not sure"],
            "context": "Understanding your current situation helps us avoid duplication and identify gaps.",
        },
        {
            "id": 6,
            "question": "What's your primary concern when it comes to retirement?",
            "field": "concerns",
            "options": [
                "Guaranteed income",
                "Market risk",
                "Outliving my money",
                "Healthcare costs",
                "Taxes",
                "Leaving a legacy",
            ],
            "context": "Your concerns guide our recommendations and priorities.",
        },
        {
            "id": 7,
            "question": "What are your main retirement goals?",
            "field": "goals",
            "options": [
                "Maintain current lifestyle",
                "Travel",
                "Support family",
                "Start a business",
                "Charitable giving",
                "Other",
            ],
            "context": "Your goals help us create a personalized plan.",
        },
    ]

    def __init__(self):
        """Initialize qualification service"""
        self.max_questions = settings.QUALIFICATION_QUESTIONS_COUNT

    def get_next_question(
        self, qualification_progress: int, answered_fields: dict = None
    ) -> dict:
        """
        Get next qualification question based on progress

        Args:
            qualification_progress: Number of questions answered (0-7)
            answered_fields: Dict of already answered fields

        Returns:
            Question dict or None if complete
        """
        if qualification_progress >= self.max_questions:
            return None

        # Get question at current progress index
        if qualification_progress < len(self.QUESTIONS):
            question = self.QUESTIONS[qualification_progress]

            # Check if this field was already answered
            if answered_fields and question["field"] in answered_fields:
                # Skip to next question
                return self.get_next_question(
                    qualification_progress + 1, answered_fields
                )

            return question

        return None

    def calculate_score(self, answers: dict) -> int:
        """
        Calculate lead score based on qualification answers
        Score range: 0-100

        Scoring breakdown:
        - Age: 25-30 points (older = higher urgency)
        - Retirement timeline: 15-30 points (sooner = higher priority)
        - Assets: 25-40 points (higher = higher value)
        - Current annuity: 10-20 points (no annuity = opportunity)
        - Concerns: 15-25 points (income/risk concerns = good fit)
        - Goals: 10-30 points (specific goals = engaged prospect)
        """
        score = 0

        # Age scoring (25-30 points)
        age_range = answers.get("age_range", "")
        age_scores = {
            "20-30": 15,  # Low urgency, long time horizon
            "31-50": 20,  # Moderate urgency
            "51-65": 28,  # High urgency, prime retirement planning years
            "65+": 30,  # Immediate needs, highest priority
        }
        score += age_scores.get(age_range, 0)

        # Retirement timeline scoring (15-30 points)
        timeline = answers.get("retirement_timeline", "")
        timeline_scores = {
            "Already retired": 30,  # Immediate income needs
            "1-5 years": 28,  # Very near term
            "6-10 years": 22,  # Mid-term planning
            "11-15 years": 18,  # Longer term
            "15+ years": 15,  # Long term, lower urgency
        }
        score += timeline_scores.get(timeline, 0)

        # Assets scoring (25-40 points)
        assets = answers.get("investable_assets", "")
        asset_scores = {
            "Less than $100k": 20,  # Smaller opportunity
            "$100k-$500k": 30,  # Good opportunity
            "$500k-$1M": 38,  # High value
            "Over $1M": 40,  # Premium client
            "Prefer not to say": 25,  # Moderate - unknown
        }
        score += asset_scores.get(assets, 0)

        # Current annuity scoring (10-20 points)
        current_annuity = answers.get("current_annuity", "")
        annuity_scores = {
            "Yes": 10,  # Already has one, may have questions or need review
            "No": 20,  # Clear opportunity
            "Not sure": 15,  # Education opportunity
        }
        score += annuity_scores.get(current_annuity, 0)

        # Concerns scoring (15-25 points)
        concerns = answers.get("concerns", "")
        concern_scores = {
            "Guaranteed income": 25,  # Perfect fit for annuities
            "Market risk": 24,  # Indexed/fixed annuity opportunity
            "Outliving my money": 25,  # Longevity protection - annuities ideal
            "Healthcare costs": 20,  # Important but not direct annuity fit
            "Taxes": 18,  # Tax planning opportunity
            "Leaving a legacy": 15,  # Estate planning focus
        }
        score += concern_scores.get(concerns, 0)

        # Goals scoring (10-30 points)
        goals = answers.get("goals", "")
        goal_scores = {
            "Maintain current lifestyle": 28,  # Income planning critical
            "Travel": 25,  # Needs reliable income
            "Support family": 22,  # Legacy and income planning
            "Start a business": 18,  # May need liquidity
            "Charitable giving": 20,  # Legacy planning
            "Other": 15,  # General interest
        }
        score += goal_scores.get(goals, 0)

        # Cap at 100
        return min(score, 100)

    def classify_lead(self, score: int) -> str:
        """
        Classify lead based on score

        Args:
            score: Lead score (0-100)

        Returns:
            Classification string
        """
        if score >= settings.HIGH_VALUE_THRESHOLD:
            return "High Value"
        elif score >= settings.QUALIFIED_THRESHOLD:
            return "Qualified"
        elif score >= settings.WARM_THRESHOLD:
            return "Warm"
        else:
            return "Cold"

    def is_qualification_complete(self, qualification_progress: int) -> bool:
        """Check if qualification is complete"""
        return qualification_progress >= self.max_questions

    def should_offer_appointment(self, score: int, qualification_progress: int) -> bool:
        """
        Determine if we should offer appointment booking

        Args:
            score: Lead score
            qualification_progress: Number of questions answered

        Returns:
            Boolean
        """
        # Offer appointment if:
        # 1. Qualification is complete, OR
        # 2. Score is high enough (60+) after at least 4 questions
        if qualification_progress >= self.max_questions:
            return True

        if qualification_progress >= 4 and score >= settings.QUALIFIED_THRESHOLD:
            return True

        return False

    def get_recommendation_message(self, score: int, classification: str) -> str:
        """Get personalized recommendation based on score"""
        if classification == "High Value":
            return (
                "Based on our conversation, I believe you'd benefit greatly from a personalized "
                "retirement income strategy. I'd love to connect you with one of our senior advisors "
                "who specializes in clients in your situation. They can provide a complimentary "
                "retirement readiness assessment and show you guaranteed income solutions."
            )
        elif classification == "Qualified":
            return (
                "Thanks for sharing that information! You're in a great position to benefit from "
                "our retirement planning services. I'd recommend speaking with one of our advisors "
                "who can review your specific situation and show you strategies to optimize your "
                "retirement income."
            )
        elif classification == "Warm":
            return (
                "I appreciate you taking the time to chat! While you're still in the planning stages, "
                "it's never too early to start thinking about guaranteed income strategies. Would you "
                "like to schedule a brief consultation to learn more about your options?"
            )
        else:  # Cold
            return (
                "Thanks for reaching out! We have educational resources and seminars that might be "
                "helpful as you begin your retirement planning journey. Would you like to register "
                "for an upcoming webinar on retirement basics?"
            )


if __name__ == "__main__":
    # Test the service
    print("Testing Qualification Service...")
    print("=" * 60)

    service = QualificationService()

    # Test getting questions
    print("\n[1/3] Testing question flow...")
    for i in range(8):
        question = service.get_next_question(i)
        if question:
            print(f"  Q{i + 1}: {question['question'][:50]}...")
        else:
            print(f"  Q{i + 1}: Complete!")

    # Test scoring
    print("\n[2/3] Testing lead scoring...")
    test_answers = {
        "age_range": "51-65",
        "retirement_timeline": "1-5 years",
        "investable_assets": "$500k-$1M",
        "current_annuity": "No",
        "concerns": "Guaranteed income",
        "goals": "Maintain current lifestyle",
    }
    score = service.calculate_score(test_answers)
    classification = service.classify_lead(score)
    print(f"  Sample Score: {score}/100")
    print(f"  Classification: {classification}")

    # Test appointment logic
    print("\n[3/3] Testing appointment recommendation...")
    should_offer = service.should_offer_appointment(score, 6)
    print(f"  Should offer appointment: {should_offer}")
    if should_offer:
        message = service.get_recommendation_message(score, classification)
        print(f"  Recommendation: {message[:100]}...")

    print("\n" + "=" * 60)
    print(" Qualification Service is working!")
