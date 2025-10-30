"""
Retirement Planning & Financial Advisory Knowledge
Domain expertise for ProVision Brokerage AI
"""

RETIREMENT_PLANNING = {
    "overview": {
        "definition": "Retirement planning is the process of determining retirement income goals and the actions necessary to achieve those goals.",
        "importance": "Proper planning ensures financial security, maintains lifestyle, and provides peace of mind in retirement years.",
        "key_components": [
            "Income planning and sources",
            "Investment strategy and asset allocation",
            "Tax-efficient distribution strategies",
            "Healthcare and long-term care planning",
            "Estate planning and legacy goals",
        ],
    },
    "age_specific_guidance": {
        "20s_30s": {
            "focus": "Building wealth foundation and starting early",
            "priorities": [
                "Maximize employer 401(k) match",
                "Start Roth IRA contributions",
                "Build emergency fund (3-6 months expenses)",
                "Pay off high-interest debt",
                "Invest in growth-oriented assets",
            ],
            "typical_concerns": [
                "Student loan debt",
                "Starting career and building income",
                "Balancing current needs vs future savings",
                "Understanding investment basics",
            ],
            "advisor_talking_points": [
                "Time is your greatest asset - compound growth advantage",
                "Every $100/month at 25 = ~$260,000 at 65 (7% return)",
                "Start small but start now",
                "Focus on habits, not perfection",
            ],
        },
        "40s_50s": {
            "focus": "Accelerating retirement savings and mid-career wealth building",
            "priorities": [
                "Maximize catch-up contributions (50+)",
                "Review and rebalance investment portfolio",
                "Consider annuities for guaranteed income",
                "Plan for college expenses vs retirement",
                "Review insurance coverage (life, disability, long-term care)",
            ],
            "typical_concerns": [
                "Behind on retirement savings",
                "Supporting aging parents and children",
                "Job security and career changes",
                "Healthcare costs before Medicare",
            ],
            "advisor_talking_points": [
                "Peak earning years - opportunity to accelerate savings",
                "Catch-up contributions allow $7,500 extra (401k) and $1,000 (IRA) at 50+",
                "Time to balance growth and protection",
                "Consider guaranteed income solutions (annuities)",
            ],
        },
        "60s_plus": {
            "focus": "Transitioning to retirement and protecting accumulated wealth",
            "priorities": [
                "Create guaranteed income streams",
                "Optimize Social Security claiming strategy",
                "Plan Medicare enrollment and supplemental coverage",
                "Develop tax-efficient withdrawal strategy",
                "Establish Required Minimum Distribution (RMD) plan",
            ],
            "typical_concerns": [
                "Will my money last?",
                "Market volatility and sequence of returns risk",
                "Healthcare and long-term care costs",
                "Leaving legacy for family",
                "When to claim Social Security",
            ],
            "advisor_talking_points": [
                "Guaranteed income = peace of mind",
                "Annuities can protect against longevity risk",
                "Social Security timing can increase benefits by 76% (62 vs 70)",
                "Tax-efficient withdrawals can save thousands annually",
                "We'll create a written income plan",
            ],
        },
    },
    "income_sources": {
        "social_security": {
            "description": "Government-provided retirement benefit based on work history",
            "claiming_ages": {
                "62": "Earliest claiming age - reduced benefits (25-30% reduction)",
                "67": "Full Retirement Age (FRA) for most - 100% of earned benefit",
                "70": "Maximum benefit age - 124-132% of FRA benefit (8% per year increase)",
            },
            "strategies": [
                "Delay claiming to age 70 for maximum benefit",
                "Spousal claiming strategies for married couples",
                "File and suspend options",
                "Consider life expectancy and health status",
            ],
        },
        "pensions": {
            "description": "Employer-sponsored defined benefit plans",
            "options": [
                "Single life annuity (highest payment)",
                "Joint and survivor annuity (lower payment, spouse coverage)",
                "Lump sum option (if available)",
                "Period certain options",
            ],
            "considerations": "COLA adjustments, company stability, survivor needs",
        },
        "retirement_accounts": {
            "401k_403b": "Employer-sponsored plans - tax-deferred growth, required RMDs at 73",
            "traditional_ira": "Individual retirement account - tax-deferred, RMDs at 73",
            "roth_ira": "After-tax contributions - tax-free growth and withdrawals, no RMDs",
            "taxable_accounts": "Brokerage accounts - no contribution limits, capital gains treatment",
        },
        "annuities": {
            "description": "Insurance products providing guaranteed lifetime income",
            "types": ["Fixed", "Variable", "Indexed", "Immediate", "Deferred"],
            "benefits": "Longevity protection, predictable income, optional death benefits",
            "reference": "See ANNUITY_EDUCATION for detailed information",
        },
    },
    "withdrawal_strategies": {
        "4_percent_rule": {
            "description": "Withdraw 4% of portfolio in year 1, adjust for inflation annually",
            "historical_success": "95% success rate over 30-year periods",
            "limitations": "Doesn't account for market volatility, fixed spending, or changing needs",
        },
        "bucket_strategy": {
            "description": "Divide portfolio into time-based buckets for withdrawals",
            "buckets": {
                "bucket_1": "0-2 years: Cash and short-term bonds (immediate needs)",
                "bucket_2": "3-10 years: Balanced portfolio (near-term needs)",
                "bucket_3": "10+ years: Growth investments (long-term growth)",
            },
            "benefits": "Reduces sequence of returns risk, provides peace of mind",
        },
        "dynamic_withdrawal": {
            "description": "Adjust withdrawals based on market performance and portfolio value",
            "benefits": "More sustainable, adapts to market conditions",
            "requires": "Flexibility in spending, active management",
        },
        "tax_efficient_order": {
            "recommended_sequence": [
                "1. RMDs from traditional accounts (required)",
                "2. Taxable account withdrawals (capital gains treatment)",
                "3. Tax-deferred accounts (traditional IRA/401k)",
                "4. Tax-free accounts (Roth) - save for last",
            ],
            "benefits": "Minimize lifetime tax burden, preserve Roth for legacy",
        },
    },
    "common_mistakes": [
        {
            "mistake": "Claiming Social Security too early",
            "impact": "25-30% permanent reduction in lifetime benefits",
            "solution": "Delay to FRA or age 70 if possible, use other assets first",
        },
        {
            "mistake": "Underestimating healthcare costs",
            "impact": "Fidelity estimates $315,000 for couple retiring at 65",
            "solution": "Plan for Medicare premiums, supplements, and out-of-pocket costs",
        },
        {
            "mistake": "Ignoring inflation",
            "impact": "3% inflation cuts purchasing power in half over 24 years",
            "solution": "Include growth investments, consider COLA annuities",
        },
        {
            "mistake": "No guaranteed income strategy",
            "impact": "Market volatility stress, uncertain monthly income",
            "solution": "Layer guaranteed income (SS + pension + annuity) to cover essentials",
        },
        {
            "mistake": "Inefficient tax planning",
            "impact": "Paying unnecessary taxes on withdrawals",
            "solution": "Strategic Roth conversions, tax-bracket management",
        },
    ],
    "qualification_questions": [
        {
            "question": "What's your current age or age range?",
            "purpose": "Tailor advice to life stage and time horizon",
            "scoring": "Older = higher urgency = higher score",
        },
        {
            "question": "When do you plan to retire?",
            "purpose": "Determine time horizon and planning urgency",
            "scoring": "Sooner retirement = higher priority = higher score",
        },
        {
            "question": "What are your current retirement savings?",
            "purpose": "Assess asset level and potential",
            "scoring": "Higher assets = higher value prospect = higher score",
        },
        {
            "question": "Do you currently have an annuity?",
            "purpose": "Understand existing guaranteed income and product knowledge",
            "scoring": "No annuity = sales opportunity = moderate score increase",
        },
        {
            "question": "What's your primary retirement concern?",
            "purpose": "Identify pain points and positioning for solutions",
            "options": [
                "Income stability",
                "Market risk",
                "Healthcare costs",
                "Legacy planning",
            ],
            "scoring": "Income/risk concerns = annuity opportunity = higher score",
        },
        {
            "question": "What are your retirement goals?",
            "purpose": "Understand lifestyle needs and required income",
            "options": [
                "Maintain lifestyle",
                "Travel",
                "Support family",
                "Charitable giving",
            ],
            "scoring": "Specific goals = engaged prospect = higher score",
        },
    ],
}


