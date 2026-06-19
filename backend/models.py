from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    company: str
    file: str
    path: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]