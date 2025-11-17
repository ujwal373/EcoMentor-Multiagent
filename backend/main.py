from fastapi import FastAPI
from pydantic import BaseModel
from agents.mentor_agent import mentor_reply
from agents.tool_agent import calculate_emission
from agents.observability_agent import log_event

app = FastAPI(title="EcoMentor API")

# ---------- Models ----------
class ChatQuery(BaseModel):
    message: str

class EmissionRequest(BaseModel):
    category: str
    value: float

class LogData(BaseModel):
    event: str
    details: dict | None = None


# ---------- Routes ----------
@app.get("/")
def home():
    return {"status": "EcoMentor backend active"}

@app.post("/chat")
def chat_endpoint(data: ChatQuery):
    reply = mentor_reply(data.message)
    return {"agent": "mentor", "response": reply}

@app.post("/calculate")
def calc_endpoint(data: EmissionRequest):
    result = calculate_emission(data.category, data.value)
    return {"agent": "tool", "result": result}

@app.post("/log")
def log_endpoint(data: LogData):
    log_event(data.event, data.details)
    return {"status": "logged"}
