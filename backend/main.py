from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from agents.mentor_agent import mentor_reply
from agents.tool_agent import calculate_emission
from agents.observability_agent import log_event
from agents.memory_agent import weekly_summary
from agents.metrics_agent import get_metrics

app = FastAPI(title="EcoMentor API")


class ChatQuery(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class EmissionRequest(BaseModel):
    category: str
    value: float


class LogData(BaseModel):
    event: str
    details: dict | None = None


@app.get("/")
def home():
    return {"status": "EcoMentor backend active"}


@app.post("/chat")
def chat_endpoint(data: ChatQuery):
    sid = data.session_id or "default"
    reply = mentor_reply(data.message, sid)
    return {"agent": "mentor", "session_id": sid, "response": reply}


@app.post("/calculate")
def calc_endpoint(data: EmissionRequest):
    result = calculate_emission(data.category, data.value)
    return {"agent": "tool", "result": result}


@app.post("/log")
def log_endpoint(data: LogData):
    log_event(data.event, data.details)
    return {"status": "logged"}


@app.get("/weekly_summary")
def weekly_summary_endpoint(session_id: str = "default"):
    summary = weekly_summary(session_id)
    return {"session_id": session_id, "weekly_summary": summary}



@app.get("/metrics")
def metrics_endpoint():
    return {"metrics": get_metrics()}
