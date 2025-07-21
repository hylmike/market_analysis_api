"""API endpoints related to AI assistant services"""

from fastapi import APIRouter

from api.ai_assistant.schemas import ChatRequest
from api.ai_assistant.ai_assistant_services import (
    gen_market_analysis,
    gen_incumbent_analysis,
    gen_funding_analysis,
    gen_growth_analysis,
)

ai_assistant_router = APIRouter()


@ai_assistant_router.post("/market-analysis")
async def market_analysis(chat_input: ChatRequest):
    """Generate market analysis for user product idea, based on searched infomation from web"""
    analysis = await gen_market_analysis(chat_input.query)

    return {"analysis": analysis}


@ai_assistant_router.post("/incumbent-analysis")
async def incumbent_analysis(chat_input: ChatRequest):
    """Generate incumbent analysis for user product idea, based on searched infomation from web"""
    analysis = await gen_incumbent_analysis(chat_input.query)

    return {"analysis": analysis}


@ai_assistant_router.post("/funding-analysis")
async def funding_analysis(chat_input: ChatRequest):
    """Generate funding analysis for user product idea, based on searched infomation from web"""
    analysis = await gen_funding_analysis(chat_input.query)

    return {"analysis": analysis}


@ai_assistant_router.post("/growth-analysis")
async def growth_analysis(chat_input: ChatRequest):
    """Generate revenue growth analysis for related market space for user product idea, based on searched infomation from web"""
    analysis = await gen_growth_analysis(chat_input.query)

    return {"analysis": analysis}
