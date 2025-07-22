"""All servives to support AI assistant endpoints"""

import asyncio

from api.utils.llm_gpt import GPTModel
from api.ai_assistant.llm_prompts import idea_enrichment_prompt
from api.utils.logger import logger
from api.ai_assistant.agents import (
    search_incumbents,
    search_funding,
    search_growth,
    gen_analysis_scores,
    gen_overall_analysis,
)


def query_analysis(query: str) -> str:
    llm = GPTModel("gpt-4o-mini")
    llm.set_system_message(idea_enrichment_prompt)
    enriched_proposal = llm.gen_completion(query)
    logger.info(f"The enriched proposal:\n {enriched_proposal}\n")
    return enriched_proposal


async def gen_market_analysis(query: str):
    proposal = query_analysis(query)
    results = await asyncio.gather(
        search_incumbents(proposal),
        search_funding(proposal),
        search_growth(proposal),
    )
    [incumbent_analysis, funding_analysis, growth_analysis] = results

    scores = await gen_analysis_scores(
        idea=query,
        incumbents_analysis=incumbent_analysis,
        funding_analysis=funding_analysis,
        growth_analysis=growth_analysis,
    )
    logger.info(f"Idea analysis scores:\n{scores}")

    overall_analysis = await gen_overall_analysis(
        incumbents_analysis=incumbent_analysis,
        funding_analysis=funding_analysis,
        growth_analysis=growth_analysis,
        scores=scores,
    )

    analysis_scores = {
        "incumbents": scores.incumbents_score,
        "funding": scores.funding_score,
        "growth": scores.growth_score,
        "overall": round(overall_analysis.overall_score, 2),
    }

    return {
        "incumbents_analysis": incumbent_analysis,
        "funding_analysis": funding_analysis,
        "growth_analysis": growth_analysis,
        "scores": analysis_scores,
        "final_judgement": overall_analysis.final_judgement,
    }


async def gen_incumbent_analysis(query: str):
    proposal = query_analysis(query)
    analysis = await search_incumbents(proposal)

    return analysis


async def gen_funding_analysis(query: str):
    proposal = query_analysis(query)
    analysis = await search_funding(proposal)

    return analysis


async def gen_growth_analysis(query: str):
    proposal = query_analysis(query)
    analysis = await search_growth(proposal)

    return analysis
