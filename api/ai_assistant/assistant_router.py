"""API endpoints related to AI assistant services"""

from fastapi import APIRouter

from api.ai_assistant.schemas import ChatRequest
from api.ai_assistant.agents import gen_market_analysis

ai_assistant_router = APIRouter()


@ai_assistant_router.post("/market-analysis")
async def chat_completion(chat_input: ChatRequest):
    """Generate AI completion for user question. combine info from chat history and knowledge base"""
    market_analysis = await gen_market_analysis(chat_input.query)

    return {"analysis": market_analysis}