ANNUITY_EDUCATION = {
    "overview": {
        "definition": "An annuity is a contract with an insurance company that provides guaranteed income, typically for retirement.",
        "purpose": "Convert accumulated savings into reliable lifetime income, protecting against longevity risk",
        "best_for": "Individuals seeking guaranteed income, market protection, and peace of mind in retirement",
    },
    "types": {
        "fixed_annuity": {
            "description": "Provides guaranteed fixed interest rate for specific period",
            "how_it_works": "Insurance company guarantees principal and minimum interest rate",
            "pros": [
                "Stable, predictable returns",
                "No market risk - principal protected",
                "Guaranteed interest rate",
                "Simple to understand",
            ],
            "cons": [
                "Lower growth potential",
                "Interest rate risk",
                "Inflation risk",
                "Surrender charges if withdrawn early",
            ],
            "best_for": "Conservative investors wanting stability over growth",
        },
        "variable_annuity": {
            "description": "Allows investment in sub-accounts similar to mutual funds",
            "how_it_works": "Returns vary based on performance of chosen investments",
            "pros": [
                "Higher growth potential",
                "Investment flexibility and choices",
                "Optional death benefit guarantees",
                "Tax-deferred growth",
            ],
            "cons": [
                "Market risk - value can decrease",
                "Higher fees (M&E charges, investment fees, rider costs)",
                "Complex - many moving parts",
                "Surrender charges",
            ],
            "best_for": "Investors comfortable with market risk seeking growth potential",
        },
        "indexed_annuity": {
            "description": "Returns tied to market index (S&P 500) with downside protection",
            "how_it_works": "Earn interest based on index performance, with a floor (typically 0%)",
            "pros": [
                "Market participation with downside protection",
                "Principal protection - can't lose money",
                "Higher potential than fixed",
                "No direct market risk",
            ],
            "cons": [
                "Participation caps limit upside",
                "Complex crediting methods",
                "Longer surrender charge periods",
                "Not direct market participation",
            ],
            "best_for": "Balance-seekers wanting growth opportunity with principal protection",
        },
        "immediate_annuity": {
            "description": "Single premium payment, income starts immediately (within 1 year)",
            "how_it_works": "Exchange lump sum for guaranteed lifetime income stream",
            "pros": [
                "Immediate income - no waiting",
                "Highest income payout rates",
                "Simple and predictable",
                "Longevity protection",
            ],
            "cons": [
                "Irrevocable - limited liquidity",
                "No growth potential",
                "Death benefit may be limited",
                "Inflation risk",
            ],
            "best_for": "Retirees needing immediate guaranteed income",
        },
        "deferred_annuity": {
            "description": "Accumulation period before income starts (years in future)",
            "how_it_works": "Money grows tax-deferred, then converts to income later",
            "pros": [
                "Tax-deferred growth during accumulation",
                "Higher future income than immediate",
                "Flexibility in timing",
                "Death benefit during accumulation",
            ],
            "cons": [
                "Delayed income",
                "Surrender charges during accumulation",
                "Opportunity cost",
                "Must wait for payouts",
            ],
            "best_for": "Pre-retirees planning ahead (5-10+ years from retirement)",
        },
    },
    "key_features": {
        "guaranteed_lifetime_income": "Annuities can provide income for life, no matter how long you live",
        "tax_deferral": "Earnings grow tax-deferred until withdrawn (non-qualified annuities)",
        "death_benefits": "Optional riders to pass remaining value to beneficiaries",
        "living_benefits": "Riders for long-term care, terminal illness, or nursing home needs",
        "income_riders": "Guaranteed minimum income benefits regardless of account value",
    },
    "common_riders": {
        "GLWB": {
            "name": "Guaranteed Lifetime Withdrawal Benefit",
            "description": "Guarantees minimum annual withdrawal for life, even if account value reaches zero",
            "cost": "Typically 0.75% - 1.5% of benefit base annually",
            "benefit": "Income certainty with growth potential",
        },
        "GMIB": {
            "name": "Guaranteed Minimum Income Benefit",
            "description": "Guarantees minimum income when annuitizing in future",
            "cost": "Typically 0.50% - 1.0% annually",
            "benefit": "Protected income floor for future",
        },
        "GMDB": {
            "name": "Guaranteed Minimum Death Benefit",
            "description": "Guarantees minimum death benefit to beneficiaries",
            "cost": "Built into M&E charge or additional 0.15% - 0.50%",
            "benefit": "Legacy protection",
        },
        "LTC_rider": {
            "name": "Long-Term Care Rider",
            "description": "Increases income if you need long-term care",
            "cost": "0.50% - 1.50% annually",
            "benefit": "Doubles or triples income for care needs",
        },
    },
    "suitability_factors": [
        "Age (typically 50+ for most annuities)",
        "Retirement time horizon",
        "Other guaranteed income sources (SS, pension)",
        "Risk tolerance",
        "Liquidity needs",
        "Estate planning goals",
        "Tax situation",
    ],
    "common_objections": {
        "too_expensive": {
            "response": "Fees pay for guarantees. Compare cost of guarantee vs. market loss. Peace of mind has value. Many annuities have reasonable fees (1-2% total)."
        },
        "lose_control": {
            "response": "You don't lose control - you exchange uncertainty for certainty. Many annuities offer liquidity options (10% annual withdrawals). Riders provide flexibility."
        },
        "die_early_lose_money": {
            "response": "Death benefit riders protect heirs. Focus on income protection for life, not death. Can structure joint life options for spouse protection."
        },
        "too_complicated": {
            "response": "We'll simplify and explain every feature. Focus on your goals: guaranteed income. Complexity is in structure, simplicity in result: guaranteed paycheck."
        },
        "low_interest_rates": {
            "response": "Annuities still offer competitive rates vs. alternatives. Focus on guarantee value, not just rate. Indexed annuities offer growth potential."
        },
    },
}


def get_retirement_advice(age_range):
    """Get age-specific retirement planning advice"""
    age_mapping = {
        "20-30": "20s_30s",
        "31-50": "40s_50s",
        "51-65": "60s_plus",
        "65+": "60s_plus",
    }

    key = age_mapping.get(age_range, "40s_50s")
    return RETIREMENT_PLANNING["age_specific_guidance"].get(key, {})


def get_annuity_type_info(annuity_type):
    """Get detailed information about specific annuity type"""
    return ANNUITY_EDUCATION["types"].get(annuity_type, {})


def get_withdrawal_strategy(strategy_name):
    """Get information about retirement withdrawal strategy"""
    return RETIREMENT_PLANNING["withdrawal_strategies"].get(strategy_name, {})


if __name__ == "__main__":
    print("Retirement Planning Knowledge Base")
    print("=" * 60)
    print("\nAge Groups:", list(RETIREMENT_PLANNING["age_specific_guidance"].keys()))
    print("\nAnnuity Types:", list(ANNUITY_EDUCATION["types"].keys()))
    print(
        "\nWithdrawal Strategies:",
        list(RETIREMENT_PLANNING["withdrawal_strategies"].keys()),
    )
