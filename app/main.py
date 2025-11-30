from fastapi import FastAPI, HTTPException
from app.models import ChatRequest, AgentResponse
from app.agent.core import AgentCore
import uvicorn

app = FastAPI(title="Relationship Manager Co-Pilot")
agent = AgentCore()

@app.post("/chat", response_model=AgentResponse)
async def chat(request: ChatRequest):
    try:
        response = agent.run(request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
