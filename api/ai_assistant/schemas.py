"""AI assistant related schemas"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
