"""All agents and tools to support AI assistant services"""

import os
import json

from pydantic_ai import Agent, RunContext
from pydantic_ai.common_tools.tavily import tavily_search_tool

from api.ai_assistant.llm_prompts import (
    search_incumbents_prompt,
    eval_result_prompt,
    search_funding_prompt,
    search_growth_prompt,
    overall_analysis_prompt,
)
from api.utils.llm_gpt import GPTModel
from api.utils.logger import logger
from api.ai_assistant.schemas import (
    OverallAnalysisInput,
    FinalResult,
    IdeaScores,
)

tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError(
        "Not found Tavily API key in environment variables, please refer to env.example to config the API key"
    )

analysis_weights = {
    "incumbents_score": 0.4,
    "funding_score": 0.3,
    "growth_score": 0.3,
}

llm = GPTModel("gpt-4o-mini")
incumbents_analysis_agent = Agent(
    "openai:gpt-4o-mini",
    tools=[tavily_search_tool(tavily_api_key)],
    instructions=search_incumbents_prompt,
)
funding_analysis_agent = Agent(
    "openai:gpt-4o-mini",
    tools=[tavily_search_tool(tavily_api_key)],
    instructions=search_funding_prompt,
)
growth_analysis_agent = Agent(
    "openai:gpt-4o-mini",
    tools=[tavily_search_tool(tavily_api_key)],
    instructions=search_growth_prompt,
)


def evaluate_result(
    product_idea: str, analysis_result: str, evaluation_criteria: str
) -> bool:
    llm.set_system_message(eval_result_prompt)
    prompt = {
        "product_idea": product_idea,
        "analysis_result": analysis_result,
        "evaluation_criteria": evaluation_criteria,
    }
    result = llm.gen_completion(json.dumps(prompt))
    logger.info(f"Evaluation result is {result}")

    return result.lower() == "true"


async def search_incumbents(
    proposal: str,
) -> str:
    retry_times = 3
    eval_criteria = f"result shoud include key information of top players in the current market strongly related to given product idea: {proposal}"
    while retry_times:
        result = await incumbents_analysis_agent.run(proposal)
        if evaluate_result(
            product_idea=proposal,
            analysis_result=result.output,
            evaluation_criteria=eval_criteria,
        ):
            break
        retry_times -= 1
    logger.info(f"The final incumbents analysis result is:\n{result.output}\n")

    return result.output


async def search_funding(proposal: str) -> str:
    retry_times = 3
    eval_criteria = f"result shoud include funding information of key players in the current market strongly related to given product idea: {proposal}"
    while retry_times:
        result = await funding_analysis_agent.run(proposal)
        if evaluate_result(
            product_idea=proposal,
            analysis_result=result.output,
            evaluation_criteria=eval_criteria,
        ):
            break
        retry_times -= 1
    logger.info(f"The final funding analysis result is:\n{result.output}\n")

    return result.output


async def search_growth(proposal: str) -> str:
    retry_times = 3
    eval_criteria = f"result shoud include market capacity and revenue growth analysis in the current market strongly related to given product idea: {proposal}"
    while retry_times:
        result = await growth_analysis_agent.run(proposal)
        if evaluate_result(
            product_idea=proposal,
            analysis_result=result.output,
            evaluation_criteria=eval_criteria,
        ):
            break
        retry_times -= 1
    logger.info(f"The final growth analysis result is:\n{result.output}\n")

    return result.output


score_analysis_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=IdeaScores,
)


async def gen_analysis_scores(
    idea: str,
    incumbents_analysis: str,
    funding_analysis: str,
    growth_analysis: str,
) -> IdeaScores:
    prompt = f"""Based on following idea and three analysis:
idea: {idea}
incumbents_analysis: {incumbents_analysis}
funding_analysis: {funding_analysis}
growth_analysis: {growth_analysis}

generate score for each analysis and return all scores with following json format:
    {{incumbents_score: float, funding_score: float, growth_score: float }}

Following are instructure for generate score for analysis:
- For incumbents analysis, less should give higher score, 0 incumbent should give 1 and more than 10 incumbent should give less than 0.3
- For funding analysis, more funding should give higher score, overall more than 100B should give 1 and less than 1B should give less than 0.3
- For growth analysis, higher market growth should give higher score, growth rate more than 100 percent should give 1 and less than 10 percent should tive less than 0.3
"""
    result = await score_analysis_agent.run(prompt)
    return result.output


overall_analysis_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=OverallAnalysisInput,
    output_type=FinalResult,
    system_prompt=overall_analysis_prompt,
)


@overall_analysis_agent.system_prompt
def gen_system_prompt(ctx: RunContext[OverallAnalysisInput]) -> str:
    return f"""context:
incumbents_analysis: {ctx.deps.incumbents_analysis}
funding_analysis: {ctx.deps.funding_analysis}
growth_analysis: {ctx.deps.growth_analysis}
"""


@overall_analysis_agent.tool
def calculate_overall_score(ctx: RunContext[OverallAnalysisInput]):
    """With given scores for each analysis, calculate the overall score"""
    scores = ctx.deps.scores
    overall_score = (
        scores.incumbents_score * analysis_weights["incumbents_score"]
        + scores.funding_score * analysis_weights["funding_score"]
        + scores.growth_score * analysis_weights["growth_score"]
    )
    logger.info(f"Overall score is {overall_score:.2f}")
    return overall_score


async def gen_overall_analysis(
    incumbents_analysis: str,
    funding_analysis: str,
    growth_analysis: str,
    scores: IdeaScores,
):
    deps = OverallAnalysisInput(
        incumbents_analysis=incumbents_analysis,
        funding_analysis=funding_analysis,
        growth_analysis=growth_analysis,
        scores=scores,
    )
    result = await overall_analysis_agent.run(
        "With the given inputs, return the final result",
        deps=deps,
    )

    return result.output
