"""Prompts to be used in AI services to get proper result or analysis"""

idea_enrichment_prompt = """Based on given product idea, enrich the original idea with strongly related information \
to return a full product proposal, proposal should be brief and within 200 words."""

eval_result_prompt = """For given product idea, analysis result and evaluation criteria, please check if analysis result \
can satisfy most evaluation criteria. Return True if analysis result can satisfy most criteria, otherwise return False.
"""

search_incumbents_prompt = """Based on given new product idea, search with Tavily for existing incumbents in market, \
summarize key information (like name, main products or features, recent business summary) of top players. Result should \
be brief and within 500 words.

Following is one example for product idea: whether Walmart should enter consumber banking.

Incumbents
Major Traditional Banks
    Traditional incumbents dominate with JPMorgan Chase ($3.64 T), Bank of America ($2.62 T), Citibank ($1.76 T), Wells Fargo ($1.71 T), \
    and U.S. Bank ($0.66 T) by assets as of March 31, 2025 US Bank Locations.
    These banks uniformly offer mobile and online banking, extensive ATM networks, branch access, checking/savings products, credit cards, \
    and P2P payments, but often lack specialized offerings for digital-native segments ConsumerAffairs.

Digital Challenger Banks
    Digital-first platforms such as Chime, Nubank, Monzo, and Revolut are rated among the top digital banking platforms for 2025, offering \
    fee-free checking, high-yield savings, early direct deposit, and real-time spending analytics SmartOSC.
    These challengers have lower overhead, highly optimized mobile experiences, and partnerships for ATM access, but have limited physical \
    presence and credit product breadth compared to incumbents SmartOSC.
"""

search_funding_prompt = """Based on given new product idea, search with Tavily for existing funding information in market for related products, \
summarize key funding information in recent market for related products. Result should be brief and within 500 words.

Following is one example for product idea: whether Walmart should enter consumber banking.

Funding Landscape

    Fintech startups globally raised $10.3 billion in Q1 2025, marking the highest quarterly funding since Q1 2023 TechCrunch.
    The Forbes Fintech 50 list features top-funded consumer and business fintechs, including Stripe ($6.5 B Series I in 2024), Brex ($300 M \
    Series D in 2025), and Chime ($750 M Series I) Forbes.
    Revli’s ranking highlights dozens of U.S. fintech startups that closed rounds over $50 million in 2025, underscoring continued investor \
    appetite revli.com.
    Fundraise Insider identifies recently funded consumer fintechs backed by top VCs like Sequoia, Accel, and Andreessen Horowitz Fundraise Insider.
"""

search_growth_prompt = """Based on given new product idea, search with Tavily for market growth information, summarize key information of \
recent market growth for related products. Result should be brief and within 500 words.

Following is one example for product idea: whether Walmart should enter consumber banking.

Market Growth

    The global consumer banking market was valued at $7.5 trillion in 2023 and is projected to reach $11.1 trillion by 2032, growing at a \
    4.5% CAGR DataIntelo.
    Grand View Research estimates the retail banking market at $2,039.25 billion in 2024, with a projection to $3,373.43 billion by 2033 at \
    a 5.8% CAGR Grand View Research.
    The Business Research Company reports a 6.7% CAGR from 2023 to 2024, forecasting $2,580.41 billion by 2028, driven by digital adoption \
    and regulatory shifts The Business Research Company.
"""

overall_analysis_prompt = """First use `calculate_overall_score` to calculate the overall score of idea, then based on overall score value and \
following judege rules and context to give final judgement:
    If overall score is higher than 0.6, should suggest moving forward with the idea, and return final suggestion with brief analysis based on \
    context (less then 100 words).
    If overall score is less than 0.6, should suggest not moving forward with idea, and return final suggestion with brief analysis based on \
    context (less then 100 words).

Following is an example of final judgement:

Go with differentiation. While the space is crowded with entrenched incumbents, strong funding trends and solid growth prospects (4~6% CAGR) \
indicate opportunities—especially if Walmart targets underserved segments (e.g., gig workers, digital-only consumers) and leverages partnerships \
to combine its brand and distribution with digital-first product innovation.
"""
