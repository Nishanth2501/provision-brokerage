"""
Intelligent Chatbot for ProVision Brokerage
Uses semantic understanding to provide relevant responses
"""

import os
import logging
from typing import Dict, List, Any
import re
import random

logger = logging.getLogger(__name__)


class IntelligentChatbot:
    """
    Intelligent chatbot that understands user intent and provides relevant responses
    """

    def __init__(self):
        """Initialize the intelligent chatbot"""
        self.knowledge_base = {
            "company_info": {
                "name": "ProVision Brokerage",
                "description": "AI-powered financial advisory services focused on retirement planning",
                "services": [
                    "Lead qualification and management",
                    "Appointment booking and scheduling",
                    "Seminar management and registration",
                    "Multi-channel client support (SMS, WhatsApp, Web)",
                    "Retirement planning consultation",
                    "Annuity education and guidance",
                    "Financial advisory services",
                ],
                "benefits": [
                    "Intelligent, personalized advice",
                    "Seamless client support across multiple channels",
                    "Instant seminar and appointment booking",
                    "Compliant, secure, and always-on service",
                    "AI-guided expertise with trusted advisors",
                ],
                "target_audience": "Individuals planning for retirement, seeking annuity solutions, and looking for financial security",
                "retirement_services": {
                    "consultation": "Free retirement readiness assessment and personalized planning consultation",
                    "annuity_guidance": "Expert guidance on fixed, variable, and indexed annuities for guaranteed income",
                    "seminar_education": "Educational seminars on retirement strategies, income planning, and annuity options",
                    "appointment_booking": "Easy scheduling with licensed retirement planning specialists",
                    "multi_channel_support": "Support via web chat, SMS, WhatsApp for ongoing guidance",
                },
                "investment_options": {
                    "annuities": "Fixed and variable annuities for guaranteed lifetime income",
                    "retirement_planning": "Comprehensive retirement income strategies and planning",
                    "tax_efficient_strategies": "Tax-deferred growth and distribution strategies",
                    "income_protection": "Protection against market volatility and longevity risk",
                },
                "age_specific_services": {
                    "20s_30s": {
                        "focus": "Building wealth foundation and starting early retirement savings",
                        "services": "Basic retirement planning, 401k optimization, and long-term wealth building strategies",
                        "products": "Growth-focused annuities and tax-advantaged retirement accounts",
                        "benefits": "Compound growth advantage and early retirement planning",
                    },
                    "40s_50s": {
                        "focus": "Accelerating retirement savings and mid-career wealth building",
                        "services": "Advanced retirement planning, catch-up contributions, and portfolio optimization",
                        "products": "Balanced annuities and diversified retirement strategies",
                        "benefits": "Peak earning years optimization and tax-efficient planning",
                    },
                    "60s_plus": {
                        "focus": "Transitioning to retirement and protecting accumulated wealth",
                        "services": "Retirement income planning, guaranteed income strategies, and legacy planning",
                        "products": "Income-focused annuities and conservative investment options",
                        "benefits": "Guaranteed income, capital preservation, and peace of mind",
                    },
                },
            },
            "annuities": {
                "definition": "Financial products that provide guaranteed income for life or a specified period",
                "types": {
                    "fixed_annuities": {
                        "description": "Offer guaranteed interest rate for specific period, principal protected",
                        "benefits": [
                            "Stable returns",
                            "No market risk",
                            "Guaranteed rate",
                        ],
                        "best_for": "Conservative investors who want stability",
                    },
                    "variable_annuities": {
                        "description": "Allow investment in sub-accounts with market-based returns",
                        "benefits": [
                            "Higher growth potential",
                            "Investment options",
                            "Flexibility",
                        ],
                        "best_for": "Investors comfortable with some risk",
                    },
                },
                "benefits": [
                    "Guaranteed lifetime income",
                    "Tax-deferred growth",
                    "Protection against outliving savings",
                    "Steady income stream during retirement",
                ],
                "considerations": [
                    "Surrender charges for early withdrawal",
                    "Tax implications on withdrawals",
                    "Long-term commitment",
                    "Insurance company guarantees",
                ],
            },
            "retirement_planning": {
                "key_concerns": [
                    "Market risk and volatility",
                    "Income certainty in retirement",
                    "Fees and costs",
                    "Tax implications",
                    "Legacy planning",
                ],
                "strategies": [
                    "Diversified investment approach",
                    "Guaranteed income products",
                    "Tax-efficient planning",
                    "Regular portfolio review",
                    "Professional guidance",
                ],
                "age_based_advice": {
                    "50s": "Focus on maximizing catch-up contributions, paying down debt, and creating a detailed retirement budget",
                    "60s": "Consider transitioning to more conservative investments and exploring guaranteed income options",
                    "70s": "Focus on required minimum distributions, healthcare planning, and estate planning",
                },
                "income_protection": [
                    "Diversify income sources (Social Security, pensions, annuities, investments)",
                    "Consider inflation protection through COLA adjustments",
                    "Build emergency fund for unexpected expenses",
                    "Plan for healthcare costs with HSA or long-term care insurance",
                ],
                "common_mistakes": [
                    "Not starting early enough",
                    "Underestimating healthcare costs",
                    "Not accounting for inflation",
                    "Taking too much or too little risk",
                    "Not having a written plan",
                ],
                "retirement_vehicles": {
                    "401k": "Employer-sponsored plan with tax advantages and potential matching",
                    "IRA": "Individual retirement account with tax benefits",
                    "Annuities": "Guaranteed income products for lifetime income",
                    "Social Security": "Government benefit based on work history",
                },
            },
            "seminars": {
                "topics": [
                    "Retirement Planning Strategies",
                    "Understanding Annuities",
                    "Tax-Efficient Retirement Planning",
                    "Income Protection Strategies",
                    "Legacy Planning",
                ],
                "benefits": [
                    "Educational content",
                    "Expert guidance",
                    "Q&A opportunities",
                    "No-pressure environment",
                    "Personalized advice",
                ],
            },
        }

        self.response_templates = {
            "greeting": [
                "Hello! I'm your AI assistant for ProVision Brokerage. How can I help you with your retirement planning today?",
                "Welcome to ProVision Brokerage! I'm here to help you understand our services and retirement planning options. What would you like to know?",
                "Hi there! I can help you learn about ProVision's services, annuities, and retirement planning. What's your main concern?",
            ],
            "company_services": [
                "ProVision Brokerage offers comprehensive financial advisory services including {services}. We specialize in {description} and help clients {benefits}.",
                "Our services at ProVision Brokerage include {services}. We provide {description} with a focus on {target_audience}.",
                "ProVision Brokerage delivers {description} through our range of services: {services}. Our goal is to help you {benefits}.",
            ],
            "provision_retirement_services": [
                "Perfect! At {age_range}, ProVision offers {age_services} tailored specifically for your life stage. We focus on {age_focus} to help you {age_benefits}. Our {age_products} are designed to maximize your retirement potential. Let's schedule a free consultation to create your personalized plan!",
                "Excellent timing! For someone in their {age_range}, ProVision provides {age_services} that align with your current needs. We specialize in {age_focus} to deliver {age_benefits}. Our {age_products} can help you achieve your retirement goals faster. Ready to get started?",
                "Great question! At {age_range}, ProVision's {age_services} are perfectly suited for your situation. We emphasize {age_focus} to ensure {age_benefits}. Our {age_products} offer the ideal balance for your retirement planning. Would you like to learn more about our specific solutions?",
            ],
            "provision_investment_options": [
                "Fantastic! ProVision's investment options are perfectly tailored for your {age_range}: {investment_options}. We recommend {age_specific_advice} to maximize {retirement_benefits}. Our proven strategies have helped thousands of clients like you build wealth. Let's create your personalized investment plan today!",
                "Excellent! At {age_range}, ProVision offers {investment_options} designed specifically for your life stage. We focus on {age_specific_advice} to deliver {retirement_benefits}. Our track record speaks for itself - let's discuss how we can accelerate your retirement goals!",
                "Perfect timing! ProVision's {investment_options} are ideal for your {age_range}. We specialize in {age_specific_advice} to ensure {retirement_benefits}. Don't wait - the earlier you start, the more you'll benefit. Ready to take the next step?",
            ],
            "annuities_general": [
                "Annuities are {definition}. They offer {benefits} and are particularly useful for {target_audience}.",
                "An annuity is a financial product that {definition}. The main benefits include {benefits}, making them ideal for retirement planning.",
                "Annuities provide {benefits} by {definition}. They're designed to help you create a steady income stream during retirement.",
            ],
            "annuities_types": [
                "There are different types of annuities. {fixed_description} are great for {fixed_best_for}. {variable_description} are better for {variable_best_for}.",
                "Annuities come in various forms. Fixed annuities offer {fixed_benefits} and are ideal for {fixed_best_for}. Variable annuities provide {variable_benefits} for {variable_best_for}.",
                "The main annuity types include fixed and variable. Fixed annuities {fixed_description} while variable annuities {variable_description}.",
            ],
            "retirement_planning": [
                "Retirement planning involves addressing key concerns like {concerns} through strategies such as {strategies}. ProVision can help you develop a personalized approach.",
                "Effective retirement planning considers {concerns} and implements {strategies}. Our advisors can guide you through this process.",
                "Retirement planning is about balancing {concerns} with {strategies}. We offer personalized guidance to help you achieve your goals.",
            ],
            "retirement_age_specific": [
                "For someone in their {age_range}, the key focus should be {age_advice}. This includes {strategies} to ensure a secure retirement. ProVision can help you create a personalized plan.",
                "At your age, retirement planning should prioritize {age_advice}. Consider {strategies} and avoid common mistakes like {common_mistakes}. Our specialists can guide you through this critical phase.",
                "Your age group should focus on {age_advice}. This means implementing {strategies} while being aware of potential pitfalls like {common_mistakes}. Let's discuss your specific situation.",
            ],
            "retirement_income_protection": [
                "Protecting retirement income requires {income_protection_strategies}. This includes {specific_strategies} to ensure you never run out of money. ProVision specializes in creating guaranteed income strategies.",
                "To secure your retirement income, focus on {income_protection_strategies}. Key strategies include {specific_strategies}. Our advisors can help you build a bulletproof retirement income plan.",
                "Retirement income protection means {income_protection_strategies}. Consider {specific_strategies} to create multiple income streams. We can help you design a comprehensive approach.",
            ],
            "retirement_vehicles": [
                "Different retirement vehicles serve different purposes: {vehicle_descriptions}. The right combination depends on your age, risk tolerance, and goals. ProVision can help you choose the optimal mix.",
                "Understanding retirement vehicles is crucial: {vehicle_descriptions}. Each has unique benefits and considerations. Our specialists can explain which options work best for your situation.",
                "Retirement planning involves various vehicles: {vehicle_descriptions}. The key is finding the right balance for your needs. Let's discuss your specific requirements.",
            ],
            "seminars": [
                "ProVision offers educational seminars on topics like {topics}. These sessions provide {benefits} in a comfortable, no-pressure environment.",
                "Our seminars cover important topics including {topics}. You'll benefit from {benefits} and can ask questions directly to our experts.",
                "We host informative seminars on {topics} where you can learn about retirement planning strategies and get {benefits}.",
            ],
            "consultation": [
                "I'd be happy to help you schedule a consultation with one of our retirement planning specialists. They can provide personalized advice based on your specific situation.",
                "A consultation with our advisors would be perfect for getting personalized retirement planning advice tailored to your needs and goals.",
                "Our retirement specialists offer free consultations to help you understand your options and develop a customized plan.",
            ],
            "not_found": [
                "Information not found. I can only help with ProVision Brokerage services, retirement planning, annuities, and financial advisory topics. Please ask about our services or retirement planning.",
                "Information not found. I specialize in ProVision Brokerage services including retirement planning, annuities, and financial advisory. How can I help you with these topics?",
                "Information not found. I can assist with ProVision's retirement planning services, annuity information, and financial guidance. What would you like to know about our services?",
            ],
        }

    def get_response(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        """Get intelligent response for user's message"""
        try:
            message_lower = message.lower()

            # Determine intent and generate appropriate response
            intent = self._analyze_intent(message_lower)
            response_text = self._generate_response(intent, message_lower)
            suggestions = self._generate_suggestions(intent)

            return {
                "message": response_text,
                "current_step": "chat",
                "qualification_progress": 0,
                "qualification_score": None,
                "suggested_actions": suggestions,
                "requires_human": False,
                "knowledge_sources": ["ProVision Brokerage Knowledge Base"],
                "context": {"current_state": "chat", "session_id": session_id},
            }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "message": "I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team.",
                "current_step": "error",
                "qualification_progress": 0,
                "qualification_score": None,
                "suggested_actions": ["Contact support"],
                "requires_human": True,
                "knowledge_sources": [],
                "context": {"current_state": "error", "session_id": session_id},
            }

    def _analyze_intent(self, message: str) -> str:
        """Analyze user message to determine intent"""

        # Greeting patterns
        if any(
            word in message
            for word in [
                "hello",
                "hi",
                "hey",
                "good morning",
                "good afternoon",
                "good evening",
            ]
        ):
            return "greeting"

        # ProVision retirement services for any age
        if any(
            word in message
            for word in [
                "20",
                "30",
                "40",
                "50",
                "60",
                "70",
                "age",
                "years old",
                "retiring",
                "retirement",
                "what can provision do",
                "provision services",
                "provision plans",
                "provision brokerage",
                "provision help",
                "what can",
                "help me",
                "do for me",
                "provision can",
                "provision offers",
            ]
        ):
            return "provision_retirement_services"

        # ProVision investment options
        if any(
            word in message
            for word in [
                "invest",
                "investment",
                "provision investment",
                "how to invest",
                "provision plans",
                "investment options",
                "provision brokerage",
            ]
        ):
            return "provision_investment_options"

        # Company/ProVision related
        if any(
            word in message
            for word in [
                "provision",
                "company",
                "services",
                "what do you do",
                "about you",
                "business",
            ]
        ):
            return "company_services"

        # Annuities general
        if any(
            word in message
            for word in ["annuity", "annuities", "what are annuities", "annuity types"]
        ):
            return "annuities_general"

        # Specific annuity types
        if any(
            word in message
            for word in [
                "fixed annuity",
                "variable annuity",
                "types of annuities",
                "annuity options",
            ]
        ):
            return "annuities_types"

        # Retirement vehicles (401k, IRA, etc.) - check first for specific terms
        if any(
            word in message
            for word in [
                "401k",
                "ira",
                "roth",
                "retirement account",
                "retirement vehicle",
                "social security",
                "pension",
                "retirement savings",
                "difference between",
            ]
        ):
            return "retirement_vehicles"

        # Income protection in retirement
        if any(
            word in message
            for word in [
                "steady income",
                "guaranteed income",
                "protect income",
                "retirement income",
                "never run out",
                "outlive money",
                "ensure income",
            ]
        ):
            return "retirement_income_protection"

        # Age-specific retirement planning
        if any(
            word in message
            for word in [
                "50",
                "60",
                "70",
                "age",
                "years old",
                "retiring in",
                "retire in",
            ]
        ):
            return "retirement_age_specific"

        # Retirement planning - general (fallback)
        if any(
            word in message
            for word in [
                "retirement",
                "retire",
                "planning",
                "financial future",
                "pension",
            ]
        ):
            return "retirement_planning"

        # Seminars
        if any(
            word in message
            for word in [
                "seminar",
                "seminars",
                "workshop",
                "event",
                "class",
                "learn",
                "education",
            ]
        ):
            return "seminars"

        # Consultation/meeting
        if any(
            word in message
            for word in [
                "consultation",
                "meeting",
                "appointment",
                "advisor",
                "specialist",
                "book",
                "schedule",
            ]
        ):
            return "consultation"

        # Tax related
        if any(
            word in message
            for word in ["tax", "taxes", "tax benefits", "tax advantage", "deduction"]
        ):
            return "annuities_general"  # Redirect to annuities for tax questions

        # Check for irrelevant topics that should return "not found"
        irrelevant_topics = [
            "weather", "sports", "politics", "cooking", "travel", "movies", "music", 
            "gaming", "technology", "programming", "coding", "software", "hardware",
            "cars", "fashion", "food", "restaurants", "shopping", "entertainment",
            "news", "current events", "history", "science", "medicine", "health",
            "fitness", "exercise", "diet", "relationships", "dating", "family",
            "education", "school", "university", "college", "jobs", "career",
            "business", "marketing", "sales", "real estate", "insurance", "loans",
            "credit", "debt", "mortgage", "banking", "cryptocurrency", "bitcoin",
            "stocks", "trading", "investing", "forex", "crypto", "blockchain"
        ]
        
        if any(
            word in message_lower
            for word in irrelevant_topics
        ):
            return "not_found"

        # Default - only for ProVision-related topics that don't match specific intents
        return "not_found"

    def _generate_response(self, intent: str, message: str) -> str:
        """Generate response based on intent"""

        if intent == "greeting":
            return random.choice(self.response_templates["greeting"])

        elif intent == "provision_retirement_services":
            template = random.choice(
                self.response_templates["provision_retirement_services"]
            )
            company = self.knowledge_base["company_info"]
            age_services = company["age_specific_services"]

            # Determine age range from message - more comprehensive detection
            age_range = "40s-50s"  # default
            message_lower = message.lower()

            # Check for specific ages first
            if any(
                word in message_lower
                for word in [
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                    "32",
                    "33",
                    "34",
                    "35",
                ]
            ):
                age_range = "20s-30s"
            elif any(
                word in message_lower
                for word in [
                    "40",
                    "41",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                    "55",
                ]
            ):
                age_range = "40s-50s"
            elif any(
                word in message_lower
                for word in [
                    "60",
                    "61",
                    "62",
                    "63",
                    "64",
                    "65",
                    "66",
                    "67",
                    "68",
                    "69",
                    "70",
                    "71",
                    "72",
                    "73",
                    "74",
                    "75",
                ]
            ):
                age_range = "60s+"
            # Check for age ranges
            elif any(
                word in message_lower
                for word in ["20s", "30s", "young", "early career"]
            ):
                age_range = "20s-30s"
            elif any(
                word in message_lower
                for word in ["40s", "50s", "mid career", "middle age"]
            ):
                age_range = "40s-50s"
            elif any(
                word in message_lower
                for word in ["60s", "70s", "retiring", "retirement age", "senior"]
            ):
                age_range = "60s+"

            # Get age-specific information
            age_key = age_range.replace("+", "_plus").replace("-", "_")
            age_info = age_services.get(age_key, age_services["40s_50s"])

            return template.format(
                age_range=age_range,
                age_services=age_info["services"],
                age_focus=age_info["focus"],
                age_benefits=age_info["benefits"],
                age_products=age_info["products"],
            )

        elif intent == "provision_investment_options":
            template = random.choice(
                self.response_templates["provision_investment_options"]
            )
            company = self.knowledge_base["company_info"]
            investment_options = company["investment_options"]
            age_services = company["age_specific_services"]

            # Determine age range from message - more comprehensive detection
            age_range = "40s-50s"  # default
            message_lower = message.lower()

            # Check for specific ages first
            if any(
                word in message_lower
                for word in [
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                    "32",
                    "33",
                    "34",
                    "35",
                ]
            ):
                age_range = "20s-30s"
            elif any(
                word in message_lower
                for word in [
                    "40",
                    "41",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                    "55",
                ]
            ):
                age_range = "40s-50s"
            elif any(
                word in message_lower
                for word in [
                    "60",
                    "61",
                    "62",
                    "63",
                    "64",
                    "65",
                    "66",
                    "67",
                    "68",
                    "69",
                    "70",
                    "71",
                    "72",
                    "73",
                    "74",
                    "75",
                ]
            ):
                age_range = "60s+"
            # Check for age ranges
            elif any(
                word in message_lower
                for word in ["20s", "30s", "young", "early career"]
            ):
                age_range = "20s-30s"
            elif any(
                word in message_lower
                for word in ["40s", "50s", "mid career", "middle age"]
            ):
                age_range = "40s-50s"
            elif any(
                word in message_lower
                for word in ["60s", "70s", "retiring", "retirement age", "senior"]
            ):
                age_range = "60s+"

            # Get age-specific information
            age_key = age_range.replace("+", "_plus").replace("-", "_")
            age_info = age_services.get(age_key, age_services["40s_50s"])

            return template.format(
                age_range=age_range,
                investment_options=", ".join(
                    [
                        f"Annuities ({investment_options['annuities']})",
                        f"Retirement Planning ({investment_options['retirement_planning']})",
                        f"Tax-Efficient Strategies ({investment_options['tax_efficient_strategies']})",
                    ]
                ),
                age_specific_advice=age_info["focus"],
                retirement_benefits=age_info["benefits"],
            )

        elif intent == "company_services":
            template = random.choice(self.response_templates["company_services"])
            company = self.knowledge_base["company_info"]
            return template.format(
                services=", ".join(company["services"][:3]) + " and more",
                description=company["description"],
                benefits=", ".join(company["benefits"][:2]) + " and more",
                target_audience=company["target_audience"],
            )

        elif intent == "annuities_general":
            template = random.choice(self.response_templates["annuities_general"])
            annuities = self.knowledge_base["annuities"]
            return template.format(
                definition=annuities["definition"],
                benefits=", ".join(annuities["benefits"][:3]) + " and more",
                target_audience="retirement planning",
            )

        elif intent == "annuities_types":
            template = random.choice(self.response_templates["annuities_types"])
            annuities = self.knowledge_base["annuities"]
            fixed = annuities["types"]["fixed_annuities"]
            variable = annuities["types"]["variable_annuities"]
            return template.format(
                fixed_description=fixed["description"],
                fixed_best_for=fixed["best_for"],
                fixed_benefits=", ".join(fixed["benefits"]),
                variable_description=variable["description"],
                variable_best_for=variable["best_for"],
                variable_benefits=", ".join(variable["benefits"]),
            )

        elif intent == "retirement_planning":
            template = random.choice(self.response_templates["retirement_planning"])
            retirement = self.knowledge_base["retirement_planning"]
            return template.format(
                concerns=", ".join(retirement["key_concerns"][:3]) + " and more",
                strategies=", ".join(retirement["strategies"][:3]) + " and more",
            )

        elif intent == "retirement_age_specific":
            template = random.choice(self.response_templates["retirement_age_specific"])
            retirement = self.knowledge_base["retirement_planning"]

            # Determine age range from message
            age_range = "50s"
            if any(word in message for word in ["60", "sixty"]):
                age_range = "60s"
            elif any(word in message for word in ["70", "seventy"]):
                age_range = "70s"

            return template.format(
                age_range=age_range,
                age_advice=retirement["age_based_advice"][age_range],
                strategies=", ".join(retirement["strategies"][:2]) + " and more",
                common_mistakes=", ".join(retirement["common_mistakes"][:2])
                + " and more",
            )

        elif intent == "retirement_income_protection":
            template = random.choice(
                self.response_templates["retirement_income_protection"]
            )
            retirement = self.knowledge_base["retirement_planning"]
            return template.format(
                income_protection_strategies="diversifying income sources and protecting against market volatility",
                specific_strategies=", ".join(retirement["income_protection"][:3])
                + " and more",
            )

        elif intent == "retirement_vehicles":
            template = random.choice(self.response_templates["retirement_vehicles"])
            retirement = self.knowledge_base["retirement_planning"]
            vehicles = retirement["retirement_vehicles"]
            vehicle_descriptions = f"401k plans ({vehicles['401k']}), IRAs ({vehicles['IRA']}), Annuities ({vehicles['Annuities']}), and Social Security ({vehicles['Social Security']})"
            return template.format(vehicle_descriptions=vehicle_descriptions)

        elif intent == "seminars":
            template = random.choice(self.response_templates["seminars"])
            seminars = self.knowledge_base["seminars"]
            return template.format(
                topics=", ".join(seminars["topics"][:3]) + " and more",
                benefits=", ".join(seminars["benefits"][:3]) + " and more",
            )

        elif intent == "consultation":
            return random.choice(self.response_templates["consultation"])

        elif intent == "not_found":
            return random.choice(self.response_templates["not_found"])

        else:
            return random.choice(self.response_templates["not_found"])

    def _generate_suggestions(self, intent: str) -> List[str]:
        """Generate relevant follow-up suggestions based on intent"""

        suggestions_map = {
            "greeting": [
                "Tell me about ProVision's services",
                "What are annuities?",
                "Schedule a consultation",
            ],
            "provision_retirement_services": [
                "What investment options do you have?",
                "How do I schedule a consultation?",
                "Tell me about your seminars",
            ],
            "provision_investment_options": [
                "What are annuities?",
                "Schedule a consultation",
                "Tell me about retirement planning",
            ],
            "company_services": [
                "What are annuities?",
                "Tell me about seminars",
                "How do I get started?",
            ],
            "annuities_general": [
                "What are fixed annuities?",
                "What are variable annuities?",
                "What are the tax benefits?",
            ],
            "annuities_types": [
                "What are the tax benefits?",
                "What are surrender charges?",
                "How do I choose?",
            ],
            "retirement_planning": [
                "What are annuities?",
                "Tell me about seminars",
                "Schedule a consultation",
            ],
            "retirement_age_specific": [
                "How do I protect my income?",
                "What are common mistakes?",
                "Schedule a consultation",
            ],
            "retirement_income_protection": [
                "What are annuities?",
                "Tell me about 401k vs IRA",
                "Schedule a consultation",
            ],
            "retirement_vehicles": [
                "What are annuities?",
                "How do I protect income?",
                "Schedule a consultation",
            ],
            "seminars": [
                "Register for a seminar",
                "What are annuities?",
                "Schedule a consultation",
            ],
            "consultation": [
                "Book an appointment",
                "Learn about annuities",
                "Ask about seminars",
            ],
            "not_found": [
                "Tell me about ProVision's services",
                "What are annuities?",
                "How can ProVision help me?",
            ],
            "default": [
                "Tell me about ProVision's services",
                "What are annuities?",
                "Schedule a consultation",
            ],
        }

        return suggestions_map.get(intent, ["Learn more", "Ask questions", "Get help"])

    def get_qualification_questions(self) -> List[str]:
        """Get list of qualification questions"""
        return [
            "What's your age range? (e.g., 55-65, 65-75, 75+)",
            "When are you planning to retire? (e.g., 1-3 years, 3-5 years, 5+ years)",
            "What state do you live in?",
            "What's your approximate investable assets range? (e.g., 100k-500k, 500k-1M, 1M+)",
            "Do you currently have any annuities or pension income?",
            "What are your main retirement concerns? (e.g., market risk, income certainty, fees, taxes, legacy)",
            "What are your primary retirement goals? (e.g., guaranteed income, growth, legacy planning)",
        ]

    def test_chatbot(self) -> Dict[str, Any]:
        """Test the chatbot with various queries"""
        test_queries = [
            "Hello",
            "What does ProVision Brokerage do?",
            "What are annuities?",
            "Tell me about fixed annuities",
            "What services do you offer?",
            "I want to learn about retirement planning",
            "Tell me about seminars",
            "I want to schedule a consultation",
        ]

        results = {}
        for query in test_queries:
            try:
                response = self.get_response(query)
                results[query] = {
                    "success": True,
                    "response": response["message"][:100] + "..."
                    if len(response["message"]) > 100
                    else response["message"],
                    "suggestions": response["suggested_actions"],
                }
            except Exception as e:
                results[query] = {"success": False, "error": str(e)}

        return {"chatbot_status": "operational", "test_results": results}
