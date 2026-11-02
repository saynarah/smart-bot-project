import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langsmith import tracing_context

from .smart_bot_project import SmartQABot, QAResponse

app = FastAPI(title="Smart Q&A Fitness & Wellness Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

class ChatRequest(BaseModel):
    question: str


bot = SmartQABot()

@app.post("/chat", response_model=QAResponse)
def chat(request: ChatRequest):
    with tracing_context(
        enabled=True,
        project_name="Smart Q&A Bot Project",
        tags=["fastapi", "smart-qa-bot"]
    ):

        return bot.ask(request.question)
