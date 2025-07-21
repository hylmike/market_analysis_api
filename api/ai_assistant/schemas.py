"""AI assistant related schemas"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class IdeaScores(BaseModel):
    incumbents_score: float
    funding_score: float
    growth_score: float


class OverallAnalysisInput(BaseModel):
    incumbents_analysis: str
    funding_analysis: str
    growth_analysis: str
    scores: IdeaScores


class FinalResult(BaseModel):
    incumbents_analysis: str
    funding_analysis: str
    growth_analysis: str
    overall_score: float
    final_judgement: str
